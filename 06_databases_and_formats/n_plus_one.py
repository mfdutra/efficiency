"""The N+1 query problem: 1 query for the list, then N more, one per row.

Run: python3 06_databases_and_formats/n_plus_one.py

SQLite is in-process so each query is cheap; with a real database over a
network every extra query also pays a full round trip (~0.5-5 ms).
ORMs make this very easy to do by accident: touching `user.orders` inside a
loop silently fires a query per user (lazy loading).
"""
import timeit

from _db import make_db

db = make_db()


# BAD: 1 + 2000 queries.
def slow():
    result = {}
    for (uid,) in db.execute("SELECT id FROM users").fetchall():
        rows = db.execute("SELECT total FROM orders WHERE user_id = ?", (uid,))
        result[uid] = sum(t for (t,) in rows)
    return result


# GOOD: one query; let the database do the join and aggregation.
def fast():
    rows = db.execute(
        """SELECT u.id, COALESCE(SUM(o.total), 0)
           FROM users u LEFT JOIN orders o ON o.user_id = u.id
           GROUP BY u.id"""
    )
    return dict(rows)


a, b = slow(), fast()
assert a.keys() == b.keys() and all(abs(a[k] - b[k]) < 1e-6 for k in a)
print(f"N+1 queries: {timeit.timeit(slow, number=1) * 1e3:8.1f} ms")
print(f"one query  : {timeit.timeit(fast, number=1) * 1e3:8.1f} ms")
