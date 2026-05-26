---
name: venue-submission-policy
description: SA1 venue scout — BYO template, G1-venue gate, journal constraints; blocks SA7/SA8 without venue_policy.md
---

# Venue submission policy (SA1)

## Triggers

- After SA0 **CONSUMER_ONBOARD** with **G0-intake** approved and Block G venue stub (no TBD on primary target).
- Before paper strategy (**SA7**) or IMRaD writing (**SA8**) on greenfield projects.
- User names a target journal, conference, or “working paper only”.
- Prompt header includes SA1 or `venue-submission-policy`.

## Read order

1. `memory/intake_report.md` — Block G answers (venue id, guidelines URL, template access, `templateDeferred`).
2. `fttp.config.json` → `paper.activeVenue`, `paper.venueProfiles[activeVenue]` (`mainTex`, `templatePath`, `templateSource`, `templateDeferred`).
3. `memory/venue_template_manifest.md` — SA0 stub; SA1 completes file list and `\documentclass` verification.
4. [VENUE_TEMPLATE_ONBOARDING.md](../docs/VENUE_TEMPLATE_ONBOARDING.md) — BYO split SA0 vs SA1.
5. [USER_APPROVAL_GATES.md](../docs/USER_APPROVAL_GATES.md) — **G1-venue** AUDIT/APPROVE protocol.
6. `paper/JOURNAL_GUIDELINES.md` — expand checklist after policy extraction.
7. `memory/user_approval_log.md` — confirm **G0-intake** approved before starting; write **G1-venue** row after user OK.
8. `skills/core/paper-strategy.md` — cross-check only **after** `memory/venue_policy.md` exists (do not run SA7 before SA1 on greenfield).

## WHY (emit to user once at SA1 start)

> We now extract detailed rules from the author guide and verify that the document class matches the files **you** copied into the paper repo. That way later strategy, prose, and figures fit the journal shell — the framework does not ship publisher templates.

## Preconditions

| Gate / artifact | Required before SA1 work | Blocks |
|-----------------|--------------------------|--------|
| **G0-intake** | `user_approval_log.md` row `approved` | SA1 start |
| Block G stub | `venueProfiles.primary` + `venue_template_manifest.md` without TBD on primary venue | Incomplete SA1 |
| **G1-venue** | User approval after SA1 deliverables | **SA7**, **SA8** |

## Steps

### 1 — Inherit SA0 stub

- Read `memory/intake_report.md` venue section and `memory/venue_template_manifest.md`.
- If `templateDeferred: true`, record date and `provisional_class` in manifest; **SA8 remains blocked** until SA1 completes with final template (see [VENUE_TEMPLATE_ONBOARDING.md](../docs/VENUE_TEMPLATE_ONBOARDING.md)).

### 2 — BYO template install (user copies; agent verifies)

The framework **does not ship** publisher `.cls` / `.bst` under **REPO_FTTP**.

| `templateSource` | Agent / user action |
|------------------|---------------------|
| `local_path` | User confirms files copied to `templatePath` under **PAPER_WS** only |
| `zip_copy_into_paper_latex` | User unpacks; agent lists paths in manifest |
| `download_url` | User downloads per license; agent records URL in manifest (no credentials) |
| `overleaf_template_project_id` | Read-only copy into `paper/latex/` in paper repo — **not** thesis Overleaf |

**Agent:** Update manifest table (relative path, file type, optional SHA256); set `redistribution_ok_for_git` and `license_note` from user confirmation.

**Forbidden:** Adding `.cls` / `.bst` to `from-thesis-to-paper` framework repo; editing thesis Overleaf to install journal class.

### 3 — Extract venue policy

1. **Venue class:** journal / conference / thesis condensation / internal report.
2. **Constraints:** word/page limits, abstract structure, reference style, figure resolution, supplementary rules (official author guide URL required).
3. **Data & code policy:** repository requirement, ORCID, conflicts, preprint rules → feeds SA6 and SA8 disclaimers.
4. **Costs & timeline:** APC if applicable; target submission window → SA7 `evidence_path` hints only (no strategy decisions in SA1).

### 4 — Write `memory/venue_policy.md` (canonical artifact)

English only. Header must include: venue display name, `authorGuidelinesUrl`, date, link to `memory/venue_template_manifest.md`.

Sections (minimum):

- **Constraints** — page/word limits or “no limit found — ASK USER”
- **Required sections** — IMRaD / highlights / graphical abstract if any
- **Forbidden in this venue** — e.g. double-blind → no identifying paths in PDF
- **Citation style** — numeric / author-year + `.bst` name if known
- **Open data** — code/data availability bullets for SA6/SA8
- **Template** — `mainTex`, `templatePath`, `\documentclass` match status
- **Deferred** — if applicable, date and what SA8 still cannot do until resolved

### 5 — Template verification

- `\documentclass` in `mainTex` matches files under `templatePath` (manifest `matching .cls on disk`).
- Run `npx from-thesis-to-paper doctor` (or `python -m fttp doctor`) from **PAPER_WS**; clear venue/template warnings or document `pending` in manifest.
- Update `paper/JOURNAL_GUIDELINES.md` with limits checklist + pointer to `memory/venue_policy.md`.

### 6 — G1-venue AUDIT and APPROVE (mandatory)

Per [USER_APPROVAL_GATES.md](../docs/USER_APPROVAL_GATES.md):

1. **`AUDIT: G1-venue`** — checklist: `memory/venue_policy.md`, `paper/JOURNAL_GUIDELINES.md`, `paper/latex/**`, `memory/venue_template_manifest.md` (page limits plausible; `\documentclass` matches files; license OK to copy).
2. **`APPROVE_ASK:`** — user replies `APPROVED: G1-venue` or `APROBADO: G1-venue`.
3. Update `memory/user_approval_log.md` — `gate_id: G1-venue`, `user_status: approved`, ISO timestamp.

**Without G1-venue approved:**

```text
TAREA INCOMPLETA
BLOQUEADO: no lanzar SA7 ni SA8 — missing approved row for G1-venue
```

## Downstream blocks (SA7 / SA8)

| SA | Blocked without |
|----|-----------------|
| **SA7** | `memory/venue_policy.md` **or** G1-venue not approved |
| **SA8** | Same as SA7 **plus** signed `memory/paper_strategy_brief.md` (**G7-strategy**) |

Orchestration: SA8 **PRECONDICIÓN** = SA7 ✓ + **G7-strategy** approved + **G1-venue** approved + `venue_policy.md` present (and final template on disk unless user accepted bounded `templateDeferred` scope in audit).

## Mandatory questions (ASK user)

1. Primary journal + optional backup venue?
2. APC budget — yes / no / unknown?
3. Target submission date (quarter or month)?
4. Public data / code repository — comfort level (required / optional / decline)?
5. Confirm BYO template files are in `paper/latex/` (or explicit deferral with date)?

Use **WHY-before-ASK** for any follow-up (one paragraph WHY, then one question).

## Forbidden

- Assuming Elsevier/Springer/IEEE defaults without author guide URL or user confirmation.
- Editing `paper/main.tex` body in SA1 (policy + guidelines + manifest only).
- Shipping publisher `.cls` / `.bst` in **REPO_FTTP**.
- Promising replication the brief has not signed.
- **HANDOFF to SA7 or SA8** without `memory/venue_policy.md` and **G1-venue** approved.

## Verify

- [ ] `memory/venue_policy.md` exists; page/limit stated or “no limit found — ASK USER”.
- [ ] `memory/venue_template_manifest.md` updated (`SA1 completed`, `\documentclass` check).
- [ ] `paper/JOURNAL_GUIDELINES.md` references venue URL and policy file.
- [ ] `doctor` run noted in HANDOFF (exit 0 or documented warnings).
- [ ] **G1-venue** row in `memory/user_approval_log.md` = `approved` or `approved_with_edits`.
- [ ] HANDOFF → **SA2** (narrative interview) — not SA7 until narrative gates apply per `workflowProfile`.

## HANDOFF

- **SA2** — `narrative-interview` after G1-venue approved.
- Payload (≤5 lines): venue id, `mainTex`, template on disk yes/no, top 3 constraints, G1-venue approved_at.
