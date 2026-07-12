
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

### Referensi & Pustaka
- **Sumber Data:** [CK3 Wiki - Crusader Kings III Paradox Wikis](https://ck3.paradoxwikis.com/)
- **Pustaka Python:**
  - `cloudscraper`: Untuk menembus sistem proteksi Cloudflare pada CK3 Wiki secara aman.
  - `beautifulsoup4` (`bs4`): Pustaka parsing DOM HTML.
  - `re` & `json`: Pustaka manipulasi regex dan ekspor format JSON.