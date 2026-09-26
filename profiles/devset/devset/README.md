# `devset`

devset itself, pinned through mise, so every machine and every CI job applies
the profiles with one release, which a release of the collection moves.
`check-devset` runs `devset status --exit-code`, so a file that has drifted from
its profile, or an update left unfinished, fails the checks, in CI as a job of
its own.

`bump-devset`, in the weekly bump, moves each source the target names by a tag
on GitHub to its newest release that is at least three days old, never
backwards, then runs `devset update`, which merges what the release changed with
the repository's own edits. An update that conflicts is taken back, with `devset
update --abort`, and the bump says so; a source elsewhere is named as unchecked.

The `agents` feature adds the `using-devset` skill in `.claude/skills/`: how an
agent changes a file devset manages, turns on a feature, and resolves an update
that conflicts.

<!-- facts: written by devset-collection -->

## Owns

| File                                     | Part  | Policy | Notes            |
| ---------------------------------------- | ----- | ------ | ---------------- |
| `.just/devset.just`                      | whole | owned  |                  |
| `.just/devset.py`                        | whole | owned  |                  |
| `.config/mise/conf.d/devset-devset.toml` | whole | owned  |                  |
| `.config/mise/mise.lock`                 | keys  | owned  |                  |
| `.claude/skills/using-devset/SKILL.md`   | whole | owned  | feature `agents` |

## Features

| Feature  | Default | Enables |
| -------- | ------- | ------- |
| `agents` |         |         |

## Recipes

- `check-devset`: Fails when a file devset manages has drifted from its profile,
  or an update is unfinished.
- `bump-devset`: Moves each source the target names by tag to its newest release
  past the cooldown, and applies it.

## Requires

- [`mise`](../../tooling/mise/README.md)

<!-- /facts -->
