#!/usr/bin/env python3
"""Install or remove a downloaded FTTP wheel without touching system Python."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _version_from_wheel(wheel: Path) -> str:
    parts = wheel.name.split("-")
    if len(parts) < 2 or not parts[1]:
        raise ValueError(f"cannot determine version from wheel name: {wheel.name}")
    return parts[1]


def _paths(prefix: Path, bin_dir: Path) -> tuple[Path, Path, Path]:
    return prefix / "versions", prefix / "active.json", bin_dir / "fttp"


def _write_launcher(launcher: Path, version_dir: Path) -> None:
    marker = launcher.with_name(launcher.name + ".fttp-managed")
    if launcher.exists() and not marker.is_file():
        raise ValueError(f"refusing to replace unmanaged launcher: {launcher}")
    launcher.parent.mkdir(parents=True, exist_ok=True)
    executable = version_dir / "bin" / "python"
    launcher.write_text(
        "#!/usr/bin/env sh\nexec " + shlex.quote(str(executable)) + ' -m fttp "$@"\n', encoding="utf-8"
    )
    launcher.chmod(0o755)
    marker.write_text("FTTP managed launcher\n", encoding="utf-8")


def _check_launcher_ownership(launcher: Path) -> None:
    marker = launcher.with_name(launcher.name + ".fttp-managed")
    if launcher.exists() and not marker.is_file():
        raise ValueError(f"refusing to replace unmanaged launcher: {launcher}")


def install(wheel: Path, prefix: Path, bin_dir: Path, python: str, checksum: str | None) -> Path:
    wheel = wheel.expanduser().resolve()
    if not wheel.is_file():
        raise ValueError(f"wheel not found: {wheel}")
    if checksum and _sha256(wheel).lower() != checksum.lower():
        raise ValueError("wheel checksum does not match the supplied SHA-256")
    probe = subprocess.run([python, "-c", "import sys; assert sys.version_info >= (3, 10)"], check=False)
    if probe.returncode:
        raise ValueError(f"Python 3.10+ with venv support is required: {python}")
    version = _version_from_wheel(wheel)
    versions, active, launcher = _paths(prefix, bin_dir)
    target = versions / version
    if target.exists():
        raise ValueError(f"version already installed: {version}")
    _check_launcher_ownership(launcher)
    staging = versions / (".staging-" + version + "-" + str(os.getpid()))
    versions.mkdir(parents=True, exist_ok=True)
    try:
        created = subprocess.run(
            [python, "-m", "venv", str(staging)], text=True, capture_output=True, check=False
        )
        if created.returncode:
            raise ValueError(created.stderr.strip() or "could not create private environment")
        installer = staging / "bin" / "python"
        result = subprocess.run(
            [str(installer), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel)],
            text=True, capture_output=True, check=False,
        )
        if result.returncode:
            raise ValueError(result.stderr.strip() or "wheel installation failed")
        check = subprocess.run(
            [str(staging / "bin" / "python"), "-m", "fttp", "--version"],
            text=True, capture_output=True, check=False,
        )
        if check.returncode:
            raise ValueError(check.stderr.strip() or "installed fttp command failed")
        staging.replace(target)
        _write_launcher(launcher, target)
        active.write_text(json.dumps({"version": version, "wheelSha256": _sha256(wheel)}) + "\n", encoding="utf-8")
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise
    return launcher


def activate(prefix: Path, bin_dir: Path, version: str) -> Path:
    versions, active, launcher = _paths(prefix, bin_dir)
    target = versions / version
    executable = target / "bin" / "python"
    if not executable.is_file():
        raise ValueError(f"managed FTTP version is not installed: {version}")
    _check_launcher_ownership(launcher)
    _write_launcher(launcher, target)
    active.write_text(json.dumps({"version": version}) + "\n", encoding="utf-8")
    return launcher


def uninstall(prefix: Path, bin_dir: Path) -> None:
    versions, active, launcher = _paths(prefix, bin_dir)
    marker = launcher.with_name(launcher.name + ".fttp-managed")
    if not active.is_file():
        raise ValueError(f"no managed FTTP installation found under {prefix}")
    record = json.loads(active.read_text(encoding="utf-8"))
    version = record.get("version")
    if not isinstance(version, str):
        raise ValueError(f"invalid managed installation record: {active}")
    if marker.is_file():
        launcher.unlink(missing_ok=True)
        marker.unlink(missing_ok=True)
    target = versions / version
    if target.is_dir():
        shutil.rmtree(target)
    active.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", type=Path)
    parser.add_argument("--checksum")
    parser.add_argument("--prefix", type=Path, default=Path.home() / ".local" / "share" / "fttp")
    parser.add_argument("--bin-dir", type=Path, default=Path.home() / ".local" / "bin")
    parser.add_argument("--python", default=sys.executable, help="Python 3.10+ interpreter for the private environment")
    parser.add_argument("--activate", metavar="VERSION", help="activate a previously installed FTTP version")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.uninstall:
            uninstall(args.prefix.expanduser(), args.bin_dir.expanduser())
            print("FTTP removed; paper workspaces were not changed.")
            return 0
        if args.activate:
            if args.wheel is not None:
                parser.error("--activate cannot be combined with --wheel")
            launcher = activate(args.prefix.expanduser(), args.bin_dir.expanduser(), args.activate)
            print(f"FTTP activated: {launcher} ({args.activate})")
            return 0
        if args.wheel is None:
            parser.error("--wheel is required unless --uninstall is used")
        launcher = install(args.wheel, args.prefix.expanduser(), args.bin_dir.expanduser(), args.python, args.checksum)
        print(f"FTTP installed: {launcher}")
        print(f"Run: {launcher} init ~/papers/my-paper --agent codex")
        if str(launcher.parent) not in os.environ.get("PATH", "").split(os.pathsep):
            print(f"Add {launcher.parent} to PATH to use `fttp` directly.")
        return 0
    except (OSError, ValueError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        print(f"FTTP install: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
