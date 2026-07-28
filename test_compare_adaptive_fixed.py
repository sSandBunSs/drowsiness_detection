"""Self-check for compare_adaptive_fixed status recomputation (run: python test_compare_adaptive_fixed.py)."""
from compare_adaptive_fixed import recompute_status


def main():
    # Prime the 150-frame PERCLOS window with alert EAR so the PERCLOS alert
    # (ratio-based) can't fire yet, isolating the EAR consecutive-frame
    # counter logic: 25 low-EAR frames after that should trip DROWSY at
    # EAR_CONSEC_FRAMES=20 frames, WARNING at half that.
    priming = [{"elapsed_sec": str(i), "ear_avg": "0.40", "mar": "0.10"} for i in range(150)]
    low = [{"elapsed_sec": str(150 + i), "ear_avg": "0.10", "mar": "0.10"} for i in range(25)]
    result = recompute_status(priming + low, fixed_threshold=0.25)
    statuses = [r["status"] for r in result[150:]]

    assert statuses[0] == "NORMAL"
    assert statuses[9] == "WARNING"   # ear_counter=10 >= EAR_CONSEC_FRAMES//2
    assert statuses[19] == "DROWSY"   # ear_counter=20 >= EAR_CONSEC_FRAMES
    assert statuses[24] == "DROWSY"

    # EAR back above threshold -> counter resets, status returns to NORMAL
    recover = [{"elapsed_sec": "175", "ear_avg": "0.40", "mar": "0.10"}]
    result_recover = recompute_status(priming + low + recover, fixed_threshold=0.25)
    assert result_recover[-1]["status"] == "NORMAL"

    print("OK: adaptive/fixed status recomputation verified")


if __name__ == "__main__":
    main()
