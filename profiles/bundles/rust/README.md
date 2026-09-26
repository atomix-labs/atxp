# `rust`

A Rust repository, whole: the pinned toolchain, formatting and the lint wall,
dependency policy and dependencies bumped one at a time, tests, the build
profiles, manifests in one shape; EditorConfig, Git attributes and ignores,
commits and the changelog; formatting and linting for Markdown, TOML, YAML and
shell, and spelling; the `just` spine, setup, mise and devset; and CI, with its
watch and its weekly bump.

A bundle owns nothing itself: each profile it requires is a layer of its own,
and its features describe the kind of project:

| Feature    | Adds                                                                         |
| ---------- | ---------------------------------------------------------------------------- |
| `docs`     | a book, with [`mdbook`](../../docs/mdbook/README.md)                          |
| `agents`   | the skills for rustdoc and manifests                                         |
| `publish`  | crates.io, with [`cargo-publish`](../../cargo/cargo-publish/README.md), and the release |
| `binaries` | release archives, with [`cargo-binaries`](../../cargo/cargo-binaries/README.md) |
| `nightly`  | nightly's own lints, cargo-hack's feature matrix, and the nightly run         |
| `strict`   | the house policy: cargo-deny's bans, the full lint wall, `panic = "abort"`   |

None is on by default. Outside it are
[`rust-msrv`](../../rust/rust-msrv/README.md), for crates that build on stable;
[`python`](../../lang/python/README.md), [`ansible`](../../lang/ansible/README.md)
and [`lychee`](../../docs/lychee/README.md); and
[`vscode`](../../tooling/vscode/README.md) and
[`suppressions`](../../tooling/suppressions/README.md).

<!-- facts: written by scripts/catalog.py -->

## Requires

- [`editorconfig`](../../tooling/editorconfig/README.md)
- [`git-attributes`](../../git/git-attributes/README.md)
- [`git-ignore`](../../git/git-ignore/README.md)
- [`cargo-workspace`](../../cargo/cargo-workspace/README.md)
- [`mise`](../../tooling/mise/README.md)
- [`just`](../../tooling/just/README.md)
- [`setup`](../../tooling/setup/README.md)
- [`rustup`](../../rust/rustup/README.md)
- [`rust-toolchain`](../../rust/rust-toolchain/README.md)
- [`github-ci`](../../github/github-ci/README.md)
- [`github-watch`](../../github/github-watch/README.md)
- [`github-nightly`](../../github/github-nightly/README.md)
- [`github-bump`](../../github/github-bump/README.md)
- [`github-release`](../../github/github-release/README.md)
- [`github-dependabot`](../../github/github-dependabot/README.md)
- [`github-automation`](../../github/github-automation/README.md)
- [`git-commits`](../../git/git-commits/README.md)
- [`git-changelog`](../../git/git-changelog/README.md)
- [`spelling`](../../lang/spelling/README.md)
- [`rust-clippy`](../../rust/rust-clippy/README.md)
- [`rust-doc`](../../rust/rust-doc/README.md)
- [`rust-fmt`](../../rust/rust-fmt/README.md)
- [`rust-lints`](../../rust/rust-lints/README.md)
- [`lints-nightly`](../../rust/lints-nightly/README.md)
- [`cargo-profiles`](../../cargo/cargo-profiles/README.md)
- [`cargo-deny`](../../cargo/cargo-deny/README.md)
- [`cargo-unused`](../../cargo/cargo-unused/README.md)
- [`cargo-shear`](../../cargo/cargo-shear/README.md)
- [`cargo-workspace-lints`](../../cargo/cargo-workspace-lints/README.md)
- [`cargo-hack`](../../cargo/cargo-hack/README.md)
- [`cargo-bump`](../../cargo/cargo-bump/README.md)
- [`cargo-manifest`](../../cargo/cargo-manifest/README.md)
- [`cargo-nextest`](../../cargo/cargo-nextest/README.md)
- [`toml`](../../lang/toml/README.md)
- [`dprint`](../../lang/dprint/README.md)
- [`markdown`](../../lang/markdown/README.md)
- [`python`](../../lang/python/README.md)
- [`yaml`](../../lang/yaml/README.md)
- [`shell`](../../lang/shell/README.md)
- [`github-workflow-lint`](../../github/github-workflow-lint/README.md)
- [`zizmor`](../../github/zizmor/README.md)
- [`conftest`](../../github/conftest/README.md)
- [`policies`](../../github/policies/README.md)
- [`suppressions`](../../tooling/suppressions/README.md)
- [`vscode`](../../tooling/vscode/README.md)
- [`claude-skills`](../../rust/claude-skills/README.md)

<!-- /facts -->
