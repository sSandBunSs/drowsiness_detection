# 🚗 Drowsiness Detection System
### Deteksi Kantuk Pengemudi Berbasis MediaPipe Face Mesh

> Sistem deteksi kantuk real-time menggunakan **EAR (Eye Aspect Ratio)**,
> **MAR (Mouth Aspect Ratio)**, dan **PERCLOS** dengan **Adaptive Threshold**.
> Kompatibel dengan **Windows 10** (PC/Laptop) dan **Raspberry Pi 4**.

---

## 📁 Struktur Project

```
drowsiness_detection/
├── src/
│   ├── detector.py          ← Program utama
│   ├── metrics_logger.py    ← Logger data untuk penelitian
│   └── generate_alarm.py    ← Generator file alarm.wav
├── sounds/
│   └── alarm.wav            ← (dibuat otomatis)
├── logs/                    ← Screenshot, video, CSV data
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup di Windows 10 (VSCode + Miniconda)

### 1. Buat environment Conda
```bash
conda create -n drowsy python=3.10 -y
conda activate drowsy
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate file alarm
```bash
cd src
python generate_alarm.py
cd ..
```

### 4. Jalankan program
```bash
python src/detector.py
```

### 5. Di VSCode
- Buka folder `drowsiness_detection`
- Pilih interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter" → pilih `drowsy`
- Jalankan `src/detector.py` dengan tombol ▶️ atau `F5`

---

## 🍓 Setup di Raspberry Pi 4

### Persiapan OS
- Gunakan **Raspberry Pi OS (64-bit)** terbaru
- Pastikan kamera sudah terhubung (USB webcam atau Pi Camera)

### 1. Update sistem & install dependencies sistem
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv libatlas-base-dev \
    libhdf5-dev libjpeg-dev libopenjp2-7 libtiff5 \
    libavcodec-dev libavformat-dev libswscale-dev \
    alsa-utils  # untuk alarm audio
```

### 2. Buat virtual environment
```bash
python3 -m venv ~/drowsy_env
source ~/drowsy_env/bin/activate
```

### 3. Install Python packages
```bash
pip install --upgrade pip
pip install opencv-python-headless mediapipe numpy
pip install matplotlib pandas
```

> ⚠️ **Catatan RPi:** Gunakan `opencv-python-headless` bukan `opencv-python`
> untuk performa lebih baik di Raspberry Pi.

### 4. Cek kamera
```bash
ls /dev/video*   # pastikan ada /dev/video0
```

### 5. Generate alarm & jalankan
```bash
cd ~/drowsiness_detection
python src/generate_alarm.py
python src/detector.py
```

### Tips Performa Raspberry Pi 4
- Turunkan resolusi ke `320x240` di `Config` untuk FPS lebih tinggi
- Matikan `record_video=False` untuk hemat CPU
- Gunakan `show_landmarks=False`

---

## 🎮 Kontrol Keyboard

| Tombol | Fungsi |
|--------|--------|
| `q`    | Keluar dari program |
| `r`    | Reset semua counter |
| `s`    | Simpan screenshot |
| `l`    | Toggle tampilan landmark wajah |
| `a`    | Toggle adaptive threshold |

---

## 📊 Parameter yang Bisa Diubah

Edit bagian `Config` di `src/detector.py`:

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| `ear_threshold_base` | `0.25` | Threshold EAR mata tertutup |
| `ear_consec_frames` | `20` | Frame berturut untuk alarm kantuk |
| `mar_threshold` | `0.65` | Threshold MAR menguap |
| `perclos_threshold` | `0.35` | 35% waktu mata tertutup |
| `calibration_frames` | `100` | Frame untuk kalibrasi baseline |
| `adaptive_enabled` | `True` | Adaptive threshold otomatis |
| `camera_index` | `0` | Index kamera (0=default) |
| `frame_width/height` | `640x480` | Resolusi frame |

---

## 📈 Data Penelitian

Program otomatis menyimpan CSV di folder `logs/`:
- `metrics_YYYYMMDD_HHMMSS.csv` — data EAR, MAR, PERCLOS per frame
- `events_YYYYMMDD_HHMMSS.csv` — event kantuk & menguap
- `session.log` — log lengkap sesi

Data ini bisa dianalisis menggunakan pandas/matplotlib untuk keperluan TA.

---

## 📚 Referensi Metode

1. **EAR**: Soukupova & Cech (2016). *Real-Time Eye Blink Detection using Facial Landmarks*
2. **MAR**: Derivasi dari EAR untuk deteksi menguap
3. **PERCLOS**: Wierwille et al. (1994). *Research on vehicle-based driver status/performance monitoring*
4. **MediaPipe Face Mesh**: Kartynnik et al. (2019). *Real-time Facial Surface Geometry from Monocular Video*

---

## 🔬 Novelty untuk Publikasi SINTA 2

1. **Adaptive Threshold** — threshold tidak hardcoded, dikalibrasi dari baseline pengemudi nyata
2. **Kombinasi EAR + MAR + PERCLOS** — multi-indikator lebih akurat dari single-metric
3. **Evaluasi kondisi pencahayaan Indonesia** — uji di siang/malam hari
4. **Komparasi platform** — hasil di PC vs Raspberry Pi (embedded system)
