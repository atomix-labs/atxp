# `github-watch`

A workflow nobody watches fails, or stops running, without anyone seeing: GitHub
drops scheduled runs under load and disables schedules in inactive repositories,
and neither makes a failure to notice. `watch` looks every hour at every
workflow with a schedule, as `.github/workflows/` declares it, so none needs
listing:

- one whose last run on the default branch failed, on schedule or by hand, or
  that has not run on schedule by twice the interval it keeps, or that is
  disabled, gets an issue named for it;
- the issue hears of each new failure once, and closes when the workflow
  recovers. A run by hand after a fix is a recovery, so a weekly workflow's
  issue closes at the watch's next run, not the next week.

Issues carry the labels, issue type and assignees that
[`github-automation`](../../github/github-automation/README.md) sets in
`.github/automation.json`.

<!-- facts: written by devset-collection -->

## Owns

| File                          | Part  | Policy | Notes |
| ----------------------------- | ----- | ------ | ----- |
| `.github/workflows/watch.yml` | whole | owned  |       |
| `.github/scripts/watch.js`    | whole | owned  |       |

## Requires

- [`github-automation`](../github-automation/README.md)

<!-- /facts -->
