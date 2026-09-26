# `rust`

A Rust repository, whole: EditorConfig, Git attributes and ignores; the `just`
spine, setup and the pinned nightly; CI, with its watch, its nightly run and its
weekly bump; formatting for Rust, TOML, Markdown, YAML, JSON and Python; the
lint wall and the build profiles; dependency policy, and dependencies bumped one
at a time; tests; commits, the changelog and the release; workflow policies;
spelling; editor settings; and Claude Code's skills.

A bundle owns nothing itself: each profile it requires is a layer of its own. To
leave one out, require the profiles wanted from a profile of the repository's
own. [`ansible-lint`](../../lang/ansible/README.md),
[`lychee`](../../docs/lychee/README.md) and [`mdbook`](../../docs/mdbook/README.md) are outside
it, for a repository with playbooks, links to check, or a book; so are
[`msrv`](../../rust/rust-msrv/README.md), for crates that build on stable, and
[`cargo-binaries`](../../cargo/cargo-binaries/README.md), for a repository whose release
ships binaries.

<!-- facts: written by scripts/catalog.py -->

## Requires

- [`editorconfig`](../../tooling/editorconfig/README.md)
- [`gitattributes`](../../git/git-attributes/README.md)
- [`gitignore`](../../git/git-ignore/README.md)
- [`gitignore-rust`](../../cargo/cargo-workspace/README.md)
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
- [`dependabot`](../../github/github-dependabot/README.md)
- [`automation`](../../github/github-automation/README.md)
- [`committed`](../../git/git-commits/README.md)
- [`git-cliff`](../../git/git-changelog/README.md)
- [`typos`](../../lang/spelling/README.md)
- [`clippy`](../../rust/rust-clippy/README.md)
- [`rustdoc`](../../rust/rust-doc/README.md)
- [`rustfmt`](../../rust/rust-fmt/README.md)
- [`lints`](../../rust/rust-lints/README.md)
- [`lints-nightly`](../../rust/lints-nightly/README.md)
- [`cargo-profiles`](../../cargo/cargo-profiles/README.md)
- [`cargo-deny`](../../cargo/cargo-deny/README.md)
- [`cargo-machete`](../../cargo/cargo-unused/README.md)
- [`cargo-shear`](../../cargo/cargo-shear/README.md)
- [`cargo-workspace-lints`](../../cargo/cargo-workspace-lints/README.md)
- [`cargo-hack`](../../cargo/cargo-hack/README.md)
- [`cargo-bump`](../../cargo/cargo-bump/README.md)
- [`manifest-lint`](../../cargo/cargo-manifest/README.md)
- [`nextest`](../../cargo/cargo-nextest/README.md)
- [`taplo`](../../lang/toml/README.md)
- [`dprint`](../../lang/dprint/README.md)
- [`rumdl`](../../lang/markdown/README.md)
- [`ruff`](../../lang/python/README.md)
- [`yamllint`](../../lang/yaml/README.md)
- [`shellcheck`](../../lang/shell/README.md)
- [`actionlint`](../../github/github-workflow-lint/README.md)
- [`zizmor`](../../github/zizmor/README.md)
- [`conftest`](../../github/conftest/README.md)
- [`policies`](../../github/policies/README.md)
- [`suppressions`](../../tooling/suppressions/README.md)
- [`vscode-rust`](../../tooling/vscode/README.md)
- [`claude-skills`](../../rust/claude-skills/README.md)

<!-- /facts -->
