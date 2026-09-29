# `github-templates`

GitHub's issue forms and pull request checklist, each written once where the
repository has none, and the repository's from then on. An issue is a bug report
or a feature request, never blank, each a form whose required fields hold what a
maintainer needs, typed Bug or Feature and labelled `triage`, which
[`github-labels`](../../github/github-labels/README.md) keeps. A vulnerability
goes to GitHub's private reporting instead; with `discussions`, a question goes
to the repository's Discussions, and where
[`mdbook`](../../docs/mdbook/README.md) is applied, the book is linked before
any of them. A repository adds its own fields to its forms, such as the output
of its tool's `--version`. The checklist asks for a description, and, as the
profiles applied bring them, a Conventional Commit title
([`git-commits`](../../git/git-commits/README.md)), `just check` passing
([`just`](../../tooling/just/README.md)), and a breaking change's entry
([`project`](../../project/project/README.md)).

<!-- facts: written by devset-collection -->

## Owns

| File                                         | Part  | Policy | Notes    |
| -------------------------------------------- | ----- | ------ | -------- |
| `.github/ISSUE_TEMPLATE/bug_report.yml`      | whole | once   |          |
| `.github/ISSUE_TEMPLATE/feature_request.yml` | whole | once   |          |
| `.github/ISSUE_TEMPLATE/config.yml`          | whole | once   | template |
| `.github/pull_request_template.md`           | whole | once   | template |

## Features

| Feature       | Default | Enables |
| ------------- | ------- | ------- |
| `discussions` |         |         |

## Variables

| Variable     | Default | Asks                              |
| ------------ | ------- | --------------------------------- |
| `repository` | none    | The GitHub repository, owner/name |

<!-- /facts -->
