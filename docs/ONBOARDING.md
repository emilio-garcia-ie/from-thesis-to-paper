# End-user onboarding — install to first RUN

> **Stack-neutral:** use **Cursor**, **Claude Code**, or **Codex** with the generated workspace resources.
> **Language:** English docs; agent chat may be Spanish or English per your choice in SA0.

The framework does **not** collect thesis paths during its own build (P0–P11). **You** (or SA0 **CONSUMER_ONBOARD**) set up a dedicated **paper workspace** — see [WORKSPACE_MODEL.md](WORKSPACE_MODEL.md).

Before answering SA0 questions, read why each step exists: [ONBOARDING_RATIONALE.md](ONBOARDING_RATIONALE.md).  
You will **audit and approve** key artifacts: [USER_APPROVAL_GATES.md](USER_APPROVAL_GATES.md).

---

## Prerequisites

| Item | Notes |
|------|-------|
| Python 3.10+ | Must include `venv`; Python 3.11+ is recommended |
| Git | Optional; it is not needed for the release-bundle route |
| Node | Optional; it is not needed for the release-bundle route |
| LaTeX (optional early) | Needed before SA9 compile |
| Overleaf account (optional) | Separate **thesis** (read-only) and **paper** (manuscript) projects |
| Agent IDE | Cursor, Claude Code, or Codex; `fttp init` creates one matching integration |

---

## Step 1 — Download and install the framework

```bash
bash install.sh
```

Download and extract the matching GitHub Release first. FTTP requires Python
3.10+ with `venv`; the installer creates a private environment and never edits
your shell profile. It prints an absolute command if `~/.local/bin` is not on
your `PATH`. Node and Git are not needed for this path.

---

## Step 2 — Create the paper workspace

Choose **one** path:

| Method | Command / action |
|--------|------------------|
| **Guided init (recommended)** | `fttp init /path/to/<workspaceSlug> --agent codex` |
| **Scaffold** | `fttp scaffold --slug <workspaceSlug> --parent /path/to/parent` |
| **Existing workspace** | Use `fttp scaffold` only when you need the lower-level template command |

Rules for `<workspaceSlug>`:

- Same name as the **Git repo folder** and Overleaf **paper** project (recommended).
- Format: lowercase, hyphens/underscores — see [WORKSPACE_MODEL.md](WORKSPACE_MODEL.md) §2.

**Do not** use the framework repo as `repoRoot`. **Do not** point `repoRoot` at thesis-only trees.

---

## Step 3 — Onboard (SA0 CONSUMER_ONBOARD)

Open the generated workspace in the selected agent, read `GETTING_STARTED.md`,
and run `fttp start` for the ready-to-paste intake prompt. The workspace carries
its own selected-agent instructions, skills, and local guides.

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
fttp doctor
```

Expect exit code **0**. Warnings may include: missing `paper/latex/` when venue is set, `readOnlyRoots` inside `repoRoot`, or slug/folder mismatch (when strict mode is enabled).
Doctor is a configuration check. A fresh scaffold reports placeholder hooks as warnings; replace those hooks before expecting a successful pipeline. Use `fttp status` for the guided next action.

`fttp scaffold --force` adds missing files without overwriting existing workspace files. Commands that write generated output use create-only behavior and fail if the target already exists.

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
