"""
theta_star_v2.py

More constrained θ★ ansatz: single global modulation for PMNS angles
and a correlated mass shift, anchored on NuFIT central values.

Idea
----
- θ★ is an angle in [0, 2π).
- We identify δ_CP ≡ theta_star (up to periodicity).
- The three PMNS mixing angles are shifted coherently around their
  NuFIT 5.2 central values by a *single* global amplitude eps_angle,
  measured in units of the 1σ uncertainties.
- The two mass-squared splittings share a common fractional shift
  controlled by a single nuisance parameter k_mass, also modulated
  by θ★.

This introduces a tighter, more physics-motivated structure than v1,
with a very small parameter set:
    params = {theta_star, eps_angle, k_mass, (CKM ...)}

CKM observables remain direct parameters for now and are included only
to allow future joint fits.
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


class ThetaStarV2Ansatz(ThetaStarAnsatz):
    """
    θ★ ansatz with a single global angle modulation and a correlated
    mass-splitting shift.

    Parameters
    ----------
    name:
        Optional custom name; default is "theta_star_v2".
    """

    def __init__(self, name: str = "theta_star_v2") -> None:
        # explicit θ★ plus 2 PMNS-related nuisance parameters
        # eps_angle: global modulation in units of 1σ for the angles
        # k_mass:   global fractional mass shift
        self._pmns_mod_params = ["eps_angle", "k_mass"]

        # CKM parameters (direct), for future joint fits
        ckm_keys = list(CKM_TARGETS.keys())
        self._ckm_keys = ckm_keys

        param_names = ["theta_star"] + self._pmns_mod_params + ckm_keys
        super().__init__(name=name, param_names=param_names)

    # ------------------------------------------------------------------ #
    # bounds
    # ------------------------------------------------------------------ #

    def _pmns_mod_bounds(self) -> Dict[str, Tuple[float, float]]:
        # eps_angle is in units of 1σ; |eps_angle| <= 0.7 means up to
        # ~0.7σ coherent shifts of all angles.
        # k_mass is a common fractional shift for dm21 and dm3l.
        return {
            "eps_angle": (-0.7, 0.7),
            "k_mass": (-0.3, 0.3),
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
        eps_angle = float(params.get("eps_angle", 0.0))
        k_mass = float(params.get("k_mass", 0.0))

        # 1. Dirac phase: δ_CP ≡ θ★ (wrap handled elsewhere via TAU)
        out["deltaCP"] = theta_star

        # 2. Mixing angles: coherent shift around NuFIT central values
        #    using 1σ scales.
        #
        # We introduce a reference theta0 in the *core* θ★ band, so that
        # the central PMNS point is recovered roughly near theta_star ≈ theta0.
        theta0 = 4.0  # rad, inside [3.2, 4.8] core band
        c = cos(theta_star - theta0)

        s12_target = targets["s12_2"]  # type: Target
        s13_target = targets["s13_2"]
        s23_target = targets["s23_2"]

        s12_0 = float(s12_target.value)
        s13_0 = float(s13_target.value)
        s23_0 = float(s23_target.value)

        # If sigma is zero for any target, treat it as a small scale to avoid
        # completely freezing that angle.
        sig12 = float(s12_target.sigma or 0.0)
        sig13 = float(s13_target.sigma or 0.0)
        sig23 = float(s23_target.sigma or 0.0)

        s12_2 = s12_0 + eps_angle * sig12 * c
        s13_2 = s13_0 + eps_angle * sig13 * c
        s23_2 = s23_0 + eps_angle * sig23 * c

        # ensure they stay within physical [0, 1]
        out["s12_2"] = _clip(s12_2, 0.0, 1.0)
        out["s13_2"] = _clip(s13_2, 0.0, 1.0)
        out["s23_2"] = _clip(s23_2, 0.0, 1.0)

        # 3. Mass-squared splittings: correlated fractional shift.
        dm21_target = targets["dm21"]
        dm3l_target = targets["dm3l"]

        dm21_0 = float(dm21_target.value)
        dm3l_0 = float(dm3l_target.value)

        # Use the same phase c for masses; k_mass sets the amplitude.
        scale = 1.0 + k_mass * c
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