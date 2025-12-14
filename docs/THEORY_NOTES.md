# THEORY_NOTES — θ★ phenomenology design

This document is the bridge between the upstream **Origin Axiom**
(the cancellation system, Einstein-limit, R/T/D scans, etc.) and the
phenomenological θ★ fits implemented in this repo.

It is deliberately text‐only (no code): code lives in `src/theta_star/`,
this file specifies what the code *should* implement.

---

## 1. Scope of θ★ in this repo

- θ★ is treated as a **single phase‐like parameter** that may influence:
  - neutrino mixing (PMNS),
  - quark mixing (CKM),
  - and possibly mass hierarchies.

- This repo does **not** attempt to re-derive the cancellation system or
  cosmological consequences. Those belong to the `origin-axiom` repo and
  the Master Files (Phase I–III).

- Our job here is:

> to specify and test concrete mappings from (θ★, nuisance parameters)
> to low‐energy flavour observables, and confront them with data.

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

3. **Produce well‐defined predictions**
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

## 4. Open questions / to-do

- [ ] Decide the parameterisation of θ★ (angle range, normalisation).
- [ ] Decide whether PMNS and CKM share θ★ directly or via different
      “projections”.
- [ ] Fix the minimal set of nuisance parameters for the first
      θ★ ansatz (Phase B in `docs/ROADMAP.md`).
- [ ] Document the relation between θ★ and the cancellation system
      constraints derived in `origin-axiom` (even if only at a
      conceptual level for now).
