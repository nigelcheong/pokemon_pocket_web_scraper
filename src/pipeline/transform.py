from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Dict

def add_snapshot_metadata(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Adds a snapshot timestamp so your dashboard can track changes over time.
    """
    snapshot_utc = datetime.now(timezone.utc).isoformat()

    out = []
    for r in rows:
        r2 = dict(r)
        r2["snapshot_utc"] = snapshot_utc
        out.append(r2)

    return out
