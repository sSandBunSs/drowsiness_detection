# BAB I PENDAHULUAN

**Judul (disepakati)**: *Implementasi Sistem Deteksi Kantuk Pengemudi Secara Real-Time Berbasis Eye Aspect Ratio, Mouth Aspect Ratio, dan PERCLOS dengan Adaptive Threshold Menggunakan MediaPipe Face Mesh*

> **Catatan struktur**: BAB I–VI mengikuti skema resmi *Pedoman Penyusunan Tugas Akhir FTII UNISBANK* (Januari 2022 v1.1) untuk kategori **Penelitian Pengembangan Sistem** (§4.3 pedoman) — bukan skema 5-bab "Penelitian Eksperimental/Pemodelan" yang dipakai draf sebelumnya. Program studi: **Teknik Informatika** (sampul biru muda, kertas buffalo).

## 1.1 Latar Belakang Penelitian

> ✅ **Statistik global dan Indonesia sudah diverifikasi ke sumber primer/independen (dibaca penuh, bukan hanya ringkasan pencarian).** Dua klaim dari data mentah awal dikoreksi setelah cross-check: persentase "human factor" Korlantas Polri (bukan mayoritas kantuk semata, seperti dijelaskan di bawah), dan atribusi kutipan jam kerja pengemudi *shuttle* (penulis yang benar adalah Zainy dkk. 2023, bukan Zuraida/Sutalaksana).

Kantuk saat berkendara (*drowsy driving*) merupakan salah satu penyebab kecelakaan lalu lintas yang sulit dideteksi oleh pengemudi itu sendiri, karena gejalanya (*microsleep*) dapat terjadi hanya dalam hitungan detik tanpa disadari — berbeda dengan distraksi lain seperti penggunaan ponsel yang lebih mudah dikenali. Secara global, National Highway Traffic Safety Administration (NHTSA) memperkirakan sekitar 100.000 kecelakaan lalu lintas per tahun disebabkan oleh kantuk pengemudi, mengakibatkan lebih dari 1.500 kematian dan 70.000 cedera (Saleem, 2022). Tinjauan sistematis yang sama, mencakup 17 studi observasional di berbagai negara (76.641 partisipan), juga melaporkan bahwa kantuk saat berkendara berkontribusi pada 3% hingga lebih dari 30% dari seluruh kecelakaan lalu lintas secara global, dengan frekuensi kantuk saat mengemudi bervariasi 1,1%–58% tergantung populasi studi.

Data resmi menunjukkan gap ini bukan sekadar isu global. KNKT (Komite Nasional Keselamatan Transportasi) mencatat kelelahan pengemudi sebagai kontribusi tertinggi penyebab kecelakaan kendaraan darat, mencapai 60% dari kasus (KNKT, dikutip dalam *news.detik.com*, 2025). Lebih spesifik pada jalan tol — konteks paling relevan untuk perjalanan jarak jauh — Ketua KNKT Soerjanto Tjahjono melaporkan 80% kecelakaan di jalan tol disebabkan pengemudi lelah dan mengantuk, dengan jam rawan pukul 00.00–06.00 dan 10.00–13.00 WIB, rentang waktu yang berpotensi memicu *microsleep* (KNKT, Forum Tematik Bakohumas "Keselamatan Jalan Tol", 30 November 2021). Secara nasional, Kementerian Perhubungan mencatat 103.645 kasus kecelakaan lalu lintas dengan 25.266 korban jiwa pada 2021 (Kemenhub, via Databoks Katadata), sementara data Korlantas Polri menunjukkan 61% kecelakaan disebabkan faktor manusia — mencakup kelalaian, kurang terampil, kantuk, dan perilaku berkendara berisiko lainnya secara bersamaan, bukan kantuk semata — dibanding 30% faktor infrastruktur dan 9% faktor kendaraan (Menhub Budi Karya Sumadi, FGD Keselamatan Transportasi Jalan, 2017). Pada tingkat regional, studi di ruas Tol Batang-Semarang menemukan 124 dari total kasus kecelakaan (61,08%) disebabkan kantuk pengemudi (Radik Mulia & Widowati, 2021, Indonesian Journal of Public Health and Nutrition, data 2019), dan studi deskriptif di Kota Pontianak (n=94) melaporkan kantuk berkontribusi pada 26,6% kecelakaan lalu lintas kota (Arfan & Wulandari, 2018) — mengindikasikan kantuk bukan isu eksklusif jalan tol/antarkota, meski studi terakhir ini berskala kecil dan lokal.

Faktor yang memperparah risiko ini pada pengemudi komersial Indonesia adalah pola kerja: pengemudi *shuttle*/travel umum dilaporkan bekerja hingga empat *trip* per hari yang terakumulasi menjadi 16 jam mengemudi, dengan istirahat hanya 30–60 menit antar-*trip* (Zainy, Pratama, Kurnianto, & Iridiastadi, 2023). Iridiastadi dkk. (2020) juga menunjukkan bahwa tugas mengemudi berdurasi panjang (diuji hingga 10 jam berkelanjutan) secara konsisten memicu kelelahan terukur pada indikator okular (durasi kedipan, PERCLOS), dan mencatat KNKT turut mengidentifikasi kelelahan dan kecerobohan sebagai faktor utama kecelakaan di Indonesia — kondisi yang berisiko memburuk saat musim mudik/liburan ketika durasi mengemudi meningkat melampaui kondisi kerja normal.

Dengan skala kasus nasional maupun regional ini, kesenjangan metodologis pada penelitian deteksi kantuk (BAB II) — threshold tetap yang tidak mempertimbangkan variasi individu dan kondisi pencahayaan lokal — menjadi relevan langsung dengan konteks keselamatan transportasi di Indonesia, bukan sekadar isu teoretis dari literatur luar negeri.

Berbagai pendekatan telah dikembangkan untuk mendeteksi kantuk pengemudi secara otomatis: sensor fisiologis (EEG, detak jantung) yang invasif dan mahal, hingga pendekatan berbasis *computer vision* yang non-invasif menggunakan kamera. Pendekatan berbasis wajah — memanfaatkan Eye Aspect Ratio (EAR), Mouth Aspect Ratio (MAR), dan Percentage of Eyelid Closure (PERCLOS) — populer karena hanya membutuhkan webcam standar tanpa perangkat tambahan.

Sebagian besar penelitian terdahulu (lihat BAB II) menggunakan threshold EAR/MAR yang bersifat tetap (*fixed threshold*), padahal bentuk mata dan pola kedipan berbeda antar individu (etnis, usia, bentuk wajah) serta antar kondisi pencahayaan (siang/malam). Gap ini bukan sekadar dugaan teoretis: Amalia dan Utaminingrum (2021) melaporkan akurasi deteksi kantuk berbasis facial landmark turun dari 98,88% pada pencahayaan normal (50–400 lux) menjadi 96,66% pada pencahayaan rendah (0–49 lux) — dan akurasi deteksi wajahnya sendiri turun lebih tajam, dari 100% ke 93,33% — menggunakan metode dengan threshold tetap. Pada sisi lain, Moredo dkk. (2025) menunjukkan bahwa model yang mencapai 95,23% akurasi pada data latih (dataset NTHU-DDD) hanya mencapai 51,85–85,71% ketika diuji langsung pada kendaraan nyata — menegaskan bahwa akurasi tinggi pada dataset laboratorium tidak serta-merta menggeneralisasi ke kondisi penggunaan sebenarnya.

Threshold tetap yang dikalibrasi untuk satu populasi/kondisi berisiko menghasilkan akurasi rendah pada pengemudi atau kondisi pencahayaan yang berbeda — gap yang coba dijembatani penelitian ini melalui *adaptive threshold* yang dikalibrasi otomatis dari baseline EAR pengemudi itu sendiri di awal sesi (100 frame pertama), serta dievaluasi secara eksplisit pada berbagai kondisi pencahayaan alih-alih hanya pada satu dataset statis. Penelitian ini mengimplementasikan sistem deteksi kantuk real-time yang menggabungkan tiga indikator (EAR, MAR, PERCLOS) dengan adaptive threshold, menggunakan MediaPipe Face Mesh (468 titik landmark wajah), serta diuji pada platform PC dan Raspberry Pi 4 untuk menilai kelayakan penerapan pada perangkat *embedded* berbiaya rendah.

## 1.2 Rumusan Masalah

1. Bagaimana mengimplementasikan sistem deteksi kantuk pengemudi secara real-time berbasis EAR, MAR, dan PERCLOS menggunakan MediaPipe Face Mesh?
2. Bagaimana pengaruh *adaptive threshold* terhadap akurasi deteksi dibandingkan dengan threshold tetap (*fixed threshold*)?
3. Bagaimana performa sistem pada kondisi pencahayaan yang berbeda (siang dan malam)?

**Batasan masalah**: agar pembahasan tidak terlalu luas, penelitian ini dibatasi pada:

1. Sistem hanya mendeteksi satu wajah dalam satu frame (*single-face detection*).
2. Input utama berupa webcam USB/kamera real-time (sistem juga mendukung pemrosesan berkas video untuk keperluan pengujian, lihat `detector.py`).
3. Penelitian ini tidak mencakup deteksi distraksi berkendara selain kantuk (mis. penggunaan ponsel, distraksi visual).

## 1.3 Tujuan dan Manfaat Penelitian

### Tujuan

1. Membangun sistem deteksi kantuk pengemudi secara real-time menggunakan MediaPipe Face Mesh.
2. Mengimplementasikan *adaptive threshold* pada perhitungan EAR untuk menyesuaikan karakteristik wajah tiap pengemudi.
3. Mengevaluasi akurasi sistem pada berbagai skenario pengujian (kondisi pencahayaan, platform PC vs Raspberry Pi 4).

### Manfaat

> Draf — sesuaikan dengan dosen pembimbing.

1. **Teoritis**: kombinasi metode (EAR + MAR + PERCLOS + adaptive threshold) sebagai rujukan penelitian deteksi kantuk berikutnya, khususnya untuk karakteristik wajah dan kondisi pencahayaan Asia Tenggara/Indonesia.
2. **Praktis**: prototipe sistem berbiaya rendah (webcam + Raspberry Pi 4) yang berpotensi diterapkan pada kendaraan nyata untuk menurunkan risiko kecelakaan akibat kantuk.

## 1.4 Hipotesis

Tidak diperlukan. Mengacu pedoman FTII (§4.1.2 Bagian Utama): penelitian yang bersifat eksplorasi/rancang bangun/rekayasa tidak memerlukan hipotesis, sedangkan penelitian yang bertujuan membuktikan kebenaran sebuah pernyataan memerlukan hipotesis. Penelitian ini adalah rancang bangun sistem (*penelitian pengembangan sistem*), bukan pengujian hipotesis statistik.

## 1.5 Metode Penelitian

Penelitian ini bersifat **penelitian terapan (applied research)** dengan pendekatan *rancang bangun sistem* — mengimplementasikan dan mengombinasikan metode yang sudah mapan (EAR, MAR, PERCLOS) dengan adaptasi (*adaptive threshold*), dievaluasi secara eksperimental-kuantitatif (accuracy, precision, recall, F1-score). Kombinasi EAR+MAR+PERCLOS mengikuti pendekatan Zhu dkk. (2022, `BAB2.md` jurnal 3) dan Albadawi dkk. (2023, jurnal 1), yang menunjukkan multi-indikator lebih andal dibanding EAR tunggal.

a. **Objek penelitian**: sistem deteksi kantuk pengemudi berbasis video wajah real-time (`DrowsinessDetector` pada `detector.py`), diuji terhadap dataset gambar berlabel publik dan (rencana) rekaman video pengemudi.

b. **Metode pengumpulan data**: dataset gambar wajah berlabel `active`/`fatigue` (~11.787 gambar, publik/Kaggle) sebagai data uji awal, karena dataset video referensi (UTA-RLDD) tidak dapat diunduh secara non-interaktif (lihat `BAB5.md` §5.1). Rencana lanjutan: rekaman video pengemudi langsung (webcam) dengan anotasi ground truth manual per interval waktu, mencakup kondisi pencahayaan siang dan malam.

c. **Metode analisis/pengembangan sistem**: tahapan meliputi (1) studi literatur (`BAB2.md`), (2) perancangan arsitektur sistem (`BAB3.md`), (3) implementasi (`BAB4.md`), (4) pengujian dan evaluasi menggunakan confusion matrix — akurasi, precision, recall, F1-score (`BAB5.md`), dan (5) penarikan kesimpulan (`BAB6.md`).

## 1.6 Keaslian Penelitian

Tinjauan terhadap 15 penelitian terdahulu (`BAB2.md` §2.1) menemukan tiga preseden langsung untuk pendekatan *adaptive/personalized threshold*: Ersoy dkk. (2026, preprint arXiv:2604.22479, belum peer-review) dengan formula kalibrasi yang identik (75% dari baseline EAR); Alvarez Oviedo dkk. (2025) yang menggunakan LSTM untuk re-kalibrasi threshold tiap 5 detik pada Raspberry Pi 4; dan IEEE 10467614 yang mengadaptasi EAR terhadap sudut wajah (bukan personalisasi baseline per-individu, sehingga tidak bersaing langsung dengan klaim penelitian ini). Tidak satu pun dari preseden ini diuji eksplisit pada kondisi pencahayaan rendah dengan breakdown angka, tidak satu pun diuji sekaligus pada platform embedded dan pencahayaan siang/malam, dan tidak satu pun melaporkan precision/recall/F1 per kelas selain akurasi agregat. Kombinasi pengujian cahaya siang/malam, platform embedded (Raspberry Pi 4), dan confusion matrix lengkap terhadap *adaptive threshold* per-pengemudi inilah yang membedakan penelitian ini dari penelitian sejenis (rincian perbandingan di `BAB2.md` §2.2.5 dan §2.3).

## 1.7 Sistematika Penulisan

Penelitian ini disusun dalam enam bab. Bab pertama menguraikan latar belakang masalah kantuk saat berkendara, rumusan dan batasan masalah, tujuan serta manfaat penelitian, metode penelitian yang digunakan, dan posisi keaslian penelitian ini di antara penelitian sejenis. Bab kedua membahas tinjauan pustaka, mencakup kajian atas lima belas penelitian terdahulu beserta landasan teori EAR, MAR, PERCLOS, MediaPipe Face Mesh, dan adaptive threshold, ditutup dengan uraian perbedaan penelitian ini terhadap penelitian-penelitian sebelumnya. Bab ketiga memaparkan analisis dan rancangan sistem, meliputi analisis kebutuhan, rancangan arsitektur `DrowsinessDetector`, dan rancangan pengujian yang akan dilakukan. Bab keempat menjelaskan implementasi sistem, mencakup perangkat keras dan perangkat lunak yang digunakan serta penerapan rancangan menjadi kode program. Bab kelima menyajikan hasil penelitian dan pembahasan, berupa hasil pengujian akurasi pada dataset gambar, eksperimen perbandingan threshold adaptif terhadap threshold tetap, serta pembahasan yang menghubungkan temuan dengan penelitian terdahulu di bab kedua. Bab keenam berisi kesimpulan yang menjawab rumusan masalah serta saran bagi pengembangan penelitian selanjutnya.

---
**Sumber**: disusun dari outline yang disepakati pada sesi brainstorming (`first_brainstorm.pdf`), status implementasi aktual proyek, dan *Pedoman Penyusunan Tugas Akhir FTII UNISBANK* (2022 v1.1). Bagian bertanda `[Placeholder]`/`⚠️` memerlukan data atau konfirmasi lebih lanjut sebelum final.
