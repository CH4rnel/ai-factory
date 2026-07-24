#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
MODEL_DIR="${PROJECT_ROOT}/models/checkpoints"
MODEL_PATH="${MODEL_DIR}/flux1-schnell-fp8.safetensors"
MODEL_URL="https://huggingface.co/Comfy-Org/flux1-schnell/resolve/main/flux1-schnell-fp8.safetensors?download=true"
EXPECTED_SIZE=17236328572

mkdir -p "${MODEL_DIR}"

if [[ -f "${MODEL_PATH}" ]] && [[ "$(stat -c %s "${MODEL_PATH}")" -eq "${EXPECTED_SIZE}" ]]; then
    echo "FLUX.1 Schnell FP8 is already installed: ${MODEL_PATH}"
    exit 0
fi

echo "Downloading FLUX.1 Schnell FP8 (approximately 17.2 GB)..."
curl \
    --location \
    --fail \
    --retry 5 \
    --retry-delay 5 \
    --continue-at - \
    --output "${MODEL_PATH}" \
    "${MODEL_URL}"

ACTUAL_SIZE="$(stat -c %s "${MODEL_PATH}")"
if [[ "${ACTUAL_SIZE}" -ne "${EXPECTED_SIZE}" ]]; then
    echo "Unexpected model size: ${ACTUAL_SIZE} bytes; expected ${EXPECTED_SIZE}." >&2
    echo "The partial file was preserved so the next run can resume it." >&2
    exit 1
fi

echo "FLUX.1 Schnell FP8 installed: ${MODEL_PATH}"
