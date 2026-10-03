#!/usr/bin/env bash
# The publish check's metadata against a workspace of four crates: one with all crates.io shows,
# which draws no finding; one with none of it; one whose keywords, categories and README crates.io
# would refuse or break; and one kept off crates.io, which the check never reads.
#
# Run in atxp's root, with git, cargo and mise.
set -euo pipefail

root=$PWD
check=$root/profiles/cargo/cargo-publish/files/.just/cargo-publish.py
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cd "$work"
git init -q -b main
mkdir -p .just/cargo-publish
cp "$check" .just/
cp "$root/profiles/cargo/cargo-publish/files/.just/cargo-publish/categories.txt" .just/cargo-publish/

cat > Cargo.toml << 'EOF'
[workspace]
members  = ["crates/*"]
resolver = "3"

[workspace.package]
version      = "0.1.0"
edition      = "2024"
rust-version = "1.98"
license      = "MIT OR Apache-2.0"
authors      = ["The atxp Developers"]
repository   = "https://github.com/example/tiles"

[workspace.lints.rust]
unsafe_code = "deny"
EOF
printf 'MIT\n' > LICENSE-MIT
printf 'Apache-2.0\n' > LICENSE-APACHE

# The root README, with each kind of relative link crates.io leaves broken, and absolute ones.
cat > README.md << 'EOF'
<!-- >>> devset: project >>> -->
<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/media/logo-dark.svg">
    <img alt="tiles" src="docs/media/logo-light.svg" height="56">
  </picture>
</h1>
<!-- <<< devset: project <<< -->

[![CI](docs/ci.svg)](https://github.com/example/tiles/actions)

Read [CONTRIBUTING.md](CONTRIBUTING.md) first, or [the book][book], or [Install](#install).

```md
[ignored](inside/a/fence.md)
```

`[ignored](inside/a/span.md)` and the [licence][mit].

[book]: https://example.github.io/tiles/
[mit]: LICENSE-MIT
EOF

# A member `$1`, in `crates/$1`, whose `[package]` keys past the inherited ones are on stdin.
member() {
    mkdir -p "crates/$1/src"
    touch "crates/$1/src/lib.rs"
    {
        printf '[package]\nname                   = "%s"\n' "$1"
        printf 'description            = "a member of a workspace the check reads."\n'
        for key in version edition rust-version license authors repository; do
            printf '%-22s = true\n' "$key.workspace"
        done
        cat
        printf '\n[lints]\nworkspace = true\n'
    } > "crates/$1/Cargo.toml"
}

member tiles << 'EOF'
homepage               = "https://example.github.io/tiles/"
keywords               = ["board", "tile", "grid"]
categories             = ["data-structures", "game-development"]
EOF
cat > crates/tiles/README.md << 'EOF'
# `tiles`

Boards of [tiles](https://github.com/example/tiles).
EOF
ln -s ../../LICENSE-MIT crates/tiles/LICENSE-MIT
ln -s ../../LICENSE-APACHE crates/tiles/LICENSE-APACHE

member tiles-bare < /dev/null

member tiles-bad << 'EOF'
homepage               = "https://example.github.io/tiles/"
readme                 = "../../README.md"
keywords               = ["board", "tile", "grid", "game", "square", "two words"]
categories             = ["data-structures", "boards"]
EOF
ln -s ../../LICENSE-MIT crates/tiles-bad/LICENSE-MIT
ln -s ../../LICENSE-APACHE crates/tiles-bad/LICENSE-APACHE

member tiles-private << 'EOF'
publish                = false
EOF
git add -A
cargo generate-lockfile --offline --quiet

want=$(cat << 'EOF'
crates/tiles-bad/Cargo.toml  keywords: 6, and crates.io takes at most 5
crates/tiles-bad/Cargo.toml  keywords: `two words` is no keyword crates.io takes: at most 20 ASCII letters, digits, `_`, `-` or `+`, the first a letter or a digit
crates/tiles-bad/Cargo.toml  categories: `boards` is no category of crates.io's; take a slug from https://crates.io/category_slugs
README.md:4  link: `docs/media/logo-dark.svg` is relative, and crates.io shows this README; answer `logo` with a URL, `devset apply --var logo=https://raw.githubusercontent.com/example/tiles/main/docs/media/logo`
README.md:5  link: `docs/media/logo-light.svg` is relative, and crates.io shows this README; answer `logo` with a URL, `devset apply --var logo=https://raw.githubusercontent.com/example/tiles/main/docs/media/logo`
README.md:10  link: `docs/ci.svg` is relative, and crates.io shows this README; write `https://raw.githubusercontent.com/example/tiles/main/docs/ci.svg`
README.md:12  link: `CONTRIBUTING.md` is relative, and crates.io shows this README; write `https://github.com/example/tiles/blob/main/CONTRIBUTING.md`
README.md:21  link: `LICENSE-MIT` is relative, and crates.io shows this README; write `https://github.com/example/tiles/blob/main/LICENSE-MIT`
crates/tiles-bare/Cargo.toml  readme: none; add a `README.md` beside this file, or `readme = "../../README.md"` for the crate the root README is for
crates/tiles-bare/Cargo.toml  keywords: none; add up to five, the words a search on crates.io finds it by, `keywords = ["…"]`
crates/tiles-bare/Cargo.toml  categories: none; add up to five of crates.io's slugs, https://crates.io/category_slugs, `categories = ["…"]`
crates/tiles-bare/Cargo.toml  homepage: none; set `homepage = "https://example.github.io/tiles/"`, the book, in `[workspace.package]`, and `homepage.workspace = true` here
crates/tiles-bare/Cargo.toml  license: `LICENSE-MIT` is not in the package; link it, `ln -s ../../LICENSE-MIT crates/tiles-bare/LICENSE-MIT`
crates/tiles-bare/Cargo.toml  license: `LICENSE-APACHE` is not in the package; link it, `ln -s ../../LICENSE-APACHE crates/tiles-bare/LICENSE-APACHE`
  crates-io: 14 finding(s) over 3 crate(s)
EOF
)

# Each finding, and no other, in the order the workspace lists its crates.
if said=$(mise exec -- python3 -B .just/cargo-publish.py metadata --book https://example.github.io/tiles/ 2> /dev/null); then
    echo "cargo-publish: a workspace crates.io would refuse drew no finding" >&2
    exit 1
fi
if [[ $(sort <<< "$said") != "$(sort <<< "$want")" ]]; then
    diff <(sort <<< "$want") <(sort <<< "$said") >&2 || true
    echo "cargo-publish: the findings above differ from those wanted" >&2
    exit 1
fi

# Without a book, no crate needs a homepage.
said=$(mise exec -- python3 -B .just/cargo-publish.py metadata 2> /dev/null || true)
if grep -q homepage <<< "$said"; then
    printf 'cargo-publish: a workspace with no book drew\n%s\n' "$said" >&2
    exit 1
fi

# The crate with all of it, alone on crates.io, draws nothing.
for crate in tiles-bare tiles-bad; do
    sed -i '/^repository.workspace/a publish                = false' "crates/$crate/Cargo.toml"
done
mise exec -- python3 -B .just/cargo-publish.py metadata --book https://example.github.io/tiles/ > /dev/null
echo "ok: the publish check names what each crate's page on crates.io lacks"
