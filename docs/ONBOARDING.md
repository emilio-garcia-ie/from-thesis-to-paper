# End-user onboarding — install to first RUN

> **Stack-neutral:** use **Cursor** or **Claude Code** with the same workspace and skills.  
> **Language:** English docs; agent chat may be Spanish or English per your choice in SA0.

The framework does **not** collect thesis paths during its own build (P0–P11). **You** (or SA0 **CONSUMER_ONBOARD**) set up a dedicated **paper workspace** — see [WORKSPACE_MODEL.md](WORKSPACE_MODEL.md).

Before answering SA0 questions, read why each step exists: [ONBOARDING_RATIONALE.md](ONBOARDING_RATIONALE.md).  
You will **audit and approve** key artifacts: [USER_APPROVAL_GATES.md](USER_APPROVAL_GATES.md).

---

## Prerequisites

| Item | Notes |
|------|-------|
| Git | For framework clone and new paper repo |
| Python 3.10+ | `pip install -e` on `from-thesis-to-paper` |
| LaTeX (optional early) | Needed before SA9 compile |
| Overleaf account (optional) | Separate **thesis** (read-only) and **paper** (manuscript) projects |
| Agent IDE | Cursor **or** Claude Code — do not cross-load `AGENTS.md` / `CLAUDE.md` (see [sync_cursor_claude.md](sync_cursor_claude.md)) |

---

## Step 1 — Install the framework

```bash
git clone https://github.com/<your-org>/from-thesis-to-paper.git
cd from-thesis-to-paper
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

Optional npm wrapper (when published or linked):

```bash
cd packages/cli && npm install
```

**Verify (maintainer path):** `./scripts/run_tests.sh smoke` inside `REPO_FTTP`.

---

## Step 2 — Create the paper workspace

Choose **one** path:

| Method | Command / action |
|--------|------------------|
| **Scaffold (recommended when available)** | `python -m fttp scaffold --slug <workspaceSlug> --parent /path/to/parent` |
| **Manual** | Copy `templates/paper-workspace/` to a new folder named `<workspaceSlug>` |
| **SA0 agent** | Run prompt **SA0 `MODO: CONSUMER_ONBOARD`** — agent copies scaffold and asks blocks 0–G |

Rules for `<workspaceSlug>`:

- Same name as the **Git repo folder** and Overleaf **paper** project (recommended).
- Format: lowercase, hyphens/underscores — see [WORKSPACE_MODEL.md](WORKSPACE_MODEL.md) §2.

**Do not** use the framework repo as `repoRoot`. **Do not** point `repoRoot` at thesis-only trees.

---

## Step 3 — Onboard (SA0 CONSUMER_ONBOARD)

Use your agent stack entry file (`AGENTS.md` for Cursor, `CLAUDE.md` for Claude) and the SA0 prompt in [creacion-de-agentes.md](creacion-de-agentes.md) or [`.cursor/plans/from-thesis-to-paper_orchestration.plan.md`](../.cursor/plans/from-thesis-to-paper_orchestration.plan.md).

SA0 covers (with **WHY** before each **ASK** — [ONBOARDING_RATIONALE.md](ONBOARDING_RATIONALE.md)):

| Block | Topic |
|-------|--------|
| **0** | `workspaceSlug` |
| **A** | New writable `repoRoot` |
| **B** | Thesis read-only sources (`readOnlyRoots`, thesis Overleaf id) |
| **B2** | Overleaf **paper** project (same name as slug) + optional MCP |
| **C** | `workflowProfile` |
| **D** | `writingMode` |
| **E** | `.env` / `.env.example` |
| **F** | Chat language (`es` / `en`) |
| **G** | Venue stub + BYO template — [VENUE_TEMPLATE_ONBOARDING.md](VENUE_TEMPLATE_ONBOARDING.md) |

**Outputs:**

- `fttp.config.json` from [`templates/workspace.config.example.json`](../templates/workspace.config.example.json)
- `memory/intake_report.md` — no `TBD` on paper/thesis paths after onboarding
- `memory/user_approval_log.md` — empty log initialized; row for **G0-intake** after your approval

**Closure:** reply `APPROVED: G0-intake` (or `APROBADO: G0-intake`) so the agent can HANDOFF to **SA1**.

---

## Step 4 — Doctor (health check)

From the **paper workspace** root (`repoRoot`):

```bash
export FTTP_CONFIG=/path/to/paper-workspace/fttp.config.json   # if not default name
python -m fttp doctor
# or, when linked:
npx from-thesis-to-paper doctor
```

Expect exit code **0**. Warnings may include: missing `paper/latex/` when venue is set, `readOnlyRoots` inside `repoRoot`, or slug/folder mismatch (when strict mode is enabled).

---

## Step 5 — RUN (SA1 → SA13)

| Order | Agent | Gate (minimum) |
|-------|-------|----------------|
| SA1 | Venue policy | **G1-venue** |
| SA2 | Narrative interview | **G2-narrative** |
| SA2b | Glossary | **G2b-glossary** |
| SA3–SA4 | Evidence (if `paper_audit+`) | **G4-evidence** |
| SA7 | Strategy brief | **G7-strategy** |
| SA8 | IMRaD writer | **G8-prose** |
| SA9 | Figures/tables | **G9-figures** |
| SA6 | Repro (if `paper_audit_repro+`) | **G6-repro** |
| SA12 | Overleaf sync (optional) | **G12-overleaf** |
| SA13 | Submission | **G13-submit** |

Full gate matrix: [USER_APPROVAL_GATES.md](USER_APPROVAL_GATES.md).  
Executor rules (WHY-before-ASK, AUDIT, Mini-Guía): [EXECUTOR_GUIDE.md](EXECUTOR_GUIDE.md).

---

## Maintainer-only: FRAMEWORK_SMOKE

Inside `REPO_FTTP` only, use SA0 `MODO: FRAMEWORK_SMOKE` — placeholders, no consumer questions, no real thesis data. See [TESTING.md](TESTING.md).

---

## Config reference

Schema and new fields (`workflowProfile`, `writingMode`, `overleafPaper`, `copyPolicy`): [ARCHITECTURE.md](ARCHITECTURE.md) §4.

---

## Related docs

| Doc | Contents |
|-----|----------|
| [WORKSPACE_MODEL.md](WORKSPACE_MODEL.md) | Three-repo model, slug, copy manifest |
| [ONBOARDING_RATIONALE.md](ONBOARDING_RATIONALE.md) | WHY / ASK / YOU_DO per block |
| [USER_APPROVAL_GATES.md](USER_APPROVAL_GATES.md) | G0–G13 and profile matrix |
| [VENUE_TEMPLATE_ONBOARDING.md](VENUE_TEMPLATE_ONBOARDING.md) | SA0 stub vs SA1 policy |
| [WORKSPACE_EXAMPLE_PAPEREPN.md](WORKSPACE_EXAMPLE_PAPEREPN.md) | Legacy consumer example |
| [MCP_OVERLEAF_OPTIONAL.md](MCP_OVERLEAF_OPTIONAL.md) | Cursor vs Claude Overleaf MCP |
