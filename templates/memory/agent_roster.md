# Agent roster — from-thesis-to-paper (fttp)

> **Template:** copy to `memory/agent_roster.md` on workspace intake (SA0) or keep as reference.  
> **Canonical source:** master plan §4 — [`.cursor/plans/from-thesis-to-paper_master.plan.md`](../../.cursor/plans/from-thesis-to-paper_master.plan.md).  
> **Skill paths:** adjust if your repo mirrors skills under `.cursor/skills/` only.

## Launch topology (summary)

```text
SA0 → SA1 → SA2 → SA2b → (SA3 ∥ SA3b*) → SA4 → SA7 → SA8 → SA9 → [SA13]
async: SA5 ~> after SA4  |  SA6 ~> after SA5 or SA4
on-demand: SA10 → SA11  |  SA12 ~> after SA9
* SA3b only if workspace config `packs` includes `optimization-or`
```

**Fast path (no review/port):** `SA0 → SA1 → SA2 → SA2b → SA3 → SA4 → SA7 → SA8 → SA9`

---

## Agent roster (17) — skill binding

| SA | Role | Skill path | Pack required? |
|----|------|------------|----------------|
| SA0 | Workspace + thesis intake | `skills/core/agent-intake.md` | no |
| SA1 | Venue policy scout | `skills/core/venue-submission-policy.md` | no |
| SA2 | Narrative interview | `skills/core/narrative-interview.md` | no |
| SA2b | Terminology EN glossary | `skills/core/terminology-glossary.md` | no |
| SA3 | Evidence archaeologist | `skills/core/evidence-archaeologist.md` | no |
| SA3b | Math / formulation audit | `skills/packs/optimization-or/math-audit-mip.md` | **yes** if thesis has MIP |
| SA4 | Join / triangulation auditor | `skills/core/evidence-join-auditor.md` | no |
| SA4o | OR-specific lineage (optional) | `skills/packs/optimization-or/gurobi-log-lineage.md` | optional |
| SA5 | Refactor port (new files only) | `skills/packs/optimization-or/refactor-port-mip.md` | optional |
| SA6 | Repro + release packager | `skills/core/reproducibility-release.md` | no |
| SA7 | Paper strategist | `skills/core/paper-strategy.md` | no |
| SA8 | Scientific writer | `skills/core/scientific-writing.md` | no |
| SA9 | Figures + LaTeX verify | `skills/core/paper-figures-latex.md` | no |
| SA10 | Peer reviewer | `skills/core/peer-review.md` | no |
| SA11 | Refactor fix | `skills/packs/optimization-or/refactor-port-mip.md` | optional |
| SA12 | Overleaf sync (paper project) | `skills/core/overleaf-sync-optional.md` | no |
| SA13 | Submission clerk | `skills/core/submission-clerk.md` | no |

---

## optimization-or pack (optional)

Enable in `fttp.config.json` / `workspace.config.json`:

```json
"packs": ["optimization-or"]
```

| Pack skill | Purpose |
|------------|---------|
| `mip-modeling-gurobi.md` | Build/solve patterns; `gurobi_cl`; **no** GurobiMCP |
| `graph-theory-routing.md` | Networks, multigraph preprocessing |
| `comp-geometry-gis.md` | Instances, slopes, GIS workflows |
| `math-audit-mip.md` | Equations vs code (SA3b) |
| `gurobi-log-lineage.md` | Log parse batch; no log dumps in chat |
| `refactor-port-mip.md` | Notebook→`.py`; READ-ONLY sources |

Each skill file MUST contain YAML frontmatter (`name`, `description`) and sections: **Triggers**, **Read order**, **Steps**, **Forbidden**, **Verify**.

---

## Workspace-specific notes

| Field | Value |
|-------|--------|
| **workspace_name** | `TBD` |
| **repoRoot** | `TBD` |
| **packs_enabled** | `TBD` — e.g. `[]` or `["optimization-or"]` |
| **last_intake** | `TBD` — ISO date after SA0 |
