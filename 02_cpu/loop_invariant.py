"""Work that does not depend on the loop variable should live outside the loop.

Run: python3 02_cpu/loop_invariant.py
"""
import timeit

data = list(range(5_000))

# BAD: max(data) is re-evaluated for every element -> O(n^2).
# Compilers sometimes hoist this for you; the Python interpreter never will.
def slow():
    return [x / max(data) for x in data]

# GOOD: compute once, reuse.
def fast():
    top = max(data)
    return [x / top for x in data]

assert slow() == fast()
print(f"inside loop : {timeit.timeit(slow, number=1) * 1e3:8.2f} ms")
print(f"hoisted     : {timeit.timeit(fast, number=1) * 1e3:8.2f} ms")
