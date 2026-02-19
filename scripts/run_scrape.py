from src.scraper.fetch import fetch_deck_html, fetch_matchups_html
from src.scraper.parse import parse_all_decks, parse_all_matchups, parse_matchups_table
from src.pipeline.transform import add_snapshot_metadata
from src.pipeline.load import save_latest_snapshot_csv, save_sqlite, save_matchups_csv
from src.config import DECK_FORMATS, URL

def main():
    print("--- Pokemon TCGP Web Scraper ---")

    # Download deck HTML files if user agrees
    user_input = input("Download Deck HTML files? (y/n): ").strip().lower()
    if user_input == 'y':
        print("Downloading Deck HTML files...")
        fetch_deck_html(save_raw=True)
        print("Deck HTML files downloaded.")
    else:
        print("\n" + "=" * 30)
        print("Skipping HTML download. Using existing files.")

    print("\n" + "=" * 30)

    print("Parsing deck formats...")
    rows = parse_all_decks()
    print(f"Parsed {len(rows)} deck rows.")

    print("\n" + "=" * 30)
    
    # Download matchup HTML files if user agrees
    user_input = input("Download Matchups HTML files? (y/n): ").strip().lower()
    if user_input == 'y':
        print("Downloading Matchups HTML files...")
        fetch_matchups_html(rows)
        print("Matchups HTML files downloaded.")
    else:
        print("\n" + "=" * 30)
        print("Skipping Matchups HTML download. Using existing files.")

    print("\n" + "=" * 30)
    print("Adding snapshot metadata...")
    rows = add_snapshot_metadata(rows)
    print("Snapshot metadata added.")

    print("\n" + "=" * 30)
    print("Saving CSV snapshot...")
    csv_path = save_latest_snapshot_csv(rows)
    print(f"Saved {len(rows)} rows to {csv_path}")

    print("\n" + "=" * 30)
    print("Saving to SQLite database...")
    db_path = save_sqlite(rows)
    print(f"Appended {len(rows)} rows to {db_path}")

    print("\n" + "=" * 30)
    print("Parsing matchup data...")
    matchups_rows = parse_all_matchups()
    print(f"Parsed {len(matchups_rows)} matchup rows.")

    print("\n" + "=" * 30)
    print("Saving matchup CSV...")
    matchups_csv_path = save_matchups_csv(matchups_rows)
    print(f"Saved {len(matchups_rows)} matchup rows to {matchups_csv_path}")

    print("\n" + "=" * 30)
    print("--- Scraping complete ---")

if __name__ == "__main__":
    main()
