#  ROADMAP 
## Phase  Targets + sources + logging (now)0 
- [ ] Pin CKM targets (PDG version) in `src/theta_star/constants.py`
- [ ] Pin PMNS targets (NuFIT version + ordering) in `src/theta_star/constants.py`
- [ ] Keep sources noted in `docs/DATA_SOURCES.md`
- [ ] Ensure run meta JSON writer exists (`src/theta_star/io/runlog.py`)

## Phase  Minimal working fit1 
- [ ] Define ansatz interface (`src/theta_star/ansatz/base.py`)
- [ ] Implement weighted   (`src/theta_star/fit/loss.py`)chi
- [ ] Make plots (`src/theta_star/plots/make_plots.py`)- [ ] Implement 
- [ ] First real run artifacts + PROGRESS_LOG entry

## Phase  Robustness + stability2 
- [ ] Optimization with restarts (`fit/optimize.py`)
- [ ] Anstze registry + comparisons
- [ ] Stability checks under:
  - weights / dropped observables / noise
  - different N ranges (if relevant)
  - different ansatz families

## Phase  Paper D3 
- [ ] Paper- [ ] Paper- [ ] Paper- [ ] es- [ ] Paper- [ ] Paper- [ ] Paperto run artifacts
