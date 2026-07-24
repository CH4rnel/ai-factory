# AI Media Factory

Local-first production pipeline for AI-generated images, voice, subtitles,
video assembly, and automated publishing.

## Current milestone

Milestone 2 integrates ComfyUI as the local image-generation engine. See
[`apps/comfy/README.md`](apps/comfy/README.md) for installation, model layout,
startup, and troubleshooting instructions.

## Requirements

- Arch Linux or another modern Linux distribution;
- Python 3.12;
- NVIDIA GPU with a compatible driver;
- CUDA-enabled PyTorch;
- Git with submodule support.

## Quick start

```bash
git clone --recurse-submodules <repository-url>
cd ai-factory
pyenv local 3.12.11
python -m venv .venv
.venv/bin/python -m pip install -r apps/comfy/ComfyUI/requirements.txt
./scripts/comfy.sh
```

ComfyUI listens only on <http://127.0.0.1:8188> by default.

## Repository policy

Source code, configuration, prompts, and reusable workflows are versioned.
Large models, caches, virtual environments, and generated media remain local
and are excluded from Git.
