"Perancangan Digital Twin Tangki Air untuk Monitoring Ketinggian dan Kondisi Air Secara Real-Time"

1. Latar Belakang

Pemantauan tangki air (rumah tangga, gedung, kampus, maupun industri kecil) umumnya masih dilakukan secara manual, yaitu dengan mengecek langsung ke tangki. Cara ini menimbulkan beberapa masalah: air meluap atau habis tanpa disadari, pompa menyala terus atau terlambat menyala, kualitas air menurun (keruh, suhu tidak normal, TDS tinggi) tanpa terdeteksi, serta tidak ada riwayat data yang bisa dianalisis. Diperlukan sistem yang mampu merepresentasikan kondisi tangki fisik secara digital (**digital twin**) dan memantaunya secara real-time agar pengelolaan air lebih efisien, aman, dan terdokumentasi.

2. Tujuan

- Membangun representasi digital (digital twin) tangki air yang mencerminkan kondisi tangki fisik secara real-time
- Memantau **ketinggian air** (level dalam cm dan persentase kapasitas)
- Memantau **kondisi air**, dengan parameter yang dibatasi pada tiga hal:
  - Suhu air (°C)
  - Kekeruhan / turbidity (NTU)
  - Kualitas air berdasarkan TDS (ppm)
- Menampilkan data dalam dashboard interaktif (visual tangki, grafik tren, status)
- Memberikan notifikasi otomatis saat kondisi tidak normal (air hampir habis, hampir meluap, kualitas di luar ambang batas)
- Menyimpan riwayat data sensor untuk analisis dan laporan
- Pada tahap pengembangan awal, data sensor menggunakan **data dummy hasil simulasi**, dengan arsitektur yang siap dihubungkan ke sensor nyata

3. Keputusan Sprint 1

a. Agile Methodology
- Metodologi yang digunakan: **Scrum**
- Durasi sprint: ± 1 bulan per sprint (mengikuti timeline Sp1–Sp5)
- Role tim: 1 orang sebagai **Scrum Master** (Ketua Tim/koordinator), sisanya **Development Team**
- Tools tracking task: **GitHub Projects**
- Artefak Scrum: Product Backlog, Sprint Backlog, dan Increment di akhir tiap sprint

b. UX Design
- Antarmuka dirancang dengan wireframe sederhana (Figma/sketsa) sebelum masuk development
- Elemen utama halaman:
  - Dashboard utama: visual tangki (animasi level air), nilai level saat ini, suhu, kekeruhan, TDS, dan indikator status (Normal / Waspada / Bahaya)
  - Grafik tren: level dan kualitas air per jam / hari / minggu
  - Riwayat data: tabel data sensor dengan filter tanggal dan parameter
  - Pengaturan ambang batas: batas minimum/maksimum level dan kualitas air
  - Notifikasi/alert (contoh: banner "Level air 15%, segera isi tangki")
  - Halaman login untuk pengguna dan admin
- Alur pengguna: login → lihat dashboard real-time → cek grafik tren → atur ambang batas → terima notifikasi → tinjau riwayat data

c. Project Setup
- Struktur folder awal repository:
  ```
  digital-twin-tangki-air/
  ├── backend/        # API server (Flask/Node.js)
  ├── frontend/       # Dashboard web (HTML/JS/CSS)
  ├── simulator/      # Python sensor simulator (data dummy)
  ├── database/       # Skema, ERD & seed data
  ├── docs/           # Charter, wireframe, FP, dokumentasi API
  └── README.md
  ```
- Tech stack awal: Python Sensor Simulator (data dummy level, suhu, kekeruhan, TDS), Flask/Node.js (backend), HTML/JS + Bootstrap/Tailwind + Chart.js (frontend awal)

4. Arsitektur Sistem

a. Objek Fisik & Pengguna (Sumber Data)
- **Tangki air fisik:** objek yang direpresentasikan, dengan sensor level (ultrasonik), suhu, kekeruhan, dan TDS
- **Pengguna/Operator:** memantau dashboard, mengatur ambang batas, menerima notifikasi
- **Admin:** mengelola pengguna, sensor/tangki, dan meninjau log sistem

b. Sistem Digital Twin (Representasi Digital)
- **Frontend web:** dashboard real-time, visual tangki, grafik, riwayat, pengaturan
- **Backend REST API:** menerima data sensor, autentikasi, pengelolaan tangki, ambang batas, dan notifikasi
- **Database:** menyimpan data sensor, pengguna, konfigurasi tangki, dan log notifikasi
- **Opsi data awal (tanpa perangkat keras):** Python Sensor Simulator yang mengirim data dummy berkala ke API, meniru perilaku sensor nyata (pengisian, pemakaian, fluktuasi kualitas)
- **Rencana integrasi sensor nyata (opsional):** ESP32 + sensor ultrasonik (level), DS18B20 (suhu), sensor turbidity, dan sensor TDS, mengirim data via HTTP/MQTT

c. Fitur Tambahan
- Notifikasi otomatis (in-app/email/Telegram/WhatsApp) saat melewati ambang batas
- Prediksi sederhana: estimasi waktu tangki penuh/habis berdasarkan laju perubahan level
- Kontrol pompa (simulasi on/off otomatis berdasarkan level)
- Ekspor riwayat data (CSV/PDF)
- Dukungan lebih dari satu tangki (multi-tank)

d. Catatan Risiko
- **Keterbatasan perangkat keras:** sensor dapat tidak akurat atau butuh kalibrasi; pada tahap awal digunakan data dummy dan validasi terhadap sensor nyata dilakukan bila perangkat tersedia
- **Keterlambatan data (latency) & koneksi:** data real-time bergantung pada jaringan; perlu penanganan data hilang dan indikator status koneksi sensor
- **Keamanan data:** autentikasi pengguna, validasi input dari sensor, dan pembatasan akses API
- **Pengelolaan waktu:** tim beranggotakan 3 orang, sehingga ruang lingkup dijaga tetap fokus (tiga parameter kondisi air dan satu jenis tangki pada rilis awal)

5. Tech Stack (Rencana Awal)

| Komponen | Teknologi |
|----------|-----------|
| Sumber Data | Python Sensor Simulator / sensor nyata (ESP32) |
| Backend | (isi sesuai kesepakatan tim, contoh: Flask atau Node.js/Express) |
| Database | (contoh: MySQL/PostgreSQL/InfluxDB untuk data time-series) |
| Frontend | HTML + JS + Bootstrap/Tailwind + Chart.js (atau React) |
| Real-time | Polling / WebSocket / MQTT (contoh: Mosquitto) |
| Notifikasi | Email / Telegram Bot API / in-app alert |
| Manajemen Proyek | GitHub & GitHub Projects |
| Komunikasi | HTTP REST API |

6. Rencana Sprint

| Sprint | Bulan | Fokus |
|--------|-------|-------|
| Sp1 | September | Project Charter, perhitungan Function Point, backlog, arsitektur & tech stack, ERD, UX wireframe, setup repo & boilerplate |
| Sp2 | October | Backend (autentikasi, API data sensor) + simulator sensor + dashboard real-time dasar (level air) |
| Sp3 | November | Monitoring kondisi air (suhu, kekeruhan, TDS), grafik tren, ambang batas & notifikasi, refinement |
| Sp4 | December | Testing, riwayat & ekspor data, kontrol pompa/prediksi (opsional), upgrade tampilan |
| Sp5 | December | Final testing, bug fixing, dokumentasi, persiapan demo/presentasi akhir |

7. Anggota Tim

|              Nama                  |        NIM      |                Peran                       |
|------------------------------------|-----------------|--------------------------------------------|
| Dekna Mutiara Ramadhani            |     240504080   | Ketua Tim / Project Manager (Scrum Master) |
| Nur Aimi Nadia Binti Hanafiah      |     240504077   |       System Analyst & UX Designer         |
| Meisya Amelia Lubis                |     240504088   |        Developer & Database Engineer       |
