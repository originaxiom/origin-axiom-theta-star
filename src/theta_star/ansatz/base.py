"""
Base interfaces for theta* ansatz models.

An ansatz is responsible for mapping a small set of free parameters
(e.g. theta_star and a few nuisances) to predictions for CKM / PMNS
observables that can be compared against the targets defined in
``theta_star.constants``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping, Sequence, Tuple

from ..constants import PMNSOrdering


ParamDict = Dict[str, float]


@dataclass
class ThetaStarAnsatz:
    """
    Minimal interface for a theta* ansatz.

    Subclasses are expected to:

    - define ``name`` and ``param_names``
    - implement ``param_bounds``
    - implement ``predict_pmns`` and ``predict_ckm``

    We deliberately keep this as a lightweight dataclass instead of an
    abstract base class so that simple ansatz implementations stay easy
    to read and instantiate.
    """

    name: str

    # ordered list of parameter names; these become column names in
    # result tables as ``p_<name>``.
    param_names: Sequence[str]

    def param_bounds(self, ordering: PMNSOrdering = "NO") -> Mapping[str, Tuple[float, float]]:
        """
        Return sampling bounds for each parameter.

        Parameters
        ----------
        ordering:
            PMNS mass ordering, propagated to ansatz logic if relevant.

        Returns
        -------
        Mapping[str, (low, high)]
            Inclusive lower / upper bounds for each parameter.
        """
        raise NotImplementedError

    # --- prediction methods -------------------------------------------------

    def predict_pmns(self, params: ParamDict, ordering: PMNSOrdering = "NO") -> Mapping[str, float]:
        """
        Predict PMNS observables given parameter values.

        Returns a mapping whose keys match those in
        ``theta_star.constants.get_pmns_targets(ordering)``.
        """
        raise NotImplementedError

    def predict_ckm(self, params: ParamDict) -> Mapping[str, float]:
        """
        Predict CKM observables given parameter values.

        Returns a mapping whose keys match those in
        ``theta_star.constants.CKM_TARGETS``.
        """
        raise NotImplementedError