---
name: cutting-releases
description: Use when asked to cut, prepare or publish a release, choose its version, write its changelog or migration notes, or check that a release went out; when `release.yml` fails, or a tag, a changelog section or a GitHub Release is wrong.
---

# Cutting Releases

A release is a signed tag, `vX.Y.Z`, on the default branch, and pushing it
starts `release.yml`. The changelog, the versions and the migration notes are
prepared in a pull request, like any change; the tag's push is the one step that
cannot be taken back, so it is the maintainer's. RELEASE.md is the repository's
own account of the steps; this skill is how to carry them out.
{%- set project = devset.layers | selectattr("profile", "equalto", "project") | map(attribute="features") | first | default([]) %}
{%- set owner = repository | split("/") | first %}
{%- set repo = repository | split("/") | last %}
{%- if "agents" in project %}

A repository's first public release walks `preparing-a-release-for-open-source`
first: everything a stranger meets, and what only the owner can set.
{%- endif %}

## Rules

- **The version says what a user must do.** A breaking change makes a major
  release, or a minor one while the major version is 0; a feature makes a minor;
  fixes alone, a patch. A breaking commit has a `!` after its type, or a footer
  that starts `BREAKING CHANGE:`.
- **The changelog is written from the commits.** A wrong line is fixed by
  rewording its commit, never by editing CHANGELOG.md.
- **Every breaking change has a migration note** in BREAKING-CHANGES.md, under
  the version being cut, where the repository keeps that file: what changed,
  why, and what a user does about it.
- **The release commit is `chore(release): vX.Y.Z`**. It holds the migration
  notes and what `just release` wrote.
- **The maintainer signs and pushes the tag**, on the release commit, once it is
  on the default branch. A published release never changes, so a mistake in one
  is fixed by the next.
- **`release.yml` publishes.** Never run `just publish` by hand.

## Steps

1. **Find what changed** since the last tag:

   ```sh
   git describe --tags --abbrev=0
   git log --format='%h %s%n%b' <last-tag>..HEAD
   ```

2. **Choose the version** by the rule above, and say why.
3. **Branch** from the up-to-date default branch: `release/vX.Y.Z`.
4. **Write it**: `RELEASE_VERSION=X.Y.Z just release` runs every `release-*`
   recipe, which writes the changelog's section.
{%- if "cargo-bump" in devset.profiles %}

   It also sets every crate's version, and the lock's.
{%- endif %}
5. **Read the new section** as a user would. For a line that says too little,
   reword its commit, `git rebase -i <last-tag>`, then run step 4 again.
6. **Write the migration notes** for each breaking change.
7. **Check**: `just check`.
8. **Commit** `chore(release): vX.Y.Z`, and open a pull request; it lands once
   CI passes, as any change does.
9. **Hand over the tag.** Tell the maintainer to run, at the release commit on
   the default branch:

   ```sh
   git tag -s vX.Y.Z -m vX.Y.Z
   git push origin vX.Y.Z
   ```

10. **Check what the release made**, once its run is done, as the checks below
    say: a release ends when each page it made is opened, not when its run
    passes.

## What `release.yml` Does
{% if "cargo-binaries" in devset.profiles %}
- Builds what every `package-*` recipe packages on each platform, and attests
  every file.
{%- endif %}
- Publishes the GitHub Release, with the changelog's section as its notes.
{%- if "cargo-publish" in devset.profiles %}
- Publishes every crate to crates.io by trusted publishing: no token is stored.
  The job publishes only the versions crates.io lacks, so rerunning it finishes
  a publish that stopped halfway.
{%- endif %}

## Checks

Once the tag is pushed, `gh run watch` follows the release run, then each page
the release made is opened:

```sh
gh release view vX.Y.Z
{%- if "cargo-binaries" in devset.profiles %}
gh attestation verify <archive> --repo {{ repository }}
{%- endif %}
{%- if "cargo-publish" in devset.profiles %}
curl -fsS -A '{{ repository }} release check' https://crates.io/api/v1/crates/<crate>/X.Y.Z | jq .version.num
{%- endif %}
{%- if "mdbook" in devset.profiles %}
curl -fsS -o /dev/null https://{{ owner }}.github.io/{{ repo }}/
{%- endif %}
```

The Release has the section as its notes.
{%- if "cargo-binaries" in devset.profiles %}

Every archive is attached, with a `.sha256` beside it.
{%- endif %}
{%- if "cargo-publish" in devset.profiles %}

crates.io lists the new version of every crate, and each crate's page,
`https://crates.io/crates/<crate>`, shows its README, every image in it, and its
description, keywords, categories and homepage. docs.rs built each one:
`https://docs.rs/crate/<crate>/X.Y.Z/builds` shows the build succeeded.
{%- endif %}
{%- if "mdbook" in devset.profiles %}

The book is deployed from the default branch's last `check` run, and shows what
the release changed.
{%- endif %}
{%- if "agents" in project %}

After a first public release, `preparing-a-release-for-open-source`'s After the
Release opens every other page a stranger meets.
{%- endif %}

## What Not to Do

- Do not tag a commit that is not on the default branch, or before CI passes on
  it.
- Do not push, move or delete a tag without the maintainer.
- Do not edit CHANGELOG.md by hand.
- Do not run `just publish`; when the publish job fails, rerun the job.
