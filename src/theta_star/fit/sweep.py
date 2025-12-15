"""
Simple random sweeps in parameter space for a given ansatz.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List, Mapping, Tuple

from pathlib import Path

import numpy as np

from ..constants import PMNSOrdering
from ..ansatz import get_ansatz
from ..fit.loss import LossBreakdown, joint_chi2
from ..io.runlog import write_run_meta
from ..io.results import write_results_table


@dataclass
class SweepConfig:
    ansatz_name: str = "example_minimal"
    ordering: PMNSOrdering = "NO"
    n_samples: int = 1000
    seed: int | None = None
    include_pmns: bool = True
    include_ckm: bool = True
    # base directory for processed results
    base_dir: Path = Path("data/processed/runs")

    def normalized_ordering(self) -> PMNSOrdering:
        o = str(self.ordering).upper()
        return "IO" if o == "IO" else "NO"


def _sample_params(bounds: Mapping[str, Tuple[float, float]], rng: np.random.Generator) -> Dict[str, float]:
    params: Dict[str, float] = {}
    for name, (lo, hi) in bounds.items():
        params[name] = float(rng.uniform(lo, hi))
    return params


def run_sweep(config: SweepConfig, run_id: str | None = None) -> Tuple[List[Dict[str, object]], Dict[str, object]]:
    """
    Run a random sweep and write artifacts to disk.

    Returns
    -------
    rows:
        List of per-sample dictionaries (the same content that is written
        to CSV).
    summary_meta:
        JSON-serialisable summary metadata (also written to run_meta.json).
    """
    ordering = config.normalized_ordering()
    ansatz = get_ansatz(config.ansatz_name)
    bounds = ansatz.param_bounds(ordering=ordering)

    rng = np.random.default_rng(config.seed)

    rows: List[Dict[str, object]] = []
    best_idx = -1
    best_loss: LossBreakdown | None = None
    best_params: Dict[str, float] | None = None
    best_pmns: Dict[str, float] | None = None
    best_ckm: Dict[str, float] | None = None

    for i in range(config.n_samples):
        params = _sample_params(bounds, rng=rng)
        pred_pmns = ansatz.predict_pmns(params, ordering=ordering)
        pred_ckm = ansatz.predict_ckm(params)

        loss = joint_chi2(
            pred_pmns,
            pred_ckm,
            ordering=ordering,
            include_pmns=config.include_pmns,
            include_ckm=config.include_ckm,
        )

        row: Dict[str, object] = {
            "sample": i,
            "chi2_total": loss.chi2_total,
            "chi2_pmns": loss.chi2_pmns,
            "chi2_ckm": loss.chi2_ckm,
            "n_pmns": loss.n_pmns,
            "n_ckm": loss.n_ckm,
        }

        # Parameters as p_<name>
        for name, value in params.items():
            row[f"p_{name}"] = value

        # Flatten predictions
        for name, val in pred_pmns.items():
            row[f"pmns_{name}"] = val
        for name, val in pred_ckm.items():
            row[f"ckm_{name}"] = val

        rows.append(row)

        if best_loss is None or loss.chi2_total < best_loss.chi2_total:
            best_idx = i
            best_loss = loss
            best_params = dict(params)
            best_pmns = dict(pred_pmns)
            best_ckm = dict(pred_ckm)

    if best_loss is None:
        raise RuntimeError("Sweep produced no samples")

    cfg_dict = asdict(config)
    # Make JSON safe
    cfg_dict["base_dir"] = str(cfg_dict.get("base_dir"))

    summary: Dict[str, object] = {
        "config": cfg_dict,
        "ordering": ordering,
        "ansatz_name": config.ansatz_name,
        "n_samples": int(config.n_samples),
        "best_sample": int(best_idx),
        "best_loss": {
            "chi2_total": float(best_loss.chi2_total),
            "chi2_pmns": float(best_loss.chi2_pmns),
            "chi2_ckm": float(best_loss.chi2_ckm),
            "n_pmns": int(best_loss.n_pmns),
            "n_ckm": int(best_loss.n_ckm),
        },
        "best_params": best_params,
        "best_pmns": best_pmns,
        "best_ckm": best_ckm,
    }

    if run_id is None:
        run_id = f"{ordering}_{config.ansatz_name}_N{config.n_samples}"

    base = Path(config.base_dir)
    csv_path = write_results_table(base, run_id, rows)
    meta_path = base / run_id / "run_meta.json"
    meta = summary | {"run_id": run_id, "results_csv": str(csv_path)}
    write_run_meta(meta_path, meta)

    return rows, summary