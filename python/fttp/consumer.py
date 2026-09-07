"""Create self-contained consumer workspaces from canonical FTTP resources."""

from __future__ import annotations

import hashlib
import json
import re
from importlib import resources
from pathlib import Path
from typing import Iterator

from fttp import __version__
from fttp.config import FttpConfigError, load_config, validate_slug
from fttp.scaffold import scaffold_workspace

_AGENTS = frozenset({"cursor", "claude", "codex"})
_GUIDES = (
    "ONBOARDING_RATIONALE.md",
    "USER_APPROVAL_GATES.md",
    "WORKSPACE_MODEL.md",
    "VENUE_TEMPLATE_ONBOARDING.md",
    "PACKS.md",
)


def _checkout_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _resource_tree(name: str) -> object:
    """Return a checkout tree when available, otherwise installed resources."""
    checkout = _checkout_root()
    source = {
        "memory": checkout / "templates" / "memory",
        "consumer": checkout / "templates" / "consumer",
        "skills": checkout / "skills",
        "docs": checkout / "docs",
    }[name]
    if source.is_dir():
        return source
    bundled = resources.files("fttp").joinpath("_resources", name)
    if not bundled.is_dir():
        raise FttpConfigError(f"Installed consumer resource is missing: {name}")
    return bundled


def _copy_new(source: object, destination: Path, manifest: dict[str, str]) -> None:
    if destination.is_symlink():
        raise FttpConfigError(f"Cannot create consumer resource through symlink: {destination}")
    if bool(getattr(source, "is_dir")()):
        if destination.exists() and not destination.is_dir():
            raise FttpConfigError(f"Cannot create directory over file: {destination}")
        destination.mkdir(parents=True, exist_ok=True)
        for child in source.iterdir():
            _copy_new(child, destination / child.name, manifest)
        return
    if destination.exists():
        raise FttpConfigError(f"Consumer resource already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as incoming, destination.open("xb") as outgoing:
        payload = incoming.read()
        outgoing.write(payload)
    manifest[str(destination)] = hashlib.sha256(payload).hexdigest()


def _copy_selected_skills(workspace: Path, agent: str, manifest: dict[str, str]) -> None:
    source = _resource_tree("skills")
    target = {
        "cursor": workspace / ".cursor" / "skills",
        "claude": workspace / ".claude" / "skills",
        "codex": workspace / ".agents" / "skills",
    }[agent]
    core = source.joinpath("core")
    for skill in sorted(core.iterdir(), key=lambda item: item.name):
        if skill.name.endswith(".md"):
            destination = target / skill.name[:-3] / "SKILL.md"
            if destination.exists() or destination.is_symlink():
                raise FttpConfigError(f"Consumer resource already exists: {destination}")
            rendered = _render_skill(skill.read_text(encoding="utf-8"))
            _write_new(destination, rendered, manifest)


def _render_skill(content: str) -> str:
    """Rebase canonical guide links for a flattened workspace skill."""
    return re.sub(
        r"(?<=\]\()\.\./\.\./docs/",
        "../../../.fttp/guides/",
        content,
    )


def _write_new(path: Path, content: str, manifest: dict[str, str]) -> None:
    if path.is_symlink() or path.exists():
        raise FttpConfigError(f"Consumer resource already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    manifest[str(path)] = hashlib.sha256(content.encode("utf-8")).hexdigest()


def _entry_instruction(agent: str) -> tuple[Path, str]:
    prompt = (
        "# FTTP workspace\n\n"
        "Read `GETTING_STARTED.md` and `.fttp/guides/ONBOARDING_RATIONALE.md` before intake. "
        "Explain why each question matters. Do not access external sources, upload data, "
        "or mark approval gates complete without explicit user confirmation. Treat configured "
        "readOnlyRoots as read-only.\n"
    )
    if agent == "cursor":
        return Path(".cursor/rules/fttp-workspace.mdc"), "---\nalwaysApply: true\n---\n\n" + prompt
    if agent == "claude":
        return Path("CLAUDE.md"), prompt
    return Path("AGENTS.md"), prompt


def initialize_workspace(
    destination: Path,
    *,
    agent: str,
    read_only_roots: list[Path] | None = None,
) -> Path:
    """Create a fresh workspace with one selected agent integration."""
    if agent not in _AGENTS:
        raise FttpConfigError(f"agent must be one of: {', '.join(sorted(_AGENTS))}")
    destination = destination.expanduser().resolve(strict=False)
    validate_slug(destination.name, label="workspace directory name")
    workspace = scaffold_workspace(destination.name, destination.parent)
    created: list[Path] = []
    manifest: dict[str, str] = {}
    try:
        config_path = workspace / "fttp.config.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        config["agentStack"] = agent
        config["readOnlyRoots"] = [str(path.expanduser().resolve()) for path in read_only_roots or []]
        config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

        memory = _resource_tree("memory")
        for item in memory.iterdir():
            if item.name == "README.md":
                continue
            name = item.name.replace("_TEMPLATE", "")
            target = workspace / "memory" / name
            _copy_new(item, target, manifest)
            created.append(target)

        docs = _resource_tree("docs")
        for name in _GUIDES:
            target = workspace / ".fttp" / "guides" / name
            _copy_new(docs.joinpath(name), target, manifest)
            created.append(target)
        consumer = _resource_tree("consumer")
        getting_started = workspace / "GETTING_STARTED.md"
        _copy_new(consumer.joinpath("GETTING_STARTED.md"), getting_started, manifest)
        created.append(getting_started)
        _copy_selected_skills(workspace, agent, manifest)

        entry_path, entry = _entry_instruction(agent)
        _write_new(workspace / entry_path, entry, manifest)
        created.append(workspace / entry_path)
        relative_manifest = {
            str(Path(path).relative_to(workspace)): digest
            for path, digest in manifest.items()
        }
        manifest_path = workspace / ".fttp" / "resource-manifest.json"
        _write_new(
            manifest_path,
            json.dumps(
                {"fttpVersion": __version__, "agent": agent, "files": relative_manifest},
                indent=2,
                sort_keys=True,
            )
            + "\n",
            manifest,
        )
        # Validate the final user-visible configuration after resources are in place.
        load_config(config_path)
        return workspace
    except Exception:
        # init always creates a new workspace. Remove only resources it added;
        # scaffold owns rollback for its own transaction.
        for path in sorted(created, key=lambda item: len(item.parts), reverse=True):
            try:
                if path.is_file() and not path.is_symlink():
                    path.unlink()
            except OSError:
                pass
        raise


def consumer_status(cfg: dict) -> list[str]:
    """Return actionable setup observations without claiming paper readiness."""
    root = Path(cfg["repoRoot"])
    notices = [f"workspace: {root}", f"agent: {cfg.get('agentStack', 'not selected')}"]
    if not (root / "GETTING_STARTED.md").is_file():
        notices.append("missing GETTING_STARTED.md; use `fttp init` for a guided workspace")
    if not cfg.get("readOnlyRoots"):
        notices.append("read-only sources are not configured; complete intake before evidence work")
    hooks = cfg.get("hooks") or {}
    placeholders = [name for name, rel in hooks.items() if (root / rel).is_file() and "FTTP_PLACEHOLDER_HOOK" in (root / rel).read_text(encoding="utf-8", errors="replace")]
    if placeholders:
        notices.append("placeholder hooks: " + ", ".join(sorted(placeholders)))
    notices.append("next: open GETTING_STARTED.md and begin guided intake")
    return notices
