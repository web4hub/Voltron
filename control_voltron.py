import os
import torch

import comfy.model_management
import comfy.utils
import folder_paths

CATEGORY = "neuromindmodel/braneworld"
CLAMP_QUANTILE = 0.99


def extract_lora(weight_diff: torch.Tensor, rank: int):
    """
    Convert a ControlNet weight delta into LoRA up/down tensors using SVD.
    Supports Linear, Conv1x1 and Conv3x3 layers.
    """

    conv2d = weight_diff.ndim == 4
    kernel = weight_diff.shape[2:] if conv2d else None
    is_conv3 = conv2d and kernel != (1, 1)

    out_dim, in_dim = weight_diff.shape[:2]
    rank = min(rank, out_dim, in_dim)

    matrix = weight_diff.float()

    if conv2d:
        matrix = matrix.flatten(1) if is_conv3 else matrix.squeeze()

    U, S, Vh = torch.linalg.svd(matrix, full_matrices=False)

    U = U[:, :rank] @ torch.diag(S[:rank])
    Vh = Vh[:rank]

    values = torch.cat((U.flatten(), Vh.flatten()))
    clamp = torch.quantile(values.abs(), CLAMP_QUANTILE)

    U = U.clamp(-clamp, clamp)
    Vh = Vh.clamp(-clamp, clamp)

    if conv2d:
        U = U.reshape(out_dim, rank, 1, 1)
        Vh = Vh.reshape(rank, in_dim, *kernel)

    return U, Vh


class ControlVoltronSave:
    """
    Save a ControlNet as a compressed Voltron LoRA (.safetensors)
    """

    CATEGORY = CATEGORY
    RETURN_TYPES = ()
    FUNCTION = "save"
    OUTPUT_NODE = True

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "control_net": ("CONTROL_NET",),
                "filename_prefix": (
                    "STRING",
                    {
                        "default": "neuromindmodel/braneworld/voltron"
                    },
                ),
                "rank": (
                    "INT",
                    {
                        "default": 64,
                        "min": 4,
                        "max": 1024,
                        "step": 4,
                    },
                ),
            }
        }

    def save(self, model, control_net, filename_prefix, rank):

        (
            output_folder,
            filename,
            counter,
            _subfolder,
            _prefix,
        ) = folder_paths.get_save_image_path(
            filename_prefix,
            self.output_dir,
        )

        comfy.model_management.load_models_gpu([model])

        model_state = model.model_state_dict()
        control_state = control_net.control_model.state_dict()

        output_state = {}
        stored = set()

        prefix = "diffusion_model."

        print("🧠 Voltron: Extracting ControlNet LoRA...")

        for key, model_weight in model_state.items():

            if not key.startswith(prefix):
                continue

            control_key = key[len(prefix):]

            if control_key not in control_state:
                control_key = f"control_model.{control_key}"

            if control_key not in control_state:
                continue

            control_weight = control_state[control_key]

            if model_weight.ndim >= 2:

                diff = (
                    control_weight.float().to(model_weight.device)
                    - model_weight.float()
                )

                up, down = extract_lora(diff, rank)

                name = control_key.removesuffix(".weight")

                output_state[f"{name}.up"] = (
                    up.detach()
                    .contiguous()
                    .half()
                    .cpu()
                )

                output_state[f"{name}.down"] = (
                    down.detach()
                    .contiguous()
                    .half()
                    .cpu()
                )

            else:
                output_state[control_key] = (
                    control_weight.detach().half().cpu()
                )

            stored.add(control_key)

        for key, tensor in control_state.items():
            if key not in stored:
                output_state[key] = tensor.detach().half().cpu()

        output_state["lora_controlnet"] = torch.empty(0)

        save_file = os.path.join(
            output_folder,
            f"{filename}_{counter:05d}.safetensors",
        )

        metadata = {
            "format": "Voltron-Control-LoRA",
            "framework": "NeuroMindModel",
            "category": CATEGORY,
            "rank": str(rank),
            "quantile_clamp": str(CLAMP_QUANTILE),
            "author": "Web4Hub / NeuroMindModel",
        }

        comfy.utils.save_torch_file(
            output_state,
            save_file,
            metadata=metadata,
        )

        print(f"✅ Voltron saved: {save_file}")

        return {}


NODE_CLASS_MAPPINGS = {
    "ControlVoltronSave": ControlVoltronSave,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ControlVoltronSave": "🧠 Voltron • ControlNet → LoRA Saver",
}
