# `cargo-publish`

crates.io: every crate a release publishes packaged on each change, and
published at the release by trusted publishing.

```sh
devset add atxp/cargo-publish --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `cargo` · In [`rust`](../bundles/rust.md): with `publish`

Publishes the workspace's crates to [crates.io](https://crates.io) at each
release. A crate is published when its `publish` allows crates.io; one with
`publish = false` never is.

- `check-cargo-publish` first holds every such crate to what its page on
  crates.io shows, below, then packages it on each change, and builds each from
  its package, as crates.io will: a file the package leaves out, or a dependency
  without a version, fails the change rather than the release. It packages the
  working tree as it is, changes and all. Between releases, while crates.io has
  a crate at its version already, cargo would build its dependents against
  crates.io's copy rather than the working tree's, so the crates are packaged
  without the build; a release's check, at the new versions, builds them all.
  Cargo never unpacks or builds again a crate it has packaged at a version, so a
  check that builds first drops what an earlier one left of the workspace's
  crates, and a sibling changed since is built as it now is.
- `publish-cargo-publish`, which `just publish` runs, publishes every crate
  crates.io does not have at its version, dependencies first. So a release that
  stopped halfway publishes the rest when it runs again.

[`github-release`](../github/github-release.md) runs `just publish` once the
GitHub Release is out, with a token crates.io gives the workflow for 30 minutes
by trusted publishing: no token is stored. A crate's first version is published
by hand, with a token of the owner's, since crates.io trusts a workflow only for
a crate that exists. Then, in the crate's settings on crates.io, add the GitHub
trusted publisher: the repository, the workflow `release.yml`, and the
environment `release`.

crates.io asks each crate for a description, a licence and a repository:
[`cargo-workspace`](cargo-workspace.md)'s crates each write their own
description and inherit the rest from `[workspace.package]`. What else its page
shows, the check holds each crate to, and names what to add where one falls
short:

- **Each crate has a README**, a `README.md` beside its `Cargo.toml`, which
  Cargo finds, or the file `readme` names. Every link and image in it is
  absolute, since crates.io shows it away from the repository: a relative `src`,
  `srcset`, `href` or Markdown link is refused, with the URL to write.
- **`keywords` holds one to five**, each at most 20 ASCII letters, digits, `_`,
  `-` or `+`, the first a letter or a digit, as crates.io takes them.
- **`categories` holds one to five slugs of crates.io's**, which
  `.just/cargo-publish/categories.txt` keeps as
  [crates.io lists them](https://crates.io/category_slugs).
- **The package holds the text of each licence `license` names**, `LICENSE-MIT`
  and `LICENSE-APACHE` for `MIT OR Apache-2.0`, linked into a crate under
  `crates/` from the root.
- **A `homepage` or a `documentation` is set where [`mdbook`](../docs/mdbook.md)
  builds a book**, and the finding names the book's URL for it,
  `https://<owner>.github.io/<name>/`.

A crate with `publish = false` is never read, so a repository that publishes
nothing is unaffected; the first crate the scaffold writes has none of these
until its owner writes them. The `rust` bundle brings this profile with its
`publish` feature: a repository opts in to publishing.

## Owns

| File                                 | Part  | Policy | Notes    |
| ------------------------------------ | ----- | ------ | -------- |
| `.just/cargo-publish.just`           | whole | owned  | template |
| `.just/cargo-publish.py`             | whole | owned  |          |
| `.just/cargo-publish/categories.txt` | whole | owned  |          |

## Recipes

- `check-cargo-publish`: Holds every crate crates.io would publish to what its
  page shows, then packages and builds it.
- `publish-cargo-publish`: Publishes every crate crates.io does not have at its
  version yet, dependencies first.

## Variables

| Variable     | Default | Asks                              |
| ------------ | ------- | --------------------------------- |
| `repository` | none    | The GitHub repository, owner/name |

## Requires

- [`just`](../tooling/just.md)
- [`rust-toolchain`](../rust/rust-toolchain.md)
