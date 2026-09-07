"""Safe direct subprocess execution for trusted local hooks."""

from __future__ import annotations

import os
import signal
import subprocess
from pathlib import Path
from typing import Sequence


def run_local_command(
    command: Sequence[str | os.PathLike[str]],
    *,
    cwd: Path,
) -> int:
    """Run a local command and convert expected launch failures to exit 1."""
    argv = [str(part) for part in command]
    try:
        result = subprocess.run(argv, cwd=str(cwd), check=False)
    except (FileNotFoundError, PermissionError, OSError) as exc:
        print(f"fttp: cannot start command {argv[0]}: {exc}", file=__import__("sys").stderr)
        return 1
    if result.returncode < 0:
        return 128 + -result.returncode
    return int(result.returncode)


def run_captured(
    command: Sequence[str | os.PathLike[str]], *, cwd: Path
) -> subprocess.CompletedProcess[str]:
    """Captured variant used by the Node parity tests and diagnostics."""
    argv = [str(part) for part in command]
    try:
        return subprocess.run(
            argv,
            cwd=str(cwd),
            check=False,
            text=True,
            capture_output=True,
        )
    except (FileNotFoundError, PermissionError, OSError) as exc:
        return subprocess.CompletedProcess(
            argv,
            1,
            "",
            f"fttp: cannot start command {argv[0]}: {exc}\n",
        )
