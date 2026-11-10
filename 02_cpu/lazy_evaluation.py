"""A list comprehension inside any()/all() defeats short-circuiting.

Run: python3 02_cpu/lazy_evaluation.py
"""
import timeit

calls = 0

def is_bad(x):  # pretend this is expensive
    global calls
    calls += 1
    return x == 3

data = list(range(100_000))

# BAD: the [] builds the full list first, so is_bad runs 100,000 times even
# though the answer is known after 4 elements.
def slow():
    return any([is_bad(x) for x in data])

# GOOD: a generator expression is lazy; any() stops at the first True.
def fast():
    return any(is_bad(x) for x in data)

for fn in (slow, fast):
    calls = 0
    fn()
    print(f"{fn.__name__}: {calls:>7,} calls to is_bad, "
          f"{timeit.timeit(fn, number=1) * 1e3:8.3f} ms")
