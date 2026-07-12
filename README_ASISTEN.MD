<h1 align="center">
  <br>
  Seleksi Warga Basdat 2026 <br>
  ETL Project
  <br>
  <br>
</h1>

<h2 align="left">
  <br>
  Singkatnya?
  <br>
</h2>
Pada tahap seleksi ini, peserta akan diminta untuk melakukan proses ETL yang meliputi data scraping, database modeling, dan data storing terkait sebuah topik yang dibebaskan kepada peserta. Peserta juga diminta untuk merancang sebuah model ERD dan model relasional yang akan diimplementasikan untuk menyimpan hasil proses data scraping sebelumnya. Tahap seleksi ini menguji kemampuan peserta untuk mengumpulkan data, merancang sebuah database, dan merealisasikan rancangan tersebut menjadi sebuah database relasional yang fungsional.
  <br>

## Step 1: Data Scraping
1. Pilih sebuah topik yang akan kalian jadikan sebagai tema pada seleksi _data scraping_ Anda. Daftarkan topik tersebut ke dalam spreadsheet berikut:
[Daftar Topik Seleksi Asisten Lab Basis Data 2026](https://docs.google.com/spreadsheets/d/1cowSMPtWQApyALrypfMBJSOuqbXyGh2cCaDXKRs8fD4/edit?usp=sharing)
    - Usahakan agar tidak ada dua atau lebih peserta dengan topik yang sama
    - First come, first served. Bila ada dua atau lebih peserta dengan topik yang sama, peserta dengan topik yang sudah terdaftar duluan (berada di atas) akan diprioritaskan.
    - Akses edit ke _spreadsheet_ topik data scraping akan ditutup pada tanggal **25 Juli pukul 20:40 WIB**
2. Lakukan _data scraping_ dari sebuah _web page_ untuk memperoleh data dan informasi sesuai dengan topik yang telah dipilih oleh masing-masing peserta. 
    - Data dan informasi yang diperoleh akan digunakan di _step_ berikutnya sebagai data yang akan disimpan di dalam sebuah RDBMS
    - Peserta **DILARANG** menggunakan API untuk melakukan proses data scraping
3. Pada folder `Data Scraping`, peserta harus mengumpulkan file _script_ dan file JSON hasil _scraping_ yang telah dilakukan
    - Folder `src` berisi _script_/_code_ yang telah digunakan untuk _scraping_. Pastikan bahwa _script_/_code_ yang kalian bua bersifat well documented dan clean. 
    - Folder `data` berisi semua data dan informasi yang berhasil kalian scrape dalam bentu JSON. Peserta diperbolehkan untuk memisahkan hasil _scraping_ ke dalam file-file yang berbeda ataupun digabung dalam satu file yang besar. Yang penting sesuai dengan output dari _script_ _data scraping_ yang digunakan
    - Folder `screenshot` berisi tangkapan layar dari _script/code_ yang kalian gunakan untuk _data scraping_. Pastikan tangkapan layar dapat dibaca dengan jelas
4. Sebagai referensi untuk mempelajari dan mengenal _data scraping_, asisten telah menyiapkan dokumen panduan singkat pada link berikut: Panduan Singkat Data Scraping
    - Dokumen tersebut hanya merupakan panduan bagi peserta. Metodologi _data scraping_ yang digunakan oleh peserta seleksi basdat dibebaskan (asal sesuai peraturan)
    - Perhatikan dan peragakan etika _data scraping_ yang baik dalam pelaksanaan seleksi ini
5. Syarat data yang diperoleh dari proses data scraping: Data yang diperoleh harus di-_preprocessing_ terlebih dahulu
    - Beberapa contoh _preprocessing_:
        - Cleaning
        - Parsing
        - Transformation
        - Dll
    - Preprocessing dilakukan untuk memastikan data yang diterima tidak sepenuh-penuhnya mentah dan tidak dapat dipahami dengan mudah
  

## Step 2: Data Modeling + Data Storing
1. Dari hasil proses _data scraping_ yang telah dilakukan, lakukan perancangan _database_ dalam bentuk **ERD**. Sertakan asumsi dan penjelasan di dalam desain ERD-nya bila diperlukan
2. Translasikan hasil desain ERD tersebut ke dalam bentuk diagram relasional. Peserta dipersilahkan untuk menambahkan tabel lain yang sekiranya relevan atau berkaitan dengan tabel-tabel yang murni didapatkan dari proses _data scraping_.
3. Implementasikan skema diagram relasional tersebut ke dalam RDBMS sesuai pilihan peserta (PostgreSQL, mariaDB, etc). Peserta **dilarang** untuk menggunakan DBMS no-SQL
    - Jangan lupa untuk mengimplementasikan _constraints_ ke dalam _database_ (primary key, foreign key, trigger, dll)
4. Setelah _database_-nya telah diimplementasikan, masukkan data yang didapatkan dari proses _scraping_ ke dalam RDBMS yang telah dibuat
    - Tabel tambahan yang dibuat pada poin 2 tidak perlu diisi dengan data (baik data _dummy_ maupun data asli). Cukup dibiarkan kosong
5. Tools yang digunakan dibebaskan kepada peserta
6. Pada folder `Data Storing`, peserta harus mengumpulkan bukti penyimpanan data pada DBMS. Folder `Data Storing` terdiri dari folder `design`, `export`, dan `screenshots`.
    - Folder `design` berisi gambar ERD dan gambar diagram relasional dari _database_ yang kalian rancang. Format file yang diterima adalah **.png**
    - Folder `src` berisi script/code yang telah digunakan untuk storing. Pastikan bahwa script/code yang kalian bua bersifat well documented dan clean. 
    - Folder `export` berisi file hasil _export_ dari DBMS dengan format **.sql**
    - Folder `screenshots` berisi tangkapan layar bukti dari penyimpanan data ke dalam RDBMS (Query SELECT FROM WHERE pada RDBMS)

## Bonus:
Task-task berikut merupakan bonus yang **TIDAK WAJIB** dilakukan oleh peserta seleksi. Penyelesaian satu atau lebih dari task bonus akan membawa nilai tambahan bagi peserta yang menyelesaikannya. Peserta dibolehkan untuk mengerjakan sebagian atau seluruh dari task bonus yang tersedia
1. Buatlah perancangan dan implementasi data warehouse berdasarkan data yang diperoleh dari proses data scraping. Rancanglah skema yang diperlukan untuk fact table dan dimension table (misalnya menggunakan pendekatan star schema atau snowflake schema) untuk mendukung kebutuhan analitik. Sertakan struktur skema data warehouse yang digunakan beserta contoh query analitik yang bisa dijalankan terhadap data tersebut. 
2. Lakukan automated scheduling untuk keseluruhan proses, sehingga data dapat di-update secara berkala. Pastikan tidak terdapat redundansi data pada DBMS. Jika mengerjakan bonus ini, jelaskan pada README dan cantumkan pada data waktu pelaksanaan scheduling, misalnya dengan menunjukkan perbedaan timestamp ekstraksi antara data pada batch pertama dan data pada batch kedua


# Pengumpulan
1. Peserta diwajibkan untuk melakukan _fork_ terhadap project [GitHub Seleksi Lab Basdat 2026](https://github.com/wargabasdat/Seleksi-2026-Tugas-1). Peserta harus melakukan _pull request_ dengan nama **TUGAS_SELEKSI_1_[NIM]** sebelum tenggat waktu yang telah ditetapkan
2. Tambahkan **.gitignore** pada _file_ atau _folder_ yang tidak perlu di-upload. NB: Binary tidak perlu di-upload
3. Sertakan file **README** yang memuat:
    - Author (Nama dan NIM)
    - Deskripsi singkat mengenai data dan DBMS yang telah dibuat + mengapa kalian memilih topik tersebut
    - Cara menggunakan scraper yang telah dibuat dan menggunakan hasil output-nya
    - Penjelasan struktur dari file JSON yang dihasilkan scraper
    - Struktur ERD dan diagram relasional RDBMS
    - Penjelasan mengenai proses translasi ERD menjadi diagram relasional
    - Beberapa screenshot dari program yang dijalankan (image di-upload sesuai folder-folder yang tersedia, di README tinggal ditampilkan)
    - Referensi (library yang digunakan, link halaman web yang di-scrape, etc)
  
# DEADLINE PENGUMPULAN ADALAH TANGGAL 23 Juli 2026, PUKUL 22:40