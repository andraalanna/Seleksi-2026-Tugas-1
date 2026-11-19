from pprint import pprint
from pathlib import Path
import sys

scraper_dir = Path(__file__).resolve().parents[2] / "Data Scraping" / "src"
sys.path.append(str(scraper_dir))

from scraper import fetch
from datetime import datetime

# 19:25, 11 July 2026 -> 

def fix_format(time):
    clean_time = time.replace('\u200e', '').strip()
    dt = datetime.strptime(clean_time, '%H:%M, %d %B %Y')
    time_stamp = dt.strftime('%Y-%m-%d %H:%M:%S')
    return time_stamp

def fetch_all_histories():
    history_to_scrape = [
        {"url": "https://ck3.paradoxwikis.com/index.php?title=List_of_hegemonies&action=history", "name": "hegemonies"},
        {"url": "https://ck3.paradoxwikis.com/index.php?title=List_of_duchies&action=history", "name": "duchies"},
        {"url": "https://ck3.paradoxwikis.com/index.php?title=List_of_counties&action=history", "name": "counties"},
        {"url": "https://ck3.paradoxwikis.com/index.php?title=List_of_kingdoms&action=history", "name": "kingdoms"},
        {"url": "https://ck3.paradoxwikis.com/index.php?title=List_of_empires&action=history", "name": "empires"},
        ]
    results = {}
    for his in history_to_scrape:
        soup = fetch(his['url'])

        if soup:
            date_element = soup.find('a', class_='mw-changeslist-date')
            if date_element:
                last_updated = date_element.text.strip()
                time_stamp = fix_format(last_updated)
                results[his['name']] = time_stamp
    return results

if __name__ == "__main__":
    print("Testing fetch_all_histories()...")
    data = fetch_all_histories()
    pprint(data)