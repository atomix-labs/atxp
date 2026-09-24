# `automation-house`

The house's settings for the collection's GitHub automation, as keys of
`.github/automation.json`: issues for failures are labelled `bug` and typed Bug,
the weekly bump's `dependencies` and Task, and assigned; the bump opens a pull
request, `bump.mode = "pr"`; and a night with no new commit is skipped.

Under `merge`, so a repository may change its mode or its assignees. It names
the house's own runner, `ubuntu-arm-latest`, to actionlint in
`.github/actionlint.yaml`.
