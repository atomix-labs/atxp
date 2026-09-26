# `github-workflow-lint`

actionlint checks every GitHub Actions workflow: its syntax, the types in its
expressions, and, where [`shellcheck`](../../lang/shell/README.md) is applied too,
the shell in each `run:` step. It checks correctness;
[`zizmor`](../../github/zizmor/README.md) checks security.

`.github/actionlint.yaml` names the self-hosted runners a workflow may run on,
from `runner_labels`; actionlint takes a label it does not know for a typo. A
workflow that picks its runner from the repository variable `CI_RUNNER`, as the
CI profiles do, needs none.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                         | Part  | Policy | Notes    |
| -------------------------------------------- | ----- | ------ | -------- |
| `.github/actionlint.yaml`                    | whole | owned  | template |
| `.just/github-workflow-lint.just`                      | whole | owned  |          |
| `.config/mise/conf.d/devset-github-workflow-lint.toml` | whole | owned  |          |
| `.config/mise/mise.lock`                     | keys  | owned  |          |

## Recipes

- `check-github-workflow-lint`: Checks every workflow: syntax, expressions, and the shell
  in each step.

## Variables

| Variable        | Default | Asks                                                          |
| --------------- | ------- | ------------------------------------------------------------- |
| `runner_labels` | empty   | Self-hosted runner labels actionlint accepts, comma-separated |

<!-- /facts -->
