"""Setuptools hooks for bundling the canonical workspace template."""

from __future__ import annotations

import shutil
from pathlib import Path

from setuptools.command.build_py import build_py as _build_py


class build_py(_build_py):
    """Copy canonical consumer resources into the wheel build directory."""

    def run(self) -> None:
        super().run()
        root = Path(__file__).resolve().parents[1]
        trees = (
            (root / "templates" / "paper-workspace", Path("_templates") / "paper-workspace"),
            (root / "templates" / "memory", Path("_resources") / "memory"),
            (root / "templates" / "consumer", Path("_resources") / "consumer"),
            (root / "skills", Path("_resources") / "skills"),
            (root / "docs", Path("_resources") / "docs"),
        )
        rel_files: list[str] = []
        for source, relative_target in trees:
            if not source.is_dir():
                raise RuntimeError(f"canonical resource tree is missing: {source}")
            target = Path(self.build_lib) / "fttp" / relative_target
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source, target, symlinks=False)
            rel_files.extend(
                str(relative_target / path.relative_to(target))
                for path in target.rglob("*")
                if path.is_file()
            )
        package = next((item for item in self.packages or [] if item == "fttp"), "fttp")
        self.data_files.append((package, rel_files))
