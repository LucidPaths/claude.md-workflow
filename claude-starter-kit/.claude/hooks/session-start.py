#!/usr/bin/env python3
"""
Session Start Hook — Auto-orientation for new AI coding sessions

Provides the AI with current project state at session start:
- Working state from previous sessions (continuity memory)
- Current git branch and recent commits
- Uncommitted changes (with commit-count warning)
- Next steps from ROADMAP.md or TODO.md

Works with any AI coding assistant that supports session hooks.

Adapted from https://github.com/vincitamore/claude-org-template
Original author: vincitamore (MIT License)
"""

import json
import sys
import os
import re
import subprocess


def get_project_root():
    """Get project root from environment or by walking up from this script."""
    env_root = os.environ.get('CLAUDE_PROJECT_DIR')
    if env_root and os.path.isdir(env_root):
        return env_root
    # Fallback: .claude/hooks/session-start.py → project root is 3 levels up
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_git(args, project_root):
    """Run a git command and return stdout, or None on failure."""
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True, text=True, cwd=project_root, timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def get_next_steps(project_root):
    """Extract next steps from ROADMAP.md or TODO.md."""
    for filename in ['ROADMAP.md', 'TODO.md']:
        filepath = os.path.join(project_root, filename)
        if not os.path.exists(filepath):
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            # Try common section headers for next steps
            for header in ['## Immediate Next Steps', '## Next Steps', '## TODO', '## Tasks']:
                match = re.search(
                    rf'{re.escape(header)}\n(.*?)(?=\n---|\n## |\Z)',
                    content, re.DOTALL
                )
                if match:
                    return match.group(1).strip()[:600]
        except Exception:
            pass
    return ""


def get_working_state(project_root):
    """Read the working state file if it exists."""
    state_path = os.path.join(project_root, 'WORKING_STATE.md')
    if not os.path.exists(state_path):
        return ""
    try:
        with open(state_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        if not content:
            return ""
        # Cap at 2000 chars to avoid bloating context
        if len(content) > 2000:
            content = content[:2000] + "\n\n*[Working state truncated — read the full file for details]*"
        return content
    except Exception:
        return ""


def count_uncommitted_files(status_output):
    """Count modified/added files from git status output."""
    if not status_output:
        return 0
    return len([line for line in status_output.strip().split('\n') if line.strip()])


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    project_root = get_project_root()

    # Gather git state
    branch = run_git(['branch', '--show-current'], project_root)
    log = run_git(['log', '--oneline', '-5'], project_root)
    status = run_git(['status', '--short'], project_root)

    # Read working state from previous sessions
    working_state = get_working_state(project_root)

    # Read next steps from roadmap/todo
    next_steps = get_next_steps(project_root)

    # Build orientation context
    lines = []
    lines.append("## Session Orientation")
    lines.append("")

    # Working state first — this is the AI's own continuity
    if working_state:
        lines.append("### Previous Session State")
        lines.append("*Your working state from the last session (read this carefully — it's your own notes):*")
        lines.append("")
        lines.append(working_state)
        lines.append("")
        lines.append("---")
        lines.append("")

    if branch:
        lines.append(f"**Branch:** `{branch}`")

    if log:
        lines.append("")
        lines.append("**Recent commits:**")
        lines.append("```")
        lines.append(log)
        lines.append("```")

    if status:
        file_count = count_uncommitted_files(status)
        lines.append("")
        if file_count >= 5:
            lines.append(f"**Uncommitted changes ({file_count} files — consider committing before starting new work):**")
        else:
            lines.append("**Uncommitted changes:**")
        lines.append("```")
        lines.append(status)
        lines.append("```")

    if next_steps:
        lines.append("")
        lines.append("**Next steps:**")
        lines.append(next_steps)

    lines.append("")
    lines.append("*Read CLAUDE.md for coding standards. Update WORKING_STATE.md as you work.*")

    output = {"additionalContext": "\n".join(lines)}
    print(json.dumps(output))


if __name__ == "__main__":
    main()
