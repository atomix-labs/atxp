"""What a profile gives an agent to read, held to the house form: each skill it ships, in
`.claude/skills/<skill>/`, and the AGENTS.md and CLAUDE.md it writes. catalog.py's `--check` reports
what `agent_read_problems` finds.

A skill is a guide, which teaches while the agent works, or a pass, which runs forked on finished
work and reports. Its front matter says which; its body stays within what Claude keeps after
compaction; its files are its profile's and its references named; each recipe or skill it names is
there when an agent reads it; and its Rust blocks compile as they stand. `FENCE`, `RUST`,
`FAILING` and `FAILS` are the fence grammar a compiler of the examples reads too.
"""

import bisect
import os
import re

# A skill a profile ships: its entry point, in the directory that names it.
SKILLS = ".claude/skills/"
SKILL = re.compile(rf"^{re.escape(SKILLS)}([^/]+)/SKILL\.md$")
# What an agent reads: every recipe or skill it names must be there when it reads it.
READ = (SKILLS, "AGENTS.md", "CLAUDE.md")
# A skill's name is what it does: a guide's a gerund phrase, `writing-rustdoc`; a pass's an
# imperative, `review-rust`, the command a person types.
GERUND = re.compile(r"[a-z]+ing(?:-[a-z0-9]+)*")
IMPERATIVE = re.compile(r"(?![a-z]+ing(?:-|$))[a-z]+(?:-[a-z0-9]+)*")
# A skill's front matter, between its two `---` lines, one field to a line.
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
# A guide says what it is for; a pass also says how it runs: forked, with the session's model,
# while the agent waits for its report.
GUIDE = {"name", "description"}
PASS = GUIDE | {"argument-hint", "context", "agent", "model", "background"}
PASS_MAY = {"allowed-tools"}
PASS_RUNS = {"context": "fork", "model": "inherit", "background": "false"}
PASS_AGENTS = {"Explore", "general-purpose"}
# The longest description the skill format allows, in characters.
DESCRIPTION = 1024
# Claude re-attaches the first 5,000 tokens of each skill after compaction: a body within this
# survives whole. It counts the source, a template's tags and all.
BODY = 18_000
# A fenced block: three or more backticks or tildes at any indent, an info string, and the lines up
# to a fence of the same character, at least as long.
BLOCK = (
    r"^ *(?P<fence>(?P<ticks>`)`{2,}|~{3,})(?P<info>[^\n`]*)\n(?P<body>.*?)"
    r"^ *(?P=fence)(?(ticks)`*|~*)[ \t]*$"
)
FENCE = re.compile(BLOCK, re.DOTALL | re.MULTILINE)
# How a Rust block is marked, and one that must fail; and the first line of a failing one, which
# names what it fails with, a lint or an error code, as `failure`.
FAILING = "rust,compile_fail"
RUST = {"rust", FAILING}
FAILS = re.compile(r"\A *// fails: (?P<failure>clippy::[a-z_]+|[a-z_]+|E\d{4})\n")
# Code in Markdown: a fenced block, or a span, which may wrap, closed by as many backticks as open
# it.
CODE = re.compile(
    rf"{BLOCK}|(?P<span>`+)(?!`)(?P<inline>.+?)(?<!`)(?P=span)(?!`)", re.DOTALL | re.MULTILINE
)
# A link to a file beside it: relative, not a URL or an anchor.
LINK = re.compile(r"\]\((?![a-z]+:|#)([^)#\s]+)")
# The recipes run in code: `just` opening a command, after any variables it sets and through any
# `mise exec --`, then each recipe it runs, the first a word and the rest `<verb>-<name>`; a
# placeholder, as `just check-<name>`, names none.
JUST = re.compile(
    r"(?:^|&&|\|\||;)\s*(?:[A-Z_][A-Z0-9_]*=\S*\s+)*(?:mise\s+exec\s+--\s+)?just\s+"
    r"([a-z][a-z0-9-]*[a-z0-9](?![\w<-])(?:[ \t]+[a-z][a-z0-9]*-[a-z0-9-]*[a-z0-9](?![\w<-]))*)",
    re.M,
)
# What a template renders: a tag, a comment or an expression.
TEMPLATED = re.compile(r"\{[%#{]")
# What a template shows as text, a raw block's body, and what it drops, a comment: a tag in either
# is none.
QUOTED = re.compile(r"\{%-?\s*raw\s*-?%\}(?P<raw>.*?)\{%-?\s*endraw\s*-?%\}|\{#.*?#\}", re.DOTALL)
# A template's line that is only a tag or a comment, which renders to nothing: one, so a line that
# holds text between two tags is not.
TAG = re.compile(r"^\s*(?:\{%(?:(?!%\}).)*%\}|\{#(?:(?!#\}).)*#\})\s*$")
# A template's conditions: what opens, turns and closes one, what a condition names, and a
# variable that holds another layer's features.
TAGS = re.compile(r"\{%-?\s*(if|elif|else|endif|for|endfor|set)\b(.*?)-?%\}", re.DOTALL)
ACTIVE = re.compile(r'"([a-z0-9-]+)"\s+in\s+devset\.profiles')
OWN = re.compile(r'"([a-z0-9-]+)"\s+in\s+devset\.features')
ON = re.compile(r'"([a-z0-9-]+)"\s+in\s+([a-z_]+)\b')
LAYER = re.compile(
    r'([a-z_]+)\s*=\s*devset\.layers\s*\|\s*selectattr\(\s*"profile",\s*"equalto",\s*"([a-z0-9-]+)"'
)
# A condition that holds nothing it names: one of several alternatives, or a negation. What it and
# an `else` hold instead, which a finding under one says.
EITHER = re.compile(r"(?<![\w-])(?:or|not)(?![\w-])")
VOID = ("void",)
NESTED = "; an `or`, a `not` or an `else` holds nothing it names: nest an `if` instead"
# What a finding in a file that is no template adds: its conditions ship as text.
TEMPLATE = ", and mark the file `template = true` in profile.toml"


class Page:
    """A file `profile` gives an agent to read, at `path` in the target, shipped as `entry`: what is
    there whatever the conditions, and, in a template, what the conditions at each offset hold."""

    def __init__(self, profile, path, entry, text):
        when = entry.get("when", {})
        required = {name for name, spec in profile.requires.items() if not spec.get("optional")}
        self.profile = profile
        self.path = path
        self.template = entry.get("template", False)
        self.features = set(when.get("features", []))
        self.present = {profile.name, *when.get("profiles", []), *required}
        self.own = path.removeprefix(SKILLS).split("/")[0] if path.startswith(SKILLS) else None
        self.text = text
        if self.template:
            # A template's comments render to nothing, but its raw text is read.
            self.scanned = masked(blanked(text, comments=True))
            self.conditions = conditions(blanked(text, raw=True, comments=True))
        else:
            self.scanned, self.conditions = text, ([0], [frozenset()])

    def at(self, offset):
        """The conditions in force at `offset`."""
        starts, held = self.conditions
        return held[bisect.bisect_right(starts, offset) - 1]

    def advice(self, held):
        """What a gate finding under the conditions `held` adds: to make the file a template, or to
        nest the innermost condition, which holds nothing."""
        if not self.template:
            return TEMPLATE
        return NESTED if VOID in held else ""


def shipped_skills(found):
    """Each skill the profiles `found` ship, by name: the profile that ships it, and the features it
    ships with."""
    return {
        skill.group(1): (profile.name, set(entry.get("when", {}).get("features", [])))
        for profile in found
        for path, entry in profile.files.items()
        if (skill := SKILL.match(path))
    }


def agent_read_problems(profile, definers, shipped, spine):
    """Each way what `profile` gives an agent to read breaks the form: a skill's front matter,
    files and fences, and a recipe or skill it names where that one may be absent. `definers`
    gives the profile that defines each recipe, `shipped` what `shipped_skills` gives, and `spine`
    the recipes every repository has."""
    where, out = profile.path, []
    for path, entry in profile.files.items():
        if not path.startswith(READ):
            continue
        page = Page(profile, path, entry, (profile.path / "files" / path).read_text())
        if skill := SKILL.match(path):
            name = skill.group(1)
            out += [f"{where}: {path}: {problem}" for problem in front_matter(name, page.text)]
            out += [f"{where}: {problem}" for problem in reference_problems(profile, name)]
        out += [f"{where}: {path}: {problem}" for problem in fence_problems(page)]
        out += [
            f"{where}: {path} {problem}"
            for problem in gate_problems(page, definers, shipped, spine)
        ]
    return out


def gate_problems(page, definers, shipped, spine):
    """Each recipe or skill that `page` names in its code where that one may be absent."""
    out = []
    for span in CODE.finditer(page.scanned):
        part = "inline" if span.group("span") else "body"
        snippet, start = span.group(part), span.start(part)
        out += recipe_gate_problems(page, snippet, start, definers, spine)
        if part == "inline":
            out += skill_gate_problems(page, snippet.removeprefix("/"), start, shipped)
    return out


def recipe_gate_problems(page, snippet, start, definers, spine):
    """Each recipe that `snippet`, at `start` in `page`, runs where the profile that defines it may
    be absent: another profile's, with no condition in force on it; or that no profile defines."""
    out = []
    for match in JUST.finditer(snippet):
        held = page.at(start + match.start(1))
        for recipe in match.group(1).split():
            owner = definers.get(recipe)
            if recipe in spine or owner in page.present:
                continue
            if owner is None:
                out.append(f"names `just {recipe}`, which no profile of the collection defines")
            elif not active(owner, held):
                out.append(
                    f"names `just {recipe}`, which {owner} defines: gate it on"
                    f' `"{owner}" in devset.profiles`{page.advice(held)}'
                )
    return out


def skill_gate_problems(page, name, start, shipped):
    """Where `name`, a code span at `start` in `page`, is a skill that may be absent: one of
    `page`'s profile that ships with a feature no condition holds, or another profile's, with no
    condition on the feature that ships it, or on its profile where it ships with none. A skill
    may name itself."""
    if name not in shipped or name == page.own:
        return []
    owner, features = shipped[name]
    held = page.at(start)
    if owner == page.profile.name:
        lacking = sorted(features - page.features - {c[1] for c in held if c[0] == "feature"})
        if not lacking:
            return []
        return [
            f"names `{name}`, which ships only with its {code(lacking)}: gate it on"
            f' `"{lacking[0]}" in devset.features`{page.advice(held)}'
        ]
    lacking = sorted(feature for feature in features if ("layer", owner, feature) not in held)
    if lacking:
        return [
            f"names `{name}`, which ships only with {owner}'s {code(lacking)}: gate it on that"
            " feature, through `devset.layers`: `{%- set <v> = devset.layers |"
            f' selectattr("profile", "equalto", "{owner}") | map(attribute="features") | first |'
            f' default([]) -%}}`, then `{{%- if "{lacking[0]}" in <v> %}}`{page.advice(held)}'
        ]
    if owner not in page.present and not active(owner, held):
        return [
            f"names `{name}`, which {owner} ships: gate it on"
            f' `"{owner}" in devset.profiles`{page.advice(held)}'
        ]
    return []


def active(owner, held):
    """Whether the conditions `held` hold the profile `owner` active: by name, or by a feature."""
    return any(condition[0] in ("profile", "layer") and condition[1] == owner for condition in held)


def blanked(text, raw=False, comments=False):
    """`text` with each template comment blanked where `comments`, and each raw block's text where
    `raw`: a tag in either is none. Newlines stay, so every offset does."""
    out, last = [], 0
    for match in QUOTED.finditer(text):
        if match.group("raw") is None and comments:
            start, end = match.span()
        elif match.group("raw") is not None and raw:
            start, end = match.span("raw")
        else:
            continue
        out += [text[last:start], re.sub(r"[^\n]", " ", text[start:end])]
        last = end
    return "".join(out) + text[last:]


def masked(text):
    """`text` with each line that is only a template's tag or comment blanked, which renders to
    nothing: what it says is not the file's. Each offset stays where it was."""
    return "".join(
        re.sub(r"[^\n]", " ", line) if TAG.match(line) else line
        for line in text.splitlines(keepends=True)
    )


def conditions(text):
    """The conditions in force from each offset of `text` on, as the offset each span starts at and
    what it holds: `("profile", p)` where the profile `p` is active, `("layer", p, f)` where its
    feature `f` is on, `("feature", f)` where this profile's is, and `VOID` where the innermost
    condition holds nothing, an `or` or a `not`, or is an `else`. A `for` holds nothing, and its
    `else` is its own."""
    layers, frames, starts, held = {}, [], [0], [frozenset()]
    for tag in TAGS.finditer(text):
        kind, rest = tag.group(1), tag.group(2)
        if kind == "set":
            if layer := LAYER.search(rest):
                layers[layer.group(1)] = layer.group(2)
            continue
        named = frozenset({VOID})
        if not EITHER.search(rest):
            named = frozenset(
                {("profile", p) for p in ACTIVE.findall(rest)}
                | {("feature", f) for f in OWN.findall(rest)}
                | {("layer", layers[v], f) for f, v in ON.findall(rest) if v in layers}
            )
        if kind in ("if", "for"):
            frames.append([kind, named if kind == "if" else frozenset()])
        elif kind == "elif" and frames:
            frames[-1][1] = named
        elif kind == "else" and frames:
            frames[-1][1] = frozenset({VOID}) if frames[-1][0] == "if" else frozenset()
        elif kind in ("endif", "endfor") and frames:
            frames.pop()
        innermost = frames[-1][1] if frames else frozenset()
        starts.append(tag.end())
        held.append(
            frozenset().union(*(frame[1] - {VOID} for frame in frames)) | innermost & {VOID}
        )
    return starts, held


def fence_problems(page):
    """Each Rust block of `page` marked other than `rust` or `rust,compile_fail`, a failing block
    that does not say what it fails with, and, in a template, a Rust block that holds template
    syntax, where no raw block wraps it whole: each is compiled as it stands."""
    shown = blanked(page.text, raw=True) if page.template else None
    out = []
    for fence in FENCE.finditer(page.text):
        # A Rust block is found in any case, and marked in one.
        info = fence.group("info").strip()
        kind = info.lower()
        line = page.text.count("\n", 0, fence.start()) + 1
        if (kind.startswith("rust") or kind.split(",")[0] == "rs") and info not in RUST:
            out.append(
                f"line {line}: a Rust block is `rust` or `rust,compile_fail`, never `{info}`"
            )
        if info == FAILING and not FAILS.match(fence.group("body")):
            out.append(f"line {line}: a failing block opens `// fails: <lint or error code>`")
        if page.template and info in RUST and TEMPLATED.search(shown, *fence.span("body")):
            out.append(
                f"line {line}: a Rust block holds no template syntax: to show it as written, wrap"
                " the whole block in `{% raw %}`"
            )
    return out


def front_matter(name, text):
    """Each way the front matter and body of the skill `name`'s SKILL.md, `text`, break the form: a
    guide's, or a pass's where it runs forked."""
    text = text.replace("\r\n", "\n")
    block = FRONT_MATTER.match(text)
    fields = dict(field(line) for line in block.group(1).splitlines()) if block else {}
    if "context" in fields:
        wrong = [f"`{k}: {fields[k]}`" for k, v in PASS_RUNS.items() if fields.get(k, v) != v]
        if PASS - set(fields) or set(fields) - PASS - PASS_MAY or wrong:
            return [
                f"a pass runs forked: its front matter holds {code(sorted(PASS))}, with "
                "`context: fork`, `model: inherit` and `background: false`, and may hold "
                f"`allowed-tools`{differences(fields, PASS, PASS_MAY, wrong)}"
            ]
        if fields["agent"] not in PASS_AGENTS:
            return [f"a pass runs on {code(sorted(PASS_AGENTS))}, not `{fields['agent']}`"]
        shape, example = IMPERATIVE, "an imperative such as `review-rust`"
    else:
        if set(fields) != GUIDE:
            return [
                f"a guide's front matter holds {code(sorted(GUIDE))}, each on one line, and"
                f" nothing else{differences(fields, GUIDE)}"
            ]
        shape, example = GERUND, "a gerund phrase such as `writing-rustdoc`"
    out = []
    if fields["name"] != name or not shape.fullmatch(name):
        out.append(f"`name` is `{name}`, its directory, {example}")
    description = fields["description"]
    if not description.startswith("Use when") or len(description) >= DESCRIPTION:
        out.append(f"`description` starts `Use when`, under {DESCRIPTION} characters")
    if len(text) - block.end() > BODY:
        out.append(f"the body is over {BODY} characters: move depth into `references/`")
    return out


def field(line):
    """A front matter line's field and its value, each stripped, the value of its quotes too."""
    key, _, value = line.partition(":")
    value = value.strip()
    if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return key.strip(), value


def differences(fields, wanted, may=(), wrong=()):
    """How the front matter `fields` differs from the `wanted` fields, with those it `may` hold,
    and the values it has `wrong`: what a finding adds, empty where there is nothing to add."""
    parts = []
    if lacks := sorted(set(wanted) - set(fields)):
        parts.append(f"lacks {code(lacks)}")
    if extra := sorted(set(fields) - set(wanted) - set(may)):
        parts.append(f"holds {code(extra)}")
    if wrong:
        parts.append(f"has {', '.join(wrong)}")
    return f"; this one {', '.join(parts)}" if parts else ""


def reference_problems(profile, skill):
    """Each file of the skill that the profile does not declare, each reference its SKILL.md does
    not name, by a link or in code, and each relative link in the skill that leads outside what its
    profile ships: a skill of another profile is named, never linked. A dot file and Python's cache
    are no file of the skill."""
    root = f"{SKILLS}{skill}/"
    declared = {path for path in profile.files if path.startswith(root)}
    base = profile.path / "files"
    on_disk = {
        found.relative_to(base).as_posix()
        for found in (base / root).rglob("*")
        if found.is_file()
        and not any(
            part.startswith(".") or part == "__pycache__"
            for part in found.relative_to(base / root).parts
        )
    }
    out = [f"{path} is not an entry of profile.toml" for path in sorted(on_disk - declared)]
    body = (base / root / "SKILL.md").read_text()
    spans = [span.group("inline") for span in CODE.finditer(body) if span.group("span")]
    named = {os.path.normpath(root + target) for target in links(body) + spans}
    out += [
        f"{path} is named nowhere in its SKILL.md, so no agent reads it"
        for path in sorted(declared)
        if path.startswith(root + "references/") and path.endswith(".md") and path not in named
    ]
    for path in sorted(declared & on_disk):
        if not path.endswith(".md"):
            continue
        here = os.path.dirname(path)
        for target in links((base / path).read_text()):
            resolved = os.path.normpath(os.path.join(here, target))
            if resolved not in profile.files:
                out.append(f"{path} links `{target}`, which its profile does not ship")
    return out


def links(text):
    """The target of each relative link in `text`, outside its code: a link in a Rust example is
    rustdoc's, not the skill's."""
    return LINK.findall(CODE.sub("", text))


def code(names):
    """`names`, each in backticks, comma-separated."""
    return ", ".join(f"`{name}`" for name in names)
