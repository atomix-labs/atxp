# `github-release`

`release.yml` publishes a release from its tag, `v<version>`, after `just
release` has written the changelog and the versions and the tag is pushed. Where
the repository has a `package-*` recipe,
[`cargo-binaries`](../../cargo/cargo-binaries/README.md)' for one, it runs `just package`
on linux-x64, linux-arm64 and macos-arm64, the platforms the locks cover; then
it attests every archive and publishes the GitHub Release, git-cliff's notes for
the tag and every archive attached. Without one, the Release has the notes
alone. Anyone can check an archive's build provenance with `gh attestation
verify <archive> --repo <owner>/<repository>`.

Where the repository has a `publish-*` recipe, the job `publish` then runs `just
publish`, which puts the release in a registry. Where
[`cargo-publish`](../../cargo/cargo-publish/README.md) is applied too, the job
first takes a crates.io token by trusted publishing, good for 30 minutes and
revoked when the job ends, so the repository stores none. That job runs in the environment `release`, which the
trusted publisher names, and holds the only `id-token` permission.

A release builds uncached, and one runs at a time, never cancelled halfway. The
job that creates the GitHub Release holds the only write permissions, and signs
the attestations; the jobs that build hold neither.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                            | Part  | Policy | Notes |
| ------------------------------- | ----- | ------ | ----- |
| `.github/workflows/release.yml` | whole | owned  |       |

## Requires

- [`just`](../../tooling/just/README.md)
- [`git-changelog`](../../git/git-changelog/README.md)

<!-- /facts -->
