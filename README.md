# origin-axiom-theta-star

**Scope:** this repo is dedicated *only* to the numerical extraction and
phenomenology of a candidate phase parameter **θ★** using experimental
flavour data (CKM + PMNS). It does **not** contain the cancellation
system PDEs or Einstein-limit scans; those live in:

- `originaxiom/origin-axiom`

This repo answers a single question:

> Given a θ★-based ansatz, can we reproduce the observed flavour
> structure of the Standard Model within experimental uncertainties?

Everything else (infrastructure, logging, plotting, paper D) exists to
support that question in a reproducible way.

---

## Repo structure (high level)

- `src/theta_star/`
  - `constants.py` — **single source of truth** for all numerical
    targets (NuFIT 5.2 PMNS, PDG 2024 CKM). No other file may hard-code
    these numbers.
  - `ansatz/`
    - `base.py` — interface for θ★ ansätze.
    - `example_minimal.py` — direct-parameter toy ansatz used only as a
      pipeline smoke test.
  - `fit/`
    - `loss.py` — χ² loss for CKM, PMNS and joint fits, with correct
      handling of periodic δ_CP.
    - `sweep.py` — random sweeps in parameter space + best-fit
      selection + artifact writing.
  - `io/`
    - `runlog.py` — run metadata (JSON) with git hash and timestamp.
    - `results.py` — helpers for writing sweep tables.
  - `plots/`
    - `inspect_run.py` — quick inspection tools (χ² histogram,
      PMNS vs χ² scatter).

- `scripts/`
  - `run_pmns_sweep.py` — PMNS-only sweep.
  - `run_ckm_sweep.py` — CKM-only sweep.
  - `run_joint_fit.py` — joint CKM+PMNS sweep.
  - `inspect_run.py` — inspect an existing run and save basic figures.

- `data/processed/runs/<run_id>/`
  - `results.csv` — one row per sample (parameters, predictions,
    χ² contributions).
  - `run_meta.json` — summary (best χ², best parameters, config).

- `data/processed/figures/`
  - Per-run plots (χ² histogram, PMNS vs χ², etc.).

- `docs/`
  - `DATA_SOURCES.md` — pinning of PDG / NuFIT versions (single source
    rule).
  - `ROADMAP.md` — project milestones (see below).
  - `THEORY_NOTES.md` — θ★ ansatz design notes and links to the
    upstream Origin Axiom documents.
  - `ARTIFACT_POLICY.md` — what must exist for a run to “count”.

- `PROGRESS_LOG.md` — human-readable changelog; every non-trivial run or
  change to targets must be logged here.

---

## Quickstart

Assuming Python ≥ 3.10 and a virtualenv with `numpy`, `pandas`,
`matplotlib`:

```bash
cd origin-axiom-theta-star

# PMNS-only sweep (NO), toy ansatz
PYTHONPATH=src python3 scripts/run_pmns_sweep.py --samples 1000 --seed 1

# Joint CKM+PMNS sweep
PYTHONPATH=src python3 scripts/run_joint_fit.py --samples 5000 --seed 1
```

This will create a new run directory under:

```text
data/processed/runs/<RUN_ID>/
```

To inspect a specific run:

```bash
PYTHONPATH=src python3 scripts/inspect_run.py --run-id <RUN_ID> --ordering NO
```

This writes:

- `data/processed/figures/<RUN_ID>_chi2_hist.png`
- `data/processed/figures/<RUN_ID>_pmns_vs_chi2.png`

---

## θ★ and ansatz philosophy

This repo is **agnostic** about the microscopic origin of θ★; that is
encoded in the separate `origin-axiom` repo and the “Master Files”
(Phase I–III). Here we only care about:

1. How θ★ (and possibly a few nuisance parameters) map to low-energy
   observables (CKM, PMNS, masses, phases),
2. Whether a given mapping is compatible with current data.

The design pattern:

- Define a `ThetaStarAnsatz` subclass in `src/theta_star/ansatz/`.
- Implement:
  - `param_names` and `param_bounds()`
  - `predict_pmns(params, ordering)`
  - `predict_ckm(params)`
- Register it in `theta_star.ansatz.__init__` so CLI scripts can use it.

We keep `example_minimal` as a deliberately trivial ansatz (parameters
= observables) to validate infrastructure. **No θ★ claims may be based
on this toy ansatz.**

---

## Roadmap (short)

See `docs/ROADMAP.md` for a detailed, dated roadmap. In one line:

> Phase A: infra + toy ansatz (DONE)  
> Phase B: first θ★-aware ansatz + scans  
> Phase C: robustness tests, systematics, and Paper D (phenomenology).
