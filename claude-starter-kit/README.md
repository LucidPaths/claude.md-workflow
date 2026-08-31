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
| `.claude/hooks/maintenance-check.py` | Claude Code | Blocks session end if code changed but docs/working state weren't updated |
| `.claude/hooks/pre-compact.py` | Claude Code | Snapshots working state before context compaction (session transcendence) |
| `.claude/hooks/session-end.py` | Claude Code | Auto-persists working state on graceful session exit |
| `.claude/hooks/precommit-doc-check.py` | Claude Code | Blocks commits where code is staged but no docs are |
| `.claude/hooks/_state_utils.py` | Claude Code | Shared utilities for state management hooks |
| `.claude/skills/<name>/SKILL.md` | Fixed | 8 invocable disciplines — see **The Skills** below |
| `docs/research-then-implement.md` | Reference | Two-phase pattern: research, write a decision, then implement with fresh context |
| `.claude/PR_GUIDELINES.md` | Fixed | Standardized PR description format and commit conventions |
| `samples/` | Reference | Filled-in examples from real projects showing what adapted files look like |
| `guards/install-guards.sh` | Fixed | Installs pre-push / pre-commit git hooks — hard blocks a model cannot talk its way past |
| `.claude/protected-paths.txt` | Template | Path prefixes the pre-commit guard refuses (ships empty) |
| `tests/test_hooks.py` | Fixed | Validates that hooks parse, emit the current schema, and that skills are registerable |

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

The starter kit ships with 6 hooks covering the full session lifecycle: session-start, maintenance-check, pre-compact, session-end, precommit-doc-check, and shared utilities (_state_utils.py). Together these enable session transcendence — context survives both session boundaries and context compaction.

### Fixed vs Adaptive

**Fixed** files contain universal truths — coding standards, decision frameworks, git workflows. They work as-is in any project.

**Adaptive** sections (marked with `<!-- [ADAPT] ... -->`) are placeholders that the AI fills in as it learns your specific project. These include: project overview, key directories, build commands, architecture patterns, and project-specific traps.

## Key Features

### Session-Transcending Memory
The `WORKING_STATE.md` pattern gives the AI persistent working memory across sessions. It tracks active tasks, corrections, learnings, uncommitted work, and codebase insights — so every session starts where the last one left off.

### Battle-Tested Quality Gate
The "Before Submitting Changes" section isn't a generic checklist — each rule exists because a specific real bug prompted it. The lattice check works when you enforce it actively on every change, not as a checkbox to skim past.

### Verification Disciplines
Eight skills, each a way of not fooling yourself: `/adversarial-review` (overclaim in opposing directions, then adjudicate), `/proof` (the check that silently lied), `/rigor` (verified vs inferred vs assumed), `/paranoia` (one defect class per pass, to convergence), `/scalpel` (size the fix to the evidence), `/unverified` (where the "I don't know" died), `/shippable` (can a stranger run it), `/goal-loop` (nothing is done without a pre-declared machine-checkable proof).

### Automatic Maintenance (Claude Code)
Session hooks ensure docs stay current and working state is updated. The stop hook blocks if code changed but maintenance wasn't done. These require Claude Code — other tools get the standards but not the automation.

## The Skills

| Skill | Use it when |
|-------|-------------|
| `/adversarial-review` | Before merging a diff. Two passes overclaiming in opposite directions, then adjudication. |
| `/proof` | Before trusting a migration, dedup, backfill, mass-edit, or any "is it actually done?" claim over real data. |
| `/rigor` | On a reasoning problem with no artifact yet. Closes with a verified / inferred / assumed ledger. |
| `/paranoia` | End of a long session, or before a handoff. Hunts one unexhausted defect class per pass. |
| `/scalpel` | When the right *size* of a fix is part of the question. |
| `/unverified` | On anything producing claims from incomplete input, especially with a model in the loop. |
| `/shippable` | Before submitting, demoing, or handing over. |
| `/goal-loop` | To close a set of gaps end to end with subagents you judge rather than trust. |

### Why folder format matters

A skill must live at `.claude/skills/<name>/SKILL.md` with YAML frontmatter carrying `name` and
`description`. **A flat `.md` file directly inside `skills/` is never registered** — it silently
does nothing, forever. `tests/test_hooks.py` checks for this, because it is the easiest way to
ship a skill that cannot be invoked.

The `description` is the most important line in the file: it is what the model reads when deciding
whether the skill applies. Write it as a trigger condition ("Use when the user runs X or asks Y"),
not as a summary.

## Hard guards (optional, recommended)

Rules and hooks shape behaviour; they do not enforce it. For the things that must never happen,
install git-level guards:

```bash
bash guards/install-guards.sh            # protect main + master
bash guards/install-guards.sh main dev   # or name your own branches
```

- **pre-push** refuses pushes to protected branches
- **pre-commit** refuses commits touching prefixes listed in `.claude/protected-paths.txt`
  (ships empty — nothing is protected until you choose)

Overrides are deliberate human acts, not model-emittable text:

```bash
ALLOW_PROTECTED_PUSH=1 git push ...
ALLOW_PROTECTED_PATHS=1 git commit ...
```

Safe to re-run. A pre-existing hook this script did not install is reported and left untouched.

## Requirements

- **Python 3** — Required for the session hooks (most systems have this)
- **Git** — Required for session-start orientation and maintenance checks
- **Claude Code** — Required for hooks to fire automatically. Standards in CLAUDE.md work with any tool that reads project instruction files

## Verifying Hooks

Run the hook test to make sure everything parses correctly:

```bash
python3 tests/test_hooks.py     # 34/34 expected
```

The suite checks that hooks compile, that `session-start.py` emits the current output envelope,
and that every skill is in a format Claude Code actually registers.

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
