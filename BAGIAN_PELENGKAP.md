# BAGIAN PELENGKAP

> **Sumber resmi**: `PEDOMAN TA FTII 2022 v1.1.pdf` (Pedoman Penyusunan Tugas Akhir, Fakultas Teknologi Informasi Dan Industri, Universitas Stikubank/UNISBANK Semarang, Januari 2022). Program studi: **Teknik Informatika**. Sudah dianalisis penuh (59 halaman) — lihat riwayat sesi untuk triase detail.

## Halaman Depan (isi manual, ikuti template resmi kampus)

- Judul skripsi: *Implementasi Sistem Deteksi Kantuk Pengemudi Secara Real-Time Berbasis Eye Aspect Ratio, Mouth Aspect Ratio, dan PERCLOS dengan Adaptive Threshold Menggunakan MediaPipe Face Mesh*
- Nama lengkap & NIM: `[isi]`
- Nama Ketua Program Studi & NIDN: `[isi]`
- Nama Dosen Pembimbing & NIDN: `[isi]`
- Tanggal: `[isi]`

Format halaman judul, halaman pengesahan, halaman pernyataan kesiapan ujian, dan lembar bimbingan mengikuti Lampiran 4a, 5, 6a, dan lampiran lembar bimbingan pada pedoman resmi (lihat PDF sumber di atas untuk contoh lengkap). Logo UNISBANK harus hitam-putih.

## Sudah Dikonfirmasi dari Pedoman Resmi (tidak perlu tanya dosen lagi)

- ✅ **Format sitasi: APA** (nama-tahun), bukan IEEE. Kutipan langsung: `(Nama, tahun, hal.)`; parafrase: `(Nama, tahun)`. 3+ penulis: sebutkan semua di sitasi pertama, lalu **"nama pertama dkk."** (bukan "et al.") di sitasi berikutnya. Nama Indonesia tanpa marga: pakai nama diri apa adanya (lihat pedoman §5.2.5b).
- ✅ **Font & spasi**: Times New Roman, seluruh naskah kecuali judul/sub-judul. Spasi 2 (double) untuk teks utama.
- ✅ **Margin**: kiri 4cm, kanan 3cm, atas 4cm, bawah 3cm. Kertas HVS A4 min. 70gsm.
- ✅ **Kertas & warna sampul**: hardcover, kertas buffalo, **biru muda** (Teknik Informatika, S1).
- ✅ **Struktur bab**: 6 bab (Penelitian Pengembangan Sistem) — lihat Peta Berkas Bab di bawah. Sudah direstrukturisasi dari draf 5-bab sebelumnya.
- ✅ **Penomoran halaman**: bagian awal (judul s.d. daftar lampiran) — angka romawi kecil, tengah-bawah. Bagian pokok (BAB I dst.) — angka Arab mulai dari 1, tengah-bawah, 1,5cm dari bawah.
- ✅ **Judul bab/sub-bab**: HURUF KAPITAL SEMUA. Nomor bab: angka Romawi. Nomor sub-bab: angka Arab desimal.
- ✅ **Gambar**: judul di **bawah** gambar, format `<no bab>.<no urut>. Judul gambar`, rata tengah. **Tabel**: judul di **atas** tabel, format sama.
- ✅ **Bimbingan**: minimal 8x konsultasi per semester dengan dosen pembimbing; direkam di Lembar Bimbingan.

## Hal yang Masih Perlu Dikonfirmasi ke Dosen Pembimbing

- [ ] Jumlah minimal subjek pengujian video (pedoman tidak menetapkan angka spesifik untuk penelitian jenis ini)
- [ ] Template Word resmi dari kampus (kalau ada versi `.docx` terbaru selain contoh di PDF pedoman)
- [ ] Nama Ketua Program Studi, Dekan FTII, dan susunan Tim Dosen Penguji (untuk halaman pengesahan)

## Naskah Publikasi (WAJIB, terpisah dari laporan TA)

> Per Surat Edaran Ditjen Dikti No. 152/E/T/2012 — wajib bagi lulusan S1 untuk publikasi di jurnal non-terakreditasi. **Draf teks sudah lengkap** di `NASKAH_TA_LENGKAP.md` §Naskah Publikasi (Judul, Abstrak, §1–§6, Daftar Pustaka) dengan angka hasil nyata dari BAB V §5.1–§5.3. Yang tersisa hanya pemformatan/pemisahan ke berkas `.doc` terpisah dan kelengkapan tanda tangan.

- [x] Draf naskah publikasi, teks lengkap tersedia di `NASKAH_TA_LENGKAP.md` §Naskah Publikasi — [ ] masih perlu dipisah jadi berkas `.doc` tersendiri (6–10 halaman, A4, margin 2cm semua sisi, spasi 1, Times New Roman 10pt).
- [x] Judul naskah ≤10 kata, berbeda dari judul skripsi, berbahasa Indonesia — "Deteksi Kantuk Pengemudi Real-Time dengan Adaptive Threshold EAR".
- [x] Struktur lengkap: Abstrak + Kata Kunci → 1. Pendahuluan → 2. Tinjauan Pustaka → 3. Metode Penelitian → 4. Hasil dan Pembahasan → 5. Kesimpulan → 6. Saran → Daftar Pustaka.
- [ ] Gambar wajib format JPG/PNG (bukan objek Office), diberi judul dengan kata "Gambar". Tabel wajib tabel native Word (bukan gambar/objek), diberi judul dengan kata "Tabel". Sub-bab dibatasi maksimal 2 level — berlaku saat konversi Markdown → Word.
- [ ] Halaman cover, lembar pengesahan (ditandatangani pembimbing), dan lembar pernyataan (setuju/tidak setuju publikasi dengan/tanpa co-author pembimbing) — format di Lampiran 11 pedoman.

## Daftar Pustaka (Sementara)

Lihat daftar 15 referensi di `BAB2.md` §2.1 — perlu diverifikasi ulang (DOI/link penuh) sebelum dijadikan final. Format entri mengikuti kaidah APA pedoman (§5.2.4): urut abjad nama belakang penulis pertama, spasi tunggal dalam satu entri, 1,5 spasi antar entri, baris pertama rata kiri dan baris berikutnya menjorok (*hanging indent*).

## Lampiran

Draf lengkap ada di `LAMPIRAN.md` (Lampiran A–F) — siap disalin ke berkas
Word lampiran.

- [x] Listing kode sumber (`detector.py`, `metrics_logger.py`, dst.) — `LAMPIRAN.md` Lampiran A (manifest 8 berkas, 1.343 baris total; salin isi berkas ke Word)
- [x] Contoh CSV hasil logging (`logs/metrics_*.csv`, `logs/events_*.csv`) — `LAMPIRAN.md` Lampiran B (potongan nyata dari sesi siang)
- [ ] Screenshot antarmuka sistem — `LAMPIRAN.md` Lampiran C; **belum bisa dihasilkan otomatis** (sandbox tanpa webcam/display), perlu diambil manual saat `python detector.py` berjalan di PC/RPi nyata (tekan `s`)
- [x] Ground truth dan hasil validasi (output `validate_accuracy.py`) — `LAMPIRAN.md` Lampiran D (output nyata, akurasi 62,59% cocok dengan BAB V §5.2.1)
- [ ] Surat Pernyataan Keaslian Tugas Akhir (didapat saat ujian TA, tidak dibuat sendiri) — `LAMPIRAN.md` Lampiran E
- [x] Surat Keterangan dari perusahaan/instansi — tidak berlaku, dinyatakan eksplisit di `LAMPIRAN.md` Lampiran F

## Peta Berkas Bab

| Berkas | Isi |
|---|---|
| `BAB1.md` | Pendahuluan |
| `BAB2.md` | Tinjauan Pustaka |
| `BAB3.md` | Analisis dan Rancangan Sistem |
| `BAB4.md` | Implementasi |
| `BAB5.md` | Hasil Penelitian dan Pembahasan |
| `BAB6.md` | Kesimpulan dan Saran |
| `BAGIAN_PELENGKAP.md` | Berkas ini — halaman depan, naskah publikasi, lampiran, daftar pustaka |
| `LAMPIRAN.md` | Draf isi Lampiran A–F (listing kode, contoh CSV, ground truth + output validasi, dll.) |
| `PEDOMAN TA FTII 2022 v1.1.pdf` | Sumber kebenaran format/struktur resmi kampus |
