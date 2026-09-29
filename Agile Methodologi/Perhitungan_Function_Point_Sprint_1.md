# Perhitungan Function Point – Sprint 1

## Daftar Fitur & Perhitungan UFC

| No. | Nama Fungsi | Jenis | Tingkat Kerumitan | Bobot |
| --- | --- | --- | --- | --- |
| 1 | Input data konfigurasi tangki (kapasitas, tinggi, diameter) | EI | Sederhana | 3 |
| 2 | Input data sensor (ketinggian, suhu, kualitas, data simulasi) | EI | Sedang | 4 |
| 3 | Tampilan visualisasi tangki & level air | EO | Sedang | 5 |
| 4 | Dashboard status & indikator kualitas air | EO | Sedang | 5 |
| 5 | Tampilan notifikasi batas kritis / anomali | EO | Sederhana | 4 |
| 6 | Lihat riwayat data pengukuran | EQ | Sederhana | 3 |
| 7 | Cari data berdasarkan rentang waktu | EQ | Sedang | 4 |
| 8 | Simpan data konfigurasi & pengguna | ILF | Sederhana | 7 |
| 9 | Simpan rekaman data sensor | ILF | Sedang | 10 |
| 10 | Simpan catatan notifikasi | ILF | Sederhana | 7 |
| 11 | Ambil data dari simulasi API sensor | EIF | Sederhana | 5 |
| | **TOTAL UFC** | | | **57** |

## Penilaian 14 Faktor Penyesuaian

| No. | Faktor Pengaruh Sistem | Nilai (0–5) |
| --- | --- | --- |
| 1 | Komunikasi data | 2 |
| 2 | Fungsi terdistribusi | 1 |
| 3 | Kinerja | 2 |
| 4 | Konfigurasi perangkat keras | 1 |
| 5 | Tingkat transaksi | 2 |
| 6 | Masukan data pengguna | 2 |
| 7 | Kemudahan efisiensi pengguna | 3 |
| 8 | Pembaruan data langsung | 2 |
| 9 | Kompleksitas pemrosesan | 2 |
| 10 | Penggunaan kembali | 2 |
| 11 | Kemudahan instalasi | 2 |
| 12 | Kemudahan operasi | 3 |
| 13 | Banyaknya perangkat | 1 |
| 14 | Kemudahan perubahan | 3 |
| | **JUMLAH ΣF** | **28** |

**Perhitungan VAF:**

```
VAF = 0,65 + (0,01 × ΣF)
    = 0,65 + (0,01 × 28)
    = 0,65 + 0,28
    = 0,93
```

## Hasil Akhir Function Point

```
FP  = UFC × VAF
    = 57 × 0,93
    = 53,01
```

## Kesimpulan

Ukuran fungsional proyek **Perancangan Digital Twin Tangki Air untuk Monitoring Ketinggian dan Kondisi Air Secara Real-Time** pada tahap Sprint 1 adalah **53,01 Function Point**.

Nilai ini mencerminkan cakupan pekerjaan yang wajar untuk proyek mahasiswa: pemantauan data, visualisasi, notifikasi, penyimpanan riwayat, dan koneksi data simulasi sesuai tujuan dan ruang lingkup yang disepakati.
