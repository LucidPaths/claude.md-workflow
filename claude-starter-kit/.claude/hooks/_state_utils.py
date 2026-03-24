"""
Shared utilities for working state auto-maintenance.

Used by pre-compact.py and session-end.py to auto-update the ephemeral
sections (Active Task, Conversation Context) from the transcript,
while preserving all curated/accumulating sections.

Project-agnostic — works with any repo. Python stdlib only.
"""

import json
import os
import re
from datetime import datetime


def get_project_root():
    """Get project root from environment or by walking up from this script."""
    env_root = os.environ.get('CLAUDE_PROJECT_DIR')
    if env_root and os.path.isdir(env_root):
        return env_root
    # Fallback: .claude/hooks/_state_utils.py → project root is 3 levels up
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Working state file lives in docs/ relative to project root
STATE_PATH = os.path.join(get_project_root(), 'docs', 'WORKING_STATE.md')

# Directory for hook data files (snapshots, etc.)
HOOK_DATA_DIR = os.path.join(get_project_root(), '.claude', 'hook-data')

# Sections that are AUTO-WRITTEN (overwritten by hooks)
EPHEMERAL_SECTIONS = {'## Active Task', '## Conversation Context'}

# Sections that are CURATED (never touched by hooks, only by Claude)
CURATED_SECTIONS = [
    '## Learnings',
    '## Corrections',
    '## Self-Improvement',
    '## Deferred Ideas',
    '## Codebase Insights',
]


def extract_transcript_context(transcript_path):
    """Extract recent conversation context from a transcript JSONL file."""
    if not transcript_path or not os.path.exists(transcript_path):
        return {'user_messages': [], 'tool_calls': [], 'assistant_snippets': []}

    try:
        file_size = os.path.getsize(transcript_path)
        read_size = min(file_size, 80 * 1024)

        with open(transcript_path, 'r', encoding='utf-8', errors='replace') as f:
            if file_size > read_size:
                f.seek(file_size - read_size)
                f.readline()  # skip partial line
            tail = f.read()

        user_messages = []
        tool_calls = []
        assistant_snippets = []

        for line in tail.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            role = entry.get('role', '')
            msg_type = entry.get('type', '')

            # User messages
            if role == 'human' or msg_type == 'human':
                content = entry.get('content', '')
                if isinstance(content, str) and content.strip():
                    user_messages.append(content.strip()[-200:])
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get('type') == 'text':
                            text = block.get('text', '').strip()
                            if text:
                                user_messages.append(text[-200:])

            # Tool calls
            if msg_type == 'tool_use' or entry.get('type') == 'tool_use':
                tool_name = entry.get('name', '')
                tool_input = entry.get('input', {})
                if isinstance(tool_input, dict):
                    path = tool_input.get('file_path', '') or tool_input.get('path', '')
                    command = tool_input.get('command', '')
                    if path:
                        tool_calls.append(f"{tool_name}: {os.path.basename(path)}")
                    elif command:
                        tool_calls.append(f"{tool_name}: {command[:80]}")

            # Assistant text
            if role == 'assistant' or msg_type == 'assistant':
                content = entry.get('content', '')
                if isinstance(content, str) and len(content) > 30:
                    assistant_snippets.append(content[:200])
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get('type') == 'text':
                            text = block.get('text', '')
                            if len(text) > 30:
                                assistant_snippets.append(text[:200])

        return {
            'user_messages': user_messages[-5:],
            'tool_calls': tool_calls[-10:],
            'assistant_snippets': assistant_snippets[-3:],
        }
    except Exception:
        return {'user_messages': [], 'tool_calls': [], 'assistant_snippets': []}


def parse_curated_sections(state_content):
    """Extract curated (accumulating) sections from working state file."""
    sections = {}
    for section_header in CURATED_SECTIONS:
        pattern = rf'({re.escape(section_header)}\n.*?)(?=\n## |\n---\n|\Z)'
        match = re.search(pattern, state_content, re.DOTALL)
        if match:
            text = match.group(1).strip()
            if len(text) > len(section_header) + 2:  # has content beyond header
                sections[section_header] = text
    return sections


def build_ephemeral_sections(context, trigger_reason="session activity"):
    """Generate the auto-written ephemeral sections from transcript context."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Active Task
    active_lines = [
        f"## Active Task",
        f"*Auto-captured from {trigger_reason} at {timestamp}*",
        "",
    ]
    if context.get('user_messages'):
        active_lines.append("Recent user requests:")
        for msg in context['user_messages']:
            clean = msg.replace('\n', ' ').strip()
            if len(clean) > 120:
                clean = clean[:120] + "..."
            active_lines.append(f"- \"{clean}\"")
    if context.get('tool_calls'):
        active_lines.append("")
        active_lines.append("Recent tool activity:")
        for tc in context['tool_calls']:
            active_lines.append(f"- {tc}")

    # Conversation Context
    context_lines = [
        "",
        "---",
        "",
        "## Conversation Context",
        f"*Auto-captured at {timestamp}*",
        "",
    ]
    if context.get('assistant_snippets'):
        context_lines.append("Recent assistant context:")
        for snip in context['assistant_snippets']:
            clean = snip.replace('\n', ' ').strip()
            if len(clean) > 150:
                clean = clean[:150] + "..."
            context_lines.append(f"- {clean}")

    return '\n'.join(active_lines), '\n'.join(context_lines)


def auto_update_state(transcript_path, trigger_reason="session activity"):
    """
    Auto-update working state file:
    - OVERWRITES ephemeral sections (Active Task, Conversation Context)
    - PRESERVES curated sections (Learnings, Corrections, etc.)
    """
    context = extract_transcript_context(transcript_path)

    # Read existing state file
    existing_content = ""
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        except Exception:
            pass

    # Parse out curated sections (these are sacred — never auto-modified)
    curated = parse_curated_sections(existing_content)

    # Build new ephemeral sections
    active_section, context_section = build_ephemeral_sections(context, trigger_reason)

    # Assemble the full file
    lines = [
        "# Claude Working State",
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        active_section,
        context_section,
    ]

    # Append all curated sections in order
    for header in CURATED_SECTIONS:
        if header in curated:
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append(curated[header])

    lines.append("")

    # Write
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    try:
        with open(STATE_PATH, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return True
    except Exception:
        return False
