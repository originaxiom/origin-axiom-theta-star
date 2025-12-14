# DATA_SOURCES

This document pins all external numerical inputs used in the
`origin-axiom-theta-star` repo. The rule is:

> Any change to a numerical target MUST update this document
> and be logged in `PROGRESS_LOG.md`.

---

## PMNS (neutrino mixing)

Source: **NuFIT 5.2 (with SK atmospheric data)**, public release 2023.  
We use the global-fit best-fit values and 1σ errors as reported in the
“NuFIT 5.2 (with SK atm.)” tables.

We store the following observables in `theta_star.constants`:

- `s12_2 = sin^2(theta12)`
- `s13_2 = sin^2(theta13)`
- `s23_2 = sin^2(theta23)`
- `dm21  = Δm^2_21 [eV^2]`
- `dm3l  = Δm^2_3ℓ [eV^2]` (sign encodes ordering)
- `deltaCP = δ_CP [rad]`

We support two orderings:

- `NO` — normal ordering
- `IO` — inverted ordering

The actual numbers are defined in `src/theta_star/constants.py` and
are copied directly from the NuFIT 5.2 tables (with SK atmospheric
data). Any update of NuFIT dataset or version must be recorded here
and logged in `PROGRESS_LOG.md`.

---

## CKM (quark mixing)

Source: **PDG 2024, CKM quark-mixing review**, global fit.

We work in terms of Wolfenstein parameters:

- `lambda`
- `A`
- `rhobar`
- `etabar`

with central values and 1σ errors taken from the PDG 2024 CKM review
summary table. The corresponding `Target` entries live in
`src/theta_star/constants.py` under `CKM_TARGETS`.

---

## Implementation rule

- No other file is allowed to hard-code CKM or PMNS target numbers.
- All code must import from `theta_star.constants` and use the
  `Target` objects defined there.
- When targets are changed:
  1. Update `src/theta_star/constants.py`,
  2. Update this page (section + version),
  3. Add a dated entry in `PROGRESS_LOG.md` explaining why.
