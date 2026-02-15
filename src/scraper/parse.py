from __future__ import annotations

import re
from pathlib import Path
from typing import List, Dict
from bs4 import BeautifulSoup

from src.config import DECK_FORMATS, DATA_DIR

BASE = "https://play.limitlesstcg.com"

# Matches: count, share%, score "W - L - T", win%
ROW_RE = re.compile(
    r"(?P<count>\d+)\s+"
    r"(?P<share>\d+(?:\.\d+)?)%\s+"
    r"(?P<wins>\d+)\s*-\s*(?P<losses>\d+)\s*-\s*(?P<ties>\d+)\s+"
    r"(?P<winpct>(?:\d+(?:\.\d+)?|NaN))%"  # Updated to match either a number or 'NaN'
)

def parse_deck_table(html: str) -> List[Dict[str, str]]:
    """
    Extracts Deck, Count, Share (%), Score, Win (%) from the page HTML.
    """
    soup = BeautifulSoup(html, "lxml")
    rows: List[Dict] = []

    for container in soup.select('tr, div, li'):
        a = container.select_one('a[href^="/decks/"]')
        if a is None:
            continue
        
        deck = a.get_text(strip=True)
        href = a.get("href", "").strip()

        if not deck or not href:
            continue

        row_text = container.get_text(" ", strip=True)

        m = ROW_RE.search(row_text)
        if not m:
            continue

        count = int(m.group("count"))
        share = float(m.group("share"))
        wins = int(m.group("wins"))
        losses = int(m.group("losses"))
        ties = int(m.group("ties"))
        
        # Check for 'NaN%' in winpct
        winpct_str = m.group("winpct")
        winpct = float(winpct_str) if winpct_str != 'NaN' else 0.0

        rows.append({
            "deck": deck,
            "count": count,
            "share": share,
            "score": f"{wins} - {losses} - {ties}",
            "winpct": winpct,
            "url": BASE + href
        })

    # Remove duplicates while preserving order
    seen = set()
    unique_rows = []
    for r in rows:
        key = (r["deck"], r["url"])
        if key not in seen:
            seen.add(key)
            unique_rows.append(r)

    return unique_rows

def parse_all_deck_formats() -> List[Dict[str, str]]:
    """
    Parses deck data from all deck format HTML files and returns combined results.
    Each row includes a 'format' field indicating the deck format (B2, B1a, etc).
    """
    all_rows: List[Dict] = []

    for deck_format in DECK_FORMATS:
        format_file_path = DATA_DIR / "raw" / f"raw_decks_pocket_{deck_format}.html"
        
        if not format_file_path.exists():
            continue

        html = format_file_path.read_text(encoding="utf-8")
        rows = parse_deck_table(html)
        
        # Add format and primary key field to each row
        for row in rows:
            row["format"] = deck_format
            row["deck_format_key"] = f"{row['deck']}|{deck_format}"
        
        all_rows.extend(rows)

    return all_rows
