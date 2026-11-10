//! False sharing: threads fight over a cache line without sharing any data.
//! Run: cargo run --release --bin false_sharing
//!
//! Each thread increments ITS OWN counter -- no logical sharing at all. But
//! the four counters sit next to each other, inside one 64-byte cache line.
//! Every write invalidates that line in the other cores' caches, so they
//! ping-pong it back and forth. Padding each counter to its own line fixes it.

use std::sync::atomic::{AtomicU64, Ordering::Relaxed};
use std::thread;
use std::time::Instant;

const THREADS: usize = 4;
const ITERS: u64 = 50_000_000;

// BAD (by accident): a plain array of counters, 8 bytes apiece.
struct Packed([AtomicU64; THREADS]);

// GOOD: align each counter to a cache line (64 bytes on most CPUs).
#[repr(align(64))]
struct Padded(AtomicU64);

fn run(label: &str, counters: Vec<&AtomicU64>) {
    let start = Instant::now();
    thread::scope(|s| {
        for c in &counters {
            s.spawn(move || {
                for _ in 0..ITERS {
                    c.fetch_add(1, Relaxed);
                }
            });
        }
    });
    println!("{label}: {:>7.1?}", start.elapsed());
}

fn main() {
    let packed = Packed(Default::default());
    run("same cache line   ", packed.0.iter().collect());

    let padded: Vec<Padded> = (0..THREADS).map(|_| Padded(AtomicU64::new(0))).collect();
    run("own cache line each", padded.iter().map(|p| &p.0).collect());
}
