#!/usr/bin/env bash
# The catalog check's skill form: a collection whose profiles each break one rule, and the finding
# each draws; a guide and a pass that keep every rule draw none.
#
# Run in atxp's root, with python3.
set -euo pipefail

catalog=$PWD/profiles/devset/devset-collection/files/.just/devset-collection/catalog.py
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cd "$work"
printf '[collection]\nname = "form"\ndescription = "Skills that break the form"\n' > collection.toml

# A profile `$1` whose skill `$2` has the SKILL.md on stdin, and any further files.
profile() {
    local name=$1 skill=$2 dir=profiles/test/$1 file
    mkdir -p "$dir/files/.claude/skills/$skill/references"
    cat > "$dir/files/.claude/skills/$skill/SKILL.md"
    {
        printf '[profile]\nname = "%s"\ndescription = "A test"\ndevset = ">=0.5.0"\n\n' "$name"
        printf '[features]\nagents = []\n\n'
        for file in ".claude/skills/$skill/SKILL.md" "${@:3}"; do
            printf '[files."%s"]\nwhen = { features = ["agents"] }\n\n' "$file"
        done
    } > "$dir/profile.toml"
}

profile good writing-tiles .claude/skills/writing-tiles/references/{grid,edges}.md << 'EOF'
---
name: writing-tiles
description: Use when laying tiles.
---

# Writing Tiles

Read [the grid](references/grid.md) before laying one, and `references/edges.md`
before a cut.
{%- if "hinges" in devset.profiles %}

Run `just check-hinges` after.
{%- endif %}

```rust
/// Lays a tile, as [`lay`](Self::lay) does.
fn lay() {}
```
EOF
printf '# The Grid\n' > profiles/test/good/files/.claude/skills/writing-tiles/references/grid.md
printf '# The Edges\n' > profiles/test/good/files/.claude/skills/writing-tiles/references/edges.md
profile good-pass review-walls << 'EOF'
---
name: review-walls
description: Use when a wall is built, before calling it done.
argument-hint: "[<paths>]"
context: fork
agent: Explore
model: inherit
background: false
---

Reads the change, then reports each finding with its place.
EOF

profile kind review-tiles << 'EOF'
---
name: review-tiles
description: Use when tiles are laid.
context: fork
---
EOF
{
    printf -- '---\nname: writing-walls\ndescription: Use when walling.\n---\n\n'
    head -c 18001 /dev/zero | tr '\0' a
} | profile budget writing-walls
profile orphan writing-roofs << 'EOF'
---
name: writing-roofs
description: Use when roofing.
---
EOF
printf '# Slates\n' > profiles/test/orphan/files/.claude/skills/writing-roofs/references/slates.md
profile gate writing-doors << 'EOF'
---
name: writing-doors
description: Use when hanging doors.
---

Run `just check-hinges` after.
EOF
mkdir -p profiles/test/hinges/files/.just
cat > profiles/test/hinges/profile.toml << 'EOF'
[profile]
name = "hinges"
description = "Hinges"
devset = ">=0.5.0"

[files.".just/hinges.just"]
EOF
cat > profiles/test/hinges/files/.just/hinges.just << 'EOF'
# Checks the hinges.
check-hinges:
    true
EOF
profile fence writing-floors << 'EOF'
---
name: writing-floors
description: Use when laying floors.
---

```rust,ignore
fn floor() {}
```
EOF

out=$(python3 -B "$catalog" --check 2>&1 || true)
failed=0
expect() {
    if grep -qF -- "$1" <<< "$out"; then
        echo "ok: $2"
    else
        echo "FAILED: $2: no \`$1\`"
        failed=1
    fi
}
expect "review-tiles/SKILL.md: a pass runs forked" "a pass without its fields"
expect "writing-walls/SKILL.md: the body is over 18000 characters" "the body's budget"
expect "writing-roofs/references/slates.md is not an entry" "a file the profile does not declare"
expect "writing-doors/SKILL.md names \`just check-hinges\`, which hinges defines" \
    "an ungated recipe"
expect "writing-floors/SKILL.md: line 6: a Rust block is \`rust\` or \`rust,compile_fail\`" \
    "an ignored block"
if grep -q "profiles/test/good.*skills" <<< "$out"; then
    echo "FAILED: a skill that keeps the form drew a finding"
    failed=1
fi
exit "$failed"
