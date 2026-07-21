-- ==========================================
-- BONUS 3: QUERY OPTIMIZATION QUERIES
-- ==========================================

-- Query 1: Hierarchical Multi-Level Join
-- Kasus: Mencari semua county di bawah Empire tertentu (e_britannia) pada tahun 1066.

-- Index
CREATE INDEX IF NOT EXISTS idx_snapshot_parent_year ON title_snapshot (parent_title_id, year);

-- Query Execution Plan
EXPLAIN ANALYZE
SELECT t_county.name AS county_name
FROM title_snapshot ts_county
JOIN title t_county ON t_county.title_id = ts_county.title_id AND t_county.tier = 'county'
JOIN title_snapshot ts_duchy ON ts_duchy.title_id = ts_county.parent_title_id AND ts_duchy.year = ts_county.year
JOIN title_snapshot ts_kingdom ON ts_kingdom.title_id = ts_duchy.parent_title_id AND ts_kingdom.year = ts_county.year
WHERE ts_kingdom.parent_title_id = 'e_britannia' AND ts_county.year = 1066;


-- Query 2: Text Search di Nama Alternatif (Pattern Matching)
-- Kasus: Mencari title berdasarkan substring nama alternatif (alt_name ILIKE '%bryn%').

-- Extension
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Index
CREATE INDEX IF NOT EXISTS idx_altname_trgm ON alt_name USING gin (alt_name gin_trgm_ops);

-- Query Execution Plan (Default Planner)
EXPLAIN ANALYZE
SELECT *
FROM alt_name
WHERE alt_name ILIKE '%bryn%';

-- Validasi Teknis Indeks (Paksa Index Scan)
SET enable_seqscan = off;
EXPLAIN ANALYZE
SELECT *
FROM alt_name
WHERE alt_name ILIKE '%bryn%';
SET enable_seqscan = on;


-- Query 3: Agregasi Budaya dan Agama per Kingdom
-- Kasus: Menghitung jumlah variasi culture dan religion per kingdom pada tahun 1178.

-- Index
CREATE INDEX IF NOT EXISTS idx_snapshot_year ON title_snapshot (year);

-- Query Execution Plan
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
