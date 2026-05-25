# Paper directory template (BYO document class)

Copy this folder layout into your **consumer** workspace under `paper/` (see `paper.dir` in `fttp.config.json`).

## Bring your own journal class

The framework does **not** ship publisher `.cls` trees (MDPI, IEEE, Elsevier, etc.). You choose:

1. **Document class** — place vendor files in `paper/` or a `paper/latex/` subfolder and `\documentclass{...}` in your `mainTex`.
2. **Venue profiles** — map multiple entry files in `fttp.config.json`:

```json
"paper": {
  "activeVenue": "primary",
  "venueProfiles": {
    "primary": { "mainTex": "main_journal.tex", "build": "scripts/paper/build_primary.sh" }
  }
}
```

3. **Compile** — `python -m fttp compile` runs `venueProfiles[activeVenue].build`, then `hooks.compile`, then checks for `mainTex.pdf`.

## Suggested layout

| Path | Role |
|------|------|
| `main.tex` | Default manuscript entry (`paper.mainTex`) |
| `tables/*.tex` | `\input{}` fragments |
| `figures/` | Graphics and TikZ |
| `REPRODUCIBILITY.md` | Tier B / discrepancy policy |
| `JOURNAL_GUIDELINES.md` | User-maintained venue checklist (SA1) |

## SA1 checklist (user workspace)

- Page limits, reference style, data/code policy → `memory/venue_policy.md`
- Do not hardcode a single publisher in framework `examples/` — use generic `user_defined_*` venue ids

## Related

- [`docs/PAPER_PRODUCTION_PIPELINE.md`](../../docs/PAPER_PRODUCTION_PIPELINE.md)
- [`skills/core/paper-figures-latex.md`](../../skills/core/paper-figures-latex.md)
