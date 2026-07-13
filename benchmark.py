"""
Benchmark performa (FPS/latency) untuk perbandingan platform PC vs Raspberry Pi 4 (BAB V §5.2.3).

Menjalankan pipeline deteksi asli (DrowsinessDetector._process_frame) tanpa
GUI/display, sehingga perintah yang sama persis bisa dijalankan headless via
SSH di Raspberry Pi 4 (lihat catatan "Running MediaPipe headless" di
CLAUDE.md) dan dibandingkan langsung dengan hasil di PC. Gunakan berkas video
yang sama pada kedua platform, bukan webcam langsung, agar FPS sumber video
tidak menjadi variabel perancu (lihat BAB3.md §3.3).

Usage:
    python benchmark.py path/to/clip.mp4
    python benchmark.py path/to/clip.mp4 --frames 500 --csv logs/benchmark_results.csv
"""
import argparse
import csv
import os
import platform
import statistics
import time

from detector import Config, DrowsinessDetector


def compute_latency_stats(latencies_ms):
    """Statistik murni, dipisah dari I/O agar bisa diuji tanpa kamera/video (lihat test_benchmark.py)."""
    if not latencies_ms:
        return {"mean_ms": 0.0, "median_ms": 0.0, "p95_ms": 0.0, "max_ms": 0.0}
    sorted_ms = sorted(latencies_ms)
    p95_idx = min(len(sorted_ms) - 1, int(len(sorted_ms) * 0.95))
    return {
        "mean_ms": statistics.mean(latencies_ms),
        "median_ms": statistics.median(latencies_ms),
        "p95_ms": sorted_ms[p95_idx],
        "max_ms": max(latencies_ms),
    }


def benchmark_video(video_path, max_frames=None, warmup=10):
    # ponytail: alarm/metrics/recording dimatikan — ini uji performa murni, bukan uji akurasi/logging.
    config = Config(log_metrics=False, alarm_enabled=False, record_video=False)
    detector = DrowsinessDetector(config)

    if not detector._init_camera(video_path):
        raise FileNotFoundError(f"Tidak bisa membuka video: {video_path}")

    latencies_ms = []
    n_frames = 0
    start = time.perf_counter()

    try:
        while True:
            ret, frame = detector.cap.read()
            if not ret:
                break
            n_frames += 1

            t0 = time.perf_counter()
            detector._process_frame(frame)
            t1 = time.perf_counter()

            if n_frames > warmup:
                latencies_ms.append((t1 - t0) * 1000.0)
            if max_frames and n_frames >= max_frames:
                break
    finally:
        # Tanpa cv2.destroyAllWindows()/imshow: harus tetap aman di opencv-python-headless (RPi).
        detector.cap.release()
        detector.face_landmarker.close()

    elapsed = time.perf_counter() - start
    stats = compute_latency_stats(latencies_ms)
    return {
        "platform": "Raspberry Pi 4" if config.is_raspberry_pi else platform.system(),
        "video_source": video_path,
        "n_frames": n_frames,
        "elapsed_s": round(elapsed, 3),
        "fps_avg": round(n_frames / elapsed, 2) if elapsed > 0 else 0.0,
        **{k: round(v, 2) for k, v in stats.items()},
    }


def append_csv(result, csv_path):
    os.makedirs(os.path.dirname(csv_path) or ".", exist_ok=True)
    is_new = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(result.keys()))
        if is_new:
            writer.writeheader()
        writer.writerow(result)


def print_report(result):
    print(f"\nPlatform      : {result['platform']}")
    print(f"Video         : {result['video_source']}")
    print(f"Frame diproses: {result['n_frames']} (dalam {result['elapsed_s']}s)")
    print(f"FPS rata-rata : {result['fps_avg']}")
    print(f"Latency/frame : mean={result['mean_ms']}ms  median={result['median_ms']}ms  "
          f"p95={result['p95_ms']}ms  max={result['max_ms']}ms")
    print("\nBaris tabel BAB V §5.2.3 (Markdown):")
    print(f"| {result['platform']} | {result['fps_avg']} | {result['mean_ms']} | — |")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("video", help="Path ke berkas video (sama persis untuk PC dan RPi4)")
    parser.add_argument("--frames", type=int, default=None, help="Batas jumlah frame (default: semua)")
    parser.add_argument("--warmup", type=int, default=10, help="Frame awal yang diabaikan dari statistik latency")
    parser.add_argument("--csv", default="logs/benchmark_results.csv", help="Berkas CSV untuk akumulasi hasil")
    args = parser.parse_args()

    result = benchmark_video(args.video, max_frames=args.frames, warmup=args.warmup)
    print_report(result)
    append_csv(result, args.csv)
    print(f"\nHasil ditambahkan ke {args.csv} — jalankan skrip ini di PC lalu di Raspberry Pi 4 "
          "dengan video yang sama untuk mengisi tabel perbandingan.")


if __name__ == "__main__":
    main()
