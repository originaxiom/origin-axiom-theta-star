# ROADMAP — origin-axiom-theta-star

**Goal of this repo:** derive and test candidate θ★‑based ansätze
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
  - `example_minimal` direct‑parameter ansatz (toy).
  - χ² loss functions for PMNS / CKM / joint fits.
  - Random sweep engine + run metadata + CSV writing.
- [x] Add run inspection helpers and basic plots.
- [x] Produce first green PMNS‑only sweeps and log them in
  `PROGRESS_LOG.md`.

**Purpose:** verify that the repo can generate runs, write artifacts and
be inspected, without making any θ★ physics claims.

---

## Phase B — First θ★‑aware ansätze (status: 🔄 active)

(See the detailed “Phase B (θ★-aware Ansätze and PMNS-only calibration)” section below for the current checkpoint status and θ★ window.)

**Objective:** introduce and compare phenomenological ansätze that
contain a true θ★ parameter and a small set of nuisance parameters, and
fit them to PMNS (and later CKM) data.

Planned / ongoing tasks:

1. **Ansatz spec (design doc)**  
   - Capture the θ★ → (PMNS, CKM) mapping in `docs/THEORY_NOTES.md`.
   - Treat that document as the contract between this repo and the
     upstream `origin-axiom` theory.

2. **Implementation: θ★ ansätze**  
   - `theta_star_delta_only`:
     - δ_CP ≡ θ★, all other PMNS observables treated as direct
       parameters (calibration ansatz).
   - `theta_star_v1`:
     - structured cosine modulation of PMNS angles and a common
       fractional shift of Δm² values, as specified in
       `docs/THEORY_NOTES.md`.
   - Register both in the ansatz registry and compare their χ²
     landscapes on the same datasets.

3. **Scans and baselines**  
   - Run PMNS‑only sweeps for each ansatz (NO and IO as needed).
   - Store artifacts under `data/processed/runs/θstar_phaseB_*`.
   - Add summary plots and a compact results note in `docs/`
     (e.g. `PhaseB_results.md`).

4. **Selection of θ★ candidates**  
   - Define a first‑pass criterion for “acceptable” θ★ values, based on:
     - χ² / dof thresholds,
     - stability across seeds / sampling variations,
     - consistency between ansätze (where applicable).

---

## Phase C — Robustness, systematics & Paper D (status: ⏳ planned)

1. **Robustness tests**
   - Vary target datasets (NuFIT variants, PDG updates).
   - Stress‑test ansätze under reasonable perturbations.
   - Add scripts to re‑run key scans automatically when targets change.

2. **Systematic effects**
   - Explore sensitivity to priors on nuisance parameters.
   - Investigate correlations between θ★ and mass‑splitting choices.

3. **Paper D (θ★ phenomenology)**
   - `paper/origin_axiom_D_theta_star_phenomenology.tex`:
     - Document ansatz definitions, fits, and robustness tests.
     - Include tables / figures generated directly from this repo.
   - Prepare a Zenodo snapshot and an arXiv‑ready bundle.

---

## Coordination with `origin-axiom`

- `origin-axiom` remains the home of:
  - cancellation system PDEs,
  - Einstein-limit checks,
  - vacuum energy tests and R/T/D scans.

- `origin-axiom-theta-star` consumes *constraints* and *intuition* from
  that repo but keeps its code and data pathways separate to avoid
  cross‑contamination.

When a θ★ candidate is selected here, it must be cross‑checked in
`origin-axiom` before being treated as “physically viable`.



### Phase B (θ★-aware Ansätze and PMNS-only calibration)

**Goal:** Introduce θ★ into simple, controllable Ansätze and use PMNS-only
data to identify a *numerically preferred* θ★ band, while stress-testing the
sweep / logging / plotting infrastructure.

Current Phase B status is:

1. **B.1 — Infrastructure + toy calibration (DONE)**  
   - Implemented a generic sweep driver (`scripts/run_pmns_sweep.py`) with
     logging to `data/processed/runs/<RUN_ID>/run_meta.json` and
     `results.csv`.  
   - Added inspection tooling (`scripts/inspect_run.py`) to produce χ²
     histograms, PMNS-vs-χ² scatter plots, and θ★ diagnostics where
     available.  
   - Verified the stack using the θ★-free `example_minimal` ansatz.

2. **B.2 — First θ★-aware Ansätze (DONE)**  
   - Calibration ansatz `theta_star_delta_only` with θ★ ≡ δ\_CP.  
   - Structured ansatz `theta_star_v1` where θ★ coherently modulates PMNS
     angles and a common mass shift.  
   - Performed multiple sweeps:
     - `NO_theta_star_delta_only_N2000` (seed 3, N = 2000).  
     - `NO_theta_star_v1_N4000` (seed 3, N = 4000).  
     - `NO_theta_star_v1_N2000` (seed 2, N = 2000).  
   - Added `scripts/analyze_theta_star_run.py` to quantify θ★ distributions
     in the good-χ² region, and `scripts/rollup_runs.py` to keep a compact
     summary of all runs.

3. **B.3 — Preliminary θ★ window from PMNS-only data (THIS CHECKPOINT)**  
   - All θ★-aware runs prefer a **mid-band** of θ★ values; none demand
     δ\_CP near 0 or 2π.  
   - Calibration ansatz (θ★ ≡ δ\_CP) yields a 16–84% θ★ band of
     roughly [3.2, 4.8] rad for χ² ≤ 20, with χ²\_min ≈ 4.45.  
   - Structured v1 ansatz gives good fits across a broader band
     [~2–5.6] rad, with χ²\_min ≈ 5.64 in the N = 4000 run.  
   - We therefore adopt, as a **working prior** for subsequent θ★ work:
     - conservative mid-band: θ★ ∈ [≈ 2.5, ≈ 5.5] rad,  
     - tighter core band: θ★ ∈ [≈ 3.2, ≈ 4.8] rad.

   This is explicitly *provisional* and will be revisited after
   CKM+PMNS fits and more physics-driven Ansätze.

### Phase B.4 – θ★ v2 baseline and first CKM+PMNS joint fits (status: ✅ in progress)

- **B.4.1 – Promote θ★ v2 to baseline ansatz (PMNS-only checks)**  
  - Two independent PMNS-only sweeps with v2 (N = 2000, seeds 1 and 2) both
    achieved χ²_min ≲ 1, with good-fit θ★ bands of roughly [2.0, 5.6] rad and
    medians around 3.2 rad.  
  - This established v2 as a robust parametrisation where a single θ★ controls
    the PMNS sector, with only two PMNS nuisance parameters (eps_angle, k_mass).

- **B.4.2 – First CKM+PMNS joint fit (θ★ v2, NO)**  
  - A joint sweep with v2 (N = 4000, seed 1) including both PMNS and CKM in
    the loss produced χ²_total ≈ 7.3 for 10 observables (6 PMNS + 4 CKM).  
  - The PMNS part is fitted almost perfectly (χ²_pmns ≈ 1), and the CKM part
    contributes a moderate χ²_ckm ≈ 6.3, consistent with a reasonable global
    fit.  
  - The joint θ★ distribution with a χ²_total ≤ 50 cut gives a 1σ band
    ≈ [2.3, 5.6] rad with median ≈ 3.6 rad, i.e. essentially the same window
    as the PMNS-only v2 sweeps.

- **B.4.3 – Outcome of Phase B.4 (current)**  
  - θ★ v2 is now the **baseline ansatz** for NO fits in this repo.  
  - A single θ★ band around 3–4.5 rad is favoured by both PMNS and CKM data
    within v2.  
  - The θ★ window is no longer purely “PMNS-derived”; it is now a **joint**
    CKM+PMNS result.

- **B.4.4 – Next steps (planned)**  
  - Run at least one additional joint v2 sweep (different seed and/or N) to
    check stability of the joint θ★ window.  
  - Start drafting the θ★ phenomenology section that connects this band to
    the cancellation system in the main `origin-axiom` repo.  
  - Optionally explore IO and/or refined θ★ ansätze once the NO baseline is fully locked.
