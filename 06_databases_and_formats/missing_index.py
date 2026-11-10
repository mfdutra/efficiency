"""Without an index, every lookup is a full table scan.

Run: python3 06_databases_and_formats/missing_index.py

Use EXPLAIN QUERY PLAN (EXPLAIN in Postgres/MySQL) to see what the database
will really do. 'SCAN' = read every row. 'SEARCH ... USING INDEX' = jump.
"""
import timeit

from _db import make_db

query = "SELECT SUM(total) FROM orders WHERE user_id = ?"

for label, indexed in (("no index  ", False), ("with index", True)):
    db = make_db(index=indexed)
    plan = db.execute("EXPLAIN QUERY PLAN " + query, (7,)).fetchone()[-1]
    t = timeit.timeit(lambda: [db.execute(query, (u,)).fetchone() for u in range(300)], number=1)
    print(f"{label}: {t * 1e3:8.1f} ms for 300 lookups   plan: {plan}")
