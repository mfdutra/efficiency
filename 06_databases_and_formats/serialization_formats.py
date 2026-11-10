"""Text vs binary vs compressed: size and CPU are a trade-off.

Run: python3 06_databases_and_formats/serialization_formats.py

Sensor readings are the typical case: millions of small numeric records
stored as JSON "because it was easy".
"""
import gzip
import json
import struct
import timeit

readings = [(i, 20.0 + (i % 100) / 10, i % 256) for i in range(100_000)]  # (id, temp, flags)

# BAD (by accident): self-describing JSON repeats every field name per record
# and writes numbers as text.
as_json = json.dumps([{"id": i, "temp": t, "flags": f} for i, t, f in readings]).encode()

# GOOD for fixed-shape numeric data: packed binary, 13 bytes/record, no parsing.
as_binary = b"".join(struct.pack("<IdB", *r) for r in readings)

# Compression shrinks anything repetitive, but costs CPU on both ends.
# Worth it for network/storage-bound data; not free for hot paths.
as_json_gz = gzip.compress(as_json, compresslevel=6)

print(f"json        : {len(as_json) / 1e6:6.2f} MB")
print(f"json + gzip : {len(as_json_gz) / 1e6:6.2f} MB   "
      f"(compress cost {timeit.timeit(lambda: gzip.compress(as_json, 6), number=1) * 1e3:.0f} ms)")
print(f"binary      : {len(as_binary) / 1e6:6.2f} MB")
print(f"decode json  : {timeit.timeit(lambda: json.loads(as_json), number=1) * 1e3:6.1f} ms")
print(f"decode binary: {timeit.timeit(lambda: list(struct.iter_unpack('<IdB', as_binary)), number=1) * 1e3:6.1f} ms")
