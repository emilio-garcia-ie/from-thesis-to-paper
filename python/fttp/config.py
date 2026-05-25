"""Load workspace configuration from fttp.config.json or workspace.config.json."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

CONFIG_FILENAMES = ("fttp.config.json", "workspace.config.json")
_REQUIRED_KEYS = ("workspaceName", "repoRoot", "paper")

KNOWN_HOOKS = frozenset(
    {"lineageBuild", "tables", "evidence", "figures", "compile"}
)


class FttpConfigError(Exception):
    """Raised when configuration cannot be loaded or validated."""


def resolve_config_path(start: Path | None = None) -> Path | None:
    """Return the config file path, or None if not found."""
    env_path = os.environ.get("FTTP_CONFIG", "").strip()
    if env_path:
        path = Path(env_path).expanduser().resolve()
        return path if path.is_file() else None

    directory = (start or Path.cwd()).resolve()
    for name in CONFIG_FILENAMES:
        candidate = directory / name
        if candidate.is_file():
            return candidate
    return None


def load_config(path: Path | None = None) -> dict[str, Any]:
    """Load and minimally validate workspace JSON config."""
    config_path = path or resolve_config_path()
    if config_path is None:
        names = ", ".join(CONFIG_FILENAMES)
        raise FttpConfigError(
            "No workspace config found. "
            f"Create {names} in the repo root, or set FTTP_CONFIG to an absolute path."
        )

    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise FttpConfigError(f"Invalid JSON in {config_path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise FttpConfigError(f"Config root must be a JSON object: {config_path}")

    missing = [key for key in _REQUIRED_KEYS if key not in raw]
    if missing:
        raise FttpConfigError(
            f"Config {config_path} is missing required field(s): {', '.join(missing)}"
        )

    paper = raw.get("paper")
    if not isinstance(paper, dict):
        raise FttpConfigError(f"Config {config_path}: 'paper' must be an object")

    for field in ("dir", "mainTex"):
        if field not in paper:
            raise FttpConfigError(
                f"Config {config_path}: paper.{field} is required"
            )

    validate_hooks(raw, config_path)
    validate_venue_profiles(raw, config_path)

    raw["_configPath"] = str(config_path)
    return raw


def _is_relative_repo_path(value: str) -> bool:
    if not value or not isinstance(value, str):
        return False
    p = Path(value)
    if p.is_absolute():
        return False
    if ".." in p.parts:
        return False
    return True


def validate_hooks(cfg: dict[str, Any], config_path: Path | str | None = None) -> None:
    """Validate optional hooks block: known keys, relative paths."""
    hooks = cfg.get("hooks")
    if hooks is None:
        return
    if not isinstance(hooks, dict):
        label = config_path or "config"
        raise FttpConfigError(f"Config {label}: 'hooks' must be an object")

    for key, rel in hooks.items():
        if key not in KNOWN_HOOKS:
            raise FttpConfigError(
                f"Config {config_path}: unknown hook '{key}' "
                f"(allowed: {', '.join(sorted(KNOWN_HOOKS))})"
            )
        if not isinstance(rel, str) or not _is_relative_repo_path(rel):
            raise FttpConfigError(
                f"Config {config_path}: hooks.{key} must be a relative path "
                "under repoRoot (no '..' or absolute paths)"
            )


def validate_venue_profiles(
    cfg: dict[str, Any], config_path: Path | str | None = None
) -> None:
    """Validate optional paper.venueProfiles and paper.activeVenue."""
    paper = cfg.get("paper")
    if not isinstance(paper, dict):
        return

    profiles = paper.get("venueProfiles")
    active = paper.get("activeVenue")

    if profiles is None and active is None:
        return

    if profiles is not None and not isinstance(profiles, dict):
        raise FttpConfigError(
            f"Config {config_path}: paper.venueProfiles must be an object"
        )

    if active is not None:
        if not isinstance(active, str) or not active.strip():
            raise FttpConfigError(
                f"Config {config_path}: paper.activeVenue must be a non-empty string"
            )
        if profiles is not None and active not in profiles:
            raise FttpConfigError(
                f"Config {config_path}: paper.activeVenue '{active}' "
                "not found in paper.venueProfiles"
            )

    if profiles:
        for name, profile in profiles.items():
            if not isinstance(profile, dict):
                raise FttpConfigError(
                    f"Config {config_path}: venueProfiles.{name} must be an object"
                )
            for path_key in ("mainTex", "guidelines", "build"):
                val = profile.get(path_key)
                if val is not None and (
                    not isinstance(val, str) or not _is_relative_repo_path(val)
                ):
                    raise FttpConfigError(
                        f"Config {config_path}: venueProfiles.{name}.{path_key} "
                        "must be a relative path under repoRoot"
                    )


def repo_root(cfg: dict[str, Any]) -> Path:
    return Path(cfg["repoRoot"]).expanduser().resolve()


def paper_dir(cfg: dict[str, Any]) -> Path:
    return repo_root(cfg) / cfg["paper"]["dir"]


def active_venue_profile(cfg: dict[str, Any]) -> dict[str, Any] | None:
    paper = cfg.get("paper") or {}
    active = paper.get("activeVenue")
    profiles = paper.get("venueProfiles") or {}
    if not active or not isinstance(profiles, dict):
        return None
    profile = profiles.get(active)
    return profile if isinstance(profile, dict) else None


def resolve_active_main_tex(cfg: dict[str, Any]) -> Path:
    """Return main TeX for active venue profile or paper.mainTex default."""
    profile = active_venue_profile(cfg)
    if profile and profile.get("mainTex"):
        return paper_dir(cfg) / profile["mainTex"]
    return paper_dir(cfg) / cfg["paper"]["mainTex"]


def paper_main_tex(cfg: dict[str, Any]) -> Path:
    """Alias for resolve_active_main_tex (venue-aware)."""
    return resolve_active_main_tex(cfg)


def hook_path(cfg: dict[str, Any], name: str) -> Path | None:
    hooks = cfg.get("hooks") or {}
    rel = hooks.get(name)
    if not rel:
        return None
    return repo_root(cfg) / rel
