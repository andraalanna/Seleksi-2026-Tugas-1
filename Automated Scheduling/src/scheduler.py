from pathlib import Path
import sys
from datetime import datetime

base_dir = Path(__file__).resolve().parents[2]

log_dir = base_dir / "Automated Scheduling" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file_path = log_dir / "scheduler.log"

def log_print(message):
    print(message)
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

sys.path.append(str(base_dir / "Data Scraping" / "src"))
sys.path.append(str(base_dir / "Data Storing" / "src"))

from scraper import scrape_one
from cleaner import clean_one
from import_data import main as import_all_data
from connect_db import get_connection
from scraper_history import fetch_all_histories

PAGE_MAP = {
    'counties': 'county',
    'duchies': 'duchy',
    'kingdoms': 'kingdom',
    'empires': 'empire',
    'hegemonies': 'hegemony'
}

if __name__ == "__main__":
    conn = get_connection()
    cur = conn.cursor()
    log_print("Starting scheduler run...")
    results = fetch_all_histories()

    pages = ['counties', 'duchies', 'kingdoms', 'empires', 'hegemonies']

    query_insert = """
    INSERT INTO log (page_name, last_checked, last_update, status)
    VALUES (%s, %s, %s, %s);
    """

    for page in pages:
        db_enum_page = PAGE_MAP[page]
        query_select = "SELECT last_update FROM log WHERE page_name = %s ORDER BY id DESC LIMIT 1;"
        cur.execute(query_select, (db_enum_page,))
        row = cur.fetchone()

        wiki_time = results.get(page)

        if row and row[0]:
            db_time = row[0].strftime('%Y-%m-%d %H:%M:%S')
        else:
            db_time = None

        if db_time is None or str(wiki_time) != str(db_time):
            log_print(f"Change detected for {page}. Running scraper...")
            scrape_one(page)
            clean_one(page)
            import_all_data()
            cur.execute(query_insert, (db_enum_page, datetime.now(), wiki_time, "UPDATED"))
            conn.commit()
            log_print(f"Log UPDATED saved for {page}")
        else:
            log_print(f"No change detected for {page}. Skipping scrape.")
            cur.execute(query_insert, (db_enum_page, datetime.now(), wiki_time, "NOT CHANGED"))
            conn.commit()

    cur.close()
    conn.close()
    log_print("Scheduler run finished successfully.")