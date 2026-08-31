#!/usr/bin/env bash
# install-guards.sh — put hard don'ts in git, not in prompts.
#
# Models forget instructions; git hooks don't. This installs:
#   pre-push   — blocks pushes to protected branches (default: main master)
#   pre-commit — blocks commits touching paths listed in .claude/protected-paths.txt
#
# Usage:
#   bash guards/install-guards.sh                 # protect main + master
#   bash guards/install-guards.sh main release    # custom protected branches
#
# Escape hatches are deliberate and explicit (a human decision, not a phrase
# a model can emit mid-session):
#   ALLOW_PROTECTED_PUSH=1 git push ...
#   ALLOW_PROTECTED_PATHS=1 git commit ...
#
# Re-running is safe: hooks installed by this script are overwritten in place.
# A pre-existing hook NOT installed by this script is left untouched and
# reported, so we never silently clobber someone's setup.

set -euo pipefail

PROTECTED_BRANCHES="${*:-main master}"
MARKER="# installed-by: claude-starter-kit install-guards.sh"

hooks_dir="$(git rev-parse --git-path hooks)"
mkdir -p "$hooks_dir"

install_hook() {
    local name="$1" content="$2" target="$hooks_dir/$1"
    if [[ -f "$target" ]] && ! grep -qF "$MARKER" "$target"; then
        echo "SKIP  $name — existing hook not installed by this script: $target"
        echo "      Merge manually or remove it, then re-run."
        return 0
    fi
    printf '%s\n' "$content" > "$target"
    chmod +x "$target"
    echo "OK    $name installed → $target"
}

# --- pre-push: block pushes to protected branches ---------------------------
pre_push_content="#!/usr/bin/env bash
$MARKER
# Blocks pushes to protected branches. Override: ALLOW_PROTECTED_PUSH=1 git push
set -euo pipefail
PROTECTED=\"$PROTECTED_BRANCHES\"
[[ \"\${ALLOW_PROTECTED_PUSH:-0}\" == \"1\" ]] && exit 0
while read -r _local_ref _local_sha remote_ref _remote_sha; do
    branch=\"\${remote_ref#refs/heads/}\"
    for p in \$PROTECTED; do
        if [[ \"\$branch\" == \"\$p\" ]]; then
            echo \"BLOCKED: push to protected branch '\$p'.\" >&2
            echo \"Push a feature branch and open a PR instead.\" >&2
            echo \"Human override: ALLOW_PROTECTED_PUSH=1 git push ...\" >&2
            exit 1
        fi
    done
done
exit 0"

# --- pre-commit: block commits touching protected paths ----------------------
pre_commit_content="#!/usr/bin/env bash
$MARKER
# Blocks commits touching paths listed in .claude/protected-paths.txt
# (one path prefix per line, # comments allowed).
# Override: ALLOW_PROTECTED_PATHS=1 git commit
set -euo pipefail
[[ \"\${ALLOW_PROTECTED_PATHS:-0}\" == \"1\" ]] && exit 0
root=\"\$(git rev-parse --show-toplevel)\"
list=\"\$root/.claude/protected-paths.txt\"
[[ -f \"\$list\" ]] || exit 0
staged=\"\$(git diff --cached --name-only)\"
[[ -n \"\$staged\" ]] || exit 0
violations=\"\"
while IFS= read -r pattern; do
    pattern=\"\${pattern%%#*}\"
    pattern=\"\$(echo \"\$pattern\" | xargs)\"
    pattern=\"\${pattern%/}\"
    [[ -n \"\$pattern\" ]] || continue
    while IFS= read -r file; do
        if [[ \"\$file\" == \"\$pattern\" || \"\$file\" == \"\$pattern\"/* ]]; then
            violations=\"\$violations  \$file (protected: \$pattern)\\n\"
        fi
    done <<< \"\$staged\"
done < \"\$list\"
if [[ -n \"\$violations\" ]]; then
    echo \"BLOCKED: commit touches protected paths:\" >&2
    printf '%b' \"\$violations\" >&2
    echo \"These paths are listed in .claude/protected-paths.txt.\" >&2
    echo \"Human override: ALLOW_PROTECTED_PATHS=1 git commit ...\" >&2
    exit 1
fi
exit 0"

install_hook "pre-push" "$pre_push_content"
install_hook "pre-commit" "$pre_commit_content"

echo ""
echo "Protected branches: $PROTECTED_BRANCHES"
if [[ -f "$(git rev-parse --show-toplevel)/.claude/protected-paths.txt" ]]; then
    echo "Protected paths:    .claude/protected-paths.txt (active)"
else
    echo "Protected paths:    none (create .claude/protected-paths.txt to enable)"
fi
