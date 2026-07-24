#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PROJECT_ROOT}/.venv/bin/python"
COMFY_ROOT="${PROJECT_ROOT}/apps/comfy/ComfyUI"
MODEL_CONFIG="${PROJECT_ROOT}/configs/comfy.extra_model_paths.yaml"

if [[ ! -x "${PYTHON}" ]]; then
    echo "Python environment not found: ${PYTHON}" >&2
    echo "Create the project virtual environment before starting ComfyUI." >&2
    exit 1
fi

if [[ ! -f "${COMFY_ROOT}/main.py" ]]; then
    echo "ComfyUI is not initialized: ${COMFY_ROOT}" >&2
    echo "Run: git submodule update --init --recursive" >&2
    exit 1
fi

if ! "${PYTHON}" -c 'import torch; raise SystemExit(0 if torch.cuda.is_available() else 1)'; then
    echo "Warning: PyTorch cannot currently access CUDA." >&2
    echo "ComfyUI will start, but GPU generation will not work until CUDA is available." >&2
fi

exec "${PYTHON}" "${COMFY_ROOT}/main.py" \
    --listen 127.0.0.1 \
    --port 8188 \
    --disable-auto-launch \
    --reserve-vram 0.5 \
    --extra-model-paths-config "${MODEL_CONFIG}" \
    "$@"
