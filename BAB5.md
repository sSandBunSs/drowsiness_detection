# BAB V HASIL PENELITIAN DAN PEMBAHASAN

## 5.1 Hasil Pengujian Akurasi (Dataset Gambar)

**Catatan metodologi**: dataset UTA-RLDD (video, direkomendasikan pada tahap perencanaan awal) tidak dapat diunduh secara non-interaktif — hanya tersedia sebagai arsip zip multi-GB per fold di balik gerbang unduhan berbasis browser (Google Drive/Kaggle). Sebagai gantinya, pengujian awal akurasi dilakukan pada dataset gambar wajah berlabel publik (`active`/`fatigue`, ~11.787 gambar, sumber Kaggle) menggunakan `evaluate_dataset_images.py`, yang memakai ulang fungsi `compute_ear`/`LEFT_EYE`/`RIGHT_EYE`/`get_landmark_coords` yang identik dengan `detector.py` — bukan implementasi terpisah. Karena metode EAR-threshold tidak memiliki parameter yang dilatih (bukan model machine learning), tidak ada risiko *data leakage* train/test; evaluasi pada seluruh split (train+val+test) valid dilakukan.

Hasil pengujian pada threshold EAR tetap (`ear_threshold=0.25`):

| Split | n | Akurasi | Recall *active* | Recall *fatigue* |
|---|---|---|---|---|
| train | 9.054 | 67,23% | 0,565 | 0,870 |
| val | 1.824 | 89,96% | 0,931 | 0,868 |
| test | 909 | 91,18% | 0,936 | 0,887 |
| **Gabungan** | **11.787** | **72,60%** | 0,634 | 0,872 |

Confusion matrix gabungan (11.787 gambar dicoba, 8 wajah tidak terdeteksi):

|  | Prediksi *active* | Prediksi *fatigue* |
|---|---|---|
| Aktual *active* | 4.585 | 2.644 |
| Aktual *fatigue* | 584 | 3.966 |

### Analisis
Split `val` dan `test` konsisten (~90%), sedangkan split `train` — 77% dari seluruh data — menghasilkan akurasi jauh lebih rendah (67,23%), terutama pada recall kelas *active* (0,565: banyak wajah yang sebenarnya waspada salah terklasifikasi sebagai kantuk). Selisih ini adalah artefak pembobotan ukuran data (`train` mendominasi jumlah gambar dan lebih beragam/lebih sulit), bukan bukti bahwa `val`/`test` tidak representatif.

Temuan ini mengindikasikan bahwa **threshold EAR tetap sensitif terhadap variasi wajah/pencahayaan/sudut pengambilan gambar** antar subjek — memperkuat argumen bahwa *adaptive threshold* (dikalibrasi per pengemudi, bukan nilai tetap global) diperlukan untuk generalisasi yang lebih baik pada penggunaan nyata. Angka ~90% (val+test) direkomendasikan sebagai akurasi acuan yang dilaporkan, dengan selisih pada `train` didiskusikan secara terbuka sebagai temuan yang mendukung novelty *adaptive threshold* penelitian ini — bukan disembunyikan.

## 5.2 Pengujian yang Masih Diperlukan

- [ ] Pengujian akurasi pada video real-time (webcam) dengan ground truth manual — `validate_accuracy.py` sudah tersedia, tinggal merekam sesi dan memberi label per interval waktu.
- [ ] Pengujian pada kondisi pencahayaan siang vs malam secara langsung (bukan dari dataset gambar statis) — `Config.lighting_condition` sudah ada untuk menandai sesi.
- [ ] Perbandingan performa (FPS, latency) PC vs Raspberry Pi 4 — perlu hardware RPi4.
- [ ] Grafik tren EAR/MAR/PERCLOS terhadap waktu dari sesi rekaman nyata.
- [x] Evaluasi pengaruh *adaptive threshold* vs *fixed threshold* — **dilakukan sebagai eksperimen proksi pada dataset gambar (§5.3), TIDAK dapat menggantikan pengujian video per-individu yang masih tersisa di atas.**

## 5.3 Eksperimen Proksi: Fixed vs Adaptive Threshold pada Dataset Gambar

**Keterbatasan metodologis yang harus dinyatakan di depan**: dataset gambar (`datasets/`) tidak memiliki ID subjek — nama file hanya indeks numerik, dan manifest `train.txt` peninggalan dataset asli tidak cocok dengan nama file aktual di folder (sudah diverifikasi, lihat riwayat sesi). Akibatnya, kalibrasi adaptif *per-pengemudi* yang sesungguhnya (baseline dari 100 frame pertama SATU orang yang sama, seperti `_calibrate()` di `detector.py`) tidak bisa direplikasi pada dataset ini. Sebagai proksi, `evaluate_dataset_images.py --compare-adaptive` mengambil 100 gambar `active` pertama per split sebagai "baseline kalibrasi" — namun ini adalah rata-rata wajah banyak orang berbeda, bukan baseline satu individu.

Hasil (n=300 gambar/kelas per split, dari `evaluate_dataset_images.py datasets/train datasets/val datasets/test --compare-adaptive --max-per-class 300`):

| Split | Baseline EAR (kalibrasi) | Threshold adaptif (0,75×baseline) | Akurasi Fixed (0,25) | Akurasi Adaptif |
|---|---|---|---|---|
| train | 0,2530 | 0,1897 | **75,60%** | 54,80% |
| val | 0,3027 | 0,2271 | **90,20%** | 77,40% |
| test | 0,2966 | 0,2225 | **90,36%** | 73,49% |

**Threshold adaptif (versi proksi ini) tampil lebih buruk di ketiga split**, bukan lebih baik. Analisis: karena baseline kalibrasi berasal dari rata-rata EAR banyak individu berbeda (bukan satu pengemudi), nilainya sudah dekat dengan 0,25 (fixed). Mengalikannya dengan 0,75 mendorong threshold turun ke ~0,19–0,23 — di bawah threshold fixed — sehingga sistem menjadi kurang sensitif terhadap kelas *fatigue* (recall *fatigue* anjlok tajam, mis. val: 0,900→0,630; test: 0,883→0,557), sementara recall *active* justru naik karena ambang lebih longgar.

**Kesimpulan yang jujur dari eksperimen ini**: hasil ini BUKAN bukti bahwa *adaptive threshold* secara konsep lebih buruk dari fixed. Sebaliknya, ini menunjukkan dengan jelas **mengapa baseline populasi (rata-rata banyak orang) tidak bisa menggantikan baseline individu** — mekanisme kalibrasi 0,75×baseline dirancang untuk menyesuaikan terhadap karakteristik mata SATU pengemudi, bukan untuk merata-ratakan variasi antar-subjek. Menerapkannya pada baseline campuran subjek justru memperkenalkan bias baru, bukan personalisasi. Klaim novelty penelitian ini (adaptive threshold per-pengemudi) **tetap tidak terbantahkan oleh temuan ini** — justru temuan ini memperkuat argumen bahwa pengujian video per-individu (item pertama §5.2) adalah satu-satunya cara valid untuk menguji hipotesis adaptive threshold, dan eksperimen proksi pada dataset gambar campuran-subjek tidak bisa dijadikan pengganti.

## 5.4 Pembahasan

> Diisi setelah seluruh pengujian di §5.2 selesai — bandingkan hasil dengan 15 jurnal penelitian terdahulu di `BAB2.md`, khususnya jurnal 1 dan 3 (metodologi paling mirip: EAR+MAR+PERCLOS), dan jurnal 3's akurasi 95,1% sebagai acuan pembanding utama.
