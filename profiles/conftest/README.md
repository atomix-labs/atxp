# `conftest`

conftest holds configuration to policies written in Rego, in `policy/`, and runs
their own tests first, `conftest verify`. The policies see every workflow and
action under `.github/` together, so one can compare them;
[`policies`](../policies/README.md) brings the ones for workflows.

Where there is no `policy/`, there is nothing to check.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                       | Part  | Policy | Notes |
| ------------------------------------------ | ----- | ------ | ----- |
| `.just/conftest.just`                      | whole | owned  |       |
| `.config/mise/conf.d/devset-conftest.toml` | whole | owned  |       |
| `.config/mise/mise.lock`                   | keys  | owned  |       |

## Recipes

- `check-conftest`: Tests the policies, then holds every workflow and action to
  them.

<!-- /facts -->
