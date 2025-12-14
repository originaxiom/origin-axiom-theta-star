"""
runlog.py

Standardized run metadata writer for all sweeps/optimizations.

We write a small JSON next to outputs so every artifact is reproducible:
- run_id
- timestamp
- git head
- argv
- params
- outputs
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


def _git_head() -> Optional[str]:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True,
        )
        return r.stdout.strip()
    except Exception:
        return None


def _jsonify(x: Any) -> Any:
    if is_dataclass(x):
        return asdict(x)
    if isinstance(x, Path):
        return str(x)
    if isinstance(x, dict):
        return {k: _jsonify(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
          tu     jsonif          tu     jsonif          tu     jsonif          tu    Pa          tu     jsonif          tu     jsonif          tu     jsonif   N                            un_i     un                 es  mp_          tu     jsonif          tim          on                    tu  :           tu                tu     jsonif          tu     jsofo          tu     jsonif     le          tu     jsonif),          tu     jsonif          tu  ine(          tu     jsonif         m.       ve          tu     jsonif               tu     jsonif          tu     ,
          tu     jsonif          t,
          tu     jsonif          t,
 
                      re                       e        Tr                      re      so                    =2                  + "\n")
