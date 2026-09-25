# Contributing

How to report a problem, and how to change atxp: the commit convention, what
counts as breaking, the rules every profile keeps, how its documents are
written, and the checks to run. [ARCHITECTURE.md](ARCHITECTURE.md) says how the
profiles fit together.

## Reporting Issues

Open an issue with the template that fits: a **bug report** names the profile,
devset's version, what happened and how to reproduce it; a **profile request**
names the tool, why, and what the profile would own. A bug in devset itself
belongs in [devset's repository](https://github.com/atomix-labs/devset/issues).

## Pull Requests

Keep each pull request to one change: a profile, a fix, or a refactor, not a mix
of them.

Commits follow [Conventional Commits](https://www.conventionalcommits.org),
which `check-committed` holds every commit of a branch to:

```text
type(scope): subject
```

- The **type** is `feat`, `fix`, `refactor`, `docs`, `perf`, `test`, `build`,
  `ci`, `chore`, `style` or `revert`.
- The **scope** is the profile the commit changes, `feat(taplo): …`, or the part
  of the repository that is not a profile: `catalog`, `suite`, `docs`, `ci` or
  `release`.
- The **subject** is imperative, lower case, with no closing period: it is the
  line the changelog shows, so it says what changed for someone reading it
  there.
- A breaking change adds `!` after the scope, and a `BREAKING CHANGE:` footer
  saying what to do.

A change is **breaking** when a repository that takes it must act: a profile, a
file or a variable removed or renamed; a scope or a policy changed; a check that
fails a build it passed; a higher minimum version of a tool. A breaking change
also adds its entry to [BREAKING-CHANGES.md](BREAKING-CHANGES.md), under the
release that will carry it.

Run `just check` and `just test-profiles` before pushing: CI runs the same.

## Changing a Profile

`check-catalog` holds every profile to these rules.

- It lives in `profiles/<id>/`, and `[profile] name` is `<id>`.
- Its `description` is one line, with no closing period; the catalog shows it.
- It has no `version`: atxp's tag is its version.
- Its `README.md` opens with ``# `<id>` ``, then says in prose what the profile
  does and why, and what stays the repository's. Below that is its facts block,
  which `just fix-catalog` writes.
- It requires another profile only when it cannot work without it, and names it
  as a sibling path.

An atom owns one tool:

- its configuration;
- its pin, in `.config/mise/conf.d/devset-<id>.toml`, named so that no tool
  reads it as its own configuration, with its entries in
  `.config/mise/mise.lock` owned as keys, and locked for `linux-arm64`,
  `linux-x64` and `macos-arm64` by `just bump-profile-pins`, a static build on
  Linux where the release has one;
- its recipes, in `.just/<id>.just`, each named for a verb, `check-<id>` and the
  like, with any helper beside them as `.just/<id>.<ext>`.

Where a repository adds to a shared file, a profile owns only its part: `scope =
"keys"` for TOML, JSON and YAML, `scope = "block"` for line formats. A value
repositories choose is a variable, with a default unless every repository's
answer differs, as the repository's name does.

Its payloads pass every check the profiles bring, in the layout their formatters
give: `just test-profiles` applies every profile at once and runs `just check`.

The bundle, `rust`, only requires, and names its profiles as sibling paths.

## Writing

Every document here keeps these rules.

- A document opens with one paragraph saying what it is for.
- A fact lives in one document; the others link to it.
- Explanation is plain statement, in the present tense; a step to follow is an
  imperative.
- Headings are in title case, one H1 a file.
- Markdown is wrapped at 80, with no em dashes.
- Identifiers are in backticks; a profile's id is linked where a document first
  names it.
- A long document collects its link targets at the bottom.
- A generated region is marked by comments that name what writes it.

## Checks

```sh
just check              # atxp's own checks, as CI runs them
just test-profiles      # the bundle on each fixture, every profile alone and all at once
just fix-catalog        # after changing a profile: the tables, every profile's facts, the spine's imports
just bump-profile-pins  # after changing a pin: its lock entries, for every platform
```

`just test-profiles` needs devset, or its path in `$DEVSET`, and the tools mise
pins.
