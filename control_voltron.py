import os
import torch
import comfy.model_management
import comfy.utils
import folder_paths

CATEGORY = "neuromindmodel/braneworld"
CLAMP_QUANTILE = 0.99


def extract_lora(weight_diff: torch.Tensor, rank: int):
    if weight_diff.ndim < 2:
        raise ValueError("LoRA extraction requires a tensor with at least two dimensions")
    conv2d = weight_diff.ndim == 4
    kernel = tuple(weight_diff.shape[2:]) if conv2d else None
    out_dim, in_dim = weight_diff.shape[:2]
    rank = min(int(rank), out_dim, in_dim)
    if rank < 1:
        raise ValueError("rank must be at least 1")
    matrix = weight_diff.float()
    if conv2d:
        matrix = matrix.flatten(1) if kernel != (1, 1) else matrix.squeeze()
    if matrix.ndim != 2:
        raise ValueError(f"Unsupported weight shape: {tuple(weight_diff.shape)}")
    u, s, vh = torch.linalg.svd(matrix, full_matrices=False)
    u = u[:, :rank] @ torch.diag(s[:rank])
    vh = vh[:rank]
    values = torch.cat((u.flatten(), vh.flatten())).abs()
    clamp = torch.quantile(values, CLAMP_QUANTILE)
    if torch.isfinite(clamp) and clamp > 0:
        u = u.clamp(-clamp, clamp)
        vh = vh.clamp(-clamp, clamp)
    if conv2d:
        u = u.reshape(out_dim, rank, 1, 1)
        vh = vh.reshape(rank, in_dim, *kernel)
    return u, vh


class ControlVoltronSave:
    CATEGORY = CATEGORY
    RETURN_TYPES = ()
    FUNCTION = "save"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "model": ("MODEL",),
            "control_net": ("CONTROL_NET",),
            "filename_prefix": ("STRING", {"default": "voltron/braneworld"}),
            "rank": ("INT", {"default": 64, "min": 1, "max": 1024, "step": 1}),
        }}

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    def save(self, model, control_net, filename_prefix, rank):
        output_folder, filename, counter, _, _ = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        comfy.model_management.load_models_gpu([model])
        model_state = model.model_state_dict()
        control_state = control_net.control_model.state_dict()
        output_state, stored = {}, set()
        prefix = "diffusion_model."
        for key, model_weight in model_state.items():
            if not key.startswith(prefix):
                continue
            control_key = key[len(prefix):]
            if control_key not in control_state:
                control_key = f"control_model.{control_key}"
            if control_key not in control_state:
                continue
            control_weight = control_state[control_key]
            if model_weight.ndim >= 2 and control_weight.shape == model_weight.shape:
                diff = control_weight.float().to(model_weight.device) - model_weight.float()
                up, down = extract_lora(diff, rank)
                name = control_key[:-7] if control_key.endswith(".weight") else control_key
                output_state[f"{name}.up"] = up.detach().contiguous().half().cpu()
                output_state[f"{name}.down"] = down.detach().contiguous().half().cpu()
            else:
                output_state[control_key] = control_weight.detach().half().cpu()
            stored.add(control_key)
        for key, tensor in control_state.items():
            if key not in stored:
                output_state[key] = tensor.detach().half().cpu()
        output_state["lora_controlnet"] = torch.empty(0)
        save_path = os.path.join(output_folder, f"{filename}_{counter:05d}.safetensors")
        comfy.utils.save_torch_file(output_state, save_path, metadata={
            "format": "Voltron-Control-LoRA",
            "framework": "NeuroMindModel",
            "namespace": CATEGORY,
            "rank": str(rank),
            "clamp_quantile": str(CLAMP_QUANTILE),
            "workbook": "Aura.xlsl / Braneworld",
        })
        print(f"[Voltron] saved {save_path}")
        return {}


NODE_CLASS_MAPPINGS = {"ControlVoltronSave": ControlVoltronSave}
NODE_DISPLAY_NAME_MAPPINGS = {"ControlVoltronSave": "Voltron - ControlNet -> LoRA Saver"}
