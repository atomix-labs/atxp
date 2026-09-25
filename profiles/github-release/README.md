# `github-release`

`release.yml` publishes a release from its tag, `v<version>`, after `just
release` has written the changelog and the versions and the tag is pushed. Where
the repository has a `package-*` recipe,
[`cargo-binaries`](../cargo-binaries/README.md)' for one, it runs `just package`
on linux-x64, linux-arm64 and macos-arm64, the platforms the locks cover; then
it publishes the GitHub Release, git-cliff's notes for the tag and every archive
attached. Without one, the Release has the notes alone.

A release builds uncached, and one runs at a time, never cancelled halfway. The
job that publishes holds the only write permission.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                            | Part  | Policy | Notes |
| ------------------------------- | ----- | ------ | ----- |
| `.github/workflows/release.yml` | whole | owned  |       |

## Requires

- [`just`](../just/README.md)
- [`git-cliff`](../git-cliff/README.md)

<!-- /facts -->
