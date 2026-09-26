# `vscode`

VS Code, set up for the tools the target's profiles bring. Each tool's extension
is recommended where the profile that brings the tool is applied: rust-analyzer
with [`rust-toolchain`](../../rust/rust-toolchain/README.md), Even Better TOML
with [`toml`](../../lang/toml/README.md), dprint's with
[`dprint`](../../lang/dprint/README.md), rumdl's with
[`markdown`](../../lang/markdown/README.md) and just's syntax with
[`just`](../just/README.md). Each language is formatted on save and on paste by
its tool, and each tool comes with its settings: rust-analyzer checks every
feature in a target directory of its own, so it never waits on a build, with
clippy as its check where [`rust-clippy`](../../rust/rust-clippy/README.md) is
applied; rumdl fixes on save, and Markdown links are validated.

It owns those keys of `.vscode/extensions.json` and `.vscode/settings.json`,
under `merge`, so settings the repository changes are kept. `recommendations`
follows the profiles applied, so it is the profile's own: a list is one value,
and an extension the repository adds to it conflicts with the next change of the
graph.

<!-- facts: written by devset-collection -->

## Owns

| File                      | Part | Policy | Notes    |
| ------------------------- | ---- | ------ | -------- |
| `.vscode/extensions.json` | keys | merge  | template |
| `.vscode/settings.json`   | keys | merge  | template |

<!-- /facts -->
