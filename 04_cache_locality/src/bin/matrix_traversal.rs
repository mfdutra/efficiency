//! Same sum, same data, different loop order.
//! Run: cargo run --release --bin matrix_traversal
//!
//! A 2D grid is stored row by row in memory. Walking along a row touches
//! consecutive addresses (each 64-byte cache line serves 16 u32s). Walking
//! down a column jumps `N * 4` bytes each step, so nearly every access is a
//! cache miss -- the CPU sits idle waiting for RAM, not computing.
//! Python can't show this: interpreter overhead hides the memory effect.

use std::hint::black_box;
use std::time::Instant;

const N: usize = 4096; // 4096 * 4096 * 4 bytes = 64 MB, far bigger than any cache

fn main() {
    // black_box hides the contents from the optimizer; otherwise LLVM can see the
    // grid is just 0..N*N and compute the sum without touching memory at all.
    let grid: Vec<u32> = black_box((0..(N * N) as u32).map(|i| i.wrapping_mul(2654435761)).collect());

    // BAD (by accident): looks natural -- "for each column, for each row".
    let start = Instant::now();
    let mut sum = 0u64;
    for col in 0..N {
        for row in 0..N {
            sum += grid[row * N + col] as u64; // stride of 16 KB between accesses
        }
    }
    println!("column-major: {:>7.1?}  (sum {})", start.elapsed(), black_box(sum));

    // GOOD: inner loop walks memory sequentially; the hardware prefetcher
    // sees the pattern and streams data in ahead of time.
    let start = Instant::now();
    let mut sum = 0u64;
    for row in 0..N {
        for col in 0..N {
            sum += grid[row * N + col] as u64;
        }
    }
    println!("row-major   : {:>7.1?}  (sum {})", start.elapsed(), black_box(sum));
}
