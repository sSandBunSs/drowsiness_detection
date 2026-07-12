"""
Validasi akurasi deteksi kantuk terhadap ground truth manual.

Ground truth CSV dibuat manual sambil menonton rekaman video (kolom):
    start_sec,end_sec,label
    0,15,NORMAL
    15,22,DROWSY
    22,40,NORMAL

label harus salah satu dari: NORMAL, WARNING, DROWSY (sama seperti status
yang ditulis detector.py ke logs/metrics_*.csv).

Usage:
    python validate_accuracy.py logs/metrics_20260708_021937.csv ground_truth.csv
"""
import csv
import sys
from collections import defaultdict

LABELS = ("NORMAL", "WARNING", "DROWSY")


def load_ground_truth(path):
    intervals = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            intervals.append((
                float(row["start_sec"]), float(row["end_sec"]),
                row["label"].strip().upper()
            ))
    return intervals


def label_at(intervals, t):
    for start, end, label in intervals:
        if start <= t < end:
            return label
    return None


def load_metrics(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def confusion_matrix(metrics_rows, intervals):
    matrix = defaultdict(lambda: defaultdict(int))  # matrix[aktual][prediksi]
    skipped = 0
    for row in metrics_rows:
        t = float(row["elapsed_sec"])
        actual = label_at(intervals, t)
        if actual is None:
            skipped += 1
            continue
        predicted = row["status"].strip().upper()
        matrix[actual][predicted] += 1
    return matrix, skipped


def print_report(matrix, skipped):
    total = sum(sum(preds.values()) for preds in matrix.values())
    correct = sum(matrix[l][l] for l in LABELS)

    print(f"\nTotal frame dinilai: {total}")
    print(f"Frame diabaikan (di luar ground truth): {skipped}")
    if total:
        print(f"Akurasi keseluruhan: {correct / total * 100:.2f}%\n")
    else:
        print("Tidak ada data untuk dinilai.\n")
        return

    print("Confusion matrix (baris=aktual, kolom=prediksi):")
    print("        " + "".join(f"{l:>10}" for l in LABELS))
    for actual in LABELS:
        row = "".join(f"{matrix[actual][pred]:>10}" for pred in LABELS)
        print(f"{actual:>8}{row}")

    print("\nPer-kelas (precision/recall/F1):")
    for label in LABELS:
        tp = matrix[label][label]
        fp = sum(matrix[a][label] for a in LABELS if a != label)
        fn = sum(matrix[label][p] for p in LABELS if p != label)
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        print(f"  {label:>8}: precision={precision:.3f}  recall={recall:.3f}  f1={f1:.3f}")

    tp = matrix["DROWSY"]["DROWSY"]
    fn = sum(matrix["DROWSY"][p] for p in LABELS if p != "DROWSY")
    fp = sum(matrix[a]["DROWSY"] for a in LABELS if a != "DROWSY")
    tn = total - tp - fn - fp
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    print("\nDROWSY vs lainnya (biner, metrik keselamatan utama):")
    print(f"  TP={tp} FN={fn} FP={fp} TN={tn}")
    print(f"  Recall (sensitivity) = {recall:.3f}  <- proporsi kejadian kantuk aktual yang terdeteksi")
    print(f"  Precision            = {precision:.3f}  <- proporsi alarm kantuk yang benar")


def main():
    if len(sys.argv) != 3:
        print("Usage: python validate_accuracy.py <metrics.csv> <ground_truth.csv>")
        sys.exit(1)
    metrics_rows = load_metrics(sys.argv[1])
    intervals = load_ground_truth(sys.argv[2])
    matrix, skipped = confusion_matrix(metrics_rows, intervals)
    print_report(matrix, skipped)


if __name__ == "__main__":
    main()
