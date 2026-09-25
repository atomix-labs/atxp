# Builds the book, and runs its Rust examples.
check-mdbook:
    mdbook build {{ book_dir }}
    mdbook test {{ book_dir }}
