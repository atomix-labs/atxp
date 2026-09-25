# `mise`

[mise](https://mise.jdx.dev) installs every tool the profiles pin from one
lockfile, `.config/mise/mise.lock`, which covers `linux-arm64`, `linux-x64` and
`macos-arm64`: a platform missing from it is refused. Every download is verified
by its checksum, and by the publisher's attestations where they exist. No
release younger than three days is chosen.

Each profile owns its tools' entries in the lock, so the lock composes as the
profiles do; tools the repository configures itself, in `mise.toml`, lock in
`mise.lock`.

- `just check-mise` fails when a tool is not locked at its pinned version, lacks
  a platform, or has neither a checksum nor provenance.
- `just bump-mise` moves the repository's own tools to their newest releases
  past the cooldown, locks them, and fills each checksum from the publisher's
  digest, or failing that from the download. The profiles' pins move with atxp's
  releases.

<!-- facts: written by scripts/catalog.py -->

## Owns

| File                                   | Part  | Policy | Notes |
| -------------------------------------- | ----- | ------ | ----- |
| `.config/mise/conf.d/devset-mise.toml` | whole | owned  |       |
| `.config/mise/mise.lock`               | keys  | owned  |       |
| `.just/mise.just`                      | whole | owned  |       |
| `.just/mise.py`                        | whole | owned  |       |

## Recipes

- `check-mise`: Checks every tool is locked for every platform, each download
  verified.
- `bump-mise`: Moves the repository's own tools to their newest releases past
  the cooldown, and locks them.

<!-- /facts -->
