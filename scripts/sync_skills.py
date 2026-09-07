#!/usr/bin/env python3
"""Validate or generate IDE skill mirrors from the canonical ``skills/`` tree."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parents[1]
CANONICAL = REPO / "skills"
MIRRORS = (REPO / ".cursor" / "skills", REPO / ".claude" / "skills")
LINK_RE = re.compile(r"(?P<prefix>!?\[[^\]]*\]\()(?P<target>[^)\s]+)(?P<suffix>\))")


def _skill_sources() -> list[tuple[Path, str]]:
    sources: list[tuple[Path, str]] = []
    for path in sorted((CANONICAL / "core").glob("*.md")):
        sources.append((path, path.stem))
    for path in sorted((CANONICAL / "packs").glob("*/")):
        for skill in sorted(path.glob("*.md")):
            sources.append((skill, f"packs/{path.name}/{skill.stem}"))
    return sources


def _rebase_links(text: str, source: Path, destination: Path) -> str:
    source_dir = source.parent
    destination_dir = destination.parent

    def replace(match: re.Match[str]) -> str:
        target = match.group("target")
        if (
            target.startswith(("http://", "https://", "mailto:", "#", "/"))
            or target.startswith("<")
        ):
            return match.group(0)
        suffix = ""
        path_part = target
        if "#" in path_part:
            path_part, suffix = path_part.split("#", 1)
            suffix = "#" + suffix
        if not path_part or not path_part.endswith((".md", ".markdown")):
            return match.group(0)
        target_path = (source_dir / path_part).resolve()
        try:
            target_path.relative_to(REPO.resolve())
        except ValueError:
            return match.group(0)
        rebased = Path(__import__("os").path.relpath(target_path, destination_dir.resolve())).as_posix()
        return f"{match.group('prefix')}{rebased}{suffix}{match.group('suffix')}"

    return LINK_RE.sub(replace, text)


def expected_mirror(source: Path, destination: Path) -> bytes:
    text = source.read_text(encoding="utf-8")
    return _rebase_links(text, source, destination).encode("utf-8")


def _expected_paths() -> set[Path]:
    return {
        mirror / Path(f"{slug}") / "SKILL.md"
        for mirror in MIRRORS
        for _, slug in _skill_sources()
    }


def check() -> list[str]:
    errors: list[str] = []
    sources = _skill_sources()
    expected = _expected_paths()
    for mirror in MIRRORS:
        actual = set(mirror.rglob("SKILL.md")) if mirror.is_dir() else set()
        for orphan in sorted(actual - expected):
            errors.append(f"unexpected mirror: {orphan.relative_to(REPO)}")
    for source, slug in sources:
        for mirror in MIRRORS:
            destination = mirror / slug / "SKILL.md"
            if not destination.is_file():
                errors.append(f"missing mirror: {destination.relative_to(REPO)}")
                continue
            if destination.read_bytes() != expected_mirror(source, destination):
                errors.append(f"stale mirror: {destination.relative_to(REPO)}")
            rendered = destination.read_text(encoding="utf-8")
            for match in LINK_RE.finditer(rendered):
                target = match.group("target").split("#", 1)[0].strip("<>")
                if not target or target.startswith(("http://", "https://", "mailto:", "#", "/")):
                    continue
                if target.endswith((".md", ".markdown")):
                    linked = (destination.parent / target).resolve()
                    if not linked.is_file():
                        errors.append(
                            f"broken rendered link: {destination.relative_to(REPO)} -> {target}"
                        )
    return errors


def write() -> None:
    for source, slug in _skill_sources():
        for mirror in MIRRORS:
            destination = mirror / slug / "SKILL.md"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(expected_mirror(source, destination))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write generated mirrors")
    parser.add_argument("--check", action="store_true", help="validate mirrors without writing (default)")
    args = parser.parse_args(argv)
    if args.write:
        write()
    errors = check()
    if errors:
        for error in errors:
            print(f"sync_skills: {error}", file=sys.stderr)
        return 1
    print(f"sync_skills: {len(_skill_sources())} skills × {len(MIRRORS)} mirrors OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
