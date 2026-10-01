# Voltron Braneworld Model — Aura Research Project Core

Voltron is the NeuroMindModel BrainWorld layer for the Aura research ecosystem. It combines the existing higher-dimensional research assets with an AuraXLSL workbook architecture, a Python cognitive engine, Scheme kernel primitives, AI adapters, a Rust runtime, and the ComfyUI ControlNet → LoRA integration.

## Namespace

neuromindmodel/braneworld

## Cognitive pipeline

Observe → Encode → Retrieve → Reason → Plan → Execute → Store

## Repository architecture

- workbook/ — AuraXLSL declarative workbooks for Braneworld, Cortex, Memory, Synapse, Vision, Audio, Robotics, and WorldModel.
- braneworld/ — Python cognitive runtime: perception, tokenization, cortex, memory, reasoning, planning, and orchestration.
- kernels/ — Scheme-style kernel, scheduler, router, and workbook primitives.
- ai/ — lightweight model-facing adapters for transformers, diffusion, ControlNet, LoRA, and embeddings.
- runtime/ — Rust tensor, memory, graph, and Braneworld runtime structures.
- datasets/ — dataset manifests and adapters; raw datasets stay external.
- checkpoints/ — checkpoint manifests; large model weights stay external.
- workflows/ — reusable workflow specifications.
- docs/ — architecture and research documentation.
- assets/ — diagrams, workbook visualizations, and generated research assets.
- .github/ — repository validation automation.

## Workbook model

The workbooks are executable specifications for the runtime rather than static documentation. Braneworld.workbook.xlsl composes the cognitive modules and declares the canonical state transition:

Observe → Encode → Retrieve → Reason → Plan → Execute → Store

The domain workbooks define the contracts for Cortex, Memory, Synapse, Vision, Audio, Robotics, and WorldModel.

## Python runtime

braneworld.engine.BraneworldEngine provides the reference orchestration path:

1. Perception normalizes multimodal input.
2. Tokenization creates searchable symbolic units.
3. Hippocampus retrieval supplies prior context.
4. Cortex combines observation and memory.
5. Reasoner produces hypotheses.
6. Planner turns hypotheses into bounded actions.
7. The executor dispatches registered tools.
8. Memory stores the resulting episode.

## AI integration

control_voltron.py remains the ComfyUI integration surface under neuromindmodel/braneworld. It performs rank-reduced ControlNet/model-delta → LoRA extraction with SVD and quantile clamping.

The new ai/ modules provide dependency-light contracts around embeddings, LoRA tensor shapes, diffusion schedules, ControlNet signals, and transformer configuration. Heavy model dependencies remain optional.

## Rust runtime

The runtime/ crate provides small, dependency-light primitives for tensors, bounded memory, graph connectivity, and the Braneworld runtime state. It can evolve independently of the Python reference engine.

## Validation

Python source is compiled and tested by .github/workflows/validate-braneworld.yml. The workflow also runs cargo check for the Rust runtime.

Existing Aura .xlsl, .xsim, Nim, simulation, telemetry, and research assets are preserved. This layer extends the merged Voltron architecture without replacing the existing research surface.
