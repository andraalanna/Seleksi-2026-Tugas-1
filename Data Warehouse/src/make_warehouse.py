import psycopg2.extras
from connect_db import get_connection

def create_dw_schema_and_tables(conn):
    """Buat schema ck3_dw, tabel dimensi (termasuk dim_year), tabel fakta, FK, dan indeks analitik."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE SCHEMA IF NOT EXISTS ck3_dw;

            -- 1. Dimensi Title
            CREATE TABLE IF NOT EXISTS ck3_dw.dim_title (
                title_id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                tier VARCHAR(50) NOT NULL
            );

            -- 2. Dimensi Year (Waktu & Era)
            CREATE TABLE IF NOT EXISTS ck3_dw.dim_year (
                year INT PRIMARY KEY,
                era_name VARCHAR(100) NOT NULL
            );

            -- 3. Dimensi Culture
            CREATE TABLE IF NOT EXISTS ck3_dw.dim_culture (
                culture_id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );

            -- 4. Dimensi Religion
            CREATE TABLE IF NOT EXISTS ck3_dw.dim_religion (
                religion_id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );

            -- 5. fact_title_snapshot
            CREATE TABLE IF NOT EXISTS ck3_dw.fact_title_snapshot (
                title_id VARCHAR(50) NOT NULL,
                year INT NOT NULL,
                tier VARCHAR(50),
                duchy_id VARCHAR(50),
                kingdom_id VARCHAR(50),
                empire_id VARCHAR(50),
                hegemony_id VARCHAR(50),
                culture_id VARCHAR(50),
                religion_id VARCHAR(50),
                development INT,
                sub_kingdoms INT,
                sub_duchies INT,
                sub_counties INT,
                PRIMARY KEY (title_id, year),
                FOREIGN KEY (title_id) REFERENCES ck3_dw.dim_title(title_id) ON DELETE CASCADE,
                FOREIGN KEY (year) REFERENCES ck3_dw.dim_year(year) ON DELETE RESTRICT,
                FOREIGN KEY (duchy_id) REFERENCES ck3_dw.dim_title(title_id) ON DELETE SET NULL,
                FOREIGN KEY (kingdom_id) REFERENCES ck3_dw.dim_title(title_id) ON DELETE SET NULL,
                FOREIGN KEY (empire_id) REFERENCES ck3_dw.dim_title(title_id) ON DELETE SET NULL,
                FOREIGN KEY (hegemony_id) REFERENCES ck3_dw.dim_title(title_id) ON DELETE SET NULL,
                FOREIGN KEY (culture_id) REFERENCES ck3_dw.dim_culture(culture_id) ON DELETE SET NULL,
                FOREIGN KEY (religion_id) REFERENCES ck3_dw.dim_religion(religion_id) ON DELETE SET NULL
            );

            -- 6. Indeks Analitik
            CREATE INDEX IF NOT EXISTS idx_fact_year ON ck3_dw.fact_title_snapshot(year);
            CREATE INDEX IF NOT EXISTS idx_fact_empire ON ck3_dw.fact_title_snapshot(empire_id);
            CREATE INDEX IF NOT EXISTS idx_fact_kingdom ON ck3_dw.fact_title_snapshot(kingdom_id);
            CREATE INDEX IF NOT EXISTS idx_fact_tier ON ck3_dw.fact_title_snapshot(tier);
        """)
    conn.commit()

def get_dw_connection():
    conn = get_connection()
    create_dw_schema_and_tables(conn)
    with conn.cursor() as cur:
        cur.execute("SET search_path TO ck3_dw, public;")
    conn.commit()
    return conn


YEARS = (867, 1066, 1178)


def extract(oltp_conn):
    """Ambil seluruh data yang dibutuhkan dari skema relasional."""
    cur = oltp_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT title_id, name, tier FROM public.title;")
    titles = cur.fetchall()

    cur.execute("SELECT culture_id, name FROM public.culture;")
    cultures = cur.fetchall()

    cur.execute("SELECT religion_id, name FROM public.religion;")
    religions = cur.fetchall()

    cur.execute("""
        SELECT title_id, year, parent_title_id, culture_id, religion_id,
               development, sub_counties, sub_duchies, sub_kingdoms
        FROM public.title_snapshot;
    """)
    snapshots = cur.fetchall()

    # Junction statis hegemony <-> empire
    cur.execute("SELECT hegemony_id, empire_id FROM public.hegemony_empire;")
    empire_to_hegemony = {
        row["empire_id"]: row["hegemony_id"] for row in cur.fetchall()
    }

    cur.close()
    return titles, cultures, religions, snapshots, empire_to_hegemony


def transform(titles, snapshots, empire_to_hegemony):
    tier_by_id = {t["title_id"]: t["tier"] for t in titles}

    # index: (title_id, year) -> parent_title_id
    parent_by_year = {
        (s["title_id"], s["year"]): s["parent_title_id"] for s in snapshots
    }

    def resolve_ancestors(title_id, year):
        """Jalan ke atas rantai parent_title_id, kelompokkan per tier."""
        ancestors = {}
        current = title_id
        seen = set()  # guard kalau ada siklus data yang salah
        while True:
            parent = parent_by_year.get((current, year))
            if not parent or parent in seen:
                break
            seen.add(parent)
            parent_tier = tier_by_id.get(parent)
            if parent_tier:
                ancestors[parent_tier] = parent
            current = parent
        return ancestors

    fact_rows = []
    for s in snapshots:
        title_id, year = s["title_id"], s["year"]
        tier = tier_by_id.get(title_id)

        ancestors = resolve_ancestors(title_id, year)
        duchy_id = ancestors.get("duchy")
        kingdom_id = ancestors.get("kingdom")
        empire_id = ancestors.get("empire")

        if tier == "empire":
            hegemony_id = empire_to_hegemony.get(title_id)
        else:
            hegemony_id = empire_to_hegemony.get(empire_id) if empire_id else None

        fact_rows.append(dict(
            title_id=title_id, year=year, tier=tier,
            duchy_id=duchy_id, kingdom_id=kingdom_id,
            empire_id=empire_id, hegemony_id=hegemony_id,
            culture_id=s["culture_id"] if tier == "county" else None,
            religion_id=s["religion_id"] if tier == "county" else None,
            development=s["development"],
            sub_kingdoms=s["sub_kingdoms"],
            sub_duchies=s["sub_duchies"],
            sub_counties=s["sub_counties"],
        ))
    return fact_rows


def load(dw_conn, titles, cultures, religions, fact_rows):
    cur = dw_conn.cursor()

    # Load Dimensi Title
    psycopg2.extras.execute_values(
        cur,
        "INSERT INTO ck3_dw.dim_title (title_id, name, tier) VALUES %s "
        "ON CONFLICT (title_id) DO UPDATE SET name = EXCLUDED.name;",
        [(t["title_id"], t["name"], t["tier"]) for t in titles],
    )

    # Load Dimensi Year & Era (interpretasi mandiri, bukan data resmi CK3)
    year_data = [
        (867, 'Carolingian Era / Early Middle Ages'),
        (1066, 'Norman Conquest / High Middle Ages'),
        (1178, 'Third Crusade / Late Middle Ages'),
    ]
    psycopg2.extras.execute_values(
        cur,
        "INSERT INTO ck3_dw.dim_year (year, era_name) VALUES %s "
        "ON CONFLICT (year) DO NOTHING;",
        year_data,
    )

    # Load Dimensi Culture
    psycopg2.extras.execute_values(
        cur,
        "INSERT INTO ck3_dw.dim_culture (culture_id, name) VALUES %s "
        "ON CONFLICT (culture_id) DO NOTHING;",
        [(c["culture_id"], c["name"]) for c in cultures],
    )

    # Load Dimensi Religion
    psycopg2.extras.execute_values(
        cur,
        "INSERT INTO ck3_dw.dim_religion (religion_id, name) VALUES %s "
        "ON CONFLICT (religion_id) DO NOTHING;",
        [(r["religion_id"], r["name"]) for r in religions],
    )

    # Load Tabel Fakta
    psycopg2.extras.execute_values(
        cur,
        """
        INSERT INTO ck3_dw.fact_title_snapshot
            (title_id, year, tier, duchy_id, kingdom_id, empire_id,
             hegemony_id, culture_id, religion_id, development,
             sub_kingdoms, sub_duchies, sub_counties)
        VALUES %s
        ON CONFLICT (title_id, year) DO UPDATE SET
            duchy_id = EXCLUDED.duchy_id,
            kingdom_id = EXCLUDED.kingdom_id,
            empire_id = EXCLUDED.empire_id,
            hegemony_id = EXCLUDED.hegemony_id,
            development = EXCLUDED.development;
        """,
        [(
            f["title_id"], f["year"], f["tier"], f["duchy_id"],
            f["kingdom_id"], f["empire_id"], f["hegemony_id"],
            f["culture_id"], f["religion_id"], f["development"],
            f["sub_kingdoms"], f["sub_duchies"], f["sub_counties"],
        ) for f in fact_rows],
    )

    dw_conn.commit()
    cur.close()


def main():
    oltp_conn = get_connection()
    dw_conn = get_dw_connection()

    titles, cultures, religions, snapshots, empire_to_hegemony = \
        extract(oltp_conn)
    fact_rows = transform(titles, snapshots, empire_to_hegemony)
    load(dw_conn, titles, cultures, religions, fact_rows)

    print(f"ETL selesai: {len(titles)} title, {len(fact_rows)} baris fact "
          f"dimuat ke ck3_dw.fact_title_snapshot.")

    oltp_conn.close()
    dw_conn.close()


if __name__ == "__main__":
    main()