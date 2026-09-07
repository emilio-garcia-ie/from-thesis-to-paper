"""Setuptools hooks for bundling the canonical workspace template."""

from __future__ import annotations

import shutil
from pathlib import Path

from setuptools.command.build_py import build_py as _build_py


class build_py(_build_py):
    """Copy templates/paper-workspace into the wheel build directory."""

    def run(self) -> None:
        super().run()
        source = Path(__file__).resolve().parents[1] / "templates" / "paper-workspace"
        if not source.is_dir():
            raise RuntimeError(f"canonical workspace template is missing: {source}")
        target = Path(self.build_lib) / "fttp" / "_templates" / "paper-workspace"
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target, symlinks=False)
        rel_files = [
            str(Path("_templates") / "paper-workspace" / path.relative_to(target))
            for path in target.rglob("*")
            if path.is_file()
        ]
        package = next((item for item in self.packages or [] if item == "fttp"), "fttp")
        self.data_files.append((package, rel_files))
