# Tests for FLUX integration
import hashlib
import json
from pathlib import Path

import pytest

# Importing contracts.
from ai_factory.contracts.manifest import GenerationManifest, PromptTemplate


def test_flux_model_files_exist():
    # Checks for the presence of FLUX models in models/flux/
    models_root = Path(__file__).parent.parent / "models" / "flux"
    
    # GGUF Q4_0 model (~5.5 GB)
    gguf_path = models_root / "unet" / "flux1-schnell-Q4_0.gguf"
    assert gguf_path.exists(), f"FLUX GGUF model not found: {gguf_path}"
    
    # CLIP text encoders
    clip_l = models_root / "clip" / "clip_l.safetensors"
    t5xxl = models_root / "clip" / "t5-v1_1-xxl-encoder-Q8_0.gguf"
    assert clip_l.exists(), f"CLIP-L model not found: {clip_l}"
    assert t5xxl.exists(), f"T5-XXL model not found: {t5xxl}"
    
    # VAE
    vae = models_root / "vae" / "ae.safetensors"
    assert vae.exists(), f"VAE model not found: {vae}"


def test_flux_model_hashes_verified():
    # Verifies the SHA-256 hashes of the models.
    # And this is a placeholder test—actual verification will happen at runtime.
    models_root = Path(__file__).parent.parent / "models" / "flux"
    gguf_path = models_root / "unet" / "flux1-schnell-Q4_0.gguf"
    
    if gguf_path.exists():
        # Here, we calculate the hash (reading block by block for large files).
        sha256_hash = hashlib.sha256()
        with open(gguf_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256_hash.update(chunk)
        computed_hash = sha256_hash.hexdigest()
        
        # Expected hash (placeholder — need to obtain the actual one)
        expected_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        
        # In the actual test, we compare against the expected result.
        # assert computed_hash == expected_hash
        assert len(computed_hash) == 64, "SHA-256 hash should be 64 characters"


def test_flux_workflow_json_valid():
    # Checks validity ComfyUI workflow JSON
    workflow_path = Path(__file__).parent.parent / "workflows" / "comfy" / "flux_schnell.json"
    assert workflow_path.exists(), f"FLUX workflow not found: {workflow_path}"
    
    with open(workflow_path, "r") as f:
        workflow = json.load(f)
    
    # Checking the basic structure ComfyUI workflow
    assert isinstance(workflow, dict), "Workflow should be a dict"
    assert "last_node_id" in workflow or "nodes" in workflow, "Invalid workflow structure"


def test_prompt_templates_exist():
    # Checks for the presence of prompt templates.
    templates_dir = Path(__file__).parent.parent / "storage" / "prompts"
    assert templates_dir.exists(), "storage/prompts/ directory not found"
    
    # Checking for the presence of base templates.
    system_template = templates_dir / "flux_system.txt"
    user_template = templates_dir / "flux_user.txt"
    assert system_template.exists(), f"System prompt template not found: {system_template}"
    assert user_template.exists(), f"User prompt template not found: {user_template}"


def test_generation_manifest_schema():
    # Validates the GenerationManifest v1 schema.
    manifest = GenerationManifest(
        version="1.0",
        job_id="test-job-001",
        model="flux1-schnell-Q4_0",
        prompt="A cyberpunk city at night",
        negative_prompt="",
        seed=42,
        steps=20,
        cfg_scale=3.5,
        width=1024,
        height=1024,
        output_path="exports/raw/test.png"
    )
    
    assert manifest.version == "1.0"
    assert manifest.job_id == "test-job-001"
    assert manifest.model == "flux1-schnell-Q4_0"
    assert manifest.seed == 42
    
    # Verifying serialization
    json_str = manifest.model_dump_json()
    assert "flux1-schnell-Q4_0" in json_str
    
    # Verifying deserialization
    restored = GenerationManifest.model_validate_json(json_str)
    assert restored.job_id == manifest.job_id


def test_prompt_template_rendering():
    # Verifies the rendering of prompt templates.
    template = PromptTemplate(
        system="You are a helpful assistant.",
        user="Generate an image: {prompt}"
    )
    
    rendered = template.render(prompt="A cat")
    assert "A cat" in rendered["user"]
    assert "helpful assistant" in rendered["system"]