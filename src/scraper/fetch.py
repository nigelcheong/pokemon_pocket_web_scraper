from __future__ import annotations

from pathlib import Path
import requests
from typing import List, Dict

from src.config import DECK_FORMATS, RAW_DECK_DATA_DIR, RAW_MATCHUPS_DATA_DIR, URL

def fetch_deck_html(save_raw: bool = True) -> str:
    """
    Downloads the decks page HTML for each deck format and returns it as a string.
    Optionally saves the raw HTML to separate files for each deck format.
    """
    RAW_DECK_DATA_DIR.mkdir(parents=True, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; educational scraper)"
    }

    deck_html_combined = ""

    for deck_format in DECK_FORMATS:
        format_url = f"{URL}&set={deck_format}"
        resp = requests.get(format_url, headers=headers, timeout=30)
        resp.raise_for_status()

        html = resp.text
        deck_html_combined += html

        if save_raw:
            format_file_path = RAW_DECK_DATA_DIR / f"raw_decks_pocket_{deck_format}.html"
            format_file_path.write_text(html, encoding="utf-8")

    return deck_html_combined

def fetch_matchups_html(deck_rows: List[Dict[str, str]]) -> List[str]:
    """
    Takes deck_rows from parse_all_deck_formats, extracts URLs, inserts '/matchups/' before '?game',
    and prints the first 10 modified URLs for validation.
    Returns the modified URLs.
    """
    urls = []
    RAW_MATCHUPS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; educational scraper)"
    }
    # Group rows by deck_format
    from collections import defaultdict
    format_rows = defaultdict(list)
    for row in deck_rows:
        deck_format = row.get('format', 'unknown')
        format_rows[deck_format].append(row)

    for deck_format, rows in format_rows.items():
        for idx, row in enumerate(rows[:10]):  # Only first 10 per format
            url = row.get('url')
            deck = row.get('deck', f'deck_{idx}')
            if url:
                # Insert '/matchups/' before '?game'
                if '?game' in url:
                    new_url = url.replace('?game', '/matchups/?game')
                else:
                    new_url = url
                urls.append(new_url)
                # Save HTML file for each matchup
                try:
                    resp = requests.get(new_url, headers=headers, timeout=30)
                    resp.raise_for_status()
                    # Sanitize filename
                    safe_deck = deck.replace('/', '_').replace(' ', '_')
                    filename = f"matchup_{safe_deck}_{deck_format}.html"
                    file_path = RAW_MATCHUPS_DATA_DIR / filename
                    file_path.write_text(resp.text, encoding="utf-8")
                except Exception as e:
                    print(f"Failed to fetch/save {new_url}: {e}")
    print("First 10 matchups URLs:")
    for url in urls[:10]:
        print(url)
    return urls
