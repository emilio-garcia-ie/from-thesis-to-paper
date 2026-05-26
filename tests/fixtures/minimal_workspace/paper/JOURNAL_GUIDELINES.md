# Journal guidelines — venue stub

> **Status:** Template stub. SA0 records the target venue; SA1 (`venue-submission-policy`) fills limits, policies, and compile checks.  
> **Authority for claims:** `memory/paper_strategy_brief.md` and `memory/venue_policy.md` (created in SA1).

## Primary venue (SA0 stub)

| Field | Value |
|-------|--------|
| **Venue id** | `user_defined_journal` (from `fttp.config.json`) |
| **Display name** | TBD |
| **Author guidelines URL** | TBD — set in `fttp.config.json` → `paper.venueProfiles.primary.authorGuidelinesUrl` |
| **Active manuscript** | `paper/main.tex` (may change to `main_journal.tex` after SA1) |
| **LaTeX template** | BYO under `paper/latex/` — see [VENUE_TEMPLATE_ONBOARDING.md](../../docs/VENUE_TEMPLATE_ONBOARDING.md) |

## Checklist (complete in SA1)

- [ ] Page limit and section structure
- [ ] Reference style (numeric vs author-year)
- [ ] Figure/table resolution and file formats
- [ ] Data availability and code availability statements
- [ ] APC / open-access policy (if applicable)
- [ ] Anonymization rules (double-blind vs single-blind)
- [ ] Compile command verified: `python -m fttp compile` or `hooks.compile`

## Framework note

The **from-thesis-to-paper** repository does **not** ship publisher `.cls` or `.bst` files. Copy your journal template into `paper/latex/<vendor>/` and record provenance in `memory/venue_template_manifest.md`.
