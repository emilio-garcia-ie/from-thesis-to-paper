"""CLI command handlers: hook delegation and doctor."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

from fttp.config import (
    FttpConfigError,
    KNOWN_HOOKS,
    doctor_workspace_checks,
    hook_path,
    load_config,
    paper_dir,
    repo_root,
    resolve_active_main_tex,
    workflow_profile,
    writing_mode,
)


def _missing(msg: str) -> int:
    print(msg, file=sys.stderr)
    return 1


def run_hook(name: str, cfg: dict[str, Any]) -> int:
    """Run hooks.<name> script under repoRoot; propagate exit code."""
    if name not in KNOWN_HOOKS:
        return _missing(f"fttp: unknown hook '{name}'")

    script = hook_path(cfg, name)
    if script is None:
        return _missing(
            f"fttp: hooks.{name} is not set in config.\n"
            f"  Add hooks.{name} (relative path under repoRoot) in fttp.config.json."
        )

    root = repo_root(cfg)
    if not script.is_file():
        return _missing(
            f"fttp: hook script not found:\n  {script}\n"
            f"  repoRoot: {root}\n"
            f"  Configure hooks.{name} or create the script."
        )

    print(f"fttp: running hooks.{name} -> {script.relative_to(root)}")
    if script.suffix == ".py":
        cmd = [sys.executable, str(script)]
    else:
        cmd = [str(script)]

    result = subprocess.run(
        cmd,
        cwd=str(root),
        check=False,
    )
    return int(result.returncode)


def cmd_doctor(cfg: dict[str, Any] | None = None) -> int:
    try:
        cfg = cfg or load_config()
    except FttpConfigError as exc:
        return _missing(f"fttp doctor: {exc}")

    root = repo_root(cfg)
    issues: list[str] = []
    warnings: list[str] = []
    print(f"fttp doctor: workspace={cfg.get('workspaceName')}")
    slug = cfg.get("workspaceSlug")
    if slug:
        print(f"  workspaceSlug: {slug}")
    print(f"  workflowProfile: {workflow_profile(cfg)}")
    print(f"  writingMode: {writing_mode(cfg)}")
    print(f"  config: {cfg.get('_configPath')}")
    print(f"  repoRoot: {root}")

    if not root.is_dir():
        issues.append(f"repoRoot does not exist: {root}")

    doc_errors, doc_warnings = doctor_workspace_checks(cfg)
    issues.extend(doc_errors)
    warnings.extend(doc_warnings)

    pdir = paper_dir(cfg)
    if not pdir.is_dir():
        issues.append(f"paper.dir missing: {pdir}")

    main_tex = resolve_active_main_tex(cfg)
    active = (cfg.get("paper") or {}).get("activeVenue", "")
    print(f"  activeVenue: {active or '(default)'}")
    print(f"  mainTex: {main_tex}")
    if not main_tex.is_file():
        issues.append(f"main TeX not found: {main_tex}")

    hooks = cfg.get("hooks") or {}
    if not hooks:
        issues.append("hooks block missing (pipeline commands need hooks.*)")
    else:
        for name in sorted(KNOWN_HOOKS):
            rel = hooks.get(name)
            if not rel:
                issues.append(f"hooks.{name} not configured")
                continue
            path = root / rel
            status = "OK" if path.is_file() else "MISSING"
            print(f"  hooks.{name}: {rel} [{status}]")
            if status == "MISSING":
                issues.append(f"hooks.{name} path missing: {path}")

    evidence = cfg.get("evidence") or {}
    for key in ("catalog", "lineageCsv"):
        rel = evidence.get(key)
        if rel:
            path = root / rel
            status = "OK" if path.is_file() else "MISSING"
            print(f"  evidence.{key}: {rel} [{status}]")

    packs = cfg.get("packs") or []
    if packs:
        print(f"  packs: {', '.join(packs)}")

    overleaf = cfg.get("overleafPaper") or {}
    if isinstance(overleaf, dict) and overleaf.get("projectId"):
        print(f"  overleafPaper.projectId: {overleaf.get('projectId')}")

    for warn in warnings:
        print(f"  WARNING: {warn}")

    if issues:
        print("fttp doctor: FAIL", file=sys.stderr)
        for item in issues:
            print(f"  - {item}", file=sys.stderr)
        return 1

    if warnings:
        print("fttp doctor: OK (with warnings)")
    else:
        print("fttp doctor: OK")
    return 0


def cmd_tables(cfg: dict[str, Any] | None = None) -> int:
    try:
        cfg = cfg or load_config()
    except FttpConfigError as exc:
        return _missing(f"fttp tables: {exc}")
    return run_hook("tables", cfg)


def cmd_evidence(cfg: dict[str, Any] | None = None) -> int:
    try:
        cfg = cfg or load_config()
    except FttpConfigError as exc:
        return _missing(f"fttp evidence: {exc}")
    return run_hook("evidence", cfg)


def cmd_figures(cfg: dict[str, Any] | None = None) -> int:
    try:
        cfg = cfg or load_config()
    except FttpConfigError as exc:
        return _missing(f"fttp figures: {exc}")
    return run_hook("figures", cfg)


def _resolve_compile_target(cfg: dict[str, Any]) -> tuple[Path | None, str]:
    """Return (script_path, mode) for compile: venue build, hook compile, or None."""
    from fttp.config import active_venue_profile

    profile = active_venue_profile(cfg)
    if profile and profile.get("build"):
        return repo_root(cfg) / profile["build"], "venue.build"

    hook = hook_path(cfg, "compile")
    if hook is not None:
        return hook, "hooks.compile"
    return None, "pdf-check"


def cmd_compile(cfg: dict[str, Any] | None = None) -> int:
    try:
        cfg = cfg or load_config()
    except FttpConfigError as exc:
        return _missing(f"fttp compile: {exc}")

    script, mode = _resolve_compile_target(cfg)
    if script is not None:
        if not script.is_file():
            return _missing(f"fttp compile: {mode} script not found:\n  {script}")
        print(f"fttp compile: running {mode} -> {script}")
        root = repo_root(cfg)
        cmd = [sys.executable, str(script)] if script.suffix == ".py" else [str(script)]
        result = subprocess.run(cmd, cwd=str(root), check=False)
        return int(result.returncode)

    main_tex = resolve_active_main_tex(cfg)
    pdf = main_tex.with_suffix(".pdf")
    if not main_tex.is_file():
        return _missing(
            f"fttp compile: main TeX not found:\n  {main_tex}\n"
            "  Set hooks.compile or paper.venueProfiles[].build."
        )
    if not pdf.is_file():
        return _missing(
            f"fttp compile: PDF not found (run build hook or latexmk):\n  {pdf}"
        )

    print(f"fttp compile: OK — {pdf} exists")
    return 0


def cmd_lineage_build(cfg: dict[str, Any] | None = None) -> int:
    try:
        cfg = cfg or load_config()
    except FttpConfigError as exc:
        return _missing(f"fttp lineage build: {exc}")
    return run_hook("lineageBuild", cfg)


def cmd_lineage_validate(csv_path: Path | None, cfg: dict[str, Any] | None = None) -> int:
    try:
        cfg = cfg or load_config()
    except FttpConfigError as exc:
        return _missing(f"fttp lineage validate: {exc}")

    from fttp.evidence.csv_lineage import validate_lineage_csv

    root = repo_root(cfg)
    if csv_path is None:
        evidence = cfg.get("evidence") or {}
        rel = evidence.get("lineageCsv")
        if not rel:
            return _missing(
                "fttp lineage validate: pass --csv or set evidence.lineageCsv in config."
            )
        csv_path = root / rel

    csv_path = csv_path.expanduser().resolve()
    if not csv_path.is_file():
        return _missing(f"fttp lineage validate: CSV not found:\n  {csv_path}")

    errors = validate_lineage_csv(csv_path)
    if errors:
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        print(f"fttp lineage validate: FAIL ({len(errors)} issue(s))", file=sys.stderr)
        return 1

    print(f"fttp lineage validate: OK — {csv_path}")
    return 0
