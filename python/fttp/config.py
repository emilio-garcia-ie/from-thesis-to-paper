"""Load workspace configuration from fttp.config.json or workspace.config.json."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

CONFIG_FILENAMES = ("fttp.config.json", "workspace.config.json")
_REQUIRED_KEYS = ("workspaceName", "repoRoot", "paper")


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

    raw["_configPath"] = str(config_path)
    return raw


def repo_root(cfg: dict[str, Any]) -> Path:
    return Path(cfg["repoRoot"]).expanduser().resolve()


def paper_dir(cfg: dict[str, Any]) -> Path:
    return repo_root(cfg) / cfg["paper"]["dir"]


def paper_main_tex(cfg: dict[str, Any]) -> Path:
    return paper_dir(cfg) / cfg["paper"]["mainTex"]
