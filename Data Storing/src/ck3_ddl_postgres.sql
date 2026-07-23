-- Creating Table like in the relational diagram
CREATE TABLE Title (
    title_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    tier VARCHAR(50) NOT NULL
);

CREATE TABLE County (
    title_id VARCHAR(50) PRIMARY KEY,
    baronies_count INT,
    FOREIGN KEY (title_id) REFERENCES Title(title_id) ON DELETE CASCADE
);

CREATE TABLE Duchy (
    title_id VARCHAR(50) PRIMARY KEY,
    FOREIGN KEY (title_id) REFERENCES Title(title_id) ON DELETE CASCADE
);

CREATE TABLE Kingdom (
    title_id VARCHAR(50) PRIMARY KEY,
    special_requirements TEXT,
    ai_requirements TEXT,
    FOREIGN KEY (title_id) REFERENCES Title(title_id) ON DELETE CASCADE
);

CREATE TABLE Empire (
    title_id VARCHAR(50) PRIMARY KEY,
    special_requirements TEXT,
    ai_requirements TEXT,
    FOREIGN KEY (title_id) REFERENCES Title(title_id) ON DELETE CASCADE
);

CREATE TABLE Hegemony (
    title_id VARCHAR(50) PRIMARY KEY,
    decision TEXT,
    notes TEXT,
    FOREIGN KEY (title_id) REFERENCES Title(title_id) ON DELETE CASCADE
);


CREATE TABLE Special_Building (
    building_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE Religion (
    religion_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE Culture (
    culture_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE Character (
    character_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    birth_year INT,
    death_year INT
);

CREATE TABLE Barony (
    barony_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    province_number INT,
    county_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (county_id) REFERENCES County(title_id) ON DELETE CASCADE
);

CREATE TABLE War (
    war_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50),
    casus_belli_type VARCHAR(50),
    year INT,
    attacker_id VARCHAR(50),
    defender_id VARCHAR(50),
    FOREIGN KEY (attacker_id) REFERENCES Character(character_id) ON DELETE RESTRICT,
    FOREIGN KEY (defender_id) REFERENCES Character(character_id) ON DELETE RESTRICT
);


CREATE TABLE Alt_Name (
    title_id VARCHAR(50) NOT NULL,
    alt_name VARCHAR(50) NOT NULL,
    year INT,
    PRIMARY KEY (title_id, alt_name),
    FOREIGN KEY (title_id) REFERENCES Title(title_id) ON DELETE CASCADE
);

CREATE TABLE Title_Snapshot (
    title_id VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    parent_title_id VARCHAR(50),
    culture_id VARCHAR(50),
    religion_id VARCHAR(50),
    ruler_id VARCHAR(50),
    development INT,
    sub_kingdoms INT,
    sub_duchies INT,
    sub_counties INT,
    sub_baronies INT,
    PRIMARY KEY (title_id, year),
    FOREIGN KEY (title_id) REFERENCES Title(title_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_title_id) REFERENCES Title(title_id) ON DELETE SET NULL,
    FOREIGN KEY (culture_id) REFERENCES Culture(culture_id) ON DELETE RESTRICT,
    FOREIGN KEY (religion_id) REFERENCES Religion(religion_id) ON DELETE RESTRICT,
    FOREIGN KEY (ruler_id) REFERENCES Character(character_id) ON DELETE SET NULL,
    CONSTRAINT chk_snapshot_year CHECK (year IN (867, 1066, 1178))
);


CREATE TABLE Title_Building (
    title_id VARCHAR(50) NOT NULL,
    building_id VARCHAR(50) NOT NULL,
    PRIMARY KEY (title_id, building_id),
    FOREIGN KEY (title_id) REFERENCES Title(title_id) ON DELETE CASCADE,
    FOREIGN KEY (building_id) REFERENCES Special_Building(building_id) ON DELETE CASCADE
);

CREATE TABLE Alt_Name_Culture (
    title_id VARCHAR(50) NOT NULL,
    alt_name VARCHAR(50) NOT NULL,
    culture_id VARCHAR(50) NOT NULL,
    PRIMARY KEY (title_id, alt_name, culture_id),
    FOREIGN KEY (title_id, alt_name) REFERENCES Alt_Name(title_id, alt_name) ON DELETE CASCADE,
    FOREIGN KEY (culture_id) REFERENCES Culture(culture_id) ON DELETE CASCADE
);

CREATE TABLE Hegemony_Empire (
    hegemony_id VARCHAR(50) NOT NULL,
    empire_id VARCHAR(50) NOT NULL,
    PRIMARY KEY (hegemony_id, empire_id),
    FOREIGN KEY (hegemony_id) REFERENCES Hegemony(title_id) ON DELETE CASCADE,
    FOREIGN KEY (empire_id) REFERENCES Empire(title_id) ON DELETE CASCADE
);

CREATE TABLE War_Contests (
    war_id VARCHAR(50) NOT NULL,
    title_id VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    transferred VARCHAR(10) DEFAULT 'pending',
    PRIMARY KEY (war_id, title_id, year),
    FOREIGN KEY (war_id) REFERENCES War(war_id) ON DELETE CASCADE,
    FOREIGN KEY (title_id, year) REFERENCES Title_Snapshot(title_id, year) ON DELETE CASCADE,
    CONSTRAINT chk_transferred CHECK (transferred IN ('pending', 'yes', 'no'))
);

/* Triggers */
-- 1) BEFORE INSERT — attacker dan defender tidak boleh orang yang sama
CREATE OR REPLACE FUNCTION check_attacker_defender_different()
RETURNS TRIGGER AS $$\data
BEGIN
    IF NEW.attacker_id = NEW.defender_id THEN
        RAISE EXCEPTION 'attacker_id dan defender_id tidak boleh sama (character_id: %)', NEW.attacker_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER bi_war_attacker_defender
BEFORE INSERT ON War
FOR EACH ROW
EXECUTE FUNCTION check_attacker_defender_different();

-- 2) BEFORE UPDATE — transferred tidak boleh kembali ke 'pending'
--    setelah pernah jadi 'yes' atau 'no' (status final tidak boleh di-revert)
CREATE OR REPLACE FUNCTION check_transferred_no_revert()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.transferred IN ('yes', 'no') AND NEW.transferred = 'pending' THEN
        RAISE EXCEPTION 'transferred tidak boleh diubah kembali ke pending setelah berstatus % (war_id: %, title_id: %, year: %)',
            OLD.transferred, NEW.war_id, NEW.title_id, NEW.year;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER bu_war_contests_transferred
BEFORE UPDATE ON War_Contests
FOR EACH ROW
EXECUTE FUNCTION check_transferred_no_revert();

-- 3) BEFORE DELETE — War tidak boleh dihapus kalau sudah ada
--    war_contests yang statusnya final (yes/no), demi menjaga histori
CREATE OR REPLACE FUNCTION prevent_delete_resolved_war()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM War_Contests
        WHERE war_id = OLD.war_id
        AND transferred IN ('yes', 'no')
    ) THEN
        RAISE EXCEPTION 'War % tidak bisa dihapus karena sudah punya war_contests dengan status final (yes/no)', OLD.war_id;
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER bd_war_prevent_delete
BEFORE DELETE ON War
FOR EACH ROW
EXECUTE FUNCTION prevent_delete_resolved_war();

-- 4) AFTER INSERT/DELETE — recalc sub_counties di parent duchy/kingdom/empire
--    AMAN di-trigger karena Title_Snapshot data-nya lengkap (bukan sparse
--    kayak Barony). TIDAK dibuatkan trigger serupa untuk sub_baronies atau
--    baronies_count di County/Duchy, karena keduanya bergantung ke tabel
--    Barony yang sengaja sparse (cuma dummy rows). nilai asli untuk kolom
--    itu diisi langsung dari hasil scraping lewat script import, bukan
--    dihitung ulang otomatis oleh trigger.
CREATE OR REPLACE FUNCTION recalc_sub_counties()
RETURNS TRIGGER AS $$
DECLARE
    target_title_id VARCHAR(50);
    target_year INT;
BEGIN
    target_title_id := COALESCE(NEW.parent_title_id, OLD.parent_title_id);
    target_year := COALESCE(NEW.year, OLD.year);

    IF target_title_id IS NOT NULL THEN
        UPDATE Title_Snapshot
        SET sub_counties = (
            SELECT COUNT(*) FROM Title_Snapshot
            WHERE parent_title_id = target_title_id AND year = target_year
        )
        WHERE title_id = target_title_id AND year = target_year;
    END IF;

    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER aid_title_snapshot_recalc_sub_counties
AFTER INSERT OR DELETE ON Title_Snapshot
FOR EACH ROW
EXECUTE FUNCTION recalc_sub_counties();