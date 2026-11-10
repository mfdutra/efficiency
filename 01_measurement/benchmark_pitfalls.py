"""Measurement pitfalls: a benchmark that lies vs. one you can trust.

Run: python3 benchmark_pitfalls.py
"""
import random
import time
import timeit


def work(data):
    return sorted(data)


# ---------------------------------------------------------------------------
# BAD (by accident): the classic "quick timing" most of us have written.
#   * the clock is time.time(): low resolution, can jump if NTP adjusts it
#   * test data is tiny, so the result says nothing about real workloads
#   * data generation is inside the timed region (measures the wrong thing)
#   * only ONE run: cold caches, noisy machine, no idea about variance
# ---------------------------------------------------------------------------
start = time.time()
data = [random.random() for _ in range(100)]
work(data)
print(f"bad : {(time.time() - start) * 1e6:9.1f} us  (one run, tiny input, includes setup)")

# ---------------------------------------------------------------------------
# GOOD: realistic size, setup outside the timer, many repeats, take the min
# (the min is the run with the least noise from other processes).
# ---------------------------------------------------------------------------
data = [random.random() for _ in range(100_000)]
runs = timeit.repeat(lambda: work(data), number=1, repeat=7)
print(f"good: {min(runs) * 1e6:9.1f} us  (best of 7, 100k items, setup excluded)")
print(f"      spread: {min(runs) * 1e3:.2f}-{max(runs) * 1e3:.2f} ms -> know your variance")
