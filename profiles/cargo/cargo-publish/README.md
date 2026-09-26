# `cargo-publish`

Publishes the workspace's crates to [crates.io](https://crates.io) at each
release. A crate is published when its `publish` allows crates.io; one with
`publish = false` never is.

- `check-cargo-publish` packages every such crate on each change, and builds each
  from its package, as crates.io will: a file the package leaves out, or a
  dependency without a version, fails the change rather than the release. It
  packages the working tree as it is, changes and all. Between releases, while
  crates.io has a crate at its version already, cargo would build its dependents
  against crates.io's copy rather than the working tree's, so the crates are
  packaged without the build; a release's check, at the new versions, builds
  them all.
- `publish-cargo-publish`, which `just publish` runs, publishes every crate
  crates.io does not have at its version, dependencies first. So a release that
  stopped halfway publishes the rest when it runs again.

[`github-release`](../../github/github-release/README.md) runs `just publish` once the
GitHub Release is out, with a token crates.io gives the workflow for 30 minutes
by trusted publishing: no token is stored. A crate's first version is published
by hand, with a token of the owner's, since crates.io trusts a workflow only for
a crate that exists. Then, in the crate's settings on crates.io, add the GitHub
trusted publisher: the repository, the workflow `release.yml`, and the
environment `release`.

It is not in the `rust` bundle: a repository opts in to publishing.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                   | Part  | Policy | Notes |
| ---------------------- | ----- | ------ | ----- |
| `.just/cargo-publish.just` | whole | owned  |       |
| `.just/cargo-publish.py`   | whole | owned  |       |

## Recipes

- `check-cargo-publish`: Packages every crate crates.io would publish, and builds
  each from its package, as crates.io will.
- `publish-cargo-publish`: Publishes every crate crates.io does not have at its
  version yet, dependencies first.

## Requires

- [`rustup`](../../rust/rustup/README.md)
- [`just`](../../tooling/just/README.md)

<!-- /facts -->
