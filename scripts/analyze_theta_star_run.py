#!/usr/bin/env python3
"""
Analyze theta_star distribution for the "good" region of a sweep run.

Usage example:

    PYTHONPATH=src python3 scripts/analyze_theta_star_run.py \
      --run-id NO_theta_star_v1_N4000 \
      --chi2-max 50

or

    PYTHONPATH=src python3 scripts/analyze_theta_star_run.py \
      --run-id NO_theta_star_v1_N4000 \
      --delta-chi2 3.84
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


def load_results(run_id: str, base_dir: Path) -> pd.DataFrame:
    run_dir = base_dir / run_id
    csv_path = run_dir / "results.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Could not find results.csv at {csv_path}")
    return pd.read_csv(csv_path)


def select_theta_column(df: pd.DataFrame) -> Optional[str]:
    if "p_theta_star" in df.columns:
        return "p_theta_star"
    if "pmns_deltaCP" in df.columns:
        return "pmns_deltaCP"
    return None


def summarize_theta(theta: np.ndarray, label: str) -> None:
    if theta.size == 0:
        print(f"[{label}] no samples – nothing to summarize")
        return

    theta_sorted = np.sort(theta)
    q16, q50, q84 = np.percentile(theta_sorted, [16, 50, 84])

    print(f"[{label}] n_samples = {theta.size}")
    print(f"  theta_star min = {theta_sorted[0]:.4f} rad")
    print(f"  theta_star max = {theta_sorted[-1]:.4f} rad")
    print(f"  theta_star 16% = {q16:.4f} rad")
    print(f"  theta_star 50% (median) = {q50:.4f} rad")
    print(f"  theta_star 84% = {q84:.4f} rad")
    print(f"  approx 1σ band: [{q16:.4f}, {q84:.4f}] rad")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize theta_star in the good-chi2 region of a run"
    )
    parser.add_argument(
        "--run-id",
        required=True,
        help="Run ID (directory name under data/processed/runs)",
    )
    parser.add_argument(
        "--base-dir",
        default="data/processed/runs",
        help="Base directory for runs",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--chi2-max",
        type=float,
        default=None,
        help="Absolute chi2_total maximum for 'good' samples",
    )
    group.add_argument(
        "--delta-chi2",
        type=float,
        default=None,
        help=(
            "Select samples with chi2_total <= chi2_min + delta_chi2; "
            "use this for approximate confidence intervals."
        ),
    )
    args = parser.parse_args()

    base_dir = Path(args.base_dir)
    df = load_results(args.run_id, base_dir)

    if "chi2_total" not in df.columns:
        raise KeyError("results.csv must contain a 'chi2_total' column")

    theta_col = select_theta_column(df)
    if theta_col is None:
        raise KeyError(
            "Could not find 'p_theta_star' or 'pmns_deltaCP' in results.csv"
        )

    chi2 = df["chi2_total"].to_numpy()
    theta = df[theta_col].to_numpy()

    chi2_min = chi2.min()
    print(f"Run: {args.run_id}")
    print(f"Total samples: {len(df)}")
    print(f"chi2_min = {chi2_min:.4f}")

    # 1) Summary over all samples
    summarize_theta(theta, label="ALL")

    # 2) Good region by absolute chi2_max, if provided
    if args.chi2_max is not None:
        mask_abs = chi2 <= args.chi2_max
        summarize_theta(theta[mask_abs], label=f"chi2 <= {args.chi2_max:g}")

    # 3) Good region by delta-chi2, if provided
    if args.delta_chi2 is not None:
        threshold = chi2_min + args.delta_chi2
        mask_delta = chi2 <= threshold
        summarize_theta(theta[mask_delta], label=f"chi2 <= chi2_min + {args.delta_chi2:g}")


if __name__ == "__main__":
    main()