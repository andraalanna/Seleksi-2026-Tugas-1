
---

# Dokumentasi Proyek Seleksi Asisten Lab Basis Data 2026

### Author
- **Nama:** Angelina Andra Alanna
- **NIM:** 13524079
- **Program Studi:** Teknik Informatika

### Deskripsi Proyek & Topik Data
- **Topik:** Data Hierarki De Jure Title & Snapshot Historis Crusader Kings III.
- **DBMS Pilihan:** PostgreSQL.
- **Deskripsi:** Proyek ini bertujuan untuk men-scrape dan memodelkan data hierarki de jure wilayah di game Crusader Kings III (dari tingkat County -> Duchy -> Kingdom -> Empire -> Hegemony) lengkap dengan snapshot historis kepemilikan wilayah tersebut pada tiga tahun awal yang berbeda: 867, 1066, dan 1178.
- **Alasan Pemilihan Topik:** Game Crusader Kings III memiliki sistem pemetaan wilayah de jure yang sangat dinamis dan berubah berdasarkan tahun awal permainan (start date). Hal ini memberikan tantangan pemodelan basis data temporal yang menarik untuk meminimalkan redundansi data melalui teknik normalisasi basis data yang matang (hingga 3NF/BCNF). PostgreSQL dipilih sebagai DBMS utama karena dukungannya terhadap fitur-fitur tingkat lanjut seperti pembuatan trigram index (GIN) untuk pencarian teks substring dinamis serta keandalan dalam menangani complex constraints & database triggers.

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
  * `culture` (List of Strings atau null): Budaya yang menggunakan nama alternatif tersebut untuk wilayah county ini.
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

#### 1. Hierarki Title (ISA)
Karena tiap tingkatan title (county, duchy, kingdom, empire, hegemony) punya atribut umum yang sama tapi juga ada atribut yang cuma dimiliki tier tertentu, aku pakai pendekatan class table inheritance — jadi ada satu tabel induk Title (nyimpen title_id, name, tier), terus masing-masing tier punya tabel sendiri (County, Duchy, Kingdom, Empire, Hegemony) yang title_id-nya sekaligus jadi PK dan FK balik ke Title, pakai ON DELETE CASCADE. Alasan milih ini dibanding gabungin semua jadi satu tabel besar: kalau digabung, bakal banyak banget kolom yang isinya NULL (misal County jelas nggak butuh kolom special_requirements yang cuma relevan buat Kingdom/Empire). Jadi mending dipisah per tabel biar tiap tier cuma nyimpen atribut yang memang relevan buat dia.

#### 2. Data yang berubah per-tahun
di CK3, hierarki de jure itu nggak tetap. County yang tahun 867 masuk Duchy A, bisa aja di tahun 1178 udah pindah ke Duchy B. Development, budaya, agama wilayah juga berubah tergantung start date yang dipilih (867/1066/1178). Kalau info ini ditaruh langsung sebagai kolom statis di Title, itu bakal salah secara konsep. Oleh sebab itu diambil keputusan untuk dipisahkan jadi tabel Title_Snapshot sendiri, dengan PK gabungan (title_id, year). Di tabel ini ada juga parent_title_id yang nunjuk balik ke Title (self-referencing FK) buat gambarin parent-nya di tahun itu, plus FK ke Culture, Religion, dan Character (buat ruler). Dengan cara ini, entitas title-nya sendiri tetap satu (nggak duplikat), tapi state-nya per tahun bisa disimpan terpisah.

#### 3. Relasi Many-to-Many
Ada beberapa hubungan yang sifatnya M:N, jadi butuh tabel penghubung:

* **Title_Building:** nghubungin Title dengan Special_Building, PK-nya gabungan (title_id, building_id).
* **Hegemony_Empire:** karena satu Hegemony bisa menaungi lebih dari satu Empire.
* **Alt_Name_Culture:** nama alternatif wilayah bisa terkait ke lebih dari satu budaya.
* **War_Contests:** nghubungin War ke state title tertentu di tahun tertentu, jadi FK-nya komposit ke (title_id, year) di Title_Snapshot.

#### 4. Relasi Many-to-One
Buat relasi yang sifatnya satu ke banyak, bukan M:N atau self-referencing, aku nggak bikin tabel penghubung terpisah. Cukup pindahin PK dari sisi "satu" ke tabel sisi "banyak" sebagai kolom FK biasa. Contohnya County yang di bawah satu Duchy tertentu, atau Special_Building yang dimiliki satu Title, dan sejenisnya — di sini duchy_id (atau id yang relevan) tinggal ditaruh langsung sebagai kolom di tabel anaknya, nggak perlu tabel tambahan. Ini pendekatan standar buat 1:N di relational mapping, karena satu baris di sisi "banyak" cuma butuh nunjuk ke satu baris pasangannya di sisi "satu", jadi FK biasa udah cukup, nggak ada redundansi yang perlu dihindari kayak kasus M:N tadi.

#### 5. Weak entity dan atribut multi-nilai
Barony itu weak entity di bawah County, dia nggak punya identitas sendiri tanpa county-nya (PK barony_id, FK county_id). Sementara Alt_Name aku model sebagai tabel terpisah karena satu title bisa punya banyak nama alternatif tergantung tahun/budaya siapa yang mengucapkannya. Kadi ini atribut multivalue, PK-nya gabungan (title_id, alt_name).

#### 6. Integritas Data (Constraint)
Untuk constraint, dipakai kombinasi beberapa jenis ON DELETE: CASCADE buat relasi subtype dan snapshot (kalau title-nya dihapus, turunannya ikut kehapus), SET NULL buat ruler_id/parent_title_id (karena kalau penguasa atau parent-nya dihapus, catatan historisnya tetap harus ada, cuma referensinya jadi kosong), dan RESTRICT buat data master (Character, Culture, Religion) biar nggak sengaja kehapus padahal masih dipakai di tempat lain. Ada juga CHECK buat batasi nilai yang valid, contohnya year cuma boleh 867/1066/1178.

Selain itu ada beberapa trigger yang dibuat: check_attacker_defender_different (mastiin penyerang dan yang diserang di tabel War nggak boleh sama), check_transferred_no_revert (status perang yang udah final nggak bisa balik jadi pending lagi), prevent_delete_resolved_war (perang yang udah selesai nggak boleh dihapus, biar histori tetap ada), dan recalc_sub_counties (otomatis update jumlah sub-county di parent snapshot kalau ada perubahan data di level bawahnya).
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
| 4 | Pertumbuhan Historis | Title mana yang development-nya naik paling drastis dari 867 ke 1178? |

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

### Automated Scheduling

#### Metodologi & Arsitektur Penjadwalan
Penjadwalan otomatis diimplementasikan menggunakan pendekatan **Incremental Change Detection (Conditional Scraping)** dengan memanfaatkan fitur MediaWiki Revision History (`action=history`):

1. **Change Detection (Deteksi Perubahan):** Sebelum mengunduh dan memproses ulang data wiki yang berukuran besar, script `scheduler.py` memeriksa timestamp revisi terakhir (`mw-changeslist-date`) dari halaman history 5 tier wiki (`List_of_counties`, `List_of_duchies`, `List_of_kingdoms`, `List_of_empires`, `List_of_hegemonies`).
2. **Logika Perbandingan:** Script membandingkan timestamp revisi terbaru wiki dengan timestamp `last_update` pada tabel `log` PostgreSQL:
   - **Jika Wiki > DB (`UPDATED`):** Terjadi pembaruan pada wiki. Sistem akan menjalankan scraper (`scrape_one`), cleaner (`clean_one`), serta meng-import data baru ke database (`import_all_data`), lalu mencatat baris log baru ber-status `UPDATED`.
   - **Jika Wiki == DB (`NOT CHANGED`):** Tidak ada pembaruan pada wiki. Sistem melewati proses scraping penuh untuk menghemat bandwidth dan beban server, lalu mencatat baris log baru ber-status `NOT CHANGED`.
3. **Penyimpanan Log Multi-Batch:** Setiap eksekusi mencatat audit trail di tabel PostgreSQL `log` (dan `Automated Scheduling/logs/scheduler.log`) untuk membuktikan keaktifan penjadwal antar siklus eksekusi.
4. **Karakteristik Data Sumber:** Data pada CK3 Wiki bersifat relatif statis dan jarang diperbarui setiap hari. Oleh karena itu, mekanisme *Conditional Scraping* via `action=history` ini sangat krusial untuk memastikan server tidak melakukan scraping redundan secara berlebihan, sementara database tetap ter-update secara otomatis jika terjadi pembaruan di wiki.

#### Bukti Eksekusi Multi-Batch & Tabel Log PostgreSQL
Tabel `log` pada PostgreSQL (`ck3_db`) mencatat riwayat eksekusi multi-batch dengan timestamp yang berbeda:

- **Batch 1 Run (`UPDATED`):** Mendeteksi perbedaan tanggal dari baseline awal (`2024-04-21`), mengeksekusi pipeline scraping & cleaning penuh, lalu meng-upsert data ke tabel database utama (`Title`, `Title_Snapshot`, dll) dan mencatat status `UPDATED`.
- **Batch 2 Run (`NOT CHANGED`):** Mendeteksi tanggal wiki sama dengan database (`2026-07-11`), secara otomatis melewati proses scraping penuh, dan mencatat status `NOT CHANGED`.

#### Registrasi OS Scheduler
Script `Automated Scheduling/src/scheduler.py` telah berhasil didaftarkan ke **Windows Task Scheduler** dengan nama task `CK3 Wiki Scraper Scheduler` untuk eksekusi otomatis secara berkala.

---

### Query Optimasi 

#### Tujuan & Ringkasan Eksperimen
Bagian ini bertujuan untuk menganalisis dan mengoptimalkan performa eksekusi query pada database PostgreSQL (`ck3_db`) dengan menggunakan perintah `EXPLAIN ANALYZE`. Pengujian dilakukan terhadap 3 jenis skenario query dengan beban kerja yang beragam (join hierarki multi-level, pencarian substring teks bebas, dan agregasi data agregat).

#### Ringkasan Perbandingan Performa

| Query | Skenario | Waktu Sebelum (Before) | Metode Scan Sebelum | Waktu Sesudah (After) | Metode Scan Sesudah | Peningkatan (%) |
|---|---|---|---|---|---|---|
| **Query 1** | Multi-Level Join (County ke Empire) | 6.022 ms | Seq Scan pada `title_snapshot` | 0.657 ms | Bitmap Index Scan / Index Scan | ~89.1% |
| **Query 2** | Text Search Substring (`ILIKE '%bryn%'`) | 0.764 ms | Seq Scan pada `alt_name` | 0.579 ms (Default) / 5.540 ms (Forced) | Seq Scan (Planner) / Bitmap Index Scan (Forced) | ~24.2% (Default) / Slowdown (Forced) |
| **Query 3** | Agregasi Budaya & Agama per Kingdom | 29.449 ms | Seq Scan pada `title_snapshot` (2x) | 15.001 ms | Bitmap Index Scan | ~49.1% |

---

#### Analisis Detail per Query

##### 1. Query 1 — Hierarchical Multi-Level Join
Query ini melakukan traversal hierarki wilayah dari tingkat County menuju Empire (`e_britannia`) pada tahun `1066` dengan melewati 2 hop relasi parent (`county` -> `duchy` -> `kingdom`).

```sql
-- Indeks yang Dibuat
CREATE INDEX idx_snapshot_parent_year ON title_snapshot (parent_title_id, year);

-- Perintah Query
EXPLAIN ANALYZE
SELECT t_county.name AS county_name
FROM title_snapshot ts_county
JOIN title t_county ON t_county.title_id = ts_county.title_id AND t_county.tier = 'county'
JOIN title_snapshot ts_duchy ON ts_duchy.title_id = ts_county.parent_title_id AND ts_duchy.year = ts_county.year
JOIN title_snapshot ts_kingdom ON ts_kingdom.title_id = ts_duchy.parent_title_id AND ts_kingdom.year = ts_county.year
WHERE ts_kingdom.parent_title_id = 'e_britannia' AND ts_county.year = 1066;
```

* **Sebelum Indeks:** PostgreSQL melakukan pembacaan berurutan (*Sequential Scan*) pada seluruh baris tabel `title_snapshot` untuk setiap tahapan join, memakan waktu eksekusi sebesar **6.022 ms**.
  ![Query 1 Before](Query%20Optimasi/screenshots/query1_before.png)

* **Sesudah Indeks:** Setelah indeks komposit `idx_snapshot_parent_year` diterapkan pada kolom `(parent_title_id, year)`, query planner menggunakan **Bitmap Index Scan** dan **Index Scan**. Waktu eksekusi turun drastis menjadi **0.657 ms** (peningkatan kecepatan sebesar **89.1%**).
  ![Query 1 After](Query%20Optimasi/screenshots/query1_after.png)

---

##### 2. Query 2 — Text Search pada Nama Alternatif
Query ini melakukan pencarian potongan nama historis alternatif (`alt_name`) menggunakan pencarian substring bebas dengan wildcard ganda (`ILIKE '%bryn%'`).

```sql
-- Ekstensi PostgreSQL untuk Trigram
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Indeks GIN Trigram
CREATE INDEX idx_altname_trgm ON alt_name USING gin (alt_name gin_trgm_ops);

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
```

* **Sebelum Indeks:** PostgreSQL melakukan *Sequential Scan* pada tabel `alt_name` dengan waktu eksekusi **0.764 ms**.
  ![Query 2 Before](Query%20Optimasi/screenshots/query2_before.png)

* **Sesudah Indeks (Default Optimizer):** Meskipun indeks GIN Trigram `idx_altname_trgm` telah diterapkan, *Cost-Based Optimizer* PostgreSQL tetap memilih *Sequential Scan* dengan waktu eksekusi yang sama (**0.579 ms**). Hal ini terjadi karena ukuran tabel `alt_name` relatif kecil (hanya 761 baris), sehingga estimasi biaya pembacaan langsung di memori lebih murah dibanding melakukan overhead pencarian pohon indeks dan re-check baris.
  ![Query 2 Default Planner](Query%20Optimasi/screenshots/query2_after.png)

* **Sesudah Indeks (Metode Bitmap Index Scan (Forced)):** Untuk membuktikan bahwa indeks GIN Trigram tersebut valid dan dapat berfungsi, perintah `SET enable_seqscan = off;` dijalankan secara sementara. Hasilnya menunjukkan bahwa query planner berhasil beralih menggunakan **Bitmap Index Scan**. Namun query malah menjadi tidak efektif dan semakin lama (**38.701 ms**). Hal ini disebabkan karena ukuran tabel alt_name yang relatif kecil menyebabkan overhead pemacaan indekes GIN Trogram dan pencocokan ulang trigram (Recheck Cond) lebih besar daripada pemindaian langsung seluruh tabel di memori. Apabila tabel alt_name menjadi jauh lebih besar query akan menjadi lebih efektif.
  ![Query 2 Forced Index](Query%20Optimasi/screenshots/query2_after_seqoff.png)

---

##### 3. Query 3 — Agregasi Budaya dan Agama per Kingdom
Query ini menghitung jumlah variasi budaya (`culture_id`) dan agama (`religion_id`) di tingkat county untuk setiap kingdom pada tahun `1178` menggunakan klausa `GROUP BY`, `COUNT(DISTINCT)`, dan `ORDER BY`.

```sql
-- Indeks yang Dibuat
CREATE INDEX idx_snapshot_year ON title_snapshot (year);

-- Perintah Query
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
```

* **Sebelum Indeks:** PostgreSQL melakukan dua kali *Sequential Scan* pada tabel `title_snapshot` (untuk alias `ts_county` dan `ts_duchy`), di mana masing-masing scan membaca 13.941 baris dan membuang 9.294 baris yang tidak sesuai filter tahun. Waktu eksekusi sebesar **29.449 ms**.
  ![Query 3 Before](Query%20Optimasi/screenshots/query3_before.png)

* **Sesudah Indeks:** Setelah indeks `idx_snapshot_year` ditambahkan pada kolom `year`, pembacaan berurut beralih menjadi **Bitmap Index Scan**. Waktu eksekusi berhasil dipangkas menjadi **15.001 ms** (peningkatan kecepatan sebesar **49.1%**).
  ![Query 3 After](Query%20Optimasi/screenshots/query3_after.png)

---
### Pernyataan Penggunaan AI

Sesuain dengan ketentuan seleksi, bagian ini menjelaskan penggunaan AI selama pengerjaan proyek ini.

#### 1. Bagian yang Dibantu Oleh AI
* **Penyusunan Jadwal & Guidebook:** Membantu menyusun rancangan target harian agar proses belajar dan pengerjaan proyek terstruktur dan dapat beriringan dengan aktivitas lainnya.

* **Pencarian Referensi & Penjelasan Konsep:** Membantu mencarikan referensi belajar tambahan saat menjelaskan konsep-konsep teknis basis data yang kurang dipahami (seperti bypass Cloudflare pakai `cloudscraper`, implementasi trigger di pgSQL, dan pembacaan metrik `EXPLAIN ANALYZE`)

* **Debugging Kode & Bug Fixing:** Membantu menganalisis log error dan mencari solusi perbaikan (*bug fixing*) saat terjadi kendala teknis pada script Python scraper/cleaner dan query SQL.
* **Penyusunan Struktur README:** Membantu merapikan struktur penulisan markdown, memperbaiki sintaks tautan gambar yang tidak konsisten, dan memformat README agar terlihat rapi dan profesional.
* **Saran & Opini Desain:** Meminta umpan balik (*feedback*), saran keefektifan, dan validasi terhadap rancangan skema ERD, Diagram Relasional, serta query optimasi agar model data yang dihasilkan optimal.
* **Registrasi OS Scheduler:** Membantu menjelaskan dan memberikan panduan cara mendaftarkan skrip penjadwal otomatis (scheduling) ke sistem operasi (OS) menggunakan Windows Task Scheduler.
* **Ekspor & Dump Database/Warehouse:** Membantu mengidentifikasi letak utilitas PostgreSQL (`pg_dump.exe`) pada lokal Windows (di runtime pgAdmin 4) dan menyusun perintah baris CLI yang tepat untuk mengekspor database secara mandiri menjadi berkas `.sql` (`ck3_relational_export.sql` & `ck3_dw_export.sql`).

#### 2. Bagian yang Tetap Dikerjakan Sendiri
* **Coding & Implementasi ETL:** Menulis dan mengimplementasikan seluruh script Python untuk scraping, data cleaning, dan data storing.
* **Perancangan skema Database:** Merancang struktur ERD dan translasinya ke Diagram Relasional dari awal dengan pemahaman yang dimiliki terkait game Crusaider Kings III (hierarki gelar de jure)
* **Eksekusi Pengujian & Screenshot:** Menjalankan database secara manual, mengeksekusi trigeer, melalukan pengetesan query optimisasi, serta mengambil tangkapa screenshot.
* **Penulisan Konten README:** Menulis konten analisis, deskripsi data, dan kesimpulan dari optimisasi query berdasarkan hasil running di database lokal.

#### 3. Refleksi Penggunaan AI
Penggunaan AI dalam proyek ini menurut saya sudah sangat baik sebagai asisten belajar (tutor) yang mempercepat pemahaman dari dokumentasi sehingga waktu dapat dipadatkan untuk pembuatan script, database, dan query serta analisis hasilnya. Meskipun AI sangat membantu dalam meberikan saran desain dan debugging, keputusan akhir, validasi kebenaran logika database, dan pemahaman alur data tetap sepenuhnya berada di tangan praktikan guna memastikan seluruh sistem berjalan sesuai dengan aturan bisnis (business rules) game CK3.

---
### Referensi & Pustaka

#### Sumber Data & Pustaka Utama
- **Sumber Data:** [CK3 Wiki - Crusader Kings III Paradox Wikis](https://ck3.paradoxwikis.com/)
- **Pustaka Python:**
  - `cloudscraper`: Pustaka penembus proteksi Cloudflare anti-bot challenge pada CK3 Wiki secara aman.
  - `beautifulsoup4` (`bs4`): Pustaka parsing DOM HTML.
  - `psycopg2`: Pustaka adapter/connector basis data PostgreSQL untuk Python.

#### Referensi Pembelajaran & Tutorial
##### A. Web Scraping (Python + Requests + BeautifulSoup)
- [BeautifulSoup Tutorial: Web Scraping with Python (2026)](https://www.youtube.com/watch?v=ztxIxbRyPJI) — paling baru, pas buat versi library terkini
- [Beautiful Soup 4 Tutorial #1 — Web Scraping With Python](https://www.youtube.com/watch?v=gRLHr664tXA) — seri dasar, cocok kalau baru pertama kali
- [Web Scraping with Python — Beautiful Soup Crash Course](https://www.youtube.com/watch?v=XVv6mJpFOb0) — versi ringkas kalau kamu mau cepat
- [Real Python — Beautiful Soup: Build a Web Scraper With Python](https://realpython.com/beautiful-soup-web-scraper-python/) — tulisan lengkap, bagus buat referensi sambil coding (bukan cuma nonton)
- Dokumentasi resmi BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Dokumentasi resmi requests: https://requests.readthedocs.io/

##### A.1 Cloudflare Bypass (cloudscraper)
- Dokumentasi resmi (PyPI): https://pypi.org/project/cloudscraper/
- Repo GitHub: https://github.com/VeNoMouS/cloudscraper
- Panduan step-by-step: https://github.com/IPRoyal/use-cloudscraper/

##### B. Entity Relationship Diagram (ERD)
- [ERD Tutorial — Part 1 (dasar)](https://www.youtube.com/watch?v=xsg9BDiwiJE)
- [ERD Tutorial — Part 2: Primary keys, foreign keys, bridge tables](https://www.youtube.com/watch?v=hktyW5Lp0Vo) — wajib ditonton, soalnya kamu butuh paham "bridge table" buat desain snapshot temporal
- [Entity Relationship Diagrams Explained: ERD Basics for Beginners](https://www.youtube.com/watch?v=fUUJyFR0gXo)
- [GeeksforGeeks — Introduction of ER Model](https://www.geeksforgeeks.org/dbms/introduction-of-er-model/)
- Tool desain: https://dbdiagram.io dan https://app.diagrams.net

##### C. PostgreSQL / SQL
- [PostgreSQL Tutorial for Beginners](https://www.youtube.com/watch?v=qw5yEgAM9nM) — tutorial lengkap dari dasar
- [Learn PostgreSQL Tutorial - Full Course for Beginners](https://www.youtube.com/watch?v=SpfIwlAYaKk) — belajar DDL, DML, constraint, dan triggers
- Dokumentasi Resmi PostgreSQL: https://www.postgresql.org/docs/
- Dokumentasi Resmi Psycopg2: https://www.psycopg.org/docs/

##### D. Data Warehouse / Star Schema (Bonus 1)
- [Datawarehousing Concepts Basics (Fact and Dimension Table)](https://www.youtube.com/watch?v=Q7KHW2oCOUI)
- [What is STAR schema | Star vs Snowflake Schema](https://www.youtube.com/watch?v=hQvCOBv_-LE)
- [Star schema — Wikipedia](https://en.wikipedia.org/wiki/Star_schema) — ringkas dan cukup buat pegangan konsep
- [Dimensional Modeling — Facts, Dimensions, and Star Schema (Data Vidhya)](https://datavidhya.com/learn/data-modeling-and-warehouse/dimensional-modeling/dimensional-modeling-intro/) — penjelasan step-by-step yang gampang diikuti