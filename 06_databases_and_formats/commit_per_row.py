"""One transaction per row = one durable disk flush (fsync) per row.

Run: python3 06_databases_and_formats/commit_per_row.py

On flash storage this is also write amplification: many tiny writes wear
the device faster than a few large ones.
"""
import os
import sqlite3
import tempfile
import timeit

path = os.path.join(tempfile.gettempdir(), "efficiency_demo.db")
rows = [(i, f"name{i}") for i in range(1000)]


def fresh():
    if os.path.exists(path):
        os.remove(path)
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE t (id INT, name TEXT)")
    return db


# BAD: committing inside the loop (or autocommit mode) forces SQLite to sync
# to disk after every single insert.
def slow():
    db = fresh()
    for r in rows:
        db.execute("INSERT INTO t VALUES (?, ?)", r)
        db.commit()


# GOOD: batch many rows into one transaction -> one sync.
def fast():
    db = fresh()
    db.executemany("INSERT INTO t VALUES (?, ?)", rows)
    db.commit()


print(f"commit per row: {timeit.timeit(slow, number=1) * 1e3:8.1f} ms")
print(f"one commit    : {timeit.timeit(fast, number=1) * 1e3:8.1f} ms")
os.remove(path)
