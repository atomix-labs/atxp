# `cargo-nextest`

Tests run with cargo-nextest, and doctests, which nextest does not run, with
cargo. Under CI, nextest's `ci` profile runs every test however many fail, and
writes a JUnit report.

It owns the `ci` profile's keys of `.config/nextest.toml`; the rest of the file,
test groups and the default profile's keys, is the repository's.

The `agents` feature adds the `writing-rust-tests` skill in `.claude/skills/`:
where unit and integration tests and their fixtures live, names that state the
property a test pins, assertion and `expect` messages that say what broke,
`#[should_panic]` and `#[ignore]` with their reasons, tests that stand alone and
wait with deadlines, fakes over mocks, trybuild compile-fail fixtures, proptest
properties, rstest tables and cargo-fuzz targets with their corpus, and how
nextest runs the tests and Cargo the doctests. Each bad example a lint catches
fails with that lint, and each good one compiles under the workspace's lints.
Where [`rust-lints`](../../rust/rust-lints/README.md) has `strict`, it teaches
what the strict lints refuse in tests; it names `just nightly-cargo-hack` only
where [`cargo-hack`](../cargo-hack/README.md) is applied, and Miri only where
[`rust-toolchain`](../../rust/rust-toolchain/README.md) has its `miri` feature.

<!-- facts: written by devset-collection -->

## Owns

| File                                                            | Part  | Policy | Notes                      |
| --------------------------------------------------------------- | ----- | ------ | -------------------------- |
| `.config/nextest.toml`                                          | keys  | owned  |                            |
| `.just/cargo-nextest.just`                                      | whole | owned  |                            |
| `.config/mise/conf.d/devset-cargo-nextest.toml`                 | whole | owned  |                            |
| `.config/mise/mise.lock`                                        | keys  | owned  |                            |
| `.claude/skills/writing-rust-tests/SKILL.md`                    | whole | owned  | template, feature `agents` |
| `.claude/skills/writing-rust-tests/references/compile-fail.md`  | whole | owned  | template, feature `agents` |
| `.claude/skills/writing-rust-tests/references/layout.md`        | whole | owned  | template, feature `agents` |
| `.claude/skills/writing-rust-tests/references/properties.md`    | whole | owned  | template, feature `agents` |
| `.claude/skills/writing-rust-tests/references/running.md`       | whole | owned  | template, feature `agents` |
| `.claude/skills/writing-rust-tests/references/sources.md`       | whole | owned  | template, feature `agents` |
| `.claude/skills/writing-rust-tests/references/writing-tests.md` | whole | owned  | template, feature `agents` |

## Features

| Feature  | Default | Enables |
| -------- | ------- | ------- |
| `agents` |         |         |

## Recipes

- `check-cargo-nextest`: Runs every test, then the doctests nextest leaves to
  cargo; under CI, with nextest's `ci` profile.

## Requires

- [`rust-toolchain`](../../rust/rust-toolchain/README.md)

<!-- /facts -->
