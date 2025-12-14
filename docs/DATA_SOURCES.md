# Data sources (canonical)

This repo uses a small set of "target" observables for CKM and PMNS fits.
We keep the sources explicit to avoid silent drift.

## CKM (quark mixing)
Canonical source: PDG (Particle Data Group), CKM matrix elements / Wolfenstein parameters.
- Exact year/version will be pinned when we fill `src/theta_star/constants.py`.- We will use a minimal set such as |Vus|, |Vcb|, |Vub|, and a CP observable (

## PMNS (lepton mixing)
Canonical source: NuFIT global fit.
- Exact NuFIT version (and mass ordering) will be pinned in `src/theta_star/constants.py`.- We will use sin

## Policy
- Targets live only in `src/theta_star/constants.py`.
- If targets change, it must be a commit that also updates this file with:
  - version/date
  - ordering (NO/IO)
  - and a brief note in `PROGRESS_LOG.md`.
