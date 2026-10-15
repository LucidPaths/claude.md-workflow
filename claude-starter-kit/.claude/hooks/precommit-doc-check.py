#!/usr/bin/env python3
"""Best-effort documentation reminder for ordinary Bash git commits.

This is not a shell interpreter or a security boundary. See README for limits.
Python stdlib only; never executes the supplied shell command.
"""
import json
import os
from pathlib import PurePath
import re
import shlex
import subprocess
import sys

CODE_EXTENSIONS = {
    '.py', '.ts', '.tsx', '.js', '.jsx', '.rs', '.go', '.java', '.rb', '.php',
    '.c', '.cpp', '.h', '.swift', '.kt', '.css', '.html', '.toml', '.yaml', '.yml',
}
DOC_NAMES = {'README', 'CLAUDE', 'ROADMAP', 'TODO', 'CHANGELOG',
             'WORKING_STATE', 'CONTRIBUTING', 'ARCHITECTURE'}


def parse_commit(command, cwd):
    """Recognize a literal git [-C dir] commit, optionally after cd dir &&.

    Unsupported shell expressions, Git options, and pathspec commits are skipped
    rather than inspecting the wrong repository/index. No eval or shell execution.
    """
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=';&|<>()')
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return None
    if tokens[:1] == ['cd'] and len(tokens) >= 4 and tokens[2] == '&&':
        cwd = os.path.abspath(os.path.join(cwd, tokens[1]))
        tokens = tokens[3:]
    if not tokens or tokens.pop(0) != 'git':
        return None
    while len(tokens) >= 2 and tokens[0] == '-C':
        cwd = os.path.abspath(os.path.join(cwd, tokens[1]))
        tokens = tokens[2:]
    if not tokens or tokens.pop(0) != 'commit':
        return None
    messages = []
    all_tracked = False
    while tokens:
        option = tokens.pop(0)
        if option in ('--amend', '--no-edit', '--no-verify', '-q', '--quiet',
                      '-s', '--signoff', '--allow-empty', '--allow-empty-message'):
            continue
        if option == '--all':
            all_tracked = True
        elif option in ('-m', '--message'):
            if not tokens:
                return None
            messages.append(tokens.pop(0))
        elif option.startswith('--message='):
            messages.append(option.partition('=')[2])
        elif option.startswith('-') and not option.startswith('--'):
            # Common short clusters: -a, -am text, -mtext, -asm text.
            flags = option[1:]
            while flags:
                flag, flags = flags[0], flags[1:]
                if flag == 'a':
                    all_tracked = True
                elif flag in 'qs':
                    continue
                elif flag == 'm':
                    if not flags and not tokens:
                        return None
                    messages.append(flags or tokens.pop(0))
                    break
                else:
                    return None
        else:
            return None
    # Literal paths only: shell expansion would change the actual target.
    if any(char in cwd for char in '$`~'):
        return None
    return cwd, all_tracked, messages


def get_candidate_files(cwd, all_tracked):
    """Index plus tracked worktree changes for -a; NUL-safe path handling."""
    commands = [['diff', '--cached', '--name-only', '-z']]
    if all_tracked:
        commands.append(['diff', '--name-only', '-z'])
    files = set()
    try:
        for args in commands:
            result = subprocess.run(['git', *args], cwd=cwd, capture_output=True,
                                    text=True, timeout=5, check=True)
            files.update(filter(None, result.stdout.split('\0')))
    except (OSError, subprocess.SubprocessError):
        return None
    return sorted(files)


def is_code_file(path):
    return os.path.splitext(path)[1].lower() in CODE_EXTENSIONS


def is_doc_file(path):
    name, ext = os.path.splitext(os.path.basename(path))
    return (ext.lower() in {'.md', '.rst'} or
            (name.upper() in DOC_NAMES and ext.lower() in {'', '.txt'}))


def is_test_only(paths):
    def is_test(path):
        parts = PurePath(path.lower()).parts
        name = parts[-1]
        stem = os.path.splitext(name)[0]
        return (bool(set(parts[:-1]) & {'test', 'tests', 'spec', 'specs', '__tests__', '__test__'})
                or name.startswith(('test_', 'spec_'))
                or stem.endswith(('_test', '_spec', '.test', '.spec')))
    return bool(paths) and all(is_test(path) for path in paths)


def main():
    try:
        data = json.load(sys.stdin)
    except (ValueError, OSError):
        return
    if not isinstance(data, dict) or data.get('tool_name') != 'Bash':
        return
    tool_input = data.get('tool_input')
    if not isinstance(tool_input, dict) or not isinstance(tool_input.get('command'), str):
        return
    cwd = data.get('cwd') or os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd()
    parsed = parse_commit(tool_input['command'], cwd)
    if parsed is None:
        return
    cwd, all_tracked, messages = parsed
    # A scoped acknowledgement, not evidence that documentation is correct.
    if any(re.search(r'(?im)^Docs-Unnecessary:[ \t]*\S[^\n]*', message)
           for message in messages):
        return
    files = get_candidate_files(cwd, all_tracked)
    if files is None:
        print(json.dumps({'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'additionalContext': 'Doc check could not read the Git candidate. Check documentation manually.'}}))
        return
    code_files = [path for path in files if is_code_file(path)]
    if not code_files or is_test_only(code_files) or any(is_doc_file(path) for path in files):
        return
    file_list = '\n'.join('  - ' + path for path in code_files[:8])
    reason = (
        'DOC CHECK: Candidate includes code but no recognized documentation.\n\n'
        f'Code files (up to 8 shown):\n{file_list}\n\n'
        'Check README.md for user-facing changes, CLAUDE.md for development instructions, '
        'and ROADMAP.md for feature status. A staged doc is only a reminder heuristic, not proof of relevance.\n\n'
        'If no doc update is needed, retry with a commit-message paragraph '
        '"Docs-Unnecessary: <specific reason>". This acknowledgement does not bypass other permissions.'
    )
    print(json.dumps({'hookSpecificOutput': {
        'hookEventName': 'PreToolUse', 'permissionDecision': 'deny',
        'permissionDecisionReason': reason}}))


if __name__ == '__main__':
    main()
