"""Orchestrate tables → evidence → figures → compile via hooks."""

from __future__ import annotations

import sys
from typing import Any, Callable

from fttp.commands import cmd_compile, cmd_evidence, cmd_figures, cmd_tables
from fttp.config import FttpConfigError, load_config

Step = tuple[str, Callable[[dict[str, Any] | None], int]]

STEPS: tuple[Step, ...] = (
    ("tables", cmd_tables),
    ("evidence", cmd_evidence),
    ("figures", cmd_figures),
    ("compile", cmd_compile),
)


def run_pipeline(cfg: dict[str, Any] | None = None) -> int:
    try:
        cfg = cfg or load_config()
    except FttpConfigError as exc:
        print(f"fttp pipeline: {exc}", file=sys.stderr)
        return 1

    for name, handler in STEPS:
        print(f"fttp pipeline: step {name}")
        code = handler(cfg)
        if code != 0:
            print(
                f"fttp pipeline: stopped at '{name}' (exit {code}). "
                "Fix the issue above before re-running.",
                file=sys.stderr,
            )
            return code

    print("fttp pipeline: all steps completed")
    return 0
