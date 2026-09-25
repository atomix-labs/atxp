# `rust`

A Rust repository, whole: EditorConfig, Git attributes and ignores; the `just`
spine, setup and the pinned nightly; CI, with its watch, its nightly run and its
weekly bump; formatting for Rust, TOML, Markdown, YAML, JSON and Python; the
lint wall and the build profiles; dependency policy, and dependencies bumped one
at a time; tests; commits, the changelog and the release; workflow policies;
spelling; editor settings; and Claude Code's skills.

A bundle owns nothing itself: each profile it requires is a layer of its own. To
leave one out, require the profiles wanted from a profile of the repository's
own. [`ansible-lint`](../ansible-lint/README.md),
[`lychee`](../lychee/README.md) and [`mdbook`](../mdbook/README.md) are outside
it, for a repository with playbooks, links to check, or a book; so are
[`msrv`](../msrv/README.md), for crates that build on stable, and
[`cargo-binaries`](../cargo-binaries/README.md), for a repository whose release
ships binaries.

<!-- facts: written by scripts/catalog.py -->

## Requires

- [`editorconfig`](../editorconfig/README.md)
- [`gitattributes`](../gitattributes/README.md)
- [`gitignore`](../gitignore/README.md)
- [`gitignore-rust`](../gitignore-rust/README.md)
- [`mise`](../mise/README.md)
- [`just`](../just/README.md)
- [`setup`](../setup/README.md)
- [`rustup`](../rustup/README.md)
- [`rust-toolchain`](../rust-toolchain/README.md)
- [`github-ci`](../github-ci/README.md)
- [`github-watch`](../github-watch/README.md)
- [`github-nightly`](../github-nightly/README.md)
- [`github-bump`](../github-bump/README.md)
- [`github-release`](../github-release/README.md)
- [`dependabot`](../dependabot/README.md)
- [`automation`](../automation/README.md)
- [`committed`](../committed/README.md)
- [`git-cliff`](../git-cliff/README.md)
- [`typos`](../typos/README.md)
- [`clippy`](../clippy/README.md)
- [`rustdoc`](../rustdoc/README.md)
- [`rustfmt`](../rustfmt/README.md)
- [`lints`](../lints/README.md)
- [`lints-nightly`](../lints-nightly/README.md)
- [`cargo-profiles`](../cargo-profiles/README.md)
- [`cargo-deny`](../cargo-deny/README.md)
- [`cargo-machete`](../cargo-machete/README.md)
- [`cargo-shear`](../cargo-shear/README.md)
- [`cargo-workspace-lints`](../cargo-workspace-lints/README.md)
- [`cargo-hack`](../cargo-hack/README.md)
- [`cargo-bump`](../cargo-bump/README.md)
- [`manifest-lint`](../manifest-lint/README.md)
- [`nextest`](../nextest/README.md)
- [`taplo`](../taplo/README.md)
- [`dprint`](../dprint/README.md)
- [`rumdl`](../rumdl/README.md)
- [`ruff`](../ruff/README.md)
- [`yamllint`](../yamllint/README.md)
- [`shellcheck`](../shellcheck/README.md)
- [`actionlint`](../actionlint/README.md)
- [`zizmor`](../zizmor/README.md)
- [`conftest`](../conftest/README.md)
- [`policies`](../policies/README.md)
- [`suppressions`](../suppressions/README.md)
- [`vscode-rust`](../vscode-rust/README.md)
- [`claude-skills`](../claude-skills/README.md)

<!-- /facts -->
