---
name: from-thesis-to-paper Orchestration
overview: "Copy-paste subagent prompts to BUILD the from-thesis-to-paper framework repo (B1–B11) then RUN thesis→paper on a user workspace (SA0–SA13). User launches each chat manually; review CIERRE before next prompt."
todos:
  - id: build-b1-p0
    content: "B1: P0 repo scaffold"
    status: pending
  - id: build-b2-p1
    content: "B2: P1 executor docs"
    status: pending
  - id: build-b3-p2
    content: "B3: P2 core rules + skills"
    status: pending
  - id: build-b4-p3
    content: "B4: P3 optimization-or pack (parallel with B5)"
    status: pending
  - id: build-b5-p4
    content: "B5: P4 memory templates (parallel with B4)"
    status: pending
  - id: build-b6-p5
    content: "B6: P5 verify orchestration plan"
    status: pending
  - id: build-b7-p6
    content: "B7: P6 Python fttp"
    status: pending
  - id: build-b8-p7
    content: "B8: P7 npm CLI"
    status: pending
  - id: build-b9-p8
    content: "B9: P8 Overleaf MCP doc (parallel with B10)"
    status: pending
  - id: build-b10-p9
    content: "B10: P9 examples (parallel with B9)"
    status: pending
  - id: build-b11-p10
    content: "B11: P10 AGENTS + CLAUDE parity"
    status: pending
  - id: build-b12-p11
    content: "B12: P11 validate"
    status: pending
  - id: run-sa0
    content: "SA0: Workspace intake"
    status: pending
  - id: run-sa1
    content: "SA1: Venue policy"
    status: pending
  - id: run-sa2
    content: "SA2: Narrative interview"
    status: pending
  - id: run-sa2b
    content: "SA2b: Terminology glossary"
    status: pending
  - id: run-sa3
    content: "SA3: Archaeologist (parallel with SA3b)"
    status: pending
  - id: run-sa3b
    content: "SA3b: Math audit OR pack (parallel with SA3)"
    status: pending
  - id: run-sa4
    content: "SA4: Join auditor gate"
    status: pending
  - id: run-sa7
    content: "SA7: Paper strategist"
    status: pending
  - id: run-sa8
    content: "SA8: Writer"
    status: pending
  - id: run-sa9
    content: "SA9: Figures + LaTeX"
    status: pending
isProject: false
---

# from-thesis-to-paper — Subagent execution (BUILD + RUN)

> **Rule:** [`.cursor/rules/plan-and-subagent-orchestration.mdc`](../rules/plan-and-subagent-orchestration.mdc)  
> **Spec:** [`from-thesis-to-paper_master.plan.md`](from-thesis-to-paper_master.plan.md)  
> **Execution:** YOU launch one subagent per chat. Do NOT batch unless you say *"lanza todos los subagentes"*.

**Replace before paste:**
- `REPO_FTTP` = absolute path to **from-thesis-to-paper** framework clone (e.g. `~/from-thesis-to-paper`)
- `REPO_WORKSPACE` = absolute path to **user writable workspace** (thesis + paper + memory; NOT the framework repo unless testing in-repo)

---

## User cheat sheet — what to say (do not repeat long instructions)

The **full copy-paste blocks** for every step are **below in this file** (`### Prompt B1` … `### Prompt SA13`).  
You do **not** need to re-explain Guía / secuencial / paralelo / CIERRE each time — cite this plan.

| You want | Say exactly (Spanish or English) |
|----------|----------------------------------|
| Full BUILD + RUN map + all blocks | `Entrega Guía + todos los prompts según @from-thesis-to-paper_orchestration.plan.md` |
| Only execution guide + table | `Guía de ejecución from-thesis-to-paper` |
| One step only | `Dame el prompt B4` or `Dame el prompt SA4` |
| Next step after ✓ | `SA3 terminó OK — ¿siguiente prompt?` |
| Parallel pair | `B3 terminó — dame B4 y B5 para paralelo` |
| Skip optional | `Ruta rápida RUN — prompts SA0 a SA9 sin opcionales` |

**Cursor rule (already in repo):** [`.cursor/rules/plan-and-subagent-orchestration.mdc`](../rules/plan-and-subagent-orchestration.mdc) — agent **must** output Guía before prompts when you use the phrases above.

**Optional User Rule (paste in Cursor Settings → Rules):**  
`When I ask for subagent prompts, read .cursor/plans/from-thesis-to-paper_orchestration.plan.md, output Guía de ejecución first, then only the requested ### Prompt blocks in ```text``` fences. Do not summarize prompts.`

---

## Guía de ejecución

### Leyenda

| Símbolo | Tipo | Qué haces tú |
|---------|------|----------------|
| → | Secuencial | Espera **SE TERMINÓ LA TAREA COMPLETA** del prompt anterior; revisa HANDOFF; luego lanza el siguiente |
| ∥ | Paralelo | Tras el **mismo gate**, abre **2 chats** y pega un prompt en cada uno; espera **ambos** ✓ antes del siguiente secuencial |
| ~> | Async / on-demand | No bloquea la cadena; lanza cuando quieras si el prompt lo permite |

### Cómo leer el cierre de cada subagente

| Frase del subagente | Tu acción |
|---------------------|-----------|
| **SE TERMINÓ LA TAREA COMPLETA** | Revisa HANDOFF → lanza el/los prompt(s) indicados |
| **TAREA INCOMPLETA** + blocker | **No** lances el siguiente; arregla o pide prompt de nuevo |
| **BLOQUEADO: no lanzar prompt N** | No avances hasta override explícito tuyo |
| **LISTO PARA PARALELO:** … | Puedes abrir el segundo chat del par ∥ ahora |
| **LISTO PARA OPCIONAL:** … | Puedes saltar o lanzar async (~>) |

---

## Test gates (smoke / unit / integration)

Reference: `docs/TESTING.md` in framework repo (create in B7). Pattern from PaperEPN: `./scripts/run_tests.sh {smoke|unit|integration|all}`.

| Tier | Command | Gurobi needed? |
|------|---------|----------------|
| **smoke** | `./scripts/run_tests.sh smoke` | No (or skip toy MIP) |
| **unit** | `./scripts/run_tests.sh unit` | No |
| **integration** | `./scripts/run_tests.sh integration` | Yes |
| **all** | `./scripts/run_tests.sh all` | Yes for integration |

### Agent × tests (mandatory)

| Agent | Run | Blocks HANDOFF if fail? |
|-------|-----|-------------------------|
| B7 | `smoke` | **Yes** |
| B12 | `smoke` + optional `all` | **Yes** |
| SA0 | `fttp doctor`; `smoke` if `REPO_WORKSPACE/tests/` exists | doctor: **Yes** |
| SA3, SA3b | **No pytest** (read-only) | — |
| SA1, SA2, SA2b, SA7, SA8 | **No pytest** | — |
| **SA4** | `smoke` if `codigo/` or `tests/` present | **Yes** — gate before SA7 |
| SA5 | `smoke` then `integration` if OR pack + Gurobi | **Yes** |
| SA9 | **LaTeX only** (`fttp paper compile`) | PDF fail blocks |
| SA10 | Report last test status; run only if code_repro mode | — |
| SA11 | `smoke` + `unit`; `integration` if MIP changed | **Yes** |
| SA13 | `smoke` minimum in checklist | checklist item |

**Block pasted in code-touching prompts:**

```text
VERIFICACIÓN TESTS (when this agent’s table row requires it):
  cd <REPO> && ./scripts/run_tests.sh <smoke|unit|integration|all>
  Record exit code in HANDOFF. If exit != 0 → TAREA INCOMPLETA (last 30 lines stderr).
  Do not declare SE TERMINÓ if a required tier was not run.
```

---

### TRACK A — BUILD framework repo (once)

**Recomendación: 12 subagentes** — B4∥B5 ahorra tiempo; resto secuencial.

```text
B1 → B2 → B3 → (B4 ∥ B5) → B6 → B7 → B8 → (B9 ∥ B10) → B11 → B12
```

| # | Prompt | Topología | Lanzar cuando | Paralelo con |
|---|--------|-----------|---------------|--------------|
| **B1** | P0 scaffold | → | Empiezas BUILD; repo vacío creado en GitHub | — |
| **B2** | P1 docs | → | B1 ✓ | — |
| **B3** | P2 core skills | → | B2 ✓ | — |
| **B4** | P3 optimization-or pack | ∥ | B3 ✓ | **B5** (mismo gate) |
| **B5** | P4 templates | ∥ | B3 ✓ | **B4** |
| **B6** | P5 plan check | → | B4 ✓ **y** B5 ✓ | — |
| **B7** | P6 Python | → | B6 ✓ | — |
| **B8** | P7 npm CLI | → | B7 ✓ | — |
| **B9** | P8 MCP doc | ∥ | B8 ✓ | **B10** |
| **B10** | P9 examples | ∥ | B8 ✓ | **B9** |
| **B11** | P10 AGENTS | → | B9 ✓ **y** B10 ✓ | — |
| **B12** | P11 validate | → | B11 ✓ | — |

**Tras B12 ✓:** framework listo para publicar (`npm` / `npx` / `pip`). **No** implica rellenar rutas de tesis del mantenedor.

---

### TRACK B — RUN thesis → paper (per end-user project)

**Audiencia:** quien **instala** fttp en su propio workspace (tesis + paper + `memory/`), no el autor del repo framework durante BUILD.

**Ciclo de producto (orden):**

| Fase | Comando / paso | Quién |
|------|----------------|--------|
| **Install** | `pip install -e .` o `npx from-thesis-to-paper` | Usuario final |
| **Onboard** | `npx from-thesis-to-paper init` *(planeado)* **o** Prompt **SA0** `MODO: CONSUMER_ONBOARD` | Usuario final — rutas, pack, Overleaf, idioma |
| **Verify** | `npx from-thesis-to-paper doctor` | Usuario final |
| **RUN** | SA1 → SA13 en Cursor | Usuario final, con `fttp.config.json` ya relleno |

**Mantenedor post-B12 (opcional):** Prompt **SA0** `MODO: FRAMEWORK_SMOKE` solo en `REPO_FTTP` — plantillas + placeholders + `doctor`; sin preguntas de tesis.

**Recomendación: 10–13 subagentes** según packs y opcionales.

```text
SA0 → SA1 → SA2 → SA2b → (SA3 ∥ SA3b*) → SA4 [smoke gate] → SA7 → SA8 → SA9
async optional: SA5 ~> after SA4 | SA6 ~> after SA5 or SA4
on-demand: SA10 → SA11 | SA12 ~> after SA9 | SA13 ~> before submit
* SA3b solo si workspace.config packs incluye optimization-or
* SA3/SA3b: no pytest; SA4 smoke obligatorio si hay codigo/ o tests/
```

| # | Prompt | Topología | Lanzar cuando | Paralelo con |
|---|--------|-----------|---------------|--------------|
| **SA0** | Onboard / intake | → | Usuario final tras **install**; o SA0-SMOKE mantenedor | — |
| **SA1** | Venue policy | → | SA0 **CONSUMER_ONBOARD** ✓ | — |
| **SA2** | Narrative interview | → | SA1 ✓ | — |
| **SA2b** | Terminology | → | SA2 ✓ | — |
| **SA3** | Archaeologist | ∥ | SA2b ✓ | **SA3b** (si pack OR) |
| **SA3b** | Math audit | ∥ | SA2b ✓; solo si `optimization-or` | **SA3** |
| **SA4** | Join auditor + **smoke gate** | → | SA3 ✓ y (SA3b ✓ o omitido) | — |
| **SA7** | Strategist | → | SA4 ✓ | — |
| **SA8** | Writer | → | SA7 ✓; brief firmado | — |
| **SA9** | Figures + LaTeX | → | SA8 ✓ (o secciones críticas listas) | — |
| **SA5** | Refactor port | ~> | Tras SA4; opcional | no bloquea SA7 |
| **SA6** | Repro release | ~> | Tras SA5 o SA4 | no bloquea SA7 |
| **SA10** | Peer review | on-demand | Tras SA8/SA9 si pides review | — |
| **SA11** | Refactor fix | on-demand | Tras SA10 ítems CODE | — |
| **SA12** | Overleaf sync | ~> | Tras SA9; proyecto paper creado por ti | — |
| **SA13** | Submission | on-demand | Antes de enviar journal | — |

**Ruta rápida (sin review/refactor):** SA0 CONSUMER_ONBOARD → SA1 → SA2 → SA2b → SA3 → SA4 → SA7 → SA8 → SA9

**SA1–SA13:** requieren `fttp.config.json` y `memory/intake_report.md` del onboarding (no lanzar tras SA0 SMOKE con placeholders).

---

## Subagent prompts — TRACK A BUILD

### Prompt B1 — P0 Repository scaffold | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper BUILD | SUBAGENTE B1 de 12 | P0 | TOPOLOGÍA: secuencial
REPO_FTTP: <absolute path — set before paste>
PRECONDICIÓN: Empty GitHub repo from-thesis-to-paper exists; you have clone path REPO_FTTP
ESPERA A: none (first BUILD step)
USER LANGUAGE: Spanish or English — mirror user in chat; files in English

ROL: Scaffold the from-thesis-to-paper framework repository (directory tree only).

LEE:
1. REPO_FTTP/.cursor/plans/from-thesis-to-paper_master.plan.md — §2 layout
2. docs/EXECUTOR_GUIDE.md — create stub if missing after tree

TAREAS (literal order):
1. cd REPO_FTTP && git init (if not initialized)
2. Create every directory in master plan §2 (docs/, packages/cli/, python/fttp/, skills/core/, skills/packs/optimization-or/, templates/memory/, .cursor/rules/, .cursor/plans/, examples/, tests/, scripts/)
3. Add .gitignore: node_modules, .venv, .env, __pycache__, *.pdf, .overleaf-mcp, dist/
4. Add README.md (≤80 lines EN): product name, niche core+OR pack, quickstart placeholder
5. Add LICENSE MIT
6. git commit -m "fttp: P0 scaffold"

EJECUTA:
find REPO_FTTP -type d | wc -l
test -f REPO_FTTP/README.md && test -f REPO_FTTP/LICENSE

PROHIBIDO:
- Copy PaperEPN verification data or thesis PDF
- npm publish
- Edit mi-investigacion-opt unless REPO_FTTP is that path by user choice

ENTREGABLE:
- Tree exists; first commit

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (B1 / P0) if find shows ≥25 dirs and git log -1 exists
- HANDOFF: Launch Prompt B2 next (sequential →)
- LISTO PARA PARALELO: none
- TAREA INCOMPLETA if tree incomplete — blocker: <path>; BLOQUEADO: do not launch B2
```

---

### Prompt B2 — P1 Executor + architecture docs | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper BUILD | SUBAGENTE B2 de 12 | P1 | TOPOLOGÍA: secuencial
REPO_FTTP: <absolute path>
PRECONDICIÓN: B1 SE TERMINÓ LA TAREA COMPLETA
ESPERA A: B1 ✓

ROL: Write English documentation for weak-model executors.

LEE: from-thesis-to-paper_master.plan.md §3, §6 micro-steps P1

TAREAS:
1. Write docs/EXECUTOR_GUIDE.md — index P0–P11, stop-on-fail, bilingual chat note
2. Write docs/ARCHITECTURE.md — mermaid §3.1–3.3, fttp.config schema
3. Write docs/PAPER_PRODUCTION_PIPELINE.md — fttp subcommands table
4. Write docs/PORTFOLIO.md — niche §1 honest scope (core vs optimization-or)
5. git commit -m "fttp: P1 docs"

EJECUTA:
test -f docs/EXECUTOR_GUIDE.md && test -f docs/ARCHITECTURE.md && grep -q "TAREA INCOMPLETA" docs/EXECUTOR_GUIDE.md

PROHIBIDO: Spanish body in docs (English only)

ENTREGABLE: four md files

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (B2) if four files exist and EXECUTOR_GUIDE mentions stop rule
- HANDOFF: B3
- TAREA INCOMPLETA — BLOQUEADO: B3
```

---

### Prompt B3 — P2 Core rules + 12 core skills | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper BUILD | SUBAGENTE B3 de 12 | P2 | TOPOLOGÍA: secuencial
REPO_FTTP: <absolute path>
PRECONDICIÓN: B2 ✓
ESPERA A: B2

ROL: Create .cursor/rules and skills/core (12 skills, English, ≥40 lines each).

LEE: master plan §4 SA table (core skills list); copy orchestration pattern from mi-investigacion-opt .cursor/rules/plan-and-subagent-orchestration.mdc if available READ-ONLY

TAREAS:
1. .cursor/rules/plan-and-subagent-orchestration.mdc — replace PaperEPN → from-thesis-to-paper / fttp
2. .cursor/rules/bilingual-agent-interaction.mdc — alwaysApply true
3. .cursor/rules/fttp-non-negotiables.mdc — READ-ONLY roots, no invent numbers, TBD/DISCREPANCY; any codigo/ change requires smoke PASS before HANDOFF
4. .cursor/rules/translation.mdc — on-demand ES→EN
5. Create skills/core/: agent-intake, venue-submission-policy, narrative-interview, terminology-glossary, evidence-archaeologist, evidence-join-auditor, paper-strategy, scientific-writing, paper-figures-latex, peer-review, reproducibility-release, overleaf-sync-optional, submission-clerk (12 files)
6. Copy each to .cursor/skills/ (duplicate, not symlink)
7. git commit -m "fttp: P2 core skills"

EJECUTA:
ls skills/core | wc -l
ls .cursor/skills | wc -l

PROHIBIDO: optimization-or pack content in core (only pointers)

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (B3) if both counts = 12
- HANDOFF: Launch B4 AND B5 in parallel (∥) — two chats
- LISTO PARA PARALELO: B4 and B5 may start now
- TAREA INCOMPLETA — BLOQUEADO: B4, B5
```

---

### Prompt B4 — P3 optimization-or pack | TOPOLOGÍA: paralelo

```text
PLAN: from-thesis-to-paper BUILD | SUBAGENTE B4 de 12 | P3 | TOPOLOGÍA: paralelo
REPO_FTTP: <absolute path>
PRECONDICIÓN: B3 ✓
ESPERA A: B3 (same gate as B5)
PARALELO CON: Prompt B5 — do not edit templates/memory/ files B5 owns

ROL: Create optimization-or skill pack (6 skills + manifest).

LEE: master plan §4 optimization-or list; skills/packs/optimization-or/

TAREAS:
1. skills/packs/optimization-or/manifest.json — lists 6 skills, requires gurobipy optional
2. Create: mip-modeling-gurobi.md, graph-theory-routing.md, comp-geometry-gis.md, math-audit-mip.md, gurobi-log-lineage.md, refactor-port-mip.md (English, Triggers/Forbidden/Verify each)
3. docs/PACKS.md — how to enable packs in workspace.config.json
4. Mirror pack skills to .cursor/skills/packs/optimization-or/ if needed
5. git commit -m "fttp: P3 optimization-or pack" (only pack files)

EJECUTA:
test -f skills/packs/optimization-or/manifest.json && ls skills/packs/optimization-or/*.md | wc -l

PROHIBIDO: Edit templates/* ; Edit skills/core/* ; Add GurobiMCP

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (B4) if manifest + 6 md skills exist
- HANDOFF: Wait for B5 ✓ then user launches B6
- LISTO PARA PARALELO: user must also run B5; if B5 incomplete say "WAIT B5"
- TAREA INCOMPLETA — BLOQUEADO: B6 until B4 and B5 both complete
```

---

### Prompt B5 — P4 Memory templates | TOPOLOGÍA: paralelo

```text
PLAN: from-thesis-to-paper BUILD | SUBAGENTE B5 de 12 | P4 | TOPOLOGÍA: paralelo
REPO_FTTP: <absolute path>
PRECONDICIÓN: B3 ✓
ESPERA A: B3 (same gate as B4)
PARALELO CON: Prompt B4 — do not edit skills/packs/

ROL: Create templates/memory and workspace config example.

TAREAS:
1. templates/memory/agent_roster.md — §4 table from master plan
2. templates/memory/source_precedence.md
3. templates/memory/paper_strategy_brief_TEMPLATE.md
4. templates/memory/glossary_thesis_en_TEMPLATE.md
5. templates/memory/intake_report_TEMPLATE.md
6. templates/workspace.config.example.json — repoRoot, readOnlyRoots, packs, thesis, paper, evidence keys
7. templates/plans/_TEMPLATE_subagent_plan.md
8. git commit -m "fttp: P4 templates"

EJECUTA:
ls templates/memory | wc -l
python3 -c "import json; json.load(open('templates/workspace.config.example.json'))"

PROHIBIDO: Edit skills/packs/ ; Edit skills/core/

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (B5) if ≥6 template files and JSON valid
- HANDOFF: Wait for B4 ✓ then B6
- TAREA INCOMPLETA — BLOQUEADO: B6 until B4 and B5 both complete
```

---

### Prompt B6 — P5 Orchestration plan verify | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper BUILD | SUBAGENTE B6 de 12 | P5 | TOPOLOGÍA: secuencial
REPO_FTTP: <absolute path>
PRECONDICIÓN: B4 ✓ AND B5 ✓
ESPERA A: B4, B5

ROL: Ensure .cursor/plans/from-thesis-to-paper_orchestration.plan.md is complete; fix gaps only.

TAREAS:
1. Read this plan file in REPO_FTTP or mi-investigacion-opt source
2. Copy/sync to REPO_FTTP/.cursor/plans/from-thesis-to-paper_orchestration.plan.md if missing
3. Verify grep "SUBAGENTE" count ≥ 24 (B1–B12 + SA0–SA13)
4. git commit -m "fttp: P5 orchestration plan" if changed

EJECUTA:
grep -c "SUBAGENTE" .cursor/plans/from-thesis-to-paper_orchestration.plan.md

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (B6) if count ≥ 24
- HANDOFF: B7
- TAREA INCOMPLETA — BLOQUEADO: B7
```

---

### Prompt B7 — P6 Python fttp | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper BUILD | SUBAGENTE B7 de 12 | P6 | TOPOLOGÍA: secuencial
REPO_FTTP: <absolute path>
PRECONDICIÓN: B6 ✓
ESPERA A: B6

ROL: Implement python/fttp package stubs.

TAREAS:
1. pyproject.toml name fttp
2. python/fttp/config.py — load fttp.config.json / FTTP_CONFIG env
3. commands: tables, evidence, figures, compile — stub friendly messages if paths missing
4. pipeline.py orchestrate
5. docs/TESTING.md — tiers smoke|unit|integration|all (see plan § Test gates)
6. scripts/run_tests.sh supporting smoke|unit|integration|all + tests/test_config.py
7. pip install -e .
8. git commit -m "fttp: P6 python"

VERIFICACIÓN TESTS (obligatoria):
  cd REPO_FTTP && ./scripts/run_tests.sh smoke
  Record exit code in reply. If exit != 0 → TAREA INCOMPLETA (last 30 lines stderr).

EJECUTA:
./scripts/run_tests.sh smoke

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (B7) if smoke exit 0 and docs/TESTING.md exists
- HANDOFF: B8
- TAREA INCOMPLETA — BLOQUEADO: B8
```

---

### Prompt B8 — P7 npm CLI | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper BUILD | SUBAGENTE B8 de 12 | P7 | TOPOLOGÍA: secuencial
REPO_FTTP: <absolute path>
PRECONDICIÓN: B7 ✓
ESPERA A: B7

ROL: npm package from-thesis-to-paper bin fttp.

TAREAS:
1. packages/cli/package.json name from-thesis-to-paper bin fttp
2. packages/cli/src/cli.js — doctor, tables, evidence, figures, compile, pipeline → spawn python -m fttp
3. fttp.config.example.json at repo root
4. README quickstart npx from-thesis-to-paper doctor
5. node packages/cli/src/cli.js doctor
6. git commit -m "fttp: P7 npm cli"

EJECUTA:
node packages/cli/src/cli.js doctor

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (B8) if doctor exits 0
- HANDOFF: Launch B9 AND B10 parallel
- LISTO PARA PARALELO: B9, B10
```

---

### Prompt B9 — P8 Overleaf MCP doc | TOPOLOGÍA: paralelo

```text
PLAN: from-thesis-to-paper BUILD | SUBAGENTE B9 de 12 | P8 | TOPOLOGÍA: paralelo
REPO_FTTP: <absolute path>
PRECONDICIÓN: B8 ✓
PARALELO CON: B10

ROL: Optional Overleaf MCP documentation (no mandatory mcp.json).

TAREAS:
1. docs/MCP_OVERLEAF_OPTIONAL.md — thesis read-only, separate paper project, no Prism
2. git commit -m "fttp: P8 mcp doc"

PROHIBIDO: Commit .env passwords

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (B9)
- HANDOFF: After B10 ✓ → B11
```

---

### Prompt B10 — P9 Examples | TOPOLOGÍA: paralelo

```text
PLAN: from-thesis-to-paper BUILD | SUBAGENTE B10 de 12 | P9 | TOPOLOGÍA: paralelo
REPO_FTTP: <absolute path>
PRECONDICIÓN: B8 ✓
PARALELO CON: B9

ROL: External case study examples only.

TAREAS:
1. examples/README.md — PaperEPN is external, not submodule
2. examples/paperepn-external.config.json — placeholder paths only
3. examples/sample-workspace.config.json — generic
4. git commit -m "fttp: P9 examples"

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (B10)
- HANDOFF: After B9 ✓ → B11
```

---

### Prompt B11 — P10 AGENTS + CLAUDE | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper BUILD | SUBAGENTE B11 de 12 | P10 | TOPOLOGÍA: secuencial
REPO_FTTP: <absolute path>
PRECONDICIÓN: B9 ✓ AND B10 ✓
ESPERA A: B9, B10

ROL: Entry files Cursor + Claude parity.

TAREAS:
1. AGENTS.md — packs, orchestration plan link, EXECUTOR_GUIDE, no cross-load CLAUDE
2. CLAUDE.md — mirror; Shelby optional; Overleaf via npx not .cursor/mcp.json required
3. docs/sync_cursor_claude.md checklist
4. git commit -m "fttp: P10 agents entry"

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (B11)
- HANDOFF: B12
```

---

### Prompt B12 — P11 Validate | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper BUILD | SUBAGENTE B12 de 12 | P11 | TOPOLOGÍA: secuencial
REPO_FTTP: <absolute path>
PRECONDICIÓN: B11 ✓
ESPERA A: B11

ROL: Final BUILD validation.

TAREAS:
1. Fix only test/doc blockers found below
2. tag v0.1.0 optional ASK USER

VERIFICACIÓN TESTS (obligatoria — run in order, stop on first fail):
  cd REPO_FTTP && ./scripts/run_tests.sh smoke
  cd REPO_FTTP && ./scripts/run_tests.sh unit
  Optional if Gurobi available: ./scripts/run_tests.sh integration
  Or: ./scripts/run_tests.sh all (if integration supported)

EJECUTA:
./scripts/run_tests.sh smoke
./scripts/run_tests.sh unit
node packages/cli/src/cli.js doctor
grep -c "SUBAGENTE" .cursor/plans/from-thesis-to-paper_orchestration.plan.md

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (B12) — FRAMEWORK BUILD DONE — only if smoke AND unit exit 0; report integration skip/pass in HANDOFF
- HANDOFF: Publicar framework. Usuario final: install → SA0 CONSUMER_ONBOARD (o `fttp init` cuando exista) en su REPO_WORKSPACE. Mantenedor opcional: SA0 FRAMEWORK_SMOKE en REPO_FTTP
- LISTO PARA PARALELO: none
- TAREA INCOMPLETA — BUILD incomplete; BLOQUEADO: all SA*
```

---

## Subagent prompts — TRACK B RUN

### Prompt SA0 — Workspace onboarding (intake) | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA0 | TOPOLOGÍA: secuencial
REPO_FTTP: <framework clone path — npm package or git clone>
REPO_WORKSPACE: <user writable project path>
MODO: CONSUMER_ONBOARD | FRAMEWORK_SMOKE
PRECONDICIÓN: B12 BUILD complete OR framework installed via npm/npx; REPO_WORKSPACE exists
ESPERA A: none (RUN start for consumer; optional maintainer smoke after B12)
SKILL: skills/core/agent-intake.md

ROL: Onboard a workspace — copy fttp templates, write fttp.config.json + intake_report.md, run doctor.
Primary product path (document in HANDOFF): npx from-thesis-to-paper init (when CLI ships) asks the same questions as CONSUMER_ONBOARD.

─── MODO: CONSUMER_ONBOARD (default — end user installing fttp) ───
WHO: Graduate student / researcher adopting the open-source tool on THEIR machine.
ASK USER — do not skip; goal is **thesis → journal paper** in writable `paper/`:

A. **Workspace & paper (writable)**
1. Confirm REPO_WORKSPACE absolute path (`repoRoot`)?
2. **Paper output:** directory for the journal manuscript (default `paper/`) and main file (default `main.tex`)? Create dirs if missing.
   → `fttp.config.json` → `paper.dir`, `paper.mainTex`

B. **Thesis ground truth (read-only)**
3. **Thesis source:** `local` (disk) \| `overleaf` \| `both`?
4. If **local:** absolute path to thesis notebooks / thesis tree → `readOnlyRoots[]`
5. If **overleaf** or **both:** Overleaf **thesis** project id — tell user:
   - Browser URL: `https://www.overleaf.com/project/<24-char-hex>` — copy only the hex after `/project/`
   - Guide: `REPO_FTTP/docs/OVERLEAF_PROJECT_ID.md`
6. If **overleaf** or **both:** Overleaf MCP setup (required for Overleaf thesis):
   - Docs: `REPO_WORKSPACE/docs/OVERLEAF_MCP_SETUP.md` or framework `docs/MCP_OVERLEAF_OPTIONAL.md`
   - ASK: Overleaf **email** + **password** → write ONLY to `REPO_WORKSPACE/.env` (gitignored); record `set in .env` in intake_report, **never** commit or echo password in report
   - Install: `overleaf-mcp`, Playwright chromium, `scripts/overleaf_mcp.sh` + `.cursor/mcp.json` if Cursor
   - First login: `overleaf_login`, `overleaf_list_projects`; create `memory/overleaf_thesis_project.md`

C. **Experiments & niche**
7. Other READ-ONLY roots — verification, multigraph, inst_generation (optional; no multi-GB copy)?
8. Pack `optimization-or` (yes/no)?
9. Chat language (es/en)?

TAREAS (CONSUMER):
1. Copy REPO_FTTP/templates/memory/* → REPO_WORKSPACE/memory/ if missing
2. Ensure `paper/` (or chosen `paper.dir`) exists; add minimal `main.tex` stub only if user OK and missing
3. Copy `templates/workspace.config.example.json` → `fttp.config.json` — repoRoot, paper.*, readOnlyRoots[], packs, thesis.source, thesis.overleafProjectId
4. Write `memory/intake_report.md` from `intake_report_TEMPLATE.md` — all answers; no TBD on paper/thesis paths
5. If Overleaf: `.env` + MCP verify; copy `docs/OVERLEAF_PROJECT_ID.md` to workspace if missing
6. cd REPO_WORKSPACE && npx from-thesis-to-paper doctor (or node REPO_FTTP/packages/cli/src/cli.js doctor)

─── MODO: FRAMEWORK_SMOKE (maintainer only — post B12, not PaperEPN thesis data) ───
WHO: Framework author validating templates; NOT collecting a real user's thesis paths.
DO NOT ask the nine consumer questions (paper, thesis, Overleaf, MCP).
TAREAS (SMOKE):
1. In REPO_FTTP or empty test dir: copy templates/memory/* if missing
2. fttp.config.json from example with placeholder paths (/path/to/...) and packs: []
3. intake_report.md with section "Consumer onboarding — pending" and TBD on user answers
4. doctor exit 0 (warn on missing readOnlyRoots acceptable)

VERIFICACIÓN TESTS (both modes):
  doctor: mandatory — exit 0
  If REPO_WORKSPACE/tests/ OR REPO_WORKSPACE/scripts/run_tests.sh exists:
    cd REPO_WORKSPACE && ./scripts/run_tests.sh smoke
  Else: note "no tests yet — smoke skipped" in intake_report.md

PROHIBIDO: Write under readOnlyRoots; copy 57GB logs into workspace; hardcode PaperEPN OneDrive paths in framework repo

EJECUTA:
doctor exit 0; smoke if tests/ present

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA0) if intake_report.md + fttp.config.json + doctor OK (+ smoke OK or explicitly skipped)
  CONSUMER: paper.dir/mainTex set; thesis.source set; readOnlyRoots and/or Overleaf id + MCP (.env) if applicable; packs and lang recorded
  SMOKE: explicit "consumer onboarding pending" in intake_report.md
- HANDOFF: CONSUMER → SA1 (→) | SMOKE → none required; publish framework
- TAREA INCOMPLETA — BLOQUEADO: SA1–SA13 (CONSUMER mode only)
```

---

### Prompt SA1 — Venue policy scout | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA1 | TOPOLOGÍA: secuencial
REPO_WORKSPACE: <path>
PRECONDICIÓN: SA0 CONSUMER_ONBOARD ✓ — fttp.config.json filled by end user (not BUILD placeholders/TBD)
ESPERA A: SA0
SKILL: skills/core/venue-submission-policy.md

PREGUNTAS OBLIGATORIAS:
1. Primary journal + backup?
2. APC budget yes/no?
3. Target submission date?
4. Public data/repo policy comfort level?

TAREAS:
1. Web search official author guides (data, code, template, highlights)
2. Write REPO_WORKSPACE/memory/venue_submission_policy.md (English, dated)
3. Draft data/code availability requirements list for SA6/SA8

PROHIBIDO: Edit paper/main.tex

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA1) if venue_submission_policy.md exists
- HANDOFF: SA2
```

---

### Prompt SA2 — Narrative interview | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA2 | TOPOLOGÍA: secuencial
REPO_WORKSPACE: <path>
PRECONDICIÓN: SA1 ✓; SA0 CONSUMER_ONBOARD ✓ (readOnlyRoots in fttp.config.json)
ESPERA A: SA1
SKILL: skills/core/narrative-interview.md

PREGUNTAS OBLIGATORIAS (author story):
1. One-sentence contribution for a journal reader?
2. narrative_arc: thesis_mirror | contribution_first | integrated?
3. What thesis chapters are OUT of scope for the paper?
4. Three ideas the reviewer must remember?
5. Managerial takeaway for Discussion (yes/no)?

TAREAS:
1. Interview user; record in memory/narrative_interview.md
2. Update or create memory/paper_strategy_brief.md — Decision table, allowed/forbidden claims, approved_by user

PROHIBIDO: Write LaTeX body; change table numbers

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA2) if paper_strategy_brief.md signed by user OK
- HANDOFF: SA2b
- TAREA INCOMPLETA if user did not approve brief — BLOQUEADO: SA2b until OK
```

---

### Prompt SA2b — Terminology glossary | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA2b | TOPOLOGÍA: secuencial
REPO_WORKSPACE: <path>
PRECONDICIÓN: SA2 ✓ (brief approved)
ESPERA A: SA2
SKILL: skills/core/terminology-glossary.md

TAREAS:
1. Extract 15–30 key terms from thesis (Overleaf read OR memory/thesis sources)
2. Propose English equivalents; ASK USER confirm/reject/add per term
3. Write memory/glossary_thesis_en.md
4. Append ≤3 rows to REPO_FTTP/docs/TRANSLATION_GUIDE.md Maintenance if new canonical terms (append-only)

PROHIBIDO: Translate full thesis catalog table cells

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA2b) if glossary_thesis_en.md has user-confirmed terms
- HANDOFF: Launch SA3 AND SA3b (if optimization-or) in parallel
- LISTO PARA PARALELO: SA3; SA3b only if packs includes optimization-or
```

---

### Prompt SA3 — Evidence archaeologist | TOPOLOGÍA: paralelo

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA3 | TOPOLOGÍA: paralelo
REPO_WORKSPACE: <path>
PRECONDICIÓN: SA2b ✓; use readOnlyRoots from fttp.config.json (no writes there)
ESPERA A: SA2b (gate shared with SA3b)
PARALELO CON: SA3b (if enabled) — do not edit math_audit files
SKILL: skills/core/evidence-archaeologist.md

TAREAS:
1. Read memory/thesis_experiment_run_artifacts.md or templates equivalent
2. Document artifact glossary for this project in memory/artifact_glossary.md
3. Map run folder patterns → catalog rows (no invent objectives; TBD/DISCREPANCY)
4. Scripts only for log paths — no full log dump in chat

PROHIBIDO: Write readOnlyRoots; edit paper/tables numbers

VERIFICACIÓN TESTS: none (read-only archaeology — do not run pytest)

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA3)
- HANDOFF: Wait SA3b if running; then SA4 after both ✓
- TAREA INCOMPLETA — BLOQUEADO: SA4
```

---

### Prompt SA3b — Math audit (optimization-or) | TOPOLOGÍA: paralelo

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA3b | TOPOLOGÍA: paralelo
REPO_WORKSPACE: <path>
PRECONDICIÓN: SA2b ✓ AND fttp.config.json packs includes optimization-or
ESPERA A: SA2b
PARALELO CON: SA3
SKILLS: skills/packs/optimization-or/math-audit-mip.md, mip-modeling-gurobi.md

TAREAS:
1. Compare thesis equations vs code/notebooks (READ-ONLY sources)
2. Write memory/math_audit_report.md — code wins for formulation conflicts
3. List critical gaps for SA5 optional port

PROHIBIDO: Edit notebooks in readOnlyRoots

VERIFICACIÓN TESTS: none unless porting code in same session (then SA5 rules apply)

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA3b) OR skip with user waiver if pack disabled
- HANDOFF: SA4 after SA3 ✓
```

---

### Prompt SA4 — Join / evidence auditor (GATE) | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA4 | TOPOLOGÍA: secuencial
REPO_WORKSPACE: <path>
PRECONDICIÓN: SA3 ✓ AND (SA3b ✓ or waived)
ESPERA A: SA3, SA3b
SKILL: skills/core/evidence-join-auditor.md

TAREAS:
1. Triangulate thesis tables vs catalog vs logs (3-layer model)
2. Mark CONFIRMED / DISCREPANCY / TBD per row policy in brief
3. Write memory/join_audit_report.md
4. State if ready for paper tables export (yes/no)

VERIFICACIÓN TESTS (gate before SA7 — mandatory if codigo/ or tests/ exists):
  cd REPO_WORKSPACE && ./scripts/run_tests.sh smoke
  Record exit code in join_audit_report.md § Test status
  If exit != 0 → TAREA INCOMPLETA — BLOQUEADO: SA7, SA8

PROHIBIDO: Change LOCKED golden objectives without user LOCKED command

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA4) if join_audit_report.md + gate PASS for tables + smoke PASS (or no codigo/tests to run)
- HANDOFF: SA7 (strategist) — may skip SA5/SA6 async
- LISTO PARA OPCIONAL: SA5 ~> refactor port | SA6 ~> repro
- TAREA INCOMPLETA — BLOQUEADO: SA7, SA8
```

---

### Prompt SA5 — Refactor port (optional async) | TOPOLOGÍA: async

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA5 | TOPOLOGÍA: async (~>)
REPO_WORKSPACE: <path>
PRECONDICIÓN: SA4 ✓; user requested clean code OR SA3b gaps
ESPERA A: SA4 (does not block SA7)
SKILL: skills/packs/optimization-or/refactor-port-mip.md

TAREAS:
1. Port one model_id at a time to REPO_WORKSPACE/codigo/ — NEW files only
2. Update memory/code_lineage.md notebook→module map

VERIFICACIÓN TESTS (obligatoria after any codigo/ write):
  cd REPO_WORKSPACE && ./scripts/run_tests.sh smoke
  If optimization-or pack AND Gurobi available: ./scripts/run_tests.sh integration
  If exit != 0 → TAREA INCOMPLETA

PROHIBIDO: Modify readOnlyRoots originals

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA5) or user skip — only if smoke PASS (+ integration if run)
- HANDOFF: SA6 optional; SA7 may already run in parallel if user chose fast path
```

---

### Prompt SA6 — Reproducibility + release (optional async) | TOPOLOGÍA: async

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA6 | TOPOLOGÍA: async (~>)
REPO_WORKSPACE: <path>
PRECONDICIÓN: SA4 ✓ or SA5 ✓
SKILL: skills/core/reproducibility-release.md

TAREAS:
1. npx from-thesis-to-paper evidence build (if configured)
2. Update paper/REPRODUCIBILITY.md
3. Draft public repo README + Zenodo checklist per venue_submission_policy.md

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA6) or skip
- HANDOFF: none required before SA13
```

---

### Prompt SA7 — Paper strategist | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA7 | TOPOLOGÍA: secuencial
REPO_WORKSPACE: <path>
PRECONDICIÓN: SA4 ✓
ESPERA A: SA4
SKILL: skills/core/paper-strategy.md

TAREAS:
1. Reconcile brief with join_audit_report.md
2. Confirm cap4/cap5 table policy, forbidden claims, evidence_path
3. User explicit OK on brief

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA7) if brief signed
- HANDOFF: SA8
- BLOQUEADO: SA8 without brief OK
```

---

### Prompt SA8 — Scientific writer | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA8 | TOPOLOGÍA: secuencial
REPO_WORKSPACE: <path>
PRECONDICIÓN: SA7 ✓; glossary_thesis_en.md exists
ESPERA A: SA7
SKILL: skills/core/scientific-writing.md

TAREAS:
1. One section per session — English only in paper/main.tex
2. Use memory/glossary_thesis_en.md for terms
3. Do not change paper/tables/*.tex numeric cells
4. thesis_mirror: Results ch4 before ch5

PROHIBIDO: Paste Spanish thesis paragraphs; cite defended thesis in bib

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA8) per section scope agreed with user
- HANDOFF: SA9 when all sections drafted OR SA10 if user wants review first
- LISTO PARA OPCIONAL: SA10 on-demand
```

---

### Prompt SA9 — Figures + LaTeX | TOPOLOGÍA: secuencial

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA9 | TOPOLOGÍA: secuencial
REPO_WORKSPACE: <path>
PRECONDICIÓN: SA8 ✓ (critical sections)
ESPERA A: SA8
SKILL: skills/core/paper-figures-latex.md

TAREAS:
1. npx from-thesis-to-paper tables export (if needed)
2. npx from-thesis-to-paper figures
3. npx from-thesis-to-paper paper compile — or pdflatex per paper/README
4. Fix compile errors only in REPO_WORKSPACE/paper/

VERIFICACIÓN TESTS:
  LaTeX/PDF gate (not pytest): main.pdf builds without fatal errors
  Optional sanity: ./scripts/run_tests.sh smoke (do not block PDF on unrelated test fail — note in HANDOFF)

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA9) if main.pdf builds
- HANDOFF: SA12 optional; SA13 before submit; SA10 if review requested
- LISTO PARA OPCIONAL: SA12, SA10
```

---

### Prompt SA10 — Peer reviewer (on-demand) | TOPOLOGÍA: on-demand

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA10 | TOPOLOGÍA: on-demand
REPO_WORKSPACE: <path>
PRECONDICIÓN: User explicitly requested peer review; SA8 or SA9 has draft
SKILL: skills/core/peer-review.md

MODOS (pick one): manuscript | evidence | OR_science | code_repro

TAREAS:
1. Read-only review; write memory/peer_review_YYYYMMDD.md
2. Each finding: ID, severity blocker/major/minor, location, fix owner SA8/SA11/SA4
3. Do not edit files
4. If mode code_repro: record last `./scripts/run_tests.sh smoke` result from join_audit or re-run and cite exit code (do not fix code)

VERIFICACIÓN TESTS: reviewer does not fix — report status only unless user asks to re-run smoke

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA10) when report delivered
- HANDOFF: SA11 if CODE items; else SA8 polish; user decides
- BLOQUEADO: SA11 without SA10 report
```

---

### Prompt SA11 — Refactor fix (on-demand) | TOPOLOGÍA: on-demand

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA11 | TOPOLOGÍA: on-demand
REPO_WORKSPACE: <path>
PRECONDICIÓN: SA10 ✓ with CODE/REPRO items
ESPERA A: SA10
SKILL: skills/packs/optimization-or/refactor-port-mip.md

TAREAS:
1. Address only numbered items from peer review; new files only

VERIFICACIÓN TESTS (obligatoria):
  cd REPO_WORKSPACE && ./scripts/run_tests.sh smoke
  cd REPO_WORKSPACE && ./scripts/run_tests.sh unit
  If MIP/code items fixed: ./scripts/run_tests.sh integration (requires Gurobi)
  If any fail → TAREA INCOMPLETA

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA11) when items closed AND smoke+unit PASS (+ integration if MIP touched)
- HANDOFF: SA10 re-review optional; SA8 if prose items
```

---

### Prompt SA12 — Overleaf paper sync (optional) | TOPOLOGÍA: async

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA12 | TOPOLOGÍA: async (~>)
REPO_WORKSPACE: <path>
PRECONDICIÓN: User created separate Overleaf PAPER project; SA9 ✓
ESPERA A: none for chain

PREGUNTA OBLIGATORIA: Paper Overleaf project id? (NEVER thesis project id)

TAREAS:
1. overleaf_push_file from REPO_WORKSPACE/paper/main.tex
2. overleaf_compile
3. Document in memory/overleaf_paper_project.md

PROHIBIDO: overleaf_write on thesis project; canonical source stays git local

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA12) or skip if no Overleaf
```

---

### Prompt SA13 — Submission clerk (on-demand) | TOPOLOGÍA: on-demand

```text
PLAN: from-thesis-to-paper RUN | SUBAGENTE SA13 | TOPOLOGÍA: on-demand
REPO_WORKSPACE: <path>
PRECONDICIÓN: SA9 ✓; venue_submission_policy.md; user wants submit
SKILL: skills/core/submission-clerk.md

TAREAS:
1. Checklist vs venue policy (template, highlights, cover letter, ORCID, SI)
2. memory/submission_checklist.md PASS/FAIL per item
3. Do not submit without user click

VERIFICACIÓN TESTS (checklist items):
  - [ ] ./scripts/run_tests.sh smoke — PASS (mandatory)
  - [ ] ./scripts/run_tests.sh all — PASS or waived if no Gurobi (optimization-or projects)

---
CIERRE DE TAREA
- SE TERMINÓ LA TAREA COMPLETA (SA13) when checklist complete including smoke PASS
- HANDOFF: none — pipeline end
```

---

## Quick reference — what to launch next

| Last completed | Launch next |
|----------------|-------------|
| B1 ✓ | B2 |
| B3 ✓ | **B4 + B5** (two chats) |
| B4 ✓ and B5 ✓ | B6 |
| B8 ✓ | **B9 + B10** (two chats) |
| B12 ✓ | Publicar framework; usuario: **SA0 CONSUMER_ONBOARD** en su workspace (opcional: SA0 SMOKE en REPO_FTTP) |
| SA2b ✓ | **SA3** (+ **SA3b** if OR pack) |
| SA3 ✓ (+ SA3b) | SA4 |
| SA4 ✓ (incl. smoke gate) | SA7 (fast) or SA5~> then SA7 |
| SA5 ✓ | Re-run smoke before SA6; SA7 if not started |
| SA7 ✓ | SA8 |
| SA8 ✓ | SA9 or SA10 (if review) |

---

*End of orchestration plan — copy one `text` block per chat.*
