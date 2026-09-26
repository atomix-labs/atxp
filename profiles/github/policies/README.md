# `policies`

Rules for GitHub Actions workflows, in Rego, which
[`conftest`](../../github/conftest/README.md) holds beside what
[`actionlint`](../../github/github-workflow-lint/README.md) and [`zizmor`](../../github/zizmor/README.md)
check:

- every job sets `timeout-minutes`, so a hung one cannot hold a runner for six
  hours; a call to a reusable workflow is exempt;
- every workflow states `permissions`, as the repository default grants more
  than any job needs;
- no job output or `github-script` step output is named `result`, which reads as
  the job's or step's own outcome and is not.

Each rule has its tests, run by `conftest verify`.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                   | Part  | Policy | Notes |
| -------------------------------------- | ----- | ------ | ----- |
| `policy/workflows/workflows.rego`      | whole | owned  |       |
| `policy/workflows/workflows_test.rego` | whole | owned  |       |

<!-- /facts -->
