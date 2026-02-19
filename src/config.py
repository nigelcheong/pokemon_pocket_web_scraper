from pathlib import Path

# Deck formats to scrape
DECK_FORMATS = ["B2", "B1a", "B1", "A4a", "A4", "A3b", "A3a", "A3", "A2b", "A2a", "A2","A1a", "A1"]

# Base URL for scraping
URL = "https://play.limitlesstcg.com/decks?game=pocket"

# Raw data paths
DATA_DIR = Path("data")
RAW_DATA_DIR = DATA_DIR / "raw"
RAW_DECK_DATA_DIR = RAW_DATA_DIR / "decks"
RAW_MATCHUPS_DATA_DIR = RAW_DATA_DIR / "matchups"

# Processed/output paths
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LATEST_CSV_PATH = PROCESSED_DATA_DIR / "deck_stats_latest.csv"
OUT_PATH = PROCESSED_DATA_DIR / "decks_basic.csv"
MATCHUPS_CSV_PATH = PROCESSED_DATA_DIR / "matchups_latest.csv"
DB_PATH = DATA_DIR / "app.db"