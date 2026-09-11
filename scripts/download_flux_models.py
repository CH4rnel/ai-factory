#!/usr/bin/env python3
# Script for downloading FLUX models with SHA-256 verification.
import hashlib
from pathlib import Path

import requests
from tqdm import tqdm


# We use community mirrors that have no licensing requirements.
MODELS = {
    "flux1-schnell-Q4_0.gguf": {
        "url": "https://huggingface.co/city96/FLUX.1-schnell-gguf/resolve/main/flux1-schnell-Q4_0.gguf",
        "sha256": "90a393d3a44bec691c707003f434fdde06064b870bb3c206eb7a4f109b25ff4e", 
        "path": "models/flux/unet"
    },
    "clip_l.safetensors": {
        "url": "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors",
        "sha256": "660c6f5b1abae9dc498ac2d21e1347d2abdb0cf6c0c0c8576cd796491d9a6cdd",
        "path": "models/flux/clip"
    },
    "t5-v1_1-xxl-encoder-Q8_0.gguf": {
        "url": "https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/resolve/main/t5-v1_1-xxl-encoder-Q8_0.gguf",
        # Current hash verified upon loading.
        "sha256": "9ec60f6028534b7fe5af439fcb535d75a68592a9ca3fcdeb175ef89e3ee99825",
        "path": "models/flux/clip"
    },
    "ae.safetensors": {
        # We use a community mirror with no licensing requirements.
        "url": "https://huggingface.co/flux-safetensors/flux-safetensors/resolve/main/ae.safetensors",
        # Current hash verified upon loading.
        "sha256": "afc8e28272cd15db3919bacdb6918ce9c1ed22e96cb12c4d5ed0fba823529e38",
        "path": "models/flux/vae"
    }
}


def download_with_progress(url: str, dest: Path):
    headers = {}
    if dest.exists():
        headers["Range"] = f"bytes={dest.stat().st_size}-"
    
    response = requests.get(url, stream=True, headers=headers)
    response.raise_for_status()
    
    total_size = int(response.headers.get("content-length", 0)) + dest.stat().st_size if dest.exists() else int(response.headers.get("content-length", 0))
    mode = "ab" if dest.exists() else "wb"
    
    with open(dest, mode) as f, tqdm(
        desc=dest.name,
        total=total_size,
        initial=dest.stat().st_size if dest.exists() else 0,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))
            
    return True


def verify_sha256(file_path: Path, expected_hash: str) -> tuple[bool, str]:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    computed_hash = sha256_hash.hexdigest()
    return computed_hash == expected_hash, computed_hash


def main():
    project_root = Path(__file__).parent.parent
    
    for model_name, config in MODELS.items():
        dest_dir = project_root / config["path"]
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / model_name
        
        if dest_path.exists():
            print(f"✓ {model_name} already exists, checking the hash...")
            is_valid, computed_hash = verify_sha256(dest_path, config["sha256"])
            if is_valid:
                print(f"  ✅ Hash matches: {computed_hash[:16]}...")
                continue
            else:
                print(f"  ⚠️  The hash does not match!")
                print(f"  Expected: {config['sha256']}")
                print(f"  Calculated: {computed_hash}")
                
                response = input("  Restart the download? (y/n): ")
                if response.lower() != 'y':
                    print(f"  ⏭️  Pass {model_name}")
                    continue
                dest_path.unlink()
        
        print(f"⬇️  Loading {model_name}...")
        try:
            download_with_progress(config["url"], dest_path)
        except Exception as e:
            print(f"❌ Loading error {model_name}: {e}")
            continue
        
        print(f"🔐 Verification SHA-256...")
        is_valid, computed_hash = verify_sha256(dest_path, config["sha256"])
        if is_valid:
            print(f"✅ {model_name} successfully uploaded (Hash: {computed_hash[:16]}...)")
        else:
            print(f"⚠️  WARNING: Hash mismatch after download!")
            print(f"   Expected: {config['sha256']}")
            print(f"   Calculated: {computed_hash}")
            print(f"   💡 The file on the server may have changed. Update the sha256 in the script to: {computed_hash}")


if __name__ == "__main__":
    main()