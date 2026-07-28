# LAMPIRAN

> Konten untuk item lampiran wajib di `BAGIAN_PELENGKAP.md` §Lampiran. Data di
> bawah diambil langsung dari berkas nyata di repo ini (bukan contoh
> buatan) — path lengkap dicantumkan di setiap bagian agar bisa diverifikasi
> ulang.

## Lampiran A — Listing Kode Sumber

Sumber lengkap ada di berkas berikut (root repo, bukan `src/` — lihat catatan
di `CLAUDE.md`). Salin isi berkas ini langsung ke lampiran Word, gunakan font
Courier New/Consolas ukuran kecil (mis. 9pt) dan penomoran baris jika pedoman
kampus mensyaratkannya.

**Sistem inti:**

| Berkas | Baris | Isi |
|---|---|---|
| `detector.py` | 639 | `Config`, `DetectionState`, fungsi geometri (EAR/MAR/PERCLOS), `AlarmSystem`, `Visualizer`, `DrowsinessDetector` — logika utama sistem |
| `metrics_logger.py` | 60 | `MetricsLogger` — penulisan CSV per-frame dan event ke `logs/` |
| `generate_alarm.py` | 33 | Sintesis `sounds/alarm.wav` (beep 1kHz) |

**Tooling penelitian (validasi & analisis, dirujuk di BAB V):**

| Berkas | Baris | Isi |
|---|---|---|
| `validate_accuracy.py` | 111 | Confusion matrix video vs ground truth manual (§5.2.1, §5.2.2, §5.2.5) |
| `evaluate_dataset_images.py` | 223 | Evaluasi threshold EAR pada dataset gambar (§5.1, §5.3) |
| `plot_trends.py` | 63 | Grafik tren EAR/MAR/PERCLOS dengan interval DROWSY diarsir (§5.2.4, Gambar 5.1/5.2) |
| `compare_adaptive_fixed.py` | 94 | Perbandingan berpasangan adaptive vs fixed threshold (§5.2.5) |
| `benchmark.py` | 120 | Pengukuran FPS/latency PC vs RPi4 (§5.2.3) |

Total: 1.343 baris kode Python (stdlib + OpenCV + MediaPipe + NumPy, tanpa
framework tambahan).

## Lampiran B — Contoh CSV Hasil Logging

Skema kolom didefinisikan di `metrics_logger.py` (lihat `CLAUDE.md`). Contoh
di bawah adalah 5 baris pertama dari sesi siang (`logs/metrics_20260713_230527.csv`,
8.720 baris total) dan `logs/events_20260713_230527.csv` (log event
`CALIBRATED`/`DROWSY`/`YAWN`) — bukan data sintetis.

**`logs/metrics_20260713_230527.csv`** (potongan, header + 5 baris pertama dari 8.720):

```
timestamp,elapsed_sec,ear_left,ear_right,ear_avg,mar,perclos,status,ear_counter,mar_counter,platform,lighting_condition
23:05:29.728,2.482,0.4115,0.4,0.4057,0.3842,0.0,NORMAL,0,0,Windows,unspecified
23:05:29.820,2.574,0.4115,0.4134,0.4124,0.3842,0.0,NORMAL,0,0,Windows,unspecified
23:05:29.850,2.604,0.3946,0.3987,0.3966,0.3754,0.0,NORMAL,0,0,Windows,unspecified
23:05:29.921,2.675,0.3967,0.398,0.3973,0.3882,0.0,NORMAL,0,0,Windows,unspecified
23:05:29.956,2.71,0.3819,0.3893,0.3856,0.3881,0.0,NORMAL,0,0,Windows,unspecified
```

**`logs/events_20260713_230527.csv`** (potongan, header + 5 baris pertama):

```
timestamp,elapsed_sec,event_type,value
23:05:33.132,5.886,CALIBRATED,baseline=0.401 threshold=0.301
23:07:35.008,127.761,DROWSY,EAR=0.302 frames=28
23:07:37.103,129.856,DROWSY,EAR=0.304 frames=31
23:07:44.714,137.468,DROWSY,EAR=0.308 frames=23
23:07:53.542,146.295,DROWSY,EAR=0.303 frames=20
```

Berkas lengkap tersedia untuk seluruh sesi pengujian di `logs/metrics_*.csv` /
`logs/events_*.csv` (6 sesi, lihat `BAB5.md` §5.2.1–§5.2.5 untuk sesi mana yang
dipakai pada masing-masing hasil).

## Lampiran C — Screenshot Antarmuka Sistem

🔶 **Belum bisa dihasilkan dari sesi ini** — sandbox pengembangan ini tidak
punya webcam/display fisik, dan `FaceLandmarker` di lingkungan headless
memerlukan library GLES yang tidak terpasang (lihat catatan headless di
`CLAUDE.md`; instalasi paket sistem untuk mengatasinya butuh persetujuan
eksplisit, dan hasilnya tetap bukan tangkapan layar UI yang autentik).

**Cara mengambil sendiri (di PC Windows/RPi Anda, dengan display nyata)**:
jalankan `python detector.py`, tunggu hingga kalibrasi selesai dan status
`NORMAL`/`WARNING`/`DROWSY` terlihat pada HUD, lalu tekan **`s`** — sistem
otomatis menyimpan `logs/screenshot_<timestamp>.jpg` (lihat `detector.py`
baris ~597). Ambil minimal satu screenshot per status (`NORMAL`, `WARNING`,
`DROWSY`) agar lampiran menunjukkan seluruh state HUD.

## Lampiran D — Ground Truth dan Hasil Validasi

`ground_truth.csv` (sesi siang, dipakai di §5.2.1/§5.2.5):

```
start_sec,end_sec,label
0,120,NORMAL
120,180,DROWSY
180,240,WARNING
240,301,NORMAL
```

`ground_truth_malam.csv` (sesi malam, dipakai di §5.2.2):

```
start_sec,end_sec,label
0,120,NORMAL
120,180,DROWSY
180,240,WARNING
240,266,NORMAL
```

Output nyata `python validate_accuracy.py logs/metrics_20260713_230527.csv ground_truth.csv`
(angka ini identik dengan yang dilaporkan di `BAB5.md` §5.2.1):

```
Total frame dinilai: 8714
Frame diabaikan (di luar ground truth): 5
Akurasi keseluruhan: 62.59%

Confusion matrix (baris=aktual, kolom=prediksi):
            NORMAL   WARNING    DROWSY
  NORMAL      4929       123        62
 WARNING       477        64      1259
  DROWSY      1236       103       461

Per-kelas (precision/recall/F1):
    NORMAL: precision=0.742  recall=0.964  f1=0.839
   WARNING: precision=0.221  recall=0.036  f1=0.061
    DROWSY: precision=0.259  recall=0.256  f1=0.257

DROWSY vs lainnya (biner, metrik keselamatan utama):
  TP=461 FN=1339 FP=1321 TN=5593
  Recall (sensitivity) = 0.256  <- proporsi kejadian kantuk aktual yang terdeteksi
  Precision            = 0.259  <- proporsi alarm kantuk yang benar
```

## Lampiran E — Surat Pernyataan Keaslian Tugas Akhir

Diperoleh dan ditandatangani saat ujian TA sesuai format kampus — tidak
dibuat/diisi di dokumen ini.

## Lampiran F — Surat Keterangan Perusahaan/Instansi

Tidak berlaku. Penelitian ini tidak melibatkan pengembangan sistem untuk
perusahaan/instansi eksternal (lihat `BAGIAN_PELENGKAP.md`).
