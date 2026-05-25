# Portfolio — from-thesis-to-paper (fttp)

> Honest scope statement for GitHub portfolio, recruiters, and weak executor agents.  
> Master plan reference: §1 Product vision and niche.

---

## Elevator pitch

**from-thesis-to-paper** productizes an agent-orchestrated workflow:

**thesis (ground truth) → evidence audit → narrative contract → LaTeX paper → optional peer review → optional public release**

The author’s proof-of-depth case study is **electric vehicle routing with terrain-aware GIS** (EVRP-SSSMP), implemented with **exact methods (Gurobi MIP)**. The **core framework** is domain-agnostic for STEM theses with computational experiments; the **optimization-or pack** is the specialized plug-in.

---

## What this repo **is**

| Aspect | Description |
|--------|-------------|
| **Problem class** | Thesis-to-journal paper with tabulated experiments, run artifacts (logs, CSV, JSON), and LaTeX |
| **Method** | Multi-agent orchestration (SA0–SA13) with explicit skill files per role |
| **Deliverable** | Open framework: rules, skills, templates, `fttp` CLI, docs — plus optional OR pack |
| **Evidence discipline** | Read-only archaeology roots; writable workspace; no invented table cells |
| **Reference implementation** | **PaperEPN** (`mi-investigacion-opt`) — external case study, not a submodule |

### Core framework (broad niche)

Works well for theses with:

- Computational experiments and reproducible artifacts
- LaTeX (or exportable tables → LaTeX)
- Journal submission discipline (strategy brief, reproducibility appendix)
- Graduate student + AI agent co-editing

Domains: applied math, engineering, CS, OR, statistics — any thesis with **numbers + logs + LaTeX**.

### optimization-or pack (narrow differentiator)

Optional pack for:

- MIP / Gurobi build and solve patterns
- Routing and multigraph preprocessing
- GIS instance generation (slopes, OSMnx-style workflows)
- Math audit (equations vs code)
- Notebook → modular `.py` refactor ports

**Requires explicit enable** in workspace config: `"packs": ["optimization-or"]`. Core agents must run **without** Gurobi installed.

---

## What this repo is **not**

| Misconception | Reality |
|---------------|---------|
| Generic “essay to paper” tool | Requires computational work and numeric artifacts |
| Full optimization platform | No cloud solver farm, no generic modeling GUI |
| PaperEPN data dump | Does not ship 57GB verification trees or thesis PDF |
| Replacement for thesis defense workflow | Focus is **journal paper** from audited evidence |
| Qualitative-only theses | No numeric artifacts → poor fit |
| Implicit OR expertise in every agent | OR skills only when pack is enabled and SA declares it |

---

## Core vs optimization-or boundary

```mermaid
flowchart TB
  subgraph core [Core_always_shipped]
    intake[Intake]
    venue[Venue_policy]
    narrative[Narrative_glossary]
    archaeologist[Evidence_archaeologist]
    strategy[Paper_strategy]
    writer[Scientific_writer]
    figures[Figures_LaTeX_verify]
    submit[Submission_clerk]
  end

  subgraph opt [Pack_optimization_or_optional]
    mathaudit[Math_MIP_audit]
    gurobi[Gurobi_log_lineage]
    refactor[Refactor_port_MIP]
    mip[MIP_Gurobi_skill]
    graph[Routing_multigraph]
    gis[GIS_instances]
  end

  core --> paper[paper/main.pdf]
  opt -.-> core
```

| Layer | Serves | Portfolio message |
|-------|--------|-------------------|
| **Core** | Any STEM thesis→paper with evidence | “I built a reusable agent framework.” |
| **optimization-or** | OR / logistics / discrete optimization | “I ship domain depth as an explicit plug-in.” |

Agents **must declare** which skill paths they load (see `templates/memory/agent_roster.md` after P4).

---

## Audience

| Audience | How to use this doc |
|----------|---------------------|
| **Graduate student** | Understand fit before adopting; configure `repoRoot` + `readOnlyRoots`; run SA0 intake |
| **Weak executor agent** | Read [`EXECUTOR_GUIDE.md`](EXECUTOR_GUIDE.md); one micro-step per commit; stop on verify fail |
| **Reviewer / recruiter** | Judge portfolio on framework + OR pack honesty, not on bundled thesis data |
| **Maintainer** | Keep PaperEPN as external evidence; framework repo stays small and MIT-licensed |

---

## PaperEPN relationship (external case study)

| Item | In `from-thesis-to-paper` repo? |
|------|--------------------------------|
| Agent orchestration pattern | **Yes** (generalized from PaperEPN) |
| optimization-or skill **content** | **Yes** (ported stubs, no data) |
| EVRP thesis tables, 242-row catalog, golden T185 | **No** — stays in user workspace |
| `mi-investigacion-opt` git tree | **No** — cited in `examples/` only |

Live thesis work can continue in PaperEPN; the portfolio ships the **framework**, not the dissertation artifacts.

### EVRP case study highlights (PaperEPN only)

- Steep-terrain electric logistics (Quito / Frutería pilot → INST_GEN → MULTIGRAPH)
- Cap. 4 model comparison (MOD, SSS) and Cap. 5 SSSMP (locked T185)
- Computers & Operations Research target venue
- Evidence path: thesis-mirror tables + reproducibility tier B documented separately

These details illustrate the **optimization-or** pack; they are not required for core framework users.

---

## Demo script (portfolio v0.1.0)

After P11 validation:

1. Clone `from-thesis-to-paper`.
2. `npx from-thesis-to-paper doctor` (no Gurobi required).
3. Show `docs/ARCHITECTURE.md` diagrams and 12 core + 6 OR skills on disk.
4. Open orchestration plan — copy-paste SA0 prompt.
5. Point to `examples/README.md`: PaperEPN paths as external case study.

Do **not** demo by copying OneDrive verification into the repo.

---

## Version and license intent

- Target: public repo `from-thesis-to-paper`, **MIT** recommended for portfolio.
- npm package name: `from-thesis-to-paper`, bin: `fttp`.
- Publish to npm only with explicit user approval.

---

## Related documentation

| File | Topic |
|------|-------|
| [`EXECUTOR_GUIDE.md`](EXECUTOR_GUIDE.md) | P0–P11 build phases |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Layers, config, repo layout |
| [`PAPER_PRODUCTION_PIPELINE.md`](PAPER_PRODUCTION_PIPELINE.md) | CLI and script matrix |
| [`.cursor/plans/from-thesis-to-paper_master.plan.md`](../.cursor/plans/from-thesis-to-paper_master.plan.md) | Full build spec |

---

*Honest niche per master plan §1 and Appendix C.*
