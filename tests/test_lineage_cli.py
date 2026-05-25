"""CLI lineage validate integration."""

from __future__ import annotations

from pathlib import Path

import pytest

from fttp.commands import cmd_lineage_validate

FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.mark.smoke
def test_cmd_lineage_validate_fixture_csv():
    cfg = {
        "repoRoot": str(FIXTURES.parent),
        "paper": {"dir": "fixtures", "mainTex": "x.tex"},
    }
    assert cmd_lineage_validate(FIXTURES / "lineage_minimal.csv", cfg) == 0
