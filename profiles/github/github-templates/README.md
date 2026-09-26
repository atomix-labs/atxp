# `github-templates`

GitHub's issue templates and pull request checklist, each written once where the
repository has none, and the repository's from then on. An issue is a bug report
or a feature request, never blank, and a vulnerability goes to GitHub's private
reporting instead. The checklist asks for a description, and, as the profiles
applied bring them, a Conventional Commit title
([`git-commits`](../../git/git-commits/README.md)), `just check` passing
([`just`](../../tooling/just/README.md)), and a breaking change's entry
([`project`](../../project/project/README.md)).

<!-- facts: written by devset-collection -->

## Owns

| File                                        | Part  | Policy | Notes    |
| ------------------------------------------- | ----- | ------ | -------- |
| `.github/ISSUE_TEMPLATE/bug_report.md`      | whole | once   |          |
| `.github/ISSUE_TEMPLATE/feature_request.md` | whole | once   |          |
| `.github/ISSUE_TEMPLATE/config.yml`         | whole | once   | template |
| `.github/pull_request_template.md`          | whole | once   | template |

## Variables

| Variable     | Default | Asks                              |
| ------------ | ------- | --------------------------------- |
| `repository` | none    | The GitHub repository, owner/name |

<!-- /facts -->
