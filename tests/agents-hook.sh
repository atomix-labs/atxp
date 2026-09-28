#!/usr/bin/env bash
# The agents profile's hooks through the turns they tell apart: one that changes nothing on a tree
# that already differs from HEAD, one that breaks the check, a stop again with nothing changed, a
# fix, a commit, and machines without mise or just. mise and just are stubs, so only the hook is
# tested; mise is found where the installer puts it, off PATH, as in a hook's shell.
#
# Run in atxp's root, with git and python3.
set -euo pipefail

script=$PWD/profiles/agents/agents/files/.claude/hooks/check.sh
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

# `mise exec -- <command>` runs the command; `just check` fails while `broken` says yes, with the
# line Claude Code once took for a hook script gone missing.
mkdir -p "$work/home/.local/bin" "$work/just" "$work/bare" "$work/repo"
cat > "$work/home/.local/bin/mise" << 'EOF'
#!/bin/sh
[ "$1" = exec ] && shift 2 && exec "$@"
EOF
cat > "$work/just/just" << 'EOF'
#!/bin/sh
if [ "$1" = check ] && grep -qs yes broken; then
    echo "env: 'tool': No such file or directory" >&2
    exit 1
fi
EOF
cp "$work/just/just" "$work/home/.local/bin/just"
chmod +x "$work/home/.local/bin/"* "$work/just/just"

cd "$work/repo"
git init -q
git config user.name suite
git config user.email suite@example.com
printf 'one\n' > file
git add file
git commit -qm one
printf 'two\n' >> file

home=$work/home path=/usr/bin:/bin failed=0
# Runs the hook as Claude Code does, and checks its answer: nothing, or a JSON object with the key.
expect() {
    local want=$1 what=$2 answer status=0
    shift 2
    answer=$(env -i HOME="$home" PATH="$path" CLAUDE_PROJECT_DIR="$work/repo" bash "$script" "$@" \
        <<< '{"session_id":"suite"}' 2> /dev/null) || status=$?
    if ((status)); then
        echo "FAILED: $what: the hook exited $status, where Claude Code reads only its answer"
        failed=1
    elif [[ -z $want && -z $answer ]] || { [[ -n $want ]] && python3 -c \
        'import json, sys; assert sys.argv[2] in json.loads(sys.argv[1])' \
        "$answer" "$want" 2> /dev/null; }; then
        echo "ok: $what"
    else
        echo "FAILED: $what: expected ${want:-nothing}, got: $answer"
        failed=1
    fi
}

expect "" "a prompt notes the state" start
expect "" "a turn that changes nothing ends at once"
expect "" "a prompt notes the state" start
echo yes > broken
expect decision "a turn that breaks the check is blocked"
expect "" "a stop with nothing changed since the block ends"
echo no > broken
expect "" "a fix passes the check"
expect "" "a prompt notes the state" start
git add -A
git commit -qm broken
echo yes > broken
git commit -qam broken
expect decision "a commit that breaks the check is blocked"

home=$work/bare path=$work/just:/usr/bin:/bin
mkdir -p .config/mise
expect "" "a prompt notes the state" start
echo three >> file
expect systemMessage "without mise, where the repository uses it, the user is told"
rm -r .config
path=/usr/bin:/bin
expect "" "a prompt notes the state" start
echo four >> file
expect systemMessage "without just, the user is told"
exit "$failed"
