---
name: agent-intake
description: SA0 workspace onboarding v2 — blocks 0–G with WHY-before-ASK; new paper repo; workflowProfile; writingMode; G0-intake approval; dual-stack MCP (Cursor or Claude Code)
---

# Agent intake (SA0) — v2

## Modes

| Mode | Who | User interaction |
|------|-----|------------------|
| **CONSUMER_ONBOARD** | End user after install / first RUN | **Required** — blocks **0–G** with **WHY → ASK → YOU_DO** per block; **G0-intake** audit + user approval before HANDOFF |
| **FRAMEWORK_SMOKE** | Maintainer post-B12 | **Do not ask** consumer blocks — placeholders + `intake_report.md` notes onboarding pending; no G0 approval |

**Product path:** `fttp scaffold --slug NAME` or copy `templates/paper-workspace/` when CLI scaffold is unavailable. Future `fttp init` will ask the same questions as CONSUMER_ONBOARD.

## Goal

Configure **thesis → journal paper** under the [three-repo model](../docs/WORKSPACE_MODEL.md):

- **REPO_FTTP** — framework (read-only for user data)
- **SOURCES_RO** — thesis / verification trees (read-only)
- **PAPER_WS** — **new** writable Git repo for one article (`memory/`, `paper/`, `experimentos/`)

## Triggers

- End user installs fttp and needs `fttp.config.json` + `memory/`.
- `fttp doctor` reports missing paths or slug mismatch.
- User says “intake”, “onboard”, “configure workspace”, “SA0”.
- Before evidence or LaTeX when `memory/intake_report.md` is absent or stale (CONSUMER only).
- Before SA1 when `memory/user_approval_log.md` lacks **approved** row for `G0-intake`.

## Read order

1. [WORKSPACE_MODEL.md](../docs/WORKSPACE_MODEL.md) — three layers, slug rule, copy manifest.
2. [ONBOARDING_RATIONALE.md](../docs/ONBOARDING_RATIONALE.md) — canonical WHY text per block (reuse in chat).
3. [USER_APPROVAL_GATES.md](../docs/USER_APPROVAL_GATES.md) — G0-intake checklist and closure tokens.
4. [VENUE_TEMPLATE_ONBOARDING.md](../docs/VENUE_TEMPLATE_ONBOARDING.md) — Block G stub vs SA1 deep policy.
5. `fttp.config.json` or `workspace.config.json` if partial config exists.
6. `templates/workspace.config.example.json` — `workspaceSlug`, `workflowProfile`, `writingMode`, `overleafPaper`, `paper.venueProfiles`, `readOnlyRoots[]`, `packs[]`.
7. `templates/paper-workspace/` — scaffold tree for new repos.
8. `docs/ARCHITECTURE.md` § config — field definitions.
9. `docs/OVERLEAF_PROJECT_ID.md` — 24-char hex from Overleaf URL.
10. **Overleaf MCP (optional):** `docs/MCP_OVERLEAF_OPTIONAL.md` (framework) or workspace `docs/OVERLEAF_MCP_SETUP.md`.
11. `docs/PACKS.md` — domain pack choice.
12. `AGENTS.md` / `CLAUDE.md` + `docs/EXECUTOR_GUIDE.md` — closure protocol and WHY-before-ASK rule.

## Interaction rule — WHY-before-ASK

Before **each** block (0–G):

1. Emit **`WHY:`** (2–4 sentences) → **`ASK:`** (one clear question) → **`YOU_DO:`** (concrete user action).
2. Wait for brief confirmation (`ok`, `understood`, `yes`) **or** the answer.
3. Record `user_ack` / `skipped` + reason in `memory/intake_report.md`.
4. Do **not** list questions without a WHY paragraph — see [ONBOARDING_RATIONALE.md](../docs/ONBOARDING_RATIONALE.md).

Chat language: user's choice (`es` / `en`); config and memory files stay **English**.

---

## CONSUMER_ONBOARD — blocks 0–G

### Block 0 — Slug (`workspaceSlug`)

| | |
|--|--|
| **WHY** | Separates the journal article from the thesis and keeps large verification trees out of the publishable repo. Using the **same name** for the Git folder and the Overleaf **paper** project reduces sync errors in SA12. |
| **ASK** | Short project name for the paper (`workspaceSlug`). |
| **YOU_DO** | Create a new folder or Git repo with that exact name; plan an empty Overleaf **paper** project with the same display name. |

**Agent:** Validate slug format when config validators exist: `^[a-z0-9][a-z0-9_-]{2,63}$`. Set `workspaceSlug` / `workspaceName` in config.

---

### Block A — New paper workspace (`repoRoot`)

| | |
|--|--|
| **WHY** | The framework does not store your thesis. You need one **writable** workspace for the manuscript, agent memory, and audited evidence copies — **not** `REPO_FTTP`. |
| **ASK** | Absolute path to the **new** repo root (or parent dir + slug if creating now). |
| **YOU_DO** | Confirm `git init` if desired; do not use the framework clone as `repoRoot`. |

**Agent steps:**

1. Copy `REPO_FTTP/templates/paper-workspace/` → `PAPER_WS` (or run `fttp scaffold --slug <slug> --parent <dir>` when available).
2. Replace `{{WORKSPACE_SLUG}}` placeholders in scaffold `fttp.config.json`.
3. Copy `REPO_FTTP/templates/memory/*` → `PAPER_WS/memory/` if missing (do not overwrite user-edited briefs without OK).
4. Initialize `memory/user_approval_log.md` from `templates/memory/user_approval_log_TEMPLATE.md` (header + TBD rows; no secrets).
5. Set `repoRoot` in `fttp.config.json`.

---

### Block B — Thesis read-only sources

| | |
|--|--|
| **WHY** | Thesis and original runs are **ground truth**. Agents read and copy bounded subsets; they must **not** edit notebooks, thesis Overleaf, or verification trees. |
| **ASK** | Thesis sources: local folder path(s), cloud mount, NAS, and/or Overleaf **thesis** project id (read-only). Optional extra RO roots (batch logs, GIS, verification). |
| **YOU_DO** | Confirm you will not ask agents to modify those locations. |

**Agent:** Set `thesis.source` (`local` \| `overleaf` \| `both`); append paths to `readOnlyRoots[]`; set `thesis.overleafProjectId` if applicable (24-char hex — `docs/OVERLEAF_PROJECT_ID.md`). Create `memory/overleaf_thesis_project.md` when Overleaf thesis id is set.

**Generic paths only** — do not assume OneDrive or PaperEPN layout in framework docs.

---

### Block B2 — Overleaf paper project + MCP (optional)

| | |
|--|--|
| **WHY (paper project)** | A **new** Overleaf project holds only the article manuscript. Your thesis project stays untouched; SA12 can sync `paper/` without risk to the dissertation. |
| **ASK** | Create an empty Overleaf **paper** project named like `workspaceSlug`; paste the 24-character project id. |
| **YOU_DO** | Create the project at overleaf.com; store credentials only in gitignored `.env`. |

| | |
|--|--|
| **WHY (MCP)** | Overleaf MCP lets agents read thesis tables and text for `thesis_adapt` without manual PDF export. |
| **ASK** | Enable MCP? If yes: Overleaf email + password → `.env` only (never commit or echo in reports). |
| **YOU_DO** | Pick **one** stack setup below. |

**Dual-stack MCP setup (pick Cursor **or** Claude Code):**

| Stack | Setup |
|-------|--------|
| **Cursor** | `overleaf-mcp`, Playwright chromium, `scripts/overleaf_mcp.sh`, project `.cursor/mcp.json` — see workspace `docs/OVERLEAF_MCP_SETUP.md` or framework `docs/MCP_OVERLEAF_OPTIONAL.md`. |
| **Claude Code** | `npx overleaf-mcp` + credentials in `.env` — see `docs/MCP_OVERLEAF_OPTIONAL.md` (no `.cursor/mcp.json` required). |

First login: `overleaf_login`, `overleaf_list_projects`. Write `memory/overleaf_paper_project.md` (paper id) separately from thesis project notes.

**Agent:** Set `overleafPaper.projectId` and `overleafPaper.displayName` (= slug). Record `credentials: set in .env` in `intake_report.md` only.

---

### Block C — Workflow profile

| | |
|--|--|
| **WHY** | Not everyone needs refactor, public release, or full MIP porting. Choosing a profile avoids spending time on agents you will skip. |
| **ASK** | `paper_only` \| `paper_audit` \| `paper_audit_repro` \| `full_pipeline` |
| **YOU_DO** | Acknowledge how many approval gates apply — see [USER_APPROVAL_GATES.md](../docs/USER_APPROVAL_GATES.md) § Mandatory gates by `workflowProfile`. |

**Agent:** Set `workflowProfile` in `fttp.config.json`. Tell user the **mandatory `gate_id` list** for their profile (e.g. `paper_audit` adds G4-evidence).

---

### Block D — Writing mode

| | |
|--|--|
| **WHY** | `thesis_adapt` preserves your voice by condensing defended thesis prose; `compose` drafts more from scratch (higher risk of generic tone). `hybrid` mixes both with a provenance map. |
| **ASK** | `thesis_adapt` \| `compose` \| `hybrid` (default recommended: `thesis_adapt`). |
| **YOU_DO** | Confirm choice; SA8 will use `memory/provenance_map.md` when adapting. |

**Agent:** Set `writingMode` in config.

---

### Block E — Environment (`.env`)

| | |
|--|--|
| **WHY** | Reproducible runs need Gurobi paths, data roots, and API tokens without guessing from old notebooks. |
| **ASK** | Review proposed `.env.example` (from scaffold, `fttp env-suggest`, or scan of RO `requirements.txt` / notebook imports). |
| **YOU_DO** | Copy to `.env`, edit values, never commit secrets. |

**Agent:** Ensure `.env.example` exists in workspace; propose keys from RO scan when user has local thesis paths. Never commit `.env`.

---

### Block F — Chat language

| | |
|--|--|
| **WHY** | You may prefer Spanish explanations while the submission manuscript stays English. |
| **ASK** | `es` or `en` for agent chat in this workspace. |
| **YOU_DO** | Reply with preference; LaTeX under `paper/` remains English unless the venue requires otherwise. |

**Agent:** Record in `intake_report.md`; mirror user language in chat only.

---

### Block G — Venue stub (mandatory before SA1 HANDOFF)

| | |
|--|--|
| **WHY** | The target journal or conference defines document class, page limits, references, and figure rules. Without a venue stub, SA8 prose may not compile to an acceptable PDF. |
| **ASK** | Primary venue name + author guidelines URL; template access (`local_path`, zip into `paper/latex/`, download URL, or Overleaf template project id); optional backup venue. |
| **YOU_DO** | Copy **your** template files into `paper/latex/<vendor>/`; confirm the framework does **not** ship publisher `.cls` files. |

**Agent steps:**

1. Set `paper.activeVenue`, `paper.venueProfiles.primary` (id, displayName, authorGuidelinesUrl, templateSource, templatePath, mainTex).
2. If user provides template zip/path: copy into `paper/latex/` **writable only**; write `memory/venue_template_manifest.md` from template.
3. Stub or update `paper/JOURNAL_GUIDELINES.md` with venue URL + checklist pointer.
4. Set `templateDeferred: true` + date only if user explicitly defers (SA7/SA8 blocked until SA1 completes).

Deep policy extraction is **SA1** — see [VENUE_TEMPLATE_ONBOARDING.md](../docs/VENUE_TEMPLATE_ONBOARDING.md).

**Optional:** Pack `optimization-or` (yes/no) → `packs[]` in config — ask with WHY if user runs MIP/GIS thesis workflows ([PACKS.md](../docs/PACKS.md)).

---

## CONSUMER_ONBOARD — automated tasks (after blocks 0–G)

1. Write `memory/intake_report.md` from `intake_report_TEMPLATE.md` — all blocks answered; **no TBD** on slug, repoRoot, thesis paths, venue stub, profile, or writing mode.
2. Ensure `paper/` exists; minimal `main.tex` stub only if user OK and file missing (replace with venue `mainTex` when known).
3. Finalize `fttp.config.json` from example + user answers.
4. If Overleaf MCP enabled: verify login; ensure workspace has Overleaf setup doc if missing.
5. `cd PAPER_WS && npx from-thesis-to-paper doctor` (or `python -m fttp doctor`) — exit **0**.
6. Optional: `./scripts/run_tests.sh smoke` if workspace has tests.

---

## G0-intake — AUDIT and APPROVE (mandatory CONSUMER closure)

After blocks 0–G and automated tasks, **before HANDOFF to SA1**:

### AUDIT: G0-intake

Emit checklist (3–7 bullets). User reviews:

- `fttp.config.json` — `workspaceSlug`, `repoRoot`, `workflowProfile`, `writingMode`, `readOnlyRoots`, `overleafPaper`, `paper.venueProfiles.primary`
- `memory/intake_report.md` — all blocks; `user_ack` recorded
- `.env.example` present (no secrets in log)
- `memory/user_approval_log.md` initialized
- Venue stub: guidelines URL + template path or explicit `templateDeferred`
- Slug matches folder name and Overleaf **paper** display name (if used)
- No thesis/verification paths inside paper repo tree

### APPROVE_ASK

> You are the final authority: I propose paths and config, but you confirm they match your real thesis layout and journal target before we continue.

Request: `APPROVED: G0-intake` (EN) or `APROBADO: G0-intake` (ES), or corrections.

### On approval

Update `memory/user_approval_log.md` row for `G0-intake`: `user_status: approved` (or `approved_with_edits`), `approved_at` ISO-8601, `notes` summary.

### Without approval

```text
TAREA INCOMPLETA
BLOQUEADO: no lanzar SA1 — missing approved row for G0-intake
```

Details: [USER_APPROVAL_GATES.md](../docs/USER_APPROVAL_GATES.md).

---

## FRAMEWORK_SMOKE (maintainer only)

1. In `REPO_FTTP` or empty test dir: copy `templates/memory/*` if missing.
2. `fttp.config.json` from example with placeholder paths (`/path/to/...`), `packs: []`.
3. `intake_report.md` with section **Consumer onboarding — pending**; TBD on user answers.
4. Skip G0 approval; no HANDOFF to SA1–SA13.
5. `doctor` exit 0 (warn on missing `readOnlyRoots` acceptable).

---

## Forbidden

- Copying multi-GB verification folders into the framework or paper repo wholesale.
- Editing master notebooks or any path under `readOnlyRoots`.
- Committing `.env` or pasting Overleaf passwords into `intake_report.md`, approval log, or chat logs in reports.
- Hardcoding one user's cloud paths into the published framework repo.
- Inventing experiment counts or table values in intake notes.
- Listing blocks 0–G as bare questions **without** WHY paragraphs.
- Cursor-only MCP wording — always offer Claude Code path too.
- HANDOFF to SA1 without **approved** `G0-intake` row (CONSUMER only).
- Shipping publisher `.cls` / `.bst` in framework repo — BYO into `paper/latex/` only.

---

## Verify

- `test -f memory/intake_report.md`
- `test -f memory/user_approval_log.md` (CONSUMER)
- Config JSON valid; `workspaceSlug`, `repoRoot`, `paper.dir`, `paper.mainTex`, `workflowProfile`, `writingMode` set.
- **CONSUMER:** `thesis.source` set; RO paths and/or Overleaf thesis id if applicable; venue stub without TBD on primary target.
- **CONSUMER:** `doctor` exit 0; G0-intake row `approved` or `approved_with_edits`.
- **CONSUMER:** HANDOFF → SA1 only after G0 approved.
- **SMOKE:** no HANDOFF to SA1–SA13.

---

## Closure

- **SE TERMINÓ LA TAREA COMPLETA (SA0)** — CONSUMER: blocks 0–G complete; config + intake report + approval log; `doctor` OK; **G0-intake approved**.
- **HANDOFF:** CONSUMER → **SA1** (venue policy from stub); SMOKE → publish framework only.
- **TAREA INCOMPLETA** — BLOQUEADO: SA1–SA13 (CONSUMER mode) until G0-intake approved or intake incomplete.
