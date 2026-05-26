"""Suggest .env keys from requirements.txt and light notebook import scans."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Map PyPI-style package names to common env documentation keys (suggestions only).
_PACKAGE_ENV_HINTS: dict[str, list[str]] = {
    "gurobipy": ["# GRB_LICENSE_FILE=/path/to/gurobi.lic"],
    "osmnx": ["# OSM_CACHE_DIR=/path/to/osm-cache"],
    "geopandas": ["# GDAL_DATA=  # set if GDAL not found on PATH"],
}

_IMPORT_RE = re.compile(
    r"^\s*(?:import|from)\s+([a-zA-Z_][\w.]*)",
    re.MULTILINE,
)

_REQUIREMENT_LINE = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9_.\-]*",
)

_NOTEBOOK_IMPORT = re.compile(r'["\']import\s+([a-zA-Z_][\w.]*)')


def _parse_requirements(path: Path) -> list[str]:
    packages: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-"):
            continue
        token = line.split(";", 1)[0].strip()
        match = _REQUIREMENT_LINE.match(token)
        if match:
            name = match.group(0).lower().replace("-", "_")
            packages.append(name.split("[", 1)[0])
    return packages


def _scan_notebook_imports(path: Path, limit: int = 200) -> set[str]:
    found: set[str] = set()
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")[:500_000]
    except OSError:
        return found

    if path.suffix == ".ipynb":
        try:
            nb = json.loads(raw)
        except json.JSONDecodeError:
            return found
        for cell in nb.get("cells") or []:
            if cell.get("cell_type") != "code":
                continue
            source = cell.get("source") or []
            if isinstance(source, list):
                text = "".join(source)
            else:
                text = str(source)
            for match in _IMPORT_RE.finditer(text):
                found.add(match.group(1).split(".", 1)[0])
            if len(found) >= limit:
                break
        return found

    for match in _IMPORT_RE.finditer(raw):
        found.add(match.group(1).split(".", 1)[0])
    return found


def collect_suggestions(roots: list[Path], *, max_notebooks: int = 50) -> dict[str, set[str]]:
    """Return {source_label: set of package/module names}."""
    result: dict[str, set[str]] = {}
    nb_count = 0

    for root in roots:
        root = root.expanduser().resolve()
        if not root.exists():
            result[f"missing:{root}"] = set()
            continue

        req = root / "requirements.txt"
        if req.is_file():
            result[f"requirements:{req}"] = set(_parse_requirements(req))

        imports: set[str] = set()
        for pattern in ("**/*.ipynb", "**/*.py"):
            for path in root.glob(pattern):
                if path.is_file() and path.suffix == ".ipynb":
                    if nb_count >= max_notebooks:
                        continue
                    nb_count += 1
                imports |= _scan_notebook_imports(path)
        if imports:
            result[f"notebooks:{root}"] = imports

    return result


def _lines_from_suggestions(suggestions: dict[str, set[str]]) -> list[str]:
    lines = [
        "# Suggested by fttp env-suggest — review before copying to .env",
        "# Overleaf (optional MCP)",
        "OVERLEAF_EMAIL=you@example.com",
        "OVERLEAF_PASSWORD=your-overleaf-password-here",
        "OVERLEAF_THESIS_PROJECT_ID=",
        "# OVERLEAF_PAPER_PROJECT_ID=",
        "",
        "# Read-only roots (authoritative list: fttp.config.json readOnlyRoots)",
        "# READ_ONLY_ROOT_1=/path/to/thesis-notebooks",
        "",
    ]

    packages: set[str] = set()
    for names in suggestions.values():
        packages |= names

    if packages:
        lines.append("# Detected packages / imports (informational)")
        for pkg in sorted(packages):
            lines.append(f"#   - {pkg}")
        lines.append("")

    hinted: set[str] = set()
    for pkg in packages:
        for hint in _PACKAGE_ENV_HINTS.get(pkg, []):
            if hint not in hinted:
                lines.append(hint)
                hinted.add(hint)

    if not hinted:
        lines.append("# Gurobi (optional; optimization-or pack)")
        lines.append("# GRB_LICENSE_FILE=/path/to/gurobi.lic")
        lines.append("")

    return lines


def suggest_env(
    roots: list[Path],
    *,
    write_path: Path | None = None,
) -> tuple[list[str], int]:
    """Build suggestion lines; optionally write to write_path. Returns (lines, exit_code)."""
    suggestions = collect_suggestions(roots)
    lines = _lines_from_suggestions(suggestions)

    for label, names in sorted(suggestions.items()):
        if label.startswith("missing:"):
            print(f"fttp env-suggest: WARNING — root not found: {label.split(':', 1)[1]}", file=sys.stderr)
        elif names:
            print(f"fttp env-suggest: {label} ({len(names)} entries)")

    for line in lines:
        print(line)

    if write_path is not None:
        write_path = write_path.expanduser().resolve()
        write_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"fttp env-suggest: wrote {write_path}")

    return lines, 0


def cmd_env_suggest(roots: list[Path], write: Path | None = None) -> int:
    if not roots:
        print("fttp env-suggest: pass at least one --roots PATH", file=sys.stderr)
        return 1
    _, code = suggest_env(roots, write_path=write)
    return code
