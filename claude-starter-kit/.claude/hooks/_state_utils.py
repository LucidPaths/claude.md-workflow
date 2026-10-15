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
import tempfile
from datetime import datetime


def get_project_root():
    """Get project root from environment or by walking up from this script."""
    env_root = os.environ.get('CLAUDE_PROJECT_DIR')
    if env_root and os.path.isdir(env_root):
        return env_root
    # Fallback: .claude/hooks/_state_utils.py → project root is 3 levels up
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_state_path(project_root=None):
    """Use the same docs-first precedence for reads and writes."""
    root = project_root or get_project_root()
    paths = [os.path.join(root, 'docs', 'WORKING_STATE.md'),
             os.path.join(root, 'WORKING_STATE.md')]
    return next((path for path in paths if os.path.lexists(path)), paths[0])


# Directory for hook data files (snapshots, etc.)
HOOK_DATA_DIR = os.path.join(get_project_root(), '.claude', 'hook-data')


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

            if not isinstance(entry, dict):
                continue
            message = entry.get('message', entry)
            if not isinstance(message, dict):
                continue
            role = message.get('role') or entry.get('type') or entry.get('role')
            content = message.get('content', '')
            blocks = ([{'type': 'text', 'text': content}]
                      if isinstance(content, str) else content)
            if not isinstance(blocks, list):
                continue
            if entry.get('type') == 'tool_use':
                blocks = [entry]
            for block in blocks:
                if not isinstance(block, dict):
                    continue
                text = block.get('text', '')
                if block.get('type') == 'text' and isinstance(text, str):
                    if role in ('human', 'user') and text.strip():
                        user_messages.append(text.strip()[-200:])
                    elif role == 'assistant' and len(text) > 30:
                        assistant_snippets.append(text[:200])
                if block.get('type') == 'tool_use':
                    tool_input = block.get('input', {})
                    if not isinstance(tool_input, dict):
                        continue
                    path = tool_input.get('file_path') or tool_input.get('path')
                    command = tool_input.get('command')
                    name = block.get('name', '')
                    if isinstance(path, str) and path:
                        tool_calls.append(f"{name}: {os.path.basename(path)}")
                    elif isinstance(command, str) and command:
                        tool_calls.append(f"{name}: {command[:80]}")

        return {
            'user_messages': user_messages[-5:],
            'tool_calls': tool_calls[-10:],
            'assistant_snippets': assistant_snippets[-3:],
        }
    except Exception:
        return {'user_messages': [], 'tool_calls': [], 'assistant_snippets': []}


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


def split_state_sections(content):
    """Split at level-two headings outside fenced code; refuse unclosed fences."""
    boundaries = [0]
    offset = 0
    fence = None
    for line in content.splitlines(keepends=True):
        text = line.rstrip('\r\n')
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', text)
        if fence is not None:
            if (marker and marker[1][0] == fence[0]
                    and len(marker[1]) >= len(fence) and not marker[2].strip(' \t')):
                fence = None
        elif marker and (marker[1][0] == '~' or '`' not in marker[2]):
            fence = marker[1]
        elif text.startswith('## ') and offset:
            boundaries.append(offset)
        offset += len(line)
    if fence is not None:
        # Appending here would put new state inside an unfinished example.
        return None
    boundaries.append(len(content))
    return [content[left:right] for left, right in zip(boundaries, boundaries[1:])]


def auto_update_state(transcript_path, trigger_reason="session activity"):
    """Replace only sections with usable new context; retain everything else.

    Atomic replacement protects against partial writes, not concurrent editors.
    Use one writer per working tree. A failed read must never become an overwrite.
    """
    context = extract_transcript_context(transcript_path)
    if not any(context.values()):
        return False
    path = get_state_path()
    temporary = None
    try:
        if os.path.islink(path):
            return False
        try:
            with open(path, encoding='utf-8', newline='') as f:
                content = f.read()
        except FileNotFoundError:
            content = "# Claude Working State\n"
        active, conversation = build_ephemeral_sections(context, trigger_reason)
        replacements = {}
        if context['user_messages'] or context['tool_calls']:
            replacements['## Active Task'] = active
        if context['assistant_snippets']:
            replacements['## Conversation Context'] = conversation
        # Only level-two headings delimit sections; horizontal rules are content.
        parts = split_state_sections(content)
        if parts is None:
            return False
        for index, part in enumerate(parts):
            header = part.split('\n', 1)[0].rstrip()
            if header in replacements:
                parts[index] = replacements.pop(header).strip() + '\n\n'
        content = ''.join(parts)
        for section in replacements.values():
            separator = '\n' if content.endswith('\n') else '\n\n'
            content += separator + section.strip() + '\n'
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='', dir=directory,
                                         prefix='.working-state-', delete=False) as f:
            temporary = f.name
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, path)
        return True
    except (OSError, UnicodeError):
        return False
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
