{%- set book = devset.layers | selectattr("profile", "equalto", "mdbook") | map(attribute="features") | first | default([]) -%}
{%- set pages = " --exclude-path " ~ book_dir ~ "/src" if "links" in book else "" -%}
# Checks every link into the repository, offline, in each Markdown file git does not ignore; the
# book's pages are mdbook's where it checks the built book, in which a link to `/` has a root.
check-lychee:
    lychee --offline --no-progress --include-fragments --extensions md{{ pages }} .

# Checks every link, the web's too.
nightly-lychee:
    lychee --no-progress --include-fragments --extensions md{{ pages }} .
