"""Offline lifecycle coverage for the managed GitHub-download installer."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
INSTALLER = REPO / "scripts" / "release_installer.py"


def _wheel(tmp_path: Path) -> Path:
    result = subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--no-isolation", "--outdir", str(tmp_path), "."],
        cwd=REPO, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return next(tmp_path.glob("fttp-*.whl"))


def _run(prefix: Path, bin_dir: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLER), "--prefix", str(prefix), "--bin-dir", str(bin_dir), *args],
        text=True, capture_output=True, check=False,
    )


@pytest.mark.smoke
def test_private_installer_installs_and_uninstalls_without_network(tmp_path):
    wheel = _wheel(tmp_path / "artifacts")
    prefix, bin_dir = tmp_path / "private", tmp_path / "bin"
    digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
    result = _run(prefix, bin_dir, "--wheel", str(wheel), "--checksum", digest)
    assert result.returncode == 0, result.stderr
    launcher = bin_dir / "fttp"
    assert subprocess.run([str(launcher), "--version"], text=True, capture_output=True).returncode == 0
    unrelated = prefix / "keep.txt"
    unrelated.parent.mkdir(parents=True, exist_ok=True)
    unrelated.write_text("keep", encoding="utf-8")
    result = _run(prefix, bin_dir, "--uninstall")
    assert result.returncode == 0, result.stderr
    assert unrelated.read_text(encoding="utf-8") == "keep"
    assert not launcher.exists()


@pytest.mark.smoke
def test_private_installer_refuses_bad_checksum_and_unmanaged_launcher(tmp_path):
    wheel = _wheel(tmp_path / "artifacts")
    prefix, bin_dir = tmp_path / "private", tmp_path / "bin"
    result = _run(prefix, bin_dir, "--wheel", str(wheel), "--checksum", "0" * 64)
    assert result.returncode == 1
    assert not (prefix / "active.json").exists()
    bin_dir.mkdir()
    launcher = bin_dir / "fttp"
    launcher.write_text("keep", encoding="utf-8")
    result = _run(prefix, bin_dir, "--wheel", str(wheel))
    assert result.returncode == 1
    assert launcher.read_text(encoding="utf-8") == "keep"
    assert not (prefix / "versions").exists()


@pytest.mark.smoke
def test_private_installer_can_reactivate_retained_version(tmp_path):
    wheel = _wheel(tmp_path / "artifacts")
    prefix, bin_dir = tmp_path / "private", tmp_path / "bin"
    assert _run(prefix, bin_dir, "--wheel", str(wheel)).returncode == 0
    version = wheel.name.split("-")[1]
    assert _run(prefix, bin_dir, "--activate", version).returncode == 0
    assert subprocess.run([str(bin_dir / "fttp"), "--version"], text=True, capture_output=True).returncode == 0
