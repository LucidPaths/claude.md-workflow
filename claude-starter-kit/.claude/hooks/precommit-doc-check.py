#!/usr/bin/env python3
"""
PreCommit Documentation Check — Fires before git commit via PreToolUse

When Claude is about to run `git commit`, checks if code files are staged
but no documentation files are. If so, blocks and reminds to update docs.

Project-agnostic — works with any repo and tech stack. Python stdlib only.
"""

import json
import sys
import os
import subprocess


# Code file extensions that warrant a doc check.
CODE_EXTENSIONS = {
    '.py', '.ts', '.tsx', '.js', '.jsx',
    '.rs', '.go', '.java', '.rb', '.php',
    '.c', '.cpp', '.h', '.swift', '.kt',
    '.css', '.html', '.toml', '.yaml', '.yml',
}

# Documentation file patterns — if ANY of these are staged, docs are covered.
DOC_PATTERNS = {
    'README', 'CLAUDE', 'ROADMAP', 'TODO', 'CHANGELOG',
    'WORKING_STATE', 'CONTRIBUTING', 'ARCHITECTURE',
}
DOC_EXTENSIONS = {'.md', '.rst', '.txt'}


def is_git_commit(command):
    """Check if a bash command is a git commit."""
    cmd = command.strip()
    # Match: git commit, git commit -m, git commit -am, etc.
    # Don't match: git commit --amend (different intent, user already decided)
    return cmd.startswith('git commit') and '--amend' not in cmd


def get_staged_files():
    """Get list of staged files from git."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split('\n')
    except Exception:
        pass
    return []


def is_code_file(filepath):
    """Check if a file is a code file by extension."""
    return os.path.splitext(filepath)[1].lower() in CODE_EXTENSIONS


def is_doc_file(filepath):
    """Check if a file is a documentation file."""
    basename = os.path.basename(filepath)
    name, ext = os.path.splitext(basename)
    # Check extension
    if ext.lower() in DOC_EXTENSIONS:
        return True
    # Check known doc filenames (with any extension)
    return name.upper() in DOC_PATTERNS


def is_test_only(code_files):
    """Check if all code files are test files."""
    test_indicators = ['test', 'spec', '__test__', '.test.', '.spec.', '_test.']
    return all(
        any(ind in f.lower() for ind in test_indicators)
        for f in code_files
    )


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    # Only trigger on Bash tool with git commit commands
    tool_name = data.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    command = tool_input.get("command", "")

    if not is_git_commit(command):
        sys.exit(0)

    # Get staged files
    staged = get_staged_files()
    if not staged:
        sys.exit(0)

    code_files = [f for f in staged if is_code_file(f)]
    doc_files = [f for f in staged if is_doc_file(f)]

    # No code files staged → no doc check needed
    if not code_files:
        sys.exit(0)

    # Test-only commits don't need doc updates
    if is_test_only(code_files):
        sys.exit(0)

    # Code files staged AND doc files staged → good
    if doc_files:
        sys.exit(0)

    # Code files staged but NO doc files → remind
    file_list = "\n".join("  - " + f for f in code_files[:8])
    if len(code_files) > 8:
        file_list += f"\n  - ... and {len(code_files) - 8} more"

    output = {
        "decision": "block",
        "reason": (
            "DOC CHECK: Code files are staged but no documentation files.\n\n"
            f"Staged code files:\n{file_list}\n\n"
            "Before committing, check if any docs need updating:\n"
            "  - README.md — if user-facing behavior changed\n"
            "  - CLAUDE.md — if coding patterns or project instructions changed\n"
            "  - ROADMAP.md — if feature status changed\n\n"
            "If docs are already up to date, add a brief note in the commit message "
            "explaining why no doc changes are needed, then re-run the commit."
        )
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
