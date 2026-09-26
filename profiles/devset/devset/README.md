# `devset`

devset itself, pinned through mise, so every machine and every CI job applies
the profiles with one release, which a release of the collection moves.
`check-devset` runs `devset status --exit-code`, so a file that has drifted from
its profile, or an update left unfinished, fails the checks, in CI as a job of
its own.

<!-- facts: written by devset-collection -->

## Owns

| File                                     | Part  | Policy | Notes |
| ---------------------------------------- | ----- | ------ | ----- |
| `.just/devset.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-devset.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                 | keys  | owned  |       |

## Recipes

- `check-devset`: Fails when a file devset manages has drifted from its profile,
  or an update is unfinished.

## Requires

- [`mise`](../../tooling/mise/README.md)

<!-- /facts -->
