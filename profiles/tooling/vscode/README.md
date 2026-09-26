# `vscode`

VS Code for a Rust repository: its tools' extensions recommended; clippy as
rust-analyzer's check, over every feature, in a target directory of its own, so
it never waits on a build; each language formatted on save and on paste by its
tool; rumdl fixing on save; and Markdown links validated.

It owns those keys of `.vscode/extensions.json` and `.vscode/settings.json`,
under `merge`, so settings the repository changes are kept.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                      | Part | Policy | Notes |
| ------------------------- | ---- | ------ | ----- |
| `.vscode/extensions.json` | keys | merge  |       |
| `.vscode/settings.json`   | keys | merge  |       |

<!-- /facts -->
