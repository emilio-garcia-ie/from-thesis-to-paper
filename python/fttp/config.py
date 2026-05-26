"""Load workspace configuration from fttp.config.json or workspace.config.json."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

CONFIG_FILENAMES = ("fttp.config.json", "workspace.config.json")
_REQUIRED_KEYS = ("workspaceName", "repoRoot", "paper")

KNOWN_HOOKS = frozenset(
    {"lineageBuild", "tables", "evidence", "figures", "compile"}
)

WORKFLOW_PROFILES = frozenset(
    {"paper_only", "paper_audit", "paper_audit_repro", "full_pipeline"}
)
WRITING_MODES = frozenset({"compose", "thesis_adapt", "hybrid"})
TEMPLATE_SOURCES = frozenset(
    {"local_path", "zip", "url", "overleaf_template"}
)

DEFAULT_WORKFLOW_PROFILE = "paper_audit"
DEFAULT_WRITING_MODE = "thesis_adapt"

_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{2,63}$")
_OVERLEAF_PROJECT_ID_RE = re.compile(r"^[0-9a-fA-F]{24}$")


class FttpConfigError(Exception):
    """Raised when configuration cannot be loaded or validated."""


def validate_slug(slug: str, *, label: str = "workspaceSlug") -> None:
    """Raise FttpConfigError if slug does not match canonical workspace slug rules."""
    if not isinstance(slug, str) or not slug.strip():
        raise FttpConfigError(f"{label} must be a non-empty string")
    if not _SLUG_RE.match(slug):
        raise FttpConfigError(
            f"{label} '{slug}' is invalid "
            "(use lowercase letters, digits, hyphens, underscores; 3–64 chars; "
            "must start with a letter or digit)"
        )


def workflow_profile(cfg: dict[str, Any]) -> str:
    """Return workflowProfile with default paper_audit when unset."""
    val = cfg.get("workflowProfile")
    if val is None:
        return DEFAULT_WORKFLOW_PROFILE
    return str(val)


def writing_mode(cfg: dict[str, Any]) -> str:
    """Return writingMode with default thesis_adapt when unset."""
    val = cfg.get("writingMode")
    if val is None:
        return DEFAULT_WRITING_MODE
    return str(val)


_WORKFLOW_BASE_AGENTS = (
    "SA0",
    "SA1",
    "SA2",
    "SA2b",
    "SA7",
    "SA8",
    "SA9",
    "SA12",
    "SA13",
)

WORKFLOW_PROFILE_AGENTS: dict[str, tuple[str, ...]] = {
    "paper_only": _WORKFLOW_BASE_AGENTS,
    "paper_audit": _WORKFLOW_BASE_AGENTS + ("SA3", "SA4"),
    "paper_audit_repro": _WORKFLOW_BASE_AGENTS + ("SA3", "SA4", "SA6"),
    "full_pipeline": _WORKFLOW_BASE_AGENTS + ("SA3", "SA4", "SA6", "SA5", "SA11"),
}


def workflow_profile_agents(cfg: dict[str, Any]) -> tuple[str, ...]:
    """Return ordered SA ids for the resolved workflowProfile (see ARCHITECTURE §4.3)."""
    return WORKFLOW_PROFILE_AGENTS[workflow_profile(cfg)]


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
    validate_onboarding_fields(raw, config_path)

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


def _path_is_under(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def validate_onboarding_fields(
    cfg: dict[str, Any], config_path: Path | str | None = None
) -> None:
    """Validate optional onboarding v2 fields when present."""
    label = config_path or "config"

    slug = cfg.get("workspaceSlug")
    if slug is not None:
        validate_slug(slug)

    wf = cfg.get("workflowProfile")
    if wf is not None:
        if not isinstance(wf, str) or wf not in WORKFLOW_PROFILES:
            allowed = ", ".join(sorted(WORKFLOW_PROFILES))
            raise FttpConfigError(
                f"Config {label}: workflowProfile must be one of: {allowed}"
            )

    wm = cfg.get("writingMode")
    if wm is not None:
        if not isinstance(wm, str) or wm not in WRITING_MODES:
            allowed = ", ".join(sorted(WRITING_MODES))
            raise FttpConfigError(
                f"Config {label}: writingMode must be one of: {allowed}"
            )

    overleaf = cfg.get("overleafPaper")
    if overleaf is not None:
        if not isinstance(overleaf, dict):
            raise FttpConfigError(f"Config {label}: overleafPaper must be an object")
        project_id = overleaf.get("projectId", "")
        if project_id is not None and project_id != "":
            if not isinstance(project_id, str) or not _OVERLEAF_PROJECT_ID_RE.match(
                project_id.strip()
            ):
                raise FttpConfigError(
                    f"Config {label}: overleafPaper.projectId must be 24 hex characters"
                )
        display = overleaf.get("displayName")
        if display is not None and not isinstance(display, str):
            raise FttpConfigError(
                f"Config {label}: overleafPaper.displayName must be a string"
            )

    copy_policy = cfg.get("copyPolicy")
    if copy_policy is not None:
        if not isinstance(copy_policy, dict):
            raise FttpConfigError(f"Config {label}: copyPolicy must be an object")
        max_mb = copy_policy.get("maxArtifactMb")
        if max_mb is not None:
            if not isinstance(max_mb, (int, float)) or max_mb <= 0:
                raise FttpConfigError(
                    f"Config {label}: copyPolicy.maxArtifactMb must be a positive number"
                )
        allow_symlinks = copy_policy.get("allowSymlinks")
        if allow_symlinks is not None and not isinstance(allow_symlinks, bool):
            raise FttpConfigError(
                f"Config {label}: copyPolicy.allowSymlinks must be a boolean"
            )

    read_only = cfg.get("readOnlyRoots")
    if read_only is not None:
        if not isinstance(read_only, list):
            raise FttpConfigError(f"Config {label}: readOnlyRoots must be an array")
        root = repo_root(cfg) if cfg.get("repoRoot") else None
        for idx, entry in enumerate(read_only):
            if not isinstance(entry, str) or not entry.strip():
                raise FttpConfigError(
                    f"Config {label}: readOnlyRoots[{idx}] must be a non-empty path string"
                )
            if root is not None and _path_is_under(Path(entry).expanduser(), root):
                raise FttpConfigError(
                    f"Config {label}: readOnlyRoots[{idx}] must not be under repoRoot"
                )


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
            for path_key in ("mainTex", "guidelines", "templatePath", "build"):
                val = profile.get(path_key)
                if val is not None and (
                    not isinstance(val, str) or not _is_relative_repo_path(val)
                ):
                    raise FttpConfigError(
                        f"Config {config_path}: venueProfiles.{name}.{path_key} "
                        "must be a relative path under repoRoot"
                    )

            url = profile.get("authorGuidelinesUrl")
            if url is not None:
                if not isinstance(url, str) or not url.strip().startswith(
                    ("http://", "https://")
                ):
                    raise FttpConfigError(
                        f"Config {config_path}: venueProfiles.{name}.authorGuidelinesUrl "
                        "must be an http(s) URL"
                    )

            source = profile.get("templateSource")
            if source is not None:
                if not isinstance(source, str) or source not in TEMPLATE_SOURCES:
                    allowed = ", ".join(sorted(TEMPLATE_SOURCES))
                    raise FttpConfigError(
                        f"Config {config_path}: venueProfiles.{name}.templateSource "
                        f"must be one of: {allowed}"
                    )

            deferred = profile.get("templateDeferred")
            if deferred is not None and not isinstance(deferred, bool):
                raise FttpConfigError(
                    f"Config {config_path}: venueProfiles.{name}.templateDeferred "
                    "must be a boolean"
                )


def primary_venue_profile(cfg: dict[str, Any]) -> dict[str, Any] | None:
    """Return venueProfiles.primary if present."""
    paper = cfg.get("paper") or {}
    profiles = paper.get("venueProfiles") or {}
    if not isinstance(profiles, dict):
        return None
    profile = profiles.get("primary")
    return profile if isinstance(profile, dict) else None


def doctor_workspace_checks(
    cfg: dict[str, Any],
) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for extended doctor validation."""
    errors: list[str] = []
    warnings: list[str] = []
    root = repo_root(cfg)

    slug = cfg.get("workspaceSlug")
    if slug:
        try:
            validate_slug(slug)
        except FttpConfigError as exc:
            errors.append(str(exc))
        else:
            if root.name != slug:
                warnings.append(
                    f"workspaceSlug '{slug}' does not match repoRoot "
                    f"dirname '{root.name}'"
                )

    for idx, entry in enumerate(cfg.get("readOnlyRoots") or []):
        if not isinstance(entry, str):
            continue
        ro_path = Path(entry).expanduser()
        if _path_is_under(ro_path, root):
            errors.append(
                f"readOnlyRoots[{idx}] is under repoRoot (must be external): {ro_path}"
            )

    overleaf = cfg.get("overleafPaper") or {}
    if isinstance(overleaf, dict):
        project_id = (overleaf.get("projectId") or "").strip()
        if project_id and not _OVERLEAF_PROJECT_ID_RE.match(project_id):
            errors.append(
                "overleafPaper.projectId must be 24 hexadecimal characters"
            )

    primary = primary_venue_profile(cfg)
    if primary:
        url = (primary.get("authorGuidelinesUrl") or "").strip()
        guidelines_rel = primary.get("guidelines")
        guidelines_path = (
            root / guidelines_rel if isinstance(guidelines_rel, str) else None
        )
        default_guidelines = root / cfg.get("paper", {}).get("dir", "paper") / "JOURNAL_GUIDELINES.md"
        has_guidelines = bool(url) or (
            guidelines_path is not None and guidelines_path.is_file()
        ) or default_guidelines.is_file()
        if not has_guidelines:
            errors.append(
                "primary venue: set authorGuidelinesUrl, venueProfiles.primary.guidelines, "
                f"or create {default_guidelines.relative_to(root)}"
            )

        if primary.get("templateDeferred") is True:
            pass
        elif primary.get("templatePath"):
            template_dir = root / primary["templatePath"]
            if not template_dir.is_dir():
                errors.append(
                    f"primary venue templatePath not found (or not a directory): {template_dir}"
                )
        else:
            errors.append(
                "primary venue: set templatePath or templateDeferred: true"
            )

    paper = cfg.get("paper") or {}
    active_key = paper.get("activeVenue")
    if active_key:
        profile = active_venue_profile(cfg) or primary_venue_profile(cfg) or {}
        if profile.get("templateDeferred") is not True:
            template_rel = profile.get("templatePath")
            if template_rel:
                template_dir = root / template_rel
                if template_dir.is_dir() and not any(template_dir.iterdir()):
                    warnings.append(
                        f"venue templatePath is empty: "
                        f"{template_dir.relative_to(root)}"
                    )
            else:
                latex_dir = paper_dir(cfg) / "latex"
                if latex_dir.is_dir() and not any(latex_dir.iterdir()):
                    warnings.append(
                        f"paper/latex/ is empty (activeVenue={active_key}; "
                        "copy BYO template files or set templateDeferred)"
                    )

    return errors, warnings


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
