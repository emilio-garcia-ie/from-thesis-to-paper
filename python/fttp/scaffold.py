"""Scaffold a new paper workspace from templates/paper-workspace/."""

from __future__ import annotations

import json
import re
import shutil
import stat
from pathlib import Path

from fttp.config import FttpConfigError, validate_slug

_PLACEHOLDER = "{{WORKSPACE_SLUG}}"
_TEXT_SUFFIXES = {
    ".md",
    ".json",
    ".tex",
    ".sh",
    ".env",
    ".example",
    ".gitignore",
    ".txt",
    ".yml",
    ".yaml",
}

_HOOK_STUBS: dict[str, str] = {
    "scripts/archaeology/build_log_lineage.py": '''"""Stub hook — replace with real lineage build (SA3/SA4)."""
import sys
print("fttp stub: lineageBuild (no-op)")
sys.exit(0)
''',
    "scripts/paper/export_tables_from_catalog.py": '''"""Stub hook — replace with table export (SA9)."""
import sys
print("fttp stub: tables (no-op)")
sys.exit(0)
''',
    "scripts/paper/build_evidence_bundle.py": '''"""Stub hook — replace with evidence bundle (SA4)."""
import sys
print("fttp stub: evidence (no-op)")
sys.exit(0)
''',
    "scripts/paper/generate_figures.py": '''"""Stub hook — replace with figure generation (SA9)."""
import sys
print("fttp stub: figures (no-op)")
sys.exit(0)
''',
    "scripts/paper/build_primary.sh": '''#!/usr/bin/env bash
# Stub compile hook — replace with latexmk or venue build script.
set -euo pipefail
echo "fttp stub: compile (no-op; create paper/main.pdf manually or add real build)"
exit 0
''',
}


def framework_root() -> Path:
    """Return the from-thesis-to-paper repository root (parent of python/)."""
    return Path(__file__).resolve().parents[2]


def template_dir() -> Path:
    path = framework_root() / "templates" / "paper-workspace"
    if not path.is_dir():
        raise FttpConfigError(
            f"Paper workspace template not found: {path}\n"
            "  Run from an installed fttp package with templates/ bundled."
        )
    return path


def _is_text_file(path: Path) -> bool:
    if path.name == ".env.example" or path.name.endswith(".example"):
        return True
    return path.suffix.lower() in _TEXT_SUFFIXES or path.name in (
        ".gitignore",
        "fttp.config.json",
    )


def _substitute_slug(content: str, slug: str) -> str:
    return content.replace(_PLACEHOLDER, slug)


def _patch_config_repo_root(dest: Path, slug: str) -> None:
    cfg_path = dest / "fttp.config.json"
    raw = json.loads(cfg_path.read_text(encoding="utf-8"))
    raw["workspaceName"] = slug
    raw["workspaceSlug"] = slug
    raw["repoRoot"] = str(dest.resolve())
    overleaf = raw.get("overleafPaper")
    if isinstance(overleaf, dict):
        overleaf["displayName"] = slug
    cfg_path.write_text(
        json.dumps(raw, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _ensure_layout_dirs(dest: Path) -> None:
    for rel in (
        "memory",
        "experimentos/evidence",
        "paper/latex",
        "paper/tables",
        "paper/figures",
        "codigo",
    ):
        (dest / rel).mkdir(parents=True, exist_ok=True)
        keep = dest / rel / ".gitkeep"
        if not any((dest / rel).iterdir()):
            keep.touch()


def _ensure_stub_hooks(dest: Path, cfg: dict) -> None:
    hooks = cfg.get("hooks") or {}
    for rel in hooks.values():
        if not isinstance(rel, str):
            continue
        body = _HOOK_STUBS.get(rel)
        if body is None:
            continue
        path = dest / rel
        if path.is_file():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        if path.suffix == ".sh":
            path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def scaffold_workspace(slug: str, parent: Path, *, force: bool = False) -> Path:
    """
    Copy templates/paper-workspace/ to parent/slug and substitute placeholders.

    Returns the resolved destination path.
    """
    validate_slug(slug)
    parent = parent.expanduser().resolve()
    parent.mkdir(parents=True, exist_ok=True)
    dest = parent / slug

    if dest.exists():
        if not force:
            raise FttpConfigError(
                f"Destination already exists: {dest}\n"
                "  Use --force to scaffold into a non-empty directory."
            )
        if dest.is_file():
            raise FttpConfigError(f"Destination is a file, not a directory: {dest}")
    else:
        dest.mkdir(parents=True)

    src = template_dir()
    for item in src.iterdir():
        target = dest / item.name
        if item.is_dir():
            if target.exists():
                shutil.copytree(item, target, dirs_exist_ok=True)
            else:
                shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)

    for path in dest.rglob("*"):
        if not path.is_file():
            continue
        if not _is_text_file(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if _PLACEHOLDER not in text and slug not in text:
            continue
        updated = _substitute_slug(text, slug)
        if updated != text:
            path.write_text(updated, encoding="utf-8")

    _ensure_layout_dirs(dest)
    _patch_config_repo_root(dest, slug)

    cfg = json.loads((dest / "fttp.config.json").read_text(encoding="utf-8"))
    _ensure_stub_hooks(dest, cfg)

    return dest


def cmd_scaffold(slug: str, parent: Path, *, force: bool = False) -> int:
    try:
        dest = scaffold_workspace(slug, parent, force=force)
    except FttpConfigError as exc:
        print(f"fttp scaffold: {exc}", file=__import__("sys").stderr)
        return 1

    print(f"fttp scaffold: OK — {dest}")
    print(f"  config: {dest / 'fttp.config.json'}")
    print("  next: set readOnlyRoots[], copy .env.example → .env, run SA0 intake")
    return 0
