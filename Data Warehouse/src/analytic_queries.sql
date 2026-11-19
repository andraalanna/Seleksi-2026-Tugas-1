SET search_path to ck3_dw;

-- Query 1: Perspektif ekonomi
-- "County mana yang paling makmur di tiap start date?"

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
    WHERE f.tier = 'county' NAD f.development IS NOT NULL
) ranked
WHERE rn <= 5
ORDER BY year, development DESC;

-- Query 2: Perspektif ekspansi wilayah
-- "Empire mana yang punya wilayah kekuasan (duchies & counties) terbanyak di tiap start date?"
SELECT dy.year, dy.era_name, dt.name AS empire_name, f.sub_counties, f.sub_duchies, f.sub_kingdoms
FROM fact_title_snapshot f
JOIN dim_year dy ON f.year = dy.year 
JOIN dim_title dt ON dt.title_id = f.title_id
WHERE f.tier = 'empire'
ORDER BY f.year, f.sub_counties DESC, f.sub_duchies DESC
LIMIT 10;

-- Query 3: Perspektif budaya & agama
-- "Kingdom mana yang tipe penduduknya homogen (stabil = bagus buat pemula) vs bergam (sering muncul pemberontakan = cocok buat advanced player)"
SELECT dy.year, dt.name AS kingdom_name, COUNT(DISTINCT f.culture_id) AS num_of_dif_culture, COUNT(DISTINCT f.religion_id) AS num_of_dif_religion, COUNT(*) AS num_of_counties
FROM fact_title_snapshot f
JOIN dim_year dy ON dy.year = f.year
JOIN dim_title dt ON dt.title_id = f.kingdom_id 
WHERE f.tier = 'county'
GROUP BY dy.year, dt.name
ORDER BY num_of_dif_culture DESC, num_of_dif_religion DESC
LIMIT 10;

-- Query 4: Perspektif Historical Growth
-- "Title mana yang berkembang pesat dari awal"
SELECT dt.name AS title_name, dt.tier, f867.development  AS dev_867, f1178.development AS dev_1178, (f1178.development - f867.development) AS pertumbuhan
FROM fact_title_snapshot f867
JOIN fact_title_snapshot f1178 ON f1178.title_id = f867.title_id AND f1178.year = 1178
JOIN dim_title dt ON dt.title_id = f867.title_id
WHERE f867.year = 867 AND f867.development IS NOT NULLAND f1178.development IS NOT NULL
ORDER BY pertumbuhan DESC
LIMIT 10;