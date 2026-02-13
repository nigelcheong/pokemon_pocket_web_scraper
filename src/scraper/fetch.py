from __future__ import annotations

from pathlib import Path
import requests

URL = "https://play.limitlesstcg.com/decks?game=pocket"

DATA_DIR = Path("data")
RAW_HTML_PATH = DATA_DIR / "raw_decks_pocket.html"

def fetch_html(save_raw: bool = True) -> str:
    """
    Downloads the decks page HTML and returns it as a string.
    Optionally saves the raw HTML to data/raw_decks_pocket.html for debugging.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; educational scraper)"
    }

    resp = requests.get(URL, headers=headers, timeout=30)
    resp.raise_for_status()

    html = resp.text

    if save_raw:
        RAW_HTML_PATH.write_text(html, encoding="utf-8")

    return html