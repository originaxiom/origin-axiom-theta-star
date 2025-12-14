"""
constants.py

Central place for:
- target observables (CKM/PMNS) we fit to
- unit conventions + helper transforms
- ordering flags (PMNS: NO vs IO)
- pinned source metadata (must match docs/DATA_SOURCES.md)

Policy:
- Targets live ONLY here.
- Any change to targets must also update docs/DATA_SOURCES.md and add an entry
  to PROGRESS_LOG.md (no silent drift).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal

PMNSOrdering = Literal["NO", "IO"]

PI = 3.141592653589793
TAU = 2.0 * PI
DEG = PI / 180.0


@dataclass(frozen=True)
class Target:
    """
    A single target observable:
      - value: central value
      - sigma: 1-sigma uncertainty (or an effective scale for loss weighting)
      - name: human label (optional)
      - units: optional string
      - note: optional short note (e.g., convention/sign)
    """
    value: float
    sigma: float
    name: str = ""
    units: str = ""
    note: str = ""


def _t(value: float, sigma: float, name: str = "", units: str = "", note: str = "") -> Target:
    return Target(value=float(value), sigma=float(sigma), name=name, units=units, note=note)


def deg2rad(x_deg: float) -> float:
    return float(x_deg) * DEG


def rad2deg(x_rad: float) -> float:
    return float(x_rad) / DEG


def wrap_to_pi(angle_rad: float) -> float:
    """
    Map angle to (-pi, pi].
    Useful for defining a continuous angular difference.
    """
    a = float(angle_rad)
    a = (a + PI) % TAU - PI
    # put +pi on the right-closed interval if needed
    if a <= -PI:
        a += TAU
    return a


def angle_distance(a_rad: float, b_rad: float) -> float:
    """
    Smallest signed difference a-b on a circle, in (-pi, pi].
    """
    return wrap_to_pi(float(a_rad) - float(b_rad))


# -------------------------
# Source metadata (pin later)
# -------------------------

PMNS_SOURCE = {
    "provider": "NuFIT",
    "version": "TBD",
    "url": "TBD",
    "retrieved_utc": "TBD",
    "notes": "Targets stored as sin^2(theta_ij), deltaCP in radians, dm in eV^2 (NuFIT conventions).",
}

CKM_SOURCE = {
    "provider": "PDG",
    "version": "TBD",
    "url": "TBD",
    "retrieved_utc": "TBD",
    "notes": "Decide Wolfenstein vs moduli+CP; then pin values here.",
}


# -------------------------
# PMNS targets (placeholders)
# -------------------------
# Conventions:
# - s12_2, s13_2, s23_2 are sin^2(theta_12/13/23) (dimensionless)
# - deltaCP is in radians (periodic mod 2pi)
# - dm21 and dm3l are in eV^2
# - dm3l carries SIGN:
#     NO: dm3l > 0
#     IO: dm3l < 0
#
# Fill these from NuFIT (and record NuFIT version + ordering choice).
#
# Note: Many global fits publish asymmetric errors; for Phase-0 we use a single
# sigma as an effective weight (can be refined later).

PMNS_TARGETS: Dict[PMNSOrdering, Dict[str, Target]] = {
    "NO": {
        "s12_2": _t(0.0, 1.0, name="sin^2(theta12)", units="", note="NuFIT"),
        "s13_2": _t(0.0, 1.0, name="sin^2(theta13)", units="", note="NuFIT"),
        "s23_2": _t(0.0, 1.0, name="sin^2(theta23)", units="", note="NuFIT (NO)"),
        "deltaCP": _t(0.0, PI, name="deltaCP", units="rad", note="periodic mod 2pi"),
        "dm21": _t(0.0, 1.0, name="Delta m^2_21", units="eV^2"),
        "dm3l": _t(0.0, 1.0, name="Delta m^2_3l", units="eV^2", note="NO: positive"),
    },
    "IO": {
        "s12_2": _t(0.0, 1.0, name="sin^2(theta12)", units="", note="NuFIT"),
        "s13_2": _t(0.0, 1.0, name="sin^2(theta13)", units="", note="NuFIT"),
        "s23_2": _t(0.0, 1.0, name="sin^2(theta23)", units="", note="NuFIT (IO)"),
        "deltaCP": _t(0.0, PI, name="deltaCP", units="rad", note="periodic mod 2pi"),
        "dm21": _t(0.0, 1.0, name="Delta m^2_21", units="eV^2"),
        "dm3l": _t(0.0, 1.0, name="Delta m^2_3l", units="eV^2", note="IO: negative"),
    },
}


def get_pmns_targets(ordering: PMNSOrdering) -> Dict[str, Target]:
    o = ordering.upper()  # type: ignore[assignment]
    if o not in ("NO", "IO"):
        raise ValueError(f"Unknown PMNS ordering: {ordering!r}")
    return PMNS_TARGETS[o]  # type: ignore[index]


# -------------------------
# CKM targets (placeholder)
# -------------------------
# Decide one canonical parameterization and pin it here.
CKM_TARGETS: Dict[str, Target] = {
    # Example placeholders:
    # "lambda": _t(0.0, 1.0, name="Wolfenstein lambda"),
    # "A":      _t(0.0, 1.0, name="Wolfenstein A"),
    # "rhobar": _t(0.0, 1.0, name="Wolfenstein rhobar"),
    # "etabar": _t(0.0, 1.0, name="Wolfenstein etabar"),
}