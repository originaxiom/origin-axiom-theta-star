"""
theta_star_delta_only.py

First θ★-aware ansatz.

- Introduces an explicit parameter `theta_star`.
- Identifies `theta_star` with the Dirac phase `deltaCP` (in radians).
- Keeps all other PMNS observables (s12^2, s13^2, s23^2, dm21, dm3l)
  as direct parameters, similar to the `example_minimal` toy ansatz.

This ansatz is meant as a *δ_CP-only projection of θ★*:
it is useful to understand how neutrino data constrains theta_star,
but it is NOT yet a full structural θ★ model.
"""

from __future__ import annotations

from typing import Dict, Mapping, Tuple

from ..constants import (
    PMNSOrdering,
    TAU,
    Target,
    CKM_TARGETS,
    get_pmns_targets,
)
from .base import ParamDict, ThetaStarAnsatz


class ThetaStarDeltaOnlyAnsatz(ThetaStarAnsatz):
    """
    θ★ ansatz where theta_star is identified with deltaCP.

    Parameters
    ----------
    name:
        Optional custom name; default is "theta_star_delta_only".
    """

    def __init__(self, name: str = "theta_star_delta_only") -> None:
        # Explicit θ★ parameter + direct parameters for remaining PMNS
        pmns_keys = ["s12_2", "s13_2", "s23_2", "dm21", "dm3l"]
        self._pmns_keys = pmns_keys

        # CKM parameters currently not linked to theta_star; kept only
        # so joint fits are technically possible later.
        ckm_keys = list(CKM_TARGETS.keys())
        self._ckm_keys = ckm_keys

        param_names = ["theta_star"] + pmns_keys + ckm_keys
        super().__init__(name=name, param_names=param_names)

    # ------------------------------------------------------------------ #
    # bounds
    # ------------------------------------------------------------------ #

    def _pmns_bounds_from_targets(self, ordering: PMNSOrdering) -> Dict[str, Tuple[float, float]]:
        targets = get_pmns_targets(ordering)
        bounds: Dict[str, Tuple[float, float]] = {}

        def around(t: Target, hard_min=None, hard_max=None, scale: float = 5.0) -> Tuple[float, float]:
            if t.sigma > 0.0:
                lo = t.value - scale * t.sigma
                hi = t.value + scale * t.sigma
            else:
                # fall back to a generic ±20% window if sigma is not set
                lo = 0.8 * t.value
                hi = 1.2 * t.value if t.value != 0.0 else 1.0
            if hard_min is not None:
                lo = max(lo, hard_min)
            if hard_max is not None:
                hi = min(hi, hard_max)
            return float(lo), float(hi)

        # Clip sin^2(theta) to [0, 1]
        if "s12_2" in targets:
            bounds["s12_2"] = around(targets["s12_2"], hard_min=0.0, hard_max=1.0)
        if "s13_2" in targets:
            bounds["s13_2"] = around(targets["s13_2"], hard_min=0.0, hard_max=1.0)
        if "s23_2" in targets:
            bounds["s23_2"] = around(targets["s23_2"], hard_min=0.0, hard_max=1.0)

        # Mass-squared differences
        if "dm21" in targets:
            bounds["dm21"] = around(targets["dm21"])
        if "dm3l" in targets:
            bounds["dm3l"] = around(targets["dm3l"])

        return bounds

    def _ckm_bounds_from_targets(self) -> Dict[str, Tuple[float, float]]:
        bounds: Dict[str, Tuple[float, float]] = {}
        for name, target in CKM_TARGETS.items():
            if target.sigma > 0.0:
                span = 5.0 * target.sigma
                lo = target.value - span
                hi = target.value + span
            else:
                lo = 0.0
                hi = 1.0
            bounds[name] = (float(lo), float(hi))
        return bounds

    def param_bounds(self, ordering: PMNSOrdering = "NO") -> Mapping[str, Tuple[float, float]]:
        bounds: Dict[str, Tuple[float, float]] = {}

        # theta_star: an angle in [0, 2π)
        bounds["theta_star"] = (0.0, TAU)

        # remaining PMNS
        bounds.update(self._pmns_bounds_from_targets(ordering))

        # CKM (currently unconstrained by theta_star in this ansatz)
        bounds.update(self._ckm_bounds_from_targets())

        return bounds

    # ------------------------------------------------------------------ #
    # predictions
    # ------------------------------------------------------------------ #

    def predict_pmns(self, params: ParamDict, ordering: PMNSOrdering = "NO") -> Mapping[str, float]:
        targets = get_pmns_targets(ordering)
        out: Dict[str, float] = {}

        # Explicit δ_CP = theta_star
        theta_star = float(params.get("theta_star", targets["deltaCP"].value))
        out["deltaCP"] = theta_star

        # Remaining PMNS observables: take from params if present,
        # otherwise default to target values.
        for key in self._pmns_keys:
            if key in params:
                out[key] = float(params[key])
            elif key in targets:
                out[key] = float(targets[key].value)

        return out

    def predict_ckm(self, params: ParamDict) -> Mapping[str, float]:
        """
        For now, CKM is not linked to theta_star in this ansatz.

        We simply treat CKM observables as direct parameters, falling
        back to the CKM targets if a parameter is omitted.
        """
        if not CKM_TARGETS:
            return {}

        out: Dict[str, float] = {}
        for key in self._ckm_keys:
            if key in params:
                out[key] = float(params[key])
            elif key in CKM_TARGETS:
                out[key] = float(CKM_TARGETS[key].value)
        return out