# `project`

The documents every project keeps, each scaffolded where the repository has none
and the repository's once written: a README, the licence, how to contribute, how
to report a vulnerability, and how to move across a breaking change; with
`conduct`, the Contributor Covenant 2.1, and with `architecture`, a page for how
the project is built.

Two of them keep a managed block:

- The README's header: centered, the logo `logo` names, drawn as
  `<logo>-light.svg` and `<logo>-dark.svg` for each theme, or else the name; the
  tagline `description` gives; and badges that follow the profiles applied: CI
  where [`github-ci`](../../github/github-ci/README.md) is, crates.io and
  docs.rs where [`cargo-publish`](../../cargo/cargo-publish/README.md) publishes
  the crate `crate` names, or else the one
  [`cargo-workspace`](../../cargo/cargo-workspace/README.md) names, and the book
  where [`mdbook`](../../docs/mdbook/README.md) builds one. Markdown cannot
  center, so the header is HTML, inside `dprint-ignore` markers that keep the
  formatter from laying it out again. A README the project starts from here
  opens with it, then the demo [`vhs`](../../docs/vhs/README.md) records where
  that is applied; one the project has already gets the block at its end, to
  move to its top in place of its own title.
- CONTRIBUTING's checks say to run `just check` before a pull request and `just
  fix` for what it can fix; [`git-commits`](../../git/git-commits/README.md)
  adds the commit rules.

`license` chooses the licence files: `MIT OR Apache-2.0`, the default, writes
`LICENSE-MIT` and `LICENSE-APACHE`; `MIT` or `Apache-2.0` writes one `LICENSE`.
The copyright line names `authors`, or else the directory. The Covenant's
contact is left for the project to fill in.

<!-- facts: written by devset-collection -->

## Owns

| File                  | Part  | Policy | Notes                                                             |
| --------------------- | ----- | ------ | ----------------------------------------------------------------- |
| `README.md`           | block | owned  | template, feature `readme`                                        |
| `CONTRIBUTING.md`     | block | owned  | feature `contributing`                                            |
| `LICENSE-MIT`         | whole | once   | template, feature `license`, `license` one of `MIT OR Apache-2.0` |
| `LICENSE-APACHE`      | whole | once   | feature `license`, `license` one of `MIT OR Apache-2.0`           |
| `LICENSE`             | whole | once   | template, feature `license`, `license` one of `MIT`, `Apache-2.0` |
| `SECURITY.md`         | whole | once   | template, feature `security`                                      |
| `BREAKING-CHANGES.md` | whole | once   | template, feature `breaking-changes`                              |
| `CODE_OF_CONDUCT.md`  | whole | once   | feature `conduct`                                                 |
| `ARCHITECTURE.md`     | whole | once   | feature `architecture`                                            |

## Features

| Feature            | Default | Enables                           |
| ------------------ | ------- | --------------------------------- |
| `readme`           | yes     |                                   |
| `license`          | yes     |                                   |
| `contributing`     | yes     |                                   |
| `security`         | yes     |                                   |
| `breaking-changes` | yes     | `git-changelog?/breaking-changes` |
| `conduct`          |         |                                   |
| `architecture`     |         |                                   |

## Variables

| Variable      | Default             | Asks                                                                            |
| ------------- | ------------------- | ------------------------------------------------------------------------------- |
| `name`        | empty               | The project's name, and its first crate's; empty takes the directory's          |
| `crate`       | empty               | The crate the crates.io and docs.rs badges show; empty takes the project's name |
| `description` | empty               | One line: what the project is                                                   |
| `logo`        | empty               | The README's logo: its path before `-light.svg` or `-dark.svg`                  |
| `authors`     | empty               | Authors, comma-separated                                                        |
| `license`     | `MIT OR Apache-2.0` | The licence, an SPDX expression                                                 |
| `repository`  | none                | The GitHub repository, owner/name                                               |

## Requires

- [`git-changelog`](../../git/git-changelog/README.md): optional

<!-- /facts -->
