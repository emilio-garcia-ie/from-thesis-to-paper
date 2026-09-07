"""Suggest .env keys from requirements.txt and light notebook import scans."""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field
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

# These limits are deliberately conservative: env-suggest is an inspection
# helper and must never turn a large consumer repository into an unbounded
# filesystem or memory operation.
MAX_NOTEBOOKS = 50
MAX_PYTHON_FILES = 200
MAX_VISITED_ENTRIES = 10_000
MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_TOTAL_BYTES = 50 * 1024 * 1024
_PRUNED_DIRS = {".git", ".venv", "node_modules", "__pycache__"}


@dataclass
class _ScanState:
    visited: int = 0
    notebooks: int = 0
    python_files: int = 0
    bytes_read: int = 0
    incomplete: list[str] = field(default_factory=list)

    def note(self, message: str) -> None:
        if message not in self.incomplete:
            self.incomplete.append(message)


def _parse_requirements(path: Path, *, state: _ScanState | None = None) -> list[str]:
    packages: list[str] = []
    try:
        size = path.stat().st_size
        remaining = MAX_TOTAL_BYTES - state.bytes_read if state is not None else MAX_FILE_BYTES
        if size > MAX_FILE_BYTES or remaining <= 0:
            if state is not None:
                state.note(f"requirements input exceeds scan budget: {path}")
            return packages
        read_limit = min(size, MAX_FILE_BYTES, remaining)
        with path.open("rb") as handle:
            raw = handle.read(read_limit)
        if state is not None:
            state.bytes_read += len(raw)
            if len(raw) < size:
                state.note(f"requirements input was capped at {read_limit} bytes: {path}")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            if state is not None:
                state.note(f"malformed UTF-8 requirements input: {path}")
            return packages
    except OSError:
        if state is not None:
            state.note(f"unreadable input: {path}")
        return packages
    for line in text.splitlines():
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


def _scan_notebook_imports(
    path: Path,
    limit: int = 200,
    *,
    state: _ScanState | None = None,
) -> set[str]:
    found: set[str] = set()
    try:
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            if state is not None:
                state.note(f"file exceeds {MAX_FILE_BYTES} bytes: {path}")
            return found
        remaining = MAX_TOTAL_BYTES - state.bytes_read if state is not None else MAX_FILE_BYTES
        if remaining <= 0:
            if state is not None:
                state.note(f"total read budget exceeded at: {path}")
            return found
        read_limit = min(size, MAX_FILE_BYTES, remaining)
        with path.open("rb") as handle:
            raw_bytes = handle.read(read_limit)
        if state is not None:
            state.bytes_read += len(raw_bytes)
            if len(raw_bytes) < size:
                state.note(f"file read was capped at {read_limit} bytes: {path}")
        try:
            raw = raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            if state is not None:
                state.note(f"malformed UTF-8 input: {path}")
            return found
    except OSError:
        if state is not None:
            state.note(f"unreadable input: {path}")
        return found

    if path.suffix == ".ipynb":
        try:
            nb = json.loads(raw)
        except json.JSONDecodeError:
            if state is not None:
                state.note(f"malformed notebook JSON: {path}")
            return found
        if not isinstance(nb, dict) or not isinstance(nb.get("cells"), list):
            if state is not None:
                state.note(f"malformed notebook cells: {path}")
            return found
        for cell in nb.get("cells") or []:
            if not isinstance(cell, dict):
                if state is not None:
                    state.note(f"malformed notebook cell: {path}")
                continue
            cell_type = cell.get("cell_type")
            if not isinstance(cell_type, str):
                if state is not None:
                    state.note(f"malformed notebook cell_type: {path}")
                continue
            if cell_type != "code":
                continue
            source = cell.get("source")
            if isinstance(source, list) and all(isinstance(line, str) for line in source):
                text = "".join(source)
            elif isinstance(source, str):
                text = source
            else:
                if state is not None:
                    state.note(f"malformed notebook cell source: {path}")
                continue
            for match in _IMPORT_RE.finditer(text):
                found.add(match.group(1).split(".", 1)[0])
            if len(found) >= limit:
                break
        return found

    for match in _IMPORT_RE.finditer(raw):
        found.add(match.group(1).split(".", 1)[0])
    return found


def _collect_suggestions_report(
    roots: list[Path], *, max_notebooks: int = MAX_NOTEBOOKS
) -> tuple[dict[str, set[str]], _ScanState]:
    """Return suggestions and bounded-scan diagnostics."""
    result: dict[str, set[str]] = {}
    state = _ScanState()

    for root in roots:
        requested_root = root.expanduser()
        if requested_root.is_symlink():
            result[f"unreadable:{requested_root}"] = set()
            state.note(f"root is a symlink: {requested_root}")
            continue
        root = requested_root.resolve(strict=False)
        if not root.exists():
            result[f"missing:{root}"] = set()
            state.note(f"root not found: {root}")
            continue
        if not root.is_dir() or root.is_symlink():
            result[f"unreadable:{root}"] = set()
            state.note(f"root is not a directory: {root}")
            continue

        req = root / "requirements.txt"
        if req.is_symlink():
            state.note(f"symlink skipped: {req}")
        elif req.is_file():
            result[f"requirements:{req}"] = set(_parse_requirements(req, state=state))

        imports: set[str] = set()
        def _walk_error(error: OSError) -> None:
            state.note(f"unreadable directory: {getattr(error, 'filename', root)}")

        # ``os.walk`` consumes a whole directory before yielding it.  Traverse
        # through scandir instead so the global entry budget bounds real work,
        # not merely the number we report after the fact.
        pending = [root]
        exhausted = False
        while pending and not exhausted:
            current_path = pending.pop()
            entries: list[os.DirEntry[str]] = []
            try:
                with os.scandir(current_path) as iterator:
                    while state.visited < MAX_VISITED_ENTRIES:
                        try:
                            entry = next(iterator)
                        except StopIteration:
                            break
                        state.visited += 1
                        entries.append(entry)
                    if state.visited >= MAX_VISITED_ENTRIES:
                        # Do not request one more entry merely to distinguish
                        # an exact-size directory from an over-limit one: that
                        # extra request defeats the advertised hard bound.
                        state.note(
                            f"visited-entry limit ({MAX_VISITED_ENTRIES}) reached under: {root}"
                        )
                        exhausted = True
            except OSError as exc:
                _walk_error(exc)
                continue
            # A partially enumerated directory is deliberately not processed:
            # processing it would make results depend on filesystem order.
            if exhausted:
                break
            for entry in sorted(entries, key=lambda item: item.name, reverse=True):
                path = Path(entry.path)
                try:
                    if entry.is_symlink():
                        continue
                    if entry.is_dir(follow_symlinks=False):
                        if entry.name not in _PRUNED_DIRS:
                            pending.append(path)
                        continue
                    if not entry.is_file(follow_symlinks=False):
                        continue
                except OSError:
                    state.note(f"unreadable input: {path}")
                    continue
                if path.suffix == ".ipynb":
                    if state.notebooks >= max_notebooks:
                        state.note(f"notebook limit ({max_notebooks}) reached under: {root}")
                        continue
                    state.notebooks += 1
                    imports |= _scan_notebook_imports(path, state=state)
                elif path.suffix == ".py":
                    if state.python_files >= MAX_PYTHON_FILES:
                        state.note(f"Python-file limit ({MAX_PYTHON_FILES}) reached under: {root}")
                        continue
                    state.python_files += 1
                    imports |= _scan_notebook_imports(path, state=state)
        if imports:
            result[f"notebooks:{root}"] = imports

    return result, state


def collect_suggestions(roots: list[Path], *, max_notebooks: int = MAX_NOTEBOOKS) -> dict[str, set[str]]:
    """Return {source_label: set of package/module names}.

    This compatibility wrapper intentionally retains the historical return
    shape.  ``suggest_env`` uses the richer internal report to expose partial
    scans to callers and to the command line.
    """
    result, _ = _collect_suggestions_report(roots, max_notebooks=max_notebooks)
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
    suggestions, state = _collect_suggestions_report(roots)
    lines = _lines_from_suggestions(suggestions)

    for label, names in sorted(suggestions.items()):
        if label.startswith("missing:"):
            print(f"fttp env-suggest: WARNING — root not found: {label.split(':', 1)[1]}", file=sys.stderr)
        elif names:
            print(f"fttp env-suggest: {label} ({len(names)} entries)")

    for line in lines:
        print(line)

    if write_path is not None:
        requested_output = write_path.expanduser()
        if requested_output.exists() or requested_output.is_symlink():
            print(
                f"fttp env-suggest: refusing to overwrite existing output: {requested_output}",
                file=sys.stderr,
            )
            return lines, 1
        write_path = requested_output.resolve(strict=False)
        try:
            write_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
        except OSError as exc:
            print(f"fttp env-suggest: cannot write {write_path}: {exc}", file=sys.stderr)
            return lines, 1
        print(f"fttp env-suggest: wrote {write_path}")

    if state.incomplete:
        print(
            "fttp env-suggest: incomplete scan ({}); rerun after addressing the limits or inputs".format(
                "; ".join(state.incomplete[:5])
            ),
            file=sys.stderr,
        )
        return lines, 1
    return lines, 0


def cmd_env_suggest(roots: list[Path], write: Path | None = None) -> int:
    if not roots:
        print("fttp env-suggest: pass at least one --roots PATH", file=sys.stderr)
        return 1
    _, code = suggest_env(roots, write_path=write)
    return code
