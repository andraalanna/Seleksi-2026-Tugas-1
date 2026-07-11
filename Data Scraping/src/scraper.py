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
        # print(f"Fetched {url} - Status Code: {response.status_code}")
        response.raise_for_status()
        time.sleep(15)  # https://ck3.paradoxwikis.com/robots.txt -> Crawl-delay: 15
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Request failed: {e}")
        return None

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
    headers_clean = []
    for c in range(tot_col):
        parent = grid[0][c].lower()
        if (len(grid)>1):
            child = grid[1][c].lower()
            if(parent!= child):
                headers_clean.append(f"{parent}_{child}")
            else:
                headers_clean.append(f"{parent}")
        else:
            headers_clean.append(f"{parent}")
    return headers_clean

def parse_table(table):
    parsed_table = []
    col_headers = parse_headers(table)
    for tr in table.find_all('tr'):
        columns = tr.find_all('td')
        row_data = []
        for col in columns:
            items = (list(col.stripped_strings))
            if not items:
                row_data.append("")
            elif len(items) == 1:
                row_data.append(items[0])
            else:
                row_data.append(items)

        if len(row_data) == len(col_headers):
            row_dict = dict(zip(col_headers, row_data))
            parsed_table.append(row_dict)
        
    return parsed_table

def save_to_json(data, path_output):
    with open(path_output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

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
            table = soup.find('table', class_='wikitable')
            result_data = parse_table(table)
            path_output = f"Data Scraping/data/{web['name']}.json"
            save_to_json(result_data, path_output)
