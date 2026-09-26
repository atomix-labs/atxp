# Contributing

How to report a problem, and how to change atxp: the commit convention, what
counts as breaking, the rules every profile and skill keeps, how its documents
are written, and the checks to run. [ARCHITECTURE.md](ARCHITECTURE.md) says how
the profiles fit together.

## Reporting Issues

Open an issue with the template that fits: a **bug report** names the profile,
devset's version, what happened and how to reproduce it; a **profile request**
names the tool, why, and what the profile would own. A bug in devset itself
belongs in [devset's repository](https://github.com/atomix-labs/devset/issues).

## Pull Requests

Keep each pull request to one change: a profile, a fix, or a refactor, not a mix
of them.

Run `just check` and `just test` before pushing: CI runs the same.

<!-- >>> devset: git-commits >>> -->

## Commits

Commits follow [Conventional Commits](https://www.conventionalcommits.org),
which `just check-git-commits` holds every commit of a branch to:

```text
type(scope): subject
```

- The **type** is `feat`, `fix`, `refactor`, `docs`, `perf`, `test`, `build`,
  `ci`, `chore`, `style` or `revert`.
- The **subject** is imperative, lower case, with no closing period: it is the
  line the changelog shows.
- A breaking change adds `!` after the scope, and a `BREAKING CHANGE:` footer
  saying what to do.

<!-- <<< devset: git-commits <<< -->

A commit's scope is the profile it changes, `feat(toml): …`, or the part of the
repository that is not a profile: `docs`, `ci`, `tests` or `release`. A change
across several profiles has no scope.

A change is **breaking** when a repository that takes it must act: a profile, a
file or a variable removed or renamed; a scope or a policy changed; a check that
fails a build it passed; a higher minimum version of a tool. A breaking change
also adds its entry to [BREAKING-CHANGES.md](BREAKING-CHANGES.md), under the
release that will carry it.

## Designing Profiles

A profile is to a repository what a crate is to a program: a unit it adopts,
updates or removes whole. Each part of a collection has its analogue:

| Unit                 | Crate analogy       | Use it for                                                  |
| -------------------- | ------------------- | ----------------------------------------------------------- |
| Source               | workspace, registry | profiles released together under one ref                    |
| Profile              | crate               | a concern a repository adopts, updates or removes as a unit |
| Feature              | cargo feature       | an optional, additive capability of that concern            |
| Variable             | configuration value | a value per repository, or a choice between alternatives    |
| Requirement          | dependency          | a concern this one cannot work without                      |
| Optional requirement | optional dependency | a capability that needs another concern                     |
| Bundle               | facade crate        | only requirements, with features for the kind of project    |
| Scaffold             | a template          | starter content that becomes the project's once written     |
| Managed entry        | a dependency's code | content that stays in sync with the source                  |

Where something belongs, the questions decide, in order:

1. Would a repository want one without the other? Then two profiles; if they
   always go together and edit the same files, one.
2. Would turning it on remove or replace something? Then a variable, not a
   feature.
3. Does the description join unrelated things with "and"? Then two profiles.
4. Does it only make sense with its concern? Then a feature of that concern.
5. Is it content the project will own and change? Then a scaffold; content that
   must follow the source is managed.
6. Names are API: removing a profile, a feature or a variable is a breaking
   change.

## Changing a Profile

`check-devset-collection` holds every profile to these rules.

- It lives in `profiles/<umbrella>/<name>/`, and `[profile] name` is `<name>`,
  unique in atxp.
- Its `description` is one line, with no closing period; the catalog shows it.
- It has no `version`: atxp's tag is its version.
- Its `README.md` opens with ``# `<name>` ``, then says in prose what the
  profile does and why, and what stays the repository's. Below that is its facts
  block, which `just fix-devset-collection` writes.
- It requires another profile, by name in `[requires]`, only when it cannot work
  without it; one it needs only for a feature is optional, turned on by that
  feature's `dep:`.
- A variable several profiles declare, each declares alike: one prompt, one
  default.

A profile owns one concern, and with it:

- its configuration;
- its tools' pins, in `.config/mise/conf.d/devset-<name>.toml`, named so that no
  tool reads it as its own configuration, with their entries in
  `.config/mise/mise.lock` owned as keys and locked for `linux-arm64`,
  `linux-x64` and `macos-arm64`, a static build on Linux where the release has
  one; a tool one feature brings is gated by it in both files;
- its recipes, in `.just/<name>.just`, each `<verb>-<name>`, one recipe a verb
  that runs each tool its features turn on, with any helper as
  `.just/<name>.<ext>` or under `.just/<name>/`;
- its output, ignored in a block of `.gitignore`.

Where a repository adds to a shared file, a profile owns only its part: `scope =
"keys"` for TOML, JSON and YAML, `scope = "block"` for line formats. A list
several profiles add to is one value, so its owner renders it from the graph,
`devset.profiles`, and no profile edits another's. A value repositories choose
is a variable, with a default unless every repository's answer differs, as the
repository's name does.

A feature only adds. What goes beyond the defaults any open-source project can
take, the house policy, is the feature `strict`, which the bundle turns on for
all three profiles that have one.

Its payloads pass every check the profiles bring, in the layout their formatters
give: `just test` applies each profile alone, with its default features and with
every feature, then runs `just check` on each fixture for the bundle with no
features and for every profile at once with every feature.

The bundle, `rust`, only requires: the core every Rust repository has, and the
rest as optional requirements its features turn on.

### Skills

A skill ships with the profile whose concern it serves, in
`.claude/skills/<skill>/`, each of its files gated by that profile's `agents`
feature. `check-devset-collection` holds each to its form: its name is the task
it does, as a gerund, `writing-rustdoc`, and its `SKILL.md` names it the same in
its front matter, which holds `name` and `description` alone, the description
under 1024 characters. A recipe a skill runs is one a profile of atxp defines.

What the check cannot hold a skill to, its author does:

- Its description says when to use it, in the third person, in the words a task
  is asked in, and what it covers; never its steps, which an agent would follow
  instead of the body.
- Its body is about 150 lines at most: the rules first, then the steps, then the
  checks, then what not to do. Longer material goes in `references/`, one level
  deep, each named where the body needs it.
- It names a recipe only where the profile that provides it is applied, so a
  skill that names another profile's recipe is a template; anything that is
  itself template language sits inside `{% raw %}`.
- It is written against what an agent does without it. An agent does a task the
  skill is for, in a repository the bundle writes, first without the skill and
  then with it; the skill says what the first run got wrong, and its examples
  come from a domain the task does not use.

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
just check                   # atxp's own checks, as CI runs them
just test                    # the suite, the bundle from nothing, and the setup stub's test
just fix-devset-collection   # after changing a profile: the catalog and every profile's facts
just bump-devset-collection  # every pin and dprint plugin moved past the cooldown, and relocked
```

After changing a pin, `mise exec -- python3 .just/devset-collection/pins.py lock
<profile>` relocks that profile's tools for every platform. `just test` runs the
devset release the `devset` profile pins, and the tools the profiles pin; to
test the profiles against another build of devset, set `$DEVSET` to its path.
