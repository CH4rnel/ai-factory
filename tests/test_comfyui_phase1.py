# Tests for ComfyUI Integration
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests


# ComfyUI Base URL
COMFYUI_URL = "http://127.0.0.1:8188"


def test_comfyui_submodule_exists():
    # Checks that the ComfyUI submodule is initialized.
    comfy_root = Path(__file__).parent.parent / "apps" / "comfy" / "ComfyUI"
    assert comfy_root.exists(), "ComfyUI submodule not found"
    assert (comfy_root / "main.py").exists(), "ComfyUI main.py not found"


def test_comfyui_gguf_node_exists():
    # Checks that the ComfyUI-GGUF custom node is installed.
    gguf_node = Path(__file__).parent.parent / "apps" / "comfy" / "ComfyUI" / "custom_nodes" / "ComfyUI-GGUF"
    assert gguf_node.exists(), "ComfyUI-GGUF custom node not found"
    assert (gguf_node / "__init__.py").exists(), "ComfyUI-GGUF __init__.py not found"


def test_extra_model_paths_config_exists():
    # Verifies that the extra_model_paths.yaml configuration has been created.
    config_path = Path(__file__).parent.parent / "configs" / "comfy.extra_model_paths.yaml"
    assert config_path.exists(), "configs/comfy.extra_model_paths.yaml not found"


def test_models_directory_structure():
    # Checks the directory structure for models.
    models_root = Path(__file__).parent.parent / "models"
    assert models_root.exists(), "models/ directory not found"
    
    # Checking subdirectories for FLUX.
    assert (models_root / "flux" / "unet").exists(), "models/flux/unet not found"
    assert (models_root / "flux" / "clip").exists(), "models/flux/clip not found"
    assert (models_root / "flux" / "vae").exists(), "models/flux/vae not found"


@pytest.mark.skip(reason="Requires ComfyUI server running")
def test_comfyui_health_check():
    # Checks the health check endpoint.
    # This test requires a running ComfyUI server.
    try:
        response = requests.get(f"{COMFYUI_URL}/system_stats", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "system" in data
        assert "devices" in data
    except requests.exceptions.ConnectionError:
        pytest.skip("ComfyUI server not running")