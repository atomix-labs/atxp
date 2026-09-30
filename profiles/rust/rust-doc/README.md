# `rust-doc`

rustdoc builds every crate's documentation with every feature, private items
included, and fails on any warning: a broken intra-doc link, a malformed code
block, a missing item it refers to.

The `strict` feature, the house policy, adds the house's doc lint to
`check-rust-doc`, over every crate of the workspace: summaries that open weakly,
filler and marketing words, a crate of the workspace named where it is neither
the crate, its family nor a dependency, process notes left in comments, sections
the house does not use, `# Arguments`, `# Returns` and their kin, and dependency
tables without their `# external` and `# internal` groups. `.just/rust-doc.py`
is the lint, which the skill runs too.

The `agents` feature adds the `writing-rustdoc` skill in `.claude/skills/`: how
docs and comments are written here, saying only what the code cannot and asking
for a fact rather than guessing it. It gives the summary each kind of item
takes; the sections, their order and form; examples that show why and end in an
assertion; the crate page; a cut list of what to delete on sight; and the
wording of each safety, invariant and ordering comment, `#[expect]` reason,
message, test name and file header. Templates, annotated exemplars, and an audit
and an inventory script come with it, so an agent writes documentation as the
repository wants it.

<!-- facts: written by devset-collection -->

## Owns

| File                                                      | Part  | Policy | Notes                        |
| --------------------------------------------------------- | ----- | ------ | ---------------------------- |
| `.just/rust-doc.just`                                     | whole | owned  | template                     |
| `.just/rust-doc.py`                                       | whole | owned  |                              |
| `.claude/skills/writing-rustdoc/SKILL.md`                 | whole | owned  | template, feature `agents`   |
| `.claude/skills/writing-rustdoc/references/comments.md`   | whole | owned  | template, feature `agents`   |
| `.claude/skills/writing-rustdoc/references/exemplars.md`  | whole | owned  | template, feature `agents`   |
| `.claude/skills/writing-rustdoc/references/sources.md`    | whole | owned  | feature `agents`             |
| `.claude/skills/writing-rustdoc/references/style.md`      | whole | owned  | feature `agents`             |
| `.claude/skills/writing-rustdoc/references/templates.md`  | whole | owned  | template, feature `agents`   |
| `.claude/skills/writing-rustdoc/references/tooling.md`    | whole | owned  | template, feature `agents`   |
| `.claude/skills/writing-rustdoc/scripts/doc-audit.sh`     | whole | owned  | executable, feature `agents` |
| `.claude/skills/writing-rustdoc/scripts/doc-inventory.py` | whole | owned  | executable, feature `agents` |

## Features

| Feature  | Default | Enables |
| -------- | ------- | ------- |
| `strict` |         |         |
| `agents` |         |         |

## Recipes

- `check-rust-doc`: Builds every crate's documentation, private items included;
  a warning, broken links too, fails.

## Requires

- [`rust-toolchain`](../rust-toolchain/README.md)

<!-- /facts -->
