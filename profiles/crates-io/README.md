# `crates-io`

Publishes the workspace's crates to [crates.io](https://crates.io) at each
release. A crate is published when its `publish` allows crates.io; one with
`publish = false` never is.

- `check-crates-io` packages every such crate on each change, and builds each
  from its package, as crates.io will: a file the package leaves out, or a
  dependency without a version, fails the change rather than the release. It
  packages the working tree as it is, changes and all.
- `publish-crates-io`, which `just publish` runs, publishes every crate
  crates.io does not have at its version, dependencies first. So a release that
  stopped halfway publishes the rest when it runs again.

[`github-release`](../github-release/README.md) runs `just publish` once the
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
| `.just/crates-io.just` | whole | owned  |       |
| `.just/crates-io.py`   | whole | owned  |       |

## Recipes

- `check-crates-io`: Packages every crate crates.io would publish, and builds
  each from its package, as crates.io will.
- `publish-crates-io`: Publishes every crate crates.io does not have at its
  version yet, dependencies first.

## Requires

- [`rustup`](../rustup/README.md)
- [`just`](../just/README.md)

<!-- /facts -->
