# `claude-skills`

Skills for Claude Code, in `.claude/skills/`: `writing-rustdoc`, the style for
docs and comments, with its audit, inventory and lint scripts; and
`writing-cargo-manifest`, the shape of a `Cargo.toml` that
[`manifest-lint`](../manifest-lint/README.md) and [`taplo`](../taplo/README.md)
hold.

[`gitignore`](../gitignore/README.md) leaves the rest of `.claude/` to each
developer.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                                          | Part  | Policy | Notes |
| ------------------------------------------------------------- | ----- | ------ | ----- |
| `.claude/skills/writing-cargo-manifest/SKILL.md`              | whole | owned  |       |
| `.claude/skills/writing-cargo-manifest/references/sources.md` | whole | owned  |       |
| `.claude/skills/writing-rustdoc/SKILL.md`                     | whole | owned  |       |
| `.claude/skills/writing-rustdoc/references/comments.md`       | whole | owned  |       |
| `.claude/skills/writing-rustdoc/references/exemplars.md`      | whole | owned  |       |
| `.claude/skills/writing-rustdoc/references/sources.md`        | whole | owned  |       |
| `.claude/skills/writing-rustdoc/references/style.md`          | whole | owned  |       |
| `.claude/skills/writing-rustdoc/references/templates.md`      | whole | owned  |       |
| `.claude/skills/writing-rustdoc/references/tooling.md`        | whole | owned  |       |
| `.claude/skills/writing-rustdoc/scripts/doc-audit.sh`         | whole | owned  |       |
| `.claude/skills/writing-rustdoc/scripts/doc-inventory.py`     | whole | owned  |       |
| `.claude/skills/writing-rustdoc/scripts/doc-lint.py`          | whole | owned  |       |

<!-- /facts -->
