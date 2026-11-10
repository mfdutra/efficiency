"""Intermediate lists you only iterate once cost memory for nothing.

Run: python3 03_memory/list_vs_generator.py
"""
import tracemalloc

N = 2_000_000


def measure(fn):
    tracemalloc.start()
    result = fn()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak / 1e6


# BAD: the square brackets build a 2M-element list (and 2M int objects) first.
slow = lambda: sum([x * x for x in range(N)])
# GOOD: a generator yields one value at a time; sum() consumes it immediately.
fast = lambda: sum(x * x for x in range(N))

for name, fn in (("list     ", slow), ("generator", fast)):
    result, peak = measure(fn)
    print(f"{name}: result={result} peak={peak:8.2f} MB")
