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
2. Write the changelog's section for the release:

   ```sh
   RELEASE_VERSION=x.y.z just release
   ```

   `release-git-cliff` writes `CHANGELOG.md` from the commits since the last
   tag.
3. Read the new section; fix a commit's subject by rewording the commit, not the
   file.
4. Commit it as `chore(release): vx.y.z`, which the changelog leaves out; tag
   the commit `vx.y.z`; push the branch and the tag.
5. Publish the GitHub Release for the tag, its notes the release's section:

   ```sh
   git cliff --latest --strip header
   ```

A repository takes the release with `devset update`, or pins it with `devset
init --tag vx.y.z`.
