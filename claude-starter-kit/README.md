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
| `CLAUDE.md` | Mixed | Project instructions — universal coding standards (fixed) + project-specific sections (adaptive) |
| `docs/PRINCIPLE_LATTICE.md` | Mixed | 5 axiomatic design principles — axioms are fixed, instantiations grow with your project |
| `docs/WORKING_STATE_TEMPLATE.md` | Template | Copy to `WORKING_STATE.md` in project root — session-transcending memory for the AI |
| `docs/TASK_CONTRACT_TEMPLATE.md` | Template | Copy per-task to define explicit acceptance criteria and done conditions |
| `docs/ROLE_TEMPLATE.md` | Template | Role-based workflow template (domain expertise, traps, checks, patterns, boundaries) |
| `docs/GLOBAL_ROUTER_TEMPLATE.md` | Template | Thin CLAUDE.md router for projects with many docs/ files |
| `.claude/settings.json` | Claude Code | Registers all lifecycle hooks |
| `.claude/hooks/session-start.py` | Claude Code | Auto-injects git state, working memory, and next steps at session start |
| `.claude/hooks/maintenance-check.py` | Claude Code | Blocks session end if code changed but docs/working state weren't updated |
| `.claude/hooks/pre-compact.py` | Claude Code | Snapshots working state before context compaction (session transcendence) |
| `.claude/hooks/session-end.py` | Claude Code | Auto-persists working state on graceful session exit |
| `.claude/hooks/precommit-doc-check.py` | Claude Code | Blocks commits where code is staged but no docs are |
| `.claude/hooks/_state_utils.py` | Claude Code | Shared utilities for state management hooks |
| `.claude/skills/structured-reasoning.md` | Fixed | Decision framework: priority hierarchy, verification levels, stuck protocol |
| `.claude/skills/project-status.md` | Fixed | `/project-status` — quick project state overview |
| `.claude/skills/research-then-implement.md` | Fixed | `/research-decide` — two-phase pattern: explore → decide → implement with fresh context |
| `.claude/skills/adversarial-review.md` | Fixed | `/adversarial-review` — three-pass bug verification (bug hunter → disprover → referee) |
| `.claude/skills/codebase-audit.md` | Fixed | `/codebase-audit` — systematic health check: silent failures, dead code, contract drift, security |
| `.claude/PR_GUIDELINES.md` | Fixed | Standardized PR description format and commit conventions |
| `tests/test_hooks.py` | Fixed | Validates that hook scripts parse and run without errors |

### Hook Lifecycle Coverage

The starter kit ships with 6 hooks covering the full session lifecycle: session-start, maintenance-check, pre-compact, session-end, precommit-doc-check, and shared utilities (_state_utils.py). Together these enable session transcendence — context survives both session boundaries and context compaction.

### Fixed vs Adaptive

**Fixed** files contain universal truths — coding standards, decision frameworks, git workflows. They work as-is in any project.

**Adaptive** sections (marked with `<!-- [ADAPT] ... -->`) are placeholders that the AI fills in as it learns your specific project. These include: project overview, key directories, build commands, architecture patterns, and project-specific traps.

## Key Features

### Session-Transcending Memory
The `WORKING_STATE.md` pattern gives the AI persistent working memory across sessions. It tracks active tasks, corrections, learnings, uncommitted work, and codebase insights — so every session starts where the last one left off.

### Battle-Tested Quality Gate
The "Before Submitting Changes" section isn't a generic checklist — each rule exists because a specific real bug prompted it. The lattice check works when you enforce it actively on every change, not as a checkbox to skim past.

### Adversarial Review
`/adversarial-review` exploits sycophancy bias in opposing directions to find real bugs — overclaim in pass 1, disprove in pass 2, adjudicate in pass 3.

### Automatic Maintenance (Claude Code)
Session hooks ensure docs stay current and working state is updated. The stop hook blocks if code changed but maintenance wasn't done. These require Claude Code — other tools get the standards but not the automation.

## Requirements

- **Python 3** — Required for the session hooks (most systems have this)
- **Git** — Required for session-start orientation and maintenance checks
- **Claude Code** — Required for hooks to fire automatically. Standards in CLAUDE.md work with any tool that reads project instruction files

## Verifying Hooks

Run the hook test to make sure everything parses correctly:

```bash
python3 tests/test_hooks.py
```

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
