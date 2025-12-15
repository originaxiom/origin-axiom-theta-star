"""
constants.py

Central place for:
- target observables (CKM/PMNS) we fit to
- unit conventions + helper transforms
- ordering flags (PMNS: NO vs IO)
- pinned source metadata (must match docs/DATA_SOURCES.md)

Policy
------
- Targets live ONLY here.
- Any change to targets must also update docs/DATA_SOURCES.md and add an
  entry to PROGRESS_LOG.md (no silent drift).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi
from typing import Dict, Literal, Mapping


PMNSOrdering = Literal["NO", "IO"]


@dataclass(frozen=True)
class Target:
    """
    A single target observable.

    Parameters
    ----------
    value:
        Central value of the observable in the chosen unit.
    sigma:
        1-sigma uncertainty (or effective scale for loss weighting) in
        the same unit as ``value``.
    name:
        Human readable label.
    unit:
        Unit label (e.g. "deg", "rad", "eV2", "dimensionless").
    ref:
        Short reference tag (e.g. "NuFIT 5.2 (NO)", "PDG 2024 CKM").
    """
    value: float
    sigma: float
    name: str
    unit: str = ""
    ref: str = ""


# ---------------------------------------------------------------------------
# Basic math / angle helpers
# ---------------------------------------------------------------------------

PI: float = pi
TAU: float = 2.0 * pi  # 2π


def deg_to_rad(x_deg: float) -> float:
    """Convert degrees to radians."""
    return x_deg * PI / 180.0


def rad_to_deg(x_rad: float) -> float:
    """Convert radians to degrees."""
    return x_rad * 180.0 / PI


def wrap_to_pi(x_rad: float) -> float:
    """
    Wrap an angle to the interval (-pi, pi].

    Useful for differences of CP phases where the loss should respect
    periodicity.
    """
    from math import fmod

    y = fmod(x_rad + PI, TAU)
    if y <= 0.0:
        y += TAU
    return y - PI


def angle_difference(a_rad: float, b_rad: float) -> float:
    """
    Smallest signed difference a-b on a circle, in (-pi, pi].
    """
    return wrap_to_pi(float(a_rad) - float(b_rad))


def angle_distance(a_rad: float, b_rad: float) -> float:
    """
    Smallest absolute distance between two angles on a circle, in [0, pi].
    """
    from math import fabs

    return fabs(angle_difference(a_rad, b_rad))


# ---------------------------------------------------------------------------
# PMNS targets (NuFIT 5.2, with SK atmospheric data)
#
# Keys match the notation used in the repo:
#   s12_2, s13_2, s23_2   := sin^2(theta_ij)
#   dm21                  := Δm^2_21
#   dm3l                  := Δm^2_3ℓ (sign carries ordering)
#   deltaCP               := Dirac phase δ (radians)
#
# Best-fit values and 1σ errors from NuFIT 5.2 (with SK atm.) as shown
# e.g. in T. Schwetz, PetcovFest slides (2023).  [oai_citation:0‡Agenda (Indico)](https://agenda.infn.it/event/34851/contributions/193747/attachments/104515/146645/PetcovFest-Schwetz.pdf)
# ---------------------------------------------------------------------------

# Symmetrised 1σ errors (average of + and -) in the table.
_PMNS_NO: Dict[str, Target] = {
    "s12_2": Target(
        value=0.303,
        sigma=0.012,
        name="sin^2 theta12 (NO)",
        unit="dimensionless",
        ref="NuFIT 5.2 (NO, with SK atm.)",
    ),
    "s23_2": Target(
        value=0.451,
        sigma=(0.019 + 0.016) / 2.0,
        name="sin^2 theta23 (NO)",
        unit="dimensionless",
        ref="NuFIT 5.2 (NO, with SK atm.)",
    ),
    "s13_2": Target(
        value=0.02225,
        sigma=(0.00056 + 0.00059) / 2.0,
        name="sin^2 theta13 (NO)",
        unit="dimensionless",
        ref="NuFIT 5.2 (NO, with SK atm.)",
    ),
    "dm21": Target(
        value=7.41e-5,
        sigma=((0.21 + 0.20) / 2.0) * 1.0e-5,
        name="Delta m^2_21",
        unit="eV2",
        ref="NuFIT 5.2 (NO, with SK atm.)",
    ),
    "dm3l": Target(
        value=2.507e-3,
        sigma=((0.026 + 0.027) / 2.0) * 1.0e-3,
        name="Delta m^2_3l (NO)",
        unit="eV2",
        ref="NuFIT 5.2 (NO, with SK atm.)",
    ),
    "deltaCP": Target(
        value=deg_to_rad(232.0),
        sigma=deg_to_rad((36.0 + 26.0) / 2.0),
        name="delta_CP (Dirac phase, NO)",
        unit="rad",
        ref="NuFIT 5.2 (NO, with SK atm.)",
    ),
}

_PMNS_IO: Dict[str, Target] = {
    "s12_2": Target(
        value=0.303,
        sigma=0.012,
        name="sin^2 theta12 (IO)",
        unit="dimensionless",
        ref="NuFIT 5.2 (IO, with SK atm.)",
    ),
    "s23_2": Target(
        value=0.569,
        sigma=(0.016 + 0.021) / 2.0,
        name="sin^2 theta23 (IO)",
        unit="dimensionless",
        ref="NuFIT 5.2 (IO, with SK atm.)",
    ),
    "s13_2": Target(
        value=0.02223,
        sigma=(0.00058 + 0.00058) / 2.0,
        name="sin^2 theta13 (IO)",
        unit="dimensionless",
        ref="NuFIT 5.2 (IO, with SK atm.)",
    ),
    "dm21": Target(
        value=7.41e-5,
        sigma=((0.21 + 0.20) / 2.0) * 1.0e-5,
        name="Delta m^2_21",
        unit="eV2",
        ref="NuFIT 5.2 (IO, with SK atm.)",
    ),
    "dm3l": Target(
        value=-2.486e-3,
        sigma=((0.025 + 0.028) / 2.0) * 1.0e-3,
        name="Delta m^2_3l (IO)",
        unit="eV2",
        ref="NuFIT 5.2 (IO, with SK atm.)",
    ),
    "deltaCP": Target(
        value=deg_to_rad(276.0),
        sigma=deg_to_rad((22.0 + 29.0) / 2.0),
        name="delta_CP (Dirac phase, IO)",
        unit="rad",
        ref="NuFIT 5.2 (IO, with SK atm.)",
    ),
}

PMNS_TARGETS: Mapping[PMNSOrdering, Mapping[str, Target]] = {
    "NO": _PMNS_NO,
    "IO": _PMNS_IO,
}


def get_pmns_targets(ordering: PMNSOrdering = "NO") -> Mapping[str, Target]:
    """
    Return the PMNS targets for the requested mass ordering.
    """
    key: PMNSOrdering = "IO" if str(ordering).upper() == "IO" else "NO"
    return PMNS_TARGETS[key]


# ---------------------------------------------------------------------------
# CKM targets (Wolfenstein parameters)
#
# Wolfenstein parameters (λ, A, ρ̄, η̄) from the PDG 2024 CKM review,
# global fit results.  [oai_citation:1‡Particle Data Group](https://pdg.lbl.gov/2025/reviews/rpp2024-rev-ckm-matrix.pdf)
# ---------------------------------------------------------------------------

CKM_TARGETS: Dict[str, Target] = {
    "lambda": Target(
        value=0.22501,
        sigma=0.00068,
        name="Wolfenstein lambda",
        unit="dimensionless",
        ref="PDG 2024 CKM global fit",
    ),
    "A": Target(
        value=0.826,
        sigma=0.016,  # symmetrised from PDG quoted errors
        name="Wolfenstein A",
        unit="dimensionless",
        ref="PDG 2024 CKM global fit",
    ),
    "rhobar": Target(
        value=0.159,
        sigma=0.010,
        name="Wolfenstein rhobar",
        unit="dimensionless",
        ref="PDG 2024 CKM global fit",
    ),
    "etabar": Target(
        value=0.348,
        sigma=0.010,
        name="Wolfenstein etabar",
        unit="dimensionless",
        ref="PDG 2024 CKM global fit",
    ),
}