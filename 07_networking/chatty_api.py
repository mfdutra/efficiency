"""Round trips dominate: 100 tiny requests cost far more than 1 bigger one.

Run: python3 07_networking/chatty_api.py

Simulated, so it runs offline. A real cross-region call is 50-150 ms; the
payload transfer time is usually negligible by comparison.
"""
import time

RTT = 0.05  # 50 ms round trip
USERS = {i: {"id": i, "name": f"user{i}"} for i in range(100)}


def get_user(user_id):  # GET /users/<id>
    time.sleep(RTT)
    return USERS[user_id]


def get_users(ids):  # GET /users?ids=1,2,3...
    time.sleep(RTT + 0.0001 * len(ids))  # tiny extra payload cost
    return [USERS[i] for i in ids]


ids = list(range(100))

# BAD: an innocent-looking loop over a client library = 100 round trips.
start = time.perf_counter()
slow = [get_user(i) for i in ids]
print(f"one request per item: {time.perf_counter() - start:5.2f} s")

# GOOD: a batch endpoint (or GraphQL / gRPC streaming / pipelining).
start = time.perf_counter()
fast = get_users(ids)
print(f"one batched request : {time.perf_counter() - start:5.2f} s")
assert slow == fast
