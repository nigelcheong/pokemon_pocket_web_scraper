from src.scraper.fetch import fetch_deck_html
from src.scraper.parse import parse_all_deck_formats
from src.pipeline.transform import add_snapshot_metadata
from src.pipeline.load import save_latest_snapshot_csv, save_sqlite

def main():
    print("--- Pokemon TCGP Web Scraper ---")
    user_input = input("Download HTML files? (y/n): ").strip().lower()
    if user_input == 'y':
        print("Downloading HTML files...")
        fetch_deck_html(save_raw=True)
        print("HTML files downloaded.")
    else:
        print("\n" + "=" * 30)
        print("Skipping HTML download. Using existing files.")

    print("\n" + "=" * 30)
    print("Parsing deck formats...")
    rows = parse_all_deck_formats()
    print(f"Parsed {len(rows)} deck rows.")

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
    print("--- Scraping complete ---")

if __name__ == "__main__":
    main()
