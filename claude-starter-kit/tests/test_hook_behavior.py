#!/usr/bin/env python3
"""Offline behavior tests; no Claude process, network, or real project mutation."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

KIT = Path(__file__).resolve().parents[1]
HOOKS = KIT / '.claude' / 'hooks'
sys.path.insert(0, str(HOOKS))
import _state_utils as state


def load(name):
    spec = importlib.util.spec_from_file_location(name, HOOKS / (name + '.py'))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


commit = load('precommit-doc-check')
start = load('session-start')


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='.hook-test-', dir=KIT)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.root))
        self.environment = patch.dict(os.environ, self.env)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.git('init', '-q')
        (self.root / 'app.py').write_text('print(1)\n')
        self.git('add', '.')
        self.git('-c', 'user.name=Test Fixture', '-c', 'user.email=test@example.invalid',
                 'commit', '-qm', 'baseline')

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, env=self.env,
                              capture_output=True, text=True, check=True).stdout

    def hook(self, name, payload):
        result = subprocess.run([sys.executable, str(HOOKS / name)],
                                cwd=self.root, env=self.env, input=json.dumps(payload),
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout) if result.stdout.strip() else None

    def doc_check(self, command):
        return self.hook('precommit-doc-check.py', {
            'cwd': str(self.root), 'tool_name': 'Bash', 'tool_input': {'command': command}})

    def stage_code(self, path='app.py'):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('print(2)\n')
        self.git('add', path)

    def assert_denied(self, result):
        self.assertIsNotNone(result)
        output = result.get('hookSpecificOutput', {})
        self.assertEqual(output.get('hookEventName'), 'PreToolUse')
        self.assertEqual(output.get('permissionDecision'), 'deny')
        self.assertTrue(output.get('permissionDecisionReason'))
        self.assertNotIn('decision', result)

    def transcript(self, records):
        path = self.root / 'transcript.jsonl'
        path.write_text(''.join(json.dumps(r) + '\n' for r in records))
        return str(path)


class CommitTests(Fixture):
    def test_plain_commit_and_current_output_contract(self):
        self.stage_code()
        self.assert_denied(self.doc_check('git commit -m fix'))

    def test_reasoned_exception_retry(self):
        self.stage_code()
        self.assert_denied(self.doc_check('git commit -m "Docs-Unnecessary:"'))
        self.assertIsNone(self.doc_check('git commit -m "fix" -m "Docs-Unnecessary: internal refactor; public behavior unchanged"'))

    def test_exception_must_be_message_not_shell_text(self):
        self.stage_code()
        self.assert_denied(self.doc_check('git commit -m fix # Docs-Unnecessary: unchanged'))

    def test_amend_word_in_message_is_not_an_option(self):
        self.stage_code()
        self.assert_denied(self.doc_check('git commit -m "remove --amend mention"'))
        self.assert_denied(self.doc_check('git commit --amend -m fix'))

    def test_cd_and_git_directory_options(self):
        self.stage_code()
        for command in ['git -C . commit -m fix', 'cd . && git commit -m fix']:
            with self.subTest(command=command):
                self.assert_denied(self.doc_check(command))

    def test_directory_option_inspects_target_repository(self):
        other = self.root / 'other repo'
        other.mkdir()
        subprocess.run(['git', 'init', '-q', str(other)], check=True)
        (other / 'service.py').write_text('pass\n')
        subprocess.run(['git', '-C', str(other), 'add', '.'], check=True)
        self.assert_denied(self.doc_check('git -C "other repo" commit -m fix'))

    def test_all_includes_unstaged_tracked_code(self):
        (self.root / 'app.py').write_text('print(3)\n')
        for flag in ['-am fix', '--all -m fix']:
            self.assert_denied(self.doc_check('git commit ' + flag))

    def assert_all_candidate(self, expected, denied):
        # The reminder must not stage, refresh the index, change files or commit.
        index = self.root / '.git' / 'index'
        before_index = index.read_bytes()
        before_head = self.git('symbolic-ref', 'HEAD')
        before_refs = self.git('for-each-ref', '--format=%(refname) %(objectname)')
        before_files = {p.relative_to(self.root): p.read_bytes()
                        for p in self.root.rglob('*')
                        if p.is_file() and '.git' not in p.relative_to(self.root).parts}
        self.assertEqual(commit.get_candidate_files(str(self.root), True), expected)
        for flags in ['-am fix', '--all -m fix']:
            result = self.doc_check('git commit ' + flags)
            if denied:
                self.assert_denied(result)
            else:
                self.assertIsNone(result)
        self.assertEqual(index.read_bytes(), before_index)
        self.assertEqual(self.git('symbolic-ref', 'HEAD'), before_head)
        self.assertEqual(self.git('for-each-ref', '--format=%(refname) %(objectname)'), before_refs)
        self.assertEqual({p.relative_to(self.root): p.read_bytes()
                          for p in self.root.rglob('*')
                          if p.is_file() and '.git' not in p.relative_to(self.root).parts},
                         before_files)
        # Actual commits are confined to this disposable fixture, never the source repo.
        self.git('-c', 'user.name=Test Fixture', '-c', 'user.email=test@example.invalid',
                 'commit', '--allow-empty', '-qam', 'candidate')
        actual = self.git('diff-tree', '--root', '--no-commit-id', '--name-only',
                          '-r', '-z', 'HEAD').split('\0')
        self.assertEqual(sorted(filter(None, actual)), expected)

    def test_all_canceled_staged_doc_does_not_suppress_reminder(self):
        doc = self.root / 'README.md'
        doc.write_text('Original docs\n')
        self.git('add', 'README.md')
        self.git('-c', 'user.name=Test Fixture', '-c', 'user.email=test@example.invalid',
                 'commit', '-qm', 'docs baseline')
        self.stage_code()
        doc.write_text('Temporary doc edit\n')
        self.git('add', 'README.md')
        doc.write_text('Original docs\n')
        self.assert_all_candidate(['app.py'], denied=True)

    def test_all_canceled_staged_code_does_not_trigger_reminder(self):
        self.stage_code()
        (self.root / 'app.py').write_text('print(1)\n')
        self.assert_all_candidate([], denied=False)

    def test_all_staged_additions_use_worktree_and_ignore_untracked_docs(self):
        self.stage_code('new\nfile.py')
        self.stage_code('removed.py')
        (self.root / 'removed.py').unlink()
        (self.root / 'new\nfile.py').write_text('print(3)\n')
        (self.root / 'README.md').write_text('Untracked docs\n')
        self.assert_all_candidate(['new\nfile.py'], denied=True)

    def test_all_unborn_candidate_omits_removed_staged_doc(self):
        self.git('checkout', '--orphan', 'unborn')
        doc = self.root / 'README.md'
        doc.write_text('Staged docs\n')
        self.git('add', 'README.md')
        doc.unlink()
        (self.root / 'app.py').write_text('print(3)\n')
        self.assert_all_candidate(['app.py'], denied=True)

    def test_all_detects_racy_clean_same_size_worktree_change(self):
        self.git('config', 'core.trustctime', 'false')
        path = self.root / 'app.py'
        before = path.stat()
        # Index time equal to the cached file time forces Git's content check.
        # A copy with a fresh mtime would incorrectly make the entry look clean.
        os.utime(self.root / '.git' / 'index', ns=(before.st_atime_ns, before.st_mtime_ns))
        path.write_text('print(3)\n')
        os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
        self.assert_all_candidate(['app.py'], denied=True)

    def test_all_keeps_staged_deletion_when_path_is_recreated_untracked(self):
        self.git('rm', 'app.py')
        (self.root / 'app.py').write_text('print(1)\n')
        self.assert_all_candidate(['app.py'], denied=True)

    def test_non_commits_do_not_trigger(self):
        self.stage_code()
        for command in ['git status', 'echo "git commit -m fix"']:
            self.assertIsNone(self.doc_check(command))

    def test_real_test_names_not_substrings(self):
        for path in ['src/contest.py', 'src/special.py', 'src/testimony.py']:
            self.assertFalse(commit.is_test_only([path]), path)
        for path in ['tests/service.py', 'test_service.py', 'src/service.test.ts', 'src/service_spec.rb']:
            self.assertTrue(commit.is_test_only([path]), path)

    def test_unrelated_text_is_not_documentation(self):
        self.stage_code()
        (self.root / 'unrelated.txt').write_text('unrelated\n')
        self.git('add', 'unrelated.txt')
        self.assert_denied(self.doc_check('git commit -m fix'))
        (self.root / 'README.md').write_text('Behavior documentation\n')
        self.git('add', 'README.md')
        self.assertIsNone(self.doc_check('git commit -m fix'))


class StateTests(Fixture):
    def update(self, transcript):
        return state.auto_update_state(transcript, 'test')

    def test_missing_or_unsupported_transcript_preserves_exact_state(self):
        path = self.root / 'docs' / 'WORKING_STATE.md'
        path.parent.mkdir()
        original = '# Working State\n## Active Task\nKeep next step\n## Corrections\nKeep correction\n'
        path.write_text(original)
        for transcript in ['', str(self.root / 'missing'), self.transcript([{'unknown': True}, None])]:
            self.assertFalse(self.update(transcript))
            self.assertEqual(path.read_text(), original)

    def test_root_state_is_updated_not_shadowed(self):
        path = self.root / 'WORKING_STATE.md'
        path.write_text('# State\n## Active Task\nOld\n## Corrections\nROOT SENTINEL\n')
        self.assertTrue(self.update(self.transcript([{'type': 'human', 'content': 'New task'}])))
        self.assertFalse((self.root / 'docs' / 'WORKING_STATE.md').exists())
        self.assertIn('New task', path.read_text())
        self.assertIn('ROOT SENTINEL', start.get_working_state(str(self.root)))

    def test_unknown_sections_and_internal_separator_survive(self):
        path = self.root / 'WORKING_STATE.md'
        retained = '## Corrections\nONE\n\n---\n\nTWO\n## Test Baseline\nKnown baseline\n'
        path.write_text('# Custom title\n## Active Task\nOld\n' + retained)
        self.assertTrue(self.update(self.transcript([{'role': 'user', 'content': 'New task'}])))
        self.assertIn('New task', path.read_text())
        self.assertIn(retained, path.read_text())
        self.assertTrue(path.read_text().startswith('# Custom title'))

    def test_session_end_preserves_fenced_example_before_or_without_real_task(self):
        path = self.root / 'WORKING_STATE.md'
        original = ('# State\n## Corrections\nKeep this literal example:\n```markdown\n'
                    '## Active Task\nEXAMPLE SENTINEL\n```\n'
                    'CURATED SENTINEL AFTER FENCE\n## Test Baseline\nBASELINE SENTINEL\n')
        transcript = self.transcript([{'role': 'user', 'content': 'Continue the current task'}])
        for real_task in ['', '## Active Task\nOLD TASK\n']:
            with self.subTest(real_task=bool(real_task)):
                path.write_text(original + real_task)
                self.hook('session-end.py', {'transcript_path': transcript, 'reason': 'review'})
                updated = path.read_text()
                self.assertTrue(updated.startswith(original), updated)
                self.assertIn('Continue the current task', updated)
                self.assertNotIn('OLD TASK', updated)
                self.assertEqual(updated.count('*Auto-captured from'), 1)

    def test_fence_delimiters_do_not_expose_example_headings(self):
        path = self.root / 'WORKING_STATE.md'
        transcript = self.transcript([
            {'role': 'user', 'content': 'New task'},
            {'role': 'assistant', 'content': 'New assistant context with sufficient detail.'}])
        for opening, nonclosers, closing in [
                ('````markdown', '```\n~~~\n```` trailing text', '`````'),
                ('~~~markdown', '~~\n```\n~~~ trailing text', '~~~~'),
                ('   ```markdown', '  ``\n    ```', '   ```  \t')]:
            with self.subTest(opening=opening):
                retained = ('# State\n## Corrections\n' + opening + '\n' + nonclosers +
                            '\n## Active Task\nEXAMPLE TASK\n## Conversation Context\n'
                            'EXAMPLE CONTEXT\n' + closing + '\nCURATED TAIL\n')
                path.write_text(retained + '## Active Task\nOLD TASK\n'
                                '## Conversation Context\nOLD CONTEXT\n')
                self.assertTrue(self.update(transcript))
                updated = path.read_text()
                self.assertTrue(updated.startswith(retained), updated)
                self.assertIn('New task', updated)
                self.assertIn('New assistant context', updated)
                self.assertNotIn('OLD TASK', updated)
                self.assertNotIn('OLD CONTEXT', updated)

    def test_fenced_heading_inside_target_does_not_end_section(self):
        path = self.root / 'WORKING_STATE.md'
        retained = '## Corrections\nCURATED CORRECTION\n'
        path.write_text('# State\n## Active Task\nOLD TASK\n~~~\n'
                        '## Corrections\nOLD EXAMPLE\n~~~\nOLD TAIL\n' + retained)
        self.assertTrue(self.update(self.transcript([{'role': 'user', 'content': 'New task'}])))
        updated = path.read_text()
        self.assertTrue(updated.endswith(retained), updated)
        self.assertNotIn('OLD', updated)
        self.assertIn('New task', updated)

    def test_unclosed_fence_preserves_exact_predecessor(self):
        path = self.root / 'WORKING_STATE.md'
        transcript = self.transcript([{'role': 'user', 'content': 'New task'}])
        for fence in ['```markdown', '~~~~']:
            with self.subTest(fence=fence):
                original = '# State\n## Active Task\nKEEP TASK\n## Corrections\n' + fence + '\n## Active Task\nKEEP EXAMPLE\n'
                path.write_text(original)
                self.assertFalse(self.update(transcript))
                self.hook('session-end.py', {'transcript_path': transcript})
                self.assertEqual(path.read_text(), original)
                self.assertEqual(list(self.root.glob('.working-state-*')), [])

    def test_append_preserves_curated_bytes_and_trailing_whitespace(self):
        path = self.root / 'WORKING_STATE.md'
        original = b'# State\r\n## Corrections\r\n~~~\r\n## Active Task\r\n~~~\r\nKEEP  \r\n \t'
        path.write_bytes(original)
        self.assertTrue(self.update(self.transcript([{'role': 'user', 'content': 'New task'}])))
        self.assertTrue(path.read_bytes().startswith(original))

    def test_partial_context_does_not_erase_other_section(self):
        path = self.root / 'WORKING_STATE.md'
        path.write_text('# State\n## Active Task\nKeep task\n## Conversation Context\nOld\n')
        self.assertTrue(self.update(self.transcript([{'type': 'assistant', 'message': {
            'role': 'assistant', 'content': [{'type': 'text', 'text': 'A new assistant explanation with enough detail.'}]}}])))
        self.assertIn('Keep task', path.read_text())
        self.assertNotIn('\nOld\n', path.read_text())

    def test_flat_and_nested_transcripts(self):
        text = 'A sufficiently long assistant explanation for extraction.'
        flat = [{'type': 'human', 'content': 'Task'}, {'type': 'assistant', 'content': text},
                {'type': 'tool_use', 'name': 'Read', 'input': {'file_path': 'a.py'}}]
        nested = [{'type': 'user', 'message': {'role': 'user', 'content': 'Task'}},
                  {'type': 'assistant', 'message': {'role': 'assistant', 'content': [
                      {'type': 'text', 'text': text}, {'type': 'tool_use', 'name': 'Read', 'input': {'file_path': 'a.py'}}]}}]
        self.assertEqual(state.extract_transcript_context(self.transcript(flat)),
                         state.extract_transcript_context(self.transcript(nested)))

    def test_replace_failure_preserves_predecessor(self):
        path = self.root / 'WORKING_STATE.md'
        path.write_text('# State\n## Active Task\nKeep me\n')
        transcript = self.transcript([{'role': 'user', 'content': 'New task'}])
        with patch.object(state.os, 'replace', side_effect=OSError('simulated failure')):
            self.assertFalse(self.update(transcript))
        self.assertEqual(path.read_text(), '# State\n## Active Task\nKeep me\n')
        self.assertEqual(list(self.root.glob('.working-state-*')), [])

    def test_unreadable_predecessor_is_not_overwritten(self):
        path = self.root / 'WORKING_STATE.md'
        path.write_bytes(b'\xff')
        self.assertFalse(self.update(self.transcript([{'role': 'user', 'content': 'New task'}])))
        self.assertEqual(path.read_bytes(), b'\xff')

    def test_session_end_then_start_preserves_root_sentinel(self):
        (self.root / 'WORKING_STATE.md').write_text('# State\n## Corrections\nSENTINEL\n')
        transcript = self.transcript([{'role': 'user', 'content': 'Continue task'}])
        self.hook('session-end.py', {'transcript_path': transcript, 'reason': 'test'})
        result = self.hook('session-start.py', {'source': 'startup'})
        self.assertIn('SENTINEL', result['hookSpecificOutput']['additionalContext'])
        self.assertIn('Continue task', result['hookSpecificOutput']['additionalContext'])


    def test_both_state_paths_use_docs_without_changing_root(self):
        root_path = self.root / 'WORKING_STATE.md'
        root_path.write_text('# Root\n## Corrections\nROOT\n')
        docs_path = self.root / 'docs' / 'WORKING_STATE.md'
        docs_path.parent.mkdir()
        docs_path.write_text('# Docs\n## Corrections\nDOCS\n')
        self.assertTrue(self.update(self.transcript([{'role': 'user', 'content': 'New task'}])))
        self.assertIn('DOCS', start.get_working_state(str(self.root)))
        self.assertEqual(root_path.read_text(), '# Root\n## Corrections\nROOT\n')

    def test_symlink_predecessor_is_not_replaced(self):
        target = self.root / 'private-state'
        target.write_text('Keep original')
        path = self.root / 'WORKING_STATE.md'
        path.symlink_to(target)
        self.assertFalse(self.update(self.transcript([{'role': 'user', 'content': 'New task'}])))
        self.assertTrue(path.is_symlink())
        self.assertEqual(target.read_text(), 'Keep original')

    def test_compact_then_start_uses_root_state(self):
        (self.root / 'WORKING_STATE.md').write_text('# State\n## Corrections\nCOMPACT SENTINEL\n')
        self.hook('pre-compact.py', {'transcript_path': '', 'trigger': 'manual'})
        snapshot = self.root / '.claude' / 'hook-data' / 'pre-compact-snapshot.md'
        self.assertIn('COMPACT SENTINEL', snapshot.read_text())
        self.assertFalse((self.root / 'docs' / 'WORKING_STATE.md').exists())
        result = self.hook('session-start.py', {'source': 'compact'})
        self.assertIn('COMPACT SENTINEL', result['hookSpecificOutput']['additionalContext'])
        self.assertFalse(snapshot.exists())


class RegistrationTests(Fixture):
    def test_registered_commands_use_project_path_with_spaces(self):
        project = self.root / 'project with spaces'
        shutil.copytree(HOOKS, project / '.claude' / 'hooks')
        settings = json.loads((KIT / '.claude' / 'settings.json').read_text())
        for event, groups in settings['hooks'].items():
            for group in groups:
                for hook in group['hooks']:
                    with self.subTest(event=event):
                        result = subprocess.run(['bash', '-c', hook['command']],
                                                cwd=self.root, input='{}', text=True,
                                                capture_output=True, timeout=10,
                                                env=dict(self.env, CLAUDE_PROJECT_DIR=str(project)))
                        self.assertEqual(result.returncode, 0, result.stderr)
                        if event == 'SessionStart':
                            self.assertEqual(json.loads(result.stdout)['hookSpecificOutput']['hookEventName'], event)


class GuardTests(Fixture):
    def install(self):
        return subprocess.run(['bash', str(KIT / 'guards' / 'install-guards.sh')],
                              cwd=self.root, env=self.env, capture_output=True, text=True, check=True)

    def test_foreign_hook_preserved_and_custom_hooks_path(self):
        self.git('config', 'core.hooksPath', '.custom-hooks')
        hooks = self.root / '.custom-hooks'
        hooks.mkdir()
        (hooks / 'pre-push').write_text('# foreign hook\n')
        self.install()
        self.assertEqual((hooks / 'pre-push').read_text(), '# foreign hook\n')
        self.assertTrue((hooks / 'pre-commit').exists())

    def test_normal_blocks_and_explicit_overrides(self):
        directory = self.root / '.claude'
        directory.mkdir()
        (directory / 'protected-paths.txt').write_text('app.py\n')
        self.install()
        self.stage_code()
        push = 'refs/heads/topic ' + '1' * 40 + ' refs/heads/main ' + '0' * 40 + '\n'
        for name, key, stdin in [('pre-push', 'ALLOW_PROTECTED_PUSH', push),
                                 ('pre-commit', 'ALLOW_PROTECTED_PATHS', '')]:
            for override, expected in [('0', 1), ('1', 0)]:
                result = subprocess.run(['bash', str(self.root / '.git' / 'hooks' / name)],
                                        cwd=self.root, env=dict(self.env, **{key: override}),
                                        input=stdin, text=True, capture_output=True)
                self.assertEqual(result.returncode, expected, result.stderr)


class StopTests(Fixture):
    def payload(self):
        return {'transcript_path': self.transcript([{}] * 101), 'stop_hook_active': False}

    def test_user_quote_does_not_acknowledge_maintenance(self):
        self.stage_code()
        payload = self.payload()
        with open(payload['transcript_path'], 'a') as f:
            f.write(json.dumps({'type': 'human', 'content': 'No maintenance needed'}) + '\n')
        self.assertEqual(self.hook('maintenance-check.py', payload)['decision'], 'block')

    def test_current_assistant_acknowledgement_and_loop_guard(self):
        self.stage_code()
        payload = self.payload()
        payload['last_assistant_message'] = 'No maintenance needed'
        self.assertIsNone(self.hook('maintenance-check.py', payload))
        payload['last_assistant_message'] = 'Still working'
        payload['stop_hook_active'] = True
        self.assertIsNone(self.hook('maintenance-check.py', payload))


if __name__ == '__main__':
    unittest.main()
