# `cargo-nextest`

cargo-nextest for every test, and cargo for the doctests; in CI, a `ci` profile
that runs them all.

```sh
devset add atxp/cargo-nextest --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `cargo` · In [`rust`](../bundles/rust.md): always

Tests run with cargo-nextest, and doctests, which nextest does not run, with
cargo. Under CI, nextest's `ci` profile runs every test however many fail, and
writes a JUnit report.

It owns the `ci` profile's keys of `.config/nextest.toml`.

## Owns

| File                                            | Part  | Policy | Notes |
| ----------------------------------------------- | ----- | ------ | ----- |
| `.config/nextest.toml`                          | keys  | owned  |       |
| `.just/cargo-nextest.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-cargo-nextest.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                        | keys  | owned  |       |

## Recipes

- `check-cargo-nextest`: Runs every test, then the doctests nextest leaves to
  cargo; under CI, with nextest's `ci` profile.

## Requires

- [`rust-toolchain`](../rust/rust-toolchain.md)
