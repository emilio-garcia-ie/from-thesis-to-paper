# Venue template manifest (template — SA0 stub / SA1 update)

> **Copy to:** `memory/venue_template_manifest.md` during SA0 Block G; SA1 completes file list and policy cross-check.  
> **Approval gates:** [docs/USER_APPROVAL_GATES.md](../../docs/USER_APPROVAL_GATES.md) — **G1-venue** reviews this file with `paper/latex/**`.  
> **Onboarding:** [docs/VENUE_TEMPLATE_ONBOARDING.md](../../docs/VENUE_TEMPLATE_ONBOARDING.md).

**Secrets:** Do not record download credentials or license keys in this file.

---

## Active venue profile

| Field | Value |
|-------|--------|
| **activeVenue key** | `TBD` — e.g. `primary` |
| **venue id** | `TBD` — slug in `fttp.config.json` → `paper.venueProfiles` |
| **displayName** | `TBD` — full journal or conference name |
| **authorGuidelinesUrl** | `TBD` |
| **mainTex** | `TBD` — e.g. `main.tex` or `main_journal.tex` |
| **templateSource** | `TBD` — `local_path` \| `zip_copy_into_paper_latex` \| `download_url` \| `overleaf_template_project_id` |
| **templatePath** | `TBD` — relative under repoRoot, e.g. `paper/latex/elsevier/` |
| **templateDeferred** | `TBD` — `true` \| `false` |
| **templateDeferred_until** | `TBD` — ISO date or `n/a` |
| **build script** | `TBD` — e.g. `scripts/paper/build_primary.sh` |

---

## Source provenance (BYO — user confirmed)

| Field | Value |
|-------|--------|
| **source_type** | `TBD` — local directory \| zip archive \| download URL \| Overleaf template project |
| **source_path_or_url** | `TBD` — absolute path, file path, or URL (no credentials) |
| **overleaf_template_project_id** | `TBD` — 24-char hex or `n/a` |
| **copy_date** | `TBD` — ISO 8601 |
| **copied_by** | `TBD` — user \| agent with user OK |
| **redistribution_ok_for_git** | `TBD` — `yes` \| `no` \| `unknown` — user confirms license |
| **license_note** | `TBD` — publisher terms summary; link to author guide |

---

## Files installed under `templatePath`

List every `.cls`, `.bst`, `.sty`, and required asset copied into the paper workspace.

| Relative path | File type | SHA256 (optional) | Notes |
|---------------|-----------|-------------------|-------|
| `TBD` | `TBD` | `TBD` | `TBD` |

**Empty until copy:** If `templateDeferred: true`, leave table empty and set **deferred_reason** below.

| Field | Value |
|-------|--------|
| **deferred_reason** | `TBD` — `none` or user-stated reason |
| **provisional_class** | `TBD` — e.g. `article` for preprint until final template |

---

## `\documentclass` verification (SA1)

| Field | Value |
|-------|--------|
| **declared in mainTex** | `TBD` — e.g. `elsarticle` |
| **matching .cls on disk** | `TBD` — `yes` \| `no` \| `not_checked` |
| **doctor warning cleared** | `TBD` — `yes` \| `n/a` \| `pending` |
| **SA1 completed** | `TBD` — `yes` \| `no` |
| **memory/venue_policy.md** | `TBD` — `linked` \| `pending` |

---

## Backup venue (optional)

| Field | Value |
|-------|--------|
| **alternate profile key** | `TBD` — `none` or e.g. `alternate` |
| **displayName** | `TBD` |
| **templatePath** | `TBD` |
| **notes** | `TBD` |

---

## Change log

| Date | Agent | Change |
|------|-------|--------|
| `TBD` | SA0 | Initial stub from intake Block G |
