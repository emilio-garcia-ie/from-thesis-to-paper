"""Scaffold preservation and rollback tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fttp.config import FttpConfigError
from fttp.scaffold import scaffold_workspace


@pytest.mark.smoke
def test_force_fills_missing_files_without_overwriting_user_bytes(tmp_path):
    dest = tmp_path / "safe-ws"
    dest.mkdir()
    manuscript = dest / "README.md"
    notes = dest / "notes.md"
    cfg = dest / "fttp.config.json"
    manuscript.write_text("user manuscript with {{WORKSPACE_SLUG}}\n", encoding="utf-8")
    notes.write_text("private notes\n", encoding="utf-8")
    cfg.write_text(
        json.dumps(
            {
                "workspaceName": "safe-ws",
                "workspaceSlug": "safe-ws",
                "repoRoot": str(dest),
                "paper": {"dir": "paper", "mainTex": "main.tex"},
            }
        ),
        encoding="utf-8",
    )
    before = {path: path.read_bytes() for path in (manuscript, notes, cfg)}
    scaffold_workspace("safe-ws", tmp_path, force=True)
    assert {path: path.read_bytes() for path in before} == before
    assert (dest / "paper" / "main.tex").is_file()


@pytest.mark.smoke
def test_force_rejects_incompatible_workspace_before_replacing_files(tmp_path):
    dest = tmp_path / "conflict-ws"
    dest.mkdir()
    marker = dest / "marker.txt"
    marker.write_text("keep", encoding="utf-8")
    (dest / "fttp.config.json").write_text(
        json.dumps(
            {
                "workspaceName": "other",
                "workspaceSlug": "other",
                "repoRoot": str(dest),
                "paper": {"dir": "paper", "mainTex": "main.tex"},
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(FttpConfigError, match="different workspaceSlug"):
        scaffold_workspace("conflict-ws", tmp_path, force=True)
    assert marker.read_text(encoding="utf-8") == "keep"
    assert not (dest / "README.md").exists()


@pytest.mark.smoke
def test_symlink_destination_is_rejected_without_writes(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    link = tmp_path / "link-ws"
    link.symlink_to(target, target_is_directory=True)
    with pytest.raises(FttpConfigError, match="symlink"):
        scaffold_workspace("link-ws", tmp_path, force=True)
    assert not (target / "README.md").exists()


@pytest.mark.smoke
def test_broken_symlink_destination_is_rejected(tmp_path):
    link = tmp_path / "broken-ws"
    link.symlink_to(tmp_path / "missing-target", target_is_directory=True)
    with pytest.raises(FttpConfigError, match="symlink"):
        scaffold_workspace("broken-ws", tmp_path, force=True)


@pytest.mark.smoke
def test_new_scaffold_rolls_back_when_template_config_is_unusable(tmp_path, monkeypatch):
    # The template is read-only in normal operation; inject a failing config
    # read to prove a new destination is removed after preflight failure.
    from fttp import scaffold as module

    original = module._patch_config_repo_root

    def fail(*args, **kwargs):
        raise FttpConfigError("injected scaffold failure")

    monkeypatch.setattr(module, "_patch_config_repo_root", fail)
    with pytest.raises(FttpConfigError, match="injected"):
        scaffold_workspace("rollback-ws", tmp_path)
    assert not (tmp_path / "rollback-ws").exists()
    monkeypatch.setattr(module, "_patch_config_repo_root", original)


@pytest.mark.smoke
def test_force_validates_existing_hook_paths_before_creating_stubs(tmp_path):
    dest = tmp_path / "unsafe-ws"
    dest.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    marker = outside / "created"
    (dest / "fttp.config.json").write_text(
        json.dumps(
            {
                "workspaceName": "unsafe-ws",
                "workspaceSlug": "unsafe-ws",
                "repoRoot": str(dest),
                "paper": {"dir": "paper", "mainTex": "main.tex"},
                "hooks": {"tables": "../outside/new-hook.py"},
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(FttpConfigError, match="relative path"):
        scaffold_workspace("unsafe-ws", tmp_path, force=True)
    assert not marker.exists()
    assert not (dest / "README.md").exists()


@pytest.mark.smoke
def test_force_rejects_symlinked_missing_hook_destination(tmp_path):
    dest = tmp_path / "symlink-hook-ws"
    dest.mkdir()
    target = dest / "hook-target"
    target.write_text("keep\n", encoding="utf-8")
    hook_link = dest / "scripts" / "paper" / "export_tables_from_catalog.py"
    hook_link.parent.mkdir(parents=True)
    hook_link.symlink_to(target)
    (dest / "fttp.config.json").write_text(
        json.dumps(
            {
                "workspaceName": "symlink-hook-ws",
                "workspaceSlug": "symlink-hook-ws",
                "repoRoot": str(dest),
                "paper": {"dir": "paper", "mainTex": "main.tex"},
                "hooks": {"tables": "scripts/paper/export_tables_from_catalog.py"},
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(FttpConfigError, match="symlink"):
        scaffold_workspace("symlink-hook-ws", tmp_path, force=True)
    assert hook_link.is_symlink()
    assert target.read_text(encoding="utf-8") == "keep\n"


@pytest.mark.smoke
@pytest.mark.parametrize("relative", ["codigo", "paper/figures", "paper/tables", "memory"])
def test_force_rejects_every_managed_symlink_before_any_write(tmp_path, relative):
    dest = tmp_path / "managed-link-ws"
    dest.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    link = dest / relative
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(outside, target_is_directory=True)
    with pytest.raises(FttpConfigError, match="symlink"):
        scaffold_workspace("managed-link-ws", tmp_path, force=True)
    assert list(outside.iterdir()) == []
    assert not (dest / "README.md").exists()


@pytest.mark.smoke
def test_force_validates_read_only_overlap_before_copying(tmp_path, monkeypatch):
    dest = tmp_path / "read-only-ws"
    dest.mkdir()
    cfg = {
        "workspaceName": "read-only-ws",
        "workspaceSlug": "read-only-ws",
        "repoRoot": str(dest),
        "paper": {"dir": "paper", "mainTex": "main.tex"},
        "readOnlyRoots": [str(tmp_path)],
    }
    (dest / "fttp.config.json").write_text(json.dumps(cfg), encoding="utf-8")
    copied: list[Path] = []
    original = __import__("fttp.scaffold", fromlist=["_copy_missing"])._copy_missing

    def track(*args, **kwargs):
        copied.append(Path(args[1]))
        return original(*args, **kwargs)

    monkeypatch.setattr("fttp.scaffold._copy_missing", track)
    with pytest.raises(FttpConfigError, match="overlaps"):
        scaffold_workspace("read-only-ws", tmp_path, force=True)
    assert copied == []
    assert not (dest / "README.md").exists()
