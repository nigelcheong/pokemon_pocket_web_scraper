from src.scraper.fetch import fetch_html
from src.scraper.parse import parse_deck_links 
from src.pipeline.transform import add_snapshot_metadata
from src.pipeline.load import save_csv

def main():
    html = fetch_html(save_raw=True)
    rows = parse_deck_links(html)
    rows = add_snapshot_metadata(rows)
    out_path = save_csv(rows)

    print(f"Saved {len(rows)} rows to {out_path}")

if __name__ == "__main__":
    main()