#!/usr/bin/env python3
"""
Smoke tests for starter kit hooks.

Verifies that hook scripts:
1. Parse without syntax errors
2. Run without crashing on empty/minimal input
3. Produce valid JSON output where expected
4. settings.json is valid and references existing hook files

Run: python3 tests/test_hooks.py
"""

import json
import os
import subprocess
import sys

STARTER_KIT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS_DIR = os.path.join(STARTER_KIT_DIR, ".claude", "hooks")
SETTINGS_PATH = os.path.join(STARTER_KIT_DIR, ".claude", "settings.json")

passed = 0
failed = 0


def test(name, condition, detail=""):
    global passed, failed
    if condition:
        print(f"  PASS  {name}")
        passed += 1
    else:
        print(f"  FAIL  {name}" + (f" — {detail}" if detail else ""))
        failed += 1


def run_hook(script_path, stdin_data="{}"):
    """Run a hook script with given stdin, return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, script_path],
        input=stdin_data,
        capture_output=True,
        text=True,
        timeout=10,
        cwd=STARTER_KIT_DIR,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


# --- Test 1: settings.json is valid JSON ---
print("\nsettings.json")
try:
    with open(SETTINGS_PATH) as f:
        settings = json.load(f)
    test("valid JSON", True)
except (json.JSONDecodeError, FileNotFoundError) as e:
    test("valid JSON", False, str(e))
    settings = {}

# --- Test 2: settings.json references hooks that exist ---
print("\nhook file references")
for event_name, event_hooks in settings.get("hooks", {}).items():
    for group in event_hooks:
        for hook in group.get("hooks", []):
            cmd = hook.get("command", "")
            # Extract the Python script path from the command
            # Format: python3 "$(git rev-parse --show-toplevel)/.claude/hooks/foo.py"
            if ".claude/hooks/" in cmd:
                script_name = cmd.split(".claude/hooks/")[-1].rstrip('"')
                script_path = os.path.join(HOOKS_DIR, script_name)
                test(
                    f"{event_name} -> {script_name} exists",
                    os.path.isfile(script_path),
                    f"not found: {script_path}",
                )

# --- Test 3: Hook scripts parse without syntax errors ---
print("\nsyntax check")
for filename in sorted(os.listdir(HOOKS_DIR)):
    if not filename.endswith(".py"):
        continue
    script_path = os.path.join(HOOKS_DIR, filename)
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", script_path],
        capture_output=True,
        text=True,
    )
    test(f"{filename} compiles", result.returncode == 0, result.stderr.strip())

# --- Test 4: session-start.py produces valid JSON on empty input ---
print("\nsession-start.py")
session_start = os.path.join(HOOKS_DIR, "session-start.py")
if os.path.isfile(session_start):
    rc, stdout, stderr = run_hook(session_start, "{}")
    test("exits cleanly", rc == 0, f"exit code {rc}, stderr: {stderr}")
    if stdout:
        try:
            output = json.loads(stdout)
            test("valid JSON output", True)
            test(
                "has additionalContext key",
                "additionalContext" in output,
                f"keys: {list(output.keys())}",
            )
        except json.JSONDecodeError as e:
            test("valid JSON output", False, str(e))
else:
    test("session-start.py exists", False)

# --- Test 5: maintenance-check.py exits cleanly on empty input ---
print("\nmaintenance-check.py")
maint_check = os.path.join(HOOKS_DIR, "maintenance-check.py")
if os.path.isfile(maint_check):
    rc, stdout, stderr = run_hook(maint_check, "{}")
    test("exits cleanly on empty input", rc == 0, f"exit code {rc}, stderr: {stderr}")
    # With no transcript_path, it should exit silently (no block)
    test("no output on empty input (no block)", stdout == "", f"got: {stdout[:100]}")
else:
    test("maintenance-check.py exists", False)

# --- Test 6: .claude/rules/ directory exists and contains .md files ---
print("\n.claude/rules/")
rules_dir = os.path.join(STARTER_KIT_DIR, ".claude", "rules")
test(".claude/rules/ directory exists", os.path.isdir(rules_dir))
if os.path.isdir(rules_dir):
    md_files = [f for f in os.listdir(rules_dir) if f.endswith(".md")]
    test("contains .md files", len(md_files) > 0, f"found {len(md_files)} .md files")
    for expected in ["coding-standards.md", "traps.md", "quality-gate.md"]:
        test(
            f"{expected} exists",
            expected in md_files,
            f"not found in {md_files}",
        )

# --- Summary ---
print(f"\n{'=' * 40}")
total = passed + failed
print(f"  {passed}/{total} passed" + (f", {failed} failed" if failed else ""))
sys.exit(1 if failed else 0)
