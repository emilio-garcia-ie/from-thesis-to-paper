# CLAUDE.md — PaperEPN / from-thesis-to-paper (Claude Code)

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

This repository hosts the **fttp** framework (`python/fttp/`, `skills/core/`, `examples/`) and the PaperEPN reference workspace.

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

## Project map (single source of truth)

**GOLDEN RULE:** Historical folders are **STRICTLY READ-ONLY**. Never modify them.

### Active environment (writable)

* `mi-investigacion-opt/`: current workspace root.
  * `codigo/` — refactored modular `.py` scripts.
  * `experimentos/` — validated results (JSON/Excel summaries).
  * `paper/` — journal manuscript `.tex`.
  * `memory/` — thesis/paper memory (shared with Cursor).
  * `memoria_hallazgos/` — discrepancy logs and technical debt (PaperEPN).

### Historical and raw data (read-only)

* `Thesis Code/` — master notebooks (formulation ground truth).
* OneDrive `Models comparison_/` (~57 GB) — Chapter 4 verification.
* OneDrive `multigrafo/` — Chapter 5 verification.
* OneDrive `inst_generation/` — GIS instance scripts.
* OneDrive `Pilot1 …` — EDA pilot.

## Workspace (6 folders)

| Folder | Role | Edit? |
|--------|------|-------|
| `mi-investigacion-opt/` | Active repo | **Yes** |
| `Thesis Code/` | Master notebooks | **READ-ONLY** |
| OneDrive `Models comparison_/` | Cap. 4 verification | **READ-ONLY** |
| OneDrive `multigrafo/` | Cap. 5 verification | **READ-ONLY** |
| OneDrive `inst_generation/` | Instances | **READ-ONLY** |
| OneDrive `Pilot1 …` | EDA pilot | **READ-ONLY** |

## Mandatory execution flow (phases)

### Phase 1 — Mathematical audit (thesis vs code)

1. Compare thesis equations to master notebooks. **Code wins.**
2. Document corrections in `memoria_hallazgos/math_corrections.md` (or `memory/` as appropriate).

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

Document proposals in `memoria_hallazgos/future_algorithms.md` — column generation, search memory, GIS generalization.

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

Overleaf MCP is **optional**. Claude does **not** require `.cursor/mcp.json`.

- Install/run via npm: `npx overleaf-mcp` (see [`docs/OVERLEAF_MCP_SETUP.md`](docs/OVERLEAF_MCP_SETUP.md) and [`docs/MCP_OVERLEAF_OPTIONAL.md`](docs/MCP_OVERLEAF_OPTIONAL.md)).
- Load credentials from gitignored `.env` locally — never commit secrets.
- **Thesis project:** read-only archaeology; numeric authority = catalog + signed brief, not Overleaf alone.
- **Paper:** edit and build local `paper/`; optional SA12 sync to a separate paper project.

## Shelby MCP (optional — Claude only)

**ShelbyMCP** (graph + persistent memory) is optional and typically configured in `.claude/settings.local.json`. Not used in Cursor. See `memory/agent_stack.md`.

## Domain skills (`.claude/skills/`)

Mirror of Cursor skills when synced. **Core:** SA0–SA13 paths under `skills/core/`. **Pack `optimization-or`:** see [`docs/PACKS.md`](docs/PACKS.md) — enable only when config lists the pack.

## Behavior guardrails

* **Specify and approve:** Max 3 logical steps without summary/approval — **except** when the user approved a written plan with explicit subagent sequence.
* **Token protection:** Never dump large files; prefer Excel summaries and catalog rows.
* **Mentor the user:** Explain *why* for engineering choices in `memoria_hallazgos/` or `memory/`.
* **Translation (on demand):** Follow `.cursor/rules/translation.mdc` and `docs/TRANSLATION_GUIDE.md`. **Default targets:** infra paths in the guide’s *Infra in scope* table (`memory/agent_stack.md`, `docs/sync_cursor_claude.md`, `.cursor-state.md`, master playbook `.cursor/plans/thesis_to_golden_archaeology.plan.md`); **banner-only** for `memory/thesis_*.md`. Do not translate `paper/main.tex` unless explicitly requested (use scientific-writing skill).

## Tests

`./scripts/run_tests.sh smoke` — same gate as Cursor; report PASS/FAIL in closure.

## Cursor ↔ Claude parity

After changing workflow, packs, or entry files: [`docs/sync_cursor_claude.md`](docs/sync_cursor_claude.md).
