# Releasing

How a release of atxp is cut: what its version says, and the steps from the
default branch to a tag. [CHANGELOG.md](CHANGELOG.md) is its record.

## Versions

A tag versions every profile at once, `vX.Y.Z` under semantic versioning. While
the major version is 0, a minor release may break a repository that takes it,
and a patch release never does. [CONTRIBUTING.md](CONTRIBUTING.md) says what
counts as breaking.

## Steps

1. Check that every breaking commit since the last tag has its entry in
   [BREAKING-CHANGES.md](BREAKING-CHANGES.md), under the version about to be
   tagged.
2. Write what the release changes:

   ```sh
   RELEASE_VERSION=x.y.z just release
   ```

   Every `release-*` recipe runs: `release-git-cliff` writes `CHANGELOG.md` from
   the commits since the last tag, in a Rust repository `release-cargo-bump`
   sets every crate's version, and atxp's own `release-readme` points the
   README's quick start at the new tag.
3. Read the new section; fix a commit's subject by rewording the commit, not the
   file.
4. Commit it as `chore(release): vx.y.z`, which the changelog leaves out; sign
   the tag, `git tag -s vx.y.z`; push the branch and the tag.
5. The tag starts `release.yml`: it builds what every `package-*` recipe
   packages on linux-x64, linux-arm64 and macos-arm64, then publishes the GitHub
   Release with the release's section as its notes and every archive attached.
   atxp packages nothing, so its Release has notes alone.

A repository takes the release with `devset update`, or pins it with `devset
init --tag vx.y.z`.
