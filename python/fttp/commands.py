"""Stub CLI command handlers for the paper production pipeline."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from fttp.config import FttpConfigError, load_config, paper_dir, paper_main_tex, repo_root


def _missing(msg: str) -> int:
    print(msg, file=sys.stderr)
    return 1


def cmd_tables(cfg: dict[str, Any] | None = None) -> int:
    try:
        cfg = cfg or load_config()
    except FttpConfigError as exc:
        return _missing(f"fttp tables: {exc}")

    root = repo_root(cfg)
    evidence = cfg.get("evidence") or {}
    catalog_rel = evidence.get("catalog")
    if not catalog_rel:
        return _missing(
            "fttp tables: evidence.catalog is not set in config.\n"
            "  Add evidence.catalog (e.g. memory/thesis_experiment_catalog.md)."
        )

    catalog = root / catalog_rel
    if not catalog.is_file():
        return _missing(
            f"fttp tables: catalog not found:\n  {catalog}\n"
            "  Run evidence archaeology (SA3) or fix evidence.catalog."
        )

    out_dir = paper_dir(cfg) / "tables"
    print(f"fttp tables: stub — would export LaTeX fragments to {out_dir}")
    print(f"  Source catalog: {catalog}")
    return 0


def cmd_evidence(cfg: dict[str, Any] | None = None) -> int:
    try:
        cfg = cfg or load_config()
    except FttpConfigError as exc:
        return _missing(f"fttp evidence: {exc}")

    root = repo_root(cfg)
    evidence = cfg.get("evidence") or {}
    lineage_rel = evidence.get("lineageCsv")
    if not lineage_rel:
        return _missing(
            "fttp evidence: evidence.lineageCsv is not set in config.\n"
            "  Add evidence.lineageCsv (e.g. experimentos/evidence/log_lineage.csv)."
        )

    lineage = root / lineage_rel
    if not lineage.is_file():
        return _missing(
            f"fttp evidence: lineage CSV not found:\n  {lineage}\n"
            "  Run scripts/archaeology/build_log_lineage.py or fix evidence.lineageCsv."
        )

    print(f"fttp evidence: stub — would build reproducibility bundle from {lineage}")
    return 0


def cmd_figures(cfg: dict[str, Any] | None = None) -> int:
    try:
        cfg = cfg or load_config()
    except FttpConfigError as exc:
        return _missing(f"fttp figures: {exc}")

    figures_dir = paper_dir(cfg) / "figures"
    style = repo_root(cfg) / "experimentos" / "fixtures" / "figure_style.json"
    if not figures_dir.is_dir():
        return _missing(
            f"fttp figures: figures directory not found:\n  {figures_dir}\n"
            "  Create paper/figures/ or run scripts/paper/generate_figures.py."
        )

    if not style.is_file():
        return _missing(
            f"fttp figures: figure style fixture not found:\n  {style}\n"
            "  Check experimentos/fixtures/figure_style.json."
        )

    print(f"fttp figures: stub — would refresh assets under {figures_dir}")
    return 0


def cmd_compile(cfg: dict[str, Any] | None = None) -> int:
    try:
        cfg = cfg or load_config()
    except FttpConfigError as exc:
        return _missing(f"fttp compile: {exc}")

    main_tex = paper_main_tex(cfg)
    pdf = main_tex.with_suffix(".pdf")
    if not main_tex.is_file():
        return _missing(
            f"fttp compile: main TeX not found:\n  {main_tex}\n"
            "  Set paper.mainTex in config or create the manuscript entry file."
        )

    if not pdf.is_file():
        return _missing(
            f"fttp compile: PDF not found (run latexmk first):\n  {pdf}\n"
            "  Stub compile checks paths only; use latexmk or scripts/paper/ locally."
        )

    print(f"fttp compile: stub OK — {pdf} exists")
    return 0
