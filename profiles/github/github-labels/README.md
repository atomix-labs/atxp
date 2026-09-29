# `github-labels`

A label gets used when a form or a bot sets it, and rarely when it waits for a
person, so this profile keeps few, and sets most of them itself. An issue's kind
is its type and a pull request's is its title's, so no label repeats either.

`.github/labels.toml` holds the labels, and the `labels` workflow keeps GitHub's
as it says on every change to it on `main`. The profile owns seven, as keys:

| Label              | Means                                       | Set by                         |
| ------------------ | ------------------------------------------- | ------------------------------ |
| `triage`           | new, and yet to be looked at                | the issue forms                |
| `waiting`          | on someone else: the reporter, or upstream  | a maintainer                   |
| `good first issue` | a small change, well described, to start on | a maintainer                   |
| `help wanted`      | accepted, and open to anyone                | a maintainer                   |
| `breaking`         | changes what users rely on                  | the workflow, from a title `!` |
| `dependencies`     | moves a pinned tool, action or crate        | the bump, Dependabot           |
| `automation`       | opened by a workflow                        | the automation                 |

The forms come from
[`github-templates`](../../github/github-templates/README.md), the labels of the
bump, the watch and the demo from
[`github-automation`](../../github/github-automation/README.md), and
Dependabot's from
[`github-dependabot`](../../github/github-dependabot/README.md).

The repository adds its own beside them. One with `paths` is an area, which the
workflow sets on a pull request that changes a file it matches, and takes off
one that no longer does:

```toml
[labels."area: docs"]
color       = "c5def5"
description = "The manual and the README"
paths       = ["docs/**", "*.md"]
```

- **`[retired]`** names a label to remove, with the issue type its issues take
  first. GitHub's first labels are retired: types say the kind, Discussions take
  questions, and closing says duplicate or not planned. A label the file does
  not name is reported, and kept.
- **Fork pull requests are labelled too**: the workflow runs on
  `pull_request_target` and checks out nothing of the pull request, whose title
  and files come from the API.
- **`check-github-labels`** holds the file to GitHub's limits, and fails where a
  form, `.github/automation.json` or `.github/dependabot.yml` names a label it
  does not hold, or retires.
- **CONTRIBUTING.md** gains a Labels section with the table, linking what awaits
  triage and the good first issues.

<!-- facts: written by devset-collection -->

## Owns

| File                            | Part  | Policy | Notes                              |
| ------------------------------- | ----- | ------ | ---------------------------------- |
| `.github/labels.toml`           | keys  | merge  |                                    |
| `.github/workflows/labels.yml`  | whole | owned  |                                    |
| `.just/github-labels.just`      | whole | owned  |                                    |
| `.just/github-labels/labels.py` | whole | owned  |                                    |
| `CONTRIBUTING.md`               | block | owned  | template, `CONTRIBUTING.md` exists |

## Recipes

- `check-github-labels`: Checks .github/labels.toml, and that the forms, the
  automation and Dependabot name only its labels.

## Variables

| Variable     | Default | Asks                              |
| ------------ | ------- | --------------------------------- |
| `repository` | none    | The GitHub repository, owner/name |

## Requires

- [`just`](../../tooling/just/README.md)

<!-- /facts -->
