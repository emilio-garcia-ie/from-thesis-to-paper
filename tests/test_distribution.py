"""Wheel, sdist and npm archive smoke checks outside the checkout."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _build_artifacts(output: Path) -> tuple[Path, Path]:
    result = subprocess.run(
        [sys.executable, "-m", "build", "--sdist", "--wheel", "--no-isolation", "--outdir", str(output), "."],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    wheel = next(output.glob("*.whl"))
    sdist = next(output.glob("*.tar.gz"))
    return wheel, sdist


def _install_and_scaffold(artifact: Path, tmp_path: Path, label: str) -> Path:
    target = tmp_path / f"installed-{label}"
    target.mkdir()
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet", "--no-deps", "--no-build-isolation", "--target", str(target), str(artifact)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    consumer_cwd = tmp_path / "consumer-cwd"
    consumer_cwd.mkdir(exist_ok=True)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(target)
    env.pop("FTTP_CONFIG", None)
    result = subprocess.run(
        [sys.executable, "-m", "fttp", "scaffold", "--slug", f"{label}-ws", "--parent", str(tmp_path)],
        cwd=consumer_cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return tmp_path / f"{label}-ws"


@pytest.mark.smoke
def test_wheel_and_sdist_scaffold_without_source_tree(tmp_path):
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()
    wheel, sdist = _build_artifacts(artifacts)
    wheel_ws = _install_and_scaffold(wheel, tmp_path, "wheel")
    sdist_ws = _install_and_scaffold(sdist, tmp_path, "sdist")
    source = REPO / "templates" / "paper-workspace"
    for workspace, slug in ((wheel_ws, "wheel-ws"), (sdist_ws, "sdist-ws")):
        for path in sorted(source.rglob("*")):
            if path.is_file():
                relative = path.relative_to(source)
                generated = workspace / relative
                assert generated.is_file(), relative
                if relative.name != "fttp.config.json":
                    expected = path.read_bytes().replace(b"{{WORKSPACE_SLUG}}", slug.encode())
                    assert generated.read_bytes() == expected, relative
        assert (workspace / "scripts" / "paper" / "build_primary.sh").stat().st_mode & 0o111


@pytest.mark.smoke
def test_npm_archive_contains_launcher_manifest_and_license(tmp_path):
    result = subprocess.run(
        ["npm", "pack", "--json", "--pack-destination", str(tmp_path)],
        cwd=REPO / "packages" / "cli",
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    metadata = json.loads(result.stdout)[0]
    archive = tmp_path / metadata["filename"]
    with tarfile.open(archive) as handle:
        names = set(handle.getnames())
    assert "package/src/cli.js" in names
    assert "package/package.json" in names
    assert "package/LICENSE" in names
