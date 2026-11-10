"""Don't redo identical, expensive work: cache pure functions.

Run: python3 02_cpu/caching.py
"""
import timeit
from datetime import datetime
from functools import lru_cache

# A log with 200k rows but only 336 distinct date strings.
dates = [f"2025-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}" for i in range(200_000)]

# BAD: strptime is surprisingly slow (format parsing every call), and we call
# it 200k times to learn the same 336 answers over and over.
def slow():
    return [datetime.strptime(d, "%Y-%m-%d") for d in dates]

# GOOD: pure function + few distinct inputs = perfect cache candidate.
# maxsize bounds memory (see 03_memory/unbounded_cache.py for why that matters).
@lru_cache(maxsize=1024)
def parse(d):
    return datetime.strptime(d, "%Y-%m-%d")

def fast():
    return [parse(d) for d in dates]

assert slow() == fast()
print(f"no cache : {timeit.timeit(slow, number=1) * 1e3:8.1f} ms")
print(f"lru_cache: {timeit.timeit(fast, number=1) * 1e3:8.1f} ms")
