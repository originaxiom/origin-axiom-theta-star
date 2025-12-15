#!/usr/bin/env python3
"""
Roll up all sweep runs and print a compact summary.

For each directory under data/processed/runs, this script will:
- read run_meta.json
- extract ansatz_name, N (n_samples), seed, best chi2, best theta_star
- print one CSV-style line

Usage:

    PYTHONPATH=src python3 scripts/rollup_runs.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


def load_run_meta(run_dir: Path) -> Optional[Dict[str, Any]]:
    meta_path = run_dir / "run_meta.json"
    if not meta_path.exists():
        return None
    with meta_path.open("r") as f:
        return json.load(f)


def main() -> None:
    base_dir = Path("data/processed/runs")
    if not base_dir.exists():
        print("No runs directory at", base_dir)
        return

    print("run_id,ansatz,N,seed,chi2_min,theta_star_best")

    for run_dir in sorted(base_dir.iterdir()):
        if not run_dir.is_dir():
            continue

        meta = load_run_meta(run_dir)
        if meta is None:
            continue

        run_id = run_dir.name
        ansatz = meta.get("ansatz_name", "unknown")

        cfg = meta.get("config", {})
        # key in run_meta is "n_samples"; fall back to "samples" if we ever change it
        N = cfg.get("n_samples", cfg.get("samples", ""))
        seed = cfg.get("seed", "")

        best_loss = meta.get("best_loss", {})
        chi2_min = best_loss.get("chi2_total", "")

        best_params = meta.get("best_params", {})
        theta_star_best = best_params.get("theta_star", "")

        print(f"{run_id},{ansatz},{N},{seed},{chi2_min},{theta_star_best}")


if __name__ == "__main__":
    main()