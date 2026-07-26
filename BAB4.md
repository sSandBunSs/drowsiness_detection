# BAB IV IMPLEMENTASI

## 4.1 Perangkat Keras dan Perangkat Lunak

### 4.1.1 Perangkat Keras
- PC: Ubuntu 24.04 LTS (WSL2), Intel Core i5-12450H, RAM 12GB
- Webcam USB (pengembangan awal); video berkas untuk pengujian performa §5.2.3 (video sumber sama dipakai di kedua platform, lihat `BAB3.md` §3.3)
- Raspberry Pi 4 (aarch64) — akses hardware fisik tidak tersedia; performa RPi4 diestimasi melalui AWS EC2 `a1.medium` (core ARM Cortex-A72, identik dengan core RPi4/BCM2711 — diverifikasi via `lscpu`) menjalankan pipeline deteksi identik dengan `mediapipe==0.10.18` — lihat metodologi lengkap (termasuk percobaan emulasi QEMU dan ARM64 native runner yang ditolak karena tidak representatif) di `BAB5.md` §5.2.3

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

`Config` juga mendeteksi otomatis platform Raspberry Pi via `/proc/device-tree/model` untuk menyesuaikan backend kamera/buffering — bagian dari implementasi rancangan "Skenario platform" di `BAB3.md` §3.3. Pengujian langsung di hardware RPi4 fisik belum dilakukan (akses tidak tersedia); performa platform aarch64 diestimasi melalui proksi core Cortex-A72 (AWS EC2 `a1.medium`, lihat `BAB5.md` §5.2.3).

Hasil pengujian terhadap implementasi ini (akurasi pada dataset gambar, eksperimen adaptive vs fixed threshold, dan pembahasan) disajikan di `BAB5.md`.
