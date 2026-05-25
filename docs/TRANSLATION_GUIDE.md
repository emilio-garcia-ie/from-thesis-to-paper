# Translation Guide (ES → EN)

**Append-only reference — read on demand.**  
Do not load this file unless a translation task is classified as **SCIENTIFIC** or **MIXED**.  
Agents may append new glossary rows at the bottom (see [Maintenance](#maintenance)); never rewrite prior rows.

---

## Scope

Paths below use **`REPO_WORKSPACE`** for the user’s writable project root (where `paper/`, `memory/`, and `fttp.config.json` live). **`REPO_FTTP`** is this framework repository (`from-thesis-to-paper`).

### Infra in scope (full translate when asked)

| Path (under `REPO_WORKSPACE` or `REPO_FTTP`) | Notes |
|------|--------|
| `AGENTS.md` / `CLAUDE.md` | Entry files; translation § and infra pointers |
| `memory/agent_stack.md` | Agent stack / plugin verdicts |
| `docs/sync_cursor_claude.md` | Cursor ↔ Claude parity checklist |
| `.cursor/plans/*_master.plan.md` | **Master playbook only** — preserve YAML todo `id`s |
| `.cursor/rules/translation.mdc` | On-demand rule (English in fttp) |
| `paper/README.md` | Paper status / build notes |
| `paper/REPRODUCIBILITY.md` | Replication narrative |

### Banner-only (`thesis_*` memory — no body translation)

| Path | Notes |
|------|--------|
| `memory/thesis_experiment_catalog.md` | Catalog table rows may stay in source language |
| `memory/thesis_model_registry.md` | Formulation cells stay in source language |
| Other `memory/thesis_*.md` | Structural prose may stay Spanish until explicit request |

Add the standard **Agent note** + **Translation** banner after the title block. Full file translation only on **explicit user request**.

### Out of scope (never translate via this guide)

| Path | Reason |
|------|--------|
| `paper/main.tex`, `paper/tables/*.tex` | Use workspace `scientific-writing` / project-specific writer skill — English manuscript |
| `codigo/**`, `experimentos/**`, consumer `tests/**` | Code, data, and fixtures stay as-is |
| `memory/thesis_*.md` **table cells** | Authoritative numeric / thesis fields |
| Thesis notebooks, verification trees in `readOnlyRoots` | **READ-ONLY** historical sources |

---

## Scientific translation

### Domain discipline

Operations Research / vehicle routing / MIP. Tone: formal journal English (pick American or British per document and stay consistent).

### Terminology mapping (canonical)

| Spanish (source) | English (target) | Notes |
|------------------|------------------|-------|
| ruteo (de vehículos) | vehicle routing | Not “routing” alone in titles |
| multigrafo | multigraph | Extended network layers |
| instancia(s) de prueba | test instance(s) | |
| formulación / modelo | formulation / model | Match `model_id` when present |
| experimento computacional | computational experiment | IMRaD Results |
| valor objetivo | objective value | From solver log when authoritative |
| brecha MIP / gap | MIP gap | Gurobi terminology |
| tesis | thesis | Do **not** cite as bibliography in paper |
| trazabilidad / linaje | lineage | Evidence policy |
| discrepancia | discrepancy | catalog vs log |
| contribución | contribution | Introduction bullets |

### Model and experiment IDs (preserve verbatim)

Keep experiment IDs (`T###`), model tags, and LaTeX macros unchanged when describing an existing `main.tex`.

### Academic standards (non-negotiable)

1. **No thesis self-citation** as a bibliographic source in manuscript text unless venue policy explicitly allows it.
2. **Forbidden claims:** do not strengthen Spanish prose into English claims not supported by signed strategy brief and Results tables.
3. **Venue checklists:** keep journal names, APC amounts, and URLs literal; translate explanatory prose only.

### IMRaD section labels

| ES | EN |
|----|-----|
| Resumen / Abstract | Abstract |
| Introducción | Introduction |
| Estado del arte | Literature and Background |
| Modelos / Metodología | Models / Methodology |
| Experimentos computacionales | Computational Experiments |
| Resultados | Results |
| Discusión | Discussion |
| Conclusiones | Conclusion |

---

## Repo and technical translation

| Spanish | English | Context |
|---------|---------|---------|
| verificación | verification | read-only roots |
| notebook gemelo | twin notebook | Archaeology phase |
| pipeline reproducible | reproducible pipeline | `paper/REPRODUCIBILITY.md` |
| fixture | fixture | tests / golden JSON |

---

## Maintenance

### Append-only glossary log

Add new rows **only** at the end, **max 3 entries per translation task**:

```text
- ES phrase → EN phrase | SCIENTIFIC | optional note
- ES phrase → EN phrase | REPO | optional note
- ES phrase → EN phrase | MIXED | optional note
```

**DOMAIN** values: `SCIENTIFIC` | `REPO` | `MIXED`.

### Initial seed entries

- tesis defendida → defended thesis | SCIENTIFIC | never bibliographic cite in paper
- guía de revistas → journal guidelines | REPO | `paper/JOURNAL_GUIDELINES.md` in consumer workspace
- orden espejo de la tesis → thesis_mirror narrative order | SCIENTIFIC | Results subsection order in brief

---

*Framework copy — generic `REPO_WORKSPACE` paths; consumer workspaces may extend this file locally.*
