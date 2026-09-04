"""Every automated run writes its raw inputs here, gzipped, so bad months can be diagnosed."""
from __future__ import annotations

import gzip
import json
from datetime import datetime
from pathlib import Path

from harness.clock import stamp

RAW_ROOT = Path("data/raw")


def write(strategy: str, name: str, payload: bytes | str | dict | list, at: datetime, root: Path = RAW_ROOT) -> Path:
    d = root / strategy / at.strftime("%Y/%m/%d")
    d.mkdir(parents=True, exist_ok=True)
    if isinstance(payload, (dict, list)):
        payload = json.dumps(payload, separators=(",", ":")).encode()
    elif isinstance(payload, str):
        payload = payload.encode()
    p = d / f"{stamp(at)}_{name}.gz"
    with gzip.open(p, "wb") as f:
        f.write(payload)
    return p
