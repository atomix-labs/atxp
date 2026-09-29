---
name: writing-rust-tests
description: Use when writing, changing or fixing Rust tests, whether a unit test, an integration test in `tests/`, a fixture or `testing.rs`, a trybuild compile-fail test, a proptest property, an rstest table, a cargo-fuzz target or a doctest; when a test fails, is flaky or hangs, or needs `#[ignore]` or `#[should_panic]`; when naming a test or writing its assertion and `expect` messages; when running tests with cargo-nextest, or choosing where a test goes. Covers test layout, names and messages, fixtures and doubles, compile-fail tests, property tests, tables, fuzzing, doctests, and how nextest runs them.
---

# Writing Rust Tests

How tests are written and run in this workspace: each where its reader looks for
it, named for the property it pins, failing with a message that says what broke;
standing alone, so nextest and `cargo test` agree; misuses the types refuse
pinned by fixtures that must not compile; invariants checked over every input,
and input from outside fuzzed. The rules below are the whole of it, each with
its reason. The references hold each rule's why, a bad and a good example, and
what holds the rule; each Rust example compiles under the workspace's lints.

The examples leave their docs out to stay short, and compile with the lints that
ask for docs off; real code writes them: a `//!` atop each file in `tests/`
saying what it proves, and a line on each fixture saying its role.
{%- set lints = devset.layers | selectattr("profile", "equalto", "rust-lints") | map(attribute="features") | first | default([]) %}
{%- set toolchain = devset.layers | selectattr("profile", "equalto", "rust-toolchain") | map(attribute="features") | first | default([]) %}
{%- set rustdoc = devset.layers | selectattr("profile", "equalto", "rust-doc") | map(attribute="features") | first | default([]) %}
{%- if "strict" in lints %}

Under `strict`, `missing_docs` asks each file in `tests/` for its `//!`, and no
lint asks a test or a fixture for more.
{%- endif %}

## Rules

### Where Tests Go

1. **Unit tests sit at the bottom of the file they pin, in `#[cfg(test)] mod
   tests`, importing each name, `use super::{Board, Pos}`**, so a reader meets
   the code first and sees what the tests touch; never `use super::*`.
2. **What a caller does is tested in `tests/<name>.rs`, through the public API,
   its tests in a `#[cfg(test)] mod tests` too, the file opening with a `//!`
   that says what it proves**; a test of several files is
   `tests/<name>/main.rs`, since `tests/<name>/mod.rs` is no target and its
   tests never run.
3. **What the crate's tests share lives in `src/testing.rs`, declared
   `#[cfg(test)] mod testing;`, its items `pub(crate)`**, so a fixture is
   written once and stays out of the API. What integration tests share lives in
   `tests/testing/mod.rs`, declared `#[cfg(test)] mod testing;` in each file,
   opening with `#![allow(dead_code, reason = "each test binary uses part of
   this module")]`, the workspace's one `allow`. What another crate's tests need
   sits behind a `testing` feature, `#[doc(hidden)] pub`, turned on only in
   their `[dev-dependencies]`.
4. **A test of what a feature adds sits under that feature's `#[cfg(feature =
   "…")]`**, since it compiles only with the feature on.

### Names and Messages

1. **A test's name is the property it pins, a sentence, article first,
   `a_step_past_the_last_column_is_refused`, and a test pins one property**;
   never `test_`, `it_works` or the function's name, since the name is what a
   failure prints first.
2. **Compare whole values with `assert_eq!`, an error included**, so a failure
   prints what arrived beside what was wanted; `assert!(a == b)`, `is_err()` and
   `matches!` say only that it was wrong.
3. **An assertion's message says the property, a lowercase fragment, and one
   test's messages read as a running sentence, `"to itself"`, `"and
   forwards"`**, never `"test failed"`; it is left out only where the expression
   says it all.
4. **An `expect` says why the call cannot fail here, `expect("3,4 lies on an 8
   by 8 board")`**, never `unwrap` or `"failed"`, so a failure names the
   assumption that broke.
5. **An impossible arm panics with what arrived, `let … else { panic!("…, not
   {moved:?}") }`**, never `unreachable!`, since a failing test is exactly when
   the arm is reached.

### Writing a Test

1. **Test each edge and each refusal**: the empty board, the first and last
   square, one past the end, the largest value, and each error a function
   returns, compared whole, with a test that pins its message.
2. **A test returns `()`**, since an `Err` out of one prints its `Debug` and no
   line.
3. **`#[should_panic(expected = "…")]`, never bare, on a test that returns
   `()`**: a bare one passes on any panic, and on a `Result` test it does not
   compile. A refusal a caller can cause is an error, and its test compares the
   `Err`.
4. **`#[ignore = "…"]` names what the test needs, `"needs a tile server on
   localhost:7070"`**, so whoever skips it knows what runs it; a slow test is
   made fast, not ignored.
5. **A test stands alone: it passes alone, in any order, and beside every other
   in one process**, since nextest gives each test a process of its own and
   hides a shared global, where `cargo test` runs a binary's tests in one.
6. **A test waits for a condition with a deadline, `recv_timeout`, a join, a
   polled flag, never a fixed sleep**, so a slow machine is slow, not red, and a
   hang fails with a message.
7. **A fixture that makes something outside the process, a directory, a port, a
   segment, makes it fresh for each test and gives it back on drop**, a
   `TempDir`, never a fixed path, since tests run at once and may panic midway.
8. **A double is a fake, a small type in the tests implementing the trait the
   code already takes**, over a value the test sets, since a mock's expectations
   restate the implementation; mockall's chained `returning` keeps the last
   value, so each value is an expectation of its own.

### Compile-Fail Tests

1. **A misuse the types refuse is a trybuild fixture,
   `tests/compile_fail/<the_refusal>.rs`, one misuse a file, its `//!` naming
   what it prevents, its `.stderr` committed**, run by `tests/trybuild.rs`; a
   rustdoc `compile_fail` block passes on any error, so it is not the test.
2. **A fixture's message is written by `TRYBUILD=overwrite` and read before it
   is committed**, never edited by hand, since it is the test; a new fixture's
   lands in `wip/`, and fails.
3. **A fixture holds with every feature on**, since trybuild builds it with the
   test's features and the checks turn every one on; one that needs a feature
   off sits in a directory compiled only under `cfg!(not(feature = "…"))`.
4. **A macro's accepted forms are `pass` fixtures in `tests/compile_pass/`**,
   beside its refusals, so a change that refuses every input fails.
5. **Several crates' trybuild suites share a nextest test group of one thread**,
   since they build under one `target/tests/trybuild/`.
6. **What a type must keep, its size, `Send`, `Sync`, `Copy`, is a `const`
   assertion beside it**, which fails the crate's own build, not only a test.

### Properties, Tables and Fuzzing

1. **An invariant over every input is a proptest property**: a round trip, a
   parser that never panics, agreement with a simple model; proptest runs 256
   cases and shrinks a failing input to the smallest.
2. **A property generates valid inputs, `0..8_u16` or `prop_map`, and never
   filters for them with `prop_assume!`**, since proptest gives up after 1,024
   rejections.
3. **A property asserts with `prop_assert!` and `prop_assert_eq!`**, which
   report the smallest failing input once, where an `assert!` prints a panic for
   each shrinking step.
4. **`proptest-regressions/` is committed**, so a case that failed once runs
   first everywhere.
5. **A table of inputs and answers is an rstest, each `#[case]` a test of its
   own, named where its input does not say what it is for**, since a loop stops
   at the first wrong row.
6. **Input from outside the program is fuzzed with cargo-fuzz, in the crate's
   `fuzz/`, a workspace of its own through an empty `[workspace]` table**: a
   target over raw bytes checks that nothing panics, one over an `Arbitrary`
   type spends its time on the grammar.
7. **A target's corpus is committed, and replayed with `cargo fuzz run
   <target> -- -runs=0`**; `cargo fuzz init` ignores it, so that line comes out.
8. **A crash the fuzzer finds, shrunk with `cargo fuzz tmin`, becomes a unit
   test**, so every check pins it, not only the next fuzzing run.
{%- if "miri" in toolchain %}
9. **Under Miri, a property is ignored with its reason, `#[cfg_attr(miri,
   ignore = "…")]`**, since proptest reads the working directory, which Miri's
   isolation blocks; a unit test of its edges runs under Miri instead.
{%- endif %}

### Running

1. **`just check-cargo-nextest` runs every test with nextest, then the doctests
   with `cargo test --doc`**, since nextest cannot run doctests; one test by
   hand is `cargo nextest run -p <crate> <name>`.
2. **An ignored test runs by hand where what it needs is, `--run-ignored
   only`**, before a change to what it tests is done, since no recipe runs it.
3. **Tests that contend for one thing outside the process run in a nextest test
   group of `max-threads = 1`, in `.config/nextest.toml`**, whose
   `[test-groups]` and `[profile.default]` keys are the repository's; the
   cargo-nextest profile owns only the `ci` profile's.
4. **A flaky test is found with `--stress-count` and fixed, never retried into a
   pass**, since a retry hides the race from all but the next run it fails.
5. **A test that can hang has a `slow-timeout` with `terminate-after`**, since
   nextest marks a slow test and stops nothing on its own.
{%- if "strict" in lints %}

Under `strict`, the lints hold more in tests:

- **`unreachable!` and `todo!` are refused**, and `panic_in_result_fn` refuses
  an assertion in a test that returns `Result`.
- **`tests_outside_test_module` refuses a `#[test]` outside a `#[cfg(test)]`
  module**, integration tests included.
- **`unreachable_pub` asks for `pub(crate)`** in `tests/testing/mod.rs`, and
  `as`, absolute paths and `std` where `core` has it are refused as elsewhere.
{%- if "rust-clippy" in devset.profiles %}
- **The workspace's `clippy.toml` lets code in a `#[test]` or a `#[cfg(test)]`
  module unwrap, expect, panic, index and print**; a helper outside both carries
  its own `#[expect]`, with a reason.
{%- endif %}
{%- endif %}

## Steps

Read each reference a step names, whole, before writing the test.

1. **Changing tests**: read the module's tests first and match them; a test
   these rules break is named in the change's description, not rewritten in
   passing.
2. **A new function or type**: `references/writing-tests.md`: a test for each
   edge and each refusal, named for its property, comparing whole values.
3. **A new error type**: `references/writing-tests.md`: a test that provokes
   each refusal, and one that pins each message.
4. **A new test file, a fixture, or a test of a feature**:
   `references/layout.md`.
5. **A misuse the types must refuse, a macro, or what a type must keep**:
   `references/compile-fail.md`.
6. **An invariant, a table of cases, or input from outside**:
   `references/properties.md`.
7. **A failing test**: `references/running.md`: run it alone and read its name
   and message; if it passes alone, run it under `cargo test` and find what it
   shares.
8. **A flaky or hanging test**: `references/running.md` and
   `references/writing-tests.md`: stress it until it fails, find the sleep or
   the shared global, and fix that.
9. **Before finishing**: the checks below, and each ignored test the change
   touches.
{%- if "agents" in lints %}

The types and errors a test pins follow `writing-rust`; a test of unsafe code, a
loom model and a compile-fail test for a misuse of unsafe code also follow
`writing-unsafe-rust`.
{%- if "async" in lints %}

An async test follows `writing-rust`'s async reference: `#[tokio::test]` runs on
one thread.
{%- endif %}
{%- endif %}
{%- if "agents" in rustdoc %}

A doctest, and the `//!` of a test file or a fixture, follow `writing-rustdoc`.
{%- endif %}

## Checks

- `just check`: every check, as CI runs them, after `just fix`.
- `just check-cargo-nextest`: every test under nextest, then the doctests under
  `cargo test --doc`; under CI, nextest's `ci` profile, which runs every test
  however many fail and writes a JUnit report.
{%- if "rust-clippy" in devset.profiles %}
- `just check-rust-clippy`: clippy on every crate, target and feature, the tests
  included.
{%- endif %}
{%- if "cargo-hack" in devset.profiles %}
- `just nightly-cargo-hack`: clippy on every crate's targets, the tests
  included, with no features and with each feature alone, which finds a test
  that needs a feature it is not gated on; it runs nightly, not in `just check`.
{%- endif %}
{%- if "miri" in toolchain %}
- `cargo miri test -p <crate>`: a crate's tests and doctests under Miri; no
  recipe runs it.
{%- endif %}
- By hand, since no recipe runs them: `cargo nextest run --run-ignored only`,
  `TRYBUILD=overwrite cargo nextest run -p <crate> --test trybuild` for a new or
  changed fixture, and `cargo fuzz run <target> -- -runs=0` for each fuzz target
  a change reaches.

## What Not to Do

| Thought                                    | Instead                                                          |
| ------------------------------------------ | ---------------------------------------------------------------- |
| "`use super::*` is shorter"                | Import each name the tests use.                                  |
| "`test_parse` says what it tests"          | The property: `a_pos_with_no_row_is_refused`.                    |
| "`assert!(result.is_err())`"               | `assert_eq!(result, Err(BoundsError { col: 8, cols: 8 }))`.      |
| "`unwrap()`, it is only a test"            | `expect("…")`, saying why it cannot fail here.                   |
| "`-> Result` and `?` keep the test short"  | `()` and `expect`: an `Err` out of a test prints no line.        |
| "`#[should_panic]` is enough"              | `expected = "…"`, with the text of the message.                  |
| "`#[ignore]` the slow one"                 | Make it fast; `#[ignore = "…"]` only for what it needs.          |
| "Sleep 50 ms for the thread"               | Wait for the thing itself, with a deadline.                      |
| "It passes under nextest"                  | It passes under `cargo test` too, with nothing shared.           |
| "Retry it, it is flaky"                    | `--stress-count` until it fails, then fix the race.              |
| "A mock for the store"                     | A fake that implements the trait over a plain value.             |
| "`tests/common/mod.rs` for the helpers"    | `tests/testing/mod.rs`; a test of several files is `main.rs`.    |
| "A `compile_fail` doctest pins it"         | A trybuild fixture, with its `.stderr`.                          |
| "Edit the `.stderr` to match"              | `TRYBUILD=overwrite`, then read the diff.                        |
| "`prop_assume!` the valid inputs"          | Generate only valid inputs.                                      |
| "Loop over the cases in one test"          | An rstest, a case each.                                          |
| "Ignore `proptest-regressions/`, `corpus`" | Commit both.                                                     |
| "nextest runs the doctests"                | `cargo test --doc`, which the check runs after nextest.          |
| "A snapshot crate for the message"         | `assert_eq!` on `to_string()`; `.stderr` are the only snapshots. |

## References

Read every reference a task touches before writing a test, and read them again
after compaction: this body is the summary, and the examples are there.

- `references/layout.md`: before a test file, a fixture, a `testing` feature, a
  test of a feature, or moving tests.
- `references/writing-tests.md`: before any test: its name, assertions and
  messages, `expect`, `#[should_panic]`, `#[ignore]`, what it shares, how it
  waits, its fixtures and doubles.
- `references/running.md`: before running tests by hand, when a test fails,
  hangs or flakes, and before a test group or `.config/nextest.toml`.
- `references/compile-fail.md`: before a compile-fail or compile-pass fixture, a
  `.stderr`, a macro's tests, or a compile-time assertion.
- `references/properties.md`: before a property, a table of cases, a fuzz
  target, or a crash one found.
- `references/sources.md`: before citing a source for a rule, or adapting one.
