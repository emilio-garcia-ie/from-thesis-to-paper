"""fttp command-line interface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from fttp import __version__
from fttp.commands import (
    cmd_compile,
    cmd_doctor,
    cmd_evidence,
    cmd_figures,
    cmd_lineage_build,
    cmd_lineage_validate,
    cmd_tables,
)
from fttp.pipeline import run_pipeline


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fttp",
        description="from-thesis-to-paper: config, hooks, and paper pipeline CLI",
    )
    parser.add_argument("--version", action="version", version=f"fttp {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Validate config, repoRoot, and hook paths")

    sub.add_parser("tables", help="Run hooks.tables under repoRoot")
    sub.add_parser("evidence", help="Run hooks.evidence under repoRoot")
    sub.add_parser("figures", help="Run hooks.figures under repoRoot")
    sub.add_parser("compile", help="Run venue/hook compile or verify PDF exists")

    lineage = sub.add_parser("lineage", help="Lineage build hook or CSV validate")
    lineage_sub = lineage.add_subparsers(dest="lineage_cmd", required=True)
    lineage_sub.add_parser("build", help="Run hooks.lineageBuild")
    val = lineage_sub.add_parser("validate", help="Validate lineage CSV (fttp.evidence)")
    val.add_argument("--csv", type=Path, default=None, help="Path to lineage CSV")

    sub.add_parser(
        "pipeline",
        help="Run tables → evidence → figures → compile in order",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        return cmd_doctor()
    if args.command == "tables":
        return cmd_tables()
    if args.command == "evidence":
        return cmd_evidence()
    if args.command == "figures":
        return cmd_figures()
    if args.command == "compile":
        return cmd_compile()
    if args.command == "lineage":
        if args.lineage_cmd == "build":
            return cmd_lineage_build()
        return cmd_lineage_validate(args.csv)
    if args.command == "pipeline":
        return run_pipeline()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
