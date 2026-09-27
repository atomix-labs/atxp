# `github-watch`

Every scheduled workflow watched: one that fails, stops running or is disabled
gets an issue.

```sh
devset add atxp/github-watch --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `github` · In [`rust`](../bundles/rust.md): always

A workflow nobody watches fails, or stops running, without anyone seeing: GitHub
drops scheduled runs under load and disables schedules in inactive repositories,
and neither makes a failure to notice. `watch` looks every hour at every
workflow with a schedule, as `.github/workflows/` declares it, so none needs
listing:

- one whose last scheduled run failed, or that has not run by twice the interval
  it keeps, or that is disabled, gets an issue named for it;
- the issue is commented on while that lasts, and closed when it recovers.

Issues carry the labels, issue type and assignees that
[`github-automation`](github-automation.md) sets in `.github/automation.json`.

## Owns

| File                          | Part  | Policy | Notes |
| ----------------------------- | ----- | ------ | ----- |
| `.github/workflows/watch.yml` | whole | owned  |       |
| `.github/scripts/watch.js`    | whole | owned  |       |

## Requires

- [`github-automation`](github-automation.md)
