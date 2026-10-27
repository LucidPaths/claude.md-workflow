# Claude Starter Kit

A portable folder you drop into any repo to bootstrap high-quality, auditable AI-assisted development. Distilled from battle-tested patterns in the [HIVE](https://github.com/LucidPaths/HiveMind) project.

**Standards are universal** — the principles, coding standards, traps, and quality gate apply to any AI coding assistant.

**Automation is Claude Code specific** — the hooks (`.claude/settings.json`, session-start, maintenance-check) use Claude Code's hook system. If you use a different tool, the hooks won't fire automatically, but the standards in CLAUDE.md still work as a project instruction file.

## Quick Start

1. **Copy** the contents of this folder into your repo root
2. **Commit** the files so your AI assistant picks them up
3. **Start a session** — the hooks and CLAUDE.md activate automatically

On first session, the AI will explore your codebase and fill in the `[ADAPT]` sections in CLAUDE.md. Future sessions build on that foundation.

## What's Inside

| File | Type | Purpose |
|------|------|---------|
| `CLAUDE.md` | Mixed | Project instructions — project-specific sections (adaptive) + context discipline and git workflow (fixed) |
| `docs/PRINCIPLE_LATTICE.md` | Mixed | 5 axiomatic design principles — axioms are fixed, instantiations grow with your project |
| `.claude/rules/coding-standards.md` | Fixed | 8 universal coding standards — auto-loaded by Claude Code |
| `.claude/rules/traps.md` | Fixed | 8 behavioral traps + anti-rationalization table — auto-loaded by Claude Code |
| `.claude/rules/quality-gate.md` | Fixed | Pre-submit verification checklist — auto-loaded by Claude Code |
| `docs/WORKING_STATE_TEMPLATE.md` | Template | Copy to `WORKING_STATE.md` in project root — session-transcending memory for the AI |
| `docs/TASK_CONTRACT_TEMPLATE.md` | Template | Copy per-task to define explicit acceptance criteria and done conditions |
| `docs/ROLE_TEMPLATE.md` | Template | Role-based workflow template (domain expertise, traps, checks, patterns, boundaries) |
| `docs/GLOBAL_ROUTER_TEMPLATE.md` | Template | Thin CLAUDE.md router for projects with many docs/ files |
| `.claude/settings.json` | Claude Code | Registers all lifecycle hooks |
| `.claude/hooks/session-start.py` | Claude Code | Auto-injects git state, working memory, and next steps at session start |
| `.claude/hooks/maintenance-check.py` | Claude Code | One-shot reminder to check docs and working state |
| `.claude/hooks/pre-compact.py` | Claude Code | Snapshots working state before context compaction (session transcendence) |
| `.claude/hooks/session-end.py` | Claude Code | Auto-persists working state on graceful session exit |
| `.claude/hooks/precommit-doc-check.py` | Claude Code | Code-only commit reminder with explicit acknowledgement |
| `.claude/hooks/_state_utils.py` | Claude Code | Shared utilities for state management hooks |
| `.claude/skills/<name>/SKILL.md` | Fixed | 11 invocable disciplines — see **The Skills** below |
| `docs/research-then-implement.md` | Reference | Two-phase pattern: research, write a decision, then implement with fresh context |
| `.claude/PR_GUIDELINES.md` | Fixed | Standardized PR description format and commit conventions |
| `samples/` | Reference | Filled-in examples from real projects showing what adapted files look like |
| `guards/install-guards.sh` | Fixed | Installs pre-push / pre-commit accident guards; bypassable by shell users |
| `.claude/protected-paths.txt` | Template | Path prefixes the pre-commit guard refuses (ships empty) |
| `tests/test_hooks.py` | Fixed | Validates that hooks parse, emit the current schema, and that skills are registerable |
| `tests/test_hook_behavior.py` | Fixed | Runs the hooks against disposable Git repositories: state retention, transcript shapes, commit classification, Stop-loop handling |
| `docs/SKILL-STANDARD.md` | Reference | How a skill is written: three kinds of decision rule, banned vague terms, standalone defaults, the closing block |
| `tests/skill_lint.py` | Fixed | Lints a skills folder against the standard; `--skills-dir` points it at your own skills |
| `tests/test_skill_lint.py` | Fixed | Proves each lint check fires on a planted defect, and that the shipped skills pass |

### Modular Architecture

The kit uses a **two-layer architecture**:
- **`CLAUDE.md`** — project-specific configuration (adaptive sections, cross-file contracts)
- **`.claude/rules/`** — universal standards (coding standards, traps, quality gate) auto-loaded by Claude Code without explicit imports

This separation means universal rules stay clean and version-controlled independently of project-specific adaptations.

**Everything above loads into every session.** That is the point, and it is also the cost — the
[memory docs](https://code.claude.com/docs/en/memory) advise staying under 200 lines per file
because longer instructions reduce adherence. The kit's always-loaded set is deliberately small, and
the trap list is capped at 8 for the same reason: a list you can hold in your head fires, a list you
skim does not.

#### Scoping your own rules to file types

When you add project rules of your own, scope them so they load only when relevant. A rule with a
`paths` frontmatter key loads when Claude reads a matching file, instead of at every launch:

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "src/**/*.{test,spec}.ts"
---

# API rules

- Every endpoint validates its input before touching the database
- Errors use the standard response shape
```

`paths` takes a YAML list of globs and supports brace expansion. **A rule with no `paths` key loads
unconditionally** — which is why the three shipped rules don't use it: coding standards, traps and
the quality gate apply to any file in any language, so scoping them would make them silently absent
exactly when they matter. Use `paths` for rules that genuinely only apply to part of your tree.

### Hook Lifecycle Coverage

The starter kit registers five events: SessionStart, Stop, PreCompact, SessionEnd and PreToolUse. `_state_utils.py` is a shared helper, not a registered hook. These scripts support continuity; installed-host behavior still requires qualification.

### Fixed vs Adaptive

**Fixed** files contain universal truths — coding standards, decision frameworks, git workflows. They work as-is in any project.

**Adaptive** sections (marked with `<!-- [ADAPT] ... -->`) are placeholders that the AI fills in as it learns your specific project. These include: project overview, key directories, build commands, architecture patterns, and project-specific traps.

## Key Features

### Session-Transcending Memory
The `WORKING_STATE.md` pattern gives the AI persistent working memory across sessions. It tracks active tasks, corrections, learnings, uncommitted work, and codebase insights — so every session starts where the last one left off.

### Battle-Tested Quality Gate
The "Before Submitting Changes" section isn't a generic checklist — each rule exists because a specific real bug prompted it. The lattice check works when you enforce it actively on every change, not as a checkbox to skim past.

### Verification Disciplines
Eleven skills, each a way of not fooling yourself: `/pick-skills` (the discipline chosen on purpose, not guessed), `/adversarial-review` (overclaim in opposing directions, then adjudicate), `/proof` (the check that silently lied), `/rigor` (verified vs inferred vs assumed), `/paranoia` (one defect class per pass, to convergence), `/scalpel` (size the fix to the evidence), `/unverified` (where the "I don't know" died), `/shippable` (can a stranger run it), `/blueprint` (a plan reviewed only by its author is a wish list), `/goal-loop` (nothing is done without a pre-declared machine-checkable proof), `/fleet-economics` (the same proof run three times proves nothing new).

### Automatic Maintenance (Claude Code)
Session hooks capture context and remind about maintenance; they do not verify documentation accuracy. Stop checks uncommitted files (not a session baseline), reminds once, and honors the host loop guard. These contracts target Claude Code; other hosts need adapters.

## The Skills

| Skill | Use it when |
|-------|-------------|
| `/pick-skills` | Before a broad task, or when you are unsure which skill fits. Prints the chain it will run, and the gaps no skill covers. |
| `/adversarial-review` | Before merging a diff. Two passes overclaiming in opposite directions, then adjudication. |
| `/proof` | Before trusting a migration, dedup, backfill, mass-edit, or any "is it actually done?" claim over real data. |
| `/rigor` | On a reasoning problem with no artifact yet. Closes with a verified / inferred / assumed ledger. |
| `/paranoia` | End of a long session, or before a handoff. Hunts one unexhausted defect class per pass. |
| `/scalpel` | When the right *size* of a fix is part of the question. |
| `/unverified` | On anything producing claims from incomplete input, especially with a model in the loop. |
| `/shippable` | Before submitting, demoing, or handing over. |
| `/blueprint` | Before a build that spans several steps, owners or contracts: inventory, locked design, a gap ledger with negative controls, a blind critic, the user's approval. |
| `/goal-loop` | To close a set of gaps end to end with subagents you judge rather than trust. |
| `/fleet-economics` | When subagents do the work: which model tier builds and critiques each slice, and the cheapest test level that proves it. |

### Why folder format matters

A skill must live at `.claude/skills/<name>/SKILL.md` with YAML frontmatter carrying `name` and
`description`. **A flat `.md` file directly inside `skills/` is never registered** — it silently
does nothing, forever. `tests/test_hooks.py` checks for this, because it is the easiest way to
ship a skill that cannot be invoked.

The `description` is the most important line in the file: it is what the model reads when deciding
whether the skill applies. Write it as a trigger condition ("Use when the user runs X or asks Y"),
not as a summary.

Every decision rule in a skill is DETERMINISTIC, a named DEFAULT, or an ASK to the user, and no skill
needs another to work: a borrowed rule comes with a standalone default inline. The full rules are in
`docs/SKILL-STANDARD.md`; `python tests/skill_lint.py` checks them.

## Local accident guards (optional)

Local Git hooks can prevent accidental prohibited pushes and commits on the normal path:

```bash
bash guards/install-guards.sh            # protect main + master
bash guards/install-guards.sh main dev   # or name your own branches
```

- **pre-push** refuses pushes to protected branches
- **pre-commit** refuses commits touching prefixes listed in `.claude/protected-paths.txt`
  (ships empty — nothing is protected until you choose)

Overrides are explicit, but not human-only. An agent with shell access can set them too:

```bash
ALLOW_PROTECTED_PUSH=1 git push ...
ALLOW_PROTECTED_PATHS=1 git commit ...
```

Safe to re-run. A pre-existing hook this script did not install is reported and left untouched.
Local hooks are also bypassable with `--no-verify` or filesystem edits. Use remote branch
protection and separately controlled permissions for enforcement against that actor.

## Requirements

- **Python 3.11** — Tested by the offline suites and CI; hooks use only the standard library
- **Git and Bash** — Required for Git checks, the configured command hooks and optional guards
- **Claude Code** — Required for hooks to fire automatically. Standards in CLAUDE.md work with any tool that reads project instruction files

## Verifying Hooks

Run the hook test to make sure everything parses correctly:

```bash
python3 tests/test_hooks.py                 # 45/45 expected
python3 tests/test_hook_behavior.py -v      # hook behavior in disposable Git repositories
python3 tests/skill_lint.py                 # RESULT PASS expected
python3 -m unittest discover -s tests       # all of the above, as unittest cases
```

The smoke suite checks compilation, references, the SessionStart envelope and that every skill is in
a format Claude Code actually registers. The behavior suite uses disposable Git repositories to
exercise state retention, transcript shapes, commit classification/acknowledgement and Stop-loop
handling. Neither suite runs an installed Claude session or measures model effectiveness. The lint
checks every skill against `docs/SKILL-STANDARD.md`, and its tests plant one defect per check to show
each one fires.

### Hook contract and limits

The implementation follows the [official hooks reference](https://code.claude.com/docs/en/hooks):
PreToolUse uses `hookSpecificOutput` with `hookEventName`, `permissionDecision: "deny"` and
`permissionDecisionReason`; silence leaves normal permissions unchanged. Stop uses top-level
`decision: "block"`/`reason`, checks `stop_hook_active`, and reads `last_assistant_message`.
Registered commands use the host's `CLAUDE_PROJECT_DIR` (quoted for spaces).

- The doc reminder recognizes literal `git [-C dir] commit`, optionally after `cd dir &&`,
  common message flags, amend and `-a`/`--all` tracked changes. For `-a`, it updates a temporary
  copy of the index and compares the net candidate to HEAD (or the empty tree on unborn branches).
  Canceling staged/worktree edits do not count. The real index is not staged or refreshed and no
  commit is created; Git may run configured clean filters and write blobs while preparing the copy.
  It never executes the supplied shell command. Aliases, wrappers, expansion, pathspec commits,
  message files and compound mutation commands are not interpreted; review these manually.
  It is not a shell security policy.
- Test classification uses directory/name conventions, not `test`/`spec` substrings.
  Markdown/reStructuredText and named text docs suppress the reminder; an unrelated `.txt`
  does not. Staging a doc still does not prove relevance. To acknowledge a code-only commit,
  add a message paragraph such as `Docs-Unnecessary: internal refactor; public behavior unchanged`.
- State reads and writes prefer existing `docs/WORKING_STATE.md`, then root `WORKING_STATE.md`;
  if neither exists, new state goes under `docs/`. Keep only one authoritative file.
- Missing, unreadable or unsupported transcripts do not clear existing state. Flat records and
  nested `message` records are supported; only sections with usable new context are refreshed.
  Other sections (including custom ones and horizontal rules) remain intact. Level-two section
  headings inside backtick/tilde fences are ignored; closers must use the same marker and at least
  the opening length. An unclosed fence skips the update rather than appending inside an example.
  Failed predecessor reads abort the write; replacement is atomic, but **not** a concurrent-writer lock.
- Use one session writer per worktree. The shared compaction snapshot is not session-isolated;
  crash recovery and concurrent-session behavior are not qualified by these tests.
- Transcript excerpts and command fragments can be sensitive. State and hook-data are ignored
  by default, not redacted. Inspect before deliberately sharing or force-adding them. Gitignore
  does not untrack files already committed.

Before adopting the hooks, exercise start → work → compact → resume → exit in the installed
Claude version. The offline tests establish script behavior, not that lifecycle qualification.

## The Principle Lattice

Five axioms guide every decision:

1. **Modularity** — Lego blocks, not monoliths
2. **Simplicity Wins** — Don't reinvent the wheel
3. **Errors Are Answers** — Every failure teaches
4. **Fix The Pattern** — Cure the root cause, not the symptom
5. **Secrets Stay Secret** — Nothing left open to exploitation

See `docs/PRINCIPLE_LATTICE.md` for the full lattice with details.

## Credits

- Principle lattice concept and hook patterns adapted from [vincitamore/claude-org-template](https://github.com/vincitamore/claude-org-template)
- Distilled from the [HIVE](https://github.com/LucidPaths/HiveMind) project by LucidPaths
