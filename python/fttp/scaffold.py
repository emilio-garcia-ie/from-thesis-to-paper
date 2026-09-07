"""Scaffold a new paper workspace from templates/paper-workspace/."""

from __future__ import annotations

import json
import shutil
import stat
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from importlib import resources

from fttp.config import FttpConfigError, load_config, validate_slug

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
    "scripts/archaeology/build_log_lineage.py": '''"""Placeholder hook — replace with real lineage build (SA3/SA4)."""
FTTP_PLACEHOLDER_HOOK = True
import sys
print("fttp placeholder: lineageBuild is not configured; replace this hook", file=sys.stderr)
sys.exit(1)
''',
    "scripts/paper/export_tables_from_catalog.py": '''"""Placeholder hook — replace with table export (SA9)."""
FTTP_PLACEHOLDER_HOOK = True
import sys
print("fttp placeholder: tables is not configured; replace this hook", file=sys.stderr)
sys.exit(1)
''',
    "scripts/paper/build_evidence_bundle.py": '''"""Placeholder hook — replace with evidence bundle (SA4)."""
FTTP_PLACEHOLDER_HOOK = True
import sys
print("fttp placeholder: evidence is not configured; replace this hook", file=sys.stderr)
sys.exit(1)
''',
    "scripts/paper/generate_figures.py": '''"""Placeholder hook — replace with figure generation (SA9)."""
FTTP_PLACEHOLDER_HOOK = True
import sys
print("fttp placeholder: figures is not configured; replace this hook", file=sys.stderr)
sys.exit(1)
''',
    "scripts/paper/build_primary.sh": '''#!/usr/bin/env bash
# FTTP_PLACEHOLDER_HOOK: replace with latexmk or venue build script.
set -euo pipefail
echo "fttp placeholder: compile is not configured; replace this hook" >&2
exit 1
''',
}


def framework_root() -> Path:
    """Return the from-thesis-to-paper repository root (parent of python/)."""
    return Path(__file__).resolve().parents[2]


def template_dir() -> Path:
    path = framework_root() / "templates" / "paper-workspace"
    if path.is_dir():
        return path
    raise FttpConfigError(
        f"Paper workspace template not found: {path}\n"
        "  Run from an installed fttp package with templates/ bundled."
    )


@contextmanager
def _template_source() -> Iterator[object]:
    """Yield the canonical checkout template or a bundled package resource."""
    source = framework_root() / "templates" / "paper-workspace"
    if source.is_dir():
        yield source
        return
    try:
        bundled = resources.files("fttp").joinpath("_templates", "paper-workspace")
        if not bundled.is_dir():
            raise FttpConfigError(f"Bundled paper workspace template is missing: {bundled}")
        # Copy through the Traversable interface directly. This works for
        # regular installs and for Python 3.10 resource readers without
        # assuming that ``as_file`` can materialize a directory.
        yield bundled
    except (FileNotFoundError, ModuleNotFoundError, OSError, TypeError) as exc:
        raise FttpConfigError(
            "Paper workspace template is unavailable from this checkout or installed package"
        ) from exc


def _copy_missing(src: object, dest: Path, created: list[Path]) -> None:
    """Copy a template tree without replacing an existing user file."""
    if dest.is_symlink():
        raise FttpConfigError(f"Cannot scaffold through symlink: {dest}")
    source_is_dir = bool(getattr(src, "is_dir")())
    if source_is_dir:
        if dest.exists() and not dest.is_dir():
            raise FttpConfigError(f"Cannot scaffold directory over file: {dest}")
        if not dest.exists():
            dest.mkdir(parents=True)
            created.append(dest)
        for child in src.iterdir():
            _copy_missing(child, dest / child.name, created)
        return
    if dest.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(src, Path):
        shutil.copy2(src, dest)
    else:
        with src.open("rb") as source_handle, dest.open("wb") as destination_handle:
            shutil.copyfileobj(source_handle, destination_handle)
    created.append(dest)


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


def _ensure_layout_dirs(dest: Path, created: list[Path]) -> None:
    for rel in (
        "memory",
        "experimentos/evidence",
        "paper/latex",
        "paper/tables",
        "paper/figures",
        "codigo",
    ):
        directory = dest / rel
        missing: list[Path] = []
        cursor = directory
        while not cursor.exists() and cursor != dest:
            missing.append(cursor)
            cursor = cursor.parent
        directory.mkdir(parents=True, exist_ok=True)
        created.extend(reversed(missing))
        keep = directory / ".gitkeep"
        if not any((dest / rel).iterdir()):
            keep.touch()
            created.append(keep)


def _ensure_stub_hooks(dest: Path, cfg: dict, created: list[Path]) -> None:
    hooks = cfg.get("hooks") or {}
    for rel in hooks.values():
        if not isinstance(rel, str):
            continue
        body = _HOOK_STUBS.get(rel)
        if body is None:
            continue
        path = dest / rel
        if path.is_symlink():
            raise FttpConfigError(f"Cannot scaffold hook through symlink: {path}")
        if path.is_file():
            continue
        missing: list[Path] = []
        cursor = path.parent
        while not cursor.exists() and cursor != dest:
            missing.append(cursor)
            cursor = cursor.parent
        path.parent.mkdir(parents=True, exist_ok=True)
        created.extend(reversed(missing))
        path.write_text(body, encoding="utf-8")
        created.append(path)
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
    new_destination = False

    if dest.is_symlink():
        raise FttpConfigError(f"Destination must not be a symlink: {dest}")
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
        new_destination = True

    created: list[Path] = [dest] if new_destination else []
    try:
        with _template_source() as src:
            for item in src.iterdir():
                _copy_missing(item, dest / item.name, created)

        new_files = [p for p in created if p.is_file()]
        for path in new_files:
            if not _is_text_file(path):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            updated = _substitute_slug(text, slug)
            if updated != text:
                path.write_text(updated, encoding="utf-8")

        _ensure_layout_dirs(dest, created)
        cfg_path = dest / "fttp.config.json"
        if not cfg_path.is_file():
            raise FttpConfigError(f"Template is missing fttp.config.json: {cfg_path}")
        try:
            raw = json.loads(cfg_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise FttpConfigError(f"Cannot read workspace config: {cfg_path}: {exc}") from exc
        if not isinstance(raw, dict):
            raise FttpConfigError(f"Workspace config must be a JSON object: {cfg_path}")
        if raw.get("workspaceSlug") not in (None, _PLACEHOLDER, slug):
            raise FttpConfigError(f"Existing workspace config has a different workspaceSlug: {cfg_path}")
        if raw.get("workspaceName") not in (None, _PLACEHOLDER, slug):
            raise FttpConfigError(f"Existing workspace config has a different workspaceName: {cfg_path}")
        if cfg_path not in created and raw.get("repoRoot") not in (None, str(dest.resolve())):
            raise FttpConfigError(f"Existing workspace config points at a different repoRoot: {cfg_path}")
        if cfg_path in created:
            _patch_config_repo_root(dest, slug)
        try:
            cfg = load_config(cfg_path)
        except FttpConfigError:
            raise
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise FttpConfigError(f"Cannot read workspace config: {cfg_path}: {exc}") from exc
        _ensure_stub_hooks(dest, cfg, created)
    except Exception:
        # Roll back only paths created by this invocation.  Existing workspace
        # files remain untouched even when --force was requested.
        for path in sorted(set(created), key=lambda p: len(p.parts), reverse=True):
            try:
                if path.is_dir() and not path.is_symlink():
                    path.rmdir()
                elif path.exists() or path.is_symlink():
                    path.unlink()
            except OSError:
                pass
        raise

    for path in new_files:
        if not path.is_file():
            continue
        if path.suffix == ".sh":
            path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    return dest


def cmd_scaffold(slug: str, parent: Path, *, force: bool = False) -> int:
    try:
        dest = scaffold_workspace(slug, parent, force=force)
    except (FttpConfigError, OSError) as exc:
        print(f"fttp scaffold: {exc}", file=__import__("sys").stderr)
        return 1

    print(f"fttp scaffold: OK — {dest}")
    print(f"  config: {dest / 'fttp.config.json'}")
    print("  next: set readOnlyRoots[], copy .env.example → .env, run SA0 intake")
    return 0
