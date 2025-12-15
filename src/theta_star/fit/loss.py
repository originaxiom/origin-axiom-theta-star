"""
Loss functions for theta* fits.

We adopt a simple weighted chi^2:

    chi^2 = sum_i ((pred_i - target_i) / sigma_i)^2

with special handling for periodic angular quantities such as delta_CP
(where we use the minimal angular distance on the circle).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping, Tuple

from ..constants import (
    CKM_TARGETS,
    PMNSOrdering,
    Target,
    angle_distance,
    get_pmns_targets,
)


@dataclass
class LossBreakdown:
    chi2_total: float
    chi2_ckm: float
    chi2_pmns: float
    n_ckm: int
    n_pmns: int
    # per-observable contributions, keyed by e.g. "pmns_s12_2"
    terms: Dict[str, float]


def _chi2_term(pred: float, target: Target) -> float:
    if target.sigma <= 0.0:
        return 0.0
    r = (float(pred) - float(target.value)) / float(target.sigma)
    return float(r * r)


def pmns_chi2(pred: Mapping[str, float], ordering: PMNSOrdering = "NO") -> Tuple[float, int, Dict[str, float]]:
    """
    Compute chi^2 for PMNS observables.
    """
    targets = get_pmns_targets(ordering)
    chi2 = 0.0
    n_used = 0
    terms: Dict[str, float] = {}

    for name, t in targets.items():
        if name not in pred:
            continue

        if name == "deltaCP":
            # Periodic: pred and target are in radians.
            d = angle_distance(float(pred[name]), float(t.value))
            if t.sigma > 0.0:
                r = d / float(t.sigma)
                c = float(r * r)
            else:
                c = 0.0
        else:
            c = _chi2_term(pred[name], t)

        chi2 += c
        n_used += 1
        terms[f"pmns_{name}"] = c

    return chi2, n_used, terms


def ckm_chi2(pred: Mapping[str, float]) -> Tuple[float, int, Dict[str, float]]:
    """
    Compute chi^2 for CKM observables.

    If CKM_TARGETS is empty, this returns (0, 0, {}).
    """
    if not CKM_TARGETS:
        return 0.0, 0, {}

    chi2 = 0.0
    n_used = 0
    terms: Dict[str, float] = {}

    for name, t in CKM_TARGETS.items():
        if name not in pred:
            continue
        c = _chi2_term(pred[name], t)
        chi2 += c
        n_used += 1
        terms[f"ckm_{name}"] = c

    return chi2, n_used, terms


def joint_chi2(
    pred_pmns: Mapping[str, float],
    pred_ckm: Mapping[str, float],
    ordering: PMNSOrdering = "NO",
    include_pmns: bool = True,
    include_ckm: bool = True,
) -> LossBreakdown:
    """
    Joint chi^2 for PMNS + CKM.

    Either sector can be switched off using the include_* flags.
    """
    total_terms: Dict[str, float] = {}

    if include_pmns:
        chi2_pmns, n_pmns, terms_pmns = pmns_chi2(pred_pmns, ordering=ordering)
        total_terms.update(terms_pmns)
    else:
        chi2_pmns, n_pmns = 0.0, 0

    if include_ckm:
        chi2_ckm, n_ckm, terms_ckm = ckm_chi2(pred_ckm)
        total_terms.update(terms_ckm)
    else:
        chi2_ckm, n_ckm = 0.0, 0

    chi2_total = chi2_pmns + chi2_ckm

    return LossBreakdown(
        chi2_total=float(chi2_total),
        chi2_ckm=float(chi2_ckm),
        chi2_pmns=float(chi2_pmns),
        n_ckm=int(n_ckm),
        n_pmns=int(n_pmns),
        terms=total_terms,
    )