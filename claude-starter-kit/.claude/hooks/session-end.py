#!/usr/bin/env python3
"""
Session End Hook — Auto-persist working state on session exit.

Auto-updates working state ephemeral sections (Active Task, Conversation
Context) from the transcript. Curated sections (Corrections, Learnings,
Self-Improvement, etc.) are never touched — those are Claude's to maintain.

This fires on graceful session ends (not hard terminal kills).

Project-agnostic — works with any repo. Python stdlib only.
"""

import json
import sys
import os

# Import shared utilities from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _state_utils import auto_update_state


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    transcript_path = data.get('transcript_path', '')
    reason = data.get('reason', 'unknown')

    # Auto-update state file
    auto_update_state(transcript_path, trigger_reason=f"session end ({reason})")

    # SessionEnd has no decision control — just exit cleanly
    sys.exit(0)


if __name__ == "__main__":
    main()
