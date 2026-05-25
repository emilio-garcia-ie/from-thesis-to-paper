# PaperEPN writing extension (reference only)

This file is **not** part of `skills/core/`. It documents how a consumer workspace (e.g. PaperEPN) extends the generic SA8 writer.

| Topic | Location |
|-------|----------|
| Generic IMRaD writer (SA8) | [`skills/core/scientific-writing.md`](../../../skills/core/scientific-writing.md) in **from-thesis-to-paper** |
| PaperEPN P4 voice, thesis_mirror, citation gates | Consumer repo: `.cursor/skills/scientific-writing-paper/SKILL.md` (or local mirror) |
| Signed narrative | Consumer `memory/paper_strategy_brief.md` |
| IMRaD body fragment | Consumer `paper/content/imrad_body.tex` (not shipped in fttp) |

**Do not** copy long P4 prompts or thesis table data into the framework repository. Configure `fttp.config.json` hooks to run consumer `scripts/paper/*` instead.
