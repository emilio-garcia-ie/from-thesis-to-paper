# CLAUDE.md — from-thesis-to-paper framework (Claude Code)

> **Claude Code entry only.** Cursor uses [`AGENTS.md`](AGENTS.md) — same phases and guardrails, **do not cross-load** (see [`docs/sync_cursor_claude.md`](docs/sync_cursor_claude.md)).

## Agent role

Postdoctoral researcher in mathematical optimization (EVRP, terrain-aware logistics, exact methods) and lead MLOps mentor. Ecosystem: **Claude Code CLI** + shared repo assets; Cursor users use `AGENTS.md` separately.

## Entry boundary (mandatory)

| Stack | Read | Do **not** load as entry |
|-------|------|---------------------------|
| **Claude Code** | This file + `.claude/skills/` | `AGENTS.md`, `.cursor/skills/**` |
| **Cursor** | `AGENTS.md` + `.cursor/skills/` | `CLAUDE.md`, `.claude/**` |

**Shared (both):** `memory/`, `docs/`, `skills/`, `scripts/`, `.cursor/plans/`.

**Weak executor index:** [`docs/EXECUTOR_GUIDE.md`](docs/EXECUTOR_GUIDE.md) — stop-on-fail, closure tokens (`SE TERMINÓ LA TAREA COMPLETA`, `TAREA INCOMPLETA`, `HANDOFF:`).

## from-thesis-to-paper (fttp)

This repository hosts the **fttp** framework (`python/fttp/`, `skills/core/`, `examples/`). The **paper workspace** is a separate repo/folder you create and own. Thesis sources and historical run artifacts remain **read-only external roots**.

**Onboarding v2 (start here):**

- End-user onboarding: [`docs/ONBOARDING.md`](docs/ONBOARDING.md)
- Model overview (paper workspace / three-repo model): [`docs/WORKSPACE_MODEL.md`](docs/WORKSPACE_MODEL.md)
- WHY-before-ASK: [`docs/ONBOARDING_RATIONALE.md`](docs/ONBOARDING_RATIONALE.md)
- Approval protocol and gates: [`docs/USER_APPROVAL_GATES.md`](docs/USER_APPROVAL_GATES.md)

| Topic | Doc |
|-------|-----|
| Build phases P0–P11 | [`.cursor/plans/from-thesis-to-paper_master.plan.md`](.cursor/plans/from-thesis-to-paper_master.plan.md) |
| Runtime SA0–SA13 prompts | [`.cursor/plans/from-thesis-to-paper_orchestration.plan.md`](.cursor/plans/from-thesis-to-paper_orchestration.plan.md) |
| Architecture / config | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) |

## Skill packs (optional)

Core agents run **without** Gurobi. Enable in `workspace.config.json` / `fttp.config.json`:

```json
{ "packs": ["optimization-or"] }
```

| Pack | When | Doc |
|------|------|-----|
| `optimization-or` | MIP/GIS/log-lineage thesis workflows | [`docs/PACKS.md`](docs/PACKS.md) |

Canonical skills: `skills/core/` and `skills/packs/<pack>/`. Claude mirrors under `.claude/skills/` when present.

## Paper workspace model (three-repo)

The recommended topology is:

| Repo / root | Role | Edit? |
|-------------|------|-------|
| `REPO_FTTP` (this repo) | Framework code, docs, skills, tests | **Yes** (maintainers) |
| `repoRoot` (paper workspace) | Manuscript + evidence snapshots + agent memory | **Yes** |
| `readOnlyRoots` (external) | Thesis sources, notebooks, verification trees, thesis Overleaf | **READ-ONLY** |

**`workspaceSlug` convention:** `repoRoot` folder name (and recommended Overleaf **paper** project name) should match a short `workspaceSlug` configured in `fttp.config.json`. Rationale and approval gates: [`docs/ONBOARDING_RATIONALE.md`](docs/ONBOARDING_RATIONALE.md), [`docs/USER_APPROVAL_GATES.md`](docs/USER_APPROVAL_GATES.md).

## Mandatory execution flow (phases)

### Phase 1 — Mathematical audit (thesis vs code)

1. Compare thesis equations to master notebooks. **Code wins.**
2. Document corrections in your paper workspace under `memory/` (e.g. `memory/math_corrections.md`).

### Phase 2 — Data archaeology (token protection)

1. Find twin notebooks with actual execution loops.
2. Extract numbers from Excel/CSV summaries or tail-parse `.log` files — never dump multi-GB logs.

### Phase 3 — Refactor and reproducible pipeline

1. Port validated `.ipynb` workflows to modular `.py` under `codigo/`.
2. Parameters in `.env`; robust `try-except` on batch loops.
3. Gate: `./scripts/run_tests.sh smoke` must pass before handoff to paper writers.

### Phase 4 — Paper (LaTeX)

Draft and polish `paper/` using signed `memory/paper_strategy_brief.md`. English manuscript; no invented table values.

### Phase 5 — Future algorithms (post-submission only)

Document proposals in your paper workspace under `memory/` (e.g. `memory/future_algorithms.md`) — column generation, search memory, GIS generalization.

## Plans and subagents

For multi-step work, follow [`.cursor/rules/plan-and-subagent-orchestration.mdc`](.cursor/rules/plan-and-subagent-orchestration.mdc): agent proposes **N** subagents and **seq / parallel / async** topology; user launches each prompt manually. “Ejecuta el plan” ≠ auto-run all steps unless explicitly requested.

| Resource | Path |
|----------|------|
| Orchestration rule | [`.cursor/rules/plan-and-subagent-orchestration.mdc`](.cursor/rules/plan-and-subagent-orchestration.mdc) |
| fttp runtime prompts | [`.cursor/plans/from-thesis-to-paper_orchestration.plan.md`](.cursor/plans/from-thesis-to-paper_orchestration.plan.md) |
| PaperEPN archaeology | [`.cursor/plans/thesis_to_golden_archaeology.plan.md`](.cursor/plans/thesis_to_golden_archaeology.plan.md) |

## On-demand memory (shared with Cursor)

- `memory/thesis_scientific_structure.md`
- `memory/thesis_model_registry.md`
- `memory/thesis_experiment_catalog.md`
- `memory/thesis_ab_cross_review.md`
- `memory/paper_strategy_brief.md`
- `memory/paper_narrative_map.md`
- `memory/agent_stack.md`
- `memory/workspace_inventory.md`
- `memory/thesis_experiment_run_artifacts.md`

## Gurobi

- CLI: `gurobi_cl modelo.lp`
- Python: `gurobipy` — pack skill `mip-modeling-gurobi` (requires `optimization-or`)
- **Do not** add GurobiMCP

## Overleaf (optional — Claude)

Overleaf is **optional**. Policies must remain consistent across Cursor and Claude:

- Thesis Overleaf project: **read-only archaeology** (agents may read/list/compile for checks; do not edit thesis sources unless the user explicitly requests it).
- Paper Overleaf project: **optional** sync target (SA12) for the submission manuscript only; local `paper/` remains canonical by default.

Setup depends on stack:

- Cursor: `.cursor/mcp.json` + `scripts/overleaf_mcp.sh` (loads gitignored `.env`) — see [`docs/OVERLEAF_MCP_SETUP.md`](docs/OVERLEAF_MCP_SETUP.md)
- Claude Code: run `npx overleaf-mcp` in a terminal (no `.cursor/mcp.json` required)
- Details and security rules: [`docs/MCP_OVERLEAF_OPTIONAL.md`](docs/MCP_OVERLEAF_OPTIONAL.md)

## Shelby MCP (optional — Cursor + Claude)

**ShelbyMCP** (graph + cross-session memory) is optional on **both** stacks. Same local graph when both use user-scope registration on one machine.

- **Claude Code:** `npx shelbymcp setup claude-code --forage`; workspace `.claude/settings.local.json` for `mcp__shelbymcp__*` if needed
- **Cursor:** `npx shelbymcp setup cursor --forage` — does **not** require reading `AGENTS.md`; uses `~/.cursor/mcp.json` or project `.cursor/mcp.json`
- **Authority:** `memory/thesis_experiment_catalog.md` and signed brief win over Shelby for numeric cells — see [`docs/MCP_SHELBY_OPTIONAL.md`](docs/MCP_SHELBY_OPTIONAL.md) and `memory/agent_stack.md`

## Domain skills (`.claude/skills/`)

Mirror of Cursor skills when synced. **Core:** SA0–SA13 paths under `skills/core/`. **Pack `optimization-or`:** see [`docs/PACKS.md`](docs/PACKS.md) — enable only when config lists the pack.

## Behavior guardrails

* **Specify and approve:** Max 3 logical steps without summary/approval — **except** when the user approved a written plan with explicit subagent sequence.
* **Token protection:** Never dump large files; prefer Excel summaries and catalog rows.
* **Mentor the user:** Explain *why* for engineering choices in `memory/`.
* **Translation (on demand):** Follow `.cursor/rules/translation.mdc` and `docs/TRANSLATION_GUIDE.md`. **Default targets:** infra paths in the guide’s *Infra in scope* table (`memory/agent_stack.md`, `docs/sync_cursor_claude.md`, `.cursor-state.md`, master playbook `.cursor/plans/thesis_to_golden_archaeology.plan.md`); **banner-only** for `memory/thesis_*.md`. Do not translate `paper/main.tex` unless explicitly requested (use scientific-writing skill).

## Tests

`./scripts/run_tests.sh smoke` — same gate as Cursor; report PASS/FAIL in closure.

## Cursor ↔ Claude parity

After changing workflow, packs, or entry files: [`docs/sync_cursor_claude.md`](docs/sync_cursor_claude.md).
