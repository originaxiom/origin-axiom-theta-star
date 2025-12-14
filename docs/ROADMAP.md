# ROADMAP — origin-axiom-theta-star

**Goal of this repo:** derive and test candidate θ★‐based ansätze
against flavour data (CKM + PMNS) in a way that is reproducible,
transparent, and clearly separated from the upstream cancellation
system physics in `origin-axiom`.

---

## Phase A — Infrastructure & smoke tests (status: ✅)

- [x] Define constants module with:
  - NuFIT 5.2 (with SK atm.) PMNS targets.
  - PDG 2024 CKM Wolfenstein parameters.
  - Angle helpers for δ_CP (periodic χ²).
- [x] Implement:
  - `ThetaStarAnsatz` base class.
  - `example_minimal` direct‐parameter ansatz (toy).
  - χ² loss functions for PMNS / CKM / joint fits.
  - Random sweep engine + run metadata + CSV writing.
- [x] Add run inspection helpers and basic plots.
- [x] Produce first green PMNS‐only sweep with toy ansatz and log it in
  `PROGRESS_LOG.md`.

**Purpose:** verify that the repo can generate runs, write artifacts and
be inspected, without making any θ★ physics claims.

---

## Phase B — First θ★‐aware ansatz (status: ⏳)

**Objective:** introduce a first phenomenological ansatz that contains a
true θ★ parameter and a small set of nuisance parameters, and fit it to
PMNS (and later CKM) data.

Planned tasks:

1. **Ansatz spec (design doc)**  
   - Write a short technical spec in `docs/THEORY_NOTES.md` describing:
     - how θ★ enters the PMNS sector (angles, δ_CP),
     - how it may be connected to CKM (directly or via shared structure),
     - what is considered “fixed structure” vs “fit parameter”.
   - This spec is the contract between this repo and the upstream
     `origin-axiom` theory.

2. **Implementation: `theta_star_X` ansatz**  
   - Implement a new ansatz class (name TBD, e.g. `PhiThetaAnsatz`) with:
     - one explicit θ★ parameter,
     - a minimal number of additional parameters,
     - deterministic mapping to PMNS / CKM observables.
   - Register it in the ansatz registry.

3. **Scans and baselines**  
   - Run PMNS-only, CKM-only and joint sweeps for the new ansatz.
   - Store artifacts under `data/processed/runs/θstar_phaseB_*`.
   - Add summary plots and a compact `PhaseB_results.md` in `docs/`.

4. **Selection of θ★ candidates**  
   - Define a first-pass criterion for “acceptable” θ★ values, based on:
     - χ² / dof thresholds,
     - stability across seeds / sampling variations.

---

## Phase C — Robustness, systematics & Paper D (status: ⏳)

1. **Robustness tests**
   - Vary target datasets (NuFIT variants, PDG updates).
   - Stress‐test ansatz under reasonable perturbations.
   - Add scripts to re-run key scans automatically when targets change.

2. **Systematic effects**
   - Explore sensitivity to priors on nuisance parameters.
   - Investigate correlations between θ★ and mass‐splitting choices.

3. **Paper D (θ★ phenomenology)**
   - `paper/origin_axiom_D_theta_star_phenomenology.tex`
     - Document ansatz definition, fits, and robustness tests.
     - Include tables / figures generated directly from this repo.
   - Prepare Zenodo snapshot and an arXiv‐ready bundle.

---

## Coordination with `origin-axiom`

- `origin-axiom` remains the home of:
  - cancellation system PDEs,
  - Einstein-limit checks,
  - vacuum energy tests and R/T/D scans.

- `origin-axiom-theta-star` consumes *constraints* and *intuition* from
  that repo but keeps its code and data pathways separate to avoid
  cross-contamination.

When a θ★ candidate is selected here, it must be cross-checked in
`origin-axiom` before being treated as “physically viable`.