"""Self-check for plot_trends metrics loading (run: python test_plot_trends.py)."""
import csv
import os
import tempfile

from plot_trends import load_metrics


def main():
    rows = [
        {"timestamp": "0", "elapsed_sec": "1.0", "ear_left": "0.4", "ear_right": "0.4",
         "ear_avg": "0.4", "mar": "0.3", "perclos": "0.0", "status": "NORMAL",
         "ear_counter": "0", "mar_counter": "0", "platform": "Windows", "lighting_condition": "siang"},
        {"timestamp": "1", "elapsed_sec": "2.0", "ear_left": "0.2", "ear_right": "0.2",
         "ear_avg": "0.2", "mar": "0.7", "perclos": "0.5", "status": "DROWSY",
         "ear_counter": "20", "mar_counter": "16", "platform": "Windows", "lighting_condition": "siang"},
    ]
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
        path = f.name

    try:
        t, ear, mar, perclos = load_metrics(path)
        assert t == [1.0, 2.0]
        assert ear == [0.4, 0.2]
        assert mar == [0.3, 0.7]
        assert perclos == [0.0, 0.5]
    finally:
        os.unlink(path)

    print("OK: plot_trends metrics CSV parsing verified")


if __name__ == "__main__":
    main()
