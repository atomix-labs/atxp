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

# A profile `$1` whose skill `$2` has the SKILL.md on stdin, and any further files: each ships with
# `agents`, and is a template where `$template` is set.
profile() {
    local name=$1 skill=$2 dir=profiles/test/$1 file
    mkdir -p "$dir/files/.claude/skills/$skill/references"
    cat > "$dir/files/.claude/skills/$skill/SKILL.md"
    {
        printf '[profile]\nname = "%s"\ndescription = "A test"\ndevset = ">=0.5.0"\n\n' "$name"
        printf '[features]\nagents = []\n\n'
        for file in ".claude/skills/$skill/SKILL.md" "${@:3}"; do
            printf '[files."%s"]\n' "$file"
            [[ -z ${template:-} ]] || printf 'template = true\n'
            printf 'when = { features = ["agents"] }\n\n'
        done
    } > "$dir/profile.toml"
}

# A profile that defines a recipe, `check-hinges`, and ships no skill.
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

# A profile that ships a skill, `writing-posts`, with no feature.
mkdir -p profiles/test/posts/files/.claude/skills/writing-posts
cat > profiles/test/posts/profile.toml << 'EOF'
[profile]
name = "posts"
description = "Posts"
devset = ">=0.5.0"

[files.".claude/skills/writing-posts/SKILL.md"]
EOF
printf -- '---\nname: writing-posts\ndescription: Use when setting posts.\n---\n' \
    > profiles/test/posts/files/.claude/skills/writing-posts/SKILL.md

# The guide and the pass that keep every rule: the guide names its references by a link and in
# code, gates another profile's recipe on it and its pass on the feature that ships it, and links
# an item in a Rust example, which is rustdoc's link, not the skill's.
tiles=.claude/skills/writing-tiles
template=1 profile good writing-tiles "$tiles"/references/{grid,edges}.md << 'EOF'
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
{%- set walls = devset.layers | selectattr("profile", "equalto", "good-pass")
    | map(attribute="features") | first | default([]) %}
{%- if "agents" in walls %}

Then run `/review-walls`.
{%- endif %}

```rust
/// Lays a tile, as [`lay`](Self::lay) does.
fn lay() {}
```
EOF
printf '# The Grid\n' > "profiles/test/good/files/$tiles/references/grid.md"
printf '# The Edges\n' > "profiles/test/good/files/$tiles/references/edges.md"
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

# Front matter: a guide with a field it does not hold, a pass without its fields, on another agent,
# a guide and a pass each named as the other, and a description that does not say when.
profile extra writing-domes << 'EOF'
---
name: writing-domes
description: Use when raising domes.
allowed-tools: Read
---
EOF
profile kind review-tiles << 'EOF'
---
name: review-tiles
description: Use when tiles are laid.
context: fork
---
EOF
profile agent review-beams << 'EOF'
---
name: review-beams
description: Use when the beams are up.
argument-hint: "[<paths>]"
context: fork
agent: Plan
model: inherit
background: false
---
EOF
profile bossy lay-bricks << 'EOF'
---
name: lay-bricks
description: Use when laying bricks.
---
EOF
profile idle reviewing-slabs << 'EOF'
---
name: reviewing-slabs
description: Use when a slab is poured.
argument-hint: "[<paths>]"
context: fork
agent: Explore
model: inherit
background: false
---
EOF
profile said writing-gables << 'EOF'
---
name: writing-gables
description: Covers gables.
---
EOF

# The body's budget.
{
    printf -- '---\nname: writing-walls\ndescription: Use when walling.\n---\n\n'
    head -c 18001 /dev/zero | tr '\0' a
} | profile budget writing-walls

# Files: one the profile does not declare, a reference the SKILL.md does not name, and a link to
# a file the profile does not ship.
profile orphan writing-roofs << 'EOF'
---
name: writing-roofs
description: Use when roofing.
---
EOF
printf '# Slates\n' > profiles/test/orphan/files/.claude/skills/writing-roofs/references/slates.md
profile unnamed writing-eaves .claude/skills/writing-eaves/references/gutters.md << 'EOF'
---
name: writing-eaves
description: Use when finishing eaves.
---
EOF
printf '# Gutters\n' \
    > profiles/test/unnamed/files/.claude/skills/writing-eaves/references/gutters.md
profile broken writing-stairs << 'EOF'
---
name: writing-stairs
description: Use when building stairs.
---

Read [the treads](references/treads.md) first.
EOF

# Gates: a recipe no profile defines; another profile's recipe named bare, in a skill and in an
# AGENTS.md, under a condition in a file that is no template, which ships the condition as text,
# and under an `or` and a `not`, which hold nothing; another profile's skill gated on its profile,
# not the feature that ships it, and one that ships with no feature, named bare; and a skill of the
# same profile that ships with another feature, named bare.
profile unknown writing-vaults << 'EOF'
---
name: writing-vaults
description: Use when vaulting.
---

Run `just check-vaults` after.
EOF
profile gate writing-doors << 'EOF'
---
name: writing-doors
description: Use when hanging doors.
---

Run `just check-hinges` after.
EOF
mkdir -p profiles/test/notes/files
cat > profiles/test/notes/profile.toml << 'EOF'
[profile]
name = "notes"
description = "Notes"
devset = ">=0.5.0"

[files."AGENTS.md"]
scope = "block"
EOF
cat > profiles/test/notes/files/AGENTS.md << 'EOF'
Run `just check-hinges` before you finish.
EOF
profile literal writing-frames << 'EOF'
---
name: writing-frames
description: Use when framing.
---
{%- if "hinges" in devset.profiles %}

Run `just check-hinges` after.
{%- endif %}
EOF
template=1 profile either writing-panes << 'EOF'
---
name: writing-panes
description: Use when glazing.
---
{%- if "hinges" in devset.profiles or "posts" in devset.profiles %}

Run `just check-hinges` after.
{%- endif %}
EOF
template=1 profile negated writing-sashes << 'EOF'
---
name: writing-sashes
description: Use when hanging sashes.
---
{%- if not "hinges" in devset.profiles %}

Run `just check-hinges` after.
{%- endif %}
EOF
template=1 profile layered writing-lintels << 'EOF'
---
name: writing-lintels
description: Use when setting lintels.
---
{%- if "good" in devset.profiles %}

Lay the tiles first, with `writing-tiles`.
{%- endif %}
EOF
profile rails writing-rails << 'EOF'
---
name: writing-rails
description: Use when fixing rails.
---

Set the posts first, with `writing-posts`.
EOF
profile sibling writing-sills << 'EOF'
---
name: writing-sills
description: Use when setting sills.
---

Hang the jambs first, with `writing-jambs`.
EOF
mkdir -p profiles/test/sibling/files/.claude/skills/writing-jambs
printf -- '---\nname: writing-jambs\ndescription: Use when hanging jambs.\n---\n' \
    > profiles/test/sibling/files/.claude/skills/writing-jambs/SKILL.md
printf '[files.".claude/skills/writing-jambs/SKILL.md"]\nwhen = { features = ["jambs"] }\n' \
    >> profiles/test/sibling/profile.toml

# Fences: an ignored Rust block, a failing one that does not say what it fails with, and one that
# holds template syntax.
profile fence writing-floors << 'EOF'
---
name: writing-floors
description: Use when laying floors.
---

```rust,ignore
fn floor() {}
```
EOF
profile failing writing-piers << 'EOF'
---
name: writing-piers
description: Use when sinking piers.
---

```rust,compile_fail
fn pier() -> u8 { "" }
```
EOF
profile braces writing-arches << 'EOF'
---
name: writing-arches
description: Use when turning arches.
---

```rust
fn arch() -> &'static str { "{{ span }}" }
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
expect "writing-domes/SKILL.md: a guide's front matter holds" \
    "a guide with a field it does not hold"
expect "review-tiles/SKILL.md: a pass runs forked" "a pass without its fields"
expect "review-beams/SKILL.md: a pass runs on \`Explore\`, \`general-purpose\`" \
    "a pass on another agent"
expect "lay-bricks/SKILL.md: \`name\` is \`lay-bricks\`, its directory, a gerund phrase" \
    "a guide named as a pass"
expect "reviewing-slabs/SKILL.md: \`name\` is \`reviewing-slabs\`, its directory, an imperative" \
    "a pass named as a guide"
expect "writing-gables/SKILL.md: \`description\` starts \`Use when\`" \
    "a description that does not say when"
expect "writing-walls/SKILL.md: the body is over 18000 characters" "the body's budget"
expect "writing-roofs/references/slates.md is not an entry" "a file the profile does not declare"
expect "writing-eaves/references/gutters.md is named nowhere in its SKILL.md" \
    "a reference the SKILL.md does not name"
expect "writing-stairs/SKILL.md links \`references/treads.md\`, which its profile does not ship" \
    "a link to nothing"
expect "writing-vaults/SKILL.md names \`just check-vaults\`, which no profile" \
    "a recipe no profile defines"
expect "writing-doors/SKILL.md names \`just check-hinges\`, which hinges defines" \
    "an ungated recipe"
expect "notes: AGENTS.md names \`just check-hinges\`, which hinges defines" \
    "an ungated recipe in an AGENTS.md"
expect "writing-frames/SKILL.md names \`just check-hinges\`, which hinges defines" \
    "a recipe gated in a file that is no template"
expect "writing-panes/SKILL.md names \`just check-hinges\`, which hinges defines" \
    "a recipe under an \`or\`"
expect "writing-sashes/SKILL.md names \`just check-hinges\`, which hinges defines" \
    "a recipe under a \`not\`"
expect "writing-lintels/SKILL.md names \`writing-tiles\`, which ships only with good's \`agents\`" \
    "another profile's skill gated on its profile"
expect "writing-rails/SKILL.md names \`writing-posts\`, which posts ships" \
    "another profile's skill of no feature, ungated"
expect "writing-sills/SKILL.md names \`writing-jambs\`, which ships only with its \`jambs\`" \
    "a skill of another feature, ungated"
expect "writing-floors/SKILL.md: line 6: a Rust block is \`rust\` or \`rust,compile_fail\`" \
    "an ignored block"
expect "writing-piers/SKILL.md: line 6: a failing block opens \`// fails:" \
    "a failing block that does not say why"
expect "writing-arches/SKILL.md: line 6: a Rust block holds no template syntax" \
    "template syntax in a Rust block"
if grep -q "profiles/test/good.*skills" <<< "$out"; then
    echo "FAILED: a skill that keeps the form drew a finding"
    grep "profiles/test/good.*skills" <<< "$out"
    failed=1
fi
exit "$failed"
