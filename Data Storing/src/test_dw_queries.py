import sys
sys.path.append('Data Storing/src')
import connect_db

conn = connect_db.get_connection()
cur = conn.cursor()
cur.execute("SET search_path TO ck3_dw, public;")

queries = [
    ("Query 1: Top 5 Counties Per Development", """
        SELECT year, county_name, development 
        FROM (
            SELECT 
                dy.year,
                dt.name AS county_name,
                f.development,
                ROW_NUMBER() OVER (PARTITION BY f.year ORDER BY f.development DESC) AS rn
            FROM fact_title_snapshot f
            JOIN dim_title dt ON dt.title_id = f.title_id
            JOIN dim_year dy ON dy.year = f.year
            WHERE f.tier = 'county' AND f.development IS NOT NULL
        ) ranked
        WHERE rn <= 5
        ORDER BY year, development DESC;
    """),
    ("Query 2: Top Empires by Sub-Counties & Sub-Duchies", """
        SELECT dy.year, dy.era_name, dt.name AS empire_name, f.sub_counties, f.sub_duchies, f.sub_kingdoms
        FROM fact_title_snapshot f
        JOIN dim_year dy ON f.year = dy.year 
        JOIN dim_title dt ON dt.title_id = f.title_id
        WHERE f.tier = 'empire'
        ORDER BY f.year, f.sub_counties DESC, f.sub_duchies DESC
        LIMIT 10;
    """),
    ("Query 3: Culture & Religion Diversity in Kingdoms", """
        SELECT dy.year, dt.name AS kingdom_name, COUNT(DISTINCT f.culture_id) AS num_of_dif_culture, COUNT(DISTINCT f.religion_id) AS num_of_dif_religion, COUNT(*) AS num_of_counties
        FROM fact_title_snapshot f
        JOIN dim_year dy ON dy.year = f.year
        JOIN dim_title dt ON dt.title_id = f.kingdom_id 
        WHERE f.tier = 'county'
        GROUP BY dy.year, dt.name
        ORDER BY num_of_dif_culture DESC, num_of_dif_religion DESC
        LIMIT 10;
    """),
    ("Query 4: Historical Development Growth (867 vs 1178)", """
        SELECT dt.name AS title_name, dt.tier, f867.development AS dev_867, f1178.development AS dev_1178, (f1178.development - f867.development) AS pertumbuhan
        FROM fact_title_snapshot f867
        JOIN fact_title_snapshot f1178 ON f1178.title_id = f867.title_id AND f1178.year = 1178
        JOIN dim_title dt ON dt.title_id = f867.title_id
        WHERE f867.year = 867 AND f867.development IS NOT NULL AND f1178.development IS NOT NULL
        ORDER BY pertumbuhan DESC
        LIMIT 10;
    """)
]

for title, sql in queries:
    print("=" * 60)
    print(title)
    print("=" * 60)
    cur.execute(sql)
    rows = cur.fetchall()
    for r in rows:
        print(r)
    print()

conn.close()
