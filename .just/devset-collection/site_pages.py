"""The collection's catalog site: an mdBook's sources, written from collection.toml, each profile's
manifest and README, which catalog.py writes and checks beside the READMEs with `--site <dir>`.
(Not `site.py`: Python keeps that name for its own module.)

    <dir>/src/SUMMARY.md             the home, the variables, then a part per group
    <dir>/src/index.md               what the collection is, how to take a profile, its bundles and groups
    <dir>/src/variables.md           every variable, its default, what it asks, who declares it
    <dir>/src/<group>/<profile>.md   a profile's page: how to take it, where it sits, its README

A link in a README to another profile's README goes to that profile's page; one to anything else in
the repository, to its page on GitHub.
"""

import os
import re
import tomllib
from collections import defaultdict
from pathlib import Path

COLLECTION = Path("collection.toml")
# A Markdown link's target, inline or by reference, that is neither a URL nor an anchor alone.
LINK = re.compile(r"(\]\(|^\[[^\]]+\]:\s*)(?![a-z]+:|#)([^)\s]+)", re.MULTILINE)
# The comments that mark a README's facts, which its page leaves out.
FACTS_MARKER = re.compile(r"^<!-- /?facts(: .*)? -->$")
# Files a profile pins tools with or hangs recipes from, which a bundle's list of files leaves out.
PLUMBING = (".just/", ".config/mise/")


class Site:
    """The catalog of `found`, the collection's profiles, for the repository `repository`."""

    def __init__(self, found, named, repository):
        self.found = found
        # Each README as this run writes it, facts and all, where it writes one.
        self.readmes = {}
        self.named = named
        self.repository = repository
        meta = tomllib.loads(COLLECTION.read_text()).get("collection", {}) if COLLECTION.is_file() else {}
        owner, _, repo = repository.partition("/")
        self.source = meta.get("name") or repo
        self.description = meta.get("description", "")
        self.url = f"https://{owner}.github.io/{repo}/"

    def page(self, profile):
        """Where `profile`'s page is, from the book's `src/`."""
        return Path(profile.group or "profiles") / f"{profile.name}.md"

    def to(self, profile, start):
        """A link to `profile`'s page from the page `start`, named for it."""
        path = Path(os.path.relpath(self.page(profile), start.parent)).as_posix()
        return f"[`{profile.name}`]({path})"

    def blob(self, path):
        """`path`, from the repository's root, on GitHub."""
        return f"https://github.com/{self.repository}/blob/main/{path.as_posix()}"

    def command(self, name):
        """How a repository takes the profile `name`."""
        return f"devset add {self.source}/{name} --git https://github.com/{self.repository} --tag <release>"

    def bundles(self):
        """The profiles that own no file and require others."""
        return [profile for profile in self.found if not profile.files and profile.requires]

    def within(self, profile):
        """Each bundle that takes `profile`, and when: always, or with one of its features."""
        out = []
        for bundle in self.bundles():
            spec = bundle.requires.get(profile.name)
            if spec is None:
                continue
            if not spec.get("optional"):
                out.append((bundle, None))
                continue
            for feature, enables in bundle.features.items():
                if f"dep:{profile.name}" in enables:
                    out.append((bundle, feature))
        return out

    def closure(self, profile):
        """`profile` and every profile it requires, required ones before those only a feature
        brings, each once."""
        seen, pending = [], [profile]
        while pending:
            current = pending.pop(0)
            if current in seen:
                continue
            seen.append(current)
            for name, spec in current.requires.items():
                if "git" not in spec and name in self.named:
                    pending.append(self.named[name][0])
        return seen

    def rewritten(self, profile, text):
        """`text`, `profile`'s README, its links to the repository moved to where the site holds
        them: another profile's page, or the file on GitHub."""
        start = self.page(profile)
        readmes = {p.readme.resolve(): p for p in self.found}

        def moved(match):
            target, _, anchor = match.group(2).partition("#")
            if not target:
                return match.group(0)
            resolved = (profile.path / target).resolve()
            fragment = f"#{anchor}" if anchor else ""
            if resolved in readmes:
                other = self.page(readmes[resolved])
                return f"{match.group(1)}{Path(os.path.relpath(other, start.parent)).as_posix()}{fragment}"
            try:
                inside = resolved.relative_to(Path.cwd())
            except ValueError:
                return match.group(0)
            return f"{match.group(1)}{self.blob(inside)}{fragment}"

        return LINK.sub(moved, text)

    def profile_page(self, profile):
        """`profile`'s page: its title and line, how to take it, where it sits, then its README."""
        start = self.page(profile)
        readme = self.readmes.get(profile.readme)
        if readme is None:
            readme = profile.readme.read_text() if profile.readme.is_file() else f"# `{profile.name}`\n"
        _, _, body = readme.partition("\n")
        where = [f"Group `{profile.group}`"] if profile.group else []
        for bundle, feature in self.within(profile):
            when = f"with `{feature}`" if feature else "always"
            where.append(f"In {self.to(bundle, start)}: {when}")
        out = [f"# `{profile.name}`", "", f"{profile.description}.", ""]
        out += ["```sh", self.command(profile.name), "```", ""]
        if where:
            out += [" · ".join(where), ""]
        # The README's facts are the page's too; their markers are the README's.
        body = "\n".join(line for line in body.splitlines() if not FACTS_MARKER.match(line))
        out.append(self.rewritten(profile, body).strip())
        if not profile.files and profile.requires:
            out += ["", *self.files_of(profile)]
        return "\n".join(out) + "\n"

    def files_of(self, bundle):
        """What the profiles `bundle` brings may write, each file with the profiles that do."""
        writers = defaultdict(list)
        for profile in self.closure(bundle):
            for path in profile.files:
                if not path.startswith(PLUMBING):
                    writers[path].append(profile)
        start = self.page(bundle)
        rows = ["## Files", "", "Every file its profiles may write, each under the gates its entry sets:", ""]
        rows += ["| File | Profiles |", "| --- | --- |"]
        for path in sorted(writers):
            rows.append(f"| `{path}` | {', '.join(self.to(p, start) for p in writers[path])} |")
        return rows

    def home(self):
        """The home page: the collection, how to take a profile, its bundles, and every group."""
        out = [f"# {self.source}", ""]
        if self.description:
            out += [f"{self.description}.", ""]
        badge = f"https://img.shields.io/github/v/release/{self.repository}?sort=semver&style=flat-square"
        releases = f"https://github.com/{self.repository}/releases"
        out += [f"[![Release]({badge})]({releases})", ""]
        out += [
            "A repository takes a profile by its name, and a release by its tag:",
            "",
            "```sh",
            self.command("<profile>"),
            "```",
            "",
            f"[The releases]({releases}) list every tag, and `devset update --dry-run` names the"
            " newer ones later. [devset's manual](https://atomix-labs.github.io/devset/) says the"
            " rest.",
            "",
        ]
        start = Path("index.md")
        if self.bundles():
            out += ["## Bundles", ""]
            out += [f"- {self.to(b, start)}: {b.description}." for b in self.bundles()]
            out.append("")
        out += ["## Profiles", ""]
        for group, members in self.groups():
            out += [f"### `{group}`", "", "| Profile | What |", "| --- | --- |"]
            out += [f"| {self.to(p, start)} | {p.description} |" for p in members]
            out.append("")
        return "\n".join(out)

    def groups(self):
        """Each group's name and profiles, in order; one at the top is under `profiles`."""
        groups = defaultdict(list)
        for profile in self.found:
            groups[profile.group or "profiles"].append(profile)
        return sorted(groups.items())

    def variables_page(self):
        """Every variable, a section each: what it asks, its default, and each profile that
        declares it."""
        seen = {}
        start = Path("variables.md")
        for profile in self.found:
            for name, spec in profile.manifest.get("vars", {}).items():
                seen.setdefault(name, (spec, []))[1].append(self.to(profile, start))
        out = [
            "# Variables",
            "",
            "A variable is a value each repository chooses; one that several profiles declare is one"
            " variable, with one default. A repository answers with `--var <name>=<value>`; one with"
            " no default, devset asks.",
            "",
        ]
        for name, (spec, by) in sorted(seen.items()):
            asks = spec.get("prompt", name).rstrip(".")
            default = (
                f"Default `{spec['default']}`" if spec.get("default") else "Empty by default" if "default" in spec else "No default"
            )
            out += [f"## `{name}`", "", f"{asks}.", "", f"{default} · Declared by {', '.join(by)}", ""]
        return "\n".join(out)

    def summary(self):
        """The book's summary: the home and the variables, then a part per group."""
        out = ["# Summary", "", f"[{self.source}](index.md)", "", "[Variables](variables.md)", ""]
        for group, members in self.groups():
            out += [f"# {group}", ""]
            out += [f"- [`{p.name}`]({self.page(p).as_posix()})" for p in members]
            out.append("")
        return "\n".join(out)

    def pages(self, root, readmes):
        """Every page, by its path under `root`, from `readmes`, each README as this run writes it."""
        self.readmes = readmes
        src = Path(root) / "src"
        out = {
            src / "SUMMARY.md": self.summary(),
            src / "index.md": self.home(),
            src / "variables.md": self.variables_page(),
        }
        for profile in self.found:
            out[src / self.page(profile)] = self.profile_page(profile)
        return out

    def readme_catalog(self):
        """What the README says of its profiles where the site holds them: the groups, linked."""
        out = [f"The profiles, by group, each with its page in [the catalog]({self.url}):", ""]
        for group, members in self.groups():
            names = ", ".join(f"[`{p.name}`]({self.url}{self.page(p).with_suffix('.html').as_posix()})" for p in members)
            out.append(f"- **`{group}`**: {names}")
        return "\n".join(out) + "\n"

    def readme_variables(self):
        """What the README says of its variables where the site holds them."""
        return f"Every variable, its default, and who declares it: [Variables]({self.url}variables.html).\n"
