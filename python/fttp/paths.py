"""Path validation shared by configuration, scaffold, and subprocess commands."""

from __future__ import annotations

import os
from pathlib import Path

from fttp.config import FttpConfigError


def canonical(path: Path | str) -> Path:
    """Resolve a path without requiring it to exist."""
    return Path(path).expanduser().resolve(strict=False)


def is_within(path: Path, root: Path) -> bool:
    try:
        canonical(path).relative_to(canonical(root))
        return True
    except ValueError:
        return False


def roots_overlap(left: Path, right: Path) -> bool:
    """Return true when either resolved root contains the other."""
    return is_within(left, right) or is_within(right, left)


def require_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FttpConfigError(f"{field} must be a non-empty string")
    return value.strip()


def require_relative(value: object, field: str) -> str:
    text = require_string(value, field)
    path = Path(text)
    if path.is_absolute() or ".." in path.parts:
        raise FttpConfigError(f"{field} must be a relative path under repoRoot")
    return text


def resolve_under(root: Path, value: object, field: str) -> Path:
    """Resolve a relative config path and reject symlink/escape traversal."""
    rel = require_relative(value, field)
    resolved_root = canonical(root)
    candidate = canonical(resolved_root / rel)
    if not is_within(candidate, resolved_root):
        raise FttpConfigError(f"{field} resolves outside repoRoot: {candidate}")
    return candidate


def validate_root_relationships(repo_root: Path, read_only_roots: object) -> None:
    if read_only_roots is None:
        return
    if not isinstance(read_only_roots, list):
        raise FttpConfigError("readOnlyRoots must be an array")
    writable = canonical(repo_root)
    for index, entry in enumerate(read_only_roots):
        text = require_string(entry, f"readOnlyRoots[{index}]")
        ro = canonical(Path(text) if os.path.isabs(text) else writable / text)
        if roots_overlap(writable, ro):
            raise FttpConfigError(
                f"readOnlyRoots[{index}] overlaps repoRoot (must be external): {ro}"
            )
