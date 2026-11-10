"""Logging costs CPU even when the message is thrown away.

Run: python3 06_databases_and_formats/lazy_logging.py
"""
import logging
import timeit

logging.basicConfig(level=logging.INFO)  # production: DEBUG is off
log = logging.getLogger("demo")
payload = {"items": list(range(500))}


# BAD (by accident): the f-string is built -- and str(payload) serialized --
# BEFORE logging decides the DEBUG message is disabled and drops it.
def slow():
    for _ in range(2000):
        log.debug(f"processing payload: {payload}")


# GOOD: pass args separately; formatting happens only if the record is emitted.
def fast():
    for _ in range(2000):
        log.debug("processing payload: %s", payload)


# If computing the argument itself is expensive, guard it explicitly:
def guarded():
    for _ in range(2000):
        if log.isEnabledFor(logging.DEBUG):
            log.debug("processing payload: %s", sorted(payload["items"]))


for fn in (slow, fast, guarded):
    print(f"{fn.__name__:8}: {timeit.timeit(fn, number=1) * 1e3:8.1f} ms")
