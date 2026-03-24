#!/usr/bin/env python3
"""
Pre-Compaction Hook — Snapshot state before context compression

PreCompact can ONLY do side effects (no additionalContext, no blocking).
This hook:
  1. Auto-updates working state ephemeral sections from transcript
  2. Saves a full snapshot to disk for post-compaction restore

Flow:
  1. PreCompact fires → this script updates working state + writes snapshot
  2. Compaction happens (context compressed)
  3. SessionStart fires → session-start.py reads the snapshot and injects
     it as additionalContext

Project-agnostic — works with any repo. Python stdlib only.
"""

import json
import sys
import os
import subprocess
from datetime import datetime

# Import shared utilities from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _state_utils import auto_update_state, STATE_PATH, HOOK_DATA_DIR


SNAPSHOT_PATH = os.path.join(HOOK_DATA_DIR, 'pre-compact-snapshot.md')


def get_project_root():
    env_root = os.environ.get('CLAUDE_PROJECT_DIR')
    if env_root and os.path.isdir(env_root):
        return env_root
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


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    project_root = get_project_root()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trigger = data.get('trigger', 'unknown')
    transcript_path = data.get('transcript_path', '')

    # Step 1: Auto-update working state ephemeral sections
    # (preserves curated sections, overwrites Active Task + Conversation Context)
    auto_update_state(transcript_path, trigger_reason=f"pre-compaction ({trigger})")

    # Step 2: Build snapshot for post-compaction restore
    branch = run_git(['branch', '--show-current'], project_root)
    status = run_git(['status', '--short'], project_root)
    diff_stat = run_git(['diff', '--stat', 'HEAD'], project_root)
    log = run_git(['log', '--oneline', '-3'], project_root)

    lines = [
        "# Pre-Compaction Snapshot",
        f"Saved: {timestamp} | Trigger: {trigger}",
        "",
    ]

    if branch:
        lines.append("## Git State")
        lines.append(f"Branch: `{branch}`")
        if log:
            lines.append(f"Recent commits:\n```\n{log}\n```")
        if status:
            lines.append(f"Uncommitted files:\n```\n{status}\n```")
        if diff_stat:
            lines.append(f"Diff summary: {diff_stat.split(chr(10))[-1].strip()}")
        lines.append("")

    # Include the full (now freshly updated) working state in the snapshot
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, 'r', encoding='utf-8') as f:
                state_content = f.read()
            lines.append("## Working State (auto-saved)")
            lines.append(state_content)
        except Exception:
            pass

    # Write snapshot
    os.makedirs(os.path.dirname(SNAPSHOT_PATH), exist_ok=True)
    try:
        with open(SNAPSHOT_PATH, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except Exception as e:
        print(f"Failed to write snapshot: {e}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
