# `devset-collection`

For a repository of profiles, such as this one: its profiles pin tools that land
in other repositories, so each pin must be locked, for every platform, before it
ships.

- `just check-devset-collection`, offline, fails when a profile's lock entry does not
  match its pin, lacks a platform or a checksum, or holds a tool another profile
  pins; and when a dprint plugin in a payload carries no `@sha256`.
- `just bump-devset-collection` moves every pin, and every dprint plugin, to its
  newest release past the cooldown: an exact pin is rewritten, a track such as
  `3.14` keeps its pin and moves in its lock. What moved is relocked for every
  platform, each checksum filled from the publisher's digest or else the
  download.

A profile pins its tools in `.config/mise/conf.d/devset-<id>.toml`, and owns
their entries in `.config/mise/mise.lock` as keys, each checked as
[`mise`](../../tooling/mise/README.md) checks it.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                      | Part  | Policy | Notes |
| ------------------------- | ----- | ------ | ----- |
| `.just/devset-collection.just` | whole | owned  |       |
| `.just/devset-collection.py`   | whole | owned  |       |

## Recipes

- `check-devset-collection`: Checks every profile's pins are locked for every
  platform, and every dprint plugin checksummed.
- `bump-devset-collection`: Moves every profile's pins and dprint plugins past the
  cooldown, and relocks what moved.

## Requires

- [`mise`](../../tooling/mise/README.md)

<!-- /facts -->
