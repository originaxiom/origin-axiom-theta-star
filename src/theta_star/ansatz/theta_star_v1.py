"""
theta_star_v1.py

First *structured* θ★ ansatz beyond the δ_CP-only projection.

Idea
----
- θ★ is an angle in [0, 2π).
- We identify δ_CP ≡ theta_star.
- The three PMNS mixing angles are modulated around their NuFIT 5.2
  central values by cosines of θ★ with fixed phase offsets.
- The two mass-squared splittings share a common fractional shift
  controlled by a single nuisance parameter k_mass.

This introduces correlations between observables while keeping the
parameter count modest:
    params = {theta_star, eps12, eps13, eps23, k_mass, (CKM ...)}

CKM observables are currently treated as direct parameters (like in the
previous ansatz); they are present only to allow future joint fits.
"""

from __future__ import annotations

from math import cos
from typing import Dict, Mapping, Tuple

from ..constants import (
    PMNSOrdering,
    TAU,
    Target,
    CKM_TARGETS,
    get_pmns_targets,
)
from .base import ParamDict, ThetaStarAnsatz


def _clip(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


class ThetaStarV1Ansatz(ThetaStarAnsatz):
    """
    θ★ ansatz with cosine modulations of PMNS angles and a common
    mass-splitting shift.

    Parameters
    ----------
    name:
        Optional custom name; default is "theta_star_v1".
    """

    def __init__(self, name: str = "theta_star_v1") -> None:
        # explicit θ★ plus 4 PMNS-related nuisance parameters
        self._pmns_mod_params = ["eps12", "eps13", "eps23", "k_mass"]

        # CKM parameters (direct), for future joint fits
        ckm_keys = list(CKM_TARGETS.keys())
        self._ckm_keys = ckm_keys

        param_names = ["theta_star"] + self._pmns_mod_params + ckm_keys
        super().__init__(name=name, param_names=param_names)

    # ------------------------------------------------------------------ #
    # bounds
    # ------------------------------------------------------------------ #

    def _pmns_mod_bounds(self) -> Dict[str, Tuple[float, float]]:
        # eps_* amplitudes are dimensionless multipliers; |eps| <= 0.5
        # means up to 50% modulation around the central value.
        return {
            "eps12": (-0.5, 0.5),
            "eps13": (-0.5, 0.5),
            "eps23": (-0.5, 0.5),
            # k_mass is a common fractional shift for dm21 and dm3l
            "k_mass": (-0.5, 0.5),
        }

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

        # modulation parameters
        bounds.update(self._pmns_mod_bounds())

        # CKM (direct)
        bounds.update(self._ckm_bounds_from_targets())

        return bounds

    # ------------------------------------------------------------------ #
    # predictions
    # ------------------------------------------------------------------ #

    def predict_pmns(self, params: ParamDict, ordering: PMNSOrdering = "NO") -> Mapping[str, float]:
        targets = get_pmns_targets(ordering)
        out: Dict[str, float] = {}

        # θ★ and nuisances (with safe defaults)
        theta_star = float(params.get("theta_star", targets["deltaCP"].value))
        eps12 = float(params.get("eps12", 0.0))
        eps13 = float(params.get("eps13", 0.0))
        eps23 = float(params.get("eps23", 0.0))
        k_mass = float(params.get("k_mass", 0.0))

        # 1. Dirac phase: δ_CP ≡ θ★
        out["deltaCP"] = theta_star

        # 2. Mixing angles: modulate around NuFIT central values.
        #
        # We use three cosine waves with fixed phase offsets:
        #   s12^2  ~ s12^2_0 * (1 + eps12 * cos(theta_star))
        #   s13^2  ~ s13^2_0 * (1 + eps13 * cos(theta_star + 2π/3))
        #   s23^2  ~ s23^2_0 * (1 + eps23 * cos(theta_star + 4π/3))
        #
        # This is a phenomenological way to encode correlated dependence
        # on a single master phase.
        phi12 = theta_star
        phi13 = theta_star + (TAU / 3.0)  # 2π/3
        phi23 = theta_star + (2.0 * TAU / 3.0)  # 4π/3

        s12_0 = float(targets["s12_2"].value)
        s13_0 = float(targets["s13_2"].value)
        s23_0 = float(targets["s23_2"].value)

        s12_2 = s12_0 * (1.0 + eps12 * cos(phi12))
        s13_2 = s13_0 * (1.0 + eps13 * cos(phi13))
        s23_2 = s23_0 * (1.0 + eps23 * cos(phi23))

        # ensure they stay within physical [0, 1]
        out["s12_2"] = _clip(s12_2, 0.0, 1.0)
        out["s13_2"] = _clip(s13_2, 0.0, 1.0)
        out["s23_2"] = _clip(s23_2, 0.0, 1.0)

        # 3. Mass-squared splittings: common fractional shift.
        dm21_0 = float(targets["dm21"].value)
        dm3l_0 = float(targets["dm3l"].value)

        scale = 1.0 + k_mass
        out["dm21"] = dm21_0 * scale
        out["dm3l"] = dm3l_0 * scale

        return out

    def predict_ckm(self, params: ParamDict) -> Mapping[str, float]:
        """
        CKM observables are currently not linked to theta_star in this
        ansatz; they are treated as direct parameters with fallback to
        the PDG targets.
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