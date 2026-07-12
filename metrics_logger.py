"""
Metrics Logger — Pencatat Data untuk Keperluan Penelitian
Menyimpan data EAR, MAR, PERCLOS, dan event ke CSV.
"""
import csv
import os
import time
from datetime import datetime


class MetricsLogger:
    def __init__(self, output_dir="logs", platform="", lighting_condition=""):
        os.makedirs(output_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csv_path = os.path.join(output_dir, f"metrics_{ts}.csv")
        self.event_path = os.path.join(output_dir, f"events_{ts}.csv")
        self.platform = platform
        self.lighting_condition = lighting_condition

        # Inisialisasi CSV metrics
        with open(self.csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "elapsed_sec",
                "ear_left", "ear_right", "ear_avg",
                "mar", "perclos", "status",
                "ear_counter", "mar_counter",
                "platform", "lighting_condition"
            ])

        # Inisialisasi CSV events
        with open(self.event_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "elapsed_sec", "event_type", "value"])

        self.start_time = time.time()
        print(f"MetricsLogger aktif: {self.csv_path}")

    def log_frame(self, ear_l, ear_r, mar, perclos, status,
                  ear_counter, mar_counter):
        elapsed = round(time.time() - self.start_time, 3)
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        ear_avg = round((ear_l + ear_r) / 2, 4)
        with open(self.csv_path, "a", newline="") as f:
            csv.writer(f).writerow([
                ts, elapsed,
                round(ear_l, 4), round(ear_r, 4), ear_avg,
                round(mar, 4), round(perclos, 4),
                status, ear_counter, mar_counter,
                self.platform, self.lighting_condition
            ])

    def log_event(self, event_type: str, value: str = ""):
        elapsed = round(time.time() - self.start_time, 3)
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        with open(self.event_path, "a", newline="") as f:
            csv.writer(f).writerow([ts, elapsed, event_type, value])

    def get_paths(self):
        return {"metrics": self.csv_path, "events": self.event_path}
