#!/usr/bin/env python3
"""
Inspect a theta-star sweep run.

Given a run_id, this script:
- prints basic chi2 statistics, and
- writes a small set of diagnostic plots to data/processed/figures/:

  * <RUN_ID>_chi2_hist.png
      - histogram of chi2_total

  * <RUN_ID>_pmns_vs_chi2.png
      - scatter of PMNS observables vs chi2_total

  * <RUN_ID>_theta_star_hist.png          (if theta_star present)
  * <RUN_ID>_theta_star_vs_chi2.png       (if theta_star present)
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def _load_run(run_id: str, base_dir: Path) -> pd.DataFrame:
    run_dir = base_dir / run_id
    csv_path = run_dir / "results.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Could not find results.csv at {csv_path}")
    return pd.read_csv(csv_path)


def _summary_stats(chi2: np.ndarray) -> str:
    return (
        f"chi2_total: min={chi2.min():.3f}, "
        f"mean={chi2.mean():.3f}, "
        f"median={np.median(chi2):.3f}"
    )


def _plot_chi2_hist(chi2: np.ndarray, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.hist(chi2, bins=40)
    plt.xlabel(r"$\chi^2_{\rm total}$")
    plt.ylabel("count")
    plt.title("Chi2 distribution")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def _plot_pmns_vs_chi2(df: pd.DataFrame, chi2: np.ndarray, out_path: Path) -> None:
    # Any columns of the form pmns_* except pmns_deltaCP
    pmns_cols: List[str] = [
        c for c in df.columns
        if c.startswith("pmns_") and c not in ("pmns_deltaCP",)
    ]
    if not pmns_cols:
        return

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 6))

    for col in pmns_cols:
        y = df[col].to_numpy()
        label = col.replace("pmns_", "")
        plt.scatter(chi2, y, s=10, alpha=0.4, label=label)

    plt.xlabel(r"$\chi^2_{\rm total}$")
    plt.ylabel("PMNS observable value")
    plt.title("PMNS predictions vs chi2")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def _plot_theta_star(df: pd.DataFrame, chi2: np.ndarray, run_id: str, fig_dir: Path) -> List[Path]:
    written: List[Path] = []

    theta_col = None
    # Prefer the sampled parameter column if present
    if "p_theta_star" in df.columns:
        theta_col = "p_theta_star"
    elif "pmns_deltaCP" in df.columns:
        theta_col = "pmns_deltaCP"

    if theta_col is None:
        return written

    theta = df[theta_col].to_numpy()

    # Histogram
    hist_path = fig_dir / f"{run_id}_theta_star_hist.png"
    hist_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.hist(theta, bins=40)
    plt.xlabel(r"$\theta_\star$ [rad]")
    plt.ylabel("count")
    plt.title(f"Theta-star distribution ({theta_col})")
    plt.tight_layout()
    plt.savefig(hist_path)
    plt.close()
    written.append(hist_path)

    # Scatter vs chi2
    scatter_path = fig_dir / f"{run_id}_theta_star_vs_chi2.png"
    plt.figure(figsize=(8, 5))
    plt.scatter(chi2, theta, s=10, alpha=0.4)
    plt.xlabel(r"$\chi^2_{\rm total}$")
    plt.ylabel(r"$\theta_\star$ [rad]")
    plt.title(f"{theta_col} vs chi2")
    plt.tight_layout()
    plt.savefig(scatter_path)
    plt.close()
    written.append(scatter_path)

    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a theta-star sweep run")
    parser.add_argument(
        "--run-id",
        required=True,
        help="Run ID (directory name under data/processed/runs)",
    )
    parser.add_argument(
        "--ordering",
        default="NO",
        choices=["NO", "IO", "no", "io"],
        help="Neutrino mass ordering (label only)",
    )
    parser.add_argument(
        "--base-dir",
        default="data/processed/runs",
        help="Base directory for runs",
    )
    parser.add_argument(
        "--fig-dir",
        default="data/processed/figures",
        help="Directory where figures will be written",
    )
    args = parser.parse_args()

    base_dir = Path(args.base_dir)
    fig_dir = Path(args.fig_dir)
    run_id = args.run_id

    df = _load_run(run_id, base_dir)
    chi2 = df["chi2_total"].to_numpy()
    n_samples = len(df)

    print(f"Run: {base_dir / run_id}")
    print(f"Samples: {n_samples}")
    print(_summary_stats(chi2))

    written: List[Path] = []

    # 1) chi2 histogram
    chi2_path = fig_dir / f"{run_id}_chi2_hist.png"
    _plot_chi2_hist(chi2, chi2_path)
    written.append(chi2_path)

    # 2) PMNS vs chi2
    pmns_path = fig_dir / f"{run_id}_pmns_vs_chi2.png"
    _plot_pmns_vs_chi2(df, chi2, pmns_path)
    written.append(pmns_path)

    # 3) theta_star plots (if present)
    written += _plot_theta_star(df, chi2, run_id, fig_dir)

    if written:
        print("Wrote figures:")
        for p in written:
            print(f"  - {p}")


if __name__ == "__main__":
    main()