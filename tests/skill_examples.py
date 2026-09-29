"""Compiles every Rust example the collection's skills show, in a workspace the rust bundle writes
with `strict` and `nightly`: a `rust` block passes clippy and nightly's lints, and a
`rust,compile_fail` block fails with the lint or error code its first line names. The lints that
ask for docs are allowed, since an example leaves its docs out to stay short: `missing_docs`, and
clippy's `missing_docs_in_private_items`, `missing_errors_doc`, `missing_panics_doc` and
`missing_safety_doc`.

Usage: skill_examples.py [<skill>...]

Run in atxp's root, with git, devset, just and the toolchain the bundle pins; $DEVSET, a path, runs
another build of devset. With skills named, compiles only their examples; a name no profile ships
fails.

Each example is a crate of the workspace, a binary where it has a `main`, with the crates its code
names. Every `rust` block compiles in one run, and each failure points at the example's own file
and line; each `rust,compile_fail` block compiles alone. A template's block compiles as its source
stands: the catalog check holds template syntax out of every Rust block, so each renders as written.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, "profiles/devset/devset-collection/files/.just/devset-collection")
from skill_form import FAILING, FAILS, FENCE, RUST, SKILLS, code, shipped_skills

from catalog import profiles

# The repository the examples compile in, and how the bundle is applied to it.
FIXTURE = Path("tests/fixtures/workspace")
BUNDLE = ("add", "atxp/rust", "--features", "strict,nightly", "--var", "repository=example/skills")
# The lints that ask for docs, which an example leaves out: the two the lint table names, taken out
# of it, and the three clippy's groups deny, allowed at the head of its clippy table.
UNDOCUMENTED = re.compile(r"^(?:missing_docs|missing_docs_in_private_items)\s*=.*\n", re.M)
UNDOCUMENTED_IN_GROUPS = ("missing_errors_doc", "missing_panics_doc", "missing_safety_doc")
CLIPPY_TABLE = "[workspace.lints.clippy]\n"
# The crates an example may name, each as its manifest takes it.
DEPENDENCIES = {
    "thiserror": 'thiserror = { version = "2", default-features = false }',
    "derive_more": 'derive_more = { version = "2", features = ["debug", "display"] }',
    "tokio": 'tokio = { version = "1", features = ["full"] }',
}
# An example's manifest: the workspace's package fields and lints, and the crates it names.
MANIFEST = """\
[package]
name = "example-{n}"
version.workspace = true
edition.workspace = true
rust-version.workspace = true
publish.workspace = true

[lints]
workspace = true

[dependencies]
{dependencies}"""
# The recipes that compile the workspace: clippy, and the lints only nightly has.
CHECKS = ("check-rust-clippy", "check-rust-lints")
# An example that has a `main` is a binary.
MAIN = re.compile(r"^(?:async\s+)?fn main\(", re.M)
# Where the compiler points into an example's crate, and an example's crate that did not compile.
LOCATION = re.compile(r"crates/example-(\d+)/src/(?:lib|main)\.rs:(\d+)(?::(\d+))?")
UNBUILT = re.compile(r"could not compile `example-(\d+)`")
# Cargo's line for each crate it starts, which says nothing of an example.
PROGRESS = re.compile(r"^ +(?:Checking|Compiling) .*\n", re.M)
# An error code, which a failing block may name in place of a lint.
ERROR_CODE = re.compile(r"E\d{4}")
# A line of source the compiler quotes, or a change to it that it suggests: it names nothing the
# compiler failed with.
SOURCE_LINE = re.compile(r"^\s*\d*\s*[|+~-]")
# What the compiler says a diagnostic failed with: its error code, or the lint it names as denied.
FAILED_WITH = re.compile(
    "|".join(
        (
            r"error\[(E\d{4})\]",
            r"`-D ([\w:-]+)` implied by",
            r"requested on the command line with `-D ([\w:-]+)`",
            r"`#\[deny\(([\w:]+)\)\]` on by default",
        )
    )
)


@dataclass(frozen=True)
class Example:
    """A Rust block of a skill: its file, the line its fence opens on, whether it must fail, its
    code as a crate holds it, and the indent that code lost."""

    path: Path
    line: int
    fails: bool
    code: str
    indent: int

    def at(self, line, column):
        """Where line `line`, column `column` of its code is in its file."""
        return f"{self.path}:{self.line + line}" + (f":{column + self.indent}" if column else "")

    @property
    def expected(self):
        """What a failing block names on its first line, or None where it names nothing."""
        first = FAILS.match(self.code)
        return first.group("failure") if first else None


def examples(found, only):
    """Every Rust block of every skill the profiles `found` ship, or of each skill in `only` where
    it names any, in the order of their files."""
    out = []
    for profile in found:
        for path in profile.files:
            skill = path.removeprefix(SKILLS).split("/")[0]
            if path.startswith(SKILLS) and path.endswith(".md") and (not only or skill in only):
                out += blocks(profile.path / "files" / path)
    return sorted(out, key=lambda example: (str(example.path), example.line))


def blocks(source):
    """Each Rust block of the file at `source`, as its source stands."""
    text = source.read_text()
    out = []
    for fence in FENCE.finditer(text):
        info = fence.group("info").strip()
        if info not in RUST:
            continue
        body = fence.group("body")
        lines = [line for line in body.splitlines() if line.strip()]
        indent = min((len(line) - len(line.lstrip()) for line in lines), default=0)
        line = text.count("\n", 0, fence.start()) + 1
        out.append(Example(source, line, info == FAILING, textwrap.dedent(body), indent))
    return out


def run(command, work, env):
    """`command`, run in `work` with `env`, what it says captured."""
    return subprocess.run(command, cwd=work, env=env, capture_output=True, text=True)


def workspace(work, env):
    """The fixture at `work`, with the rust bundle applied, the lints that ask for docs allowed."""
    shutil.copytree(FIXTURE, work)
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=work, check=True)
    devset = os.environ.get("DEVSET", "devset")
    source = str(Path.cwd() / "profiles")
    command = [devset, "-q", "--no-input", *BUNDLE, "--path", source]
    subprocess.run(command, cwd=work, env=env, check=True)
    manifest = work / "Cargo.toml"
    allowed = "".join(f'{lint} = "allow"\n' for lint in UNDOCUMENTED_IN_GROUPS)
    text = UNDOCUMENTED.sub("", manifest.read_text())
    manifest.write_text(text.replace(CLIPPY_TABLE, CLIPPY_TABLE + allowed))


def crate(work, n, example):
    """The `n`th example as a crate of the workspace at `work`, with each crate its code names."""
    home = work / "crates" / f"example-{n}"
    (home / "src").mkdir(parents=True)
    text = example.code
    (home / "src" / ("main.rs" if MAIN.search(text) else "lib.rs")).write_text(text)
    named = [spec for name, spec in DEPENDENCIES.items() if re.search(rf"\b{name}::", text)]
    dependencies = "".join(f"{spec}\n" for spec in named)
    (home / "Cargo.toml").write_text(MANIFEST.format(n=n, dependencies=dependencies))
    return home


def checked(work, env):
    """Whether the workspace at `work` passes clippy and nightly's lints, and what they said."""
    lock = run(["cargo", "generate-lockfile", "-q"], work, env)
    if lock.returncode:
        return False, lock.stderr
    said, ok = [], True
    for recipe in CHECKS:
        done = run(["just", recipe], work, env)
        said += [done.stdout, done.stderr]
        ok = ok and done.returncode == 0
    return ok, "".join(said)


def mapped(said, found):
    """What the compiler `said`, without cargo's progress, each place it points into an example's
    crate its file and line instead, and the examples it names."""
    named = {int(n) for n in UNBUILT.findall(said)}

    def place(location):
        n = int(location.group(1))
        named.add(n)
        column = int(location.group(3)) if location.group(3) else 0
        return found[n].at(int(location.group(2)), column)

    return LOCATION.sub(place, PROGRESS.sub("", said)), named


def told(said):
    """The lines of what the compiler `said` that are its own, not source it quotes or would
    change."""
    return [line for line in said.splitlines() if not SOURCE_LINE.match(line)]


def names(said, expected):
    """Whether the compiler, having `said` this, failed with `expected`, an error code or a lint:
    one it names in its own lines, whole, with cargo's dashes read as underscores, and not as the
    anchor of a lint's page."""
    if ERROR_CODE.fullmatch(expected):
        return f"error[{expected}]" in said
    lint = re.compile(rf"(?<![\w:#]){re.escape(expected)}(?!\w)")
    return any(lint.search(line.replace("-", "_")) for line in told(said))


def failures(said):
    """Each error code and denied lint the compiler, having `said` this, failed with, a lint's
    dashes as underscores."""
    found = FAILED_WITH.finditer("\n".join(told(said)))
    return sorted({next(filter(None, match.groups())).replace("-", "_") for match in found})


def passing_problems(work, env, found):
    """Each `rust` block of `found` that does not compile in the workspace at `work`, with why:
    all compile at once, and what the compiler says goes to stderr, pointed at the examples."""
    homes = [crate(work, n, example) for n, example in enumerate(found) if not example.fails]
    ok, said = checked(work, env)
    for home in homes:
        shutil.rmtree(home)
    if ok:
        return []
    said, named = mapped(said, found)
    print(said, file=sys.stderr)
    if not named:
        return [(None, "the workspace does not compile")]
    why = "does not compile: fix it, or mark a fragment `text`"
    return [(found[n], why) for n in sorted(named)]


def failing_problems(work, env, found):
    """Each `rust,compile_fail` block of `found` that does not fail as its first line says, in the
    workspace at `work`, with why: each compiles alone."""
    out = []
    for n, example in enumerate(found):
        expected = example.expected
        if not example.fails:
            continue
        if expected is None:
            out.append((example, "opens with no `// fails: <lint or error code>`"))
            continue
        home = crate(work, n, example)
        ok, said = checked(work, env)
        shutil.rmtree(home)
        if ok:
            out.append((example, f"compiles, but must fail with {expected}"))
        elif not names(said, expected):
            print(mapped(said, found)[0], file=sys.stderr)
            instead = ", ".join(failures(said)) or "nothing it names"
            out.append((example, f"fails, but not with {expected}: with {instead}"))
    return out


def main(only):
    """Compiles the examples of the skills in `only`, or of every skill, and names each that does
    not compile as its block says, by its file and line."""
    found = profiles()
    if unknown := sorted(only - shipped_skills(found).keys()):
        print(f"failed: no profile of the collection ships {code(unknown)}", file=sys.stderr)
        return 1
    shown = examples(found, only)
    with tempfile.TemporaryDirectory() as temp:
        work = Path(temp) / "workspace"
        # A recipe that reaches mise reads the workspace's configuration, trusted as the suite's.
        env = {**os.environ, "MISE_TRUSTED_CONFIG_PATHS": str(work), "MISE_YES": "1"}
        workspace(work, env)
        failed = passing_problems(work, env, shown) + failing_problems(work, env, shown)
    for example, why in failed:
        where = f"{example.path}:{example.line}: " if example else ""
        print(f"failed: {where}{why}", file=sys.stderr)
    if failed:
        return 1
    fails = sum(example.fails for example in shown)
    print(f"ok: {len(shown)} examples compiled, {fails} of them failing as their first lines say")
    return 0


if __name__ == "__main__":
    sys.exit(main(set(sys.argv[1:])))
