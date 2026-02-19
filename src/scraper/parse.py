from __future__ import annotations

import re
from pathlib import Path
from typing import List, Dict
from bs4 import BeautifulSoup

from src.config import DECK_FORMATS, RAW_DECK_DATA_DIR, RAW_MATCHUPS_DATA_DIR

BASE = "https://play.limitlesstcg.com"

# Matches: count, share%, score "W - L - T", win%
ROW_RE = re.compile(
    r"(?P<count>\d+)\s+"
    r"(?P<share>\d+(?:\.\d+)?)%\s+"
    r"(?P<wins>\d+)\s*-\s*(?P<losses>\d+)\s*-\s*(?P<ties>\d+)\s+"
    r"(?P<winpct>(?:\d+(?:\.\d+)?|NaN))%"  # Updated to match either a number or 'NaN'
)

MATCHUP_RE = re.compile(
    r"(?P<matches>\d+)\s+"
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
    deck_rows = []
    for r in rows:
        key = (r["deck"], r["url"])
        if key not in seen:
            seen.add(key)
            deck_rows.append(r)

    return deck_rows

def parse_all_decks() -> List[Dict[str, str]]:
    """
    Parses deck data from all deck format HTML files and returns combined results.
    Each row includes a 'format' field indicating the deck format (B2, B1a, etc).
    """
    all_rows: List[Dict] = []

    for deck_format in DECK_FORMATS:
        format_file_path = RAW_DECK_DATA_DIR / f"raw_decks_pocket_{deck_format}.html"
        
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

def parse_matchups_table(html):
    """
    Extracts data-name, data-matches, data-winrate, and the string from class='nowrap' from each matchup row in the HTML.
    Returns a list of dicts for each matchup row.
    """
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", class_="striped")
    if not table:
        return []

    rows = []
    for tr in table.find_all("tr"):
        # Only process rows with data-name, data-matches, and data-winrate attributes
        data_name = tr.get("data-name")
        data_matches = tr.get("data-matches")
        data_winrate = tr.get("data-winrate")
        nowrap_td = tr.find("td", class_="nowrap")
        nowrap_text = nowrap_td.get_text(strip=True) if nowrap_td else None

        if data_name and data_matches and data_winrate:
            rows.append({
                "opponent_deck": data_name,
                "count": data_matches,
                "win_pct": data_winrate,
                "score": nowrap_text
            })

    return rows

def parse_all_matchups() -> List[Dict[str, str]]:
    """
    Parses matchup data from all matchup HTML files and returns combined results.
    Each row includes a 'format' field indicating the deck format (B2, B1a, etc).
    """
    all_rows: List[Dict] = []

    for matchup_file in RAW_MATCHUPS_DATA_DIR.glob("matchup_*.html"):
        html = matchup_file.read_text(encoding="utf-8")
        file_rows = parse_matchups_table(html)

        # Extract deck_name and set from the file name
        # Example: matchup_Charizard_ex_Moltres_ex_A1a.html
        filename = matchup_file.stem  # removes .html
        parts = filename.split('_')
        if len(parts) >= 3:
            deck_name = '_'.join(parts[1:-1])
            set_name = parts[-1]
        else:
            deck_name = ''
            set_name = ''

        for row in file_rows:
            row['deck_name'] = deck_name
            row['set'] = set_name
            all_rows.append(row)

        # For validation, print the first 5 rows from each file
        print(f"Parsed {len(file_rows)} matchups from {matchup_file.name}. Sample:")
        for sample_row in file_rows[:5]:
            print(sample_row)

    return all_rows
