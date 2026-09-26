# `github-workflow-lint`

Every GitHub Actions workflow checked, by three tools, each a feature on by
default; `check-github-workflow-lint` runs the ones that are on, and names each
as it goes.

- `actionlint` checks each workflow's syntax, the types in its expressions, and,
  where [`shell`](../../lang/shell/README.md) is applied too, the shell in each
  `run:` step. `.github/actionlint.yaml` names the self-hosted runners a
  workflow may run on, from `runner_labels`; actionlint takes a label it does
  not know for a typo. A workflow that picks its runner from the repository
  variable `CI_RUNNER`, as the CI profiles do, needs none.
- `zizmor` audits every workflow, action and Dependabot configuration the
  repository owns for security: template injection, dangerous triggers, broad
  permissions, credentials left in a checkout, and more. It runs offline, with
  `.github/zizmor.yml`, needing no token.
- `policies` holds the workflows and actions under `.github/` to rules in Rego,
  in `policy/`, with conftest, after running the rules' own tests. The profile
  brings the rules for workflows: every job sets `timeout-minutes`, so a hung
  one cannot hold a runner for six hours, a call to a reusable workflow exempt;
  every workflow states `permissions`, as the repository default grants more
  than any job needs; and no job output or `github-script` step output is named
  `result`, which reads as the job's or step's own outcome and is not. A
  repository adds its own rules beside them.

A file `.gitattributes` marks `linguist-vendored` or `linguist-generated` is
someone else's and is left out.

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
