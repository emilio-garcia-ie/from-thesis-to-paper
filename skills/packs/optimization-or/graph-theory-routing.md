---
name: graph-theory-routing
description: Directed graphs, multigraph layers, and preprocessing for VRP/EVRP routing models
---

# Graph theory for routing

## Triggers

- Multigraph construction, arc filtering, or layer selection (Cap. 5 SSSMP).
- User asks about parallel arcs, dominance, or reducing |A| before MIP.
- Comparing thesis network figures with notebook adjacency construction.

## Read order

1. `memory/thesis_model_registry.md` — which model uses simple vs multigraph input.
2. Read-only multigrafo verification tree (structure only; no writes).
3. `graph-theory-routing` pack enabled in config; else stop and use core evidence archaeologist only.
4. Master notebook cells that build `G`, `A`, or layer lists (Thesis Code/, read-only).

## Steps

1. **Graph type:** identify directed graph `G=(V,A)` or multigraph with layer set `L` and arcs `(i,j,l)`.
2. **Node roles:** tag depot, customers, charging stations; ensure V indices match instance JSON ids.
3. **Feasibility preprocessing:** remove dominated arcs, impossible energy edges, or zero-demand loops — log counts removed.
4. **Multigraph merge policy:** document whether parallel arcs are kept for MIP or collapsed to min-cost representative.
5. **Metrics on graph:** report |V|, |A|, density, max out-degree — store in memory note for paper Methods.
6. **Consistency check:** every arc in MIP variable index set must exist in preprocessed arc list (bidirectional grep).
7. **Visualization:** export small GraphML/CSV to writable `experimentos/` only; do not commit huge edge lists.
8. **Handoff to MIP skill:** pass arc list path and layer map as structured dict/JSON for `mip-modeling-gurobi`.

## Forbidden

- Treating route JSON (`solucion_*.json`) as authoritative for **objective** value (structure only).
- Editing preprocessing outputs inside read-only OneDrive trees.
- Claiming multigraph is “complete multilayer” unless thesis definition requires it.
- Inventing arc costs not present in instance or DEM/slope pipeline.

## Verify

- Preprocessed |A| and |V| documented with before/after counts.
- Spot-check: random sample of 10 arcs has feasible endpoints in instance JSON.
- No orphan nodes reachable from depot under directed reachability (or document exceptions).
- HANDOFF → `mip-modeling-gurobi` when moving to formulation; → SA3 archaeology for table coverage.
