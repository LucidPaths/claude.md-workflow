# Project Instructions for Claude Code

> Universal rules (coding standards, traps, quality gate) are in `.claude/rules/`. Claude Code loads them automatically.

> **First Session Bootstrap:** When starting your first session on this project, explore the codebase and fill in all `[ADAPT]` sections below. Read the code, understand the structure, document what you find. Future sessions depend on this orientation. The `[ADAPT]` markers are inside HTML comments — replace them with real content.

---

## Project Overview

<!-- [ADAPT] Describe this project in 2-3 sentences. What does it do? What is it NOT?
     Example: "A REST API for managing inventory. It is NOT a frontend — the React app lives in a separate repo."
     Being clear about what the project ISN'T prevents scope creep in AI suggestions. -->

### What This Project Is NOT

<!-- [ADAPT] Explicitly list what this project is NOT. This prevents Claude from drifting.
     Examples:
     - "NOT a full-stack app — backend only. Don't suggest frontend components."
     - "NOT a library — it's a CLI tool. Don't add exports or public API surface."
     This section is the #1 defense against scope creep. Be specific and harsh. -->

## Key Directories

<!-- [ADAPT] Map out the project structure. Annotate each directory.
     Example:
     ```
     src/
     ├── components/    # React UI components
     ├── lib/           # Shared utilities and helpers
     ├── api/           # Backend API routes
     └── types/         # Shared TypeScript types
     ```
-->

## Development Guidelines

<!-- [ADAPT] List project-specific gotchas and rules as you discover them. Examples:
     - "Use pnpm, not npm"
     - "Config format is YAML, not JSON"
     - "Never import from `internal/` outside the package"
     - "Tests must pass before pushing: `npm test`"
-->

## Common Tasks

### Building
<!-- [ADAPT] Your build command. Example: `npm run build` -->

### Running Development Mode
<!-- [ADAPT] Your dev command. Example: `npm run dev` -->

### Running Tests
<!-- [ADAPT] Your test command. Example: `npm test` -->

---

### Project-Specific Coding Standards

<!-- [ADAPT] Add standards specific to your tech stack as you discover them. Examples:
     - "Always use `const` assertions for TypeScript enums"
     - "Shell scripts must use `set -euo pipefail`"
     - "All database queries use parameterized statements (never string interpolation)"
-->

---

## Cross-File Contracts

Track contracts here so they don't drift silently. See Coding Standard #5.

<!-- [ADAPT] Track contracts here as you discover them.

     | Contract | Source of Truth | Mirror | Sync Method |
     |----------|----------------|--------|-------------|
     | Example: API routes | routes.ts | client.ts | Cross-ref comment |
-->

---

## What Each Key File Does

<!-- [ADAPT] Fill this in as you explore the codebase.

     | File | Purpose | Touch carefully? |
     |------|---------|------------------|
     | src/index.ts | Entry point, initializes app | Yes — core logic |
     | src/api/routes.ts | API route definitions | Moderate |
     | src/types.ts | Shared types and constants | Usually safe |
-->

## Current State (Honest Assessment)

<!-- [ADAPT] Track what works, what's broken, what's missing. Be honest — Claude
     should know what's incomplete, not just what exists.

     | Component | Status | Gap |
     |-----------|--------|-----|
     | Auth flow | Working | None |
     | Email sending | PARTIAL | Templates not implemented yet |
     | Search | MISSING | Only placeholder, no real indexing |

     Status values: Working, PARTIAL, MISSING, CRUDE, BROKEN
     Update this table as the project evolves. -->

## Architecture Patterns

<!-- [ADAPT] Document key architectural patterns as they emerge. Examples:
     - Data flow diagrams
     - State management approach
     - API request/response patterns
-->

---

## Git Workflow (MANDATORY)

**ALWAYS sync with main before pushing:**
```bash
git fetch origin
git merge origin/main --no-edit
git push -u origin <branch-name>
```

Never push without fetching first. Commit messages follow conventional style: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`.

---

### Project-Specific Traps

<!-- [ADAPT] Add traps discovered during development. Format:
     ### Trap N: "The tempting thing to say"
     **Stop.** Why it's wrong and what to do instead. -->

### Quality Gate — Lessons Learned

<!-- [ADAPT] Track bugs that prompted rules. This is the project's immune system.

| Bug | Root Cause | Rule Added |
|-----|-----------|------------|
| Example: API key in error message | Raw error passed to toast | P5 check in error handler |
| Example: Tests pass but feature broken | Test bypassed real code path | "Test the production path" rule |
-->

---

## "When Editing X, Check Y" Rules

<!-- [ADAPT] Add conditional rules as you discover dangerous edit patterns. Format:

     ### When editing [area]:
     1. Check [thing that breaks if you forget]
     2. Verify [related invariant]
     3. Update [related file/config]
-->

---

## Context Discipline

**Research and implementation are separate phases.** When a task requires exploring 5+ files or choosing between approaches, don't mix thinking and doing — research first, write a concrete decision, then implement with fresh focus. See `.claude/skills/research-then-implement.md` for the full pattern.

**Don't use subagents/task tools for research.** Do research directly with Read/Grep/Glob. Subagents burn 5-10x more tokens for the same result. Only use subagents for truly independent parallel *write* tasks.

---

## Session Continuity

Maintain a persistent state file at `docs/WORKING_STATE.md` (or `WORKING_STATE.md` in the project root). See `docs/WORKING_STATE_TEMPLATE.md` for the template.

**On session start:** Read `WORKING_STATE.md` before doing anything else. It contains your own continuity — active tasks, things you learned, mistakes to avoid, ideas you parked.

**Update it** after completing significant steps, when the user corrects you, when you learn something undocumented, and before context-heavy operations.

**Rules:**
- **Track uncommitted work.** Always. If 5+ files are modified without a commit, note it prominently. The "20 fixes sitting on disk unpushed" situation must never happen.
- **Corrections are sacred.** When the user corrects you, write it down immediately. These are the highest-value entries — they prevent you from repeating the same mistake next session.
- **Prune aggressively.** Learnings promoted to CLAUDE.md get removed. Irrelevant deferred ideas get deleted. Keep under ~200 lines.

### Self-Improvement Lifecycle

Discoveries follow a promotion path:

1. **Session discovery** → Note it in WORKING_STATE.md Learnings section
2. **Proven stable across 3+ sessions** → Promote to CLAUDE.md `[ADAPT]` section
3. **If promoted to CLAUDE.md, remove from WORKING_STATE.md** — no duplication

**Corrections are sacred — never auto-pruned.** User corrections are the highest-value entries. They survive until explicitly superseded by a newer correction or promoted to a permanent rule.
