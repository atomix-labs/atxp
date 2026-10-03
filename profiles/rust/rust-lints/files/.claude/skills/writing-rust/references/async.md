# Async

Read this before writing or changing async Rust on tokio: an `async fn`, a
spawned task, a lock, a channel, a `select!`, a trait with async methods, an
async test, or a log line. Several rules here correct guides that are widely
copied, and say so.

## A `std` Lock's Guard Never Spans an `.await`

A task suspended at an `.await` keeps its thread's worker free but its guard
held, so every other task that wants the lock blocks its whole worker thread
until the first is polled again, and with few workers that is a deadlock. A
guard from `std::sync::Mutex` or `RwLock` is dropped before the next `.await`:
take what the work needs, release, then await.

```rust,compile_fail
// fails: clippy::await_holding_lock
use core::time::Duration;
use std::sync::{Mutex, PoisonError};

use tokio::time;

pub async fn place_later(squares: &Mutex<Vec<u8>>, tile: u8) {
    let mut guard = squares.lock().unwrap_or_else(PoisonError::into_inner);
    // Bad: the guard waits out the sleep, and every task that wants it waits too.
    time::sleep(Duration::from_millis(10)).await;
    guard.push(tile);
}
```

```rust
use core::time::Duration;
use std::sync::{Mutex, PoisonError};

use tokio::time;

pub async fn place_later(squares: &Mutex<Vec<u8>>, tile: u8) {
    time::sleep(Duration::from_millis(10)).await;
    squares.lock().unwrap_or_else(PoisonError::into_inner).push(tile);
}
```

Held by `clippy::await_holding_lock`, and `clippy::await_holding_refcell_ref`
for a `RefCell` borrow.

## A `tokio` Lock Is for a Guard That Must Span an `.await`

`tokio::sync::Mutex` exists so that a guard can be held across an `.await`: a
critical section that itself awaits, as a write that must not interleave with
another. Holding its guard over an `.await` is its purpose, not a fault, though
some guides forbid it. Where no `.await` sits inside the section, `std`'s lock
is cheaper and is the one to use; tokio's own documentation says the same.

```rust
use tokio::sync::Mutex;

#[derive(Debug, Default)]
pub struct Tally {
    // Bad: an async lock for a section that never awaits, paying for an
    // `.await` on every count.
    painted_count: Mutex<u32>,
}

impl Tally {
    pub async fn count(&self) {
        let mut count = self.painted_count.lock().await;
        *count = count.saturating_add(1);
    }
}
```

```rust
use std::io;

use tokio::fs::File;
use tokio::io::AsyncWriteExt;
use tokio::sync::Mutex;

/// Appends one move to the log file; the guard spans both writes, so two moves
/// never interleave.
pub async fn log_move(log: &Mutex<File>, line: &[u8]) -> io::Result<()> {
    let mut log = log.lock().await;
    log.write_all(line).await?;
    log.write_all(b"\n").await
}
```

Held by review.

## A Channel Is Bounded

An unbounded channel lets a producer that runs faster than its consumer grow the
queue until memory runs out. A bounded one makes `send().await` wait once the
queue is full, which slows the producer to the consumer's pace. Its bound is a
constant, named and documented, and a refused `send` hands the value back.

```rust
use tokio::sync::mpsc;

// Bad: a producer that gets ahead of the painter grows this queue without end.
#[must_use]
pub fn painter() -> (mpsc::UnboundedSender<u8>, mpsc::UnboundedReceiver<u8>) {
    mpsc::unbounded_channel()
}
```

```rust
use tokio::sync::mpsc;
use tokio::sync::mpsc::error::SendError;

/// Squares waiting to be painted: a producer that gets this far ahead waits.
const QUEUE_CAPACITY: usize = 64;

#[must_use]
pub fn painter() -> (mpsc::Sender<u8>, mpsc::Receiver<u8>) {
    mpsc::channel(QUEUE_CAPACITY)
}

pub async fn queue(tiles: &mpsc::Sender<u8>, tile: u8) -> Result<(), SendError<u8>> {
    tiles.send(tile).await
}
```

Held by review. Each channel has its use: `mpsc` for work to one consumer,
`oneshot` for a single reply, `watch` for the latest value of something that
changes, `broadcast` for every message to every subscriber.

## Blocking Work Leaves the Runtime's Threads

A worker thread runs every task scheduled on it, so a call that blocks, a file
read, a lock wait, a long computation, stalls all of them. A task yields at an
`.await` often: a rule of thumb from tokio's maintainers is within 10 to 100
microseconds. File access goes through `tokio::fs`, and computation or a
blocking library through `spawn_blocking`.

```rust
use std::path::Path;
use std::{fs, io};

use tokio::sync::mpsc;

pub async fn save(boards: &mut mpsc::Receiver<Vec<u8>>, path: &Path) -> io::Result<()> {
    while let Some(board) = boards.recv().await {
        // Bad: the write blocks every task on this worker until the disk answers.
        fs::write(path, board)?;
    }
    Ok(())
}
```

```rust
use std::io;
use std::path::Path;

use tokio::sync::mpsc;
use tokio::{fs, task};

fn render(board: &[u8]) -> Vec<u8> {
    board.iter().map(|&tile| if tile == 0 { b'.' } else { b'#' }).collect()
}

pub async fn save(boards: &mut mpsc::Receiver<Vec<u8>>, path: &Path) -> io::Result<()> {
    while let Some(board) = boards.recv().await {
        let drawing =
            task::spawn_blocking(move || render(&board)).await.map_err(io::Error::other)?;
        fs::write(path, drawing).await?;
    }
    Ok(())
}
```

Held by review: `clippy::unused_async` catches an `async fn` that never awaits,
not one that blocks between awaits.

## Spawned Tasks Live in a `JoinSet`

A dropped `JoinHandle` detaches its task, which runs on after its caller has
given up, and its panic is never seen. A `JoinSet` owns the tasks it spawns:
`join_next` hands back each result, a panic included, and dropping the set
aborts every task still in it, so no task outlives the work it was for. A task
spawned onto the runtime is `Send` and `'static`, so it owns what it uses: an
`Arc` cloned into it, or a value moved in. Borrowing from an `Arc` the task owns
across an `.await` is fine.

```rust
use tokio::task::{self, JoinHandle};

async fn paint(tile: u8) -> u8 {
    task::yield_now().await;
    tile
}

// Bad: a caller that drops these handles leaves every task running, and a
// panic in one is lost.
#[must_use]
pub fn paint_all(tiles: Vec<u8>) -> Vec<JoinHandle<u8>> {
    tiles.into_iter().map(|tile| task::spawn(paint(tile))).collect()
}
```

```rust
use tokio::task::{self, JoinError, JoinSet};

async fn paint(tile: u8) -> u8 {
    task::yield_now().await;
    tile
}

pub async fn paint_all(tiles: Vec<u8>) -> Result<Vec<u8>, JoinError> {
    let mut painting = JoinSet::new();
    for tile in tiles {
        painting.spawn(paint(tile));
    }
    let mut painted_tiles = Vec::with_capacity(painting.len());
    while let Some(painted_tile) = painting.join_next().await {
        painted_tiles.push(painted_tile?);
    }
    Ok(painted_tiles)
}
```

Held by review.

## Independent Futures Run Together, and `try_join!` Drops the Rest

Two awaits in a row run one after the other, though neither needs the other.
`join!` runs them together; `try_join!` does too, and returns at the first
error. The futures it has not finished are then dropped, cancelled where they
stood, not left running, as some guides claim. Work that must finish once
started, a write, is spawned, so dropping the future that waits for it does not
stop it.

```rust
use std::io;
use std::path::Path;

use tokio::fs;

pub async fn open_board(tiles: &Path, layout: &Path) -> io::Result<(Vec<u8>, Vec<u8>)> {
    // Bad: the layout is not read until the tiles are.
    let tiles = fs::read(tiles).await?;
    let layout = fs::read(layout).await?;
    Ok((tiles, layout))
}
```

```rust
use std::io;
use std::path::Path;

use tokio::{fs, try_join};

pub async fn open_board(tiles: &Path, layout: &Path) -> io::Result<(Vec<u8>, Vec<u8>)> {
    try_join!(fs::read(tiles), fs::read(layout))
}
```

Held by review.

## A Long-Lived Task Stops When Told

A loop that runs until its runtime drops it stops wherever it happens to be,
halfway through a save. It awaits a stop signal beside its work in `select!`,
and ends at a point it chose. A `watch` channel is the signal with tokio alone;
tokio-util's `CancellationToken` serves a tree of tasks, where cancelling a
token cancels each `child_token()` of it, and dropping one does not: a child
outlives a parent that is dropped without being cancelled, unless a `DropGuard`
cancels it on drop.

```rust
use core::time::Duration;

use tokio::time;

// Bad: nothing stops this loop but dropping it, wherever it is.
pub async fn autosave(saves: &mut u32) {
    let mut interval = time::interval(Duration::from_secs(5));
    loop {
        interval.tick().await;
        *saves = saves.saturating_add(1);
    }
}
```

```rust
use core::time::Duration;

use tokio::sync::watch;
use tokio::{select, time};

/// Saves every five seconds until `stop` changes, or its sender is gone.
pub async fn autosave(mut stop: watch::Receiver<bool>, saves: &mut u32) {
    let mut interval = time::interval(Duration::from_secs(5));
    loop {
        select! {
            _ = interval.tick() => *saves = saves.saturating_add(1),
            _ = stop.changed() => break,
        }
    }
}
```

Held by review.

## A `select!` Loop Ends When Its Channel Closes

A branch whose pattern does not match is disabled, and `else` runs only once
every branch is: with a stop signal that stays pending, it never does, and a
closed channel leaves the loop waiting on the signal alone. The loop matches
`recv()`'s `None` itself. Each branch is also cancel-safe: `select!` drops the
branches that lose, so a future that had read half a frame loses the half.
`recv` on a channel is cancel-safe, `read_exact` is not, and state that must
survive a lost branch lives outside the loop.

```rust
use tokio::select;
use tokio::sync::{mpsc, watch};

pub async fn paint(
    mut tiles: mpsc::Receiver<u8>, mut stop: watch::Receiver<bool>, painted_tiles: &mut Vec<u8>,
) {
    loop {
        select! {
            Some(tile) = tiles.recv() => painted_tiles.push(tile),
            _ = stop.changed() => break,
            // Bad: `stop` stays pending, so this never runs once `tiles` closes.
            else => break,
        }
    }
}
```

```rust
use tokio::select;
use tokio::sync::{mpsc, watch};

pub async fn paint(
    mut tiles: mpsc::Receiver<u8>, mut stop: watch::Receiver<bool>, painted_tiles: &mut Vec<u8>,
) {
    loop {
        select! {
            tile = tiles.recv() => match tile {
                Some(tile) => painted_tiles.push(tile),
                None => break,
            },
            _ = stop.changed() => break,
        }
    }
}
```

Held by review.

## A `#[tokio::test]` Runs on One Thread

`#[tokio::test]` builds a current-thread runtime, not a multi-thread one as some
guides say, so a spawned task runs only while the test awaits. A test awaits
what it waits for, through tokio's channels, and keeps its one thread; only a
test that needs two tasks truly at once asks for `#[tokio::test(flavor =
"multi_thread")]`.

```rust
#[cfg(test)]
mod tests {
    use std::sync::mpsc;

    use tokio::task;

    #[tokio::test]
    async fn a_painter_paints_while_the_test_waits() {
        let (tiles, painted_tiles) = mpsc::channel();
        task::spawn(async move {
            let _unsent_tile = tiles.send(7_u8);
        });
        // Bad: `recv` blocks the one thread, so the painter never runs.
        assert_eq!(painted_tiles.recv(), Ok(7), "the painter's tile");
    }
}
```

```rust
#[cfg(test)]
mod tests {
    use tokio::sync::oneshot;
    use tokio::task;

    #[tokio::test]
    async fn a_painter_paints_while_the_test_waits() {
        let (tiles, painted_tiles) = oneshot::channel();
        task::spawn(async move {
            let _unsent_tile = tiles.send(7_u8);
        });
        assert_eq!(painted_tiles.await, Ok(7), "the painter's tile");
    }
}
```

Held by review.

## A Public Trait's Async Method Says Its Future Is `Send`

`async fn` in a trait is native since Rust 1.75, so no `async-trait` crate and
no boxed future. In a public trait, though, it leaves a caller no way to require
that the future be `Send`, and a multi-thread runtime can spawn only one that
is. The trait declares `fn … -> impl Future<Output = …> + Send`; an
implementation may still write `async fn`.

```rust,compile_fail
// fails: async_fn_in_trait
pub trait Store {
    // Bad: no caller can require this future to be `Send`.
    async fn load(&self, name: &str) -> Vec<u8>;
}
```

```rust
use core::future::Future;

use tokio::sync::RwLock;

pub trait Store {
    fn load(&self, name: &str) -> impl Future<Output = Vec<u8>> + Send;
}

#[derive(Debug, Default)]
pub struct Memory {
    boards: RwLock<Vec<(String, Vec<u8>)>>,
}

impl Store for Memory {
    async fn load(&self, name: &str) -> Vec<u8> {
        let boards = self.boards.read().await;
        boards
            .iter()
            .find(|(board_name, _)| board_name == name)
            .map_or_else(Vec::new, |(_, board)| board.clone())
    }
}
```

Held by rustc's `async_fn_in_trait`.

## An Async Closure Is Bounded by `AsyncFn`

A function that takes an async closure bounds it by `AsyncFn`, `AsyncFnMut` or
`AsyncFnOnce`, stable since Rust 1.85, in one bound that reads like `Fn`. The
older pair, `F: Fn() -> Fut` and `Fut: Future`, is longer and refuses a closure
whose future borrows from the closure.

```rust
use core::future::Future;

// Bad: two parameters for one closure, and no future that borrows from it.
pub async fn retry<T, E, F, Fut>(attempts: u32, attempt: F) -> Result<T, E>
where
    F: Fn() -> Fut,
    Fut: Future<Output = Result<T, E>>,
{
    let mut attempts_left = attempts;
    loop {
        match attempt().await {
            Err(_failed_attempt) if attempts_left > 1 => {
                attempts_left = attempts_left.saturating_sub(1);
            },
            last_attempt => return last_attempt,
        }
    }
}
```

```rust
pub async fn retry<T, E, F>(attempts: u32, attempt: F) -> Result<T, E>
where
    F: AsyncFn() -> Result<T, E>,
{
    let mut attempts_left = attempts;
    loop {
        match attempt().await {
            Err(_failed_attempt) if attempts_left > 1 => {
                attempts_left = attempts_left.saturating_sub(1);
            },
            last_attempt => return last_attempt,
        }
    }
}
```

Held by review.

## A Log Line Is a `tracing` Event with Fields

A service, and async code generally, logs through `tracing`, whose events carry
fields a collector can filter on. The message is a stable lowercase phrase with
no final period, and every value is a field, never text in the message, so each
line of one kind reads alike and can be searched. An error is logged once, where
it is handled, dropped, retried or answered, as `error = %error`: code that
passes it on with `?` or `map_err` does not log it, or the one failure is logged
at every level it crosses. An `Err(_)` or an `is_err()` that logs nothing hides
the failure. A library emits events and never installs a subscriber, which is
the binary's. A secret, a token or a user's data is never a field. Code that
takes no logging crate reports through what it returns, and only a binary
prints, where an operator watches.

```rust
use std::path::Path;

use tokio::fs;
use tokio::sync::mpsc;
use tracing::info;

pub async fn autosave(mut boards: mpsc::Receiver<Vec<u8>>, path: &Path) {
    while let Some(board) = boards.recv().await {
        // Bad: the values are in the message, and a failed save goes unlogged.
        if fs::write(path, &board).await.is_ok() {
            info!("Saved {} squares to {}.", board.len(), path.display());
        }
    }
}
```

```rust
use std::path::Path;

use tokio::fs;
use tokio::sync::mpsc;
use tracing::{debug, warn};

/// Saves each board it is sent, until the senders are gone.
pub async fn autosave(mut boards: mpsc::Receiver<Vec<u8>>, path: &Path) {
    while let Some(board) = boards.recv().await {
        match fs::write(path, &board).await {
            Ok(()) => debug!(squares = board.len(), "board saved"),
            // Handled here: the next board tries again, so the error is logged
            // and dropped.
            Err(error) => warn!(error = %error, path = %path.display(), "board save failed"),
        }
    }
}
```

Held by review.
