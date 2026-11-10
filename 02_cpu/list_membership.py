"""`x in some_list` is a linear scan. Inside a loop it becomes O(n * m).

Run: python3 02_cpu/list_membership.py
"""
import timeit

allowed = list(range(20_000))          # e.g. ids loaded from a file or DB
requests = list(range(18_000, 22_000))  # ids we need to check

# BAD: reads naturally, but each `in` scans up to 20,000 items.
def slow():
    return [r for r in requests if r in allowed]

# GOOD: build a set once (O(n)); each lookup is then O(1) on average.
allowed_set = set(allowed)
def fast():
    return [r for r in requests if r in allowed_set]

assert slow() == fast()
print(f"list: {timeit.timeit(slow, number=3) / 3 * 1e3:8.2f} ms")
print(f"set : {timeit.timeit(fast, number=3) / 3 * 1e3:8.2f} ms")
