# Claude Starter Kit

A portable folder you drop into any repo to bootstrap high-quality, auditable, future-proofed AI-assisted development with Claude Code. Distilled from battle-tested patterns in the [HIVE](https://github.com/LucidPaths/HiveMind) project.

## Quick Start

1. **Copy** the contents of this folder into your repo root
2. **Commit** the files so Claude Code picks them up
3. **Start a Claude Code session** — the hooks and CLAUDE.md activate automatically

On first session, Claude will explore your codebase and fill in the `[ADAPT]` sections in CLAUDE.md. Future sessions build on that foundation.

## What's Inside

| File | Type | Purpose |
|------|------|---------|
| `CLAUDE.md` | Mixed | Project instructions — universal coding standards (fixed) + project-specific sections (adaptive) |
| `docs/PRINCIPLE_LATTICE.md` | Mixed | 5 axiomatic design principles — axioms are fixed, instantiations grow with your project |
| `.claude/settings.json` | Fixed | Registers session-start and session-stop hooks |
| `.claude/hooks/session-start.py` | Fixed | Auto-injects git state and next steps at session start |
| `.claude/hooks/maintenance-check.py` | Fixed | Blocks session end if code changed but docs weren't updated |
| `.claude/skills/structured-reasoning.md` | Fixed | Decision framework: priority hierarchy, stuck protocol, decomposition triggers |
| `.claude/skills/project-status.md` | Fixed | `/project-status` skill for quick project state overview |
| `.claude/skills/research-then-implement.md` | Fixed | `/research-decide` skill — two-phase pattern: research → decision file → implement with fresh context |
| `.claude/skills/adversarial-review.md` | Fixed | `/adversarial-review` skill — three-pass bug verification (bug hunter → disprover → referee) |
| `.claude/PR_GUIDELINES.md` | Fixed | Standardized PR description format and commit conventions |
| `docs/TASK_CONTRACT_TEMPLATE.md` | Template | Copy per-task to define explicit acceptance criteria and done conditions |

### Fixed vs Adaptive

**Fixed** files contain universal truths — coding standards, decision frameworks, git workflows. They work as-is in any project. Don't modify them unless you have a strong reason.

**Adaptive** sections (marked with `<!-- [ADAPT] ... -->` in HTML comments) are placeholders that Claude fills in as it learns your specific project. These include: project overview, key directories, build commands, architecture patterns, and project-specific traps.

## Requirements

- **Python 3** — Required for the session hooks (most systems have this)
- **Git** — Required for session-start orientation and maintenance checks
- **Claude Code** — The CLI tool this kit is designed for

## The Principle Lattice

Five principles guide every decision:

1. **Modularity** — Lego blocks, not monoliths
2. **Simplicity Wins** — Don't reinvent the wheel
3. **Errors Are Answers** — Every failure teaches
4. **Fix The Pattern** — Cure the root cause, not the symptom
5. **Secrets Stay Secret** — Nothing left open to exploitation

See `docs/PRINCIPLE_LATTICE.md` for the full lattice with details and demands.

## Credits

- Principle lattice concept and hook patterns adapted from [vincitamore/claude-org-template](https://github.com/vincitamore/claude-org-template)
- Distilled from the [HIVE](https://github.com/LucidPaths/HiveMind) project by LucidPaths
