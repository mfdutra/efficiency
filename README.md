# Writing Efficient Code: examples

Companion code for the *Runtime Arguments* episode 41. Each example shows a
problem solved **accidentally inefficiently** (the kind of code that looks
fine in review) and then **the efficient way**, with comments explaining why.

Python 3.12+ (stdlib only). Cache/memory-layout examples are Rust, because
the Python interpreter hides those effects.

| Directory | Doc section | Examples |
|---|---|---|
| `01_measurement/` | The measurement mindset | benchmark pitfalls, profile before optimizing |
| `02_cpu/` | CPU | list vs set, quadratic concat, loop invariants, caching, laziness, threads vs processes |
| `03_memory/` | Memory capacity and allocation | readlines, list vs generator, object overhead, unbounded cache |
| `04_cache_locality/` (Rust) | Memory bandwidth and cache hierarchy | row/column traversal, AoS vs SoA, false sharing |
| `05_io_and_storage/` | I/O and storage | reopen per write, syscall overhead, sequential await |
| `06_databases_and_formats/` | Databases, formats, logging | N+1, missing index, SELECT *, commit per row, lazy logging, serialization |
| `07_networking/` | Networking | chatty API, connection reuse, retry storms |
| `08_cross_cutting/` | Cross-cutting | polling vs blocking (energy) |

## Running

```bash
python3 02_cpu/list_membership.py
cd 06_databases_and_formats && python3 n_plus_one.py   # uses _db.py helper
cd 04_cache_locality && cargo run --release --bin matrix_traversal
```

Always run Rust with `--release`. Absolute timings vary by machine; look at the ratios.
