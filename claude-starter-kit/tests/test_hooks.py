#!/usr/bin/env python3
"""
Smoke tests for starter kit (v2).

Verifies that:
1. settings.json is valid and references existing hook files
2. Hook scripts compile and run cleanly on empty/minimal input
3. session-start.py emits valid additionalContext JSON
4. change-check.py is silent on empty input and honors its loop guards
5. Rules, skills, templates, and guards exist; guards script is valid bash

Run: python3 tests/test_hooks.py
"""

import json
import os
import shutil
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
        print(f"  FAIL  {name}" + (f" -- {detail}" if detail else ""))
        failed += 1


def run_hook(script_path, stdin_data="{}"):
    result = subprocess.run(
        [sys.executable, script_path],
        input=stdin_data,
        capture_output=True,
        text=True,
        timeout=10,
        cwd=STARTER_KIT_DIR,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


# --- settings.json ---
print("\nsettings.json")
try:
    with open(SETTINGS_PATH) as f:
        settings = json.load(f)
    test("valid JSON", True)
except (json.JSONDecodeError, FileNotFoundError) as e:
    test("valid JSON", False, str(e))
    settings = {}

print("\nhook file references")
for event_name, event_hooks in settings.get("hooks", {}).items():
    for group in event_hooks:
        for hook in group.get("hooks", []):
            cmd = hook.get("command", "")
            if ".claude/hooks/" in cmd:
                script_name = cmd.split(".claude/hooks/")[-1].rstrip('"')
                script_path = os.path.join(HOOKS_DIR, script_name)
                test(
                    f"{event_name} -> {script_name} exists",
                    os.path.isfile(script_path),
                    f"not found: {script_path}",
                )

# --- syntax ---
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

# --- session-start.py ---
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

# --- change-check.py ---
print("\nchange-check.py")
change_check = os.path.join(HOOKS_DIR, "change-check.py")
if os.path.isfile(change_check):
    rc, stdout, stderr = run_hook(change_check, "{}")
    test("exits cleanly on empty input", rc == 0, f"exit code {rc}, stderr: {stderr}")

    # stop_hook_active guard: must be silent even if changes exist
    rc, stdout, stderr = run_hook(
        change_check, json.dumps({"stop_hook_active": True, "session_id": "test"})
    )
    test("silent when stop_hook_active", rc == 0 and stdout == "", f"got: {stdout[:100]}")

    # marker guard: second invocation with same session_id must be silent
    marker_dir = os.path.join(STARTER_KIT_DIR, ".claude", "hook-data")
    marker = os.path.join(marker_dir, "change-check-smoketest-session")
    os.makedirs(marker_dir, exist_ok=True)
    with open(marker, "w") as f:
        f.write("fired\n")
    rc, stdout, stderr = run_hook(
        change_check, json.dumps({"session_id": "smoketest-session"})
    )
    test("silent when marker exists", rc == 0 and stdout == "", f"got: {stdout[:100]}")
    os.remove(marker)
    if not os.listdir(marker_dir):
        os.rmdir(marker_dir)
else:
    test("change-check.py exists", False)

# --- rules ---
print("\n.claude/rules/")
rules_path = os.path.join(STARTER_KIT_DIR, ".claude", "rules", "core.md")
test("core.md exists", os.path.isfile(rules_path))
if os.path.isfile(rules_path):
    with open(rules_path, encoding="utf-8") as f:
        line_count = len(f.readlines())
    test(f"core.md under 100 lines (is {line_count})", line_count <= 100)

# --- skills ---
print("\n.claude/skills/")
skills_dir = os.path.join(STARTER_KIT_DIR, ".claude", "skills")
for expected in ["verify.md", "adversarial-review.md", "parallel-roadmap.md"]:
    test(f"{expected} exists", os.path.isfile(os.path.join(skills_dir, expected)))

# --- templates ---
print("\ntemplates/")
templates_dir = os.path.join(STARTER_KIT_DIR, "templates")
for expected in ["TASK_CONTRACT.md", "WORKING_STATE.md"]:
    test(f"{expected} exists", os.path.isfile(os.path.join(templates_dir, expected)))

# --- guards ---
print("\nguards/")
guards_script = os.path.join(STARTER_KIT_DIR, "guards", "install-guards.sh")
test("install-guards.sh exists", os.path.isfile(guards_script))
bash = shutil.which("bash")
if os.path.isfile(guards_script) and bash:
    result = subprocess.run(
        [bash, "-n", guards_script], capture_output=True, text=True
    )
    test("install-guards.sh valid bash (bash -n)", result.returncode == 0,
         result.stderr.strip())

# --- summary ---
print(f"\n{'=' * 40}")
total = passed + failed
print(f"  {passed}/{total} passed" + (f", {failed} failed" if failed else ""))
sys.exit(1 if failed else 0)
