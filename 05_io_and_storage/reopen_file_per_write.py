"""Opening and closing a file for every record.

Run: python3 05_io_and_storage/reopen_file_per_write.py
"""
import os
import tempfile
import timeit

path = os.path.join(tempfile.gettempdir(), "efficiency_demo_out.txt")
records = [f"event {i}\n" for i in range(50_000)]


# BAD (by accident): a tidy helper "append_line(path, text)" that is perfectly
# safe on its own, then gets called in a loop. Each call = open + write +
# close (3+ syscalls, a flush to the OS, directory lookups).
def append_line(p, text):
    with open(p, "a") as f:
        f.write(text)

def slow():
    open(path, "w").close()
    for r in records:
        append_line(path, r)


# GOOD: open once; Python buffers small writes and flushes in big blocks.
def fast():
    with open(path, "w") as f:
        f.writelines(records)


print(f"open per write: {timeit.timeit(slow, number=1) * 1e3:8.1f} ms")
print(f"open once     : {timeit.timeit(fast, number=1) * 1e3:8.1f} ms")
os.remove(path)
