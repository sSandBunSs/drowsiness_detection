"""Self-check for validate_accuracy confusion matrix logic (run: python test_validate_accuracy.py)."""
from validate_accuracy import confusion_matrix


def main():
    intervals = [(0.0, 10.0, "NORMAL"), (10.0, 20.0, "DROWSY")]
    metrics_rows = [
        {"elapsed_sec": "1", "status": "NORMAL"},   # aktual NORMAL, benar
        {"elapsed_sec": "5", "status": "DROWSY"},   # aktual NORMAL, salah (false positive)
        {"elapsed_sec": "15", "status": "DROWSY"},  # aktual DROWSY, benar
        {"elapsed_sec": "25", "status": "NORMAL"},  # di luar ground truth -> diabaikan
    ]

    matrix, skipped = confusion_matrix(metrics_rows, intervals)

    assert skipped == 1
    assert matrix["NORMAL"]["NORMAL"] == 1
    assert matrix["NORMAL"]["DROWSY"] == 1
    assert matrix["DROWSY"]["DROWSY"] == 1
    assert matrix["DROWSY"]["NORMAL"] == 0

    print("OK: confusion matrix + ground-truth interval matching verified")


if __name__ == "__main__":
    main()
