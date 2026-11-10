"""Shared helper: an in-memory SQLite database with users and orders."""
import sqlite3


def make_db(users=2000, orders_per_user=20, index=True):
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, avatar BLOB)")
    db.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INT, total REAL)")
    db.executemany(
        "INSERT INTO users VALUES (?, ?, ?)",
        ((i, f"user{i}", b"x" * 10_000) for i in range(users)),
    )
    db.executemany(
        "INSERT INTO orders (user_id, total) VALUES (?, ?)",
        ((u, 9.99) for u in range(users) for _ in range(orders_per_user)),
    )
    if index:
        db.execute("CREATE INDEX idx_orders_user ON orders (user_id)")
    db.commit()
    return db
