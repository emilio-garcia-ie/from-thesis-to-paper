"""Bounded, deterministic and nondestructive env-suggest tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fttp import env_suggest
from fttp.env_suggest import MAX_FILE_BYTES, suggest_env


@pytest.mark.smoke
def test_large_valid_notebook_is_read_within_file_budget(tmp_path):
    source = "import gurobipy\n" + ("# padding\n" * 80_000)
    notebook = {"cells": [{"cell_type": "code", "source": [source]}]}
    (tmp_path / "large.ipynb").write_text(json.dumps(notebook), encoding="utf-8")
    lines, code = suggest_env([tmp_path])
    assert code == 0
    assert any("gurobipy" in line for line in lines)


@pytest.mark.smoke
def test_over_limit_and_malformed_inputs_are_partial_nonzero(tmp_path, capsys):
    (tmp_path / "too-large.py").write_bytes(b"import pandas\n" + b"x" * MAX_FILE_BYTES)
    (tmp_path / "bad.ipynb").write_text("{not json", encoding="utf-8")
    (tmp_path / "bad-encoding.py").write_bytes(b"import numpy\n\xff\xfe")
    _, code = suggest_env([tmp_path])
    assert code == 1
    assert "incomplete scan" in capsys.readouterr().err


@pytest.mark.smoke
def test_missing_root_and_symlinked_tree_are_reported(tmp_path, capsys):
    missing = tmp_path / "missing"
    target = tmp_path / "target"
    target.mkdir()
    (target / "loop").symlink_to(target, target_is_directory=True)
    _, code = suggest_env([missing, target])
    assert code == 1
    err = capsys.readouterr().err
    assert "root not found" in err

    linked_root = tmp_path / "linked-root"
    linked_root.symlink_to(target, target_is_directory=True)
    _, linked_code = suggest_env([linked_root])
    assert linked_code == 1


@pytest.mark.smoke
def test_malformed_notebook_cell_shape_is_partial(tmp_path, capsys):
    (tmp_path / "bad-cell.ipynb").write_text(
        json.dumps({"cells": [{"cell_type": "code", "source": [1, 2]}]}),
        encoding="utf-8",
    )
    _, code = suggest_env([tmp_path])
    assert code == 1
    assert "malformed notebook cell source" in capsys.readouterr().err


@pytest.mark.smoke
def test_write_is_create_only(tmp_path, capsys):
    output = tmp_path / ".env.example"
    output.write_text("keep\n", encoding="utf-8")
    _, code = suggest_env([tmp_path], write_path=output)
    assert code == 1
    assert output.read_text(encoding="utf-8") == "keep\n"
    assert "refusing to overwrite" in capsys.readouterr().err


@pytest.mark.smoke
def test_write_refuses_broken_symlink_target(tmp_path):
    target = tmp_path / "missing-target"
    output = tmp_path / ".env.example"
    output.symlink_to(target)
    _, code = suggest_env([tmp_path], write_path=output)
    assert code == 1
    assert not target.exists()


@pytest.mark.smoke
def test_notebook_limit_is_deterministic(tmp_path, capsys):
    for index in range(51):
        (tmp_path / f"{index:03d}.ipynb").write_text(
            json.dumps({"cells": [{"cell_type": "code", "source": ["import pandas\n"]}]}),
            encoding="utf-8",
        )
    _, code = suggest_env([tmp_path])
    assert code == 1
    assert "notebook limit" in capsys.readouterr().err


@pytest.mark.smoke
def test_entry_limit_bounds_actual_scandir_iteration(tmp_path, monkeypatch):
    for index in range(30):
        (tmp_path / f"{index:03d}.py").write_text("import os\n", encoding="utf-8")
    monkeypatch.setattr(env_suggest, "MAX_VISITED_ENTRIES", 5)
    seen = 0
    original_scandir = env_suggest.os.scandir

    class CountedScandir:
        def __init__(self, path):
            self.iterator = original_scandir(path)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.iterator.close()

        def __iter__(self):
            return self

        def __next__(self):
            nonlocal seen
            entry = next(self.iterator)
            seen += 1
            return entry

    monkeypatch.setattr(env_suggest.os, "scandir", CountedScandir)
    _, state = env_suggest._collect_suggestions_report([tmp_path])
    assert seen == 5
    assert state.visited == 5
    assert any("visited-entry limit" in item for item in state.incomplete)
