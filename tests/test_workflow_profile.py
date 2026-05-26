"""Workflow profile → expected SA agent list (onboarding v2)."""

from __future__ import annotations

import pytest

from fttp.config import (
    WORKFLOW_PROFILE_AGENTS,
    workflow_profile,
    workflow_profile_agents,
)

_BASE = (
    "SA0",
    "SA1",
    "SA2",
    "SA2b",
    "SA7",
    "SA8",
    "SA9",
    "SA12",
    "SA13",
)


def _cfg(profile: str | None) -> dict:
    base = {
        "workspaceName": "t",
        "repoRoot": "/tmp",
        "paper": {"dir": "paper", "mainTex": "main.tex"},
    }
    if profile is not None:
        base["workflowProfile"] = profile
    return base


@pytest.mark.smoke
@pytest.mark.parametrize(
    ("profile", "expected"),
    [
        ("paper_only", _BASE),
        ("paper_audit", _BASE + ("SA3", "SA4")),
        ("paper_audit_repro", _BASE + ("SA3", "SA4", "SA6")),
        ("full_pipeline", _BASE + ("SA3", "SA4", "SA6", "SA5", "SA11")),
    ],
)
def test_workflow_profile_agents_snapshot(profile: str, expected: tuple[str, ...]):
    assert WORKFLOW_PROFILE_AGENTS[profile] == expected
    assert workflow_profile_agents(_cfg(profile)) == expected


@pytest.mark.smoke
def test_workflow_profile_default_uses_paper_audit_agents():
    assert workflow_profile(_cfg(None)) == "paper_audit"
    assert workflow_profile_agents(_cfg(None)) == WORKFLOW_PROFILE_AGENTS["paper_audit"]
