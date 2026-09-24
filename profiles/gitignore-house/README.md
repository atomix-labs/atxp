# `gitignore-house`

Git ignores, in a block of `.gitignore`, what the house's tools keep locally
(rumdl's cache, Python's bytecode, Claude Code's per-developer settings, notes),
editors' own files but the shared VS Code settings, and anything that looks like
a secret: `.env`, keys and certificates, `.secrets/`.

Lines of `.gitignore` are read in order: a repository's exception, such as a
throwaway key it does commit, goes after the block.
