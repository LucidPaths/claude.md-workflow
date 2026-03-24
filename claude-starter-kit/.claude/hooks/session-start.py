#!/usr/bin/env python3
"""
Session Start Hook — Auto-orientation for new AI coding sessions

Provides the AI with current project state at session start:
- Time since last session (helps calibrate how much context to rebuild)
- Working state from previous sessions (continuity memory)
- Current git branch and recent commits
- Uncommitted changes (with commit-count warning)
- Next steps from ROADMAP.md or TODO.md
- Post-compaction context restore (reads snapshot saved by pre-compact.py)

Works with any AI coding assistant that supports session hooks.
Project-agnostic — Python stdlib only.

Adapted from https://github.com/vincitamore/claude-org-template
Original author: vincitamore (MIT License)
"""

import json
import sys
import os
import re
import subprocess
from datetime import datetime


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
    """Extract next steps from ROADMAP.md, TODO.md, or SESSION_NOTES.md."""
    for filename in ['ROADMAP.md', 'TODO.md', 'SESSION_NOTES.md']:
        filepath = os.path.join(project_root, filename)
        if not os.path.exists(filepath):
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            # Try common section headers for next steps
            for header in ['## Immediate Next Steps', '## Next Steps', '## TODO', '## Tasks', '## Next steps']:
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
    # Check both docs/WORKING_STATE.md and WORKING_STATE.md
    for rel_path in ['docs/WORKING_STATE.md', 'WORKING_STATE.md']:
        state_path = os.path.join(project_root, rel_path)
        if not os.path.exists(state_path):
            continue
        try:
            with open(state_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            if not content:
                continue
            # Cap at 2000 chars to avoid bloating context
            if len(content) > 2000:
                content = content[:2000] + "\n\n*[Working state truncated — read the full file for details]*"
            return content
        except Exception:
            pass
    return ""


def get_state_file_path(project_root):
    """Find the working state file path."""
    for rel_path in ['docs/WORKING_STATE.md', 'WORKING_STATE.md']:
        path = os.path.join(project_root, rel_path)
        if os.path.exists(path):
            return path
    return None


def get_time_since_last_session(project_root):
    """Check when working state was last modified to estimate time gap."""
    state_path = get_state_file_path(project_root)
    if not state_path:
        return None
    try:
        mtime = os.path.getmtime(state_path)
        last = datetime.fromtimestamp(mtime, tz=None)
        now = datetime.now()
        delta = now - last

        if delta.total_seconds() < 300:  # <5 min
            return "just now (< 5 min ago)"
        elif delta.total_seconds() < 3600:  # <1 hr
            mins = int(delta.total_seconds() / 60)
            return f"{mins} minutes ago"
        elif delta.total_seconds() < 86400:  # <1 day
            hours = int(delta.total_seconds() / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = int(delta.total_seconds() / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
    except Exception:
        return None


def read_and_consume_snapshot(project_root):
    """Read pre-compaction snapshot if it exists, then delete it."""
    snapshot_path = os.path.join(project_root, '.claude', 'hook-data', 'pre-compact-snapshot.md')
    if not os.path.exists(snapshot_path):
        return None
    try:
        with open(snapshot_path, 'r', encoding='utf-8') as f:
            content = f.read()
        os.remove(snapshot_path)
        return content if content.strip() else None
    except Exception:
        return None


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

    # Time context
    time_gap = get_time_since_last_session(project_root)

    # Read working state from previous sessions
    working_state = get_working_state(project_root)

    # Read next steps from roadmap/todo
    next_steps = get_next_steps(project_root)

    # Check for post-compaction snapshot
    snapshot = read_and_consume_snapshot(project_root)

    # Build orientation context
    lines = []
    lines.append("## Session Orientation")
    lines.append("")

    if time_gap:
        lines.append(f"**Last session:** {time_gap}")
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

    # Post-compaction restore
    if snapshot:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## CONTEXT RESTORED FROM PRE-COMPACTION SNAPSHOT")
        lines.append("")
        lines.append("The following was saved by the PreCompact hook right before")
        lines.append("context compression. Use it to resume where you left off.")
        lines.append("")
        lines.append(snapshot)

    lines.append("")
    lines.append("*Read CLAUDE.md for coding standards. Update docs/WORKING_STATE.md as you work.*")

    output = {"additionalContext": "\n".join(lines)}
    print(json.dumps(output))


if __name__ == "__main__":
    main()
