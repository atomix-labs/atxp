{%- set lints = devset.layers | selectattr("profile", "equalto", "rust-lints") | map(attribute="features") | first | default([]) -%}
# Threads

Read this before a counter or a flag that several threads write, before a thread
that waits for another by spinning, before a busy poll, a pinned or isolated
core, a clock read in a hot loop, and memory a hot thread touches for the first
time. Threads cost each other through what they share, down to the cache line,
and a hot thread costs its machine a core; this is what each costs, and how it
is paid once instead of on every turn.
{%- if "agents" in lints %}

Which ordering an atomic needs, and the `// ORDERING:` each operation carries,
are `writing-unsafe-rust`'s.
{%- endif %}

## Values Written by Different Threads Live on Different Cache Lines

A core writes a whole cache line, never a word of it: two values that different
threads write, side by side on one line, move that line between the two cores on
every write, though neither thread reads the other's value. That is false
sharing, and it runs both threads at the speed of the line crossing between
them. A line is 64 bytes on x86-64 and on Arm's server cores, so a value written
by one thread and read or written by others sits on a line of its own:
`#[repr(align(64))]` on a wrapper, asserted. crossbeam's `CachePadded` aligns to
128 bytes on x86-64 and aarch64, since Intel's cores fetch lines in pairs, and
serves where the repository has crossbeam. Measure it: the cost depends on the
machine and on how often each thread writes.

```rust
use core::sync::atomic::AtomicU64;
use core::sync::atomic::Ordering::Relaxed;

#[derive(Debug, Default)]
pub struct Tally {
    // Bad: one line for both, so each painter's write takes it from the eraser.
    painted: AtomicU64,
    erased: AtomicU64,
}

impl Tally {
    pub fn paint(&self) {
        // ORDERING: Relaxed, a statistic that publishes only itself.
        self.painted.fetch_add(1, Relaxed);
    }

    pub fn erase(&self) {
        // ORDERING: Relaxed, a statistic that publishes only itself.
        self.erased.fetch_add(1, Relaxed);
    }
}
```

```rust
use core::sync::atomic::AtomicU64;
use core::sync::atomic::Ordering::Relaxed;

#[derive(Debug, Default)]
#[repr(align(64))]
pub struct Line<T>(T);

#[derive(Debug, Default)]
pub struct Tally {
    painted: Line<AtomicU64>,
    erased: Line<AtomicU64>,
}

// Each count is written by its own thread, so each has a cache line to itself.
const _: () = assert!(size_of::<Tally>() == 128, "two counts, a line each");

impl Tally {
    pub fn paint(&self) {
        // ORDERING: Relaxed, a statistic that publishes only itself.
        self.painted.0.fetch_add(1, Relaxed);
    }

    pub fn erase(&self) {
        // ORDERING: Relaxed, a statistic that publishes only itself.
        self.erased.0.fetch_add(1, Relaxed);
    }
}
```

Held by review, and by the size assertion.

## Each Thread Adds Its Count Once

Threads that all write one atomic take turns at its line, whatever they write to
it, so a count bumped once for each tile by every worker runs no faster than one
worker. Each worker counts in a value of its own, and adds it to the shared
count once, when it is done; a count read while the work goes on is split into
one part a thread, each on its own line, and summed when read.

```rust
use core::sync::atomic::AtomicU64;
use core::sync::atomic::Ordering::Relaxed;
use std::thread;

#[must_use]
pub fn lit(rows: &[Vec<u8>]) -> u64 {
    let lit = AtomicU64::new(0);
    thread::scope(|scope| {
        for row in rows {
            let lit = &lit;
            scope.spawn(move || {
                for tile in row {
                    if *tile > 0 {
                        // Bad: every worker takes the one line for every tile.
                        // ORDERING: Relaxed throughout, a count read once the scope has joined.
                        lit.fetch_add(1, Relaxed);
                    }
                }
            });
        }
    });
    lit.into_inner()
}
```

```rust
use core::sync::atomic::AtomicU64;
use core::sync::atomic::Ordering::Relaxed;
use std::thread;

#[must_use]
pub fn lit(rows: &[Vec<u8>]) -> u64 {
    let lit = AtomicU64::new(0);
    thread::scope(|scope| {
        for row in rows {
            let lit = &lit;
            scope.spawn(move || {
                let mine = row.iter().filter(|tile| **tile > 0).count();
                // ORDERING: Relaxed throughout, a count read once the scope has joined.
                lit.fetch_add(u64::try_from(mine).unwrap_or(u64::MAX), Relaxed);
            });
        }
    });
    lit.into_inner()
}
```

Held by review.

## A Spin Waits a Bounded While, with `spin_loop`, Then Yields

A thread waiting for another either spins, reading until the value changes, or
blocks, and the operating system wakes it later. Waking takes far longer than a
spin that ends soon, so a wait expected to be that short spins; one that may be
long blocks, on a channel, a lock or `thread::park`, since a spinning thread
burns its core, and on a core it shares, delays the very thread it waits for. So
a spin calls `core::hint::spin_loop()` on every turn, which tells the core it is
waiting, `pause` on x86-64 and `isb` on Arm, and after a bounded number of turns
it yields the core, or blocks.

```rust
use core::sync::atomic::AtomicBool;
use core::sync::atomic::Ordering::Acquire;

pub fn wait_for(ready: &AtomicBool) {
    // Bad: an unbounded spin, with no hint to the core that it waits.
    // ORDERING: Acquire, pairing with the Release store that sets `ready`.
    while !ready.load(Acquire) {}
}
```

```rust
use core::hint::spin_loop;
use core::sync::atomic::AtomicBool;
use core::sync::atomic::Ordering::Acquire;
use std::thread;

const SPINS: u32 = 1_000;

pub fn wait_for(ready: &AtomicBool) {
    let mut spins = 0_u32;
    // ORDERING: Acquire, pairing with the Release store that sets `ready`.
    while !ready.load(Acquire) {
        if spins < SPINS {
            spins = spins.saturating_add(1);
            spin_loop();
        } else {
            thread::yield_now();
        }
    }
}
```

Held by review.

## A Busy Poll Runs Only on a Core of Its Own

A loop that polls for input with no wait, `epoll_wait` with a zero timeout or a
`try_recv` in a loop, answers the moment input lands, and uses all of its core
to do it, whether or not anything comes. So it runs only where it has a core to
itself, pinned there, on a machine that isolates that core from other work;
anywhere else, it waits in the kernel and pays the wake-up.

```text
# Bad: a zero-timeout poll on a core the scheduler shares with the rest.
poll(timeout = 0) in a loop, on any core
```

```text
# The hot thread, pinned to isolated core 6, polls with no wait; every other thread blocks.
pin(6); loop { poll(timeout = 0); drive(ready) }
```

Held by review.

## A Hot Thread Is Pinned, and Each Thread Pins Itself

A thread the scheduler moves loses its caches, and one that shares a core waits
its turn, so a thread that must answer fast is pinned to a core of its own. On
Linux, `taskset -c` pins a whole process, and `sched_setaffinity`, through the
crate the repository uses for it, pins one thread. The scheduler spreads no
thread across isolated cores: two threads of a process given two isolated cores
both run on the first, so each thread pins itself to its own.

```text
# Bad: two isolated cores for two hot threads, which then share the first.
taskset -c 6,7 ./paint
```

```text
# Each thread pins itself: the painter to 6, the uploader to 7.
./paint --painter-core 6 --uploader-core 7
```

Held by review.

## A Hot Loop Reads the Clock Once a Turn

A clock read is a call into the platform's timekeeping, cheap but not free, and
two reads in one turn disagree. So a loop reads the clock once a turn, at its
top, and passes that instant to everything the turn decides, as a reactor hands
out the time it woke: each decision sees the same now, and the loop pays for one
read. Measure what a read costs on the machine.

```rust
use std::time::Instant;

#[derive(Debug)]
pub struct Stamp {
    pub tile: u32,
    pub at: Instant,
}

pub fn stamp(tiles: &[u32], out: &mut Vec<Stamp>) {
    for tile in tiles {
        // Bad: a clock read for each tile, and each tile a different now.
        out.push(Stamp { tile: *tile, at: Instant::now() });
    }
}
```

```rust
use std::time::Instant;

#[derive(Debug)]
pub struct Stamp {
    pub tile: u32,
    pub at: Instant,
}

pub fn stamp(tiles: &[u32], now: Instant, out: &mut Vec<Stamp>) {
    out.extend(tiles.iter().map(|tile| Stamp { tile: *tile, at: now }));
}
```

Held by review.

## A Hot Thread's Memory Is Written Before Its Loop Starts

The operating system maps a large fresh allocation lazily: the first write to
each page traps into the kernel, which finds a page and maps it, so a hot path
that touches new memory pays for the page as well as the write. A hot thread's
buffers are allocated and written once before its loop starts, locked where the
kernel could otherwise take them back, and a large table read at random sits on
huge pages, since each 4 KiB page costs an entry in the translation cache and a
2 MiB page covers 512 of them. Measure the first touch against the second.

```text
# Bad: the ring allocated at startup, and first written by the hot loop.
ring = allocate(64 MiB); loop { ring.write(next) }
```

```text
# Each page of the ring written once, and the ring locked, before the loop.
ring = allocate(64 MiB); ring.write_each_page(0); lock(ring); loop { ring.write(next) }
```

Held by review, and by a benchmark that measures the first turn.
