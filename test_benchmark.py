"""Self-check for benchmark latency stats logic (run: python test_benchmark.py)."""
from benchmark import compute_latency_stats


def main():
    stats = compute_latency_stats([10.0, 20.0, 30.0, 40.0, 100.0])
    assert stats["mean_ms"] == 40.0
    assert stats["median_ms"] == 30.0
    assert stats["max_ms"] == 100.0
    assert stats["p95_ms"] == 100.0  # n=5 -> idx min(4, int(5*0.95)=4) = 4 (last/max)

    empty = compute_latency_stats([])
    assert empty == {"mean_ms": 0.0, "median_ms": 0.0, "p95_ms": 0.0, "max_ms": 0.0}

    print("OK: benchmark latency stats verified")


if __name__ == "__main__":
    main()
