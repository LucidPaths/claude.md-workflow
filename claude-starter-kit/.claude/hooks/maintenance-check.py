#!/usr/bin/env python3
"""
Maintenance Check Hook — Run before session ends

Checks if code files were modified during the session and reminds
Claude to update relevant documentation before stopping.

The stop hook is what makes documentation maintenance automatic
rather than discipline-dependent. Without it, docs drift.

Adapted from https://github.com/vincitamore/claude-org-template
Original author: vincitamore (MIT License)
"""

import json
import sys
import os
import subprocess

# Minimum transcript lines before triggering maintenance check.
# Avoids nagging on quick single-command sessions.
TRIVIAL_SESSION_THRESHOLD = 15

# Code file extensions that trigger the doc update reminder.
CODE_EXTENSIONS = {
    '.py', '.ts', '.tsx', '.js', '.jsx',
    '.rs', '.go', '.java', '.rb', '.php',
    '.c', '.cpp', '.h', '.swift', '.kt',
    '.css', '.html', '.toml', '.yaml', '.yml',
}


def get_project_root():
    """Get project root from environment or by walking up from this script."""
    env_root = os.environ.get('CLAUDE_PROJECT_DIR')
    if env_root and os.path.isdir(env_root):
        return env_root
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_modified_files(project_root):
    """Check git for modified files (staged + unstaged) since last commit."""
    files = []
    try:
        # Unstaged changes
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD'],
            capture_output=True, text=True, cwd=project_root, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            files.extend(result.stdout.strip().split('\n'))

        # Staged but uncommitted
        result2 = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True, text=True, cwd=project_root, timeout=5
        )
        if result2.returncode == 0 and result2.stdout.strip():
            files.extend(result2.stdout.strip().split('\n'))
    except Exception:
        pass
    return list(set(files))


def has_code_changes(files):
    """Check if any modified files are code files."""
    return any(
        os.path.splitext(f)[1].lower() in CODE_EXTENSIONS
        for f in files
    )


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    # Check transcript length — skip trivial sessions
    transcript_path = data.get("transcript_path")
    if not transcript_path or not os.path.exists(transcript_path):
        sys.exit(0)

    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            content = f.read()
            line_count = content.count('\n')
    except Exception:
        sys.exit(0)

    if line_count < TRIVIAL_SESSION_THRESHOLD:
        sys.exit(0)

    # Check if Claude already stated "No maintenance needed"
    recent = content[-2000:] if len(content) > 2000 else content
    if "No maintenance needed" in recent:
        sys.exit(0)

    # Check for code changes
    project_root = get_project_root()
    modified = get_modified_files(project_root)

    if not has_code_changes(modified):
        sys.exit(0)

    # Build the reminder
    code_files = [
        f for f in modified
        if os.path.splitext(f)[1].lower() in CODE_EXTENSIONS
    ]

    file_list = "\n".join("- " + f for f in code_files[:10])
    if len(code_files) > 10:
        file_list += f"\n- ... and {len(code_files) - 10} more"

    output = {
        "decision": "block",
        "reason": (
            "MAINTENANCE CHECK\n\n"
            f"Code files were modified this session:\n{file_list}\n\n"
            "Before stopping, check if any documentation needs updating:\n\n"
            "| If this changed...       | Update...                          |\n"
            "|--------------------------|------------------------------------||\n"
            "| Features or behavior     | README.md (user-facing docs)       |\n"
            "| Build process or setup   | CLAUDE.md (dev instructions)       |\n"
            "| Code patterns or lessons | CLAUDE.md (coding standards)       |\n"
            "| API or interface changes | docs/ (API documentation)          |\n\n"
            'If docs are already up to date, state "No maintenance needed" and stop.\n'
            "If ANY need updating: do it now. Lost context is unrecoverable."
        )
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
