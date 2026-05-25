# AGENTS.md — from-thesis-to-paper framework (Cursor)

> **Cursor entry only.** Claude Code uses [`CLAUDE.md`](CLAUDE.md) — same phases and guardrails, **do not cross-load** (see [`docs/sync_cursor_claude.md`](docs/sync_cursor_claude.md)).

## Entry boundary (mandatory)

| Stack | Read | Do **not** load as entry |
|-------|------|---------------------------|
| **Cursor** | This file + `.cursor/rules/` + `.cursor/skills/` | `CLAUDE.md`, `.claude/**` |
| **Claude Code** | `CLAUDE.md` + `.claude/skills/` | `AGENTS.md`, `.cursor/skills/**` |

**Shared (both):** `memory/`, `docs/`, `skills/`, `scripts/`, `.cursor/plans/` (orchestration and archaeology playbooks).

**Weak executor index:** [`docs/EXECUTOR_GUIDE.md`](docs/EXECUTOR_GUIDE.md) — stop-on-fail, closure tokens (`SE TERMINÓ LA TAREA COMPLETA`, `TAREA INCOMPLETA`, `HANDOFF:`).

## from-thesis-to-paper (fttp)

Standalone **fttp** framework repository. User workspaces (e.g. PaperEPN `mi-investigacion-opt`) are **external** — see [`examples/README.md`](examples/README.md) and [`examples/paperepn-external.config.json`](examples/paperepn-external.config.json).

| Topic | Doc |
|-------|-----|
| Build phases P0–P11 | [`.cursor/plans/from-thesis-to-paper_master.plan.md`](.cursor/plans/from-thesis-to-paper_master.plan.md) |
| Runtime SA0–SA13 prompts | [`.cursor/plans/from-thesis-to-paper_orchestration.plan.md`](.cursor/plans/from-thesis-to-paper_orchestration.plan.md) |
| Architecture / config | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) |

## Skill packs (optional)

Core agents run **without** Gurobi. Enable domain packs in `workspace.config.json` / `fttp.config.json`:

```json
{ "packs": ["optimization-or"] }
```

| Pack | When | Doc |
|------|------|-----|
| `optimization-or` | MIP/GIS/log-lineage thesis workflows | [`docs/PACKS.md`](docs/PACKS.md) |

Canonical skills: `skills/core/` and `skills/packs/<pack>/`. Cursor mirrors under `.cursor/skills/` (including `packs/optimization-or/`).

## Workspace (6 folders)

| Folder | Role | Edit? |
|--------|------|-------|
| `mi-investigacion-opt/` | Active repo: `codigo/`, `paper/`, `memory/`, `scripts/` | **Yes** |
| `Thesis Code/` | Master notebooks | **READ-ONLY** |
| OneDrive `Models comparison_/` | Cap. 4 verification (~57 GB) | **READ-ONLY** |
| OneDrive `multigrafo/` | Cap. 5 verification | **READ-ONLY** |
| OneDrive `inst_generation/` | Instances | **READ-ONLY** |
| OneDrive `Pilot1 …` | EDA pilot | **READ-ONLY** |

## Phases (summary)

1. Math audit — thesis vs code (code wins)
2. Archaeology — twin notebooks, Excel/log summaries only
3. Refactor — `.py` pipelines, `.env`
4. **Paper** — LaTeX in `paper/` (this phase)
5. Future algorithms — after paper submit

**Guardrails:** Max 3 logical steps then summarize; token protection (no log dumps); never edit verification trees.

## Plans and subagents (default workflow)

When the user asks for a **plan**, **prompts**, or **part of a plan**, follow [`.cursor/rules/plan-and-subagent-orchestration.mdc`](.cursor/rules/plan-and-subagent-orchestration.mdc):

1. **Agent** chooses N subagents and labels each **sequential (→)**, **parallel (∥)**, or **async (~>)** in the launch map.
2. **User** launches each chat manually; reviews cierre; asks for next prompt (“dame el prompt 3”).
3. On “dame los prompts” / “ejecuta el plan X”: deliver **Guía de ejecución** first (leyenda topología + mapa + tabla cuándo lanzar), **then** numbered copy-paste blocks — never silent batch unless user says *“lanza todos los subagentes”*.
4. Plans in [`.cursor/plans/`](.cursor/plans/) with DoD, todos, CIERRE / HANDOFF / TAREA INCOMPLETA in each prompt.

| Resource | Path |
|----------|------|
| Orchestration rule | [`.cursor/rules/plan-and-subagent-orchestration.mdc`](.cursor/rules/plan-and-subagent-orchestration.mdc) |
| Plan template | [`.cursor/plans/_TEMPLATE_subagent_execution_plan.md`](.cursor/plans/_TEMPLATE_subagent_execution_plan.md) |
| fttp runtime prompts | [`.cursor/plans/from-thesis-to-paper_orchestration.plan.md`](.cursor/plans/from-thesis-to-paper_orchestration.plan.md) |
| PaperEPN example | [`.cursor/plans/p4_paper_completo_797d4550.plan.md`](.cursor/plans/p4_paper_completo_797d4550.plan.md) |

Skip for trivial one-file fixes unless requested.

## On-demand memory

- `memory/thesis_scientific_structure.md`
- `memory/thesis_model_registry.md`
- `memory/thesis_experiment_catalog.md`
- `memory/thesis_ab_cross_review.md`
- `memory/paper_strategy_brief.md`
- `memory/paper_narrative_map.md`
- `memory/agent_stack.md`
- `memory/workspace_inventory.md`
- `memory/thesis_experiment_run_artifacts.md` — run design, artifact glossary, log lineage workflow (read before OneDrive logs)

Playbook: `.cursor/plans/thesis_to_golden_archaeology.plan.md`

## Gurobi

- CLI: `gurobi_cl modelo.lp`
- Python: `gurobipy` — pack skill `mip-modeling-gurobi` (requires `optimization-or`)
- **Do not** add GurobiMCP

## Overleaf MCP (Cursor)

- Config: `.cursor/mcp.json` → `scripts/overleaf_mcp.sh` (loads repo `.env`)
- Setup: `docs/OVERLEAF_MCP_SETUP.md` — credentials, first login, thesis project id
- Optional / not required: `docs/MCP_OVERLEAF_OPTIONAL.md`
- Discovery file: `memory/overleaf_thesis_project.md`
- **Read-only** on thesis Overleaf for table/value archaeology; edit `paper/` locally
- **Do not** commit `.env` or Overleaf passwords

## Shelby MCP (optional — Cursor + Claude)

**ShelbyMCP** (graph + cross-session memory) is optional on **both** stacks. Complements git-tracked `memory/`; does not replace catalog or signed brief for numbers.

- **Cursor:** `npx shelbymcp setup cursor --forage` (or manual `~/.cursor/mcp.json` / project `.cursor/mcp.json`) — see [`docs/MCP_SHELBY_OPTIONAL.md`](docs/MCP_SHELBY_OPTIONAL.md)
- **Claude Code:** `npx shelbymcp setup claude-code --forage`; workspace `.claude/settings.local.json` for `mcp__shelbymcp__*` permissions
- **Stack table:** `memory/agent_stack.md` (user workspace)

## Domain skills (`.cursor/skills/`)

**Core (always available):** `agent-intake`, `narrative-interview`, `terminology-glossary`, `evidence-archaeologist`, `evidence-join-auditor`, `paper-strategy`, `scientific-writing`, `paper-figures-latex`, `reproducibility-release`, `overleaf-sync-optional`, `venue-submission-policy`, `submission-clerk` — canonical text under `skills/core/`.

**Pack `optimization-or` (if enabled):** `graph-theory-routing`, `mip-modeling-gurobi`, `comp-geometry-gis`, `math-audit-mip`, `gurobi-log-lineage`, `refactor-port-mip` — see [`docs/PACKS.md`](docs/PACKS.md).

## Translation (on demand)

When the user asks to translate or requests an English version of a file:

1. Follow `.cursor/rules/translation.mdc`.
2. Read `docs/TRANSLATION_GUIDE.md` for SCIENTIFIC or MIXED content.
3. **Default targets:** infra paths in the guide’s *Infra in scope* table (`memory/agent_stack.md`, `docs/sync_cursor_claude.md`, `.cursor-state.md`, master playbook `.cursor/plans/thesis_to_golden_archaeology.plan.md`); **banner-only** for `memory/thesis_*.md` (no table-cell translation unless explicitly requested).

Do not translate `paper/main.tex` unless explicitly requested.

## Tests

`./scripts/run_tests.sh smoke` — Gurobi, log lineage, paper pipeline fixtures + legend figure

## Cursor ↔ Claude parity

After changing workflow, packs, or entry files: [`docs/sync_cursor_claude.md`](docs/sync_cursor_claude.md). Extended PaperEPN notes: `memory/sync_cursor_claude.md`.
