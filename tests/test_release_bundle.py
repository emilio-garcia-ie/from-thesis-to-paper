"""The archive intended for GitHub Releases contains the tested install path."""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_release_bundle_contains_installer_and_artifacts(tmp_path):
    result = subprocess.run(
        [sys.executable, "scripts/build_release_bundle.py", str(tmp_path)],
        cwd=REPO, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    bundle = next(tmp_path.glob("fttp-*-macos-linux.zip"))
    with zipfile.ZipFile(bundle) as archive:
        names = set(archive.namelist())
    assert "install.sh" in names
    assert "scripts/release_installer.py" in names
    assert "SHA256SUMS" in names
    assert any(name.endswith(".whl") for name in names)
    assert any(name.endswith(".tar.gz") for name in names)
