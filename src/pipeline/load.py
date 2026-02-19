from __future__ import annotations

from pathlib import Path
from typing import List, Dict
import sqlite3
import pandas as pd

from src.config import PROCESSED_DATA_DIR, LATEST_CSV_PATH, OUT_PATH, DB_PATH, MATCHUPS_CSV_PATH


def save_csv(rows: List[Dict], path: Path = OUT_PATH) -> Path:
    """
    Generic CSV saver (kept from your base).
    """
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    return path


def save_latest_snapshot_csv(rows: List[Dict], path: Path = LATEST_CSV_PATH) -> Path:
    """
    Power BI-friendly snapshot CSV.
    Overwrites each run so Power BI can refresh the same file path.
    """
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)

    # Keep columns stable and in a nice order if present
    preferred_order = ["snapshot_utc", "Deck", "Count", "Share (%)", "Score", "Win (%)", "url", "format", "deck_format_key"]
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
        "Deck ID": "deck_format_key",
        "Deck": "deck",
        "Count": "count",
        "Share (%)": "share_pct",
        "Score": "score",
        "Win (%)": "win_pct",
        "url": "url",
        "snapshot_utc": "snapshot_utc",
        "Format": "format",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    df.to_sql("deck_stats", conn, if_exists="append", index=False)
    conn.close()

    return DB_PATH

def save_matchups_csv(rows: List[Dict], path: Path = MATCHUPS_CSV_PATH) -> Path:
    """
    Save parsed matchup rows to a CSV file in the processed directory.
    Overwrites each run for easy downstream use.
    """
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)

    # Reorder columns so deck_name is first, followed by the rest in a logical order
    preferred_order = [
        "deck_name", "set", "opponent_deck", "count", "wins", "losses", "ties", "score", "win_pct"
    ]
    ordered_cols = [c for c in preferred_order if c in df.columns] + [c for c in df.columns if c not in preferred_order]
    df = df[ordered_cols]
    df.to_csv(path, index=False)
    return path
