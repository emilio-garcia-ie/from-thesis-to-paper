"""Smoke tests: canonical skills/ mirrors match .cursor/skills/ and .claude/skills/."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
CORE_SRC = REPO / "skills" / "core"
PACK_SRC = REPO / "skills" / "packs" / "optimization-or"
CURSOR_ROOT = REPO / ".cursor" / "skills"
CLAUDE_ROOT = REPO / ".claude" / "skills"

from scripts.sync_skills import expected_mirror


def _canonical_core_slugs() -> list[str]:
    return sorted(p.stem for p in CORE_SRC.glob("*.md"))


def _canonical_pack_slugs() -> list[str]:
    if not PACK_SRC.is_dir():
        return []
    return sorted(p.stem for p in PACK_SRC.glob("*.md"))


def _mirror_path(stack_root: Path, slug: str, *, pack: bool = False) -> Path:
    if pack:
        return stack_root / "packs" / "optimization-or" / slug / "SKILL.md"
    return stack_root / slug / "SKILL.md"


@pytest.mark.smoke
def test_core_skill_count_matches_canonical():
    core = _canonical_core_slugs()
    cursor = sorted(p.parent.name for p in CURSOR_ROOT.glob("*/SKILL.md"))
    claude = sorted(p.parent.name for p in CLAUDE_ROOT.glob("*/SKILL.md"))
    assert len(cursor) >= len(core)
    assert len(claude) >= len(core)
    for slug in core:
        assert slug in cursor, f"missing .cursor mirror for {slug}"
        assert slug in claude, f"missing .claude mirror for {slug}"


@pytest.mark.smoke
def test_pack_skill_count_matches_canonical():
    pack = _canonical_pack_slugs()
    assert pack, "canonical optimization-or pack must contain skills"
    for slug in pack:
        assert _mirror_path(CURSOR_ROOT, slug, pack=True).is_file(), slug
        assert _mirror_path(CLAUDE_ROOT, slug, pack=True).is_file(), slug


@pytest.mark.smoke
def test_cursor_mirrors_match_canonical_bytes():
    for slug in _canonical_core_slugs():
        src = CORE_SRC / f"{slug}.md"
        dest = _mirror_path(CURSOR_ROOT, slug)
        assert dest.is_file(), dest
        assert dest.read_bytes() == expected_mirror(src, dest), f"cursor drift: {slug}"


@pytest.mark.smoke
def test_claude_mirrors_match_canonical_bytes():
    for slug in _canonical_core_slugs():
        src = CORE_SRC / f"{slug}.md"
        dest = _mirror_path(CLAUDE_ROOT, slug)
        assert dest.is_file(), dest
        assert dest.read_bytes() == expected_mirror(src, dest), f"claude drift: {slug}"


@pytest.mark.smoke
def test_pack_mirrors_match_canonical_bytes():
    for slug in _canonical_pack_slugs():
        src = PACK_SRC / f"{slug}.md"
        cursor_dest = _mirror_path(CURSOR_ROOT, slug, pack=True)
        claude_dest = _mirror_path(CLAUDE_ROOT, slug, pack=True)
        assert cursor_dest.read_bytes() == expected_mirror(src, cursor_dest), f"cursor pack drift: {slug}"
        assert claude_dest.read_bytes() == expected_mirror(src, claude_dest), f"claude pack drift: {slug}"


@pytest.mark.smoke
def test_cursor_and_claude_have_same_skill_count():
    expected = len(_canonical_core_slugs()) + len(_canonical_pack_slugs())
    cursor_count = len(list(CURSOR_ROOT.rglob("SKILL.md")))
    claude_count = len(list(CLAUDE_ROOT.rglob("SKILL.md")))
    assert cursor_count == expected, (cursor_count, expected)
    assert claude_count == expected, (claude_count, expected)
