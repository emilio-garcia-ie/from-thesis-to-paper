# from-thesis-to-paper (fttp)

**from-thesis-to-paper** is an agent-oriented framework to turn a defended thesis and its run artifacts into a **journal-ready paper pipeline**: onboarding → evidence audit → strategy brief → IMRaD prose → figures/tables → (optional) Overleaf sync → submission bundle.

It is designed for **Cursor** and **Claude Code** users who want a repeatable process with explicit **user approval gates** before the pipeline advances.

---

## What it helps with

- **Onboarding a “paper workspace”** (a new writable repo for one submission) and keeping thesis sources **read-only**.
- **Running “doctor” checks** to catch path/config mistakes before writing or copying evidence.
- **Orchestrating an agent pipeline (SA0–SA13)** with explicit approval gates (G0–G13).
- **Optional packs** (e.g., `optimization-or`) for domain workflows (MIP/Gurobi, routing, GIS) when enabled in config.

## What it does NOT do

- **It does not contain your thesis, logs, or manuscript.** Those live in your own workspace and read-only roots.
- **It does not make read-only trees writable** (thesis Overleaf, notebooks, verification folders).
- **It does not ship publisher LaTeX templates** (`.cls`, `.bst`, etc.). You bring your venue template into your paper workspace (`paper/latex/`).
- **It does not promise an npm-published CLI.** This repo includes a Node wrapper CLI, but your usage may be local (`npm link`) unless you publish it yourself.

---

## Workspace model (three repositories)

You work across three logical roots. Only one is writable by agents.

```mermaid
flowchart TB
  subgraph fttp[REPO_FTTP: from-thesis-to-paper (framework)]
    PY[python/fttp (CLI + helpers)]
    SK[skills/core + skills/packs]
    TPL[templates/paper-workspace]
    PLAN[.cursor/plans (orchestration)]
  end

  subgraph ro[SOURCES_RO: thesis + run artifacts (read-only)]
    TH[Thesis text/tables (Overleaf or local)]
    NB[Master notebooks]
    LOG[Logs / verification trees / exports]
  end

  subgraph ws[PAPER_WS: your paper workspace (writable Git repo)]
    CFG[fttp.config.json]
    MEM[memory/]
    PAP[paper/]
    EXP[experimentos/]
    CODE[codigo/ (optional)]
  end

  fttp -->|SA0–SA13 agents + CLI| ws
  ro -->|read + bounded copy (manifested)| ws
```

More detail: [`docs/WORKSPACE_MODEL.md`](docs/WORKSPACE_MODEL.md).

---

## Agent pipeline (SA0–SA13) with approval gates

The framework uses explicit gates so **you** approve artifacts before the next agent runs.

```mermaid
flowchart LR
  SA0[SA0: Onboard] --> G0[G0-intake]
  G0 --> SA1[SA1: Venue policy] --> G1[G1-venue]
  G1 --> SA2[SA2: Narrative interview] --> G2[G2-narrative]
  G2 --> SA2b[SA2b: Glossary] --> G2b[G2b-glossary]
  G2b --> SA3[SA3: Evidence archaeologist]
  SA3 --> SA4[SA4: Evidence join auditor] --> G4[G4-evidence]
  G4 --> SA7[SA7: Strategy brief] --> G7[G7-strategy]
  G7 --> SA8[SA8: IMRaD writer] --> G8[G8-prose]
  G8 --> SA9[SA9: Figures/tables + LaTeX build] --> G9[G9-figures]
  G9 --> SA12[SA12: Overleaf sync (optional)] --> G12[G12-overleaf]
  G12 --> SA13[SA13: Submission bundle] --> G13[G13-submit]

  %% Optional lanes (profile-dependent)
  SA5[SA5: Refactor/port code (optional)] -.-> SA8
  SA6[SA6: Repro/public release (optional)] -.-> SA13
```

- **Gate rules**: [`docs/USER_APPROVAL_GATES.md`](docs/USER_APPROVAL_GATES.md)
- **Onboarding (install → SA0 → doctor → RUN)**: [`docs/ONBOARDING.md`](docs/ONBOARDING.md)
- **WHY-before-ASK rationale**: [`docs/ONBOARDING_RATIONALE.md`](docs/ONBOARDING_RATIONALE.md)

---

## Install and first run (recommended path)

### 1) Install the Python package (framework)

From `REPO_FTTP`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Verify the CLI exists:

```bash
fttp --version
python -m fttp --version
```

### 2) Create a paper workspace (new writable repo)

Scaffold a new workspace from the template:

```bash
python -m fttp scaffold --slug <workspaceSlug> --parent /path/to/parent
```

Then follow SA0 onboarding in your agent stack (Cursor or Claude Code), as described in:

- [`docs/ONBOARDING.md`](docs/ONBOARDING.md)

### 3) Run doctor (must be first)

From inside your **paper workspace root** (`PAPER_WS`):

```bash
fttp doctor
```

If your config is not named `fttp.config.json`, point to it explicitly:

```bash
FTTP_CONFIG=/abs/path/to/fttp.config.json fttp doctor
```

What `doctor` checks: Python importability, config discovery, `repoRoot`, `paper.mainTex`, and optional evidence paths.

---

## Optional: Node wrapper CLI (local usage)

This repo includes a Node CLI wrapper at `packages/cli/` that spawns `python -m fttp ...`.

Local install + link (so you can call `fttp` from anywhere):

```bash
cd packages/cli
npm install
npm link
```

Then in your **paper workspace**:

```bash
fttp doctor
fttp tables
fttp pipeline
```

If you prefer not to link, you can run it directly:

```bash
node /path/to/from-thesis-to-paper/packages/cli/src/cli.js doctor
```

Note: `npx from-thesis-to-paper doctor` will only work if **you** have the package available to `npx` (e.g., published or otherwise resolvable). This README does not assume it is published.

---

## Cursor + Claude Code: shared workspace + skill mirrors

Most artifacts are shared between stacks; only the entry files and IDE-specific mirrors differ.

```mermaid
flowchart TB
  subgraph shared[Shared (git-tracked)]
    MEM[memory/]
    DOC[docs/]
    SK[skills/core + skills/packs/]
    PLN[.cursor/plans/]
    SCR[scripts/ + tests/]
  end

  subgraph cursor[Cursor-only]
    AG[AGENTS.md]
    CR[.cursor/rules/]
    CSK[.cursor/skills/ (mirror)]
    MCP[.cursor/mcp.json (optional)]
  end

  subgraph claude[Claude Code-only]
    CL[CLAUDE.md]
    DSK[.claude/skills/ (mirror)]
    CSET[.claude/settings.local.json (optional)]
  end

  cursor --> shared
  claude --> shared
```

Sync checklist: [`docs/sync_cursor_claude.md`](docs/sync_cursor_claude.md).

---

## Testing

- Framework tests (run in `REPO_FTTP`): [`docs/TESTING.md`](docs/TESTING.md)

```bash
./scripts/run_tests.sh smoke
```

---

## Repository layout (high level)

| Path | Role |
|------|------|
| `python/fttp/` | Python package + `python -m fttp` CLI |
| `packages/cli/` | Node wrapper CLI (`fttp`) that spawns Python |
| `skills/` | Canonical skills (core + optional packs) |
| `templates/` | Paper workspace scaffolds + memory templates |
| `docs/` | Product documentation (canonical, English) |
| `examples/` | External workspace examples (no large RO trees) |

---

## PaperEPN reference workspace (external example)

This framework is used with an external workspace such as PaperEPN (`mi-investigacion-opt`). One relevant doc there:

- Local relative path (when repos are siblings): [`../mi-investigacion-opt/docs/creacion-de-agentes.md`](../mi-investigacion-opt/docs/creacion-de-agentes.md)

If that link does not resolve in your environment, open it at:

- `mi-investigacion-opt/docs/creacion-de-agentes.md`

---

## License

MIT — see [`LICENSE`](LICENSE).
