# `agents`

What a coding agent reads before it changes the repository. AGENTS.md, which
every agent that follows the format reads, is started where the repository has
none, with a heading for what the repository is and one for its rules, both the
repository's to write. Its managed block says how to check a change, and which
files devset manages. CLAUDE.md, scaffolded where there is none, imports
AGENTS.md for Claude Code and says where the skills are.

Where the repository has a pass, a skill that runs on finished work in a fork of
its own, the block also has Before You Finish: each pass to run before a change
is done, with what it is for, and to fix what it finds or say why a finding does
not hold. It names `/review-rust` where
[`rust-lints`](../../rust/rust-lints/README.md)' `agents` is on, and is left out
where no pass is.

`.claude/settings.json` holds Claude Code's permissions as keys, under `merge`,
so the repository keeps its own beside them. An agent may run every `check-*`
and `fix-*` recipe, `just --list`, devset's commands that only read, and `git
diff`, `git log`, `git show` and `git status`, which a pass reads the change
with, without asking. It may never run `just publish`, which no release can take
back, or `just bump`, the weekly workflow's; `just release`, which only writes,
asks first. Claude Code honours the list only in a workspace whose trust dialog
was accepted; in one that is untrusted, a pass reads the files it can and says
in its report what it could not run.

With `hook`, the default, a turn that changes the repository ends only once
`just check` passes. As each prompt arrives, a `UserPromptSubmit` hook notes the
repository's state: `HEAD`, the changes to tracked files, and the untracked
files. The Stop hook runs `just check` only if that state has changed, so a turn
that reads, plans or answers ends at once, whatever the tree held before it.

- **The check runs through `mise exec`**, as CI's does, since a hook's shell has
  no mise activated; mise is found on `PATH` or in `~/.local/bin`.
- **Its failures block the stop**, and the agent works on. If it then changes
  nothing, it may stop, so a failure it cannot fix, or that was there before the
  turn, never loops.
- **When the check cannot run**, with mise or just not installed or mise
  failing, the hook tells you why and lets the agent stop.

The notes are kept per session in `.git/claude-hook/`.

Skills come with the profiles they teach, each under that profile's `agents`
feature; the bundle [`rust`](../../bundles/rust/README.md)'s `agents` turns on
this profile and every skill.

<!-- facts: written by devset-collection -->

## Owns

| File                     | Part  | Policy | Notes                      |
| ------------------------ | ----- | ------ | -------------------------- |
| `AGENTS.md`              | block | owned  | template                   |
| `CLAUDE.md`              | whole | once   | scaffold `claude`          |
| `.claude/settings.json`  | keys  | merge  | template                   |
| `.claude/hooks/check.sh` | whole | owned  | executable, feature `hook` |

## Features

| Feature | Default | Enables |
| ------- | ------- | ------- |
| `hook`  | yes     |         |

## Requires

- [`just`](../../tooling/just/README.md)

<!-- /facts -->
