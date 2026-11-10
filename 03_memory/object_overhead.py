"""Object overhead in managed languages: every Python object carries a header,
and a per-instance __dict__ costs far more than the data it stores.

Run: python3 03_memory/object_overhead.py
"""
import tracemalloc
from dataclasses import dataclass
from typing import NamedTuple

N = 200_000


# BAD (by accident): the default for "a little record" -- a plain class (or a
# dict). Each instance has its own hash table for attributes.
class PointDict:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z


# BETTER: __slots__ stores attributes in a fixed layout. No per-instance dict.
@dataclass(slots=True)
class PointSlots:
    x: float
    y: float
    z: float


# ALSO GOOD: tuples are immutable and compact; NamedTuple adds field names.
class PointTuple(NamedTuple):
    x: float
    y: float
    z: float


def measure(make):
    tracemalloc.start()
    items = [make(float(i), 1.0, 2.0) for i in range(N)]
    current, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return current / N, len(items)


for name, make in [
    ("dict            ", lambda x, y, z: {"x": x, "y": y, "z": z}),
    ("plain class     ", PointDict),
    ("dataclass(slots)", PointSlots),
    ("NamedTuple      ", PointTuple),
]:
    per_item, _ = measure(make)
    print(f"{name}: {per_item:6.0f} bytes per record")
