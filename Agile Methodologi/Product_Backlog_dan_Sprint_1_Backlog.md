# Product Backlog & Sprint 1 Backlog

**Proyek:** Perancangan Digital Twin Tangki Air untuk Monitoring Ketinggian dan Kondisi Air Secara Real-Time

---

## 1. Product Backlog

Prioritas: **Tinggi** = fondasi/inti sistem, **Sedang** = fitur pendukung, **Rendah** = pengembangan lanjutan.
Bobot FP diambil dari perhitungan Function Point Sprint 1 (UFC).

| ID | Fitur | User Story | Jenis FP | Bobot FP | Prioritas | Sprint |
| --- | --- | --- | --- | --- | --- | --- |
| PBI-01 | Konfigurasi tangki | Sebagai operator, saya ingin memasukkan kapasitas, tinggi, dan diameter tangki agar model digital sesuai tangki asli. | EI | 3 | Tinggi | 1 |
| PBI-02 | Input data sensor | Sebagai sistem, saya ingin menerima data ketinggian, suhu, dan kualitas air agar kondisi tangki dapat dipantau. | EI | 4 | Tinggi | 1 |
| PBI-03 | Visualisasi tangki & level air | Sebagai operator, saya ingin melihat gambar tangki dengan level air yang bergerak sesuai data agar kondisi air mudah dipahami. | EO | 5 | Tinggi | 1 |
| PBI-04 | Dashboard status & kualitas air | Sebagai operator, saya ingin melihat ringkasan status dan indikator kualitas air dalam satu halaman. | EO | 5 | Tinggi | 1 |
| PBI-05 | Notifikasi batas kritis / anomali | Sebagai operator, saya ingin mendapat peringatan saat air terlalu rendah, terlalu tinggi, atau kualitas menurun agar dapat segera bertindak. | EO | 4 | Tinggi | 1 |
| PBI-06 | Riwayat data pengukuran | Sebagai operator, saya ingin melihat riwayat pengukuran untuk memantau perubahan dari waktu ke waktu. | EQ | 3 | Sedang | 1 |
| PBI-07 | Pencarian berdasarkan rentang waktu | Sebagai operator, saya ingin menyaring data berdasarkan tanggal/jam agar mudah menemukan data tertentu. | EQ | 4 | Sedang | 1 |
| PBI-08 | Penyimpanan konfigurasi & pengguna | Sebagai sistem, saya ingin menyimpan data konfigurasi tangki dan pengguna agar tidak hilang. | ILF | 7 | Tinggi | 1 |
| PBI-09 | Penyimpanan rekaman data sensor | Sebagai sistem, saya ingin menyimpan setiap rekaman sensor sebagai dasar riwayat dan analisis. | ILF | 10 | Tinggi | 1 |
| PBI-10 | Penyimpanan catatan notifikasi | Sebagai sistem, saya ingin menyimpan log notifikasi agar kejadian anomali dapat ditelusuri. | ILF | 7 | Sedang | 1 |
| PBI-11 | Pengambilan data dari API simulasi sensor | Sebagai sistem, saya ingin mengambil data dari API simulasi agar pengembangan bisa berjalan tanpa sensor fisik. | EIF | 5 | Tinggi | 1 |
| PBI-12 | Login & manajemen peran pengguna | Sebagai admin, saya ingin mengatur akun dan hak akses agar sistem aman. | – | TBD | Sedang | 2 |
| PBI-13 | Grafik tren ketinggian & kualitas air | Sebagai operator, saya ingin melihat grafik tren agar pola perubahan terlihat jelas. | – | TBD | Sedang | 2 |
| PBI-14 | Ekspor laporan (CSV/PDF) | Sebagai operator, saya ingin mengunduh data riwayat sebagai laporan. | – | TBD | Sedang | 2 |
| PBI-15 | Pengaturan ambang batas notifikasi | Sebagai admin, saya ingin mengubah batas kritis sendiri tanpa mengubah kode. | – | TBD | Sedang | 2 |
| PBI-16 | Integrasi sensor fisik (mis. ESP32/MQTT) | Sebagai sistem, saya ingin menerima data dari sensor sungguhan menggantikan simulasi. | – | TBD | Rendah | 3 |
| PBI-17 | Prediksi waktu tangki habis/penuh | Sebagai operator, saya ingin perkiraan kapan tangki kosong/penuh agar bisa merencanakan pengisian. | – | TBD | Rendah | 3 |
| PBI-18 | Visualisasi 3D tangki | Sebagai operator, saya ingin tampilan 3D yang lebih realistis sebagai digital twin. | – | TBD | Rendah | 3 |
| PBI-19 | Pengujian menyeluruh & dokumentasi akhir | Sebagai tim, kami ingin sistem teruji dan terdokumentasi untuk penyerahan proyek. | – | TBD | Tinggi | 3 |

> Sprint 2 dan 3 bersifat rencana awal dan dapat disesuaikan setelah Sprint Review.

---

## 2. Sprint 1 Backlog

### Sprint Goal

Menghasilkan versi awal sistem yang dapat menerima data simulasi sensor, menyimpannya, menampilkannya pada visualisasi tangki dan dashboard, serta memberi notifikasi saat kondisi kritis.

### Ringkasan

| Item | Keterangan |
| --- | --- |
| Jumlah PBI | 11 (PBI-01 s.d. PBI-11) |
| Ukuran fungsional | UFC 57 → **53,01 FP** (VAF 0,93) |
| Total estimasi tugas | 108 jam |
| Durasi sprint | 2 minggu *(asumsi, sesuaikan dengan jadwal tim)* |

### Daftar Tugas

Urutan tugas mengikuti ketergantungan: database dan simulator dulu, lalu fitur yang memakainya.

| ID Tugas | PBI | Tugas | Estimasi (jam) | Status |
| --- | --- | --- | --- | --- |
| T-01 | PBI-08 | Merancang skema database (konfigurasi, pengguna, sensor, notifikasi) | 4 | To Do |
| T-02 | PBI-08 | Membuat tabel & model konfigurasi tangki dan pengguna | 4 | To Do |
| T-03 | PBI-09 | Membuat tabel rekaman sensor beserta indeks waktu | 4 | To Do |
| T-04 | PBI-10 | Membuat tabel catatan notifikasi | 3 | To Do |
| T-05 | PBI-11 | Membuat API simulasi sensor (ketinggian, suhu, kualitas air) | 8 | To Do |
| T-06 | PBI-11 | Membuat layanan pengambilan data berkala dari API simulasi | 6 | To Do |
| T-07 | PBI-01 | Membuat form konfigurasi tangki dengan validasi | 6 | To Do |
| T-08 | PBI-01 | Menyimpan dan mengubah konfigurasi tangki ke database | 3 | To Do |
| T-09 | PBI-02 | Membuat proses input data sensor dengan validasi | 6 | To Do |
| T-10 | PBI-02 | Menyimpan rekaman sensor ke database | 3 | To Do |
| T-11 | PBI-03 | Membuat model visualisasi tangki | 10 | To Do |
| T-12 | PBI-03 | Menghubungkan level air pada visualisasi dengan data real-time | 6 | To Do |
| T-13 | PBI-04 | Membuat tata letak halaman dashboard | 6 | To Do |
| T-14 | PBI-04 | Membuat indikator kualitas air (suhu dan parameter kualitas) | 6 | To Do |
| T-15 | PBI-05 | Membuat logika ambang batas dan deteksi anomali | 6 | To Do |
| T-16 | PBI-05 | Menampilkan notifikasi di antarmuka dan menyimpannya ke log | 5 | To Do |
| T-17 | PBI-06 | Membuat halaman tabel riwayat pengukuran | 5 | To Do |
| T-18 | PBI-07 | Menambahkan filter rentang waktu pada riwayat | 5 | To Do |
| T-19 | Umum | Pengujian fungsional seluruh fitur Sprint 1 | 8 | To Do |
| T-20 | Umum | Integrasi akhir dan persiapan demo Sprint Review | 4 | To Do |
| | | **TOTAL** | **108** | |

### Definition of Done

- Fitur berjalan sesuai user story dan lolos pengujian fungsional.
- Data tersimpan dan dapat ditampilkan kembali dengan benar.
- Tidak ada kesalahan kritis (error) yang tersisa pada alur utama.
- Kode tersimpan di repositori bersama.
- Fitur dapat didemokan pada Sprint Review.

### Catatan

- Kolom penanggung jawab (PIC) belum diisi karena anggota tim belum diketahui; bisa ditambahkan.
- Estimasi jam adalah perkiraan awal dan sebaiknya dikonfirmasi bersama tim pada Sprint Planning.
- Isi Sprint 2 dan 3 adalah usulan; bobot FP-nya baru bisa dihitung setelah fitur dirinci.
