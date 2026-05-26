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
from fttp.env_suggest import cmd_env_suggest
from fttp.pipeline import run_pipeline
from fttp.scaffold import cmd_scaffold
from fttp.venue_validate import cmd_venue_validate


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fttp",
        description="from-thesis-to-paper: config, hooks, and paper pipeline CLI",
    )
    parser.add_argument("--version", action="version", version=f"fttp {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Validate config, repoRoot, and hook paths")

    scaf = sub.add_parser("scaffold", help="Create paper workspace from template")
    scaf.add_argument("--slug", required=True, help="workspaceSlug (folder name)")
    scaf.add_argument(
        "--parent",
        type=Path,
        required=True,
        help="Parent directory for the new workspace",
    )
    scaf.add_argument(
        "--force",
        action="store_true",
        help="Allow scaffolding into an existing directory",
    )

    env_s = sub.add_parser(
        "env-suggest",
        help="Suggest .env keys from requirements.txt and notebook imports",
    )
    env_s.add_argument(
        "--roots",
        type=Path,
        nargs="+",
        required=True,
        help="One or more roots to scan",
    )
    env_s.add_argument(
        "--write",
        type=Path,
        default=None,
        metavar="PATH",
        help="Write suggestions to PATH (e.g. .env.example)",
    )

    venue = sub.add_parser("venue", help="Venue LaTeX layout checks")
    venue_sub = venue.add_subparsers(dest="venue_cmd", required=True)
    venue_sub.add_parser("validate", help="Check mainTex and paper/latex/ layout")

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
    if args.command == "scaffold":
        return cmd_scaffold(args.slug, args.parent, force=args.force)
    if args.command == "env-suggest":
        return cmd_env_suggest(args.roots, write=args.write)
    if args.command == "venue":
        if args.venue_cmd == "validate":
            return cmd_venue_validate()
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
