#!/usr/bin/env python3
"""Build the GitHub-release ZIP from already-tested FTTP artifacts."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main(argv: list[str] | None = None) -> int:
    output = Path(argv[0]).resolve() if argv else ROOT / "release-artifacts"
    output.mkdir(parents=True, exist_ok=True)
    build = subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--sdist", "--no-isolation", "--outdir", str(output), "."],
        cwd=ROOT, check=False,
    )
    if build.returncode:
        return build.returncode
    wheel = next(output.glob("fttp-*.whl"))
    sdist = next(output.glob("fttp-*.tar.gz"))
    bundle = output / f"fttp-{wheel.name.split('-')[1]}-macos-linux.zip"
    checksums = output / "SHA256SUMS"
    checksums.write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in (wheel, sdist)),
        encoding="utf-8",
    )
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as archive:
        for path, name in (
            (wheel, wheel.name), (sdist, sdist.name), (ROOT / "install.sh", "install.sh"),
            (ROOT / "scripts" / "release_installer.py", "scripts/release_installer.py"),
            (ROOT / "LICENSE", "LICENSE"), (ROOT / "README.md", "README.md"),
            (checksums, "SHA256SUMS"),
        ):
            archive.write(path, name)
    checksums.write_text("".join(f"{sha256(path)}  {path.name}\n" for path in (wheel, sdist, bundle)), encoding="utf-8")
    print(bundle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
