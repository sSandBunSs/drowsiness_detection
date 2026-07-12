"""Self-check for MetricsLogger CSV schema (run: python test_metrics_logger.py)."""
import csv
import tempfile

from metrics_logger import MetricsLogger


def main():
    with tempfile.TemporaryDirectory() as tmp:
        log = MetricsLogger(output_dir=tmp, platform="TestPlatform",
                             lighting_condition="siang")
        log.log_frame(ear_l=0.28, ear_r=0.27, mar=0.1, perclos=0.05,
                      status="NORMAL", ear_counter=0, mar_counter=0)
        log.log_event("DROWSY", "EAR=0.199 frames=20")

        with open(log.csv_path, newline="") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 1
        assert rows[0]["platform"] == "TestPlatform"
        assert rows[0]["lighting_condition"] == "siang"
        assert rows[0]["status"] == "NORMAL"

        with open(log.event_path, newline="") as f:
            events = list(csv.DictReader(f))
        assert len(events) == 1
        assert events[0]["event_type"] == "DROWSY"

    print("OK: metrics_logger CSV schema + platform/lighting_condition verified")


if __name__ == "__main__":
    main()
