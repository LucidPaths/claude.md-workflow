#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Ensure Python 3 is available (required for claude-starter-kit hooks)
if ! command -v python3 &> /dev/null; then
  apt-get update -qq && apt-get install -y -qq python3 > /dev/null 2>&1
fi

# Ensure git is available (required for session-start orientation hook)
if ! command -v git &> /dev/null; then
  apt-get update -qq && apt-get install -y -qq git > /dev/null 2>&1
fi
