"""The one mise version atxp runs: the setup stub's pin and checksums, the mise profile's
`min_version`, and every workflow's mise-action.

Usage: mise-version.py check | bump [<report>]

`check` fails when they disagree, or when the stub's checksums are not the ones the release
publishes. `bump` moves them all to mise's newest release past the cooldown, and writes a Markdown
report.
"""

import re
import subprocess
import sys
import urllib.request
from pathlib import Path

STUB = Path("profiles/setup/files/setup.sh")
MINIMUM = Path("profiles/mise/files/.config/mise/conf.d/devset-mise.toml")
WORKFLOWS = ("profiles/*/files/.github/workflows/*.yml", ".github/workflows/*.yml")
# The stub's checksum names, and the release asset each is the sha256 of.
ASSETS = {
    "LINUX_X64": "linux-x64-musl",
    "LINUX_ARM64": "linux-arm64-musl",
    "MACOS_ARM64": "macos-arm64",
}
COOLDOWN = "3d"
VERSION = re.compile(r"^MISE_VERSION=(\S+)$", re.MULTILINE)
CHECKSUM = re.compile(r"^MISE_SHA256_([A-Z0-9_]+)=([0-9a-f]{64})$", re.MULTILINE)
MIN_VERSION = re.compile(r'^min_version = "([^"]+)"$', re.MULTILINE)
ACTION = re.compile(r"^(\s*)(- )?uses: jdx/mise-action@")
ACTION_VERSION = re.compile(r"^(\s+version:\s*)(\S+)$")


def stub():
    """The stub's mise version, and its checksum for each asset."""
    text = STUB.read_text()
    return VERSION.search(text).group(1), dict(CHECKSUM.findall(text))


def workflows():
    """Every workflow file: the payloads, and atxp's own."""
    return sorted(path for pattern in WORKFLOWS for path in Path().glob(pattern))


def steps(lines):
    """The lines of each mise-action step in `lines` after its `uses:`, as a range."""
    for at, line in enumerate(lines):
        step = ACTION.match(line)
        if not step:
            continue
        indent = len(step.group(1)) + (2 if step.group(2) else 0)
        end = at + 1
        while end < len(lines) and (not lines[end].strip() or len(lines[end]) - len(lines[end].lstrip()) >= indent):
            end += 1
        yield range(at + 1, end)


def versions(path):
    """The mise each mise-action step in `path` installs; `None` for one that takes the latest."""
    lines = path.read_text().splitlines()
    found = []
    for body in steps(lines):
        named = (ACTION_VERSION.match(lines[at]) for at in body)
        match = next((m for m in named if m), None)
        found.append(match.group(2).strip("\"'") if match else None)
    return found


def published(version):
    """The sha256 the release of `version` publishes for each of its assets."""
    url = f"https://github.com/jdx/mise/releases/download/v{version}/SHASUMS256.txt"
    request = urllib.request.Request(url, headers={"User-Agent": "atxp"})
    with urllib.request.urlopen(request) as response:
        text = response.read().decode()
    rows = (line.split() for line in text.splitlines() if line.strip())
    return {name.removeprefix("./"): digest for digest, name in rows}


def check():
    """Prints each disagreement, and fails if there is one."""
    problems = []
    version, sums = stub()
    minimum = MIN_VERSION.search(MINIMUM.read_text())
    if not minimum or minimum.group(1) != version:
        problems.append(f"{MINIMUM}: min_version must be {version}, the stub's mise")
    for path in workflows():
        problems += [f"{path}: mise-action installs {found or 'the latest mise'}, not {version}" for found in versions(path) if found != version]
    release = published(version)
    for key, asset in ASSETS.items():
        name = f"mise-v{version}-{asset}.tar.gz"
        if sums.get(key) != release.get(name):
            problems.append(f"{STUB}: MISE_SHA256_{key} is not the sha256 of {name}")
    for problem in problems:
        print(problem, file=sys.stderr)
    return 1 if problems else 0


def latest():
    """mise's newest release past the cooldown."""
    args = ["mise", "latest", "github:jdx/mise", "--minimum-release-age", COOLDOWN]
    out = subprocess.run(args, capture_output=True, text=True, check=True)
    return out.stdout.strip().removeprefix("v")


def repin(version):
    """Moves the stub, `min_version` and every mise-action step to `version`."""
    release = published(version)
    text = VERSION.sub(f"MISE_VERSION={version}", STUB.read_text())
    for key, asset in ASSETS.items():
        digest = release[f"mise-v{version}-{asset}.tar.gz"]
        text = re.sub(rf"^MISE_SHA256_{key}=\S+$", f"MISE_SHA256_{key}={digest}", text, flags=re.MULTILINE)
    STUB.write_text(text)
    MINIMUM.write_text(MIN_VERSION.sub(f'min_version = "{version}"', MINIMUM.read_text()))
    for path in workflows():
        lines = path.read_text().splitlines(keepends=True)
        for body in steps([line.rstrip("\n") for line in lines]):
            for at in body:
                lines[at] = ACTION_VERSION.sub(rf"\g<1>{version}", lines[at].rstrip("\n")) + "\n"
        path.write_text("".join(lines))


def bump(report):
    """Moves every pin of mise to its newest release past the cooldown, and reports."""
    have, _ = stub()
    want = latest()
    moved = [f"mise {have} -> {want}"] if want != have else []
    if moved:
        repin(want)
    text = "### mise\n\n" + ("".join(f"- {item}\n" for item in moved) or "Nothing to move.\n")
    if report:
        Path(report).write_text(text)
    else:
        print(text, end="")
    return 0


def main(args):
    match args:
        case ["check"]:
            return check()
        case ["bump", *report] if len(report) <= 1:
            return bump(report[0] if report else None)
    print(__doc__.strip().splitlines()[2], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
