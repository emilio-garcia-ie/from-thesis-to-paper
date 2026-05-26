"""Validate venue LaTeX layout against workspace config."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from fttp.config import (
    FttpConfigError,
    active_venue_profile,
    load_config,
    paper_dir,
    repo_root,
    resolve_active_main_tex,
)

_DOCUMENTCLASS_RE = re.compile(
    r"\\documentclass(?:\[[^\]]*\])?\{([^}]+)\}",
)


def _find_cls_files(latex_dir: Path) -> set[str]:
    names: set[str] = set()
    if not latex_dir.is_dir():
        return names
    for path in latex_dir.rglob("*.cls"):
        names.add(path.stem)
    return names


def validate_venue(cfg: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for venue LaTeX files."""
    errors: list[str] = []
    warnings: list[str] = []
    root = repo_root(cfg)
    pdir = paper_dir(cfg)
    main_tex = resolve_active_main_tex(cfg)

    if not pdir.is_dir():
        errors.append(f"paper.dir missing: {pdir}")
        return errors, warnings

    if not main_tex.is_file():
        errors.append(f"main TeX not found: {main_tex}")
    else:
        text = main_tex.read_text(encoding="utf-8", errors="replace")
        match = _DOCUMENTCLASS_RE.search(text)
        if match:
            cls_name = match.group(1).strip()
            latex_dir = pdir / "latex"
            cls_files = _find_cls_files(latex_dir)
            if cls_name not in cls_files and not (latex_dir / f"{cls_name}.cls").is_file():
                warnings.append(
                    f"documentclass '{cls_name}' not found under {latex_dir.relative_to(root)} "
                    f"(found .cls: {sorted(cls_files) or 'none'})"
                )
        else:
            warnings.append(f"no \\documentclass in {main_tex.relative_to(root)}")

    profile = active_venue_profile(cfg) or {}
    template_rel = profile.get("templatePath")
    if profile.get("templateDeferred") is True:
        return errors, warnings

    if template_rel:
        template_dir = root / template_rel
        if not template_dir.is_dir():
            errors.append(f"templatePath not found: {template_dir}")
        elif not any(template_dir.iterdir()):
            warnings.append(f"templatePath is empty: {template_dir.relative_to(root)}")
    else:
        latex_dir = pdir / "latex"
        if latex_dir.is_dir() and not any(latex_dir.iterdir()):
            warnings.append("paper/latex/ is empty (copy BYO template or set templateDeferred)")

    guidelines = profile.get("guidelines")
    if guidelines:
        gpath = root / guidelines
        if not gpath.is_file():
            warnings.append(f"guidelines file missing: {gpath.relative_to(root)}")

    return errors, warnings


def cmd_venue_validate(cfg: dict[str, Any] | None = None) -> int:
    try:
        cfg = cfg or load_config()
    except FttpConfigError as exc:
        print(f"fttp venue validate: {exc}", file=sys.stderr)
        return 1

    root = repo_root(cfg)
    active = (cfg.get("paper") or {}).get("activeVenue", "")
    main_tex = resolve_active_main_tex(cfg)
    print(f"fttp venue validate: workspace={cfg.get('workspaceName')}")
    print(f"  repoRoot: {root}")
    print(f"  activeVenue: {active or '(default)'}")
    print(f"  mainTex: {main_tex}")

    errors, warnings = validate_venue(cfg)
    for warn in warnings:
        print(f"  WARNING: {warn}")
    if errors:
        print("fttp venue validate: FAIL", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    if warnings:
        print("fttp venue validate: OK (with warnings)")
    else:
        print("fttp venue validate: OK")
    return 0
