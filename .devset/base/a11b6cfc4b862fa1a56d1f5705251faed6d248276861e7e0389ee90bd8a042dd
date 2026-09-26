---
name: authoring-devset-profiles
description: Use when adding, changing, splitting or removing a profile in a collection of devset profiles; when deciding whether something is a profile, a feature, a variable or a scaffold; when writing a profile.toml, a payload template, a recipe or a pin; or when the collection's check or its suite fails.
---

# Authoring `devset` Profiles

This repository is a collection: profiles devset applies to other repositories,
released together under one tag. A profile is a directory holding
`profile.toml`, its payloads under `files/` at the paths they take in a target,
and a `README.md`. devset's manual says how profiles work; the rules below are
the ones `just check-devset-collection` holds every profile to, and the ones it
cannot check.

## Rules

- **One concern a profile**: a tool with its configuration, pins, recipes and
  output, or one policy. Ask devset's questions in order
  ([Designing Profiles][designing]): would a repository want one without the
  other; would turning it on remove something; does the description join
  unrelated things with "and"; does it only make sense with its concern; is it
  content the project will own.
- **Names are API.** Removing or renaming a profile, a feature or a variable
  breaks every repository that names it, so it is a breaking change.
- **A profile lives in `profiles/<group>/<name>/`**, and `[profile] name` is its
  directory's, unique in the collection. Its `description` is one line with no
  closing period. Its README opens with its name as the title, then says in
  prose what it does and what stays the repository's; the catalog writes the
  rest.
- **Recipes are `<verb>-<name>`**, in `.just/<name>.just`, for the spine's
  verbs: `check`, `fix`, `bump`, `nightly`, `test`, `setup`, `host`, `release`,
  `package`, `publish`. A helper is `.just/<name>.<ext>`, or under
  `.just/<name>/`.
- **Pins live in the profile's own mise file**,
  `.config/mise/conf.d/devset-<name>.toml`, and their entries in
  `.config/mise/mise.lock` are the profile's keys, locked for every platform.
- **A shared file is shared by parts** ([Parts of a File][parts]): keys for
  TOML, JSON and YAML, a block for a line format. A list several profiles add to
  is one value, so its owner renders it from the graph, never from what is on
  disk ([Templates][templates]).
- **A variable several profiles declare is declared alike**: one prompt, one
  default.
- **A feature only adds.** A file it brings is gated by it, in the file's
  `when`; an optional requirement is turned on by `dep:`. A choice between
  alternatives is a variable.
- **A payload renders to the layout the target's formatters give**, whatever the
  graph and the answers. Text the graph adds is a whole line, paragraph or list
  item; an answer sits in a heading, a table, a code block or a link definition,
  never inside a paragraph a formatter wraps.
- **Content the project will own is a scaffold** ([Gates and Scaffolds][gates]):
  written once, where the repository lacks it.

## Steps

1. **Decide**, by the questions above, what it is and where it goes; a concern
   another profile owns is a feature of that profile.

2. **Write `profile.toml`**: `[profile]`, then `[features]`, `[requires]`,
   `[vars]`, `[scaffolds.<group>]`, and a `[files."<path>"]` table for each
   file, with its scope, policy, template flag and gates.

3. **Write the payloads** under `files/`. A template sees the answers and
   `devset`: `devset.profiles` and `devset.layers` for the graph,
   `devset.features` for the profile's own features, `devset.target` for the
   directory's name.

4. **Pin the tools**, then lock them for every platform:

   ```sh
   python3 .just/devset-collection/pins.py lock <name>
   ```

5. **Write the README**'s prose, then `just fix-devset-collection`, which writes
   the catalog and every profile's facts.

6. **Check**, below. A change to a payload is checked only when the suite
   renders it.

## Checks

- `just check-devset-collection`: the catalog and the facts are current, and
  every profile keeps the rules it can check.
- `just test`: the suite applies each profile alone, with its default features
  and with every feature, then every profile at once on each fixture, and runs
  `just check` there. It is slow, and it is the only check of a payload.

## What Not to Do

- Do not edit the catalog or a facts block by hand.
- Do not detect a profile by a file on disk: read the graph.
- Do not add a feature that removes or replaces what another adds.
- Do not copy another profile's file into a new one: require that profile.
- Do not skip `just test` after changing a payload because `just check` passed.

[designing]: https://atomix-labs.github.io/devset/designing.html
[gates]: https://atomix-labs.github.io/devset/gates.html
[parts]: https://atomix-labs.github.io/devset/parts.html
[templates]: https://atomix-labs.github.io/devset/templates.html
