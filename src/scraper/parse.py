from __future__ import annotations

import re
from typing import List, Dict
from bs4 import BeautifulSoup

BASE = "https://play.limitlesstcg.com"

# Matches: count, share%, score "W - L - T", win%
ROW_RE = re.compile(
    r"(?P<count>\d+)\s+"
    r"(?P<share>\d+(?:\.\d+)?)%\s+"
    r"(?P<wins>\d+)\s*-\s*(?P<losses>\d+)\s*-\s*(?P<ties>\d+)\s+"
    r"(?P<winpct>\d+(?:\.\d+)?)%"
)

def parse_deck_table(html: str) -> List[Dict[str, str]]:
    """
    Extracts Deck, Count, Share (%), Score, Win (%) from the page HTML.
    """
    soup = BeautifulSoup(html, "lxml")
    rows: List[Dict] = []

    for a in soup.select('a[href^="/decks/"]'):
        deck = a.get_text(strip=True)
        href = a.get("href", "").strip()

        if not deck or not href:
            continue

        container = a.find_parent(["tr", "div", "li"])
        if container is None:
            container = a.parent
        
        row_text = container.get_text(" ", strip=True)

        m = ROW_RE.search(row_text)
        if not m:
            continue

        count = int(m.group("count"))
        share = float(m.group("share"))
        wins = int(m.group("wins"))
        losses = int(m.group("losses"))
        ties = int(m.group("ties"))
        winpct = float(m.group("winpct"))

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
