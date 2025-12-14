# origin-axiom-theta-star

(CKM and PMNS). This repo is intentionally separate from `origin-axiom` (Act II sanity layer).Phenomenology module for extracting/validating a candidate **

## What this repo does
- Defines **targets** (CKM/PMNS observables + uncertainties) from canonical sources.
- Fits via **weighted ***, runs **sweeps/optimizations**, logs every run with full metadata.chi- Implements **ansatz models** that map 
- Generates plots + tables for **Paper D** (
## Reproducibility rules (non-negotiable)
A runonly if it produces: realis 
1) `data/processed/runs/<run_id>/results.csv`
2) `data/processed/runs/<run_id>/run_meta.json`
3) `figures/runs/<run_id>/*.png`
4) an entry in `PROGRESS_LOG.md`
5) a git commit

Run folders are immutable. Never overwrite a run; use a new `run_id`.

## Layout
- `src/theta_star/constants. target observables + uncertainties + ci- `src/theta_star/constar/io/runlog. standard run meta writerpy` py` 
- `src/theta_star/ loss, sweep, optimizefit/` 
- `src/theta_star/ model familiesansatz/` 
- `docs/DATA_SOURCES. canonical sources + what we extractedmd` 
- `paper/or- `paper/or- `paper/oar- `paper/or- `paper/or- `paper/oar- `paper/or- `paper/or- `paper/oar- `paper/or- `pckm_sweep.py`
- `scripts/run_pmns_sweep.py`
- `scripts/run_joint_fit.py`
