# Voltron Braneworld Model - Aura Research Project Core

Voltron is the NeuroMindModel BrainWorld layer for the Aura research ecosystem. It combines the existing higher-dimensional braneworld research with a ComfyUI ControlNet -> LoRA exporter and an AuraXLSL workbook model.

## Namespace

neuromindmodel/braneworld

## AuraXLSL model

The workbook layer is declarative: Observe -> Encode -> Retrieve -> Reason -> Plan -> Execute -> Store.

Core concepts:

- Cortex - reasoning and planning
- Synapse - adapter and LoRA operations
- Memory - persistent state and knowledge interfaces
- Vision - perceptual conditioning
- WorldModel - environment and state simulation

The canonical workbook concepts are documented in workbook/Aura.xlsl.md and Voltron_spec.md.

## ComfyUI

control_voltron.py exposes the node category neuromindmodel/braneworld and converts compatible ControlNet/model weight deltas into rank-reduced LoRA tensors using SVD.

## Repository

This repository retains the existing Aura .xlsl, .xsim, Nim, simulation, telemetry, and research assets. The Braneworld runtime layer extends those assets rather than replacing them.
