"""A cache with no eviction policy is a memory leak with good intentions.

Run: python3 03_memory/unbounded_cache.py
"""
import tracemalloc
from functools import lru_cache

# BAD: the classic hand-rolled memo dict. Fine in a script, a slow leak in a
# long-running server where keys (user ids, urls, request ids) never repeat.
_cache = {}

def render_unbounded(user_id):
    if user_id not in _cache:
        _cache[user_id] = f"<profile for user {user_id}>" * 10
    return _cache[user_id]


# GOOD: bounded. Least-recently-used entries are evicted, memory is capped,
# and hot keys still hit. Always ask "what removes entries from this cache?"
@lru_cache(maxsize=1_000)
def render_bounded(user_id):
    return f"<profile for user {user_id}>" * 10


for name, fn in (("unbounded", render_unbounded), ("bounded  ", render_bounded)):
    tracemalloc.start()
    for uid in range(100_000):  # 100k distinct users, each seen once
        fn(uid)
    current, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{name}: {current / 1e6:7.2f} MB retained")
