# How to find your Overleaf project ID

The **project id** is the long hexadecimal string in the Overleaf URL when you open the project in the browser.

## URL pattern

```text
https://www.overleaf.com/project/663a1b2c3d4e5f6789abcdef01
                              └──────────── 24 characters ────────────┘
```

Copy **only** the id segment (usually **24** lowercase hex characters). Do not include `/project/` or query parameters (`?`, `#`).

## Examples

| URL fragment | Project id |
|--------------|------------|
| `.../project/663a1b2c3d4e5f6789abcdef01` | `663a1b2c3d4e5f6789abcdef01` |
| `.../project/abc123def456789012345678` | `abc123def456789012345678` |

## Where to store it (fttp)

| Location | Purpose |
|----------|---------|
| `fttp.config.json` → `thesis.overleafProjectId` | Machine-readable config for agents |
| `memory/overleaf_thesis_project.md` | Human notes + table file paths after discovery |
| `.env` → `OVERLEAF_THESIS_PROJECT_ID` | Optional; MCP launcher may read it |

**Thesis vs paper:** use the **thesis** project id for read-only archaeology (SA0, SA3). A **separate** paper submission project id is configured later (SA12) — never use the thesis id for writing the journal manuscript on Overleaf.

## If you only have a project title

After MCP login, run `overleaf_list_projects` and match by title; then read the id from the tool output or open the project and copy from the browser URL.
