# Voltron Braneworld Architecture

Voltron is organized as a layered NeuroMindModel runtime.

- workbook/ — AuraXLSL declarative cognitive specifications.
- braneworld/ — Python orchestration and cognitive primitives.
- kernels/ — Scheme-style runtime primitives and routing.
- ai/ — model-facing adapters for embeddings, diffusion, ControlNet, LoRA, and transformer configuration.
- runtime/ — dependency-light Rust structures for tensors, memory, graphs, and runtime state.
- datasets/ — external dataset manifests.
- checkpoints/ — external model-weight manifests.
- workflows/ — reusable execution descriptions.

The canonical cognitive flow is:

Observe → Encode → Retrieve → Reason → Plan → Execute → Store

The existing control_voltron.py ComfyUI node remains the model-delta/ControlNet → LoRA integration surface under neuromindmodel/braneworld.
