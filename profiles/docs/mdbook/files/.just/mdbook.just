# Lints the book (every page in SUMMARY.md, every include and anchor there, every recipe the prose
# names), builds it, and runs its Rust examples.{% if "api" in devset.features %} The workspace's
# API lands at /api, with rustdoc's index page.{% endif %}{% if "links" in devset.features %} Then
# lychee checks every link of the built book, offline.{% endif %}
check-mdbook:
    #!/usr/bin/env bash
    set -euo pipefail
    mise exec -- python3 -B .just/mdbook.py {{ book_dir }}
    mdbook build {{ book_dir }}
    # mdbook runs rustdoc from a temporary directory, where rust-toolchain.toml no longer applies.
    RUSTUP_TOOLCHAIN="$(rustup show active-toolchain | cut -d' ' -f1)" mdbook test {{ book_dir }}
{%- if "api" in devset.features %}
    # rustdoc's index page is nightly's; its output lands in target/doc, not target/<triple>/doc.
    env -u CARGO_BUILD_TARGET RUSTDOCFLAGS="-Zunstable-options --enable-index-page" \
        cargo doc --workspace --no-deps
    rm -rf {{ book_dir }}/book/api
    cp -R target/doc {{ book_dir }}/book/api
    find {{ book_dir }}/book/api -maxdepth 1 -name '.*' -delete
{%- endif %}
{%- if "links" in devset.features %}
    # The pages alone, as a stylesheet names fallbacks, such as KaTeX's fonts, a browser never
    # fetches; rustdoc's own pages aside, and the 404 page, whose links resolve against the site's
    # URL, which only a server has.
    book="$PWD/{{ book_dir }}/book"
    lychee --offline --no-progress --include-fragments --root-dir "$book" \
        --exclude-path "$book/api" --exclude-path "$book/404.html" "$book/**/*.html"
{%- endif %}
