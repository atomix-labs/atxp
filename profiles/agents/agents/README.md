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
not hold. It names `/humanize` and `/review-names` where `readability` is on,
`/review-rust` where [`rust-lints`](../../rust/rust-lints/README.md)' `agents`
is, and `/review-security` where `security` is; it is left out where no pass is.

`.claude/settings.json` holds Claude Code's permissions as keys, under `merge`,
so the repository keeps its own beside them. An agent may run every `check-*`
and `fix-*` recipe, `just --list`, devset's commands that only read, and `git
diff`, `git log`, `git show` and `git status`, which a pass reads the change
with, without asking. With `readability`, it may also invoke `/humanize`: in a
session run with `-p` or by the SDK, Claude Code refuses an agent's call to a
skill whose front matter grants it tools unless a rule allows it, and the rule
holds only where the list does, so that elsewhere only a person who types
`/humanize` runs it. It may never run `just publish`, which no release can take
back, or `just bump`, the weekly workflow's; `just release`, which only writes,
asks first. Each holds however the recipe is reached: `just` runs every recipe
it is given, so the list also refuses `just check publish`, which the allowed
`just check*` would otherwise admit, and asks before `just check release`.
Claude Code honours the list only in a workspace whose trust dialog was
accepted; in one that is untrusted, a pass reads the files it can and says in
its report what it could not run.

With `hook`, a default, a turn that changes the repository ends only once `just
check` passes. As each prompt arrives, a `UserPromptSubmit` hook notes the
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

With `readability`, a default, this profile teaches how a repository reads to
the person who maintains it, in any language, in `.claude/skills/`.
`writing-prose` is for every sentence a reader meets: documents, comments and
doc comments, commits, pull requests and changelogs, error, log and panic
messages, a CLI's help, a suppression's reason and an assertion's message. It
puts the fact first, once, in the present tense, says what is rather than what
was done, and keeps out the tells of generated text, ranked by strength, while
keeping the words technical text uses literally. `writing-readable-code` is for
the shape of code: names in the domain's words, never `data`, `manager` or
`utils`; a function that does one thing at one level; early returns over
nesting; states as types, an enum over flags and boolean parameters; no trait,
option or wrapper that nothing needs yet; dead code deleted; and the codebase's
own way over a local preference. Where another profile's skill holds a part,
each names it and defers to it, where it is applied: the Rust skills of
[`rust-lints`](../../rust/rust-lints/README.md) and
[`rust-doc`](../../rust/rust-doc/README.md) for Rust's own rules and its `///`,
`cutting-releases` for release notes. Each adds what Python asks where
[`python`](../../lang/python/README.md) is applied, and what the shell asks
where [`shell`](../../lang/shell/README.md) is.

`humanize` is the pass that acts on both, and the first in Before You Finish.
Given a path, a revision range or pasted text, it rewrites in place what a
change says to a reader (its prose, comments, doc comments, messages and names)
and code whose shape was left mechanical, the strongest tells first. It keeps
what the code does and every fact: it edits the code first and runs `just check`
and `just test` before any prose, undoing an edit that breaks a test, and makes
no rename or change of shape that no test or compiler would catch. It never
renames a public item, or a name a user types or a tool reads, and leaves what
devset manages alone. Its report lists each change and each tell it left, with
why, a public name among them for `/review-names`. In a session run with `-p` or
by the SDK, a fork cannot ask for an approval, so its front matter grants, for
the turn it runs, edits under the directory the session started in and the
commands it runs, `just fix`, `just check` and `just test` each only as written.
Those edits and recipes skip the prompts a session in the default mode would
show, and, unlike the allow-list, the grant holds in a workspace that is not
trusted. Claude Code still refuses an edit to `.git/`, and to the settings and
hooks in `.claude/`.

With `readability` too, the profile ships the `review-names` pass, which reads
each name a change adds, renames or makes false, or every name under a path, and
changes nothing. It reads each name's definition, uses and tests before it
judges it, public names first, and reports each that misleads, is unclear,
clashes with the codebase, citing the names it clashes with, or breaks the
language's conventions, leaving to the lints what they refuse. A published
crate's rename of a name a release has shipped breaks its callers, so the fix
keeps the old name as a deprecated alias; an unpublished crate's moves every
caller and keeps none. It takes a revision range or paths, and after `--` what
the change is for, `/review-names main..HEAD -- the grid's cursor moves by
squares`.

With `security`, a default, the profile ships the `review-security` pass, which
reviews a change for what someone outside the process can reach through it, and
changes nothing. It maps each input the change reads from outside the process
and who controls it, traces each through the attack classes a library or a CLI
meets, tries to refute each candidate, and reports only a finding with a
concrete path from the input to the harm, weighed by what an attacker gains.
Path traversal, command injection, unbounded allocation, decoding without
limits, secrets in logs and errors, races on files, input printed unescaped and
a recipe's arguments are always checked; panics on input, size arithmetic and
unsound `unsafe` where `rust-lints` is applied, with `writing-unsafe-rust` for a
proof where its `agents` is on; dependency advisories, through
`check-cargo-deny`, where [`cargo-deny`](../../cargo/cargo-deny/README.md) is;
scripts and Python where [`shell`](../../lang/shell/README.md) and
[`python`](../../lang/python/README.md) are; and a workflow's expressions where
[`github-ci`](../../github/github-ci/README.md) is. A published crate's public
function is judged for every caller it could have, an unpublished one's for the
workspace's. It adapts the method of Cloudflare's security-audit skill, MIT,
whose notice its `sources.md` carries. It takes a revision range or paths, and
after `--` what the change is for and who sends its input, `/review-security
main..HEAD -- the tile server loads the set a client names`.

<!-- facts: written by devset-collection -->

## Owns

| File                                                            | Part  | Policy | Notes                           |
| --------------------------------------------------------------- | ----- | ------ | ------------------------------- |
| `AGENTS.md`                                                     | block | owned  | template                        |
| `CLAUDE.md`                                                     | whole | once   | scaffold `claude`               |
| `.claude/settings.json`                                         | keys  | merge  | template                        |
| `.claude/hooks/check.sh`                                        | whole | owned  | executable, feature `hook`      |
| `.claude/skills/humanize/SKILL.md`                              | whole | owned  | template, feature `readability` |
| `.claude/skills/humanize/references/sources.md`                 | whole | owned  | feature `readability`           |
| `.claude/skills/review-names/SKILL.md`                          | whole | owned  | template, feature `readability` |
| `.claude/skills/review-security/SKILL.md`                       | whole | owned  | template, feature `security`    |
| `.claude/skills/review-security/references/attack-classes.md`   | whole | owned  | template, feature `security`    |
| `.claude/skills/review-security/references/sources.md`          | whole | owned  | template, feature `security`    |
| `.claude/skills/writing-prose/SKILL.md`                         | whole | owned  | template, feature `readability` |
| `.claude/skills/writing-prose/references/comments.md`           | whole | owned  | template, feature `readability` |
| `.claude/skills/writing-prose/references/messages.md`           | whole | owned  | template, feature `readability` |
| `.claude/skills/writing-prose/references/sources.md`            | whole | owned  | template, feature `readability` |
| `.claude/skills/writing-prose/references/tells.md`              | whole | owned  | template, feature `readability` |
| `.claude/skills/writing-readable-code/SKILL.md`                 | whole | owned  | template, feature `readability` |
| `.claude/skills/writing-readable-code/references/naming.md`     | whole | owned  | template, feature `readability` |
| `.claude/skills/writing-readable-code/references/simplicity.md` | whole | owned  | template, feature `readability` |
| `.claude/skills/writing-readable-code/references/sources.md`    | whole | owned  | template, feature `readability` |
| `.claude/skills/writing-readable-code/references/structure.md`  | whole | owned  | template, feature `readability` |

## Features

| Feature       | Default | Enables |
| ------------- | ------- | ------- |
| `hook`        | yes     |         |
| `readability` | yes     |         |
| `security`    | yes     |         |

## Requires

- [`just`](../../tooling/just/README.md)

<!-- /facts -->
