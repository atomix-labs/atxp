# `rust-doc`

rustdoc builds every crate's documentation with every feature, private items
included, and fails on any warning: a broken intra-doc link, a malformed code
block, a missing item it refers to.

The `strict` feature, the house policy, adds the house's doc lint to
`check-rust-doc`, over every crate of the workspace: summaries that open weakly,
filler and marketing words, process notes left in comments, sections named other
than `# Errors`, `# Panics`, `# Safety` and `# Examples`, and dependency tables
without their `# internal` and `# external` groups. `.just/rust-doc.py` is the
lint, which the skill runs too.

The `agents` feature adds the `writing-rustdoc` skill in `.claude/skills/`: the
house style for docs and comments, with its audit and inventory scripts, so an
agent writes documentation as the repository wants it.

<!-- facts: written by devset-collection -->

## Owns

| File                                                      | Part  | Policy | Notes            |
| --------------------------------------------------------- | ----- | ------ | ---------------- |
| `.just/rust-doc.just`                                     | whole | owned  | template         |
| `.just/rust-doc.py`                                       | whole | owned  |                  |
| `.claude/skills/writing-rustdoc/SKILL.md`                 | whole | owned  | feature `agents` |
| `.claude/skills/writing-rustdoc/references/comments.md`   | whole | owned  | feature `agents` |
| `.claude/skills/writing-rustdoc/references/exemplars.md`  | whole | owned  | feature `agents` |
| `.claude/skills/writing-rustdoc/references/sources.md`    | whole | owned  | feature `agents` |
| `.claude/skills/writing-rustdoc/references/style.md`      | whole | owned  | feature `agents` |
| `.claude/skills/writing-rustdoc/references/templates.md`  | whole | owned  | feature `agents` |
| `.claude/skills/writing-rustdoc/references/tooling.md`    | whole | owned  | feature `agents` |
| `.claude/skills/writing-rustdoc/scripts/doc-audit.sh`     | whole | owned  | feature `agents` |
| `.claude/skills/writing-rustdoc/scripts/doc-inventory.py` | whole | owned  | feature `agents` |

## Features

| Feature  | Default | Enables |
| -------- | ------- | ------- |
| `strict` |         |         |
| `agents` |         |         |

## Recipes

- `check-rust-doc`: Builds every crate's documentation, private items included;
  a warning, such as a broken link, fails. Then the house's doc lint, over every
  crate (with `strict`).

## Requires

- [`rust-toolchain`](../rust-toolchain/README.md)

<!-- /facts -->
