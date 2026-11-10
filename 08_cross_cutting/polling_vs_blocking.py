"""Energy efficiency: waiting by polling keeps the CPU awake.

Run: python3 08_cross_cutting/polling_vs_blocking.py

On a phone or embedded device, CPU wake-ups are battery drain. We measure
CPU time (not wall time) used while "waiting" 1 second for an event.
"""
import threading
import time


def measure(wait_fn):
    event = threading.Event()
    threading.Timer(1.0, event.set).start()  # event fires after 1 second
    cpu_start = time.process_time()
    wait_fn(event)
    return time.process_time() - cpu_start


# BAD (by accident): "while not done: sleep(tiny)" -- wakes ~10,000 times/sec,
# each wake-up costing a context switch and keeping the core out of deep sleep.
# Even worse: no sleep at all (a pure spin loop) burns 100% of a core.
def poll(event):
    while not event.is_set():
        time.sleep(0.0001)


# GOOD: block until notified. The thread is descheduled; zero wake-ups
# until the event actually happens. (Same idea: epoll/select, asyncio,
# interrupts on embedded, push notifications instead of polling a server.)
def block(event):
    event.wait()


print(f"polling : {measure(poll) * 1e3:7.1f} ms of CPU in 1 s of waiting")
print(f"blocking: {measure(block) * 1e3:7.1f} ms of CPU in 1 s of waiting")
