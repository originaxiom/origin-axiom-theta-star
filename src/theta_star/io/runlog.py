"""
runlog.py

Tiny run logging utilities.
Goal: every sweep/fit writes:
- run_id
- parameters (including ordering)
- git hash (if available)
- output paths
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


def git_head() -> Optional[str]:
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


def write_run_meta(path: Path, meta: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    meta2 = dict(meta)
    meta2.setdefault("timestamp_local", datetime.now().isoformat(timespec="seconds"))
    meta2.setdefault("git_head", git_head())

    # dataclass-safe
    for k, v in list(meta2.items()):
        if is_dataclass(v):
            meta2[k] = asdict(v)

    path.write_text(json.dumps(meta2, indent=2, sort_keys=True) + "\n")