---
name: comp-geometry-gis
description: GIS instance generation — coordinates, slopes, OSMnx-style networks, INST_GEN workflows
---

# Computational geometry and GIS instances

## Triggers

- INST_GEN, scenario folders (`10c_*`, `20c_*`), or coordinate/slope fields in instance JSON.
- User asks how instances were built from OSM / elevation / service polygons.
- Validating that paper instance descriptions match `inst_generation` read-only roots.

## Read order

1. `memory/workspace_intake.md` — path to `inst_generation` read-only root.
2. `memory/thesis_experiment_run_artifacts.md` — instance JSON glossary.
3. Pilot EDA folder (read-only) for spatio-temporal context if cited in thesis.
4. `comp-geometry-gis` only when pack enabled; do not copy GIS rasters into framework repo.

## Steps

1. **Bounding workflow:** document city/bbox, CRS, and snap tolerance used in generation scripts (cite script path, do not rerun blindly).
2. **Node placement:** customers from demand points; depot/chargers from thesis rules — match ids in `*__ins_*.json`.
3. **Slope / energy relevance:** note DEM source, percent slope caps, and how slope enters arc cost or energy constraints.
4. **OSMnx (or equivalent):** driving network type, simplification, speed assumptions — align with thesis Methods wording.
5. **Scenario naming:** map `scenario` prefix to client count and replicate id; link to catalog row ids.
6. **QA metrics:** report bbox area, graph diameter estimate, min/max customer distance to depot (writable summary only).
7. **Export contract:** instance JSON schema fields (`coords`, `demand`, `E_max`, time windows) — flag missing vs thesis table needs.
8. **Paper alignment:** Methods subsection cites reproducibility tier; no invented city names or instance counts.

## Forbidden

- Committing full shapefiles, rasters, or 57GB verification trees into fttp repo.
- Rewriting historical `inst_generation` scripts (read-only unless user explicitly ports to `codigo/`).
- Assuming Frutería pilot parameters apply to all scenarios without catalog row proof.
- Pasting WKT or coordinate dumps into chat (>20 lines).

## Verify

- Every scenario referenced in catalog has resolvable `instance_path_abs` or `TBD` with reason.
- CRS and units stated once in `memory/` or paper Methods stub.
- Spot-check: haversine or network distance for one customer pair matches order of magnitude in thesis.
- HANDOFF → `graph-theory-routing` for arc generation; → SA3 for catalog row coverage.
