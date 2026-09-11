# AI Factory CLI - a single entry point for all teams.
import shutil
import sys
from pathlib import Path

import typer

app = typer.Typer(
    help="AI Factory - local-first media production pipeline",
    add_completion=False,
)


@app.command()
def doctor():
    # Checks the environment: Python, CUDA, GPU, PyTorch, FFmpeg, ComfyUI.
    typer.echo("🔍 AI Factory Doctor - environment check\n")
    
    # Python version
    typer.echo(f"✅ Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # CUDA availability (lazy import torch)
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            gpu_name = torch.cuda.get_device_name(0)
            vram_total = torch.cuda.get_device_properties(0).total_memory / (1024**2)
            typer.echo(f"✅ CUDA: available, GPU: {gpu_name}")
            typer.echo(f"   VRAM total: {vram_total:.0f} MB")
            typer.echo(f"   VRAM usable budget: ~5000 MB.")
        else:
            typer.echo("❌ CUDA: unavailable (GPU inference will not work)")
    except ImportError:
        typer.echo("⚠️  PyTorch: not established (uv add --group gpu torch)")
    
    # FFmpeg
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        typer.echo(f"✅ FFmpeg: {ffmpeg_path}")
    else:
        typer.echo("❌ FFmpeg: not found in PATH")
    
    # ComfyUI
    comfy_root = Path(__file__).parent.parent.parent / "apps" / "comfy" / "ComfyUI"
    if comfy_root.exists() and (comfy_root / "main.py").exists():
        typer.echo(f"✅ ComfyUI: found in {comfy_root}")
    else:
        typer.echo("⚠️  ComfyUI: not initialized (git submodule update --init --recursive)")
    
    # Disk space
    project_root = Path(__file__).parent.parent.parent
    disk_usage = shutil.disk_usage(project_root)
    free_gb = disk_usage.free / (1024**3)
    typer.echo(f"✅ Disk: {free_gb:.1f} GB free")
    
    typer.echo("\n✅ Doctor check completed")


@app.command()
def version():
    # Outputs the AI ​​Factory version.
    typer.echo("AI Factory v0.1.0")


if __name__ == "__main__":
    app()