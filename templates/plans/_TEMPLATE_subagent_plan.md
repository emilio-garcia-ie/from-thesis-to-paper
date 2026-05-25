---
name: <Plan title>
overview: "<One sentence goal>"
todos:
  - id: step-1
    content: "<Subagent or phase description>"
    status: pending
isProject: false
---

# <Plan title>

> **Status:** DRAFT | APPROVED | CLOSED  
> **Rule:** `.cursor/rules/plan-and-subagent-orchestration.mdc` (or fttp equivalent)  
> **Execution:** user launches each subagent manually; ask for “prompt N” on demand.  
> **Full prompts:** deliver in chat via Guía de ejecución — do not embed all `text` blocks here by default.

## Goal

TBD — one paragraph.

## Non-goals

- TBD

## Prerequisites

- TBD — config, prior phases, signed brief if writing

## Recomendación: N subagentes

*(Agent writes one paragraph: why this N, merge/split rationale, topology symbols.)*

**Example:** 6 subagentes — SA0 async; (SA3 ∥ SA3b) after SA2b gate; SA8 sequential after SA7.

## Definition of Done

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | TBD | `command` or file check |

## Task checklist

- [ ] **step-1** — TBD

## Launch map (topology)

```text
1 → 2 → (3 ∥ 4) → 5
Optional async: 6 ~> after 2
```

| Subagente | Topology | Waits on | Can parallel with |
|-----------|----------|----------|-------------------|
| 1 | async | — | — |
| 3 | parallel | 2 | 4 |

## Subagent map

| Subagente | SA IDs | Todo IDs | Topology | Files touched |
|-----------|--------|----------|----------|---------------|
| 1 | SA0 | step-1 | async | `memory/` read-only |

---

## Guía de ejecución (fill when delivering prompts)

| Símbolo | Tipo | Acción |
|---------|------|--------|
| → | Secuencial | Tras cierre ✓ del anterior |
| ∥ | Paralelo | Mismo gate; 2+ chats |
| ~> | Async | Sin esperar otros |

**Mapa:** `1 → 2 → …`  
**Estado:** update when user reports each subagent closure.

### Subagente 1 — SA0 | TOPOLOGÍA: async

```text
PLAN: <title> | SUBAGENTE 1 de N | SA0 | TOPOLOGÍA: async
REPO: <absolute repoRoot>
PRECONDICIÓN: ninguna
ESPERA A: ninguno
…
---
CIERRE DE TAREA
SE TERMINÓ LA TAREA COMPLETA (Subagente 1 / SA0)
HANDOFF: Subagente 2
```

*(Add further subagent `text` blocks in chat or sidecar `*_prompts.md` when user requests.)*
