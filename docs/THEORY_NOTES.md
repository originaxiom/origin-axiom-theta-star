# THEORY_NOTES — θ★ phenomenology design

This document is the bridge between the upstream **Origin Axiom**
(the cancellation system, Einstein-limit, R/T/D scans, etc.) and the
phenomenological θ★ fits implemented in this repo.

It is deliberately text‑only (no code): code lives in `src/theta_star/`,
this file specifies what the code *should* implement.

---

## 1. Scope of θ★ in this repo

- θ★ is treated as a **single phase‑like parameter** that may influence:
  - neutrino mixing (PMNS),
  - quark mixing (CKM),
  - and possibly mass hierarchies.

- This repo does **not** attempt to re-derive the cancellation system or
  cosmological consequences. Those belong to the `origin-axiom` repo and
  the Master Files (Phase I–III).

- Our job here is:

> to specify and test concrete mappings from (θ★, nuisance parameters)
> to low‑energy flavour observables, and confront them with data.

---

## 2. Design requirements for θ★ ansätze

Any θ★ ansatz implemented in `src/theta_star/ansatz/` should:

1. **Expose θ★ explicitly**
   - θ★ appears as a parameter named `theta_star` (or similar).
   - Its domain is typically an angle, e.g. `[0, 2π)`.

2. **Minimise arbitrary freedom**
   - Additional parameters (“nuisances”) should be:
     - clearly motivated by structure (e.g. scaling, offsets),
     - kept as few as possible to avoid overfitting.

3. **Produce well‑defined predictions**
   - For a given parameter set, the ansatz must deterministically
     produce:
     - PMNS observables `{s12_2, s13_2, s23_2, dm21, dm3l, deltaCP}`,
     - CKM observables `{lambda, A, rhobar, etabar}` (or a documented
       subset).

4. **Be testable and replaceable**
   - Different ansätze can coexist (v1, v2, …).
   - Each must be selectable via CLI (`--ansatz` flag).
   - No ansatz is “privileged” until it survives the robustness tests
     defined in `docs/ROADMAP.md`.

---

## 3. Candidate structure (to be refined)

> This section is intentionally a placeholder for future math derived
> from the Master Files and the `origin-axiom` simulations.

Sketch (to refine later):

- Treat θ★ as the “master phase” controlling a small set of internal
  angles `{φ_i}`.
- Construct mixing angles and phases as combinations of `{φ_i}` plus
  fixed offsets and small tunable deformations.
- Example pattern (symbolic only, not yet committed):

  ```text
  s12^2  = f_12(theta_star; a_12, b_12, ...)
  s13^2  = f_13(theta_star; a_13, b_13, ...)
  s23^2  = f_23(theta_star; a_23, b_23, ...)
  deltaCP = g(theta_star; a_δ, ...)
  ```

- Equivalent structure on the CKM side, possibly sharing some of the
  internal phases or deformation parameters.

Once a concrete functional form is chosen (even if initially simple),
it must be written here first and only then implemented in a new ansatz
class (e.g. `PhiThetaAnsatz`) in code.

---

## 4. Ansatz v1 — θ★-locked PMNS modulation

The first structured θ★ ansatz implemented in code is
`ThetaStarV1Ansatz` (file: `src/theta_star/ansatz/theta_star_v1.py`).

### Parameters

- `theta_star` — master phase angle (in `[0, 2π)`).  
- `eps12`, `eps13`, `eps23` — dimensionless modulation amplitudes for
  the three PMNS mixing angles.  
- `k_mass` — common fractional shift for both mass‑squared splittings.  
- CKM parameters `{lambda, A, rhobar, etabar}` — currently treated as
  direct fit parameters, not linked to θ★ in v1.

### Mapping to observables

Let the NuFIT 5.2 central values be

- `s12_0 = sin^2(theta12)_0`,  
- `s13_0 = sin^2(theta13)_0`,  
- `s23_0 = sin^2(theta23)_0`,  
- `dm21_0 = Δm^2_21_0`,  
- `dm3l_0 = Δm^2_3ℓ_0`.

We define:

- **Dirac phase**:

  ```text
  deltaCP = theta_star
  ```

- **Mixing angles (cosine modulation with fixed offsets)**

  ```text
  phi12 = theta_star
  phi13 = theta_star + 2π/3
  phi23 = theta_star + 4π/3
  ```

  and

  ```text
  s12^2 = clip( s12_0 * (1 + eps12 * cos(phi12)), 0, 1 )
  s13^2 = clip( s13_0 * (1 + eps13 * cos(phi13)), 0, 1 )
  s23^2 = clip( s23_0 * (1 + eps23 * cos(phi23)), 0, 1 )
  ```

- **Mass‑squared splittings (common fractional shift)**

  ```text
  dm21 = dm21_0 * (1 + k_mass)
  dm3l = dm3l_0 * (1 + k_mass)
  ```

This ansatz enforces correlated θ★‑dependence across all three mixing
angles and both mass‑squared splittings while keeping the number of
nuisance parameters modest.

CKM observables remain structurally trivial in v1:

- `{lambda, A, rhobar, etabar}` are taken either from the parameter
  dictionary or, if absent, from the PDG 2024 targets.

### Status

- v1 is a phenomenological testbed to see whether such a simple
  θ★‑locked modulation can reproduce current PMNS data with acceptable
  χ².
- If it fails badly, the failure is informative for the design of more
  refined θ★ ansätze (e.g. different phase offsets, non‑universal
  modulations, or more nuanced mass‑sector treatment).


## 5. Preliminary θ★ window from PMNS-only sweeps

This section records the *current* numerical picture of θ★ from the Phase B
PMNS-only scans, so that later Ansätze (v2+) and the joint CKM+PMNS stage can
be compared against a well-defined baseline.

### 5.1 Ansätze used in the θ★ lab

We have so far used three ansätze in the `origin-axiom-theta-star` lab:

1. **`example_minimal` (no θ★)**  
   - Direct-parameter toy model, included only as a smoke test.  
   - Parameters: PMNS angles and mass splittings sampled directly in their
     physical ranges, with no θ★ dependence.  
   - Purpose: verify the sweep loop, χ² computation, logging, and plotting.

2. **`theta_star_delta_only` (calibration ansatz)**  
   - Identification θ★ ≡ δ\_CP with all other PMNS parameters free.  
   - Inputs:
     - θ★ drawn uniformly in [0, 2π), and used directly as δ\_CP.  
     - (s12², s13², s23², dm21, dm3l) sampled independently over broad
       but physically reasonable ranges.  
   - Purpose:
     - Provide a *minimal* θ★-aware ansatz that reproduces the known
       NuFIT δ\_CP band when fitted to PMNS data.  
     - Serve as a calibration for more structured θ★ ansätze.

3. **`theta_star_v1` (structured modulation ansatz)**  
   - θ★ controls correlated modulations of the PMNS angles and a coherent
     shift of the mass splittings.  
   - Working v1 implementation:
     - Start from a fixed “central” point (roughly the current NuFIT best
       fit for NO).  
     - Add cosine-modulated corrections of the form
       Δx ∝ ε\_x cos(θ★ + ϕ\_x) for each angle, with small amplitudes
       ε\_x sampled in a narrow interval.  
     - Add a common fractional shift k\_mass to the mass splittings.  
   - Purpose:
     - Test whether a *single* coherent phase θ★ can steer the PMNS sector
       into the observed region with only modest nuisance parameters.  
     - Check for any obvious “forbidden” θ★ values once correlations are
       turned on.

### 5.2 Summary of runs and best-fit θ★

The following runs are treated as the current Phase B reference set:

- **Baseline (no θ★)**  
  - `NO_example_minimal_N1000` (PMNS-only, NO ordering)  
    - χ²\_min ≈ 5.85 for n\_pmns = 6 (χ²/dof ≈ 0.98).  
    - No θ★ parameter; used only to validate the sweep infrastructure.

- **Calibration ansatz (θ★ ≡ δ\_CP)**  
  - `NO_theta_star_delta_only_N2000` (seed = 3, N = 2000)  
    - χ²\_min ≈ 4.45 for n\_pmns = 6.  
    - Best-fit θ★\_best ≈ 4.76 rad (≈ 273°).  
    - Using `analyze_theta_star_run.py` with `chi2_max = 20` gives:
      - 16–84% band for θ★ of roughly [3.18, 4.78] rad.  
      - Interpretation: good fits live in a **mid-band** of θ★, consistent
        with the NuFIT δ\_CP region, and do not accumulate near 0 or 2π.

- **Structured ansatz v1 (cosine-modulated)**  
  - `NO_theta_star_v1_N4000` (seed = 3, N = 4000)  
    - χ²\_min ≈ 5.64 for n\_pmns = 6.  
    - Best-fit θ★\_best ≈ 3.36 rad (≈ 192°).  
    - For samples with χ² ≤ 50, the empirical 16–84% band is roughly
      [2.55, 5.55] rad, with a median near 4.4 rad.  
  - `NO_theta_star_v1_N2000` (seed = 2, N = 2000)  
    - χ²\_min ≈ 14.3 for n\_pmns = 6 (worse fit, as expected from smaller
      N and a different random cloud).  
    - Best-fit θ★\_best ≈ 2.72 rad (≈ 156°).  
    - For χ² ≤ 50, the 16–84% band is roughly [1.94, 5.58] rad, with median
      near 3.2 rad.

All three θ★-aware runs therefore place their θ★\_best values in the **same
broad mid-band** of the circle:

> θ★\_best ∈ [2.7, 4.8] rad (≈ 155°–275°).

The calibration ansatz (θ★ ≡ δ\_CP) gives a somewhat tighter preference
around θ★ ≈ 4–5 rad, while v1 admits a broader band because its extra
nuisance parameters can partially compensate for different θ★ values.

### 5.3 Working θ★ window (to be refined)

For the purposes of ongoing work in this repo, we adopt the following
*provisional* θ★ window based purely on PMNS-only data and the simple
Ansätze above:

- **Conservative mid-band:**  
  - θ★ ∈ [≈ 2.5, ≈ 5.5] rad (≈ 145°–315°).  
  - This covers essentially all θ★ values supported by the good-fit regions
    of both the δCP-only and v1 sweeps.

- **Tighter “core” band suggested by calibration ansatz:**  
  - θ★ ∈ [≈ 3.2, ≈ 4.8] rad (≈ 185°–275°).  
  - This is the 16–84% interval of θ★ among δCP-only samples with
    χ² ≤ 20, and overlaps well with the best-fit region of v1.

We emphasize that this is **not yet a final θ★ determination**, but rather:

1. A **data-driven prior** for subsequent θ★-based Ansätze, especially
   more physics-motivated v2/v3 constructions.  
2. A **consistency check**: any future θ★ proposals that lie completely
   outside the conservative mid-band would require either
   - substantial new structure in the model, or  
   - additional data/constraints beyond the PMNS sector to be viable.

Future steps that will refine this window include:

- Joint CKM+PMNS fits that tie θ★ simultaneously to quark and lepton
  sectors.  
- More constrained Ansätze where θ★ controls fewer but more rigid
  deformations of the mixing matrices and mass spectra.  
- Cross-checks against the upstream cancellation-system simulations and
  Einstein-limit constraints documented in the main `origin-axiom` repo.

### 5.4. θ★ window with CKM+PMNS joint fits (θ★ v2, NO)

In the previous subsection we extracted a preliminary θ★ window using
PMNS-only sweeps with the θ★ v2 ansatz. Two independent runs
(N = 2000, seeds 1 and 2) gave:

- v2 PMNS-only, seed 1: 1σ(χ² ≤ 50) ≈ [2.01, 5.66] rad, median ≈ 3.20 rad.
- v2 PMNS-only, seed 2: 1σ(χ² ≤ 50) ≈ [1.93, 5.60] rad, median ≈ 3.22 rad.

We then promoted v2 to the baseline θ★ ansatz and performed the first
joint CKM+PMNS fit (NO ordering, N = 4000, seed 1), with both sectors
active in the loss function. The best-fit χ² split was

- χ²_pmns ≈ 1.0 (6 PMNS observables),
- χ²_ckm ≈ 6.3 (4 CKM observables),
- χ²_total ≈ 7.3 for 10 observables,

so the ansatz is capable of describing both sectors simultaneously
without obvious tension.

The θ★ distribution for the joint run, using a χ²_total ≤ 50 cut, gave

- 1σ(χ² ≤ 50) ≈ [2.33, 5.61] rad, median ≈ 3.64 rad,

which is essentially the same band as the PMNS-only v2 window, with a
slight upward shift of the median. In particular,

- the lower edge moves from ≈ 2.0 rad to ≈ 2.3 rad, and
- the upper edge remains around ≈ 5.6 rad.

The key point is that **including CKM does not push θ★ out of the
PMNS-preferred interval**. A single θ★ band, roughly

> θ★ ∈ [2.3, 5.6] rad, with a core around 3–4.5 rad,

is now supported by both neutrino and quark mixing data within the v2
ansatz. This joint window will be the starting point for any further
θ★ phenomenology (e.g. mapping back to the cancellation system, testing
IO, or exploring refined ansätze).

---

## 6. Open questions / to‑do

- [ ] Decide the parameterisation of θ★ (angle range, normalisation).
- [ ] Decide whether PMNS and CKM share θ★ directly or via different
      “projections”.
- [ ] Fix the minimal set of nuisance parameters for the first
      θ★ ansatz (Phase B in `docs/ROADMAP.md`).
- [ ] Document the relation between θ★ and the cancellation system
      constraints derived in `origin-axiom` (even if only at a
      conceptual level for now).

---