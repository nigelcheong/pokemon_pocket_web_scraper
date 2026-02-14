from __future__ import annotations

from pathlib import Path
from typing import List, Dict
import sqlite3
import pandas as pd

PROCESSED_DIR = Path("data") / "processed"

# "Latest snapshot" CSV for Power BI (overwrite each run)
LATEST_CSV_PATH = PROCESSED_DIR / "deck_stats_latest.csv"

# Optional: keep your original output too
OUT_PATH = PROCESSED_DIR / "decks_basic.csv"

DB_PATH = Path("data") / "app.db"


def save_csv(rows: List[Dict], path: Path = OUT_PATH) -> Path:
    """
    Generic CSV saver (kept from your base).
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    return path


def save_latest_snapshot_csv(rows: List[Dict], path: Path = LATEST_CSV_PATH) -> Path:
    """
    Power BI-friendly snapshot CSV.
    Overwrites each run so Power BI can refresh the same file path.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)

    # Keep columns stable and in a nice order if present
    preferred_order = ["snapshot_utc", "Deck", "Count", "Share (%)", "Score", "Win (%)", "url"]
    ordered_cols = [c for c in preferred_order if c in df.columns] + [c for c in df.columns if c not in preferred_order]
    df = df[ordered_cols]

    df.to_csv(path, index=False)
    return path


def save_sqlite(rows: List[Dict]) -> Path:
    """
    Save to SQLite for historical storage (optional for now).
    Uses DB-friendly column names.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    df = pd.DataFrame(rows)

    # Map from your CSV/table headers to DB-friendly column names
    rename_map = {
        "Deck": "deck",
        "Count": "count",
        "Share (%)": "share_pct",
        "Score": "score",
        "Win (%)": "win_pct",
        "url": "url",
        "snapshot_utc": "snapshot_utc",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    df.to_sql("deck_stats", conn, if_exists="append", index=False)
    conn.close()

    return DB_PATH
