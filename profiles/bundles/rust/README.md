# `rust`

A Rust repository, whole, from nothing: a workspace where there is none, the
pinned toolchain, formatting and the lint wall, dependency policy and
dependencies bumped one at a time, tests, the build profiles, manifests in one
shape; EditorConfig, Git attributes and ignores, commits and the changelog;
formatting and linting for Markdown, TOML, YAML and shell, and spelling; the
`just` spine, setup, mise and devset; and CI, with its watch and its weekly
bump.

A bundle owns nothing itself: each profile it requires is a layer of its own,
and its features describe the kind of project:

| Feature    | Adds                                                                                                             |
| ---------- | ---------------------------------------------------------------------------------------------------------------- |
| `docs`     | a book, with [`mdbook`](../../docs/mdbook/README.md)                                                             |
| `agents`   | the skills for rustdoc and manifests                                                                             |
| `publish`  | crates.io, with [`cargo-publish`](../../cargo/cargo-publish/README.md), the release, and the project's documents |
| `binaries` | release archives, with [`cargo-binaries`](../../cargo/cargo-binaries/README.md)                                  |
| `oss`      | an open-source project's documents with its code of conduct, and the issue and pull request templates            |
| `nightly`  | nightly's own lints, cargo-hack's feature matrix, and the nightly run                                            |
| `strict`   | the house policy: cargo-deny's bans, the full lint wall, the doc lint, `panic = "abort"`                         |

None is on by default. Outside it are
[`rust-msrv`](../../rust/rust-msrv/README.md), for crates that build on stable;
[`python`](../../lang/python/README.md),
[`ansible`](../../lang/ansible/README.md) and
[`lychee`](../../docs/lychee/README.md); and
[`vscode`](../../tooling/vscode/README.md) and
[`suppressions`](../../tooling/suppressions/README.md).

<!-- facts: written by devset-collection -->

## Features

| Feature    | Default | Enables                                                                              |
| ---------- | ------- | ------------------------------------------------------------------------------------ |
| `docs`     |         | `dep:mdbook`                                                                         |
| `agents`   |         | `rust-doc/agents`, `cargo-manifest/agents`                                           |
| `publish`  |         | `dep:cargo-publish`, `dep:github-release`, `dep:project`                             |
| `binaries` |         | `dep:cargo-binaries`, `dep:github-release`                                           |
| `oss`      |         | `dep:project`, `project/conduct`, `dep:github-templates`                             |
| `nightly`  |         | `rust-lints/nightly`, `dep:cargo-hack`, `dep:github-nightly`                         |
| `strict`   |         | `cargo-deny/strict`, `rust-lints/strict`, `cargo-profiles/strict`, `rust-doc/strict` |

## Requires

- [`rust-toolchain`](../../rust/rust-toolchain/README.md)
- [`rust-fmt`](../../rust/rust-fmt/README.md)
- [`rust-clippy`](../../rust/rust-clippy/README.md)
- [`rust-lints`](../../rust/rust-lints/README.md)
- [`rust-doc`](../../rust/rust-doc/README.md)
- [`cargo-workspace`](../../cargo/cargo-workspace/README.md)
- [`cargo-deny`](../../cargo/cargo-deny/README.md)
- [`cargo-unused`](../../cargo/cargo-unused/README.md)
- [`cargo-nextest`](../../cargo/cargo-nextest/README.md)
- [`cargo-profiles`](../../cargo/cargo-profiles/README.md)
- [`cargo-manifest`](../../cargo/cargo-manifest/README.md)
- [`cargo-bump`](../../cargo/cargo-bump/README.md)
- [`git-ignore`](../../git/git-ignore/README.md)
- [`git-attributes`](../../git/git-attributes/README.md)
- [`git-commits`](../../git/git-commits/README.md)
- [`git-changelog`](../../git/git-changelog/README.md)
- [`github-ci`](../../github/github-ci/README.md)
- [`github-bump`](../../github/github-bump/README.md)
- [`github-watch`](../../github/github-watch/README.md)
- [`github-dependabot`](../../github/github-dependabot/README.md)
- [`github-workflow-lint`](../../github/github-workflow-lint/README.md)
- [`markdown`](../../lang/markdown/README.md)
- [`toml`](../../lang/toml/README.md)
- [`yaml`](../../lang/yaml/README.md)
- [`spelling`](../../lang/spelling/README.md)
- [`shell`](../../lang/shell/README.md)
- [`mise`](../../tooling/mise/README.md)
- [`just`](../../tooling/just/README.md)
- [`setup`](../../tooling/setup/README.md)
- [`editorconfig`](../../tooling/editorconfig/README.md)
- [`devset`](../../devset/devset/README.md)
- [`mdbook`](../../docs/mdbook/README.md): optional
- [`cargo-publish`](../../cargo/cargo-publish/README.md): optional
- [`github-release`](../../github/github-release/README.md): optional
- [`cargo-binaries`](../../cargo/cargo-binaries/README.md): optional
- [`cargo-hack`](../../cargo/cargo-hack/README.md): optional
- [`github-nightly`](../../github/github-nightly/README.md): optional
- [`project`](../../project/project/README.md): optional
- [`github-templates`](../../github/github-templates/README.md): optional

<!-- /facts -->
