"""Threads don't speed up CPU-bound Python (the GIL); processes do.

Run: python3 02_cpu/threads_vs_processes.py

Takeaway: "just add threads" is not free and not always effective. Threads
help I/O-bound work (waiting); for CPU-bound work you need processes, a
free-threaded build, or a compiled language. Locks/contention add more cost.
"""
import os
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def count_primes(limit):
    return sum(all(n % d for d in range(2, int(n**0.5) + 1)) for n in range(2, limit))


def timed(label, executor_cls, jobs):
    start = time.perf_counter()
    with executor_cls(max_workers=os.cpu_count()) as pool:
        list(pool.map(count_primes, jobs))
    print(f"{label:10}: {time.perf_counter() - start:6.2f} s")


if __name__ == "__main__":
    jobs = [200_000] * 4
    start = time.perf_counter()
    for j in jobs:
        count_primes(j)
    print(f"{'serial':10}: {time.perf_counter() - start:6.2f} s")
    timed("threads", ThreadPoolExecutor, jobs)     # ~same as serial (GIL)
    timed("processes", ProcessPoolExecutor, jobs)  # scales with cores
