import cloudscraper
from bs4 import BeautifulSoup
import time
import json

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) (Basis Data/Angelina Andra Alanna/13524079@std.stei.itb.ac.id)"}

def fetch(url):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, headers=headers)
        print(f"Fetched {url} - Status Code: {response.status_code}")
        response.raise_for_status()
        time.sleep(15)  # https://ck3.paradoxwikis.com/robots.txt -> Crawl-delay: 15
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Request failed: {e}")
        return None


def parse_table_raw(soup):
    if not soup:
        return []
    table = soup.find('table', class_='wikitable')
    if not table:
        print("Table not found!")
        return []
    
    all_rows = []
    for row in table.find_all('tr'):
        columns = row.find_all(['th', 'td'])
        row_data = []
        for col in columns:
            links = col.find_all('li')
            if links:
                cell_items = []
                for link in links:
                    cell_items.append(link.get_text(strip=True))
                row_data.append(cell_items)
            else:
                row_data.append(col.get_text(strip=True))
        all_rows.append(row_data) 
    return all_rows

def map_row(header,row):
    return dict(zip(header, row))

if __name__ == "__main__":
    test_url = "https://ck3.paradoxwikis.com/List_of_hegemonies"
    soup = fetch(test_url)
    if soup:
        print("Sukses! Otw Print Data Per Row")
        raw_rows = parse_table_raw(soup)
        # for row in raw_rows:
        #     for i, value in enumerate(row):
        #         print(i, value)
        #     print('---------------------------------------------')
        # print(f"Jumlah baris: {len(raw_rows)}")
        header_row = raw_rows[0]
        data_rows = raw_rows[1:]
        header_clean  = [h.lower().replace(' ', '_') for h in header_row]
        data = []
        for row in data_rows:
            data.append(map_row(header_clean, row))
        
        for d in data:
            print(d)
            
        output_path = "Data Scraping/data/hegemonies.json"
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"\nSukses! Data berhasil disimpan ke: {output_path}")

    else:
        print("gagal")
    