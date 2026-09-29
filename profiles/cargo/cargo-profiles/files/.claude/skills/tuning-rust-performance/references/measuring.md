{%- set lints = devset.layers | selectattr("profile", "equalto", "rust-lints") | map(attribute="features") | first | default([]) -%}
# Measuring

Read this before changing code to make it faster, before a benchmark or a
profile, and before a claim about speed in a doc, a commit or a review. Code is
made faster here by measuring it, and a claim of speed is a number someone else
can run again: what was measured, on what machine, with what build, and where
the run is kept. The numbers in these examples were measured, by the benchmark
shown below, on the machine its manifest names; the `<commit>` in each path is
the example's placeholder.

## Measure Before a Change and After, and Keep It Only If the Number Moved

Where a program spends its time is rarely where it is guessed to, so a change
made for speed is measured twice: on the same benchmark, machine and build,
before and after. One change at a time, so each number says what moved it. A
change that moved nothing comes out again, since a form that looks faster and is
not only costs its reader.

```text
# Bad: a change for speed, and a claim with nothing behind it.
perf(tiles): sum a row's brightness faster
```

```text
perf(tiles): sum a row's brightness over eight lanes

`taskset -c 8 cargo bench -p tiles --bench brightness`, 4,096 values, on a
Graviton4: p50 2,958 ns before, 404 ns after; p99 2,960 ns before, 407 ns
after; an empty round 32 ns.
Results: crates/tiles/benches/results/2026-09-29T21-10Z-<commit>-brightness/
```

Held by review.

## Find Where the Time Goes with a Profiler, on the `profiling` Build

A profile says which functions and lines the time is spent in, which is where a
change can pay. `profiling` is `release` with full debug info, packed beside the
binary, and nothing stripped, so a profiler names each function and line of the
code that ships; a dev build's profile shows unoptimized code, whose hot spots
are not the release's. On Linux, `perf record --call-graph dwarf` and `perf
report` read it; samply or Instruments serve elsewhere; no profile pins one, so
use the one the machine has. The workspace's `.gitignore` keeps what they leave,
`perf.data`, a flame graph and `*.profraw`, out of commits.

```text
# Bad: a profile of the dev build, whose hot spots are not the release's.
cargo build -p tiles --bin paint
perf record ./target/debug/paint
```

```text
cargo build -p tiles --bin paint --profile profiling
perf record --call-graph dwarf ./target/profiling/paint
perf report
```

Held by review.

## A Benchmark Is a `harness = false` Target, Run by `cargo bench`

A benchmark is a file in the crate's `benches/`, declared as a `[[bench]]` with
`harness = false`, whose own `main` warms up, times and reports. `cargo bench`
builds it under the `bench` profile, which is `release` with fat LTO and one
codegen unit, so it measures the code that ships, and runs it with `--bench`
after any arguments given past `--`. A timing inside a `#[test]` measures the
`test` profile, at `opt-level = 0`, and runs beside every other test; Rust's own
`#[bench]` needs nightly. Where the repository already has criterion or divan, a
benchmark uses it; otherwise the file is its own harness, as below. clippy's
`--all-targets` reads a benchmark like any code.

```rust
// Bad: a timing at `opt-level = 0`, beside every other test.
#[cfg(test)]
mod tests {
    use core::time::Duration;
    use std::time::Instant;

    #[test]
    fn painting_a_row_is_fast() {
        let mut row = vec![0_u32; 4_096];
        let start = Instant::now();
        row.fill(7);
        assert!(start.elapsed() < Duration::from_micros(10), "a row paints in 10 us");
        assert_eq!(row.first(), Some(&7), "with its tile");
    }
}
```

```toml
# crates/tiles/Cargo.toml
[[bench]]
name    = "brightness"
harness = false
```

```rust
//! What a row's brightness costs, summed in order and over eight lanes, per call.

use core::error::Error;
use core::hint::black_box;
use core::time::Duration;
use std::io::{self, Write};
use std::time::Instant;

type BoxError = Box<dyn Error + Send + Sync>;

const WARM_UP: usize = 1_000;
const ROUNDS: usize = 100_000;

#[inline(never)]
fn in_order(row: &[f32]) -> f32 {
    row.iter().sum()
}

#[inline(never)]
fn over_lanes(row: &[f32]) -> f32 {
    let (chunks, rest) = row.as_chunks::<8>();
    let mut lanes = [0.0_f32; 8];
    for chunk in chunks {
        for (lane, value) in lanes.iter_mut().zip(chunk) {
            *lane += value;
        }
    }
    lanes.iter().sum::<f32>() + rest.iter().sum::<f32>()
}

fn nearest_rank(took: &[Duration], per_mille: usize) -> Duration {
    let rank = took.len().saturating_mul(per_mille) / 1_000;
    took.get(rank.min(took.len().saturating_sub(1))).copied().unwrap_or_default()
}

fn time<F: FnMut()>(name: &str, mut op: F) -> Result<(), BoxError> {
    let mut took = Vec::with_capacity(ROUNDS);
    for round in 0..WARM_UP.saturating_add(ROUNDS) {
        let start = Instant::now();
        op();
        let elapsed = start.elapsed();
        if round >= WARM_UP {
            took.push(elapsed);
        }
    }
    took.sort_unstable();
    let (p50, p99) = (nearest_rank(&took, 500), nearest_rank(&took, 990));
    let max = took.last().copied().unwrap_or_default();
    writeln!(io::stdout().lock(), "{name}: p50 {p50:?}, p99 {p99:?}, max {max:?}")?;
    Ok(())
}

fn main() -> Result<(), BoxError> {
    let row: Vec<f32> = (0..4_096_u16).map(|at| f32::from(at) * 0.5).collect();
    time("an empty round", || {})?;
    time("in order, 4,096 values", || {
        black_box(in_order(black_box(&row)));
    })?;
    time("over eight lanes, 4,096 values", || {
        black_box(over_lanes(black_box(&row)));
    })?;
    Ok(())
}
```

Held by review. No recipe runs a benchmark: `cargo bench -p tiles --bench
brightness` runs one by hand.
{%- if "strict" in lints %}

Under `strict`, a benchmark is no test to clippy, so the allowances for tests do
not reach it: it writes its report through `io::Write`, since `print_stdout`
refuses `println!`, and returns its failures from `main`, since `unwrap_used`
refuses an `unwrap`.
{%- endif %}

## Pass What Is Measured Through `black_box`, Its Input and Its Result

The optimizer deletes work whose result nobody reads, and computes ahead of time
what depends only on constants, so a benchmark that drops its result, or feeds a
constant, can time nothing at all. `core::hint::black_box` hides a value from
the optimizer: around the input, so the work cannot be folded, and around the
result, so it cannot be dropped. `#[inline(never)]` does not do this: a call to
a function with no side effects is still removed when its result is unused. A
`#[must_use]` on a pure function flags a dropped result; it does not stop the
folding.

```rust
use core::time::Duration;
use std::time::Instant;

#[inline(never)]
fn weigh(row: &[u32]) -> u32 {
    row.iter().fold(0, |acc, tile| acc.rotate_left(3) ^ tile.wrapping_mul(0x9e37_79b9))
}

#[must_use]
pub fn time_weigh(row: &[u32]) -> Duration {
    let start = Instant::now();
    // Bad: the result is unused, so the call is removed and nothing is timed.
    weigh(row);
    start.elapsed()
}
```

```rust
use core::hint::black_box;
use core::time::Duration;
use std::time::Instant;

#[inline(never)]
fn weigh(row: &[u32]) -> u32 {
    row.iter().fold(0, |acc, tile| acc.rotate_left(3) ^ tile.wrapping_mul(0x9e37_79b9))
}

#[must_use]
pub fn time_weigh(row: &[u32]) -> Duration {
    let start = Instant::now();
    black_box(weigh(black_box(row)));
    start.elapsed()
}
```

Held by review.

## Warm Up, Repeat, and Report the Distribution, on a Quiet, Pinned Core

The first rounds pay for what later ones do not: cold caches, pages touched for
the first time, a core's clock rising. So a benchmark discards a warm-up, times
many rounds, and reports their distribution, the median, the 99th percentile and
the maximum, since a mean hides the tail a latency is judged by; it reports the
cost of an empty round beside them, the harness's own floor. It runs on one
core, pinned with `taskset -c`, on a machine doing nothing else, so a migration
or a neighbour does not move the number. Where the machine isolates cores
(`/sys/devices/system/cpu/isolated`), a benchmark runs on them; the scheduler
spreads no thread across isolated cores, so a benchmark with several threads
pins each thread itself.

```text
# Bad: one run, on whatever core is free, reported as a mean.
cargo bench -p tiles --bench brightness
```

```text
taskset -c 8 cargo bench -p tiles --bench brightness
```

Held by review.

## Results Are Committed with What They Were Measured On

A number means nothing without its conditions, and a later change is judged
against the same ones. Each run a change rests on is committed in the crate's
`benches/results/<UTC time>-<commit>-<name>/`: the harness's transcript, and a
manifest of the machine, the kernel and its isolated cores, the toolchain, the
profile and the flags, what was run and the numbers that matter. The raw profile
of a run is never committed; its summary is.

```text
# Bad: the numbers in a pull request's comment, and nowhere else.
p50 went from 3 us to 0.4 us on my machine.
```

```toml
# crates/tiles/benches/results/2026-09-29T21-10Z-<commit>-brightness/manifest.toml
run-id  = "2026-09-29T21-10Z-<commit>-brightness"
purpose = "what a row's brightness costs, summed in order and over eight lanes"

[hardware]
cpu        = "AWS Graviton4 (Arm Neoverse V2)"
cores      = 32
cache-line = 64

[environment]
kernel        = "Linux 6.12.53-69.119.amzn2023.aarch64"
isolated-cpus = "6-31"
placement     = "taskset -c 8"

[toolchain]
rustc   = "1.101.0-nightly (d080e7dff 2026-09-27)"
profile = "bench: release, fat LTO, one codegen unit"
flags   = "the workspace's floor, +crc"

[parameters]
values  = 4_096
rounds  = 100_000
warm-up = 1_000

[results.ns]
empty-round = { p50 = 32, p99 = 34, max = 39 }
in-order    = { p50 = 2_958, p99 = 2_960, max = 10_957 }
over-lanes  = { p50 = 404, p99 = 407, max = 5_240 }
```

Held by review.

## A Doc That Claims a Speed Cites Its Number and Its Run

"Fast" in a doc is a promise nobody can check. A doc that says one form is
faster than another says by how much, on what input, and where the run is
committed, so a reader can run it again, and a later change can see when the
claim stopped holding.

```rust
/// A row's brightness, summed over eight lanes.
///
// Bad: a claim of speed that nobody can check.
/// Much faster than an ordered sum.
#[must_use]
pub fn brightness(row: &[f32]) -> f32 {
    let (chunks, rest) = row.as_chunks::<8>();
    let mut lanes = [0.0_f32; 8];
    for chunk in chunks {
        for (lane, value) in lanes.iter_mut().zip(chunk) {
            *lane += value;
        }
    }
    lanes.iter().sum::<f32>() + rest.iter().sum::<f32>()
}
```

```rust
/// A row's brightness, summed over eight lanes.
///
/// Seven times as fast as an ordered sum over 4,096 values on a Graviton4, p50
/// 404 ns against 2,958 ns, measured under
/// `benches/results/2026-09-29T21-10Z-<commit>-brightness`; the sum may differ
/// from an ordered one in its last bits.
#[must_use]
pub fn brightness(row: &[f32]) -> f32 {
    let (chunks, rest) = row.as_chunks::<8>();
    let mut lanes = [0.0_f32; 8];
    for chunk in chunks {
        for (lane, value) in lanes.iter_mut().zip(chunk) {
            *lane += value;
        }
    }
    lanes.iter().sum::<f32>() + rest.iter().sum::<f32>()
}
```

Held by review.

## A Claim About Generated Code Is Read in the Binary That Ships

A benchmark says how fast code is, not why: whether a call was inlined, a bounds
check removed or a loop vectorized is read in the machine code of the binary
that ships. Under fat LTO, as `release` and `bench` build, Cargo compiles a
library with `-C linker-plugin-lto`, as bitcode the binary's LTO optimizes
again, and much of the inlining and vectorizing happens there, so `--emit asm`
on the library shows the code before it: a loop that ships vectorized reads as
scalar. So the binary is read: `cargo bench --no-run` prints each benchmark
binary's path, and on Linux `objdump -d -C --disassemble='tiles::brightness'
<path>` shows one function as it ships; a function inlined into every caller has
no symbol of its own, so the one read is `#[inline(never)]`, as a benchmark's
are, or is read in its caller. With `--config 'profile.release.lto="off"'`,
`--emit asm` shows a crate's own code optimized without LTO, which is close to
what ships and is not it. A call is a `call` or `bl`; a bounds check, a branch
to `panic_bounds_check`; a vectorized loop, packed instructions, `paddd` or
`addps` on x86-64 and `add v0.4s` or `fadd v0.4s` on Arm, where a scalar float
addition is `addss`, in an `xmm` register all the same, or `fadd s0`.

```text
# Bad: the library's code before LTO, where the loop that ships vectorized reads as scalar.
cargo rustc -p tiles --release --lib -- --emit asm=target/tiles.s
```

```text
cargo bench -p tiles --bench brightness --no-run
objdump -d -C --disassemble='tiles::brightness' <the benchmark's path>
```

Held by review.
