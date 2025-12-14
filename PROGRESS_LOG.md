# Progress  origin-axiom-theta-starLog 

Rule: every significant run or dataset change gets a dated entry with:
- command line
- run_id
- outputs (CSV + meta + plots)
- key numbers (best 
---

## 2025-12- Repo initialized (skeleton)14 
- Next: Phase 0 targets + sources + run meta logging discipline.- Created repo structure for t




## 2025-12-14 — First theta-star sweep pipeline green run

- Repo: `origin-axiom-theta-star`
- Context: infrastructure validation, not a physics result.
- Command:

  ```bash
  PYTHONPATH=src python3 scripts/run_pmns_sweep.py --samples 1000 --seed 1
  ```

- Ansatz: `example_minimal` (direct-parameter toy ansatz)
- Ordering: NO
- Outputs:
  - `data/processed/runs/NO_example_minimal_N1000/run_meta.json`
  - `data/processed/runs/NO_example_minimal_N1000/results.csv`
- Best fit summary:
  - `chi2_pmns ≈ 5.854` with `n_pmns = 6` (χ²/dof ~ 0.98)
  - Parameters close to NuFIT 5.2 (with SK atm.) targets.
- Interpretation:
  - Confirms sweep + loss + logging stack is functioning.
  - This run is NOT used to define θ★; it is only a pipeline smoke test.
