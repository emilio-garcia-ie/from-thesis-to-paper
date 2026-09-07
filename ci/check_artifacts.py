"""Verify release archives and write a deterministic artifact manifest."""

from __future__ import annotations

import argparse
import hashlib
import tarfile
import zipfile
from pathlib import Path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _archive_names(path: Path) -> set[str]:
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as archive:
            return set(archive.namelist())
    if path.suffix == ".gz" and path.name.endswith(".tar.gz"):
        with tarfile.open(path, "r:gz") as archive:
            return {member.name for member in archive.getmembers()}
    if path.suffix == ".tgz":
        with tarfile.open(path, "r:gz") as archive:
            return {member.name for member in archive.getmembers()}
    raise ValueError(f"unsupported artifact type: {path}")


def _require(names: set[str], expected: set[str], label: str) -> None:
    missing = sorted(
        item
        for item in expected
        if not any(name == item or name.endswith(f"/{item}") for name in names)
    )
    if missing:
        raise ValueError(f"{label} is missing: {', '.join(missing)}")


def verify(artifact_dir: Path, manifest_path: Path) -> int:
    wheels = sorted(artifact_dir.glob("*.whl"))
    sdists = sorted(artifact_dir.glob("*.tar.gz"))
    npm_archives = sorted(artifact_dir.glob("*.tgz"))
    if len(wheels) != 1 or len(sdists) != 1 or len(npm_archives) != 1:
        raise ValueError(
            "expected exactly one wheel, one sdist, and one npm archive in "
            f"{artifact_dir}"
        )

    wheel, sdist, npm = wheels[0], sdists[0], npm_archives[0]
    wheel_names = _archive_names(wheel)
    sdist_names = _archive_names(sdist)
    npm_names = _archive_names(npm)
    _require(
        wheel_names,
        {
            "fttp/_templates/paper-workspace/fttp.config.json",
            "fttp/_templates/paper-workspace/.env.example",
            "fttp/_templates/paper-workspace/scripts/run_tests.sh",
        },
        wheel.name,
    )
    _require(
        sdist_names,
        {
            "templates/paper-workspace/fttp.config.json",
            "templates/paper-workspace/.env.example",
            "python/build_support.py",
        },
        sdist.name,
    )
    _require(
        npm_names,
        {"package/src/cli.js", "package/package.json", "package/LICENSE"},
        npm.name,
    )

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    artifacts = (wheel, sdist, npm)
    manifest_path.write_text(
        "".join(f"{_sha256(path)}  {path.name}\n" for path in artifacts),
        encoding="utf-8",
    )
    print(f"artifact check OK: {len(artifacts)} archives; manifest={manifest_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact_dir", type=Path)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    try:
        return verify(args.artifact_dir, args.manifest)
    except (OSError, ValueError, zipfile.BadZipFile, tarfile.TarError) as exc:
        parser.error(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
