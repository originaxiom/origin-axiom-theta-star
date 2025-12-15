#!/usr/bin/env python3
"""
CKM-only sweep for a given ansatz.

Usage (from repo root):

    PYTHONPATH=src python3 scripts/run_ckm_sweep.py --samples 5000
"""

from __future__ import annotations

import argparse
from pathlib import Path

from theta_star.fit.sweep import SweepConfig, run_sweep
from theta_star.ansatz import available_ansatze


def main() -> None:
    parser = argparse.ArgumentParser(description="CKM-only theta* sweep")
    parser.add_argument("--ansatz", default="example_minimal", choices=available_ansatze())
    parser.add_argument("--samples", type=int, default=2000, help="Number of random samples")
    parser.add_argument("--seed", type=int, default=123, help="RNG seed")
    parser.add_argument("--run-id", default=None, help="Optional explicit run_id")
    args = parser.parse_args()

    cfg = SweepConfig(
        ansatz_name=args.ansatz,
        ordering="NO",  # PMNS ordering irrelevant when include_pmns=False
        n_samples=args.samples,
        seed=args.seed,
        include_pmns=False,
        include_ckm=True,
        base_dir=Path("data/processed/runs"),
    )

    _, summary = run_sweep(cfg, run_id=args.run_id)

    best = summary["best_loss"]
    print(f"[ckm-only] ansatz={cfg.ansatz_name} samples={cfg.n_samples} "
          f"best_chi2={best['chi2_ckm']:.3f}")


if __name__ == "__main__":
    main()