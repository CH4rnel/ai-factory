import subprocess
import sys
from pathlib import Path


def test_doctor_command_via_subprocess():
    # Verifies that the `ai-factory doctor` command is launched via `uv run`.
    result = subprocess.run(
        ["uv", "run", "ai-factory", "doctor"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    
    # The command must execute successfully (exit code 0).
    assert result.returncode == 0, f"Doctor command failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    
    # It should display information about Python.
    assert "Python" in result.stdout or "python" in result.stdout.lower()