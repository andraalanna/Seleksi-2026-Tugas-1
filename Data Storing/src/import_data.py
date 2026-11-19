import json
import psycopg2
import random
from faker import Faker
from connect_db import get_connection

fake = Faker()

def to_snake_id(text):
    if not text:
        return None
    return text.strip().lower().replace(" ", "_").replace("-", "_")

def load_all_json():
    with open("Data Scraping/data/empires_cleaned.json", "r", encoding="utf-8") as f:
        empires = json.load(f)
    with open("Data Scraping/data/kingdoms_cleaned.json", "r", encoding="utf-8") as f:
        kingdoms = json.load(f)
    with open("Data Scraping/data/duchies_cleaned.json", "r", encoding="utf-8") as f:
        duchies = json.load(f)
    with open("Data Scraping/data/counties_cleaned.json", "r", encoding="utf-8") as f:
        counties = json.load(f)
    with open("Data Scraping/data/hegemonies_cleaned.json", "r", encoding="utf-8") as f:
        hegemonies = json.load(f)
    return empires, kingdoms, duchies, counties, hegemonies

def build_name_to_id_map(empires, kingdoms, duchies, counties, hegemonies):
    name_to_id = {}
    for item in empires:
        name_to_id[("empire", item["empire"].lower())] = item["id"]
    for item in kingdoms:
        name_to_id[("kingdom", item["kingdom"].lower())] = item["id"]
    for item in duchies:
        name_to_id[("duchy", item["duchy"].lower())] = item["id"]
    for item in counties:
        name_to_id[("county", item["county"].lower())] = item["id"]
    for item in hegemonies:
        h_id = f"h_{to_snake_id(item['hegemony'])}"
        name_to_id[("hegemony", item["hegemony"].lower())] = h_id
    return name_to_id

def insert_static_dimensions(cur, counties, duchies, empires, kingdoms):
    cultures = set()
    religions = set()
    buildings = set()

    for c in counties:
        for year in [867, 1066, 1178]:
            cult = c.get(f"culture_{year}")
            relg = c.get(f"religion_{year}")
            if cult:
                cultures.add(cult)
            if relg:
                religions.add(relg)
        b_data = c.get("special_buildings")
        if b_data:
            b_list = b_data if isinstance(b_data, list) else [b_data]
            for b in b_list:
                buildings.add(b)
        for alt in c.get("alternative_names") or []:
            for cult in alt.get("culture") or []:
                cultures.add(cult)

    for d in duchies:
        b_data = d.get("special_buildings")
        if b_data:
            b_list = b_data if isinstance(b_data, list) else [b_data]
            for b in b_list:
                buildings.add(b)
        for alt in d.get("alternative_names") or []:
            for cult in alt.get("culture") or []:
                cultures.add(cult)

    for e in empires:
        for alt in e.get("alternative_names") or []:
            for cult in alt.get("culture") or []:
                cultures.add(cult)

    for k in kingdoms:
        for alt in k.get("alternative_names") or []:
            for cult in alt.get("culture") or []:
                cultures.add(cult)

    for cult in cultures:
        cur.execute(
            "INSERT INTO Culture (culture_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (to_snake_id(cult), cult)
        )

    for relg in religions:
        cur.execute(
            "INSERT INTO Religion (religion_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (to_snake_id(relg), relg)
        )

    for bld in buildings:
        cur.execute(
            "INSERT INTO Special_Building (building_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (to_snake_id(bld), bld)
        )

def insert_characters(cur, n_chars=150):
    char_ids = []
    for i in range(1, n_chars + 1):
        char_id = f"char_{i}"
        name = fake.name()
        birth = random.randint(800, 1150)
        death = birth + random.randint(20, 75)
        cur.execute(
            "INSERT INTO Character (character_id, name, birth_year, death_year) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;",
            (char_id, name, birth, death)
        )
        char_ids.append(char_id)
    return char_ids

def insert_titles_and_subclasses(cur, empires, kingdoms, duchies, counties, hegemonies, name_to_id):
    for item in empires:
        cur.execute(
            "INSERT INTO Title (title_id, name, tier) VALUES (%s, %s, %s) ON CONFLICT (title_id) DO UPDATE SET name = EXCLUDED.name, tier = EXCLUDED.tier;",
            (item["id"], item["empire"], "empire")
        )
        cur.execute(
            "INSERT INTO Empire (title_id, special_requirements, ai_requirements) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
            (item["id"], item.get("special_requirements"), item.get("ai_requirements"))
        )

    for item in kingdoms:
        cur.execute(
            "INSERT INTO Title (title_id, name, tier) VALUES (%s, %s, %s) ON CONFLICT (title_id) DO UPDATE SET name = EXCLUDED.name, tier = EXCLUDED.tier;",
            (item["id"], item["kingdom"], "kingdom")
        )
        cur.execute(
            "INSERT INTO Kingdom (title_id, special_requirements, ai_requirements) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
            (item["id"], item.get("special_requirements"), item.get("ai_requirements"))
        )

    for item in duchies:
        cur.execute(
            "INSERT INTO Title (title_id, name, tier) VALUES (%s, %s, %s) ON CONFLICT (title_id) DO UPDATE SET name = EXCLUDED.name, tier = EXCLUDED.tier;",
            (item["id"], item["duchy"], "duchy")
        )
        cur.execute(
            "INSERT INTO Duchy (title_id) VALUES (%s) ON CONFLICT DO NOTHING;",
            (item["id"],)
        )

    for item in counties:
        cur.execute(
            "INSERT INTO Title (title_id, name, tier) VALUES (%s, %s, %s) ON CONFLICT (title_id) DO UPDATE SET name = EXCLUDED.name, tier = EXCLUDED.tier;",
            (item["id"], item["county"], "county")
        )
        cur.execute(
            "INSERT INTO County (title_id, baronies_count) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (item["id"], item.get("baronies"))
        )

    for item in hegemonies:
        h_id = name_to_id[("hegemony", item["hegemony"].lower())]
        cur.execute(
            "INSERT INTO Title (title_id, name, tier) VALUES (%s, %s, %s) ON CONFLICT (title_id) DO UPDATE SET name = EXCLUDED.name, tier = EXCLUDED.tier;",
            (h_id, item["hegemony"], "hegemony")
        )
        cur.execute(
            "INSERT INTO Hegemony (title_id, decision, notes) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
            (h_id, item.get("decision"), item.get("notes"))
        )
        for emp_name in item.get("empires", []):
            emp_id = name_to_id.get(("empire", emp_name.lower()))
            if emp_id:
                cur.execute(
                    "INSERT INTO Hegemony_Empire (hegemony_id, empire_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
                    (h_id, emp_id)
                )

def insert_alternative_names(cur, item, name_to_id):
    alt_names = item.get("alternative_names")
    if not alt_names:
        return
    title_id = item["id"]
    for alt in alt_names:
        alt_name = alt.get("name")
        year = alt.get("year")
        cur.execute(
            "INSERT INTO Alt_Name (title_id, alt_name, year) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
            (title_id, alt_name, year)
        )
        cultures = alt.get("culture", [])
        if cultures:
            for c_name in cultures:
                c_id = to_snake_id(c_name)
                cur.execute(
                    "INSERT INTO Alt_Name_Culture (title_id, alt_name, culture_id) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
                    (title_id, alt_name, c_id)
                )

def insert_special_buildings_links(cur, item):
    b_data = item.get("special_buildings")
    if not b_data:
        return
    title_id = item["id"]
    b_list = b_data if isinstance(b_data, list) else [b_data]
    for b in b_list:
        cur.execute(
            "INSERT INTO Title_Building (title_id, building_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (title_id, to_snake_id(b))
        )

def insert_snapshots(cur, empires, kingdoms, duchies, counties, name_to_id, char_ids):
    for item in empires:
        title_id = item["id"]
        insert_alternative_names(cur, item, name_to_id)
        for year in [867, 1066, 1178]:
            ruler = random.choice(char_ids)
            sub_k = item.get(f"kingdoms_{year}", 0)
            sub_d = item.get(f"duchies_{year}", 0)
            sub_c = item.get(f"counties_{year}", 0)
            cur.execute(
                """
                INSERT INTO Title_Snapshot (
                    title_id, year, parent_title_id, culture_id, religion_id, ruler_id,
                    development, sub_kingdoms, sub_duchies, sub_counties, sub_baronies
                ) VALUES (%s, %s, NULL, NULL, NULL, %s, NULL, %s, %s, %s, 0)
                ON CONFLICT (title_id, year) DO NOTHING;
                """,
                (title_id, year, ruler, sub_k, sub_d, sub_c)
            )

    for item in kingdoms:
        title_id = item["id"]
        insert_alternative_names(cur, item, name_to_id)
        for year in [867, 1066, 1178]:
            parent_name = item.get(f"empire_{year}")
            parent_id = name_to_id.get(("empire", parent_name.lower())) if parent_name else None
            ruler = random.choice(char_ids)
            sub_d = item.get(f"duchies_{year}", 0)
            sub_c = item.get(f"counties_{year}", 0)
            cur.execute(
                """
                INSERT INTO Title_Snapshot (
                    title_id, year, parent_title_id, culture_id, religion_id, ruler_id,
                    development, sub_kingdoms, sub_duchies, sub_counties, sub_baronies
                ) VALUES (%s, %s, %s, NULL, NULL, %s, NULL, 0, %s, %s, 0)
                ON CONFLICT (title_id, year) DO NOTHING;
                """,
                (title_id, year, parent_id, ruler, sub_d, sub_c)
            )

    for item in duchies:
        title_id = item["id"]
        insert_alternative_names(cur, item, name_to_id)
        insert_special_buildings_links(cur, item)
        for year in [867, 1066, 1178]:
            parent_name = item.get(f"kingdom_{year}")
            parent_id = name_to_id.get(("kingdom", parent_name.lower())) if parent_name else None
            ruler = random.choice(char_ids)
            dev = item.get(f"average_development_{year}")
            sub_c = item.get("counties", 0)
            sub_b = item.get("baronies", 0)
            cur.execute(
                """
                INSERT INTO Title_Snapshot (
                    title_id, year, parent_title_id, culture_id, religion_id, ruler_id,
                    development, sub_kingdoms, sub_duchies, sub_counties, sub_baronies
                ) VALUES (%s, %s, %s, NULL, NULL, %s, %s, 0, 0, %s, %s)
                ON CONFLICT (title_id, year) DO NOTHING;
                """,
                (title_id, year, parent_id, ruler, dev, sub_c, sub_b)
            )

    for item in counties:
        title_id = item["id"]
        insert_alternative_names(cur, item, name_to_id)
        insert_special_buildings_links(cur, item)
        for year in [867, 1066, 1178]:
            parent_name = item.get("duchy")
            parent_id = name_to_id.get(("duchy", parent_name.lower())) if parent_name else None
            ruler = random.choice(char_ids)
            dev = item.get(f"development_{year}")
            cult_id = to_snake_id(item.get(f"culture_{year}"))
            relg_id = to_snake_id(item.get(f"religion_{year}"))
            sub_b = item.get("baronies", 0)
            cur.execute(
                """
                INSERT INTO Title_Snapshot (
                    title_id, year, parent_title_id, culture_id, religion_id, ruler_id,
                    development, sub_kingdoms, sub_duchies, sub_counties, sub_baronies
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, 0, 0, 0, %s)
                ON CONFLICT (title_id, year) DO NOTHING;
                """,
                (title_id, year, parent_id, cult_id, relg_id, ruler, dev, sub_b)
            )

def main():
    empires, kingdoms, duchies, counties, hegemonies = load_all_json()
    name_to_id = build_name_to_id_map(empires, kingdoms, duchies, counties, hegemonies)

    conn = get_connection()
    cur = conn.cursor()

    try:
        insert_static_dimensions(cur, counties, duchies, empires, kingdoms)
        char_ids = insert_characters(cur, 150)
        insert_titles_and_subclasses(cur, empires, kingdoms, duchies, counties, hegemonies, name_to_id)
        insert_snapshots(cur, empires, kingdoms, duchies, counties, name_to_id, char_ids)
        conn.commit()
        print("Data successfully loaded into the database.")
    except Exception as e:
        conn.rollback()
        print("Failed to load data. Transaction rolled back:", e)
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
