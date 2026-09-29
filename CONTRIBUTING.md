# Contributing

How to report a problem, and how to change atxp: setting up a checkout, how a
pull request lands, what counts as breaking, the rules every profile and skill
keeps, how its documents are written, and the checks to run.
[ARCHITECTURE.md](ARCHITECTURE.md) says how the profiles fit together.

## Reporting Issues

Open an issue with the form that fits: a **bug report** names the profile,
devset's version, what happened and how to reproduce it; a **profile request**
names the tool, why, and what the profile would own. A question, or a profile to
talk over first, goes to
[Discussions](https://github.com/atomix-labs/atxp/discussions), and a collection
of your own to show others to its Show and tell. A bug in devset itself belongs
in [devset's repository](https://github.com/atomix-labs/devset/issues).

<!-- >>> devset: setup >>> -->

## Getting Started

`./setup.sh` readies a machine to work on the repository: it installs mise,
pinned and checked against its release's sha256, then every tool the repository
pins, at the version its lock records, and runs `just setup`. It needs git, curl
and bash, installs into your home directory without sudo, and `--dry-run` says
what it would do. Fork the repository, then:

```sh
git clone https://github.com/<you>/atxp.git
cd atxp
./setup.sh
```

Or clone and set up in one line:

```sh
curl -fsSL https://atomix-labs.github.io/atxp/setup.sh | bash -s -- github.com/atomix-labs/atxp
```

The first run takes a few minutes; run it again after pulling, and it installs
only what moved. `./setup.sh --activate` adds mise to your shell, so the tools
are on `PATH` in every new one; without it, `mise exec -- just check` runs them.

<!-- <<< devset: setup <<< -->

## Pull Requests

Keep each pull request to one change: a profile, a fix, or a refactor, not a mix
of them. Every change to `main` is a pull request, merged once its checks pass:
`check`, every check recipe; `profiles`, the suite; and `title`, its title.

Run `just check` and `just test` before pushing: CI runs the same. `just test`
applies every profile to scratch repositories and checks each, which takes a few
minutes.

<!-- >>> devset: git-commits >>> -->

## Commits

A pull request lands squashed, as one commit its title names, so its **title**
follows [Conventional Commits](https://www.conventionalcommits.org), which CI
checks on every edit:

```text
type(scope): subject
```

- The **type** is `feat`, `fix`, `refactor`, `docs`, `perf`, `test`, `build`,
  `ci`, `chore`, `style` or `revert`.
- The **subject** is imperative, lower case, with no closing period: it is the
  line the changelog shows.
- A breaking change adds `!` after the scope, and its description says what to
  do.

The commits on your branch are yours to shape; `just check-git-commits` checks
them against the same rules, for a branch that reads well in review.

<!-- <<< devset: git-commits <<< -->

A commit's scope is the profile it changes, `feat(toml): …`, or the part of the
repository that is not a profile: `docs`, `ci`, `tests` or `release`. A change
across several profiles has no scope.

A change is **breaking** when a repository that takes it must act: a profile, a
file or a variable removed or renamed; a scope or a policy changed; a check that
fails a build it passed; a higher minimum version of a tool. A breaking change
also adds its entry to [BREAKING-CHANGES.md](BREAKING-CHANGES.md), under the
release that will carry it.

<!-- >>> devset: github-labels >>> -->

## Labels

An issue's kind is its type, Bug, Feature or Task, and a pull request's is its
title's. Labels say the rest, and most are set for you:

| Label              | Means                                       | Set by               |
| ------------------ | ------------------------------------------- | -------------------- |
| `triage`           | new, and yet to be looked at                | the issue forms      |
| `waiting`          | on someone else: the reporter, or upstream  | a maintainer         |
| `good first issue` | a small change, well described, to start on | a maintainer         |
| `help wanted`      | accepted, and open to anyone                | a maintainer         |
| `breaking`         | changes what users rely on                  | a title's `!`        |
| `dependencies`     | moves a pinned tool, action or crate        | the bump, Dependabot |
| `automation`       | opened by a workflow                        | the workflow         |
| `area: <name>`     | where a change lands                        | the files it changes |

A maintainer takes `triage` off once an issue is understood. See
[what awaits triage][triage], and the [good first issues][first].
`.github/labels.toml` holds the labels, and each area's paths.

[triage]: https://github.com/atomix-labs/atxp/issues?q=is%3Aopen+label%3Atriage
[first]: https://github.com/atomix-labs/atxp/contribute

<!-- <<< devset: github-labels <<< -->

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
  `.just/<name>.<ext>` or under `.just/<name>/`; a `check-` or `nightly-` recipe
  that runs cargo, rustc, rustdoc or rustup has `[metadata("rust")]` above it,
  so its CI job restores Cargo's build, and no other recipe has it;
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
feature. It is a guide, which teaches while the agent works, or a pass, which
runs forked on finished work and reports. `check-devset-collection` holds each
to its form:

- **Front matter.** A guide's holds `name` and `description` alone, the name its
  directory's and a gerund phrase for the task, `writing-rustdoc`. A pass's also
  holds `argument-hint`, `context: fork`, `agent`, which is `Explore` or
  `general-purpose`, `model: inherit` and `background: false`, and may hold
  `allowed-tools`; its name is an imperative for its command, `review-rust`. A
  description starts "Use when", under 1024 characters.
- **The body** stays within 18,000 characters, counted in the source, a
  template's tags and all.
- **Files.** Every file under the skill's directory is an entry of its profile;
  the `SKILL.md` names each reference, by a link or in code; and each relative
  link outside code leads to a file the profile ships, so a skill of another
  profile is named, never linked.
- **Recipes and gates**, in a skill's files, AGENTS.md and CLAUDE.md. A recipe
  named there is one a profile of the collection defines. A recipe of a profile
  this one does not require sits under a condition on the profile that defines
  it: `"<profile>" in devset.profiles`, or a `devset.layers` variable for it. A
  skill of another profile sits under the feature that ships it, through a
  `devset.layers` variable, or under that profile where it ships with no
  feature; a skill of the same profile, under its feature through
  `devset.features`, unless the file ships with that feature too.
  - A skill counts as named where a code span holds its name alone,
    `writing-rustdoc` or `/review-rust`.
  - Only a file marked `template = true` has conditions, and a tag in a comment
    or inside `{% raw %}` is text: it gates nothing.
  - A condition with `or` or `not`, and so one with `and not`, holds nothing it
    names, nor does an `else`: nest an `if` instead.
- **Fences.** A Rust block is `rust` or `rust,compile_fail`, a
  `rust,compile_fail` block opens `// fails: <lint or error code>`, and no Rust
  block in a template holds template syntax, unless `{% raw %}` wraps the whole
  block. `test-skill-examples` compiles every Rust block as a crate of a
  workspace the rust bundle writes with `strict`, the lints that ask for docs
  allowed (`missing_docs`, and clippy's `missing_docs_in_private_items`,
  `missing_errors_doc`, `missing_panics_doc` and `missing_safety_doc`): a `rust`
  block passes clippy and nightly's lints, and a `rust,compile_fail` block fails
  with what its first line names. A fragment, an excerpt or a skeleton is
  `text`.

What the check cannot hold a skill to, its author does:

- Its description says when to use it, in the third person, in the words a task
  is asked in, and what it covers; never its steps, which an agent would follow
  instead of the body.
- Its body keeps its order: the rules first, then the steps, then the checks,
  then what not to do. Longer material goes in `references/`, one level deep,
  each named where the body needs it.
- In a template, template language meant as text sits inside `{% raw %}`.

Whether a skill works, only an agent shows, so its author validates it with one,
and CI never does: a model's pass rate is noisy, each run costs, and a fork's
pull request gets no secrets. No check calls a model or holds an API key.

1. **Without the skill first.** Write two or three cases, each a task the skill
   is for, asked as a user would ask it, never by the skill's name, and one near
   miss, close to those, that must not load it. Run each three times in a
   repository the bundle writes, each run a fresh `claude -p` session or
   subagent, never the session that wrote the skill. What the runs get wrong,
   verbatim, is what the skill says.
2. **Then with it**, three runs of each case at least. Read a failing transcript
   before changing a word, and write the fix as a rule, never as the case's
   answer: the skill's examples come from a domain the cases do not use. A pass
   also runs on a change seeded with faults, to see that it finds them and
   invents none. `claude plugin eval` can drive the runs; it loads the skill as
   a plugin skill, where a repository loads it as a project skill.
3. **The evidence, in the pull request**: the model, Claude Code's version, the
   runs, what failed without the skill and what holds with it. A change of
   wording alone says so instead.

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
just test                    # the suite, the bundle from nothing, the setup stub and the hooks
just fix-devset-collection   # after changing a profile: the catalog and every profile's facts
just bump-devset-collection  # every pin and dprint plugin moved past the cooldown, and relocked
```

After changing a pin, `mise exec -- python3 .just/devset-collection/pins.py lock
<profile>` relocks that profile's tools for every platform. `just test` runs the
devset release the `devset` profile pins, and the tools the profiles pin; to
test the profiles against another build of devset, set `$DEVSET` to its path.
