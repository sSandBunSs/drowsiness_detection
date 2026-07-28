"""
Perbandingan berpasangan adaptive vs fixed threshold pada baseline individu
yang sama — untuk BAB5.md §5.2.1 (bandingkan dengan kenaikan 1,53% Ersoy dkk.
2026).

`logs/metrics_*.csv` hanya menyimpan status yang dihasilkan pada threshold
adaptif yang aktif saat perekaman (mis. 0,301). Skrip ini menghitung ulang
status per frame dengan threshold TETAP (`--fixed-threshold`, default 0,25),
mereplikasi logika `_process_frame` di `detector.py` (EAR counter, MAR
counter, PERCLOS, prioritas status), lalu menyekor kedua versi terhadap
ground truth yang sama untuk perbandingan langsung.

Usage:
    python compare_adaptive_fixed.py logs/metrics_20260713_230527.csv ground_truth.csv
"""
import argparse
import csv
from collections import deque

from validate_accuracy import confusion_matrix, load_ground_truth, print_report

EAR_CONSEC_FRAMES = 20     # Config.ear_consec_frames
MAR_CONSEC_FRAMES = 15     # Config.mar_consec_frames
MAR_THRESHOLD = 0.65       # Config.mar_threshold
PERCLOS_THRESHOLD = 0.35   # Config.perclos_threshold
PERCLOS_WINDOW = 150       # Config.perclos_window


def recompute_status(metrics_rows, fixed_threshold):
    """Mereplikasi logika status detector.py._process_frame dengan threshold tetap."""
    perclos_window = deque(maxlen=PERCLOS_WINDOW)
    ear_counter = mar_counter = 0
    rows = []
    for row in metrics_rows:
        ear = float(row["ear_avg"])
        mar = float(row["mar"])

        perclos_window.append(ear)
        closed = sum(1 for e in perclos_window if e < fixed_threshold)
        perclos = closed / len(perclos_window)

        ear_counter = ear_counter + 1 if ear < fixed_threshold else 0
        mar_counter = mar_counter + 1 if mar > MAR_THRESHOLD else 0

        is_ear_alert = ear_counter >= EAR_CONSEC_FRAMES
        is_perclos_alert = perclos >= PERCLOS_THRESHOLD
        is_yawn_warning = mar_counter >= MAR_CONSEC_FRAMES

        if is_ear_alert or is_perclos_alert:
            status = "DROWSY"
        elif is_yawn_warning or ear_counter >= EAR_CONSEC_FRAMES // 2:
            status = "WARNING"
        else:
            status = "NORMAL"

        rows.append({"elapsed_sec": row["elapsed_sec"], "status": status})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("metrics_csv")
    parser.add_argument("ground_truth_csv")
    parser.add_argument("--fixed-threshold", type=float, default=0.25)
    args = parser.parse_args()

    with open(args.metrics_csv, newline="") as f:
        metrics_rows = list(csv.DictReader(f))
    intervals = load_ground_truth(args.ground_truth_csv)

    lighting = metrics_rows[0].get("lighting_condition", "?")
    print(f"=== Adaptif (threshold aktif saat perekaman, lighting={lighting}) ===")
    matrix_adaptive, skipped = confusion_matrix(metrics_rows, intervals)
    print_report(matrix_adaptive, skipped)
    total_adaptive = sum(sum(p.values()) for p in matrix_adaptive.values())
    correct_adaptive = sum(matrix_adaptive[l][l] for l in ("NORMAL", "WARNING", "DROWSY"))
    acc_adaptive = correct_adaptive / total_adaptive * 100 if total_adaptive else 0.0

    print(f"\n=== Fixed (threshold={args.fixed_threshold}) ===")
    fixed_rows = recompute_status(metrics_rows, args.fixed_threshold)
    matrix_fixed, skipped_fixed = confusion_matrix(fixed_rows, intervals)
    print_report(matrix_fixed, skipped_fixed)
    total_fixed = sum(sum(p.values()) for p in matrix_fixed.values())
    correct_fixed = sum(matrix_fixed[l][l] for l in ("NORMAL", "WARNING", "DROWSY"))
    acc_fixed = correct_fixed / total_fixed * 100 if total_fixed else 0.0

    print("\n=== Ringkasan ===")
    print(f"Akurasi adaptif : {acc_adaptive:.2f}%")
    print(f"Akurasi fixed   : {acc_fixed:.2f}%")
    print(f"Selisih (adaptif - fixed): {acc_adaptive - acc_fixed:+.2f} poin persentase")


if __name__ == "__main__":
    main()
