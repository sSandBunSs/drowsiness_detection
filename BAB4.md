# BAB IV IMPLEMENTASI

## 4.1 Perangkat Keras dan Perangkat Lunak

### 4.1.1 Perangkat Keras
- PC: Windows 10 Pro, Intel Core i7-4790, RAM 10GB, GPU RX550 4GB, SSD 512GB
- Webcam USB
- Raspberry Pi 4 — untuk pengujian platform embedded (**belum dilakukan** per saat draf ini ditulis, memerlukan hardware fisik — lihat `BAB5.md` §5.2)

### 4.1.2 Perangkat Lunak
- Python 3.10 (conda environment `drowsy`)
- OpenCV (`opencv-python` di PC; `opencv-python-headless` direkomendasikan di Raspberry Pi)
- MediaPipe Tasks API (`FaceLandmarker`, model `face_landmarker.task`, 468 titik landmark)
- NumPy, Pandas, Matplotlib (analisis data)

## 4.2 Implementasi Sistem

Rancangan arsitektur pada `BAB3.md` §3.2 diterapkan sebagai modul Python berikut:

- `detector.py` — kelas `DrowsinessDetector` (orkestrasi alur deteksi), fungsi geometri (`compute_ear`, `compute_mar`, `compute_perclos`), kelas `AlarmSystem` dan `Visualizer`.
- `metrics_logger.py` — kelas `MetricsLogger`, menulis metrik per-frame dan event diskrit ke CSV di `logs/`.
- `generate_alarm.py` — skrip mandiri yang mensintesis `sounds/alarm.wav`.

Sistem diimplementasikan dalam Python 3.10, menggunakan MediaPipe Tasks API (`FaceLandmarker`, mode `VIDEO`) dan OpenCV. Parameter awal (`Config` di `detector.py`):

| Parameter | Nilai | Keterangan |
|---|---|---|
| `ear_threshold_base` | 0.25 | Threshold EAR dasar (sebelum kalibrasi adaptif) |
| `ear_consec_frames` | 20 | Frame berturut-turut sebelum status DROWSY |
| `mar_threshold` | 0.65 | Threshold MAR (menguap) |
| `perclos_threshold` | 0.35 | 35% waktu mata tertutup dianggap kantuk |
| `calibration_frames` | 100 | Jumlah frame kalibrasi baseline |

`Config` juga mendeteksi otomatis platform Raspberry Pi via `/proc/device-tree/model` untuk menyesuaikan backend kamera/buffering — bagian dari implementasi rancangan "Skenario platform" di `BAB3.md` §3.3, meski pengujian langsung di hardware RPi4 belum dilakukan.

Hasil pengujian terhadap implementasi ini (akurasi pada dataset gambar, eksperimen adaptive vs fixed threshold, dan pembahasan) disajikan di `BAB5.md`.
