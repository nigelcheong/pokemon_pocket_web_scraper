from __future__ import annotations

from typing import List, Dict
from bs4 import BeautifulSoup

BASE = "https://play.limitlesstcg.com"

def parse_deck_links(html: str) -> List[Dict[str, str]]:
    """
    Extracts a basic list of deck archetype names and their URLs.
    This is intentionally simple as a first step.
    """
    soup = BeautifulSoup(html, "lxml")

    rows = []
    for a in soup.select('a[href^="/decks/"]'):
        name = a.get_text(strip=True)
        href = a.get("href", "").strip()

        if not name or not href:
            continue

        rows.append({
            "archetype": name,
            "url": BASE + href
        })

    # Remove duplicates while preserving order
    seen = set()
    unique_rows = []
    for r in rows:
        key = (r["archetype"], r["url"])
        if key not in seen:
            seen.add(key)
            unique_rows.append(r)

    return unique_rows