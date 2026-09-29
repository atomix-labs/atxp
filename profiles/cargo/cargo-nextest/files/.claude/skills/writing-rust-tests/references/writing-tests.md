{%- set lints = devset.layers | selectattr("profile", "equalto", "rust-lints") | map(attribute="features") | first | default([]) -%}
{%- set toolchain = devset.layers | selectattr("profile", "equalto", "rust-toolchain") | map(attribute="features") | first | default([]) -%}
# Writing Tests

Read this before writing or changing a test: its name, its assertions and their
messages, what it provokes, how it fails, what it shares with the tests beside
it, and what it stands in for. A test is read twice: when it is written, and
when it fails in someone else's run, where its name and its messages are all
that reader has.

## A Test's Name Is the Property It Pins

A failing run prints the test's name first, and often alone, so the name says
what should hold, as a sentence in snake case, its subject first:
`a_step_past_the_last_column_is_refused`. A test pins one property, with as many
assertions as that property needs, so its name can state it; a second property
is a second test. A name that says only what is called, `test_step`, `it_works`
or `step_right_2`, tells the reader nothing the stack trace does not.

```rust
#[must_use]
pub fn step_right(col: u16, cols: u16) -> Option<u16> {
    col.checked_add(1).filter(|&next| next < cols)
}

#[cfg(test)]
mod tests {
    use super::step_right;

    // Bad: names that say what is called, and one test for two properties.
    #[test]
    fn test_step_right() {
        assert_eq!(step_right(3, 8), Some(4), "one column right");
        assert_eq!(step_right(7, 8), None, "none past the last");
    }
}
```

```rust
#[must_use]
pub fn step_right(col: u16, cols: u16) -> Option<u16> {
    col.checked_add(1).filter(|&next| next < cols)
}

#[cfg(test)]
mod tests {
    use super::step_right;

    #[test]
    fn a_step_right_moves_one_column() {
        assert_eq!(step_right(3, 8), Some(4), "one column right");
    }

    #[test]
    fn a_step_past_the_last_column_is_refused() {
        assert_eq!(step_right(7, 8), None, "from the last column");
        assert_eq!(step_right(u16::MAX, u16::MAX), None, "and from the largest");
    }
}
```

Held by review: `clippy::redundant_test_prefix`, which refuses `test_`, is a
restriction lint no check turns on.

## Compare Whole Values with `assert_eq!`

`assert_eq!` prints both sides when they differ, so a failure shows what arrived
beside what was wanted. `assert!(a == b)` prints neither, and `assert!(result
.is_err())` or `assert!(matches!(…))` say only that the shape was wrong. The
workspace's error types are `PartialEq` where their payload allows, so a test
compares the whole `Result`, the error and its fields included.
{%- if "rust-lints" in devset.profiles %}

```rust,compile_fail
// fails: clippy::manual_assert_eq
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Pos {
    pub col: u16,
    pub row: u16,
}

#[must_use]
pub fn step_right(at: Pos) -> Option<Pos> {
    at.col.checked_add(1).map(|col| Pos { col, ..at })
}

#[cfg(test)]
mod tests {
    use super::{Pos, step_right};

    #[test]
    fn a_step_right_moves_one_column() {
        // Bad: a failure says the comparison was false, and not what came back.
        assert!(step_right(Pos { col: 3, row: 4 }) == Some(Pos { col: 4, row: 4 }));
    }
}
```
{%- endif %}

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Pos {
    pub col: u16,
    pub row: u16,
}

#[must_use]
pub fn step_right(at: Pos) -> Option<Pos> {
    at.col.checked_add(1).map(|col| Pos { col, ..at })
}

#[cfg(test)]
mod tests {
    use super::{Pos, step_right};

    #[test]
    fn a_step_right_moves_one_column() {
        assert_eq!(step_right(Pos { col: 3, row: 4 }), Some(Pos { col: 4, row: 4 }), "one column");
    }
}
```

{% if "rust-lints" in devset.profiles -%}
Held by `clippy::manual_assert_eq`, which refuses `assert!(a == b)` with no
message; with one, and on `is_err` or `matches!`, by review.
{%- else -%}
Held by review.
{%- endif %}

## A Message Says the Property, Where the Expression Does Not

An assertion's message is what a failure prints beside the two values, so it
says what should have held: a lowercase fragment with no final period, the
property as a claim, `"the last column"`, never `"test failed"` or `"should be
equal"`, which say what any failure says. The messages of one test read as a
running sentence: `"to itself"`, `"and forwards"`, `"never backwards"`. An
assertion whose expression says it all, `assert_eq!(board.cols(), 8)`, may leave
the message out.

```rust
#[must_use]
pub const fn offset(from: u16, to: u16) -> Option<u16> {
    to.checked_sub(from)
}

#[cfg(test)]
mod tests {
    use super::offset;

    #[test]
    fn an_offset_is_only_measured_forwards() {
        // Bad: each message says what any failure says.
        assert_eq!(offset(4, 4), Some(0), "values should be equal");
        assert_eq!(offset(4, 6), Some(2), "wrong offset");
        assert_eq!(offset(4, 3), None, "test failed");
    }
}
```

```rust
#[must_use]
pub const fn offset(from: u16, to: u16) -> Option<u16> {
    to.checked_sub(from)
}

#[cfg(test)]
mod tests {
    use super::offset;

    #[test]
    fn an_offset_is_only_measured_forwards() {
        assert_eq!(offset(4, 4), Some(0), "to itself");
        assert_eq!(offset(4, 6), Some(2), "and forwards");
        assert_eq!(offset(4, 3), None, "never backwards");
    }
}
```

Held by review: no lint asks for a message in a test, since
`clippy::missing_assert_message` spares test code.

## An `expect` Says Why the Call Cannot Fail

A test may unwrap: what it calls must succeed, and a panic is its failure. It
writes `expect` rather than `unwrap`, with a message that says why the call
cannot fail here, `"3,4 lies on an 8 by 8 board"`, so a failure names the
assumption that broke. `"failed"`, `"should work"` or the call's own name say
nothing a reader does not see in the stack trace.

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Board {
    pub cols: u16,
    pub rows: u16,
}

impl Board {
    #[must_use]
    pub fn index(self, col: u16, row: u16) -> Option<usize> {
        if col >= self.cols || row >= self.rows {
            return None;
        }
        usize::from(row).checked_mul(usize::from(self.cols))?.checked_add(usize::from(col))
    }
}

#[cfg(test)]
mod tests {
    use super::Board;

    #[test]
    fn a_square_is_counted_row_by_row() {
        let board = Board { cols: 8, rows: 8 };
        // Bad: a failure says an `Option` was `None`, and not what was assumed.
        assert_eq!(board.index(3, 4).unwrap(), 35, "four rows of eight, then three");
        assert_eq!(board.index(0, 7).expect("failed"), 56, "the last row's first square");
    }
}
```

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Board {
    pub cols: u16,
    pub rows: u16,
}

impl Board {
    #[must_use]
    pub fn index(self, col: u16, row: u16) -> Option<usize> {
        if col >= self.cols || row >= self.rows {
            return None;
        }
        usize::from(row).checked_mul(usize::from(self.cols))?.checked_add(usize::from(col))
    }
}

#[cfg(test)]
mod tests {
    use super::Board;

    #[test]
    fn a_square_is_counted_row_by_row() {
        let board = Board { cols: 8, rows: 8 };
        let at = board.index(3, 4).expect("3,4 lies on an 8 by 8 board");
        assert_eq!(at, 35, "four rows of eight, then three");
    }
}
```

Held by review.
{%- if "rust-clippy" in devset.profiles %}

The workspace's `clippy.toml` lets code in a `#[test]` function or a
`#[cfg(test)]` module unwrap, expect, panic, index and print, which the lints
refuse elsewhere; a helper outside both carries its own `#[expect]` with a
reason.
{%- endif %}

## An Impossible Arm Panics with What Arrived

A test that must see one variant takes it with `let … else`, and the `else`
panics with a message naming what should have come and, where it helps, what
did: `panic!("a step off the board is blocked, not {moved:?}")`. A `match` whose
other arms cannot happen does the same. `unreachable!` says the arm is
impossible when a failing test is exactly the case where it is not.
{%- if "strict" in lints %}

```rust,compile_fail
// fails: clippy::unreachable
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Move {
    Step(u16),
    Blocked { at: u16 },
}

#[must_use]
pub const fn step(col: u16, cols: u16) -> Move {
    match col.checked_add(1) {
        Some(next) if next < cols => Move::Step(next),
        _ => Move::Blocked { at: col },
    }
}

#[cfg(test)]
mod tests {
    use super::{Move, step};

    #[test]
    fn a_step_off_the_board_names_where_it_stopped() {
        // Bad: a failing test is the case where this arm is reached.
        let Move::Blocked { at } = step(7, 8) else { unreachable!() };
        assert_eq!(at, 7, "the last column");
    }
}
```
{%- endif %}

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Move {
    Step(u16),
    Blocked { at: u16 },
}

#[must_use]
pub const fn step(col: u16, cols: u16) -> Move {
    match col.checked_add(1) {
        Some(next) if next < cols => Move::Step(next),
        _ => Move::Blocked { at: col },
    }
}

#[cfg(test)]
mod tests {
    use super::{Move, step};

    #[test]
    fn a_step_off_the_board_names_where_it_stopped() {
        let moved = step(7, 8);
        let Move::Blocked { at } = moved else {
            panic!("a step off the board is blocked, not {moved:?}");
        };
        assert_eq!(at, 7, "the last column");
    }
}
```

{% if "strict" in lints -%}
Held by `clippy::unreachable`, which refuses the macro in tests too, as
`clippy::todo` refuses `todo!`.
{%- else -%}
Held by review.
{%- endif %}

## Each Edge and Each Refusal Has a Test

A bug lives at an edge far more often than in the middle: the empty board, the
first square and the last, one past the end, the largest value the type holds,
zero. So a function's tests run each edge its inputs have, and each refusal it
can return has a test that provokes it and compares the whole error, whose
message is pinned too, since a caller reads it.

```rust
use thiserror::Error;

#[derive(Debug, Error, Clone, Copy, PartialEq, Eq)]
#[error("bounds error: column {col} is past a board of {cols} columns")]
pub struct BoundsError {
    pub col: u16,
    pub cols: u16,
}

pub const fn check(col: u16, cols: u16) -> Result<u16, BoundsError> {
    if col < cols { Ok(col) } else { Err(BoundsError { col, cols }) }
}

#[cfg(test)]
mod tests {
    use super::check;

    // Bad: the one case nobody doubted.
    #[test]
    fn a_column_on_the_board_is_checked() {
        assert_eq!(check(3, 8), Ok(3), "the fourth column");
    }
}
```

```rust
use thiserror::Error;

#[derive(Debug, Error, Clone, Copy, PartialEq, Eq)]
#[error("bounds error: column {col} is past a board of {cols} columns")]
pub struct BoundsError {
    pub col: u16,
    pub cols: u16,
}

pub const fn check(col: u16, cols: u16) -> Result<u16, BoundsError> {
    if col < cols { Ok(col) } else { Err(BoundsError { col, cols }) }
}

#[cfg(test)]
mod tests {
    use super::{BoundsError, check};

    #[test]
    fn the_first_and_last_columns_are_on_the_board() {
        assert_eq!(check(0, 8), Ok(0), "the first");
        assert_eq!(check(7, 8), Ok(7), "and the last");
    }

    #[test]
    fn a_column_past_the_last_is_refused() {
        assert_eq!(check(8, 8), Err(BoundsError { col: 8, cols: 8 }), "one past");
        assert_eq!(check(0, 0), Err(BoundsError { col: 0, cols: 0 }), "and any, on no board");
    }

    #[test]
    fn a_bounds_error_names_the_column_and_the_board() {
        let refused = BoundsError { col: 8, cols: 8 };
        assert_eq!(refused.to_string(), "bounds error: column 8 is past a board of 8 columns");
    }
}
```

Held by review.

## A Test Returns `()`

A test that returns `Result` and fails through `?` prints the error's `Debug`,
`Error: ParseTileError { held: '?' }`, and no line, so the reader cannot tell
which call failed; a panic from `expect` names its file and line, and its
message says what was assumed. A test returns `()`, and each call that must
succeed says so with an `expect`.

```rust
use thiserror::Error;

#[derive(Debug, Error, Clone, Copy, PartialEq, Eq)]
#[error("parse tile error: want `.` or `#`, not `{held}`")]
pub struct ParseTileError {
    pub held: char,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Tile {
    Blank,
    Wall,
}

impl TryFrom<char> for Tile {
    type Error = ParseTileError;

    fn try_from(held: char) -> Result<Self, Self::Error> {
        match held {
            '.' => Ok(Self::Blank),
            '#' => Ok(Self::Wall),
            _ => Err(ParseTileError { held }),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{ParseTileError, Tile};

    // Bad: a failure prints the error and no line, and nothing checks which tile came back.
    #[test]
    fn a_row_of_tiles_parses() -> Result<(), ParseTileError> {
        for held in ['.', '#', '.'] {
            let _tile = Tile::try_from(held)?;
        }
        Ok(())
    }
}
```

```rust
use thiserror::Error;

#[derive(Debug, Error, Clone, Copy, PartialEq, Eq)]
#[error("parse tile error: want `.` or `#`, not `{held}`")]
pub struct ParseTileError {
    pub held: char,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Tile {
    Blank,
    Wall,
}

impl TryFrom<char> for Tile {
    type Error = ParseTileError;

    fn try_from(held: char) -> Result<Self, Self::Error> {
        match held {
            '.' => Ok(Self::Blank),
            '#' => Ok(Self::Wall),
            _ => Err(ParseTileError { held }),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::Tile;

    #[test]
    fn each_tile_parses_from_its_own_character() {
        assert_eq!(Tile::try_from('.'), Ok(Tile::Blank), "a dot is blank");
        assert_eq!(Tile::try_from('#'), Ok(Tile::Wall), "and a hash a wall");
    }
}
```

{% if "strict" in lints -%}
Held by review, and by `clippy::panic_in_result_fn`, which refuses an assertion
in a test that returns `Result`.
{%- else -%}
Held by review.
{%- endif %}

## `#[should_panic]` Names Its Message, on a Test That Returns `()`

A test that pins a panic says which one: `#[should_panic(expected = "…")]`,
whose text the panic's message must contain. A bare `#[should_panic]` passes on
any panic at all, an index out of bounds in the test's own setup included. The
panic is the test's result, so it returns `()`: on a test that returns `Result`,
`#[should_panic]` does not compile. A refusal a caller can cause is an error,
not a panic, and its test compares the `Err`.

```text
// Bad: rustc refuses it: "functions using `#[should_panic]` must return `()`".
#[test]
#[should_panic(expected = "a board has at least one column")]
fn a_board_of_no_columns_panics() -> Result<(), ParseTileError> {
    let _board = Board::new(0);
    Ok(())
}
```
{%- if "rust-lints" in devset.profiles %}

```rust,compile_fail
// fails: clippy::should_panic_without_expect
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Board {
    cols: u16,
}

impl Board {
    #[must_use]
    #[track_caller]
    pub const fn new(cols: u16) -> Self {
        assert!(cols > 0, "a board has at least one column");
        Self { cols }
    }

    #[must_use]
    pub const fn cols(self) -> u16 {
        self.cols
    }
}

#[cfg(test)]
mod tests {
    use super::Board;

    // Bad: passes on any panic, a typo in the test included.
    #[test]
    #[should_panic]
    fn a_board_of_no_columns_panics() {
        let _board = Board::new(0);
    }
}
```
{%- endif %}

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Board {
    cols: u16,
}

impl Board {
    #[must_use]
    #[track_caller]
    pub const fn new(cols: u16) -> Self {
        assert!(cols > 0, "a board has at least one column");
        Self { cols }
    }

    #[must_use]
    pub const fn cols(self) -> u16 {
        self.cols
    }
}

#[cfg(test)]
mod tests {
    use super::Board;

    #[test]
    #[should_panic(expected = "a board has at least one column")]
    fn a_board_of_no_columns_panics() {
        let _board = Board::new(0);
    }
}
```

{% if "rust-lints" in devset.profiles -%}
Held by `clippy::should_panic_without_expect`, and by rustc for a `Result`.
{%- else -%}
Held by rustc for a `Result`, and by review.
{%- endif %}

## `#[ignore]` Says What the Test Needs

A test that cannot run everywhere, one that needs a hugepage mount, a device or
a server, is ignored with the reason, `#[ignore = "needs a tile server on
localhost:7070"]`, which `cargo test` prints beside it, so whoever skips it
knows what would run it. A slow test is made fast, not ignored. `cargo nextest
run --run-ignored only` runs the ignored tests where what they need is there, as
`running.md` says.
{%- if "rust-lints" in devset.profiles %}

```rust,compile_fail
// fails: clippy::ignore_without_reason
#[cfg(test)]
mod tests {
    // Bad: skipped, and nothing says what would run it.
    #[test]
    #[ignore]
    fn a_tile_server_serves_a_board() {}
}
```
{%- endif %}

```rust
#[cfg(test)]
mod tests {
    #[test]
    #[ignore = "needs a tile server on localhost:7070"]
    fn a_tile_server_serves_a_board() {}
}
```

{% if "rust-lints" in devset.profiles -%}
Held by `clippy::ignore_without_reason`.
{%- else -%}
Held by review.
{%- endif %}

## A Test Stands Alone

nextest runs each test in a process of its own, so a test that leaves a global
behind, a `static`, an environment variable, the working directory, a process
lock, passes there whatever it left. `cargo test` runs a binary's tests as
threads of one process, in no fixed order, and so does a loom model's run: there
the next test finds what the last one left. A test builds what it reads, and
passes alone, in any order, and beside every other.

```rust
use core::sync::atomic::{AtomicU32, Ordering};

// Bad: one count for the whole process, which every test adds to.
static PAINTED: AtomicU32 = AtomicU32::new(0);

pub fn paint(squares: &mut [u8], tile: u8) {
    squares.fill(tile);
    // ORDERING: Relaxed; a statistic that publishes only itself.
    PAINTED.fetch_add(1, Ordering::Relaxed);
}

#[must_use]
pub fn painted() -> u32 {
    // ORDERING: Relaxed; a statistic that publishes only itself.
    PAINTED.load(Ordering::Relaxed)
}

#[cfg(test)]
mod tests {
    use super::{paint, painted};

    // Passes under nextest, and fails under `cargo test` whenever the other test runs first.
    #[test]
    fn a_paint_is_counted() {
        paint(&mut [0; 4], 7);
        assert_eq!(painted(), 1, "one paint");
    }

    #[test]
    fn a_paint_of_no_squares_is_counted_too() {
        paint(&mut [], 7);
        assert_eq!(painted(), 1, "one paint, of nothing");
    }
}
```

```rust
#[derive(Debug, Default)]
pub struct Canvas {
    painted: u32,
}

impl Canvas {
    pub fn paint(&mut self, squares: &mut [u8], tile: u8) {
        squares.fill(tile);
        self.painted = self.painted.saturating_add(1);
    }

    #[must_use]
    pub const fn painted(&self) -> u32 {
        self.painted
    }
}

#[cfg(test)]
mod tests {
    use super::Canvas;

    #[test]
    fn a_paint_is_counted() {
        let mut canvas = Canvas::default();
        canvas.paint(&mut [0; 4], 7);
        assert_eq!(canvas.painted(), 1, "one paint");
    }

    #[test]
    fn a_paint_of_no_squares_is_counted_too() {
        let mut canvas = Canvas::default();
        canvas.paint(&mut [], 7);
        assert_eq!(canvas.painted(), 1, "one paint, of nothing");
    }
}
```

Held by review. Where a process-wide value must be set, a logger or an owner's
identity, every test sets the same one, so whichever runs first does the work
and the rest find it done.

## A Test Waits for a Condition, with a Deadline

A test that sleeps a fixed time for a thread to get somewhere fails on a loaded
machine, and wastes the time on an idle one. It waits for the thing itself, a
message on a channel, a join, a flag it polls, with a deadline long enough that
only a hang reaches it, so a slow run is slow, not red, and a lost wakeup fails
with a message instead of hanging the run.

```rust
use std::sync::mpsc::Sender;
use std::thread;

pub fn paint_later(tile: u8, painted: Sender<u8>) {
    thread::spawn(move || {
        let _sent = painted.send(tile);
    });
}

#[cfg(test)]
mod tests {
    use core::time::Duration;
    use std::sync::mpsc;
    use std::thread;

    use super::paint_later;

    #[test]
    fn a_painter_reports_its_tile() {
        let (painted, reports) = mpsc::channel();
        paint_later(7, painted);
        // Bad: fails whenever the painter takes longer than this, and waits this long when not.
        thread::sleep(Duration::from_millis(50));
        assert_eq!(reports.try_recv(), Ok(7), "the painter's tile");
    }
}
```

```rust
use std::sync::mpsc::Sender;
use std::thread;

pub fn paint_later(tile: u8, painted: Sender<u8>) {
    thread::spawn(move || {
        let _sent = painted.send(tile);
    });
}

#[cfg(test)]
mod tests {
    use core::time::Duration;
    use std::sync::mpsc;

    use super::paint_later;

    #[test]
    fn a_painter_reports_its_tile() {
        let (painted, reports) = mpsc::channel();
        paint_later(7, painted);
        let tile = reports.recv_timeout(Duration::from_secs(10));
        assert_eq!(tile, Ok(7), "the painter's tile, well within ten seconds");
    }
}
```

Held by review. A loop that polls sleeps a millisecond or so between tries and
asserts against a deadline, `Instant::now() < deadline`, on each.

## A Fixture Gives Back What It Made

A test that writes files, binds a port or makes a shared-memory segment runs
beside others that do the same, and may panic before its last line. So it makes
each in a fresh place of its own, a directory from `tempfile`, never a fixed
path, and holds it in a value whose `Drop` removes it, so it is gone however the
test ends.

```text
// Bad: a fixed path every run shares, removed only if nothing above panics.
#[test]
fn a_board_file_reads_back() {
    fs::write("/tmp/tiles-test/board.txt", "8x8").expect("the directory exists");
    assert_eq!(read_board("/tmp/tiles-test/board.txt"), Ok(Board { cols: 8, rows: 8 }));
    fs::remove_file("/tmp/tiles-test/board.txt").expect("the file was written");
}
```

```text
#[test]
fn a_board_file_reads_back() {
    let scratch = TempDir::new().expect("a scratch directory");
    let path = scratch.path().join("board.txt");
    fs::write(&path, "8x8").expect("a fresh directory takes a file");
    assert_eq!(read_board(&path), Ok(Board { cols: 8, rows: 8 }), "the board it wrote");
}
```

Held by review. A fixture several tests use is a type in `testing.rs` that holds
the `TempDir`, so each test gets a fresh one.

## A Double Is a Fake of a Trait the Code Already Takes

Code that reaches outside the process, a store, a clock, a dealer of tiles,
takes it as a trait, and a test hands it a fake: a small type in the tests that
implements the trait over a plain value the test sets, and reads back what the
code did to it. A fake behaves; a mock framework's expectations restate the
implementation, and break when it changes without a bug.

```text
// Bad: mockall, and a chain whose last `returning` wins, so the dealer deals 3, 3, 3.
let mut dealer = MockDealer::new();
dealer.expect_deal().times(3).returning(|| Some(1)).returning(|| Some(2)).returning(|| Some(3));
```

```rust
pub trait Dealer {
    fn deal(&mut self) -> Option<u8>;
}

pub fn deal_row<D: Dealer>(dealer: &mut D, row: &mut [u8]) -> usize {
    row.iter_mut()
        .map_while(|square| {
            *square = dealer.deal()?;
            Some(())
        })
        .count()
}

#[cfg(test)]
mod tests {
    use super::{Dealer, deal_row};

    struct Deck<I>(I);

    impl<I: Iterator<Item = u8>> Dealer for Deck<I> {
        fn deal(&mut self) -> Option<u8> {
            self.0.next()
        }
    }

    #[test]
    fn a_short_deck_fills_the_row_as_far_as_it_goes() {
        let mut row = [0; 4];
        assert_eq!(deal_row(&mut Deck([2, 3].into_iter()), &mut row), 2, "two tiles dealt");
        assert_eq!(row, [2, 3, 0, 0], "and the rest left blank");
    }
}
```

Held by review. Where a repository does use mockall, a value for each call is an
expectation for each, `.times(1).return_const(Some(1))`, in a `Sequence` where
their order matters.
