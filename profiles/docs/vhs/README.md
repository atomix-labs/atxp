# `vhs`

The README's demo, recorded by [VHS](https://github.com/charmbracelet/vhs) from
tapes: each a terminal session written as the keys to type and the output to
wait for, played and filmed in a real terminal. Each tape in `docs/demo/`
records one GIF into `docs/src/media/`, so a demo made for a dark page and one
made for a light page play the same session, `docs/demo/parts/demo.tape`, each
in its own colours.

On each release's tag, and on demand, the `demo` workflow records every tape
again, with the repository's own tools, and opens a pull request with the
recordings that changed, in one commit GitHub signs, labelled `documentation`
and assigned to the `assignees`
[`github-automation`](../../github/github-automation/README.md) names. A tape
that waits for output which no longer comes fails the workflow, so a demo does
not show a project as it used to be. A person merges it; with the feature
`merge`, off unless the repository turns it on, the workflow merges it itself,
every tape having played to its end, and says so on it.

GitHub lets a workflow open pull requests only where the repository allows it:
Settings, Actions, General, Workflow permissions. A pull request the workflow's
own token opens has its checks held until a maintainer approves them, so `merge`
merges on the recording alone, its commit skipping them. With the automation's
GitHub App, the variable `BUMP_APP_ID` and the secret `BUMP_APP_KEY` the weekly
bump uses too, the pull request runs the repository's checks, and GitHub's
auto-merge merges it once they pass: the way through a default branch whose
rules require them.

Where the repository has no tape, it scaffolds a pair, dark and light, and a
session to replace with the project at work. They are the repository's from then
on. A README started from [`project`](../../project/project/README.md) shows the
demo under its header, as a `<picture>` that follows the reader's theme:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/src/media/demo-dark.gif">
  <img alt="What the demo shows, in one sentence" src="docs/src/media/demo-light.gif" width="720">
</picture>
```

To record by hand, from the repository's root, with VHS, ttyd and ffmpeg
installed: `for tape in docs/demo/*.tape; do vhs "$tape"; done`.

<!-- facts: written by devset-collection -->

## Owns

| File                         | Part  | Policy | Notes           |
| ---------------------------- | ----- | ------ | --------------- |
| `.github/workflows/demo.yml` | whole | owned  |                 |
| `.github/scripts/demo.js`    | whole | owned  |                 |
| `docs/demo/demo-dark.tape`   | whole | once   | scaffold `demo` |
| `docs/demo/demo-light.tape`  | whole | once   | scaffold `demo` |
| `docs/demo/parts/demo.tape`  | whole | once   | scaffold `demo` |

## Features

| Feature | Default | Enables |
| ------- | ------- | ------- |
| `merge` |         |         |

## Requires

- [`github-automation`](../../github/github-automation/README.md)

<!-- /facts -->
