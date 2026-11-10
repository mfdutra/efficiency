"""`items = items + [x]` copies the whole list every time -> O(n^2).

Run: python3 02_cpu/quadratic_concat.py
"""
import timeit

N = 30_000

# BAD: looks harmless (and is "immutable style"), but allocates and copies a
# brand new list on every iteration.
def slow():
    items = []
    for i in range(N):
        items = items + [i]
    return items

# GOOD: append is amortized O(1) (a comprehension is even better).
def fast():
    return [i for i in range(N)]

assert slow() == fast()
print(f"concat : {timeit.timeit(slow, number=1) * 1e3:8.2f} ms")
print(f"append : {timeit.timeit(fast, number=1) * 1e3:8.2f} ms")
