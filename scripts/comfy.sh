#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
# We use the Python from the uv environment.
PYTHON="${PROJECT_ROOT}/.venv/bin/python"
COMFY_ROOT="${PROJECT_ROOT}/apps/comfy/ComfyUI"
MODEL_CONFIG="${PROJECT_ROOT}/configs/comfy.extra_model_paths.yaml"

if [[ ! -x "${PYTHON}" ]]; then
    echo "❌ Python environment not found: ${PYTHON}" >&2
    echo "💡 Run: uv sync" >&2
    exit 1
fi

if [[ ! -f "${COMFY_ROOT}/main.py" ]]; then
    echo "❌ ComfyUI is not initialized: ${COMFY_ROOT}" >&2
    echo "💡 Run: git submodule update --init --recursive" >&2
    exit 1
fi

# CUDA check (do not interrupt operation, but issue a warning)
if ! "${PYTHON}" -c 'import torch; raise SystemExit(0 if torch.cuda.is_available() else 1)' 2>/dev/null; then
    echo "⚠️ Warning: PyTorch cannot currently access CUDA. GPU generation will be slow or fail." >&2
fi

echo "🚀 Starting ComfyUI with low-VRAM optimizations for ~5GB budget..."
exec "${PYTHON}" "${COMFY_ROOT}/main.py" \
    --listen 127.0.0.1 \
    --port 8188 \
    --disable-auto-launch \
    --lowvram \
    --extra-model-paths-config "${MODEL_CONFIG}" \
    "$@"