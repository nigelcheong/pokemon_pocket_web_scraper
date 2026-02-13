from __future__ import annotations

from pathlib import Path
from typing import List, Dict
import pandas as pd

PROCESSED_DIR = Path("data") / "processed"
OUT_PATH = PROCESSED_DIR / "decks_basic.csv"

def save_csv(rows: List[Dict], path: Path = OUT_PATH) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)

    return path