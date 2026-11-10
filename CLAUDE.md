# efficiency

Small, self-contained educational examples: an accidentally-inefficient version
vs. the efficient one, with comments explaining why. One directory per section of
the podcast outline (see README.md for the mapping).

- Python (stdlib only) by default; Rust (`04_cache_locality`) where Python hides the effect.
- Each script prints timings/sizes for both versions, runs in seconds, and asserts both give the same result.
- Keep examples short; the "bad" version should be code people write by accident, not strawmen.
- Rust: benchmark with `--release`, use `black_box` so LLVM can't optimize the work away.
- Keep README.md's table in sync when adding directories.
