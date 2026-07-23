
-- KASUS 1: Hierarchical Multi-Level Join (County ke Empire)
-- Fungsi: Mencari seluruh county de jure di bawah Empire 'e_britannia' pada tahun 1066.

EXPLAIN ANALYZE
SELECT t_county.name AS county_name
FROM title_snapshot ts_county
JOIN title t_county ON t_county.title_id = ts_county.title_id AND t_county.tier = 'county'
JOIN title_snapshot ts_duchy ON ts_duchy.title_id = ts_county.parent_title_id AND ts_duchy.year = ts_county.year
JOIN title_snapshot ts_kingdom ON ts_kingdom.title_id = ts_duchy.parent_title_id AND ts_kingdom.year = ts_county.year
WHERE ts_kingdom.parent_title_id = 'e_britannia' AND ts_county.year = 1066;

-- Indeks komposit B-Tree dibuat pada kolom (parent_title_id, year).
CREATE INDEX IF NOT EXISTS idx_snapshot_parent_year ON title_snapshot (parent_title_id, year);



-- KASUS 2: Text Search Nama Alternatif (Pencarian Substring)
-- Fungsi: Mencari nama gelar alternatif yang mengandung kata kunci substring '%bryn%'.

EXPLAIN ANALYZE
SELECT *
FROM alt_name
WHERE alt_name ILIKE '%bryn%';

-- Ekstensi pg_trgm memecah teks menjadi potongan 3 karakter (trigram).
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX IF NOT EXISTS idx_altname_trgm ON alt_name USING gin (alt_name gin_trgm_ops);

SET enable_seqscan = off;
EXPLAIN ANALYZE
SELECT *
FROM alt_name
WHERE alt_name ILIKE '%bryn%';
SET enable_seqscan = on;


-- KASUS 3: Agregasi Budaya dan Agama per Kingdom
-- Fungsi: Menghitung variasi jumlah budaya, agama, dan county per kingdom pada tahun 1178.

EXPLAIN ANALYZE
SELECT 
    ts_county.year,
    t_kingdom.name AS kingdom_name,
    COUNT(DISTINCT ts_county.culture_id) AS num_of_dif_culture,
    COUNT(DISTINCT ts_county.religion_id) AS num_of_dif_religion,
    COUNT(*) AS num_of_counties
FROM title_snapshot ts_county
JOIN title t_county ON t_county.title_id = ts_county.title_id AND t_county.tier = 'county'
JOIN title_snapshot ts_duchy ON ts_duchy.title_id = ts_county.parent_title_id AND ts_duchy.year = ts_county.year
JOIN title t_kingdom ON t_kingdom.title_id = ts_duchy.parent_title_id
WHERE ts_county.year = 1178
GROUP BY ts_county.year, t_kingdom.name
ORDER BY num_of_dif_culture DESC, num_of_dif_religion DESC
LIMIT 10;

-- Kolom 'year' digunakan dalam klausa WHERE untuk memfilter snapshot tahun tertentu.
CREATE INDEX IF NOT EXISTS idx_snapshot_year ON title_snapshot (year);

