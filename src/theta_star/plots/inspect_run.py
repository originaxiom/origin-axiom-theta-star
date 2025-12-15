"""
Helpers to inspect a single sweep run: basic stats + plots.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd

from ..constants import get_pmns_targets, PMNSOrdering


def load_run(run_dir: Path) -> pd.DataFrame:
    run_dir = Path(run_dir)
    csv_path = run_dir / "results.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"No results.csv in {run_dir}")
    return pd.read_csv(csv_path)


def summarize_chi2(df: pd.DataFrame) -> Tuple[float, float, float]:
    chi2 = df["chi2_total"]
    return float(chi2.min()), float(chi2.mean()), float(chi2.median())


def plot_chi2_hist(df: pd.DataFrame, out_path: Path) -> None:
    fig = plt.figure(figsize=(6, 4))
    ax = plt.gca()
    ax.hist(df["chi2_total"], bins=40)
    ax.set_xlabel(r"$\chi^2_{\mathrm{total}}$")
    ax.set_ylabel("count")
    ax.set_title("Chi2 distribution")
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def plot_pmns_scatter(df: pd.DataFrame, out_path: Path, ordering: PMNSOrdering = "NO") -> None:
    pmns_targets = get_pmns_targets(ordering)
    # Only look at the observables we know about
    keys = ["s12_2", "s13_2", "s23_2", "dm21", "dm3l"]

    fig = plt.figure(figsize=(8, 6))
    ax = plt.gca()

    for key in keys:
        col = f"pmns_{key}"
        if col not in df.columns or key not in pmns_targets:
            continue
        x = df["chi2_total"]
        y = df[col]
        ax.plot(x, y, ".", alpha=0.3, label=key)

    ax.set_xlabel(r"$\chi^2_{\mathrm{total}}$")
    ax.set_ylabel("PMNS observable value")
    ax.set_title("PMNS predictions vs chi2")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)