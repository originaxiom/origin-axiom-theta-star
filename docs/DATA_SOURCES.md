# Data sources (canonical)

This repository fits a small set of **target observables** for CKM and PMNS.
We keep sources explicit and pinned to prevent “silent drift”.

## Single-source rule (hard)
For each sector, there is exactly **one canonical source/version** at a time.
If the source/version changes, we must update:
1) `src/theta_star/constants.py` (numbers + metadata),
2) `docs/DATA_SOURCES.md` (this file),
3) `PROGRESS_LOG.md` (one dated entry explaining why).

No other file should contain target numbers.

---

## CKM (quark mixing)

**Canonical source**
- PDG “Review of Particle Physics” (RPP), year: **TBD**, entry: CKM / Wolfenstein.

**Canonical target set (Phase 0 minimal)**
We will use one of the following target parameterizations (choose one and stick to it):
- **Option A: Wolfenstein**: (λ, A, ρ̄, η̄)
- **Option B: minimal moduli + CP**: |V_us|, |V_cb|, |V_ub|, and one CP observable (δ or J or γ)

**Pinned in code**
- `src/theta_star/constants.py`:
  - `CKM_SOURCE = {...}`
  - `CKM_TARGETS = {...}`

---

## PMNS (lepton mixing)

**Canonical source**
- NuFIT global fit, version: **TBD**, date: **TBD**.

**Mass ordering**
We must maintain separate targets for:
- **NO** (normal ordering)
- **IO** (inverted ordering)

**Canonical target set (Phase 0 minimal)**
- sin²θ12
- sin²θ13
- sin²θ23
- δCP (degrees or radians, but be consistent)
- Δm²21
- Δm²3ℓ  (use NuFIT’s convention; keep sign consistent with ordering)

**Pinned in code**
- `src/theta_star/constants.py`:
  - `PMNS_SOURCE = {...}`
  - `PMNS_TARGETS = {"NO": {...}, "IO": {...}}`

---

## Policy: updating targets
Any change to targets must be a single commit that:
- updates `constants.py` (values + uncertainties + metadata),
- updates this file with the new pinned source/version,
- adds a dated note to `PROGRESS_LOG.md` describing:
  - what changed,
  - why,
  - what fit outputs might shift.