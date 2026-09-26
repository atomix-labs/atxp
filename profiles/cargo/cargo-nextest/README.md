# `cargo-nextest`

Tests run with cargo-nextest, and doctests, which nextest does not run, with
cargo. Under CI, nextest's `ci` profile runs every test however many fail, and
writes a JUnit report.

It owns the `ci` profile's keys of `.config/nextest.toml`.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                      | Part  | Policy | Notes |
| ----------------------------------------- | ----- | ------ | ----- |
| `.config/nextest.toml`                    | keys  | owned  |       |
| `.just/cargo-nextest.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-cargo-nextest.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                  | keys  | owned  |       |

## Recipes

- `check-cargo-nextest`: Runs every test, then the doctests nextest leaves to cargo;
  under CI, with nextest's `ci` profile.

<!-- /facts -->
