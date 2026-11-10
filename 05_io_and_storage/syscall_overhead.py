"""Every read()/write() call into the kernel costs ~1 microsecond or more,
no matter how few bytes it moves. Batch them.

Run: python3 05_io_and_storage/syscall_overhead.py
"""
import os
import tempfile
import timeit

path = os.path.join(tempfile.gettempdir(), "efficiency_demo_bytes.bin")
with open(path, "wb") as f:
    f.write(os.urandom(2_000_000))


# BAD: buffering=0 gives raw file access; reading one byte = one syscall.
# This happens by accident when someone disables buffering "to be safe" or
# uses os.read(fd, 1) in a parser.
def slow():
    total = 0
    with open(path, "rb", buffering=0) as f:
        while b := f.read(1):
            total += b[0]
    return total


# GOOD: read in large chunks (64 KiB), then process in memory.
def fast():
    total = 0
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            total += sum(chunk)
    return total


assert slow() == fast()
print(f"1 byte/syscall : {timeit.timeit(slow, number=1) * 1e3:8.1f} ms")
print(f"64 KiB chunks  : {timeit.timeit(fast, number=1) * 1e3:8.1f} ms")
os.remove(path)
