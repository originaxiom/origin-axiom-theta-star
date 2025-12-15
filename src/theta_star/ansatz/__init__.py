"""
Ansatz registry.

This provides a small helper to construct ansatz instances from a
string name, which is convenient for CLI scripts.
"""

from __future__ import annotations

from typing import Dict, List

from .base import ThetaStarAnsatz
from .example_minimal import ExampleMinimalAnsatz
from .theta_star_delta_only import ThetaStarDeltaOnlyAnsatz
from .theta_star_v1 import ThetaStarV1Ansatz
from .theta_star_v2 import ThetaStarV2Ansatz

# Internal registry mapping string names to ansatz classes.
_REGISTRY: Dict[str, type[ThetaStarAnsatz]] = {
    "example_minimal": ExampleMinimalAnsatz,
    "theta_star_delta_only": ThetaStarDeltaOnlyAnsatz,
    "theta_star_v1": ThetaStarV1Ansatz,
    "theta_star_v2": ThetaStarV2Ansatz,
}

# Public alias (if someone imports ANSATZ_REGISTRY directly).
ANSATZ_REGISTRY = _REGISTRY


def available_ansatze() -> List[str]:
    """Return the list of registered ansatz names."""
    return sorted(_REGISTRY.keys())


def get_ansatz(name: str) -> ThetaStarAnsatz:
    """
    Instantiate an ansatz by name.
    """
    key = name.strip()
    if key not in _REGISTRY:
        raise KeyError(f"Unknown ansatz {name!r}. Known: {sorted(_REGISTRY)}")
    return _REGISTRY[key]()  # type: ignore[call-arg]