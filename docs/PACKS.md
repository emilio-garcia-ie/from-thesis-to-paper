# Skill packs — from-thesis-to-paper

Optional domain packs extend the **core** agent skills (`skills/core/`). Core agents must run **without** installing Gurobi or OR-specific tooling.

---

## Enable a pack

Add the pack id to the workspace config at the repository root (`workspace.config.json` or `fttp.config.json`):

```json
{
  "workspaceName": "my-thesis-workspace",
  "repoRoot": "/absolute/path/to/writable/project",
  "readOnlyRoots": [],
  "paper": {
    "dir": "paper",
    "mainTex": "main.tex"
  },
  "packs": ["optimization-or"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `packs` | `string[]` | no | Enabled pack ids; omit or `[]` for core-only |

### Schema example (minimal)

```json
{
  "workspaceName": "example-or-thesis",
  "repoRoot": "/path/to/workspace",
  "packs": []
}
```

```json
{
  "workspaceName": "example-or-thesis",
  "repoRoot": "/path/to/workspace",
  "packs": ["optimization-or"]
}
```

Copy a full template from `templates/workspace.config.example.json` (P4) when available.

---

## Available packs

| Pack id | Path | Gurobi required? | Typical agents |
|---------|------|------------------|----------------|
| `optimization-or` | `skills/packs/optimization-or/` | **Optional** (`gurobipy`, `gurobi_cl`) | SA3b, SA4 (log lineage), SA5, SA11 |

Manifest: [`skills/packs/optimization-or/manifest.json`](../skills/packs/optimization-or/manifest.json)

### optimization-or skills

| Slug | File | Purpose |
|------|------|---------|
| `mip-modeling-gurobi` | `mip-modeling-gurobi.md` | Build/solve MIP; `gurobi_cl`; no GurobiMCP |
| `graph-theory-routing` | `graph-theory-routing.md` | Graphs, multigraph preprocessing |
| `comp-geometry-gis` | `comp-geometry-gis.md` | GIS instances, slopes, OSMnx-style flows |
| `math-audit-mip` | `math-audit-mip.md` | Equations vs code (SA3b) |
| `gurobi-log-lineage` | `gurobi-log-lineage.md` | Batch log parse, lineage CSV |
| `refactor-port-mip` | `refactor-port-mip.md` | Notebook → `codigo/` port |

---

## How agents load packs

1. **SA0 intake** records which packs are enabled in `memory/workspace_intake.md`.
2. Orchestration prompts for SA3b / SA5 / SA11 reference pack paths only when `optimization-or` is listed.
3. Core skills (e.g. evidence-archaeologist) **must not** embed pack steps — they point to `docs/PACKS.md` or the manifest.

---

## Cursor mirror

Pack skills are mirrored under `.cursor/skills/packs/optimization-or/<slug>/SKILL.md` for Cursor discovery (copy of canonical `skills/packs/optimization-or/*.md`).

---

## Verify pack on disk

```bash
test -f skills/packs/optimization-or/manifest.json && ls skills/packs/optimization-or/*.md | wc -l
```

Expect **6** `.md` skill files (excluding `manifest.json`).

---

## Related docs

- [`ARCHITECTURE.md`](ARCHITECTURE.md) §2 agent and skill packs
- [`PORTFOLIO.md`](PORTFOLIO.md) core vs optimization-or boundary
- [`EXECUTOR_GUIDE.md`](EXECUTOR_GUIDE.md) phase P3
