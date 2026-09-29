# `devset-collection`

For a collection of profiles, such as this one: a repository whose profiles
devset applies elsewhere. Its profiles are every `profile.toml` under
`profiles/`, each grouped by the directory it is in, as
`profiles/<group>/<name>/`. Where the repository has no `collection.toml`, it
scaffolds one, which names the collection after the directory and describes it
with `collection_description`.

- `just fix-devset-collection` writes the catalog: the README's tables of the
  profiles, under each group's heading, and of the variables; and each profile
  README's facts: the files it owns and when, its features, its recipes, its
  variables and what it requires. A recipe is described by the comment above it,
  where what it does only with a feature on closes with the feature, as "(with
  `api`)". Each lies between comments that name this profile, and dprint formats
  it where [`markdown`](../../lang/markdown/README.md) is applied.
- `just check-devset-collection` fails when any of them is stale, or when a
  profile breaks a rule. A profile's name is unique, and its directory's; its
  description is one line, with no closing period; its README opens with its
  title; it owns a file or requires a profile, and each profile it requires is
  in the collection. Its recipes are in `.just/<name>.just`, each
  `<verb>-<name>`, whose comment templates nothing but a feature's `{% if %}`,
  and a `check-` or `nightly-` recipe carries `[metadata("rust")]` exactly where
  it runs cargo, rustc, rustdoc or rustup, which
  [`github-ci`](../../github/github-ci/README.md) reads; its helpers are
  `.just/<name>.<ext>` or under `.just/<name>/`, and its pins are in
  `.config/mise/conf.d/devset-<name>.toml`. A variable several profiles declare,
  each declares alike; and every workflow a profile ships runs one mise. A skill
  a profile ships, `.claude/skills/<skill>/SKILL.md`, is a guide or a pass. A
  guide's front matter holds `name`, its directory's and a gerund phrase, and
  `description` alone; a pass's, which runs forked, also `argument-hint`,
  `context: fork`, `agent`, `model: inherit` and `background: false`, and may
  hold `allowed-tools`, its name an imperative. The description starts "Use
  when", under 1024 characters, and the body stays within 18,000. Every file of
  a skill is an entry of the profile, its SKILL.md names each reference, and a
  relative link leads to a file the profile ships. A recipe or skill that a
  skill, AGENTS.md or CLAUDE.md names is one the collection has, under a
  condition on the profile or the feature that provides it, unless the profile
  requires that one. A Rust block is `rust` or `rust,compile_fail`, a failing
  one says what it fails with, and none holds template syntax.
- `just test-devset-collection` runs the suite, with the devset that
  [`devset`](../devset/README.md) pins. Every profile alone, with its default
  features and with every feature, applies without drift. Then on each fixture
  in `tests/fixtures/`, each bundle with no features, and every profile at once
  with every feature, applies, and `just check` passes there. `$DEVSET`, a path,
  runs another build of devset.

With `pins`, for a collection whose profiles pin tools with mise, each pin is
held to what [`mise`](../../tooling/mise/README.md) holds a repository's own to:

- `just check-devset-collection` also fails when a profile's lock entry does not
  match its pin, lacks a platform or a checksum, or holds a tool the profile
  does not pin; and when a dprint plugin in a payload carries no `@sha256`.
- `just bump-devset-collection` moves every pin, and every dprint plugin, to its
  newest release past the cooldown: an exact pin is rewritten, a track such as
  `3.14` keeps its pin and moves in its lock. What moved is relocked for every
  platform, each checksum filled from the publisher's digest or else the
  download.

A collection's payloads are templates until devset renders them, and the suite
checks them rendered, so its own formatters and linters leave them alone: the
recipes export `DPRINT_CONFIG_DISCOVERY=ignore-descendants`, so dprint reads no
payload's `dprint.json` as configuration, and a collection adds
`profiles/**/files/**` to what dprint, rumdl, taplo, ruff and yamllint leave
out, as atxp does.

With `site`, off unless the collection turns it on, the catalog is a site too:
an mdBook in `catalog/`, whose pages `just fix-devset-collection` writes under
`catalog/src/` from the manifests and READMEs, and `just
check-devset-collection` checks and builds:

- a home: what the collection is, how a repository takes a profile, its bundles,
  and every group with its profiles;
- a page per profile: how to take it, its group, the bundles that take it and
  when, then its README and facts, a link to another profile's README moved to
  that profile's page and one to anything else in the repository to its page on
  GitHub; a bundle's page lists every file its profiles may write;
- a page of every variable, its default, what it asks and who declares it.

The README's tables then name the groups, each profile linked to its page, and
the site holds the rest. `catalog/book.toml` is scaffolded, the repository's
from then on; the palette is [`mdbook`](../../docs/mdbook/README.md)'s, and
mdBook is pinned. A release's pages say `--tag <release>`, which never goes
stale, beside a badge of the newest.
[`github-ci`](../../github/github-ci/README.md)'s `pages` publishes the built
book from a recipe `.github/automation.json` names.

Its default feature, `schemas`, turns on [`toml`](../../lang/toml/README.md)'s,
so where toml is applied, `check-toml` holds every `profile.toml` and
`collection.toml` to devset's schemas.

A profile pins its tools in `.config/mise/conf.d/devset-<name>.toml`, and owns
their entries in `.config/mise/mise.lock` as keys. A pin may gate each tool by a
feature, between lines of `{% if "<feature>" in devset.features %}` and `{%
endif %}`: its lock entries carry the same gate, and both files are templates.

The `agents` feature adds the `authoring-devset-profiles` skill in
`.claude/skills/`: the design questions, the rules above, and the checks, for an
agent that adds or changes a profile.

A collection others may take is easiest to find tagged: the GitHub topic
`devset-collection` on its repository lists it at
<https://github.com/topics/devset-collection>, beside atxp.

<!-- facts: written by devset-collection -->

## Owns

| File                                                | Part  | Policy | Notes                                        |
| --------------------------------------------------- | ----- | ------ | -------------------------------------------- |
| `collection.toml`                                   | whole | once   | template, scaffold `collection`              |
| `.just/devset-collection.just`                      | whole | owned  | template                                     |
| `.just/devset-collection/catalog.py`                | whole | owned  |                                              |
| `.just/devset-collection/suite.sh`                  | whole | owned  |                                              |
| `.just/devset-collection/site_pages.py`             | whole | owned  |                                              |
| `.just/devset-collection/pins.py`                   | whole | owned  | feature `pins`                               |
| `catalog/book.toml`                                 | whole | once   | template, scaffold `catalog`, feature `site` |
| `catalog/theme/palette.css`                         | whole | merge  | feature `site`                               |
| `catalog/theme/catalog.css`                         | whole | owned  | feature `site`                               |
| `.gitignore`                                        | block | owned  | feature `site`                               |
| `.claude/skills/authoring-devset-profiles/SKILL.md` | whole | owned  | template, feature `agents`                   |

## Features

| Feature   | Default | Enables           |
| --------- | ------- | ----------------- |
| `pins`    |         |                   |
| `schemas` | yes     | `toml?/schemas`   |
| `agents`  |         |                   |
| `site`    |         | `dep:mdbook-tool` |

## Recipes

- `check-devset-collection`: Checks the catalog and every profile's facts are
  current, and every profile keeps the rules.
- `fix-devset-collection`: Writes the catalog and every profile's facts.
- `bump-devset-collection`: Moves every pin and dprint plugin past the cooldown,
  and relocks what moved for every platform.
- `test-devset-collection`: Tests every profile: alone, then each bundle and all
  at once on each fixture, with `just check`.

## Variables

| Variable                 | Default | Asks                                             |
| ------------------------ | ------- | ------------------------------------------------ |
| `collection_description` | empty   | One line: what the collection's profiles are for |
| `repository`             | none    | The GitHub repository, owner/name                |

## Requires

- [`devset`](../devset/README.md)
- [`just`](../../tooling/just/README.md)
- [`mdbook-tool`](../../docs/mdbook-tool/README.md): optional
- [`mise`](../../tooling/mise/README.md)
- [`toml`](../../lang/toml/README.md): optional

<!-- /facts -->
