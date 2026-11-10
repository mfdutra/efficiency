"""Loading everything just to loop over it once: memory scales with input size.

Run: python3 03_memory/read_whole_file.py
"""
import os
import tempfile
import tracemalloc

# Make a ~20 MB log file to work with.
path = os.path.join(tempfile.gettempdir(), "efficiency_demo.log")
with open(path, "w") as f:
    f.writelines(f"2025-01-01 INFO request {i} ok\n" for i in range(600_000))


# BAD: readlines() materializes every line (plus a str object each) at once.
# Peak memory ~ file size * overhead. A 10 GB log means 10+ GB of RAM.
def slow():
    with open(path) as f:
        return sum(1 for line in f.readlines() if "request 5" in line)


# GOOD: iterating the file streams one line at a time. Memory stays flat
# regardless of file size, and the OS read-ahead keeps it fast.
def fast():
    with open(path) as f:
        return sum(1 for line in f if "request 5" in line)


for fn in (slow, fast):
    tracemalloc.start()
    result = fn()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{fn.__name__}: result={result} peak memory={peak / 1e6:7.2f} MB")
os.remove(path)
