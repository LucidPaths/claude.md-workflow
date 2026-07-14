#!/usr/bin/env python3
"""
Change Check Hook (Stop) — one evidence-based documentation reminder.

Design constraints, learned from the v1 kit:
- Evidence, not self-report: fires only on observable state (code files changed
  in the working tree while no documentation file was touched). There is no
  magic phrase that silences it.
- Never a nag loop: fires AT MOST ONCE per session (marker file keyed by
  session_id, plus stop_hook_active as a belt-and-braces guard). After
  delivering the evidence once, it stays silent — whether docs need updating
  is a judgment call, and looping on a judgment call trains workarounds.

Project-agnostic. Python stdlib only.
"""

import json
import os
import subprocess
import sys

CODE_EXTENSIONS = {
    '.py', '.ts', '.tsx', '.js', '.jsx',
    '.rs', '.go', '.java', '.rb', '.php',
    '.c', '.cpp', '.h', '.swift', '.kt',
    '.css', '.html', '.toml', '.yaml', '.yml',
}
DOC_EXTENSIONS = {'.md', '.rst', '.txt'}
DOC_BASENAMES = {
    'README', 'CLAUDE', 'ROADMAP', 'TODO', 'CHANGELOG',
    'WORKING_STATE', 'CONTRIBUTING', 'ARCHITECTURE',
}
TEST_INDICATORS = ('test', 'spec', '__test__', '.test.', '.spec.', '_test.')


def get_project_root():
    env_root = os.environ.get('CLAUDE_PROJECT_DIR')
    if env_root and os.path.isdir(env_root):
        return env_root
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_changed_files(project_root):
    """Staged + unstaged + untracked files, deduplicated."""
    files = []
    commands = [
        ['git', 'diff', '--name-only', 'HEAD'],
        ['git', 'diff', '--cached', '--name-only'],
        ['git', 'ls-files', '--others', '--exclude-standard'],
    ]
    for cmd in commands:
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=project_root, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                files.extend(result.stdout.strip().split('\n'))
        except Exception:
            pass
    return sorted(set(f for f in files if f.strip()))


def is_code_file(path):
    return os.path.splitext(path)[1].lower() in CODE_EXTENSIONS


def is_doc_file(path):
    name, ext = os.path.splitext(os.path.basename(path))
    return ext.lower() in DOC_EXTENSIONS or name.upper() in DOC_BASENAMES


def is_test_file(path):
    lower = path.lower()
    return any(ind in lower for ind in TEST_INDICATORS)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    # Loop guard #1: harness-level flag set when a Stop hook already blocked.
    if data.get('stop_hook_active'):
        sys.exit(0)

    project_root = get_project_root()

    # Loop guard #2: fire at most once per session.
    session_id = str(data.get('session_id', '')) or 'unknown'
    marker_dir = os.path.join(project_root, '.claude', 'hook-data')
    marker = os.path.join(marker_dir, f'change-check-{session_id[:32]}')
    if os.path.exists(marker):
        sys.exit(0)

    changed = get_changed_files(project_root)
    code_files = [f for f in changed if is_code_file(f) and not is_test_file(f)]
    doc_files = [f for f in changed if is_doc_file(f)]

    # Nothing to say unless non-test code changed and no doc was touched.
    if not code_files or doc_files:
        sys.exit(0)

    # Record that the reminder fired before delivering it.
    try:
        os.makedirs(marker_dir, exist_ok=True)
        with open(marker, 'w', encoding='utf-8') as f:
            f.write('fired\n')
    except Exception:
        pass

    file_list = "\n".join("  - " + f for f in code_files[:10])
    if len(code_files) > 10:
        file_list += f"\n  - ... and {len(code_files) - 10} more"

    reason = (
        "DOC CHECK (fires once per session, evidence below):\n\n"
        f"Code files changed with no documentation file touched:\n{file_list}\n\n"
        "Decide explicitly — for each area that changed:\n"
        "  - User-facing behavior → README.md\n"
        "  - Build/setup/patterns → CLAUDE.md\n"
        "  - Corrections or insights this session → WORKING_STATE.md\n\n"
        "Update what needs updating, or state to the user why nothing does. "
        "This reminder will not repeat."
    )

    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


if __name__ == "__main__":
    main()
