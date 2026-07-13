"""
Menu terpadu untuk mengisi seluruh data yang masih diperlukan di BAB V §5.2:
rekam sesi real-time, validasi akurasi, benchmark PC vs Raspberry Pi 4, dan
grafik tren metrik. Membungkus detector.py/validate_accuracy.py/benchmark.py
yang sudah ada — tidak menduplikasi logikanya — supaya semua langkah bisa
dijalankan berurutan dari satu tempat, dalam satu atau beberapa sesi.

Usage:
    python collect_missing_data.py
"""
import glob
import os

from benchmark import append_csv, benchmark_video
from benchmark import print_report as print_benchmark_report
from detector import Config, DrowsinessDetector
from validate_accuracy import confusion_matrix, load_ground_truth, load_metrics
from validate_accuracy import print_report as print_accuracy_report


def _pick_file(prompt, pattern):
    """Tampilkan berkas yang cocok dengan `pattern` sebagai pilihan cepat, atau terima path manual."""
    candidates = sorted(glob.glob(pattern))
    if candidates:
        print(f"Berkas ditemukan untuk '{pattern}':")
        for i, path in enumerate(candidates, 1):
            print(f"  {i}. {path}")
    raw = input(f"{prompt} (nomor di atas, atau path manual, kosongkan=batal): ").strip()
    if not raw:
        return None
    if raw.isdigit() and 1 <= int(raw) <= len(candidates):
        return candidates[int(raw) - 1]
    return raw


# ─── §5.2.1 / §5.2.2: Rekam sesi real-time ─────────────────────
def menu_record_session():
    print("\n--- Rekam Sesi Real-Time (§5.2.1 / §5.2.2) ---")
    source = input("Path video (kosongkan untuk webcam langsung): ").strip() or None
    lighting = input("Kondisi pencahayaan [siang/malam] (default: unspecified): ").strip() or "unspecified"

    cfg = Config(lighting_condition=lighting, log_metrics=True)
    detector = DrowsinessDetector(cfg)
    print("Jendela kamera terbuka. Tekan 'q' untuk berhenti — hasil tersimpan otomatis ke logs/metrics_*.csv.")
    detector.run(video_source=source)
    print("Sesi selesai. Buat ground_truth.csv (start_sec,end_sec,label) sambil menonton hasil rekaman, "
          "lalu pakai menu 2 untuk validasi.")


# ─── §5.2.1 / §5.2.2: Validasi akurasi ─────────────────────────
def menu_validate_accuracy():
    print("\n--- Validasi Akurasi terhadap Ground Truth (§5.2.1 / §5.2.2) ---")
    metrics_path = _pick_file("Metrics CSV", "logs/metrics_*.csv")
    if not metrics_path or not os.path.exists(metrics_path):
        print("Batal: berkas metrics tidak ditemukan.")
        return
    gt_path = _pick_file("Ground truth CSV", "ground_truth*.csv")
    if not gt_path or not os.path.exists(gt_path):
        print("Batal: berkas ground truth tidak ditemukan.")
        return

    matrix, skipped = confusion_matrix(load_metrics(metrics_path), load_ground_truth(gt_path))
    print_accuracy_report(matrix, skipped)


# ─── §5.2.3: Benchmark PC vs Raspberry Pi 4 ────────────────────
def menu_benchmark():
    print("\n--- Benchmark Performa PC vs Raspberry Pi 4 (§5.2.3) ---")
    video_path = input("Path video untuk benchmark (sama persis di PC & RPi4): ").strip()
    if not video_path or not os.path.exists(video_path):
        print("Batal: berkas video tidak ditemukan.")
        return
    frames_raw = input("Batas jumlah frame (kosongkan = semua): ").strip()
    max_frames = int(frames_raw) if frames_raw else None

    result = benchmark_video(video_path, max_frames=max_frames)
    print_benchmark_report(result)
    append_csv(result, "logs/benchmark_results.csv")
    print("Hasil ditambahkan ke logs/benchmark_results.csv "
          "— jalankan langkah ini juga di Raspberry Pi 4 dengan video yang sama.")


# ─── §5.2.4: Grafik tren metrik ────────────────────────────────
def plot_metrics(metrics_csv, ground_truth_csv, output_png):
    import matplotlib
    matplotlib.use("Agg")  # headless-safe (tidak perlu display, aman untuk RPi via SSH)
    import matplotlib.pyplot as plt
    import pandas as pd

    df = pd.read_csv(metrics_csv)
    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    axes[0].plot(df["elapsed_sec"], df["ear_avg"], color="tab:blue")
    axes[0].set_ylabel("EAR")
    axes[1].plot(df["elapsed_sec"], df["mar"], color="tab:orange")
    axes[1].set_ylabel("MAR")
    axes[2].plot(df["elapsed_sec"], df["perclos"], color="tab:green")
    axes[2].set_ylabel("PERCLOS")
    axes[2].set_xlabel("Waktu (detik)")

    if ground_truth_csv:
        for start, end, label in load_ground_truth(ground_truth_csv):
            if label == "DROWSY":
                for ax in axes:
                    ax.axvspan(start, end, color="red", alpha=0.15)

    fig.suptitle("Tren EAR/MAR/PERCLOS terhadap Waktu (area merah = DROWSY pada ground truth)")
    fig.tight_layout()
    fig.savefig(output_png, dpi=150)
    plt.close(fig)


def menu_plot_metrics():
    print("\n--- Grafik Tren Metrik EAR/MAR/PERCLOS (§5.2.4) ---")
    metrics_path = _pick_file("Metrics CSV", "logs/metrics_*.csv")
    if not metrics_path or not os.path.exists(metrics_path):
        print("Batal: berkas metrics tidak ditemukan.")
        return
    gt_path = _pick_file("Ground truth CSV (opsional)", "ground_truth*.csv")
    out_path = input("Simpan grafik ke (default: logs/metrics_plot.png): ").strip() or "logs/metrics_plot.png"

    plot_metrics(metrics_path, gt_path, out_path)
    print(f"Grafik disimpan: {out_path}")


MENU = {
    "1": ("Rekam sesi real-time (webcam/video)      — §5.2.1 / §5.2.2", menu_record_session),
    "2": ("Validasi akurasi terhadap ground truth   — §5.2.1 / §5.2.2", menu_validate_accuracy),
    "3": ("Benchmark performa PC vs Raspberry Pi 4   — §5.2.3", menu_benchmark),
    "4": ("Grafik tren metrik EAR/MAR/PERCLOS        — §5.2.4", menu_plot_metrics),
}


def main():
    while True:
        print("\n" + "=" * 68)
        print("  DATA YANG MASIH DIPERLUKAN — BAB V §5.2")
        print("=" * 68)
        for key, (label, _) in MENU.items():
            print(f"  {key}. {label}")
        print("  0. Keluar")
        choice = input("\nPilih nomor (bisa beberapa dipisah spasi, mis. '1 3 4'): ").strip()

        if choice in ("", "0", "q", "quit", "exit"):
            break
        for c in choice.split():
            entry = MENU.get(c)
            if entry:
                entry[1]()
            else:
                print(f"Pilihan tidak dikenal: {c}")


if __name__ == "__main__":
    main()
