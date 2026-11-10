"""Awaiting inside a loop turns concurrent I/O back into sequential I/O.

Run: python3 05_io_and_storage/sequential_await.py
"""
import asyncio
import time


async def fetch(i):
    await asyncio.sleep(0.1)  # stand-in for a network or disk wait
    return i


async def slow():
    # BAD: async/await syntax, but each fetch waits for the previous one.
    # 20 x 100 ms = 2 s, with the CPU idle the whole time.
    return [await fetch(i) for i in range(20)]


async def fast():
    # GOOD: start all the waits together; total time ~ the slowest one.
    # (Cap concurrency with a Semaphore if the target can't take 20 at once.)
    return await asyncio.gather(*(fetch(i) for i in range(20)))


async def main():
    for fn in (slow, fast):
        start = time.perf_counter()
        await fn()
        print(f"{fn.__name__}: {time.perf_counter() - start:5.2f} s")


asyncio.run(main())
