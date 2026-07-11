import cloudscraper
from bs4 import BeautifulSoup
import time
import json
from pprint import pprint

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

def parse_headers(table):
    header_rows = [row for row in table.find_all('tr') if row.find('th')]
    tot_col = 0
    for th in header_rows[0].find_all('th'):
        tot_col += int(th.get('colspan', 1))
    grid = [[None] * tot_col for _ in range(len(header_rows))]

    for r_idx, row in enumerate(header_rows):
        c_idx = 0
        for th in row.find_all('th'):
            while c_idx < tot_col and grid[r_idx][c_idx] is not None:
                c_idx +=1
            text = th.get_text(strip=True)
            colspan = int(th.get('colspan', 1))
            rowspan = int(th.get('rowspan', 1))
            for r_offset in range(rowspan):
                for c_offset in range(colspan):
                    if r_idx + r_offset < len(header_rows):
                        grid[r_idx + r_offset][c_idx + c_offset] = text
            c_idx += colspan
    return grid

                    
if __name__ == "__main__":
    wesbite_to_scrape = [
        {"url": "https://ck3.paradoxwikis.com/List_of_hegemonies", "name": "hegemonies"},
        {"url": "https://ck3.paradoxwikis.com/List_of_duchies", "name": "duchies"},
        {"url": "https://ck3.paradoxwikis.com/List_of_counties", "name": "counties"},
        {"url": "https://ck3.paradoxwikis.com/List_of_kingdoms", "name": "kingdoms"},
        {"url": "https://ck3.paradoxwikis.com/List_of_empires", "name": "empires"},
    ]
    for web in wesbite_to_scrape:
        soup = fetch(web['url'])
        if soup:
            print("Sukses! Otw Print Data Per Row")
            table = soup.find('table', class_='wikitable')
            grid = parse_headers(table)
            pprint(grid)
