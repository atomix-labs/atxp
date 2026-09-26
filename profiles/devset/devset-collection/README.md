# `devset-collection`

For a collection of profiles, such as this one: a repository whose profiles
devset applies elsewhere. Its profiles are every `profile.toml` under
`profiles/`, each grouped by the directory it is in, as
`profiles/<group>/<name>/`.

- `just fix-devset-collection` writes the catalog: the README's tables of the
  profiles, under each group's heading, and of the variables; and each profile
  README's facts: the files it owns and when, its features, its recipes, its
  variables and what it requires. Each lies between comments that name this
  profile, and dprint formats it where
  [`markdown`](../../lang/markdown/README.md) is applied.
- `just check-devset-collection` fails when any of them is stale, or when a
  profile breaks a rule. A profile's name is unique, and its directory's; its
  description is one line, with no closing period; its README opens with its
  title; it owns a file or requires a profile, and each profile it requires is
  in the collection. Its recipes are in `.just/<name>.just`, each
  `<verb>-<name>`, its helpers are `.just/<name>.<ext>` or under
  `.just/<name>/`, and its pins are in `.config/mise/conf.d/devset-<name>.toml`.
  A variable several profiles declare, each declares alike; and every workflow a
  profile ships runs one mise.
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
`profiles/**/files/**` to what dprint, taplo, ruff and yamllint leave out, as
atxp does.

A profile pins its tools in `.config/mise/conf.d/devset-<name>.toml`, and owns
their entries in `.config/mise/mise.lock` as keys. A pin may gate each tool by a
feature, between lines of `{% if "<feature>" in devset.features %}` and `{%
endif %}`: its lock entries carry the same gate, and both files are templates.

<!-- facts: written by devset-collection -->

## Owns

| File                                 | Part  | Policy | Notes          |
| ------------------------------------ | ----- | ------ | -------------- |
| `.just/devset-collection.just`       | whole | owned  | template       |
| `.just/devset-collection/catalog.py` | whole | owned  |                |
| `.just/devset-collection/suite.sh`   | whole | owned  |                |
| `.just/devset-collection/pins.py`    | whole | owned  | feature `pins` |

## Features

| Feature | Default | Enables |
| ------- | ------- | ------- |
| `pins`  |         |         |

## Recipes

- `check-devset-collection`: Checks the catalog and every profile's facts are
  current, and every profile keeps the collection's rules; with `pins`, also
  every pin locked for every platform, and every dprint plugin checksummed.
- `fix-devset-collection`: Writes the catalog and every profile's facts.
- `bump-devset-collection`: Moves every pin and dprint plugin past the cooldown,
  and relocks what moved for every platform.
- `test-devset-collection`: Tests every profile: alone, then each bundle and all
  at once on each fixture, with `just check`.

## Requires

- [`devset`](../devset/README.md)
- [`just`](../../tooling/just/README.md)
- [`mise`](../../tooling/mise/README.md)

<!-- /facts -->
