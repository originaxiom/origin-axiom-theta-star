# origin-axiom-theta-star

Act II: fitting a single phase angle \(\theta_\star\) to flavor data (PMNS + CKM) and exporting a prior for the main **Origin Axiom** toy-universe repo.

This repository does one focused job:

> Explore a family of phenomenological ansätze where a single angle \(\theta_\star\) organizes neutrino (PMNS) and quark (CKM) mixing, and turn those fits into a compact prior that other repos can consume.

The repo is deliberately small and technical. It is **not** a full flavor-physics analysis; it is an internal “Act II” workbench whose output is a \(\theta_\star\) prior used by `origin-axiom` when scanning scalar toy universes and microcavities.

---

## 1. What this repo contains

Conceptually there are three layers:

1. **Targets and loss**  
   - Define PMNS/CKM observables and their uncertainties.  
   - Provide a chi-square loss \(\chi^2\) that compares model predictions to those targets.

2. **Ansätze for \(\theta_\star\)**  
   - Small set of parametric models `ThetaStarAnsatz` implementing
     - a parameter space \(p\),
     - predictions for PMNS and (optionally) CKM observables given \(p\).

3. **Scans and post-processing**  
   - Randomly sample \(p\) in each ansatz, compute \(\chi^2\), and store the results.  
   - Analyze the resulting posterior for \(\theta_\star\).  
   - Export a compact prior (fiducial value + band) to be used downstream.

The typical workflow is:

1. Choose an ansatz (e.g. `theta_star_v2`).  
2. Run PMNS-only and joint PMNS+CKM scans.  
3. Analyze the distribution of \(\theta_\star\) under a chi-square cut.  
4. Combine several runs into a **global \(\theta_\star\) posterior**.  
5. Export the current preferred prior and record it in `PROGRESS_LOG.md`.

---

## 2. Repository layout

At a high level:

```text
src/
  theta_star/
    __init__.py
    constants.py        # targets (PMNS, CKM), units, ordering flags
    io/
      results.py        # load/save run results (CSV, JSON)
    fit/
      loss.py           # chi2 definitions (PMNS, CKM, total)
      sweep.py          # generic random-scan driver
    ansatz/
      base.py           # ThetaStarAnsatz base class
      example_minimal.py
      theta_star_delta_only.py
      theta_star_v1.py
      theta_star_v2.py  # current workhorse ansatz
    plots/
      inspect_run.py    # helper plotting functions

scripts/
  run_pmns_sweep.py         # PMNS-only scans
  run_ckm_sweep.py          # (currently unused) CKM-only scans
  run_joint_fit.py          # combined PMNS + CKM scans
  inspect_run.py            # quick scatter/hist plots for a run
  analyze_theta_star_run.py # 1D posterior summary for one run
  summarize_theta_star_posterior.py
                           # combine several runs into one posterior
  rollup_runs.py            # CSV rollup of best chi2 per run

data/
  processed/
    runs/
      <RUN_ID>/results.csv      # per-sample parameters & predictions
      <RUN_ID>/run_meta.json    # configuration & best-fit summary
    theta_star_posterior_summary.json
                               # global \(\theta_\star\) posterior

figures/
  NO_theta_star_*_*.png        # scan diagnostics
  theta_star_posterior_*.png   # posterior summaries

docs/
  THEORY_NOTES.md              # conceptual notes about \(\theta_\star\)
  ROADMAP.md                   # what has been done; what is next
  paper/
    ACTII_theta_star_section.tex
                               # LaTeX section for Act II paper

PROGRESS_LOG.md                # running log of scans and decisions
```

The exact run IDs will evolve, but the structure above is stable.

---

## 3. Targets and conventions

- PMNS targets and uncertainties are defined in `src/theta_star/constants.py` using NuFIT-like central values.
- CKM targets use Wolfenstein parameters (`lambda`, `A`, `rhobar`, `etabar`) with PDG-style errors.
- PMNS ordering can be `"NO"` (normal) or `"IO"` (inverted). All Act II scans currently use `"NO"`.

Each `Target` entry contains:

```python
Target(
    value=...,  # central value
    sigma=...,  # 1σ error (used as χ² weight scale)
    name="..."  # human-readable label
)
```

The chi-square definitions in `fit/loss.py` use these targets so that:

- `chi2_pmns` is a sum over {s12², s13², s23², dm21, dm3l, deltaCP}.
- `chi2_ckm` is a sum over {lambda, A, rhobar, etabar}.
- `chi2_total = chi2_pmns + chi2_ckm` for joint fits.

If you ever change target values, errors, or add/remove observables, **log it in `PROGRESS_LOG.md`** with a short justification.

---

## 4. Available ansätze for \(\theta_\star\)

All ansätze live in `src/theta_star/ansatz/` and inherit from `ThetaStarAnsatz`:

- **`example_minimal`**  
  Toy ansatz with almost trivial structure. Useful only as a smoke test.

- **`theta_star_delta_only`**  
  - \(\theta_\star \equiv \delta_{CP}\) for the PMNS phase.  
  - All mixing angles and mass splittings are held fixed at their central values.  
  - No CKM structure yet.  
  - Good for checking whether *just* identifying \(\theta_\star\) with \(\delta_{CP}\) is “consistent enough” with neutrino data.

- **`theta_star_v1`** (cosine-modulated PMNS, simple mass shift)  
  - Parameters: `theta_star`, `eps12`, `eps13`, `eps23`, `k_mass`, plus direct CKM parameters.  
  - PMNS angles are modulated with three cosines of \(\theta_\star\) with fixed phase offsets.  
  - `k_mass` controls a common fractional shift of `dm21` and `dm3l`.  
  - CKM observables are treated as direct parameters, not yet tied to \(\theta_\star\).

- **`theta_star_v2`** (current workhorse)  
  - More compact parameterization; improves PMNS fits and allows joint PMNS+CKM fits with \(\chi^2 \sim \mathcal{O}(1)`–`10\).  
  - Introduces a single PMNS angle modulation parameter (`eps_angle`) plus `k_mass` for splittings and Wolfenstein CKM parameters.  
  - Produces a robust \(\theta_\star\) posterior band when combining PMNS-only and joint scans.

The registry in `ansatz/__init__.py` exposes:

```python
from theta_star.ansatz import available_ansatze, get_ansatz

print(available_ansatze())
ansatz = get_ansatz("theta_star_v2")
```

---

## 5. Running scans

All examples below assume you are in the repo root and have `PYTHONPATH=src` set.

### 5.1 PMNS-only sweep

Sample \(p\) for a given ansatz and fit only PMNS data:

```bash
PYTHONPATH=src python3 scripts/run_pmns_sweep.py   --ansatz theta_star_v2   --ordering NO   --samples 2000   --seed 1
```

The script prints the best chi-square found and writes a run directory like:

```text
data/processed/runs/NO_theta_star_v2_N2000/
  results.csv
  run_meta.json
```

You can quickly visualize the run with:

```bash
PYTHONPATH=src python3 scripts/inspect_run.py   --run-id NO_theta_star_v2_N2000   --ordering NO
```

This produces scatter plots `PMNS vs χ²`, `θ★ vs χ²`, and histograms in `figures/`.

To summarize the \(\theta_\star\) posterior for that run under a chi-square cut:

```bash
PYTHONPATH=src python3 scripts/analyze_theta_star_run.py   --run-id NO_theta_star_v2_N2000   --chi2-max 50
```

which prints \(q_{16}, q_{50}, q_{84}\) for \(\theta_\star\) and reports how many samples survive the cut.

### 5.2 Joint PMNS + CKM fit

To run a joint scan that includes CKM data:

```bash
PYTHONPATH=src python3 scripts/run_joint_fit.py   --ansatz theta_star_v2   --ordering NO   --samples 4000   --seed 1
```

This produces a run such as `NO_theta_star_v2_N4000` with entries for both `chi2_pmns` and `chi2_ckm`. You can inspect and summarize it exactly as for the PMNS-only case.

### 5.3 Rollup of runs

To get a CSV overview of all existing runs (best \(\chi^2\), best-fit \(\theta_\star\), etc.):

```bash
PYTHONPATH=src python3 scripts/rollup_runs.py
```

This prints a table like:

```text
run_id,ansatz,N,seed,chi2_min,theta_star_best
NO_theta_star_delta_only_N2000,theta_star_delta_only,2000,3,4.4453,4.7627
NO_theta_star_v2_N2000,theta_star_v2,2000,2,0.2670,4.2057
NO_theta_star_v2_N4000,theta_star_v2,4000,1,7.3034,3.8288
...
```

---

## 6. Combining runs into a global \(\theta_\star\) posterior

Once you have several good-quality runs, you can combine them into a single posterior summary:

```bash
PYTHONPATH=src python3 scripts/summarize_theta_star_posterior.py   --run-id NO_theta_star_delta_only_N2000   --run-id NO_theta_star_v2_N2000   --run-id NO_theta_star_v2_N4000   --run-id NO_theta_star_v2_N8000   --chi2-max 50
```

The script prints per-run and global quantiles:

```text
[NO_theta_star_v2_N8000]
  n_total   = 8000
  n_used    = 3304
  chi2_min  = 0.1280
  theta★ (q16, q50, q84) = (2.0089, 3.4523, 5.6358)

GLOBAL theta★ summary (all runs combined):
  n_total_used = 5888
  theta★ (q16, q50, q84) = (2.0982, 3.5299, 5.5915)
```

and writes:

```text
data/processed/theta_star_posterior_summary.json
```

This JSON is the official summary for how \(\theta_\star\) behaves in all the flavor fits used so far.

Whenever you **change** which runs are considered “Act II official” or update the chi-square cut, record the decision in `PROGRESS_LOG.md`.

---

## 7. Exporting the \(\theta_\star\) prior to other repos

The main `origin-axiom` repo does not read raw scan results. Instead, we export a small prior:

```text
θ★_fid   ≈ 3.63 rad
θ★_band  ≈ [2.18, 5.54] rad
```

in a config file that `origin-axiom` can load. A typical export step (already wired once) is:

1. Run `summarize_theta_star_posterior.py` with the chosen runs and chi-square cut.
2. Hand-pick a fiducial value (e.g. the global median) and a band (e.g. [q16, q84] or a slightly expanded range).
3. Write these into a small JSON file in the main repo, e.g. `origin-axiom/config/theta_star_config.json`.
4. Log the exact numbers and provenance in `PROGRESS_LOG.md` here.

From that point on, `origin-axiom` treats the exported prior as the “Act II θ★ input” for twisted vacua and microcavity scans.

---

## 8. Reproducibility and logging

To keep this Act II work reproducible:

- **Environment** – pin your Python version and dependencies in `requirements.txt` or similar (to be added). For local development, a simple virtualenv is enough.
- **Random seeds** – every scan script takes `--seed`. Always record seed, sample count, ansatz name, ordering, and chi-square cuts in `PROGRESS_LOG.md`.
- **Runs and figures** – the `data/processed/runs/` and `figures/` directories are treated as *derived* data. They are not committed to git by default (see `.gitignore`).
- **Narrative** – use `docs/THEORY_NOTES.md` for higher-level conceptual notes and `docs/ROADMAP.md` for a forward-looking to-do list.

For a quick “what has been done so far?” overview, **read `PROGRESS_LOG.md` first**, then skim:

- `docs/ROADMAP.md` for planned ansatz changes or future combined fits.
- `docs/THEORY_NOTES.md` for the conceptual picture of \(\theta_\star\).
- `docs/paper/ACTII_theta_star_section.tex` for the current draft of the Act II paper section.

This repo is intentionally narrow in scope: it is *only* about pinning down \(\theta_\star\) from flavor and handing that information to the scalar toy-universe world. Everything else (Einstein limit, vacuum energy, microcavities, multi-field dynamics) happens in the main `origin-axiom` repo.