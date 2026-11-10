"""SELECT * drags every column (including big blobs) across the wire.

Run: python3 06_databases_and_formats/fetch_only_what_you_need.py
"""
import timeit

from _db import make_db

db = make_db(users=5000, orders_per_user=0)


# BAD: `SELECT *` is convenient, but each row carries a 10 KB avatar we never
# use. Adding a column to the table later silently makes this slower.
def slow():
    return [row[1] for row in db.execute("SELECT * FROM users")]


# GOOD: name the columns you need. Less to read, copy, serialize and send --
# and an index covering these columns could answer without touching the table.
def fast():
    return [name for (name,) in db.execute("SELECT name FROM users")]


assert slow() == fast()
print(f"SELECT *    : {timeit.timeit(slow, number=5) / 5 * 1e3:8.2f} ms")
print(f"SELECT name : {timeit.timeit(fast, number=5) / 5 * 1e3:8.2f} ms")
