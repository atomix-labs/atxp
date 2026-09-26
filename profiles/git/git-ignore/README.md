# `git-ignore`

Git ignores, in a block of `.gitignore`, what is kept locally (Claude Code's
per-developer settings, notes), editors' own files but the shared VS Code
settings, and anything that looks like a secret: `.env`, keys and certificates,
`.secrets/`. Each tool's own output is ignored by the profile that brings the
tool, in a block of its own. Where the repository has no `.gitignore`, it starts
one, with a line saying how the file is laid out.

Lines of `.gitignore` are read in order: a repository's exception, such as a
throwaway key it does commit, goes after the block.

<!-- facts: written by devset-collection -->

## Owns

| File         | Part  | Policy | Notes |
| ------------ | ----- | ------ | ----- |
| `.gitignore` | block | owned  |       |

<!-- /facts -->
