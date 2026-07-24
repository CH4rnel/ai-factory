# ComfyUI engine

ComfyUI is included as a Git submodule in `apps/comfy/ComfyUI`. The project
wrapper keeps application code separate from downloaded models and generated
media.

## Initial setup

From the repository root:

```bash
git submodule update --init --recursive
.venv/bin/python -m pip install -r apps/comfy/ComfyUI/requirements.txt
```

The project expects Python 3.12 and a CUDA-enabled PyTorch installation.

## Start

```bash
./scripts/comfy.sh
```

Open <http://127.0.0.1:8188> after the server starts. Extra arguments are
forwarded to ComfyUI:

```bash
./scripts/comfy.sh --verbose DEBUG
```

The default launcher is intentionally bound to localhost. Do not bind ComfyUI
to `0.0.0.0` unless access is protected by a firewall or reverse proxy.

## Model layout

Shared models live outside the ComfyUI submodule:

```text
models/
├── checkpoints/
├── clip/
├── clip_vision/
├── controlnet/
├── diffusion_models/
├── embeddings/
├── flux/
├── loras/
├── text_encoders/
├── upscale_models/
└── vae/
```

The mapping is defined in `configs/comfy.extra_model_paths.yaml`. Model files
are local runtime assets and must not be committed to Git.

## RTX 2060 profile

The launcher uses the conservative profile intended for 6 GB VRAM:

- text encoders are offloaded to system RAM;
- dynamic VRAM mode is disabled so `--lowvram` is effective;
- 0.5 GB VRAM is reserved for the desktop and display server;
- browser auto-launch is disabled.

If an inference still runs out of memory, close other GPU applications and try
`./scripts/comfy.sh --novram` instead. `--novram` is slower because it performs
more aggressive CPU offloading.

## Verification

Check the environment:

```bash
.venv/bin/python -c "import torch; print(torch.cuda.is_available())"
```

Expected result on the host is `True`. A container or sandbox may return
`False` even when the host driver works.
