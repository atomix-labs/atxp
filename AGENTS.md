# Working in `atxp`

atxp is a collection of devset profiles for Rust repositories, released together
under one tag. [ARCHITECTURE.md](ARCHITECTURE.md) says how the profiles are
built and compose, and [CONTRIBUTING.md](CONTRIBUTING.md) the rules each keeps.

<!-- >>> devset: agents >>> -->

## Before You Commit

Run `just check`: CI runs the same checks, and names each that fails. `just fix`
fixes what a formatter or linter can, and `just --list` shows every recipe.

## Managed Files

Profiles, applied by devset, manage some of the files here. `devset status`
names each, and whether a local change to it is kept or is drift; `devset
explain <file>` says which profile owns what in it. What a profile owns changes
with the profile, on `devset update`. Never edit `.devset/`.

<!-- <<< devset: agents <<< -->

## The Repository

```text
profiles/<group>/<name>/  every profile: profile.toml, README.md, files/
tests/fixtures/           the repositories the suite applies the profiles to
tests/bundle.sh           the bundle applied to nothing, with the features given
scripts/                  atxp's own tools
.just/, .github/          written by the profiles atxp applies to itself
```

## Changing a Profile

- A profile's payloads under `files/` are templates, which `just check` never
  renders; `just test` does, so run it after changing one.
- `just fix-devset-collection` writes the catalog in the README and every
  profile's facts; they are never edited by hand.
- The `authoring-devset-profiles` skill has the design questions and the rules
  an agent needs; CONTRIBUTING.md is the whole account.
- A change a repository must act on is breaking. Its commit adds `!` after the
  scope and a footer that says what to do, and it adds its entry to
  [BREAKING-CHANGES.md](BREAKING-CHANGES.md).

## Releases

[RELEASE.md](RELEASE.md) has the steps, which the `cutting-releases` skill
carries out. Pushing the tag is the maintainer's.

<!-- >>> devset: git-commits >>> -->

## Commits

`just check-git-commits` holds every commit of a branch to Conventional Commits:
`type(scope): subject`, the subject imperative and lower case, with no closing
period, since it is the line the changelog shows. A breaking change adds `!`
after the scope, and a footer that starts `BREAKING CHANGE:` and says what to
do.

<!-- <<< devset: git-commits <<< -->
