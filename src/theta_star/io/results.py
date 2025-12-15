"""
Helpers for writing sweep / fit results to disk.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

import pandas as pd


def run_dir(base: Path, run_id: str) -> Path:
    """
    Directory for a given run_id under the chosen base directory.
    """
    return base / run_id


def results_csv_path(base: Path, run_id: str) -> Path:
    """
    Path to the main CSV table for a run.
    """
    return run_dir(base, run_id) / "results.csv"


def write_results_table(base: Path, run_id: str, rows: Iterable[Mapping[str, object]]) -> Path:
    """
    Write a sweep table (list of dict-like rows) to CSV.

    Returns the path to the written file.
    """
    base = Path(base)
    rdir = run_dir(base, run_id)
    rdir.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(list(rows))
    out_path = rdir / "results.csv"
    df.to_csv(out_path, index=False)
    return out_path