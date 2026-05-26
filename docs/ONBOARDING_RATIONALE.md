# Onboarding rationale — WHY before ASK

> **Audience:** agents (SA0–SA13) and users who want context before answering questions.  
> **Language:** English canonical text; agents may translate to the user's chat language while keeping config and memory files in English.

## Rule: WHY-before-ASK

Before each question or user action:

1. Emit **2–4 sentences**: why it matters, what it protects, what it unlocks next.
2. Use the fixed labels: **`WHY:`** → **`ASK:`** → **`YOU_DO:`**
3. Do not advance to the next block until the user confirms briefly (`ok`, `understood`, `yes`) **or** provides an answer.
4. If the user declines an optional step, record `skipped` + reason in `memory/intake_report.md`.

Full product rules: [EXECUTOR_GUIDE.md](EXECUTOR_GUIDE.md) § Continuous onboarding.

---

## SA0 blocks (CONSUMER_ONBOARD)

### Block 0 — Slug

| | |
|--|--|
| **WHY** | Separates the journal article from the thesis and keeps huge verification trees out of the publishable repo. Using the **same name** for the Git folder and the Overleaf **paper** project reduces sync errors in SA12. |
| **ASK** | Short project name for the paper (`workspaceSlug`). |
| **YOU_DO** | Create a new folder or Git repo with that exact name; plan an empty Overleaf project with the same display name. |

---

### Block A — New paper workspace

| | |
|--|--|
| **WHY** | The framework does not store your thesis. You need one **writable** workspace for the manuscript, agent memory, and audited evidence copies. |
| **ASK** | Absolute path to the **new** repo root (not `REPO_FTTP`). |
| **YOU_DO** | Copy `templates/paper-workspace/` (or run `fttp scaffold` when available); optional `git init`. |

---

### Block B — Thesis read-only sources

| | |
|--|--|
| **WHY** | Thesis and original runs are **ground truth**. Agents read and copy subsets; they must **not** edit notebooks, thesis Overleaf, or verification trees. |
| **ASK** | Paths to thesis sources: local folder, cloud mount, NAS, and/or Overleaf **thesis** project id (read-only). |
| **YOU_DO** | Confirm you will not ask agents to modify those locations; add paths to `readOnlyRoots` in config. |

---

### Block B2 — Overleaf paper project (separate from thesis)

| | |
|--|--|
| **WHY** | A **new** Overleaf project holds only the article manuscript. Your thesis project stays untouched; SA12 can sync `paper/` without risk to the dissertation. |
| **ASK** | Create an empty Overleaf project named like `workspaceSlug`; paste the 24-character project id into config / `.env`. |
| **YOU_DO** | Create the project at overleaf.com; store credentials only in gitignored `.env`. |

**MCP (optional):**

| | |
|--|--|
| **WHY** | Overleaf MCP lets agents read thesis tables and text for `thesis_adapt` without manual PDF export. |
| **ASK** | Whether to enable MCP; email/token in `.env` only. |
| **YOU_DO** | Cursor: project `.cursor/mcp.json` — **or** Claude Code: `npx overleaf-mcp` per [MCP_OVERLEAF_OPTIONAL.md](MCP_OVERLEAF_OPTIONAL.md). |

---

### Block C — Workflow profile

| | |
|--|--|
| **WHY** | Not everyone needs refactor, public release, or full MIP porting. Choosing a profile avoids spending time on agents you will skip. |
| **ASK** | `paper_only` \| `paper_audit` \| `paper_audit_repro` \| `full_pipeline` |
| **YOU_DO** | Set `workflowProfile` in `fttp.config.json`; note how many approval gates apply — [USER_APPROVAL_GATES.md](USER_APPROVAL_GATES.md). |

---

### Block D — Writing mode

| | |
|--|--|
| **WHY** | `thesis_adapt` preserves your voice by condensing defended thesis prose; `compose` drafts more from scratch (higher risk of generic tone). `hybrid` mixes both with a provenance map. |
| **ASK** | `thesis_adapt` \| `compose` \| `hybrid` (default recommended: `thesis_adapt`). |
| **YOU_DO** | Set `writingMode` in config; SA8 uses `memory/provenance_map.md` when adapting. |

---

### Block E — Environment (.env)

| | |
|--|--|
| **WHY** | Reproducible runs need Gurobi paths, data roots, and API tokens without guessing from old notebooks. |
| **ASK** | Review proposed `.env.example` (from `fttp env-suggest` or SA0 scan of RO `requirements.txt` / imports). |
| **YOU_DO** | Copy to `.env`, edit values, never commit secrets. |

---

### Block F — Chat language

| | |
|--|--|
| **WHY** | You may prefer Spanish explanations while the submission manuscript stays English. |
| **ASK** | `es` or `en` for agent chat in this workspace. |
| **YOU_DO** | Tell the agent; LaTeX under `paper/` remains English unless the venue requires otherwise. |

---

### Block G — Venue stub (mandatory before SA1 handoff)

| | |
|--|--|
| **WHY** | The target journal or conference defines document class, page limits, references, and figure rules. Without a venue stub, SA8 prose may not compile to an acceptable PDF. |
| **ASK** | Primary venue name + author guidelines URL; how you provide the template (`local_path`, zip into `paper/latex/`, download URL, or Overleaf template project id); optional backup venue. |
| **YOU_DO** | Copy **your** template files into `paper/latex/`; confirm the framework does **not** ship publisher `.cls` files. |

Deep policy extraction is **SA1** — see [VENUE_TEMPLATE_ONBOARDING.md](VENUE_TEMPLATE_ONBOARDING.md).

**WHY for SA1 (one paragraph):** SA1 turns your stub into `memory/venue_policy.md`, validates `\documentclass` against files on disk, and blocks SA7/SA8 if the template is missing (unless you explicitly sign `templateDeferred` with a date).

---

## After SA0 — approval before SA1

| | |
|--|--|
| **WHY** | You are the final authority: agents propose paths and config, but you confirm they match your real thesis layout and journal target. |
| **ASK** | Review `AUDIT: G0-intake` checklist; reply `APPROVED: G0-intake` or corrections. |
| **YOU_DO** | Add a row to `memory/user_approval_log.md` with `status: approved`. |

Details: [USER_APPROVAL_GATES.md](USER_APPROVAL_GATES.md).

---

## Agent copy-paste template

```text
WHY: <2-4 sentences>
ASK: <single clear question>
YOU_DO: <concrete user action>
```

For runtime steps SA1–SA13, also use the Mini-Guía header in [EXECUTOR_GUIDE.md](EXECUTOR_GUIDE.md).

---

## Related docs

| Doc | Contents |
|-----|----------|
| [ONBOARDING.md](ONBOARDING.md) | Step-by-step install and RUN |
| [WORKSPACE_MODEL.md](WORKSPACE_MODEL.md) | Three-repo model and slug |
| [USER_APPROVAL_GATES.md](USER_APPROVAL_GATES.md) | G0–G13 gates |
