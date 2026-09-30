import importlib

node_list = [
    "control_voltron_create",
    "control_voltron",
    "color_blend",
    "image_nodes",
]

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for module_name in node_list:
    try:
        imported_module = importlib.import_module(f".{module_name}", __name__)
    except ModuleNotFoundError:
        continue
    NODE_CLASS_MAPPINGS.update(getattr(imported_module, "NODE_CLASS_MAPPINGS", {}))
    NODE_DISPLAY_NAME_MAPPINGS.update(getattr(imported_module, "NODE_DISPLAY_NAME_MAPPINGS", {}))

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
