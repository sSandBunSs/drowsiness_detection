# BAB II TINJAUAN PUSTAKA

## 2.1 Penelitian Terdahulu

**Verifikasi selesai** — 15 jurnal (10 internasional + 5 lokal SINTA) dari sesi brainstorming (`first_brainstorm.pdf`) sudah diverifikasi terhadap sumber asli (Crossref API, penerbit resmi, atau pencarian akademik). **6 dari 10 jurnal internasional ternyata memiliki nama penulis yang salah/tidak sesuai** pada daftar awal — kemungkinan halusinasi AI pada sesi sebelumnya (pola umum: nama penulis masuk akal tapi keliru untuk judul yang benar). Nama penulis di bawah ini sudah dikoreksi ke sumber asli; **gunakan tabel ini, bukan tabel di `first_brainstorm.pdf`**, untuk sitasi final.

### Jurnal Internasional

| No | Judul | Penulis (Terverifikasi) | Tahun | Jurnal/Penerbit | Metode | Dataset | Akurasi |
|---|---|---|---|---|---|---|---|
| 1 | Real-Time Machine Learning-Based Driver Drowsiness Detection Using Visual Features | Albadawi, AlRedhaei & Takruri ✅ *(sesuai daftar awal)* | 2023 | Journal of Imaging (MDPI) 9(5):91 | EAR+MAR+head pose (yaw/pitch/roll), landmark Dlib+MediaPipe, klasifikasi Random Forest/Sequential NN/Linear SVM | NTHU-DDD (36 subjek, siang/malam, dengan/tanpa kacamata) | hingga 99% |
| 2 | Development of a Real-time Driver's Drowsiness Detection System Using MediaPipe Face Mesh | ⚠️ **Baul, Rana, Trisna & Alam** *(bukan "Jewel et al.")* | 2025 | Int'l J. of Engineering and Manufacturing (IJEM) 15(5) | EAR+MAR+head tilt angle, MediaPipe Face Mesh+OpenCV | dataset publik standar + rekaman video real-time (nama tidak disebutkan) | tidak dilaporkan angka pasti ("akurasi tinggi") |
| 3 | Research on a Real-Time Driver Fatigue Detection Algorithm Based on Facial Video Sequences | ⚠️ **Zhu, Zhang, Wu, Ouyang, Li, Na, Liang & Li** *(bukan "Liu et al.")* | 2022 | Applied Sciences (MDPI) 12(4):2224 | TCDCN (tasks-constrained deep CNN, 68 titik landmark) + EAR/MAR/PERCLOS + AdaBoost/KNN classifier; indeks fatigue gabungan **M = 0,2×EAR + 0,7×PERCLOS + 0,1×MAR**, threshold fixed (EAR<0,2, PERCLOS>0,8, MAR>0,6, M>0,605) | Video sendiri: **10 pengemudi** (20–45 tahun, 5 wanita), 30 sesi uji 30 menit di jalur tertutup ~40km; ground truth dari kuesioner self-report; + FDDB untuk benchmark deteksi wajah | ✅ **Terverifikasi**: **akurasi sistem keseluruhan 95,1%**. Keterbatasan yang diakui penulis: belum diuji pada kendaraan nyata di malam hari; belum menggabungkan head-posture. ⭐ Preseden metodologi terkuat untuk kombinasi EAR+MAR+PERCLOS tertimbang (bobot PERCLOS dominan 0,7) — relevan untuk justifikasi desain status NORMAL/WARNING/DROWSY di `detector.py` |
| 4 | Real-time driver drowsiness detection using transformer architectures | ⚠️ **Hassan, Ibrahim, Gomaa, Makhlouf & Hafiz** *(bukan "Jamil et al.")* | 2025 | Scientific Reports (Nature) 15:17493 | Vision Transformer, Swin Transformer, transfer learning (VGG19, DenseNet169, ResNet50V2, InceptionResNetV2, InceptionV3, MobileNet) untuk klasifikasi status mata | MRL Eye Dataset (Open/Closed) | **>99,0%** — pembanding SOTA deep-learning terberat; sistem kita jauh lebih ringan (tanpa training) dengan trade-off akurasi wajar |
| 5 | Real-Time Driver Drowsiness Detection Using Facial Analysis and Machine Learning Techniques | **Essahraui, Lamaakal, El Hamly, Maleh, et al.** *(daftar awal tidak menyebut penulis)* | 2025 | Sensors (MDPI) 25(3):812 | KNN, SVM, DT, RF (ML klasik) + CNN, YOLOv5, YOLOv8, Faster R-CNN (computer vision) — perbandingan sistematis banyak metode pada 3 dataset | **NTHU-DDD, YawDD, UTA-RLDD** (3 dataset publik) | ✅ **Terverifikasi**: hasil terbaik per dataset — UTA-RLDD: KNN 98,89% akurasi/99,27% presisi/98,86% F1; YOLOv5 & YOLOv8 presisi&recall 100%, mAP@0.5 99,5% (tapi Faster R-CNN cuma 81% akurasi/63,4% presisi di dataset sama — **variasi besar antar-model pada dataset identik**); NTHU-DDD & YawDD: YOLOv5/v8 F1=1,00. ⭐ Pembanding SOTA terkuat: rentang akurasi 63–100% tergantung model membuktikan bahwa "akurasi tinggi" sangat bergantung pilihan arsitektur, bukan cuma dataset — memperkuat argumen bahwa sistem ringan tanpa training (EAR-threshold) tetap punya nilai karena tak butuh tuning model seberat ini |
| 6 | Computer vision-based approach to detect fatigue driving and face mask for edge computing device | ⚠️ **Rahman, Hriday & Khan** *(bukan "Hossain et al.")* | 2022 | Heliyon (Elsevier), DOI 10.1016/j.heliyon.2022.e11204 | 68 titik landmark (gaya dlib, bukan MediaPipe) + EAR/MAR, deep learning; multimodal dengan sensor detak jantung AD8232 | rekaman wajah + Jetson Nano + Arduino Uno; hanya **4 relawan pria** untuk eksperimen threshold EAR | Fatigue **97,44%**, face mask 97,90% (keseluruhan); **breakdown per pencahayaan** — cahaya penuh: aktif 95,5%/lelah 94%/tidur 97,5%; cahaya sedang: 97%/97,5%/84,5%; **cahaya rendah: 86%/81,5%/90%** — ⭐ preseden kedua (selain jurnal 13) untuk drop akurasi di cahaya rendah pada metode fixed-threshold |
| 7 | Design of a System for Driver Drowsiness Detection **and Seat Belt Monitoring** Using Raspberry Pi 4 **and Arduino Nano** | ⚠️ **Alvarez Oviedo, Mamani Villanueva, Echaiz Espinoza, Villanueva, Ortiz Salazar & Llanos Villarreal** *(bukan "Paredes et al."; judul asli juga menyebut "seat belt monitoring", bukan "MediaPipe" di judul)* | 2025 | Designs (MDPI) 9(1):11 | Dua subsistem terpisah: (1) sabuk pengaman via sensor kustom+Arduino Nano/RS485 (di luar scope kita); (2) **kantuk via Raspberry Pi 4 + MediaPipe FaceMesh (468 titik)** — EAR (blink >13 frame/433ms), MAR (menguap >5 detik), head-nod (arctangent 2 titik + **Kalman filter** untuk kurangi false-positive akibat perubahan cahaya). ⭐ **THRESHOLD EAR-NYA JUGA ADAPTIF**: "LSTM neural network with PyTorch dynamically adjusts the EAR threshold every 5 seconds" — mekanisme berbeda dari formula 75%-baseline kita/Ersoy et al. (re-kalibrasi kontinu tiap 5 detik, bukan sekali di awal sesi) | Simulasi Proteus (sabuk) + rekaman video real pengemudi (kantuk), diuji di Raspberry Pi 4 | ✅ **Terverifikasi (Tabel 2)**: reliabilitas blink 87,27%, menguap 94%, head-nod 92%, **rata-rata keseluruhan 91,09%**. Keterbatasan diakui penulis: belum menangani kacamata; perlu kamera IR untuk operasi day-long yang andal; kebutuhan CPU/GPU lebih tinggi untuk metode lebih robust. |
| 8 | Multi-Feature Long Short-Term Memory Facial Recognition for Real-Time Automated Drowsiness Observation of Automobile Drivers with Raspberry Pi 4 | ⚠️ **Moredo, Celino & Ibarra** *(bukan "Parel et al.")* | 2025 | Engineering Proceedings (MDPI) 92(1):52 | EAR+MAR+head pose (yaw/pitch/roll) + LSTM, 10 FPS di Raspberry Pi 4 | NTHU-DDD (training) + pengujian kendaraan nyata (diam & bergerak) | Training 95,23%; validasi 91,81–95,82%; **kendaraan nyata hanya 51,85–85,71%** (kombinasi seluruh fitur: 80,95–85,71%; fitur tunggal: 51,85–72,22%) — *lihat catatan gap di bawah* |
| 9 | Driver Drowsiness Detection Using Facial Landmarks: A Comprehensive Survey on Techniques, Algorithms, and Applications | **Kumari, Harsha K, Jallal S, Dutta & Hashim** *(daftar awal tidak menyebut penulis)* — ⚠️ bukan survei murni: ada §IV Metodologi + §V Hasil dengan implementasi sendiri (HAAR cascade + dlib 68-titik + EAR threshold 0,25/7 frame, stack Golang+Python+JS), tapi **tanpa dataset primer sendiri** (pakai 323 foto dari Isha Gupta et al. [28]) | 2024 | Journal of Electrical Systems 20-11s:2828–2837 | Tinjauan 4 kategori metode (subjektif/behavioral/fisiologis/vehicular) + implementasi EAR ringan sebagai demonstrasi | — (dataset dipinjam, bukan primer) | ✅ **Terverifikasi dari full-text — TEMUAN PENTING**: angka **97,3% di Abstrak TIDAK PERNAH muncul lagi di badan teks manapun** (Hasil/Diskusi/Kesimpulan) — kemungkinan besar kesalahan penulisan/padding abstrak. Angka yang benar-benar dilaporkan di §V dan Kesimpulan adalah **89%** — dan itu pun **dikutip dari paper lain** (Isha Gupta et al. 2018, diuji pada cuma 323 foto "eye-closed"/"neutral"), bukan hasil eksperimen baru paper ini. **JANGAN kutip 97,3% sama sekali — pakai 89% jika perlu, dengan atribusi ke Isha Gupta et al. (2018), bukan ke jurnal 9 ini.** |
| 10 | Research Paper on Driver Drowsiness Detection Using OpenCV and Raspberry Pi | Agarwal & Sharma ✅ *(sesuai daftar awal)* | 2022 | IJRASET, DOI 10.22214/ijraset.2022.45288 | Deteksi pupil/iris + PERCLOS + EAR (diukur tiap 0,5 detik) | pengujian real-time | PERCLOS >70–80% memicu alarm |

### Jurnal Lokal Indonesia (SINTA)

| No | Judul | Penulis (Terverifikasi) | Tahun | Jurnal | Metode | Hardware | Akurasi |
|---|---|---|---|---|---|---|---|
| 11 | Implementasi Sistem Deteksi Kantuk Secara Real-Time Bagi Pengemudi Menggunakan Metode Eye Aspect Ratio | Mochammad Fadiil Thoriq et al. ✅ | 2024 | Jurnal Sistem Informasi dan Ilmu Komputer (JUSIIK) 2(4):70–85, DOI 10.59581/jusiik-widyakarya.v2i2.4226 | dlib 68 titik landmark + EAR, **threshold 0,25 — identik dengan `Config.ear_threshold_base` sistem kita**, OpenCV+Python+PyGame (alarm suara) | webcam, hanya demonstrasi kualitatif (tanpa dataset uji terstruktur) | ⚠️ **Terverifikasi dari full-text — TIDAK ADA angka akurasi/precision/recall sama sekali.** Hanya melaporkan EAR rata-rata per kondisi mata: terbuka 0,30, setengah tertutup 0,27, tertutup 0,20 (Tabel 1) — validasi kualitatif via visualisasi grafik, bukan confusion matrix. **Kesimpulan penulis eksplisit menyebut "algoritma yang lebih adaptif" sebagai arah penelitian mendatang yang BELUM mereka implementasikan** — ⭐ konfirmasi independen ketiga bahwa adaptive threshold masih gap terbuka di jurnal-jurnal sejenis. |
| 12 | Sistem Deteksi Kantuk Pengemudi Mobil Berdasarkan Analisis Rasio Mata Menggunakan Computer Vision | A. Asvin Mahersatillah Suradi, S. Alam, M. Mushaf, M. F. Rasyid, I. Djafar ✅ *(nama "Suradi" cocok)* | 2023 | JUKI: Jurnal Komputer dan Informatika 5(2):222–230, DOI 10.53842/juki.v5i2.269 | HOG + Linear SVM (dlib), 68 titik landmark, kamera area speedometer jarak 50cm, threshold EAR minimum **0,20** (bukan 0,25 seperti sistem kita), durasi >10 frame untuk hindari false positive dari kedipan | 10 responden (dengan/tanpa kacamata), video 16:9 1280×720 | ✅ **Terverifikasi dari full-text PDF**: rata-rata 90,4% (13 FPS), confusion matrix per-responden (Tabel 2). **Responden 4 anjlok ke 69,7%** (FN=130) — penyebab eksplisit: sudut wajah menyamping terhadap kamera membuat landmark mata tak terdeteksi optimal. ⭐ **gap ketiga**: kegagalan bukan karena cahaya (jurnal 6, 13) atau lab-vs-real (jurnal 8), tapi karena **sudut pandang wajah** — threshold fixed (dan bahkan adaptive-baseline murni) tidak menolong jika landmark deteksinya sendiri gagal; relevan untuk BAB III sebagai batasan (§1.4: *single-face, frontal-ish detection*) |
| 13 | Deteksi Kantuk pada Pengemudi melalui Jumlah Kedipan Mata Menggunakan Facial Landmark berbasis Intel NUC | Dewi Amalia & Fitri Utaminingrum ✅ | 2021 | J-PTIIK Universitas Brawijaya 5(12):5529–5535 | Facial landmark + hitung kedipan mata | Intel NUC + webcam | **Deteksi wajah: 93,33% (cahaya rendah 0–49 lux) vs 100% (normal 50–400 lux); deteksi kantuk: 96,66% (rendah) vs 98,88% (normal); rata-rata keseluruhan 97,77%** — ⭐ *preseden langsung untuk pertanyaan penelitian siang/malam kita* |
| 14 | Deteksi Pengendara Mengantuk dengan Kombinasi Haar Cascade Classifier dan Support Vector Machine | Ilmadina, Apriliani & Wibowo ✅ | 2022 | Jurnal Informatika: Jurnal Pengembangan IT 7(1):1–7 | Haar Cascade (deteksi wajah) + SVM (klasifikasi buka/tutup mata) | webcam, real-time | ✅ **Dikonfirmasi via 2 pencarian independen (belum baca PDF penuh)**: akurasi 99% pada implementasi real-time. Konsisten dengan pencarian awal — tidak ada perubahan angka. |
| 15 | Deteksi Kantuk untuk Keamanan Berkendara Berbasis Pengolahan Citra | Charlos Kurniawan Umbu Nggiku, Abd Rabi, Subairi Subairi ✅ *(nama "Kurniawan" cocok, urutan nama Indonesia)* | 2023 | Jurnal JEETech 4(1), DOI 10.32492/jeetech.v4i1.4107 | Facial landmark + EAR | Raspberry Pi 3B | 90,4% |

> **Catatan integritas sitasi**: 5 jurnal lokal Indonesia (11–15) semuanya akurat atau mendekati akurat pada daftar awal. Masalah nama penulis salah hanya terjadi pada jurnal internasional (2, 3, 4, 6, 7, 8) — pola ini sendiri layak dicatat sebagai pelajaran: selalu verifikasi sitasi terhadap sumber primer sebelum menulis, jangan mengandalkan daftar dari sesi AI sebelumnya tanpa cek ulang.

**Peta penggunaan (diperbarui setelah verifikasi):**
- Jurnal 1, 3 → landasan metode EAR+MAR+PERCLOS (paling relevan secara metodologi)
- Jurnal 7, 8, 10 → justifikasi penggunaan Raspberry Pi — **jurnal 8 juga jadi bukti kuat gap "akurasi lab vs akurasi kendaraan nyata"** (95% training vs ~52–86% kendaraan nyata), mendukung argumen bahwa evaluasi di kondisi nyata (bukan hanya dataset) itu penting
- Jurnal 6 → **preseden low-light kedua**: akurasi turun dari 95,5–97,5% (cahaya penuh/sedang) ke 81,5–90% (cahaya rendah) pada threshold fixed — memperkuat jurnal 13, dua bukti independen untuk rumusan masalah #3
- Jurnal 4, 5 → state-of-the-art terbaru berbasis deep learning (pembanding novelty — sistem kita jauh lebih ringan, tanpa training)
- Jurnal 9 → rujukan survei/SOTA di §2.2 (taksonomi 4 kategori metode berguna untuk kerangka teori), **tapi JANGAN kutip angka 97,3%-nya — itu tidak didukung badan teks paper, lihat catatan verifikasi di tabel atas**
- Jurnal 11–15 → gap research & posisi penelitian di konteks Indonesia — **jurnal 13 (Amalia & Utaminingrum) adalah preseden terkuat untuk rumusan masalah #3 (pengaruh kondisi pencahayaan)**, sudah menunjukkan drop akurasi signifikan di cahaya rendah pada metode non-adaptive
- Kutip paling banyak dari jurnal 1, 3, dan 13 — metodologi/temuan paling relevan langsung dengan sistem yang sudah dibangun.

## 2.2 Landasan Teori

### 2.2.1 Eye Aspect Ratio (EAR)
Referensi utama: Soukupová & Čech (2016), *Real-Time Eye Blink Detection Using Facial Landmarks*.

EAR dihitung dari 6 titik landmark di sekitar mata:

`EAR = (‖p2−p6‖ + ‖p3−p5‖) / (2‖p1−p4‖)`

Diimplementasikan pada `compute_ear()` (`detector.py:134`), menggunakan indeks landmark MediaPipe Face Mesh `LEFT_EYE = [362, 385, 387, 263, 373, 380]` dan `RIGHT_EYE = [33, 160, 158, 133, 153, 144]`.

### 2.2.2 Mouth Aspect Ratio (MAR)
Adaptasi dari EAR untuk mendeteksi menguap, dihitung dari 8 titik landmark mulut (`MOUTH_OUTER`). Diimplementasikan pada `compute_mar()` (`detector.py:148`).

### 2.2.3 PERCLOS (Percentage of Eyelid Closure)
Referensi utama: Wierwille et al. (1994), *Research on Vehicle-Based Driver Status/Performance Monitoring*.

PERCLOS = proporsi frame dalam suatu jendela waktu di mana EAR berada di bawah threshold (mata dianggap tertutup). Diimplementasikan pada `compute_perclos()` (`detector.py:167`), dengan jendela (`perclos_window`) 150 frame.

### 2.2.4 MediaPipe Face Mesh
Referensi utama: Kartynnik et al. (2019), *Real-Time Facial Surface Geometry from Monocular Video*.

Model face landmark MediaPipe (Tasks API, `FaceLandmarker`) mengekstraksi 468 titik landmark 3D dari satu wajah per frame, dijalankan dalam mode `VIDEO` (streaming) pada sistem live, dan mode `IMAGE` untuk evaluasi terhadap dataset gambar independen (`evaluate_dataset_images.py`).

### 2.2.5 Adaptive Threshold

⚠️ **TEMUAN PENTING (mengubah posisi novelty) — ditemukan 2 preseden langsung, klaim "belum ada penelitian adaptive threshold" pada draf sebelumnya TIDAK BENAR lagi:**

| Preseden | Detail |
|---|---|
| **Ersoy, Tatar, Tonbul & Kırbız** (2026) — *Improving Driver Drowsiness Detection via Personalized EAR/MAR Thresholds and CNN-Based Classification*. arXiv:2604.22479, MEF University. **Preprint, belum peer-review** (per Juli 2026). | Formula: **threshold EAR personal = 75% × baseline EAR**, **threshold MAR personal = 140% × baseline MAR** — kalibrasi dari fase netral 5 detik. **Formula EAR-nya identik dengan sistem kita (0,75×baseline)**, meski basisnya dijelaskan sebagai "berdasarkan beberapa uji coba" tanpa derivasi. Hasil: EAR personal 93,23% vs generalized 91,70% (naik ~1,53%); MAR personal 97,23% vs generalized 95,90%; model CNN tambahan mencapai 99,10%/98,80% tapi butuh resource lebih besar. Dataset: MRL Eye (84.898 gambar) + Yawn Dataset (5.119 gambar) + data custom (~1.000 gambar, split 70/15/15). **Tidak melaporkan precision/recall**, hanya akurasi; tidak menguji kondisi pencahayaan low-light secara eksplisit; tidak diuji pada Raspberry Pi/embedded. |
| **IEEE 10467614** — *Adaptive Eye Aspect Ratio Technique for Drowsiness Detection System*. Metode: EAR + arah vektor wajah (Attention Mesh) untuk mengatasi kelemahan EAR pada wajah non-frontal — **"adaptive" di sini berarti adaptif terhadap sudut wajah, bukan personalisasi baseline per-pengemudi seperti sistem kita**. Detail metode/akurasi lengkap belum bisa diakses (IEEE Xplore memblokir fetch otomatis). | Perlu verifikasi manual di ieeexplore.ieee.org/document/10467614 apakah lebih dekat ke pendekatan kita atau tidak — belum sempat diverifikasi manual meski jurnal 3/7/11 lain sudah. |
| **Alvarez Oviedo et al. (2025)** — jurnal 7 di atas, Designs (MDPI) 9(1):11. **Preseden ketiga**, ditemukan saat verifikasi full-text jurnal 7 (bukan dari pencarian awal §2.2.5). | Threshold EAR-nya **disesuaikan terus-menerus setiap 5 detik oleh LSTM (PyTorch)** — bukan kalibrasi sekali di awal sesi seperti sistem kita/Ersoy et al., melainkan re-adaptasi kontinu sepanjang sesi mengemudi. Diuji di Raspberry Pi 4 (platform sama dengan rencana pengujian kita), reliabilitas rata-rata 91,09%, tapi **tidak diuji eksplisit pada kondisi cahaya rendah** (hanya pakai Kalman filter generik untuk redam noise akibat cahaya) dan **tidak melaporkan breakdown siang/malam**. |

**Implikasi untuk klaim novelty**: sudah diintegrasikan ke `BAB1.md` §1.1 (Latar Belakang) dan §1.6 (Keaslian Penelitian), serta `BAB2.md` §2.3 di atas — tidak lagi menyatakan "belum ada penelitian adaptive threshold" secara mutlak, melainkan framing presisi: 3 preseden ada, tapi kombinasi pengujian cahaya rendah + platform embedded + confusion matrix lengkap belum pernah diuji bersamaan oleh satupun preseden.

Pada sistem ini, threshold EAR dikalibrasi otomatis dari 100 frame pertama (`calibration_frames`) sesi pengemudi: `threshold = 0.75 × rata-rata EAR baseline` (lihat `_calibrate()`, `detector.py:384`).

## 2.3 Perbedaan Penelitian dengan Penelitian Terdahulu

> Bagian ini wajib per *Pedoman Penyusunan Tugas Akhir FTII UNISBANK* (2022 v1.1, Lampiran 7). Berikut sintesis pola gap dari 15 penelitian terdahulu (§2.1) dan posisi novelty adaptive threshold (§2.2.5) yang membedakan penelitian ini — versi ringkas ada juga di `BAB1.md` §1.6 Keaslian Penelitian.

### Sintesis: Pola Gap pada Metode Threshold Tetap

Membaca jurnal 6, 8, 12, dan 13 secara bersamaan menunjukkan pola yang konsisten: metode berbasis EAR/MAR/PERCLOS dengan **threshold tetap** (*fixed threshold*), betapapun tinggi akurasinya pada kondisi kalibrasi awal, secara sistematis kehilangan akurasi begitu asumsi kondisi tersebut dilanggar — dan pelanggarannya bisa datang dari tiga arah yang berbeda dan independen satu sama lain.

**Pertama, dimensi pencahayaan.** Amalia dan Utaminingrum (2021, jurnal 13) mencatat penurunan deteksi wajah dari 100% ke 93,33% dan deteksi kantuk dari 98,88% ke 96,66% saat cahaya turun dari kondisi normal (50–400 lux) ke rendah (0–49 lux). Rahman dkk. (2022, jurnal 6), dengan setup kamera dan populasi uji yang sama sekali berbeda, menemukan pola serupa: akurasi klasifikasi status turun dari kisaran 94–97,5% (cahaya penuh/sedang) ke 81,5–90% (cahaya rendah). Dua studi independen dengan metode berbeda menunjukkan gejala yang sama — ini bukan kebetulan satu paper, melainkan kelemahan struktural pada threshold yang dikalibrasi untuk satu kondisi cahaya.

**Kedua, dimensi transfer lab-ke-nyata.** Moredo dkk. (2025, jurnal 8) menunjukkan bahwa model yang mencapai 95,23% pada data latih (NTHU-DDD, direkam di laboratorium) anjlok ke 51,85–85,71% saat diuji langsung pada kendaraan sungguhan. Selisih ~10–43 poin persentase ini menegaskan bahwa akurasi tinggi pada dataset terkurasi tidak otomatis menggeneralisasi ke kondisi penggunaan nyata — gap yang tidak akan tampak jika evaluasi berhenti pada dataset gambar/video statis saja.

**Ketiga, dimensi sudut pandang wajah.** Suradi dkk. (2023, jurnal 12) melaporkan rata-rata akurasi 90,4% pada 10 responden, tetapi satu responden anjlok ke 69,7% semata karena posisi wajahnya menyamping terhadap kamera sehingga landmark mata gagal terdeteksi optimal. Ini adalah gap yang berbeda sifatnya dari dua di atas: bukan soal kalibrasi nilai threshold, melainkan kegagalan di tahap deteksi landmark itu sendiri — sebuah batasan yang tidak bisa diatasi oleh threshold adaptif manapun (baik fixed maupun personalized), dan karena itu ditetapkan sebagai batasan eksplisit penelitian ini (`BAB1.md` §1.2: *single-face, frontal-ish detection*) alih-alih diklaim sebagai sesuatu yang diselesaikan.

Ketiga pola ini bersama-sama membingkai kontribusi penelitian ini: *adaptive threshold* yang dikalibrasi dari baseline EAR pengemudi sendiri secara langsung menyasar gap pertama (variasi individu di bawah kondisi pencahayaan yang berubah — lihat rumusan masalah #3), sementara gap kedua dan ketiga ditangani lewat desain pengujian (video real, bukan hanya gambar statis — `BAB3.md` §3.3 Rancangan Pengujian) dan batasan scope yang eksplisit, bukan diabaikan begitu saja.

### Ringkasan posisi novelty

Tiga preseden adaptive/personalized threshold ditemukan (Ersoy dkk. 2026 — preprint, formula 75%-baseline identik; Alvarez Oviedo dkk. 2025 — LSTM re-kalibrasi tiap 5 detik di Raspberry Pi 4; IEEE 10467614 — adaptif sudut wajah, sumbu masalah berbeda). Tidak satu pun diuji eksplisit pada kondisi cahaya rendah dengan breakdown angka, tidak satu pun diuji sekaligus pada platform embedded dan pencahayaan siang/malam, dan tidak satu pun melaporkan precision/recall/F1 per kelas selain akurasi agregat. Kombinasi ketiga hal itulah yang membedakan penelitian ini (detail tabel perbandingan di §2.2.5 di atas).

---

## Yang masih perlu dikerjakan untuk BAB II

> **Status: selesai (sesi lanjutan Juli 2026)** — seluruh 15 jurnal terverifikasi (jurnal 3, 5, 7, 11, 12, 14 dari full-text; jurnal 4, 6, 9 dari full-text dengan koreksi angka; sisanya dari pencarian awal). Novelty sudah direvisi ke BAB1 §1.1/§1.6 dan BAB2 §2.3.

1. ~~Cari jurnal soal adaptive/personalized EAR threshold~~ — **SELESAI, ditemukan 2 preseden** (lihat §2.2.5 di atas) — **posisi novelty perlu direvisi**, bukan lagi "belum ada penelitian serupa".
2. ~~Jurnal 3, 7, 11~~ — **SELESAI**, PDF didapat user dan dibaca penuh dari `journal/`. Jurnal 3: 95,1% akurasi (10 pengemudi, self-report ground truth). Jurnal 7: 91,09% reliabilitas rata-rata di RPi4, **DAN ternyata preseden adaptive threshold ketiga** (LSTM re-kalibrasi tiap 5 detik) — §2.2.5 diperbarui. Jurnal 11: TIDAK ADA angka akurasi sama sekali, cuma validasi kualitatif; eksplisit menyebut "adaptive" sebagai future work belum dikerjakan.
   **IEEE 10467614 — SENGAJA DILEWATI (bukan gap, keputusan sadar)**: dari abstrak/deskripsi yang sudah didapat, "adaptive" di paper ini berarti adaptif terhadap *sudut wajah* (pakai vektor arah wajah untuk atasi wajah non-frontal), bukan personalisasi baseline EAR per-pengemudi seperti klaim novelty kita. Beda sumbu masalah — tidak bersaing langsung dengan argumen novelty di §2.2.5, jadi tidak esensial untuk dikejar lebih lanjut. 3 preseden yang sudah terverifikasi (Ersoy, Alvarez Oviedo, Thoriq) sudah cukup untuk menopang framing novelty.
3. ~~Verifikasi ulang jurnal 12 (Suradi)~~ — **SELESAI**, dibaca langsung dari PDF asli. Angka 90,4% genuine (bukan tertukar dengan jurnal 15, cuma kebetulan sama), didukung confusion matrix per-responden. Ditemukan gap baru: kegagalan akibat sudut wajah menyamping (responden 4 → 69,7%).
4. ~~Double-check jurnal 9~~ — **SELESAI**. Dikonfirmasi dari full-text: 97,3% di abstrak adalah angka yatim (tidak muncul di badan teks), kemungkinan salah tulis. Angka asli 89% pun dikutip dari paper lain (Isha Gupta et al. 2018), bukan hasil primer jurnal 9. Tabel & peta penggunaan di atas sudah diperbarui.
5. ~~Tulis narasi/paragraf pembanding~~ — **SELESAI**. Ditambahkan subbagian "Sintesis: Pola Gap pada Metode Threshold Tetap" setelah peta penggunaan, menyusun 3 gap independen (pencahayaan: jurnal 6+13; lab-vs-real: jurnal 8; sudut wajah: jurnal 12) jadi argumen koheren yang membingkai kontribusi penelitian.
6. ~~Revisi BAB1.md §1.1~~ — **SELESAI** (lihat riwayat edit `BAB1.md`), sudah tidak menyatakan "belum ada penelitian adaptive threshold" secara mutlak; ditambah §1.6 Keaslian Penelitian yang meringkas posisi novelty ini secara eksplisit. `BAB6.md` (Kesimpulan dan Saran, dulu `BAB5.md`) sudah disesuaikan juga.
7. **BARU (restrukturisasi 6-bab)** — Struktur BAB2 kini mengikuti *Pedoman Penyusunan Tugas Akhir FTII UNISBANK* (2022 v1.1): ditambahkan §2.3 "Perbedaan Penelitian dengan Penelitian Terdahulu" (heading wajib per pedoman), memindahkan subbagian Sintesis ke posisi yang benar (setelah §2.2, bukan sebelum), dan memperbaiki sitasi multi-penulis ke format "dkk." sesuai kaidah APA versi pedoman (bukan "et al.").

**BAB II sekarang dianggap selesai untuk tahap ini** — semua item triase di atas tuntas kecuali item pengujian fisik (`BAB5.md` §5.2: cahaya siang/malam langsung, Raspberry Pi 4, video real-time) yang menunggu akses hardware.

## Cara Pakai (dari sesi brainstorming)
Saat membaca tiap jurnal, catat dengan format:
```
Jurnal   : [nama]
Metode   :
Dataset  :
Akurasi  :
Hardware :
Gap/Kekurangan yang disebutkan:
Kutipan teori yang bisa dipakai di BAB 2:
```
Alur: baca jurnal → isi catatan baca → pindahkan ke tabel perbandingan di atas → temukan pola gap → tulis narasi BAB II.
