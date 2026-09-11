#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PROJECT_ROOT}/.venv/bin/python"
COMFY_ROOT="${PROJECT_ROOT}/apps/comfy/ComfyUI"
MODEL_CONFIG="${PROJECT_ROOT}/configs/comfy.extra_model_paths.yaml"

# Checking for the presence of a Python environment.
if [[ ! -x "${PYTHON}" ]]; then
    echo "❌ Python environment not found: ${PYTHON}" >&2
    echo "💡 Run: uv sync" >&2
    exit 1
fi

# Checking ComfyUI initialization.
if [[ ! -f "${COMFY_ROOT}/main.py" ]]; then
    echo "❌ ComfyUI is not initialized: ${COMFY_ROOT}" >&2
    echo "💡 Run: git submodule update --init --recursive" >&2
    exit 1
fi

# Checking for the presence of the ComfyUI-GGUF custom node.
if [[ ! -d "${COMFY_ROOT}/custom_nodes/ComfyUI-GGUF" ]]; then
    echo "❌ ComfyUI-GGUF custom node not found" >&2
    echo "💡 Run: cd apps/comfy/ComfyUI/custom_nodes && git clone https://github.com/city96/ComfyUI-GGUF.git" >&2
    exit 1
fi

# Checking for the presence of the model paths configuration.
if [[ ! -f "${MODEL_CONFIG}" ]]; then
    echo "❌ Model paths config not found: ${MODEL_CONFIG}" >&2
    echo "💡 Create configs/comfy.extra_model_paths.yaml" >&2
    exit 1
fi

# CUDA check (do not interrupt operation, but issue a warning).
if ! "${PYTHON}" -c 'import torch; raise SystemExit(0 if torch.cuda.is_available() else 1)' 2>/dev/null; then
    echo "⚠️  Warning: PyTorch cannot access CUDA. GPU generation will fail." >&2
fi

echo "🚀 Starting ComfyUI with --lowvram for ~5GB VRAM budget (§1.2)..."
exec "${PYTHON}" "${COMFY_ROOT}/main.py" \
    --listen 127.0.0.1 \
    --port 8188 \
    --disable-auto-launch \
    --lowvram \
    --extra-model-paths-config "${MODEL_CONFIG}" \
    "$@"