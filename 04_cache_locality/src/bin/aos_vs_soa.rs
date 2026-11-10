//! Array-of-structures vs structure-of-arrays.
//! Run: cargo run --release --bin aos_vs_soa
//!
//! We only need one field (`x`) of each particle. In the AoS layout every
//! cache line we fetch is mostly fields we never read, so we move ~16x more
//! memory than necessary. SoA packs the hot field contiguously.

use std::hint::black_box;
use std::time::Instant;

const N: usize = 5_000_000;

// The "natural" way to model data: one struct per thing. 64 bytes each.
#[derive(Clone, Default)]
#[allow(dead_code)] // the point: these fields exist but this program never reads them
struct Particle {
    x: f32,
    y: f32,
    z: f32,
    vx: f32,
    vy: f32,
    vz: f32,
    mass: f32,
    charge: f32,
    name: [u8; 32], // cold data riding along in every cache line
}

// Hot fields split into their own array.
struct Particles {
    x: Vec<f32>,
    // y, z, ... would be separate Vecs too
}

fn main() {
    let aos: Vec<Particle> = black_box((0..N).map(|i| Particle { x: i as f32, ..Default::default() }).collect::<Vec<_>>());
    let soa = Particles { x: black_box((0..N).map(|i| i as f32).collect()) };

    let start = Instant::now();
    let sum: f32 = aos.iter().map(|p| p.x).sum(); // loads 64 bytes to use 4
    println!("AoS (320 MB read): {:>7.1?}  (sum {})", start.elapsed(), black_box(sum));

    let start = Instant::now();
    let sum: f32 = soa.x.iter().sum(); // loads 4 bytes to use 4 (and SIMD-friendly)
    println!("SoA ( 20 MB read): {:>7.1?}  (sum {})", start.elapsed(), black_box(sum));
}
