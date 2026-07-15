import json
import re

def duplicate_buildings_fix(new_data2):
    for row in new_data2:
        buildings = row.get('special_buildings')
        if isinstance(buildings, list):
            unique = list(dict.fromkeys(buildings))
            if len(unique) == 1:
                row['special_buildings'] = unique[0]
            else:
                row['special_buildings'] = unique
    return new_data2

def alt_name_fix(new_data1):
    for row in new_data1:
        value = row.get('alternative_names')
        if not value:
            continue
        raw_list = value if isinstance(value, list) else [value]
        new_alt = []
        pat = r'([^(,]+)\s*\(([^()]+)\)'
        for item in raw_list:
            if isinstance(item, str):
                item = item.strip()
                if not item:
                    continue
                matches = re.findall(pat, item)
                if matches:
                    for name, inside in matches:
                        name = name.strip()
                        if inside.isdigit():
                            new_alt.append({'name': name, 'year': int(inside), 'culture': None})
                        else:
                            cultures = [c.strip() for c in inside.split(',')]
                            new_alt.append({'name': name, 'year': None, 'culture': cultures})
                else:
                    names = [n.strip() for n in item.split(',')]
                    for name in names:
                        if name:
                            new_alt.append({'name': name, 'year': None, 'culture': None})
            elif isinstance(item, dict):
                new_alt.append(item)
        if new_alt:
            row['alternative_names'] = new_alt
    return new_data1

        
def clean1(path_input, path_output):
    with open(path_input, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_data = []
    for row in data:
        new_row = {}
        for k, val in row.items():
            key = k.replace(" ", "_")
            new_row[key] = clean_value(val) if isinstance(val, str) else val
        new_data.append(new_row)
        
    new_data = alt_name_fix(new_data)
    new_data = duplicate_buildings_fix(new_data)
    
    with open(path_output, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)
    
def clean_value(v):
    if isinstance(v, str):
        v = v.strip()
        if v == "":
            return None
    try: 
        return int(v)
    except ValueError:
        return v
    

def clean2(path_input, path_output):
    with open(path_input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_data = []
    for row in data:
        notes = row.get('notes', '')
        if isinstance(notes, list): 
            row['notes'] = " ".join(row['notes'])
        new_data.append(row)
    
    with open(path_output, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)
    
if __name__ == "__main__":
    '''
    Counties, duchies, empires, Kingdoms
    (
        Cleaning Alternative Names Into Format : 
        (title, name, tahun, bahasa, budaya)
    )

    '''
    cleaning_1 = [
        {'name': 'counties'},
        {'name': 'duchies'},
        {'name': 'empires'},
        {'name': 'kingdoms'},
    ]

    for item in cleaning_1:
        path_input = f"Data Scraping/data/{item['name']}_raw.json"
        path_output = f"Data Scraping/data/{item['name']}_cleaned.json"
        clean1(path_input, path_output)

    

    # """
    # Hegemonies
    # (
    #     Cleaning Notes from array into string
    # )
    # """

    cleaning_2 = [{'name':'hegemonies'}]
    for item in cleaning_2:
        path_input = f"Data Scraping/data/{item['name']}_raw.json"
        path_output = f"Data Scraping/data/{item['name']}_cleaned.json"
        clean2(path_input, path_output)


    

