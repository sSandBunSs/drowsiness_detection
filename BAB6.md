# BAB VI KESIMPULAN DAN SARAN

> Status: **draf awal** — kesimpulan final harus ditulis setelah seluruh pengujian di `BAB5.md` §5.2 selesai, sesuai urutan penulisan yang direkomendasikan pada sesi brainstorming (BAB II → III → I → IV → V → VI).

## 6.1 Kesimpulan

Draf sementara berdasarkan temuan saat ini, menjawab rumusan masalah di `BAB1.md` §1.2:

1. Sistem deteksi kantuk berbasis EAR+MAR+PERCLOS dengan MediaPipe Face Mesh berhasil diimplementasikan dan berjalan real-time, dengan dukungan input webcam maupun berkas video (rumusan masalah #1).
2. Threshold EAR tetap (`0.25`) menghasilkan akurasi ~90% pada data yang relatif homogen (val/test) namun turun signifikan (~67%) pada data yang lebih beragam (train) — menunjukkan sensitivitas terhadap variasi wajah/kondisi, mendukung kebutuhan *adaptive threshold*.
3. Eksperimen proksi (dataset gambar, bukan video per-individu — lihat `BAB5.md` §5.3) menunjukkan threshold adaptif yang dikalibrasi dari baseline *populasi* (rata-rata banyak subjek) justru tampil lebih buruk daripada fixed 0,25 (mis. 90,20%→77,40% pada val). Ini **bukan bantahan terhadap adaptive threshold per-pengemudi** — sebaliknya, ini menegaskan bahwa kalibrasi hanya bermakna jika dilakukan per-individu (satu pengemudi, satu sesi), sesuai desain `_calibrate()` di `detector.py`. **Kesimpulan final soal adaptive vs fixed per-pengemudi (rumusan masalah #2) tetap menunggu pengujian video real dengan satu subjek per sesi** (item pertama `BAB5.md` §5.2, belum dilakukan).
4. [Kesimpulan soal performa PC vs Raspberry Pi 4 dan kondisi pencahayaan siang/malam (rumusan masalah #3) — perlu pengujian hardware RPi4 dan sesi rekaman langsung terlebih dahulu.]

## 6.2 Saran

Draf sementara:

1. Penelitian selanjutnya dapat menguji sistem pada populasi pengemudi yang lebih besar dan beragam (etnis, usia, penggunaan kacamata/sunglasses).
2. Integrasi dengan sensor tambahan (mis. pola kemudi, sensor fisiologis) dapat menjadi arah lanjutan tanpa mengubah scope penelitian menjadi S2/S3, selama tetap dalam kerangka evaluasi/kombinasi metode yang sudah ada (lihat `BAB2.md`/diskusi batas S1 pada `first_brainstorm.pdf`).
3. [Saran lain setelah `BAB5.md` final.]
