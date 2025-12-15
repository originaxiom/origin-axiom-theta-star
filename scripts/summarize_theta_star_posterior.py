#!/usr/bin/env python3
"""
summarize_theta_star_posterior.py

Combine multiple theta★ runs into a single posterior summary.

Usage example:

    PYTHONPATH=src python3 scripts/summarize_theta_star_posterior.py \
        --run-id NO_theta_star_delta_only_N2000 \
        --run-id NO_theta_star_v2_N2000 \
        --run-id NO_theta_star_v2_N4000 \
        --chi2-max 50

This will:

  * For each run:
      - load data/processed/runs/<run_id>/results.csv,
      - apply a chi2_total <= chi2_max cut,
      - compute theta★ quantiles (16, 50, 84%),
      - print a per-run summary.
  * Then combine all filtered samples and print a global theta★ summary.
  * Finally, write a JSON file:

      data/processed/theta_star_posterior_summary.json

    with both per-run and global stats.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


RUNS_BASE = Path("data/processed/runs")
OUTPUT_JSON = Path("data/processed/theta_star_posterior_summary.json")


@dataclass
class RunSummary:
    run_id: str
    n_total: int
    n_used: int
    chi2_min: float
    chi2_max_cut: float
    theta_q16: float
    theta_q50: float
    theta_q84: float


@dataclass
class GlobalSummary:
    n_total_used: int
    chi2_max_cut: float
    theta_q16: float
    theta_q50: float
    theta_q84: float


def load_run_df(run_id: str) -> pd.DataFrame:
    csv_path = RUNS_BASE / run_id / "results.csv"
    if not csv_path.is_file():
        raise FileNotFoundError(f"Could not find results.csv for {run_id!r} at {csv_path}")

    df = pd.read_csv(csv_path)
    if "p_theta_star" not in df.columns:
        raise KeyError(f"Column 'p_theta_star' not found in {csv_path} (run_id={run_id!r})")
    if "chi2_total" not in df.columns:
        raise KeyError(f"Column 'chi2_total' not found in {csv_path} (run_id={run_id!r})")
    return df


def summarize_run(run_id: str, chi2_max: float) -> Tuple[RunSummary, np.ndarray]:
    df = load_run_df(run_id)
    n_total = len(df)
    chi2_min = float(df["chi2_total"].min())

    mask = df["chi2_total"] <= chi2_max
    df_used = df.loc[mask]

    if df_used.empty:
        raise RuntimeError(
            f"No samples with chi2_total <= {chi2_max} in run {run_id!r} "
            f"(chi2_min = {chi2_min:.3f})."
        )

    theta = df_used["p_theta_star"].to_numpy()
    q16, q50, q84 = np.quantile(theta, [0.16, 0.5, 0.84])

    summary = RunSummary(
        run_id=run_id,
        n_total=n_total,
        n_used=int(mask.sum()),
        chi2_min=chi2_min,
        chi2_max_cut=chi2_max,
        theta_q16=float(q16),
        theta_q50=float(q50),
        theta_q84=float(q84),
    )
    return summary, theta


def summarize_global(all_thetas: List[np.ndarray], chi2_max: float) -> GlobalSummary:
    if not all_thetas:
        raise RuntimeError("No theta★ samples collected for global summary.")

    theta_concat = np.concatenate(all_thetas)
    q16, q50, q84 = np.quantile(theta_concat, [0.16, 0.5, 0.84])

    return GlobalSummary(
        n_total_used=int(theta_concat.size),
        chi2_max_cut=chi2_max,
        theta_q16=float(q16),
        theta_q50=float(q50),
        theta_q84=float(q84),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize theta★ posterior across multiple runs.")
    parser.add_argument(
        "--run-id",
        action="append",
        dest="run_ids",
        required=True,
        help="Run ID to include (can be passed multiple times).",
    )
    parser.add_argument(
        "--chi2-max",
        type=float,
        default=50.0,
        help="Chi² cut: only samples with chi2_total <= chi2_max are used (default: 50).",
    )

    args = parser.parse_args()
    run_ids: List[str] = args.run_ids
    chi2_max: float = args.chi2_max

    print(f"Summarizing theta★ for runs: {', '.join(run_ids)}")
    print(f"Chi² cut: chi2_total <= {chi2_max:.3f}")
    print("-" * 72)

    per_run_summaries: List[RunSummary] = []
    all_thetas: List[np.ndarray] = []

    for run_id in run_ids:
        summary, theta = summarize_run(run_id, chi2_max=chi2_max)
        per_run_summaries.append(summary)
        all_thetas.append(theta)

        print(f"[{run_id}]")
        print(f"  n_total   = {summary.n_total}")
        print(f"  n_used    = {summary.n_used}")
        print(f"  chi2_min  = {summary.chi2_min:.4f}")
        print(
            f"  theta★ (q16, q50, q84) = "
            f"({summary.theta_q16:.4f}, {summary.theta_q50:.4f}, {summary.theta_q84:.4f})"
        )
        print("-" * 72)

    global_summary = summarize_global(all_thetas, chi2_max=chi2_max)
    print("GLOBAL theta★ summary (all runs combined):")
    print(f"  n_total_used = {global_summary.n_total_used}")
    print(
        f"  theta★ (q16, q50, q84) = "
        f"({global_summary.theta_q16:.4f}, {global_summary.theta_q50:.4f}, {global_summary.theta_q84:.4f})"
    )

    # Write JSON
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    out: Dict[str, object] = {
        "chi2_max": global_summary.chi2_max_cut,
        "per_run": [asdict(s) for s in per_run_summaries],
        "global": asdict(global_summary),
    }
    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)

    print()
    print(f"Wrote JSON summary to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()