
---

# Dokumentasi Proyek Seleksi Asisten Lab Basis Data 2026

### Author
- **Nama:** Angelina Andra Alanna
- **NIM:** 13524079
- **Program Studi:** Teknik Informatika

### Deskripsi Proyek & Topik Data
- **Topik:** Data Hierarki De Jure Title & Snapshot Historis Crusader Kings III.
- **DBMS Pilihan:** MariaDB / MySQL.
- **Deskripsi:** Proyek ini bertujuan untuk men-scrape dan memodelkan data hierarki de jure wilayah di game Crusader Kings III (dari tingkat County -> Duchy -> Kingdom -> Empire -> Hegemony) lengkap dengan snapshot historis kepemilikan wilayah tersebut pada tiga tahun awal yang berbeda: 867, 1066, dan 1178.
- **Alasan Pemilihan Topik:** Game Crusader Kings III memiliki sistem pemetaan wilayah de jure yang sangat dinamis dan dipengaruhi oleh tahun awal permainan (start date). Hal ini memberikan tantangan pemodelan basis data temporal yang sangat baik untuk meminimalkan redundansi data melalui teknik normalisasi database yang matang (hingga 3NF/BCNF).

---

### Cara Menjalankan Scraper & Cleaner

1. **Persiapan Lingkungan (Setup Environment):**
   Pastikan Python 3 telah terinstall di sistem kamu. Silakan install pustaka (*dependencies*) eksternal yang dibutuhkan melalui terminal:
   ```bash
   pip install cloudscraper beautifulsoup4
   ```

2. **Menjalankan Data Scraping (Step 1):**
   Jalankan script `scraper.py` untuk mengambil data mentah dari CK3 Wiki:
   ```bash
   python "Data Scraping/src/scraper.py"
   ```
   *Output data mentah akan disimpan dalam bentuk JSON di folder `Data Scraping/data/` (seperti `counties.json`, `duchies.json`, dll).*

3. **Menjalankan Data Preprocessing & Cleaning:**
   Jalankan script `cleaner.py` untuk membersihkan data mentah, memecah nama alternatif, mengonversi tipe data angka menjadi Integer, dan menghilangkan duplikasi data:
   ```bash
   python "Data Scraping/src/cleaner.py"
   ```
   *Output data bersih akan disimpan di folder `Data Scraping/data/` dengan akhiran `_cleaned.json` (seperti `counties_cleaned.json`, `duchies_cleaned.json`, dll).*

---

### Penjelasan Struktur File JSON Hasil Scraping (Cleaned)

#### 1. Counties (`counties_cleaned.json`)
Menyimpan informasi tingkat county (tingkat wilayah de jure terkecil).
* `county` (String): Nama wilayah county.
* `duchy` (String): Nama duchy de jure dari county tersebut.
* `kingdom_867` / `kingdom_1066` / `kingdom_1178` (String): Nama kingdom de jure county tersebut pada tahun snapshot.
* `empire_867` / `empire_1066` / `empire_1178` (String): Nama empire de jure county tersebut pada tahun snapshot.
* `baronies` (Integer): Jumlah barony di dalam county.
* `development_867` / `development_1066` / `development_1178` (Integer): Tingkat pembangunan (development) wilayah pada tahun snapshot.
* `special_buildings` (String, List of Strings, atau null): Nama bangunan khusus di county tersebut (duplikasi seperti Hadrian's Wall telah di-deduplicate).
* `culture_867` / `culture_1066` / `culture_1178` (String): Budaya mayoritas county pada tahun snapshot.
* `religion_867` / `religion_1066` / `religion_1178` (String): Agama mayoritas county pada tahun snapshot.
* `alternative_names` (List of Objects): Nama alternatif wilayah berdasarkan budaya atau tahun tertentu.
  * `name` (String): Nama alternatif.
  * `year` (Integer atau null): Tahun nama tersebut aktif.
  * `culture` (List of Strings atau null): Budaya penguasa yang memicu nama tersebut.
* `id` (String): Kode ID unik gelar wilayah (contoh: `c_middlesex`).

#### 2. Duchies (`duchies_cleaned.json`)
Menyimpan data wilayah tingkat Duchy.
* `duchy` (String): Nama wilayah duchy.
* `kingdom_867` / `kingdom_1066` / `kingdom_1178` (String): Nama kingdom de jure duchy tersebut pada tahun snapshot.
* `empire_867` / `empire_1066` / `empire_1178` (String): Nama empire de jure duchy tersebut pada tahun snapshot.
* `counties` (Integer): Jumlah total county de jure di bawah duchy ini.
* `baronies` (Integer): Jumlah total barony de jure di bawah duchy ini.
* `average_development_867` / `average_development_1066` / `average_development_1178` (Integer): Rata-rata tingkat pembangunan wilayah duchy pada tahun snapshot.
* `special_buildings` (String atau List of Strings atau null): Nama bangunan khusus yang ada di wilayah duchy ini (jika ada).
* `alternative_names` (List of Objects): Nama alternatif wilayah (format sama dengan County).
* `capital` (String): Nama ibukota de jure duchy.
* `id` (String): ID unik gelar duchy (contoh: `d_essex`).

#### 3. Kingdoms (`kingdoms_cleaned.json`)
Menyimpan data wilayah tingkat Kingdom.
* `kingdom` (String): Nama wilayah kingdom.
* `hegemony_867` / `hegemony_1066` / `hegemony_1178` (String atau null): Nama hegemoni de jure kingdom tersebut pada tahun snapshot.
* `empire_867` / `empire_1066` / `empire_1178` (String): Nama empire de jure kingdom tersebut pada tahun snapshot.
* `duchies_867` / `duchies_1066` / `duchies_1178` (Integer): Jumlah duchy de jure di bawah kingdom ini pada tahun snapshot.
* `counties_867` / `counties_1066` / `counties_1178` (Integer): Jumlah county de jure di bawah kingdom ini pada tahun snapshot.
* `special_requirements` (String atau null): Persyaratan khusus untuk mendirikan/menciptakan gelar kingdom tersebut.
* `ai_requirements` (String atau null): Persyaratan AI untuk mendirikan kingdom tersebut.
* `alternative_names` (List of Objects): Nama alternatif wilayah (format sama dengan County).
* `capital` (String): Nama ibukota de jure kingdom.
* `id` (String): ID unik gelar kingdom (contoh: `k_england`).

#### 4. Empires (`empires_cleaned.json`)
Menyimpan data wilayah tingkat Empire.
* `empire` (String): Nama wilayah empire.
* `kingdoms_867` / `kingdoms_1066` / `kingdoms_1178` (Integer): Jumlah kingdom de jure di bawah empire ini pada tahun snapshot.
* `duchies_867` / `duchies_1066` / `duchies_1178` (Integer): Jumlah duchy de jure di bawah empire ini pada tahun snapshot.
* `counties_867` / `counties_1066` / `counties_1178` (Integer): Jumlah county de jure di bawah empire ini pada tahun snapshot.
* `special_requirements` (String atau null): Persyaratan khusus pembentukan gelar empire.
* `ai_requirements` (String atau null): Persyaratan AI untuk mendirikan empire.
* `alternative_names` (List of Objects): Nama alternatif wilayah (format sama dengan County).
* `capital` (String): Nama ibukota de jure empire.
* `id` (String): ID unik gelar empire (contoh: `e_britannia`).

#### 5. Hegemonies (`hegemonies_cleaned.json`)
* `hegemony` (String): Nama gelar hegemoni (contoh: "China").
* `empires` (List of Strings): Empire yang tercakup dalam hegemoni tersebut.
* `capital` (String): Ibukota de jure hegemoni.
* `decision` (String): Keputusan pembentukannya.
* `notes` (String): Paragraf catatan khusus mengenai hegemoni tersebut (telah disatukan dari bentuk list mentah).

---

### Desain ERD & Diagram Relasional (Step 2 - Data Modeling)

Perancangan basis data dilakukan melalui pemodelan *Entity-Relationship Diagram* (ERD) dan ditranslasikan ke dalam Diagram Relasional:

#### 1. Entity-Relationship Diagram (ERD)
![Entity Relationship Diagram](Data%20Storing/design/Asisten_BasisData_CK3-ERD.drawio.png)

#### 2. Diagram Relasional
![Relational Diagram](Data%20Storing/design/Asisten_BasisData_CK3-Relational%20Diagram.drawio%20(1).png)

---

### Penjelasan Proses Translasi ERD ke Relasional

Skema basis data relasional pada proyek ini didesain menggunakan skrip DDL [ck3_ddl_postgres.sql](Data%20Storing/src/ck3_ddl_postgres.sql) dengan menerapkan 5 pendekatan utama dalam memetakan Entity-Relationship Diagram (ERD) menjadi skema tabel relasional:

#### 1. Spesialisasi & Generalisasi (ISA Hierarchy): *Class Table Inheritance (Table-per-Subtype)*
- **Pola:** *Class Table Inheritance* (atau *Subclass Mapping Pattern*).
- **Implementasi:**
  - Tabel Basis (Supertype): `Title` (`title_id`, `name`, `tier`).
  - Tabel Subtype Spesifik: `County`, `Duchy`, `Kingdom`, `Empire`, `Hegemony`.
  - Primary Key pada setiap tabel subtype (`title_id`) sekaligus berfungsi sebagai Foreign Key ke `Title(title_id)` dengan *constraint* `ON DELETE CASCADE`.
- **Rasionalitas Design:** Setiap tingkatan gelar dalam CK3 memiliki atribut umum (`title_id`, `name`, `tier`), namun hirarki tertentu memiliki atribut unik (seperti `baronies_count` pada County, `special_requirements` pada Kingdom/Empire, serta `decision` & `notes` pada Hegemony). Pendekatan ini mencegah kemunculan kolom bernilai `NULL` yang berlebihan (dibandingkan *Single Table Inheritance*) sekaligus menjaga integritas data spesifik per tier.

#### 2. Pemodelan Data Temporal & Dinamis: *Temporal Bridge Table (Snapshot Pattern)*
- **Pola:** *Temporal Bridge Table / Point-in-Time Snapshot Pattern*.
- **Implementasi:**
  - Tabel `Title_Snapshot` dengan Composite Primary Key `(title_id, year)`.
  - Memiliki *Self-referencing Foreign Key* `parent_title_id` yang merujuk ke `Title(title_id)`.
  - Memiliki Foreign Key ke entitas master pendukung: `culture_id` (`Culture`), `religion_id` (`Religion`), dan `ruler_id` (`Character`).
- **Rasionalitas Design:** Dalam CK3, struktur hierarki *de jure* (misal: County tertentu milik Duchy mana) dan atribut statistik wilayah (*development*, penguasa, agama, budaya) **sangat dinamis dan berubah-ubah berdasarkan tahun awal permainan (*start date*: 867, 1066, 1178)**. Pemisahan entitas statis (`Title`) dari state temporalnya (`Title_Snapshot`) meminimalkan duplikasi data entitas utama dan memodelkan relasi dinamis secara efisien.

#### 3. Pemetaan Relasi Banyak-ke-Banyak (Many-to-Many / M:N): *Junction / Bridge Tables*
- **Pola:** Tabel Penghubung (*Bridge / Junction Table*).
- **Implementasi:**
  - `Title_Building`: Menghubungkan `Title` dengan `Special_Building` (M:N) dengan Primary Key gabungan `(title_id, building_id)`.
  - `Hegemony_Empire`: Menghubungkan `Hegemony` dengan `Empire` (M:N, karena 1 Hegemony menaungi banyak Empire). Primary Key gabungan `(hegemony_id, empire_id)`.
  - `Alt_Name_Culture`: Menghubungkan nama alternatif wilayah dengan `Culture` (M:N). Menghubungkan Composite PK `(title_id, alt_name)` dari tabel `Alt_Name` dengan `culture_id`.
  - `War_Contests`: Menghubungkan entitas `War` dengan state snapshot wilayah (`Title_Snapshot`). Menghubungkan `war_id` dengan Composite FK `(title_id, year)`.

#### 4. Entitas Lemah (Weak Entities) & Atribut Multi-nilai (*Multivalued Attributes*)
- **Implementasi:**
  - `Barony`: Dimodelkan sebagai weak entity di bawah `County` (PK `barony_id`, FK `county_id` -> `County(title_id)`).
  - `Alt_Name`: Atribut multi-nilai dari `Title` yang tergantung pada tahun aktif tertentu. Dimodelkan sebagai tabel terpisah dengan Composite Primary Key `(title_id, alt_name)`.

#### 5. Penegakan Aturan Bisnis & Integritas Referensial (*Referential Integrity & Triggers*)
- **Integritas Referensial:**
  - `ON DELETE CASCADE` pada relasi subtype dan snapshot agar jika suatu `Title` dihapus, data turunannya otomatis terhapus.
  - `ON DELETE SET NULL` pada `ruler_id` dan `parent_title_id` agar penghapusan penguasa/parent tidak menghancurkan record snapshot sejarah.
  - `ON DELETE RESTRICT` pada master data (`Character`, `Culture`, `Religion`) untuk mencegah penghapusan data referensi yang sedang aktif digunakan.
  - `CHECK Constraint` untuk validasi domain nilai (seperti `year IN (867, 1066, 1178)` dan `transferred IN ('pending', 'yes', 'no')`).
- **Database Triggers (Stored Procedures PL/pgSQL):**
  - `check_attacker_defender_different`: Memastikan `attacker_id != defender_id` dalam tabel `War`.
  - `check_transferred_no_revert`: Mencegah perubahan status perang dari status final (`yes`/`no`) kembali ke `pending`.
  - `prevent_delete_resolved_war`: Menjaga histori perang agar tidak bisa dihapus apabila perang tersebut sudah selesai (berstatus final).
  - `recalc_sub_counties`: Otomatis menghitung ulang agregat `sub_counties` pada `Title_Snapshot` parent saat terjadi manipulasi data snapshot child.

---

### Pengujian Skema Database & Integrity Constraints (Step 2 - Data Storing)

Setelah proses import data selesai menggunakan skrip [import_data.py](Data%20Storing/src/import_data.py), dilakukan serangkaian pengujian (*queries verification*) dan pengujian aturan integritas (*integrity constraints & database triggers*) untuk memastikan bahwa skema basis data PostgreSQL berjalan sesuai dengan perancangan.

#### 1. Verifikasi Struktur Tabel (`DESCRIBE / \d`) & Jumlah Data

Daftar seluruh 18 tabel yang ada di dalam database `ck3_db` dapat dilihat pada perintah `\dt`:

![Daftar Tabel](Data%20Storing/screenshot/queries/list_tables.png)

Struktur ke-18 tabel relasional yang dihasilkan dari skrip DDL dapat dilihat pada screenshot hasil perintah `\d <nama_tabel>` di bawah ini:

<details>
<summary><b>Klik di sini untuk melihat Screenshot Struktur 18 Tabel (\d)</b></summary>
<br>

| Nama Tabel | Tangkapan Layar Struktur (`\d`) |
| :--- | :--- |
| **Title** | ![Describe Title](Data%20Storing/screenshot/describe/describe_Title.png) |
| **County** | ![Describe County](Data%20Storing/screenshot/describe/describe_County.png) |
| **Duchy** | ![Describe Duchy](Data%20Storing/screenshot/describe/describe_Duchy.png) |
| **Kingdom** | ![Describe Kingdom](Data%20Storing/screenshot/describe/describe_Kingdom.png) |
| **Empire** | ![Describe Empire](Data%20Storing/screenshot/describe/describe_Empire.png) |
| **Hegemony** | ![Describe Hegemony](Data%20Storing/screenshot/describe/describe_Hegemony.png) |
| **Barony** | ![Describe Barony](Data%20Storing/screenshot/describe/describe_Barony.png) |
| **Character** | ![Describe Character](Data%20Storing/screenshot/describe/describe_Character.png) |
| **Culture** | ![Describe Culture](Data%20Storing/screenshot/describe/describe_Culture.png) |
| **Religion** | ![Describe Religion](Data%20Storing/screenshot/describe/describe_Religion.png) |
| **Special_Building** | ![Describe Special Building](Data%20Storing/screenshot/describe/describe_Special_Building.png) |
| **Alt_Name** | ![Describe Alt Name](Data%20Storing/screenshot/describe/describe_Alt_Name.png) |
| **Alt_Name_Culture** | ![Describe Alt Name Culture](Data%20Storing/screenshot/describe/describe_Alt_Name_Culture.png) |
| **Hegemony_Empire** | ![Describe Hegemony Empire](Data%20Storing/screenshot/describe/describe_Hegemony_Empire.png) |
| **Title_Building** | ![Describe Title Building](Data%20Storing/screenshot/describe/describe_Title_Building.png) |
| **Title_Snapshot** | ![Describe Title Snapshot](Data%20Storing/screenshot/describe/describe_Title_Snapshot.png) |
| **War** | ![Describe War](Data%20Storing/screenshot/describe/describe_War.png) |
| **War_Contests** | ![Describe War Contests](Data%20Storing/screenshot/describe/describe_War_Contests.png) |

</details>

<br>

Untuk memverifikasi bahwa data hasil scraping dan cleaning berhasil di-insert secara utuh tanpa ada yang hilang, dijalankan query agregat jumlah data pada seluruh tabel:

```sql
SELECT 'Title' AS tabel, COUNT(*) FROM Title
UNION ALL SELECT 'County', COUNT(*) FROM County
UNION ALL SELECT 'Duchy', COUNT(*) FROM Duchy
UNION ALL SELECT 'Kingdom', COUNT(*) FROM Kingdom
UNION ALL SELECT 'Empire', COUNT(*) FROM Empire
UNION ALL SELECT 'Hegemony', COUNT(*) FROM Hegemony
UNION ALL SELECT 'Title_Snapshot', COUNT(*) FROM Title_Snapshot
UNION ALL SELECT 'Culture', COUNT(*) FROM Culture
UNION ALL SELECT 'Religion', COUNT(*) FROM Religion
UNION ALL SELECT 'Special_Building', COUNT(*) FROM Special_Building;
```

![Tabel Aggregation Count](Data%20Storing/screenshot/queries/count_rows_all_tables.png)

##### Sampel Data Hasil Import:
- **Tabel Title (Kingdom):**
  ```sql
  SELECT * FROM Title WHERE tier = 'kingdom' LIMIT 10;
  ```
  ![Sampel Kingdom](Data%20Storing/screenshot/queries/select_kingdom_sample.png)

- **Tabel Title_Snapshot:**
  ```sql
  SELECT * FROM Title_Snapshot WHERE year = 1066 LIMIT 10;
  ```
  ![Sampel Title Snapshot](Data%20Storing/screenshot/queries/select_snapshot_sample.png)

---

#### 2. Pengujian Aturan Integritas & Trigger Database

Pengujian dilakukan untuk membuktikan bahwa *Domain Constraints*, *Foreign Key Referential Actions*, dan *PL/pgSQL Triggers* bekerja dengan benar dalam memvalidasi operasi `INSERT`, `UPDATE`, dan `DELETE`:

##### A. Domain Check Constraint (`chk_snapshot_year`)
* **Query:** `INSERT INTO Title_Snapshot (title_id, year) VALUES ('c_middlesex', 2026);`
* **Penjelasan:** DBMS menolak data karena tahun 2026 berada di luar pilihan *start date* resmi game (867, 1066, 1178).

![Check Year Rejected](Data%20Storing/screenshot/constraint_triggers/check_year_rejected.png)

##### B. Trigger Attacker != Defender (`bi_war_attacker_defender`)
* **Query:** `INSERT INTO War (war_id, name, attacker_id, defender_id) VALUES ('war_fail1', 'Self War', 'char_test1', 'char_test1');`
* **Penjelasan:** Trigger memblokir pembuatan record perang apabila pihak penyerang dan bertahan merujuk pada karakter yang sama.

![Trigger Attacker Defender Rejected](Data%20Storing/screenshot/constraint_triggers/trigger_attacker_defender_rejected.png)

##### C. Trigger Immutability Status Perang (`bu_war_contests_transferred`)
* **Query:** `UPDATE War_Contests SET transferred = 'pending' WHERE war_id = 'war_test2';`
* **Penjelasan:** Trigger menolak perubahan status perang yang sudah berstatus final (`yes`/`no`) untuk kembali menjadi `pending`.

![Trigger Revert Pending Rejected](Data%20Storing/screenshot/constraint_triggers/trigger_revert_pending_rejected.png)

##### D. Trigger Proteksi Histori Perang (`prevent_delete_resolved_war`)
* **Query:** `DELETE FROM War WHERE war_id = 'war_test2';`
* **Penjelasan:** Operasi `DELETE` ditolak karena perang terkait sudah memiliki hasil akhir yang telah tersimpan.

![Trigger Delete Resolved War Rejected](Data%20Storing/screenshot/constraint_triggers/trigger_delete_resolved_war_rejected.png)

##### E. Trigger Auto-Recalculate `sub_counties` (`aid_title_snapshot_recalc_sub_counties`)
* **Query:** `INSERT INTO Title_Snapshot (title_id, year, parent_title_id) VALUES ('c_sub1', 1066, 'd_test_duchy');`
* **Penjelasan:** Saat snapshot wilayah anak ditambahkan, trigger secara otomatis memperbarui nilai agregat `sub_counties` pada snapshot parent terkait tanpa perlu query update manual.
  * **Sebelum Insert Child Snapshot:**  
    ![Recalc Sub Counties Before](Data%20Storing/screenshot/constraint_triggers/trigger_recalc_sub_counties_before.png)
  * **Setelah Insert Child Snapshot:**  
    ![Recalc Sub Counties After](Data%20Storing/screenshot/constraint_triggers/trigger_recalc_sub_counties_after.png)

##### F. Integritas Referensial `ON DELETE CASCADE`
* **Query:** `DELETE FROM Title WHERE title_id = 'c_test_casc';`
* **Penjelasan:** Menghapus record pada tabel induk `Title` secara otomatis menghapus record terkait pada tabel spesialisasi `County` dan `Title_Snapshot`.

![FK Cascade After Delete](Data%20Storing/screenshot/constraint_triggers/fk_cascade_after_delete.png)

##### G. Integritas Referensial `ON DELETE SET NULL`
* **Query:** `DELETE FROM Character WHERE character_id = 'char_ruler_1';`
* **Penjelasan:** Menghapus penguasa dari tabel `Character` akan mengosongkan nilai `ruler_id` pada `Title_Snapshot` menjadi `NULL` tanpa menghapus data snapshot wilayah tersebut.

![FK Set Null After Delete](Data%20Storing/screenshot/constraint_triggers/fk_set_null_after_delete.png)

##### H. Integritas Referensial `ON DELETE RESTRICT`
* **Query:** `DELETE FROM Religion WHERE religion_id = 'apostolic';`
* **Penjelasan:** DBMS menolak penghapusan master data agama yang sedang dirujuk oleh record snapshot wilayah yang aktif.

![FK Restrict Religion Rejected](Data%20Storing/screenshot/constraint_triggers/fk_restrict_religion_rejected.png)

---
### Data Warehouse

#### Metodologi & Langkah Perancangan

Perancangan Data Warehouse pada proyek ini mengikuti **Kimball's Four-Step Dimensional Design Process**:

1. **Select the business process**: Menentukan proses/tujuan analitik yang mau didukung. Dipilih framing **"starting position advisor untuk pemain baru CK3"**. DW ini membantu pemain menentukan start date & wilayah awal yang paling sesuai gaya bermain mereka, alih-alih framing generik ala data warehouse korporat yang kurang relevan dengan topik title hierarchy.
2. **Rumuskan pertanyaan bisnis**: didapat 4 perspektif (lihat di bawah). Setiap perspektif divalidasi dulu terhadap ketersediaan data hasil scraping.
3. **Declare the grain**: level detail 1 baris pada fact table ditetapkan sebagai **"satu title pada satu tahun snapshot (867/1066/1178)"**.
4. **Identify the dimensions**: `dim_title` (title lintas tier), `dim_year` (3 start date), `dim_culture`, `dim_religion`.
5. **Identify the facts**: `development`, `sub_kingdoms`, `sub_duchies`, `sub_counties` sebagai measure numerik.

#### 4 Perspektif Bisnis
| No | Perspektif | Pertanyaan Bisnis |
|---|---|---|
| 1 | Ekonomi & Pembangunan | County mana yang paling makmur (development tertinggi) di tiap start date, cocok dijadikan ibu kota? |
| 2 | Ekspansi Wilayah | Empire mana yang menaungi wilayah (sub-county/sub-duchy) terbanyak, cocok untuk gaya main ekspansif? |
| 3 | Stabilitas Budaya & Agama | Kingdom mana yang homogen (stabil, cocok pemula) vs beragam (rawan konflik)? |
| 4 | Pertumbuhan Historis | Title mana yang development-nya naik paling drastis dari 867 → 1178? |

##### Star Schema

Struktur: **1 fact table** (`fact_title_snapshot`) + **4 dimension table** (`dim_title`, `dim_year`, `dim_culture`, `dim_religion`).
 
![Star Schema Data Warehouse](Data%20Warehouse/design/warehouse_design_star_schema.png)

Poin desain penting:
- **Role-playing dimension**: `duchy_id`, `kingdom_id`, `empire_id`, `hegemony_id` pada fact table sama-sama merujuk ke `dim_title`. Satu tabel dimensi dipakai berulang untuk peran hierarki yang berbeda, sehingga satu baris fact bisa langsung di-*join* ke semua level parent tanpa recursive query berjenjang.
- **Sparsity by design**: kolom `culture_id`/`religion_id` hanya terisi untuk baris bertingkat `county` (NULL di tier lain, karena atribut ini memang hanya tersedia di level county pada data sumber). Kolom `duchy_id`/`kingdom_id`/`empire_id`/`hegemony_id` juga NULL secara bertahap tergantung tingkatan title itu sendiri (contoh: baris `empire` tidak punya `duchy_id`/`kingdom_id`, karena dia sendiri sudah di atas keduanya).
- **`dim_year.era_name`** adalah label deskriptif periode sejarah yang **diinterpretasikan sendiri** berdasarkan konteks historis umum tiap start date (bukan data resmi dari game maupun hasil scraping), ditambahkan sebagai *enrichment*.

#### Query Analitik Data Warehouse

4 query lengkap tersedia di skrip [analytic_queries.sql](Data%20Warehouse/src/analytic_queries.sql), masing-masing menjawab 1 perspektif bisnis di atas:

- **Query 1 (Ekonomi & Pembangunan):**  
  ![Query 1 Ekonomi](Data%20Warehouse/screenshot/query1_economy.png)

- **Query 2 (Ekspansi Wilayah):**  
  ![Query 2 Ekspansi](Data%20Warehouse/screenshot/query2_expansion.png)

- **Query 3 (Stabilitas Budaya & Agama):**  
  ![Query 3 Stabilitas](Data%20Warehouse/screenshot/query3_stability.png)

- **Query 4 (Pertumbuhan Historis):**  
  ![Query 4 Pertumbuhan](Data%20Warehouse/screenshot/query4_growth.png)

---

### Referensi & Pustaka
- **Sumber Data:** [CK3 Wiki - Crusader Kings III Paradox Wikis](https://ck3.paradoxwikis.com/)
- **Pustaka Python:**
  - `cloudscraper`: Untuk menembus sistem proteksi Cloudflare pada CK3 Wiki secara aman.
  - `beautifulsoup4` (`bs4`): Pustaka parsing DOM HTML.
  - `re` & `json`: Pustaka manipulasi regex dan ekspor format JSON.