from pathlib import Path

# Deck formats to scrape
DECK_FORMATS = ["B2", "B1a", "B1", "A4a", "A4", "A3b", "A3a", "A3", "A2b", "A2a", "A2","A1a", "A1"]

# Data directories
DATA_DIR = Path("data")
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
