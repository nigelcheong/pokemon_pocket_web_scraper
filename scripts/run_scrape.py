from src.scraper.fetch import fetch_html
from src.scraper.parse import parse_deck_table
from src.pipeline.transform import add_snapshot_metadata
from src.pipeline.load import save_latest_snapshot_csv, save_sqlite


def main():
    html = fetch_html(save_raw=True)
    rows = parse_deck_table(html)
    rows = add_snapshot_metadata(rows)

    csv_path = save_latest_snapshot_csv(rows)
    db_path = save_sqlite(rows)

    print(f"Saved {len(rows)} rows to {csv_path}")
    print(f"Appended {len(rows)} rows to {db_path}")


if __name__ == "__main__":
    main()
