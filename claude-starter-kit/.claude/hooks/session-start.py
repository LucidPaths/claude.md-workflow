#!/usr/bin/env python3
"""
Session Start Hook — Auto-orientation for new Claude Code sessions

Provides Claude with current project state at session start:
- Current git branch and recent commits
- Uncommitted changes
- Next steps from ROADMAP.md or TODO.md

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

    # Read next steps from roadmap/todo
    next_steps = get_next_steps(project_root)

    # Build orientation context
    lines = []
    lines.append("## Project Orientation")
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
        lines.append("")
        lines.append("**Uncommitted changes:**")
        lines.append("```")
        lines.append(status)
        lines.append("```")

    if next_steps:
        lines.append("")
        lines.append("**Next steps:**")
        lines.append(next_steps)

    lines.append("")
    lines.append("*See CLAUDE.md for coding standards and project instructions.*")

    output = {"additionalContext": "\n".join(lines)}
    print(json.dumps(output))


if __name__ == "__main__":
    main()
