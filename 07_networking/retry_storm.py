"""Immediate retries turn a hiccup into an outage.

Run: python3 07_networking/retry_storm.py

Simulation: a server can handle 100 requests per second. It hits trouble
for 2 seconds, then recovers. 1,000 clients are calling it. What load do
the clients create while it is trying to recover?
"""
import random

random.seed(1)
CLIENTS, OUTAGE_END, HORIZON = 1000, 2.0, 12.0


def simulate(next_delay, max_attempts):
    """Returns total requests sent and the peak load from RETRIES (after the initial burst)."""
    sent = []
    for _ in range(CLIENTS):
        t = random.uniform(0, 1)  # first call
        for attempt in range(max_attempts):
            sent.append(t)
            if t >= OUTAGE_END:  # server is back: success
                break
            t += next_delay(attempt)
    sent = [t for t in sent if t < HORIZON]
    peak = max(sum(1 for s in sent if w <= s < w + 1) for w in range(1, int(HORIZON)))
    return len(sent), peak


# BAD: "if it fails, try again right away" (fixed 50 ms), up to 50 times.
bad = simulate(lambda attempt: 0.05, max_attempts=50)

# GOOD: exponential backoff (0.1, 0.2, 0.4 ... capped) plus random jitter so
# clients don't all come back at the same instant.
good = simulate(lambda attempt: random.uniform(0, min(8, 0.1 * 2**attempt)), max_attempts=8)

print(f"fixed fast retries : {bad[0]:7,} requests total, peak retry load {bad[1]:6,}/s (capacity: 100/s)")
print(f"backoff with jitter: {good[0]:7,} requests total, peak retry load {good[1]:6,}/s")
