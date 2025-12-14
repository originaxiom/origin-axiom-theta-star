"""
constants.py

Central place for:
- target observables (CKM/PMNS) we fit to
- unit conventions
- ordering flags (PMNS: NO vs IO)

Important: we keep target numbers *explicitly sourced* (see docs/DATA_SOURCES.md).
Do not silently change them without logging in PROGRESS_LOG.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal, Optional


PMNSOrdering = Literal["NO", "IO"]


@dataclass(frozen=True)
class Target:
    """
    A single target observable:
      - value: central value
      - sigma: 1-sigma uncertainty (or an effective scale for loss weighting)
      - name: human label (optional)
      - units: optional string
    """
    value: float
    sigma: float
    name: str = ""
    units: str = ""


def _t(value: float, sigma: float, name: str = "", units: str = "") -> Target:
    return Target(value=float(value), sigma=float(sigma), name=name, units=units)


# --- PMNS targets (placeholders) ---
# Convention: angles in radians, delta_cp in radians, mass splittings in eV^2.
# Fill these from your chosen global-fit source and record it in docs/DATA_SOURCES.md.

PMNS_TARGETS_NO: Dict[str, Target] = {
    # Mixing angles
    "theta12": _t(value=0.0, sigma=1.0, name="theta12", units="rad"),  # TODO
    "theta13": _t(value=0.0, sigma=1.0, name="theta13", units="rad"),  # TODO
    "theta23": _t(value=0.0, sigma=1.0, name="theta23", units="rad"),  # TODO
    # CP phase
    "deltaCP": _t(value=0.0, sigma=3.14159, name="deltaCP", units="rad"),  # TODO
    # Mass splittings (optional in early phase)
    "dm21": _t(value=0.0, sigma=1.0, name="Delta m^2_21", units="eV^2"),  # TODO
    "dm3l": _t(value=0.0, sigma=1.0, name="Delta m^2_3l (NO)", units="eV^2"),  # TODO (positive)
}

PMNS_TARGETS_IO: Dict[str, Target] = {
    "theta12": _t(value=0.0, sigma=1.0, name="theta12", units="rad"),  # TODO
    "theta13": _t(value=0.0, sigma=1.0, name="theta13", units="rad"),  # TODO
    "theta23": _t(value=0.0, sigma=1.0, name="theta23", units="rad"),  # TODO
    "deltaCP": _t(value=0.0, sigma=3.14159, name="deltaCP", units="rad"),  # TODO
    "dm21": _t(value=0.0, sigma=1.0, name="Delta m^2_21", units="eV^2"),  # TODO
    "dm3l": _t(value=0.0, sigma=1.0, name="Delta m^2_3l (IO)", units="eV^2"),  # TODO (negative)
}


def get_pmns_targets(ordering: PMNSOrdering) -> Dict[str, Target]:
    ordering = ordering.upper()  # type: ignore[assignment]
    if ordering == "NO":
        return PMNS_TARGETS_NO
    if ordering == "IO":
        return PMNS_TARGETS_IO
    raise ValueError(f"Unknown PMNS ordering: {ordering!r}")


# Small helpers (you'll use these in ansatz code)
PI = 3.141592653589793
DEG = PI / 180.0


def deg2rad(x_deg: float) -> float:
    return float(x_deg) * DEG