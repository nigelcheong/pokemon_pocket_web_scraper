from __future__ import annotations

from pathlib import Path
import requests

from src.config import DECK_FORMATS, DATA_DIR

URL = "https://play.limitlesstcg.com/decks?game=pocket"

RAW_HTML_PATH = DATA_DIR / "raw" / "raw_decks_pocket.html"

def fetch_url(url: str, save_raw: bool = False, raw_name: str = "raw.html") -> str:
    """
    Fetches the given URL and returns the HTML as a string.
    Optionally saves the raw HTML to data/raw/<raw_name>.
    """
    from src.config import DATA_DIR
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; educational scraper)"
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    html = resp.text
    if save_raw:
        raw_path = DATA_DIR / "raw" / raw_name
        raw_path.write_text(html, encoding="utf-8")
    return html

def fetch_html(save_raw: bool = True) -> str:
    """
    Downloads the decks page HTML for each deck format and returns it as a string.
    Optionally saves the raw HTML to separate files for each deck format.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; educational scraper)"
    }

    html_combined = ""

    for deck_format in DECK_FORMATS:
        format_url = f"{URL}&set={deck_format}"
        resp = requests.get(format_url, headers=headers, timeout=30)
        resp.raise_for_status()

        html = resp.text
        html_combined += html

        if save_raw:
            format_file_path = DATA_DIR / "raw" / f"raw_decks_pocket_{deck_format}.html"
            format_file_path.write_text(html, encoding="utf-8")

    return html_combined
