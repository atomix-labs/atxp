# `github-release`

A release from its tag: every package-* recipe on each platform, then the GitHub
Release with its notes.

```sh
devset add atxp/github-release --git https://github.com/atomix-labs/atxp --tag <release>
```

Group `github` · In [`rust`](../bundles/rust.md): with `publish` · In
[`rust`](../bundles/rust.md): with `binaries`

`release.yml` publishes a release from its tag, `v<version>`, after `just
release` has written the changelog and the versions and the tag is pushed. Where
the repository has a `package-*` recipe,
[`cargo-binaries`](../cargo/cargo-binaries.md)' for one, it runs `just package`
on linux-x64, linux-arm64 and macos-arm64, the platforms the locks cover; then
it attests every archive and publishes the GitHub Release, its notes and every
archive attached. Without one, the Release has the notes alone. Anyone can check
an archive's build provenance with `gh attestation verify <archive> --repo
<owner>/<repository>`.

The notes are `.github/release-notes.md`, the repository's, with the release in
it: `{version}` and `{tag}` take the release's, and the line `<!-- changes -->`
takes its changes, git-cliff's section for the tag without its heading, which
the release's title says already. A release with a breaking change opens its
changes with a callout linking its migration in `BREAKING-CHANGES.md`. The file
is scaffolded once, `description` above the changes, for the repository to add
what a reader needs around them, such as how to install or verify the release;
without it, the notes are the changes alone. `check-github-release` renders the
next release's notes on every change, so a file that lost its `<!-- changes -->`
line fails before a tag needs it.

Where the repository has a `publish-*` recipe, the job `publish` then runs `just
publish`, which puts the release in a registry. Where
[`cargo-publish`](../cargo/cargo-publish.md) is applied too, the job first takes
a crates.io token by trusted publishing, good for 30 minutes and revoked when
the job ends, so the repository stores none. That job runs in the environment
`release`, which the trusted publisher names, and holds the only `id-token`
permission.

Where the repository has no `RELEASE.md`, it scaffolds one, written for the
profiles applied: the versions, what a release ships, and the steps from `just
release` to a published, verified release. It is the repository's from then on.

A release builds uncached, and one runs at a time, never cancelled halfway. The
job that creates the GitHub Release holds the only write permissions, and signs
the attestations; the jobs that build hold neither.

The `agents` feature adds the `cutting-releases` skill in `.claude/skills/`:
choosing the version, the release's pull request, and checking the published
release. The tag stays the maintainer's to push.

## Owns

| File                                       | Part  | Policy | Notes                        |
| ------------------------------------------ | ----- | ------ | ---------------------------- |
| `RELEASE.md`                               | whole | once   | template, scaffold `release` |
| `.github/workflows/release.yml`            | whole | owned  | template                     |
| `.github/release-notes.md`                 | whole | once   | template, scaffold `notes`   |
| `.just/github-release.just`                | whole | owned  | template                     |
| `.just/github-release/notes.py`            | whole | owned  |                              |
| `.claude/skills/cutting-releases/SKILL.md` | whole | owned  | template, feature `agents`   |

## Features

| Feature  | Default | Enables |
| -------- | ------- | ------- |
| `agents` |         |         |

## Recipes

- `check-github-release`: Renders the next release's notes from
  .github/release-notes.md and the changes, as a release will.

## Variables

| Variable      | Default | Asks                              |
| ------------- | ------- | --------------------------------- |
| `repository`  | none    | The GitHub repository, owner/name |
| `description` | empty   | One line: what the project is     |

## Requires

- [`git-changelog`](../git/git-changelog.md)
- [`just`](../tooling/just.md)
