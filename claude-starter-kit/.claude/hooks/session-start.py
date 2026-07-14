#!/usr/bin/env python3
"""
Session Start Hook — deterministic git orientation.

Injects at session start:
- Current branch, last 5 commits, uncommitted changes
- WORKING_STATE.md (curated memory, project root — the one canonical location)
- Next steps from ROADMAP.md or TODO.md if present

Deliberately does NOT manage memory or snapshots — context continuity across
compaction is the harness's job; curated memory is the model's job.

Project-agnostic. Python stdlib only.
Adapted from https://github.com/vincitamore/claude-org-template (MIT).
"""

import json
import os
import re
import subprocess
import sys


def get_project_root():
    env_root = os.environ.get('CLAUDE_PROJECT_DIR')
    if env_root and os.path.isdir(env_root):
        return env_root
    # .claude/hooks/session-start.py → project root is 3 levels up
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_git(args, project_root):
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True, text=True, cwd=project_root, timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def get_working_state(project_root):
    """Read WORKING_STATE.md from the project root (single canonical location)."""
    path = os.path.join(project_root, 'WORKING_STATE.md')
    if not os.path.exists(path):
        return ""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        if len(content) > 2000:
            content = content[:2000] + "\n\n*[Truncated — read WORKING_STATE.md for the rest]*"
        return content
    except Exception:
        return ""


def get_next_steps(project_root):
    """Extract a next-steps section from ROADMAP.md or TODO.md."""
    for filename in ['ROADMAP.md', 'TODO.md']:
        filepath = os.path.join(project_root, filename)
        if not os.path.exists(filepath):
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
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
        json.load(sys.stdin)
    except Exception:
        pass

    project_root = get_project_root()

    branch = run_git(['branch', '--show-current'], project_root)
    log = run_git(['log', '--oneline', '-5'], project_root)
    status = run_git(['status', '--short'], project_root)

    lines = ["## Session Orientation", ""]

    working_state = get_working_state(project_root)
    if working_state:
        lines += [
            "### Working State (your curated memory from previous sessions)",
            "",
            working_state,
            "",
            "---",
            "",
        ]

    if branch:
        lines.append(f"**Branch:** `{branch}`")
    if log:
        lines += ["", "**Recent commits:**", "```", log, "```"]
    if status:
        file_count = len([l for l in status.split('\n') if l.strip()])
        header = "**Uncommitted changes:**"
        if file_count >= 5:
            header = f"**Uncommitted changes ({file_count} files — consider committing before new work):**"
        lines += ["", header, "```", status, "```"]

    next_steps = get_next_steps(project_root)
    if next_steps:
        lines += ["", "**Next steps:**", next_steps]

    lines += ["", "*Rules are in `.claude/rules/core.md`. Project facts in CLAUDE.md. "
              "Run `/verify` before any completion claim.*"]

    print(json.dumps({"additionalContext": "\n".join(lines)}))


if __name__ == "__main__":
    main()
