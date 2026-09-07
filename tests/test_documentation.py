"""Scoped documentation link and command-reference checks."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def _markdown_files() -> list[Path]:
    roots = [REPO / "README.md", REPO / "docs", REPO / "skills", REPO / "templates" / "paper-workspace"]
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        elif root.is_dir():
            files.extend(root.rglob("*.md"))
    return sorted(files)


@pytest.mark.smoke
def test_internal_markdown_links_resolve():
    errors: list[str] = []
    for source in _markdown_files():
        text = source.read_text(encoding="utf-8")
        for raw in LINK.findall(text):
            target = raw.split("#", 1)[0].strip().strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if "mi-investigacion-opt" in target or "PaperEPN" in target:
                continue
            if source.name in {"MCP_OVERLEAF_OPTIONAL.md", "sync_cursor_claude.md"} and (
                target.startswith("../memory/") or target == "../.env.example"
            ):
                continue
            if source.name == "creacion-de-agentes.md" and (
                target.startswith("../rules/")
                or target.endswith("from-thesis-to-paper_master.plan.md")
            ):
                continue
            candidate = (source.parent / target).resolve()
            if not candidate.exists():
                errors.append(f"{source.relative_to(REPO)} -> {target}")
    assert not errors, "unresolved internal links:\n" + "\n".join(errors)


@pytest.mark.smoke
def test_documented_cli_commands_use_current_surface():
    text = "\n".join(path.read_text(encoding="utf-8") for path in _markdown_files())
    assert "fttp paper compile" not in text
    assert "npx from-thesis-to-paper paper compile" not in text
    assert "fttp compile" in text
    assert "fttp scaffold" in text
