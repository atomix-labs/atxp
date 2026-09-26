# `agents`

What a coding agent reads before it changes the repository. AGENTS.md, which
every agent that follows the format reads, is started where the repository has
none, with a heading for what the repository is and one for its rules, both the
repository's to write. Its managed block says how to check a change, and which
files devset manages. CLAUDE.md, scaffolded where there is none, imports
AGENTS.md for Claude Code and says where the skills are.

`.claude/settings.json` holds Claude Code's permissions as keys, under `merge`,
so the repository keeps its own beside them. An agent may run every `check-*`
and `fix-*` recipe, `just --list`, and devset's commands that only read, without
asking. It may never run `just publish`, which no release can take back, or
`just bump`, the weekly workflow's; `just release`, which only writes, asks
first.

With `hook`, the default, a Stop hook runs `just check` before the agent stops,
on a tree that differs from `HEAD`, and its failures keep the agent at work.
Once it has blocked, the agent may stop if nothing changed since, so a failure
it cannot fix never loops.

Skills come with the profiles they teach, each under that profile's `agents`
feature; the bundle [`rust`](../../bundles/rust/README.md)'s `agents` turns on
this profile and every skill.

<!-- facts: written by devset-collection -->

## Owns

| File                     | Part  | Policy | Notes                      |
| ------------------------ | ----- | ------ | -------------------------- |
| `AGENTS.md`              | block | owned  | template                   |
| `CLAUDE.md`              | whole | once   | scaffold `claude`          |
| `.claude/settings.json`  | keys  | merge  | template                   |
| `.claude/hooks/check.sh` | whole | owned  | executable, feature `hook` |

## Features

| Feature | Default | Enables |
| ------- | ------- | ------- |
| `hook`  | yes     |         |

## Requires

- [`just`](../../tooling/just/README.md)

<!-- /facts -->
