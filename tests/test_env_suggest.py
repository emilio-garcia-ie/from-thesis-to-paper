"""Tests for fttp env-suggest command."""

from __future__ import annotations

from pathlib import Path

import pytest

from fttp.env_suggest import collect_suggestions, suggest_env


@pytest.mark.smoke
def test_collect_suggestions_from_requirements(tmp_path):
    req = tmp_path / "requirements.txt"
    req.write_text(
        "gurobipy>=11.0\n# comment\npandas>=2.0\n-r other.txt\n",
        encoding="utf-8",
    )
    out = collect_suggestions([tmp_path])
    key = f"requirements:{req.resolve()}"
    assert key in out
    assert "gurobipy" in out[key]
    assert "pandas" in out[key]


@pytest.mark.smoke
def test_collect_notebook_imports(tmp_path):
    nb = tmp_path / "analysis.ipynb"
    nb.write_text(
        json_dumps_minimal(["import gurobipy", "from pathlib import Path"]),
        encoding="utf-8",
    )
    out = collect_suggestions([tmp_path])
    nb_keys = [k for k in out if k.startswith("notebooks:")]
    assert nb_keys
    imports = out[nb_keys[0]]
    assert "gurobipy" in imports
    assert "pathlib" in imports


@pytest.mark.smoke
def test_suggest_env_write_file(tmp_path):
    (tmp_path / "requirements.txt").write_text("numpy\n", encoding="utf-8")
    target = tmp_path / ".env.example"
    lines, code = suggest_env([tmp_path], write_path=target)
    assert code == 0
    assert target.is_file()
    text = target.read_text(encoding="utf-8")
    assert "OVERLEAF_EMAIL" in text
    assert "numpy" in text or "# Detected" in text
    assert any("OVERLEAF" in line for line in lines)


def json_dumps_minimal(code_lines: list[str]) -> str:
    import json

    cells = [
        {
            "cell_type": "code",
            "metadata": {},
            "source": [line + "\n" for line in code_lines],
            "outputs": [],
        }
    ]
    return json.dumps({"cells": cells, "nbformat": 4, "nbformat_minor": 5})
