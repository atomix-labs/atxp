"""The book's lint: what mdBook renders without a word, and should not.

Usage: mdbook.py <book-dir>

- A page under src/ that SUMMARY.md never links is never published.
- An include of a file that is not there only logs; one of an anchor the file lacks renders an
  empty block.
- A recipe a page names that the justfile does not have describes something that fails.

Prints each finding, and fails if there is one.
"""

import re
import subprocess
import sys
from pathlib import Path

LINK = re.compile(r"\]\(\s*(?:\./)?([^)#\s]+\.md)(?:#[^)]*)?\s*\)")
INCLUDE = re.compile(r"\{\{#(?:rustdoc_)?include\s+([^}\s]+)\s*\}\}")
RECIPE = re.compile(r"`just ([a-z][a-z0-9-]*)")


def listed(src):
    """Every page SUMMARY.md links, resolved."""
    summary = src / "SUMMARY.md"
    return {(src / link).resolve() for link in LINK.findall(summary.read_text())}


def recipes():
    """Every recipe the justfile has."""
    out = subprocess.run(["just", "--summary"], capture_output=True, text=True, check=True).stdout
    return set(out.split())


def includes(page, text):
    """Each broken include on `page`: a file that is not there, or an anchor the file lacks."""
    for spec in INCLUDE.findall(text):
        path, _, anchor = spec.partition(":")
        target = page.parent / path
        if not target.is_file():
            yield f"{page}: includes {path}, which is not there"
        elif anchor and not anchor[0].isdigit():
            body = target.read_text()
            for marker in ("ANCHOR", "ANCHOR_END"):
                if not re.search(rf"{marker}:\s*{re.escape(anchor)}(?![\w-])", body):
                    yield f"{page}: {path} has no `{marker}: {anchor}`"


def main(args):
    if len(args) != 1:
        print(
            next(line for line in __doc__.splitlines() if line.startswith("Usage:")),
            file=sys.stderr,
        )
        return 2
    src = Path(args[0]) / "src"
    published, known, found = listed(src), recipes(), []
    for page in sorted(src.rglob("*.md")):
        if page.name != "SUMMARY.md" and page.resolve() not in published:
            found.append(f"{page}: no entry in SUMMARY.md")
        text = page.read_text()
        found += includes(page, text)
        found += [
            f"{page}: names `just {recipe}`, which is no recipe"
            for recipe in RECIPE.findall(text)
            if recipe not in known
        ]
    for finding in found:
        print(finding, file=sys.stderr)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
