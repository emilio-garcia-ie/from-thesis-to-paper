# Executor Guide — from-thesis-to-paper (fttp)

> **Audience:** weak executor agents and graduate students running the build plan.  
> **Language:** all documentation bodies in this repo are **English only**. User chat may be Spanish or English.

## Purpose

This guide is the step index for implementing the **from-thesis-to-paper** (`fttp`) framework. Follow micro-steps in [`.cursor/plans/from-thesis-to-paper_master.plan.md`](../.cursor/plans/from-thesis-to-paper_master.plan.md) literally. Do not skip verification gates.

**Reference workspace:** `mi-investigacion-opt` (PaperEPN) holds the master plan and these docs until copied into the standalone `from-thesis-to-paper` repository.

---

## Stop-on-fail rule (mandatory)

After **every** micro-step, run the **Verify** command listed in the master plan.

- If verification **fails**, **halt immediately**.
- Report closure as **`TAREA INCOMPLETA`** (use this exact phrase in your message to the user).
- Include: step id, verify command, stderr or exit code, and what you tried.
- **Do not** start the next phase until the user or orchestrator explicitly overrides.

Success path: run verify → pass → commit (if the step says so) → proceed.

---

## Phase index (P0–P11)

| Phase | ID | Goal | Primary deliverables | Verify hint |
|-------|-----|------|----------------------|-------------|
| **P0** | `p0-repo-scaffold` | Empty public repo scaffold | `README.md`, `LICENSE`, `.gitignore`, directory tree §2 | `git status`, `find . -type d \| wc -l` ≥ 25 |
| **P1** | `p1-executor-docs` | Executor + architecture docs | `docs/EXECUTOR_GUIDE.md`, `ARCHITECTURE.md`, `PAPER_PRODUCTION_PIPELINE.md`, `PORTFOLIO.md` | `grep TAREA INCOMPLETA docs/EXECUTOR_GUIDE.md` |
| **P2** | `p2-core-rules-skills` | Core Cursor rules + 12 core skills | `.cursor/rules/*`, `skills/core/*.md`, mirror `.cursor/skills/` | `ls skills/core \| wc -l` = 12 |
| **P3** | `p3-opt-pack-skills` | optimization-or pack (6 skills) | `skills/packs/optimization-or/*`, `docs/PACKS.md` | valid `manifest.json` |
| **P4** | `p4-memory-templates` | Workspace templates | `templates/memory/*`, `workspace.config.example.json` | JSON parse |
| **P5** | `p5-master-plan-prompts` | SA0–SA13 copy-paste prompts | `.cursor/plans/from-thesis-to-paper_orchestration.plan.md` | `grep -c SUBAGENTE` ≥ 14 |
| **P6** | `p6-python-pipeline` | Python `fttp` package | `python/fttp/`, `pyproject.toml` | `pip install -e .`, pytest |
| **P7** | `p7-npm-cli` | npm `fttp` CLI | `packages/cli/`, `fttp.config.example.json` | `node packages/cli/src/cli.js doctor` |
| **P8** | `p8-mcp-docs` | Optional Overleaf MCP | `docs/MCP_OVERLEAF_OPTIONAL.md` | file exists |
| **P9** | `p9-examples` | External case study config | `examples/README.md`, `paperepn-external.config.json` | no secrets |
| **P10** | `p10-agents-entry` | Agent entry parity | `AGENTS.md`, `CLAUDE.md`, `docs/sync_cursor_claude.md` | cross-check lists |
| **P11** | `p11-validate` | Release validation | tests + doctor | `./scripts/run_tests.sh`, `npx from-thesis-to-paper doctor` |

**Recommended commit message pattern:** `fttp: <phase-id> <short description>` (e.g. `fttp: P1 docs`).

---

## Bilingual interaction

| Context | Language |
|---------|----------|
| User ↔ agent chat | Spanish **or** English (user preference) |
| New repo files (`docs/`, `skills/`, rules) | **English only** |
| Generated paper LaTeX | **English** (journal manuscript) |
| Thesis memory templates (`thesis_*`) | Often Spanish source; glossary via SA2b before writing |

See `docs/TRANSLATION_GUIDE.md` when the user requests ES→EN translation of infra files.

---

## Continuous onboarding (runtime SA0–SA13)

Product onboarding does not end after SA0. Every runtime step should help the user understand **why** before **what**, and require **explicit approval** before HANDOFF on gated artifacts.

Canonical references:

| Doc | Role |
|-----|------|
| [ONBOARDING_RATIONALE.md](ONBOARDING_RATIONALE.md) | WHY / ASK / YOU_DO per SA0 block |
| [USER_APPROVAL_GATES.md](USER_APPROVAL_GATES.md) | G0–G13, tokens, `workflowProfile` matrix |
| [WORKSPACE_MODEL.md](WORKSPACE_MODEL.md) | Three-repo boundaries |

### WHY-before-ASK (mandatory)

Before each user question or block transition:

1. Emit **2–4 sentences**: why the step matters, what it protects, what it unlocks.
2. Use labels: **`WHY:`** → **`ASK:`** → **`YOU_DO:`**
3. Wait for brief confirmation or an answer; if declined, log `skipped` + reason in `memory/intake_report.md`.
4. **Prohibited:** question lists without a WHY paragraph; internal jargon (“SA3 gate”) without user-facing benefit.

### AUDIT and APPROVE_ASK (mandatory on gated steps)

After creating or updating a gate artifact:

1. **`AUDIT:`** — paths, 3–7 bullet checklist for the user.
2. **`APPROVE_ASK:`** — request `APPROVED: <gate_id>` or `APROBADO: <gate_id>`.
3. Write `memory/user_approval_log.md` with `status: approved` (or `approved_with_edits`) before HANDOFF.
4. Without approval → **`TAREA INCOMPLETA`** and **`BLOQUEADO: no lanzar SA<n+1>`**.

### Mini-Guía (every SA prompt SA1–SA13)

Prefix each runtime prompt with:

```text
WHY_THIS_STEP: <2–3 sentences — use chat_language; English canonical in plan/docs>
WHAT_I_NEED: <inputs, files, confirmations>
WHAT_I_WILL_NOT_TOUCH: <readOnlyRoots, thesis Overleaf, framework repo, …>
```

Optional mirror in orchestration prompts as three bullets: **Why this step** / **What I need** / **What I will not touch**.

---

## Handoff and closure protocol

Every subagent or executor step must end with one of:

### Success

```text
SE TERMINÓ LA TAREA COMPLETA (<Subagente or Phase>)
HANDOFF: <next step id> — <one line what it does>
```

Optional payload (≤5 lines): paths created, verify output summary, commit hash.

### Failure

```text
TAREA INCOMPLETA
<step-id>: <what failed>
<verify command and error>
BLOQUEADO: <next step id> — do not launch until fixed
```

### Orchestration map (runtime agents, not build phases)

After the framework is built, user-controlled subagents SA0–SA13 follow [`.cursor/plans/from-thesis-to-paper_orchestration.plan.md`](../.cursor/plans/from-thesis-to-paper_orchestration.plan.md). Build phases P0–P11 are **implementation** of the framework repo itself.

---

## Read order (first session)

1. This file (`docs/EXECUTOR_GUIDE.md`)
2. [`docs/ARCHITECTURE.md`](ARCHITECTURE.md) — layers, config schema, repo boundaries
3. [`docs/PORTFOLIO.md`](PORTFOLIO.md) — what the product is / is not
4. Master plan §0–§3 — [`.cursor/plans/from-thesis-to-paper_master.plan.md`](../.cursor/plans/from-thesis-to-paper_master.plan.md)

---

## Practical commands

### PaperEPN (current reference repo)

| Task | Command |
|------|---------|
| Smoke tests | `./scripts/run_tests.sh smoke` |
| Export tables from catalog | `python scripts/paper/export_tables_from_catalog.py` (see script `--help`) |
| Build evidence bundle | `python scripts/paper/build_evidence_bundle.py` |
| Generate figures | `python scripts/paper/generate_figures.py` |
| LaTeX build | `cd paper && latexmk -pdf main.tex` (or project Makefile) |

### fttp framework (after P6–P7)

| Task | Command |
|------|---------|
| Health check | `npx from-thesis-to-paper doctor` |
| Full paper pipeline | `npx from-thesis-to-paper pipeline` |
| Subcommands | See [`docs/PAPER_PRODUCTION_PIPELINE.md`](PAPER_PRODUCTION_PIPELINE.md) |

### Configuration

- Copy `fttp.config.example.json` → `fttp.config.json` in workspace root (or set `FTTP_CONFIG`).
- Schema: [`docs/ARCHITECTURE.md`](ARCHITECTURE.md) § Configuration.

---

## What executors must NOT do

- Copy 57GB verification trees or massive logs into any repo.
- Edit **read-only** roots (`Thesis Code/`, OneDrive verification folders).
- Invent numeric results in paper tables (use catalog, logs, or mark TBD/DISCREPANCY).
- Enable GurobiMCP.
- Commit `.env`, passwords, or API tokens.
- Merge `from-thesis-to-paper` as a subdirectory of PaperEPN (separate public repo).

---

## Related documentation

| Document | Contents |
|----------|----------|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Mermaid diagrams, `fttp.config.json`, layout |
| [`ONBOARDING.md`](ONBOARDING.md) | Install → SA0 → doctor → RUN |
| [`ONBOARDING_RATIONALE.md`](ONBOARDING_RATIONALE.md) | WHY-before-ASK blocks |
| [`USER_APPROVAL_GATES.md`](USER_APPROVAL_GATES.md) | Audit/approve gates |
| [`WORKSPACE_MODEL.md`](WORKSPACE_MODEL.md) | Three-repo model |
| [`PAPER_PRODUCTION_PIPELINE.md`](PAPER_PRODUCTION_PIPELINE.md) | CLI subcommands, tables → PDF |
| [`PORTFOLIO.md`](PORTFOLIO.md) | Portfolio narrative, core vs OR pack |
| [`TRANSLATION_GUIDE.md`](TRANSLATION_GUIDE.md) | ES→EN infra translation |
| [`OVERLEAF_MCP_SETUP.md`](OVERLEAF_MCP_SETUP.md) | PaperEPN Overleaf MCP (optional) |

---

## ASK USER gates

Stop and ask the user (do not guess) when the master plan says **ASK USER**, including:

- GitHub org/username for the new `from-thesis-to-paper` remote
- Absolute `repoRoot` and `readOnlyRoots` for a workspace
- Whether to enable `optimization-or` pack
- Preferred chat language (es/en)

---

*Last aligned with master plan: from-thesis-to-paper_master.plan.md (P1).*
