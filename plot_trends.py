"""
Grafik tren EAR/MAR/PERCLOS terhadap waktu, dengan interval DROWSY (ground
truth) diarsir — untuk BAB5.md §5.2.4 (Gambar 5.1/5.2).

Usage:
    python plot_trends.py logs/metrics_20260713_230527.csv ground_truth.csv figures/gambar_5_1_trend_siang.png --title "Sesi Siang"
    python plot_trends.py logs/metrics_20260713_231846.csv ground_truth_malam.csv figures/gambar_5_2_trend_malam.png --title "Sesi Malam"
"""
import argparse
import csv
import os

import matplotlib.pyplot as plt

from validate_accuracy import load_ground_truth


def load_metrics(path):
    t, ear, mar, perclos = [], [], [], []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            t.append(float(row["elapsed_sec"]))
            ear.append(float(row["ear_avg"]))
            mar.append(float(row["mar"]))
            perclos.append(float(row["perclos"]))
    return t, ear, mar, perclos


def plot_trends(metrics_csv, ground_truth_csv, output_png, title=""):
    t, ear, mar, perclos = load_metrics(metrics_csv)
    intervals = load_ground_truth(ground_truth_csv)
    drowsy_spans = [(s, e) for s, e, label in intervals if label == "DROWSY"]

    fig, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 7))
    series = [("EAR", ear, "tab:blue"), ("MAR", mar, "tab:green"),
              ("PERCLOS", perclos, "tab:purple")]
    for ax, (label, values, color) in zip(axes, series):
        ax.plot(t, values, color=color, linewidth=0.8)
        ax.set_ylabel(label)
        for start, end in drowsy_spans:
            ax.axvspan(start, end, color="red", alpha=0.15)
        ax.grid(alpha=0.3)

    axes[-1].set_xlabel("Waktu (detik)")
    axes[0].set_title(title or os.path.basename(metrics_csv))
    fig.tight_layout()
    os.makedirs(os.path.dirname(output_png) or ".", exist_ok=True)
    fig.savefig(output_png, dpi=150)
    print(f"Tersimpan: {output_png}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("metrics_csv")
    parser.add_argument("ground_truth_csv")
    parser.add_argument("output_png")
    parser.add_argument("--title", default="")
    args = parser.parse_args()
    plot_trends(args.metrics_csv, args.ground_truth_csv, args.output_png, args.title)


if __name__ == "__main__":
    main()
