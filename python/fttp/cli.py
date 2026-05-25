"""fttp command-line interface."""

from __future__ import annotations

import argparse
import sys

from fttp import __version__
from fttp.commands import cmd_compile, cmd_evidence, cmd_figures, cmd_tables
from fttp.pipeline import run_pipeline


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fttp",
        description="from-thesis-to-paper: paper pipeline CLI (stub implementations)",
    )
    parser.add_argument("--version", action="version", version=f"fttp {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("tables", help="Export LaTeX table fragments (stub)")
    sub.add_parser("evidence", help="Build evidence / lineage bundle (stub)")
    sub.add_parser("figures", help="Generate or refresh figure assets (stub)")
    sub.add_parser("compile", help="Verify paper PDF paths (stub)")
    sub.add_parser(
        "pipeline",
        help="Run tables → evidence → figures → compile in order",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    handlers = {
        "tables": cmd_tables,
        "evidence": cmd_evidence,
        "figures": cmd_figures,
        "compile": cmd_compile,
        "pipeline": lambda _: run_pipeline(),
    }
    return handlers[args.command](None)


if __name__ == "__main__":
    raise SystemExit(main())
