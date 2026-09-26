# `github-watch`

A workflow nobody watches fails, or stops running, without anyone seeing: GitHub
drops scheduled runs under load and disables schedules in inactive repositories,
and neither makes a failure to notice. `watch` looks every hour at every
workflow with a schedule, as `.github/workflows/` declares it, so none needs
listing:

- one whose last scheduled run failed, or that has not run by twice the interval
  it keeps, or that is disabled, gets an issue named for it;
- the issue is commented on while that lasts, and closed when it recovers.

Issues carry the labels, issue type and assignees that
[`github-automation`](../../github/github-automation/README.md) sets in
`.github/automation.json`.

<!-- facts: written by devset-collection -->

## Owns

| File                          | Part  | Policy | Notes |
| ----------------------------- | ----- | ------ | ----- |
| `.github/workflows/watch.yml` | whole | owned  |       |
| `.github/scripts/watch.js`    | whole | owned  |       |
| `.github/scripts/issue.js`    | whole | owned  |       |

## Requires

- [`github-automation`](../github-automation/README.md)

<!-- /facts -->
