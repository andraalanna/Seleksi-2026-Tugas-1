-- Query 1 (Before indexing)
EXPLAIN ANALYZE
SELECT t_county.name AS county_name
FROM title_snapshot ts_county
JOIN title t_county ON t_county.title_id = ts_county.title_id AND t_county.tier = 'county'
JOIN title_snapshot ts_duchy ON ts_duchy.title_id = ts_county.parent_title_id AND ts_duchy.year = ts_county.year
JOIN title_snapshot ts_kingdom ON ts_kingdom.title_id = ts_duchy.parent_title_id AND ts_kingdom.year = ts_county.year
WHERE ts_kingdom.parent_title_id = 'e_britannia' AND ts_county.year = 1066;

-- Query Add Index
CREATE INDEX idx_snapshot_parent_year ON title_snapshot (parent_title_id, year);

CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_altname_trgm ON alt_name USING gin (alt_name gin_trgm_ops);