import subprocess
import sys
from pathlib import Path

def test_uv_environment_exists():
    # Check that uv.lock and .venv exist.
    root = Path(__file__).parent.parent
    assert (root / "uv.lock").exists(), "uv.lock not found. Run 'uv sync'"
    assert (root / ".venv").exists(), ".venv not found. Run 'uv sync'"

def test_python_version():
    # Checking Python 3.12.x.
    version = sys.version_info
    assert version.major == 3 and version.minor == 12, f"Expected Python 3.12, got {version.major}.{version.minor}"