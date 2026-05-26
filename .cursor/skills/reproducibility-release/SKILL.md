---
name: reproducibility-release
description: SA6 reproducibility and public release packaging — REPRODUCIBILITY.md, fixtures, smoke tests
---

# Reproducibility and release (SA6)

## Triggers

- Async after SA4 or SA5 refactor (`SA6 ~> after SA4 or SA5`).
- Before public GitHub release or journal data-availability statement.
- User asks for “repro pack”, “REPRODUCIBILITY”, “release checklist”.

## Read order

1. `memory/paper_strategy_brief.md` `evidence_path`.
2. `paper/REPRODUCIBILITY.md` if exists; `templates/memory/` repro template.
3. `fttp.config.json` → `readOnlyRoots[]`, **`copyPolicy`** — [docs/WORKSPACE_MODEL.md](../../docs/WORKSPACE_MODEL.md) §4 copy manifest.
4. Paper workspace **README** (repo root) — tier A/B expectations from `templates/paper-workspace/README.md` scaffold.
5. `scripts/run_tests.sh` and smoke test docs.
6. SA5 output if refactor created new `codigo/` modules.
7. `memory/user_approval_log.md` — write **G6-repro** when profile requires it (below).

## In-repo vs external data policy

Document what lives **inside PAPER_WS** vs what stays **read-only** under `readOnlyRoots[]`:

| Tier | Location | Release / manuscript rule |
|------|----------|----------------------------|
| **In-repo (Tier A)** | `experimentos/evidence/`, fixtures, smoke scripts, locked JSON anchors | Ship in public Git when user approves release; cite paths in `paper/REPRODUCIBILITY.md` |
| **External (Tier B)** | Verification trees, master notebooks, multi-GB logs under `readOnlyRoots[]` | **Never** copy wholesale; cite absolute or mount-relative paths only |
| **Secrets** | `.env`, Overleaf passwords, Gurobi license files | Gitignored; document variable **names** only |

Respect `copyPolicy.maxArtifactMb` and `copyPolicy.allowSymlinks` from config — same bounds as SA3 archaeology ([docs/WORKSPACE_MODEL.md](../../docs/WORKSPACE_MODEL.md)).

## Paper workspace README expectations

When SA6 runs on a scaffolded workspace, ensure the repo root README (from `templates/paper-workspace/README.md`) still states:

- Three-repo model (framework / read-only sources / this paper repo).
- **Slug rule:** folder name = `workspaceSlug` = Overleaf **paper** project display name.
- Smoke command: `./scripts/run_tests.sh smoke`.
- Pointer to `paper/REPRODUCIBILITY.md` for Tier A/B and discrepancy policy.

Update README only if SA6 adds release-specific commands or fixture paths — do not duplicate full onboarding prose.

## Steps

1. Document environment: Python version, Gurobi version (if used), key env vars — no secrets in repo.
2. List **golden fixtures** (e.g. locked experiment ids) and how to run smoke pipeline.
3. Explain discrepancy policies (catalog vs log) with reproducible commands, not invented numbers.
4. Separate **public** artifact list from **read-only** paths too large to ship.
5. Update `paper/REPRODUCIBILITY.md` and `memory/reproducibility_status.md`.
6. Run `./scripts/run_tests.sh smoke` when `codigo/` changed; record PASS/FAIL in status file.
7. Run **G6-repro** AUDIT / APPROVE when `workflowProfile` is `paper_audit_repro` or `full_pipeline` (below).

## G6-repro — AUDIT / APPROVE (profile-dependent)

Per [docs/USER_APPROVAL_GATES.md](../../docs/USER_APPROVAL_GATES.md).

| `workflowProfile` | G6 required? |
|-------------------|--------------|
| `paper_only`, `paper_audit` | No — note G6 waived in log if row exists |
| `paper_audit_repro`, `full_pipeline` | **Yes** — blocks public release / data-availability sign-off |

After `paper/REPRODUCIBILITY.md` and README smoke pointers are updated:

```text
AUDIT: G6-repro — review paper/REPRODUCIBILITY.md and paper workspace README
Checklist:
- In-repo vs external (readOnlyRoots) paths explicit; no multi-GB trees promised in-repo
- Smoke command documented; discrepancy / TBD policy matches G4 when applicable
- No secrets in committed files; env var names only
APPROVE_ASK: Confirm reproducibility statement matches what you can share publicly. Reply APPROVED: G6-repro (EN) or APROBADO: G6-repro (ES) or corrections.
```

On user approval: update row **`G6-repro`** in `memory/user_approval_log.md`.

**When G6 is required but not approved:**

```text
TAREA INCOMPLETA
BLOQUEADO: public release / journal data statement — missing approved row for G6-repro
```

G6 does **not** block SA7–SA9 on the fast path unless the user explicitly ties release to those steps.

## Forbidden

- Committing `.env`, Overleaf passwords, or license files with secrets.
- Copying 57GB verification trees into the release bundle.
- Claiming full replication if brief is `thesis_only_B` without stating limits.

## Verify

- `paper/REPRODUCIBILITY.md` exists and references smoke command; Tier A vs external RO paths explicit.
- Repo README mentions smoke gate and points to `REPRODUCIBILITY.md` (scaffold or SA6 update).
- If `codigo/` touched in same tranche: smoke exit code 0.
- When profile requires G6: `memory/user_approval_log.md` has **G6-repro** `approved` before public release HANDOFF.
- HANDOFF → SA13 or user release tag; does not block SA7–SA9 on fast path unless user requests.
