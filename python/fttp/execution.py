"""Safe direct subprocess execution for trusted local hooks."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
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
        process = subprocess.Popen(
            argv,
            cwd=str(cwd),
            start_new_session=os.name == "posix",
        )
    except (FileNotFoundError, PermissionError, OSError) as exc:
        print(f"fttp: cannot start command {argv[0]}: {exc}", file=sys.stderr)
        return 1
    try:
        code = process.wait()
    except KeyboardInterrupt:
        # Hooks are trusted local programs, but a Ctrl+C must still leave no
        # framework-owned child running and must not leak a Python traceback.
        if os.name == "posix":
            try:
                os.killpg(process.pid, signal.SIGINT)
            except ProcessLookupError:
                pass
        elif process.poll() is None:
            process.send_signal(signal.SIGINT)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        print("fttp: interrupted", file=sys.stderr)
        return 130
    if code < 0:
        return 128 + -code
    return int(code)


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
