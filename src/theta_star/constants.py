"""
constants.py

Targets (CKM / PMNS) + uncertainties for phenomenology fits.

Policy:
- All numeric targets live here.
- Must include a source/version string for CKM and PMNS.
- If targets change, update docs/DATA_SOURCES.md + PROGRESS_LOG.md.

We start with placeholders and lock numbers once you choose:
- CKM year/version (PDG YYYY)
- PMNS NuFIT version + ordering (NO/IO)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Target:
    name: str
    value: float
    sigma: float
    source: str


# -----------------------------
# Source/version pins (EDIT ME)
# -----------------------------
CKM_SOURCE = "PDG YYYY (to fill)"
PMNS_SOURCE = "NuFIT vX.Y (NO/IO) (to fill)"


# -----------------------------
# CKM targets (minimal set)
# -----------------------------
CKM_TARGETS: Dict[str, Target] = {
    # Examples (placeholders):
    # "Vus": Target("Vus", 0.2243, 0.0005, CKM_SOURCE),
    # "Vcb": Target("Vcb", 0.0422, 0.0008, CKM_SOURCE),
    # "Vub": Target("Vub", 0.00394, 0.00036, CKM_SOURCE),
    # Optional CP: "J": Target("J", 3.0e-5, 0.2e-5, CKM_SOURCE),
}


# -----------------------------
# PMNS targets (minimal set)
# -----------------------------
PMNS_TARGETS: Dict[str, Target] = {
    # Examples (placeholders):
    # "s12_2": Target("sin2_theta12", 0.304, 0.012, PMNS_SOURCE),
    # "s23_2": Target("sin2_theta23", 0.573, 0.016, PMNS_SOURCE),
    # "s13_2": Target("sin2_theta13", 0.0222, 0.0006, PMNS_SOURCE),
    # Optional CP phase (deg): "delta_cp_deg": Target("delta_cp_deg", 195.0, 25.0, PMNS_SOURCE),
}


def as_dict(targets: Dict[str, Target]) -> Dict[str, Dict[str, float]]:
    return {k: {"value": v.value, "sigma": v.sigma} for k, v in targets.items()}