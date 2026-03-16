# Project Instructions for Claude Code

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

## Coding Standards

These are the rules. Each one exists because a real bug prompted it. Follow them exactly.

### 1. Simplicity First

Prefer the simpler approach that already works. Three clear lines beat one clever abstraction. Don't create helpers for one-time operations. If something worked before, check git history before rewriting it.

### 2. Actionable Errors

Every error must say what happened, why, and what the user can do about it. `"Something went wrong"` is itself a bug.

### 3. No Dead Code

If you replace a function, remove the old one. No commented-out code, no unused imports, no `_`-prefixed variables that nothing references. If you add a function, something must call it.

### 4. Fix All Instances

When you find a bug, grep for the same pattern across the entire codebase. Fix every instance, or fix none. One fix creates a false sense of safety. This applies to security lists, validation, naming — everything.

### 5. Single Source of Truth for Cross-File Contracts

If two files must agree on a string, format, or list — there must be one authoritative definition that both reference. Never rely on comments like "must match foo.ts." When you discover a contract, add it to the table below and add cross-reference comments in both files.

### 6. User-Agent on External APIs

External services block requests without proper User-Agent headers. Always set one.

### 7. Closed By Default

Empty allowlists mean "deny all", not "allow all." This applies to permissions, feature flags, API access — anything where the safe default is "no."

### 8. Both Sides of the Boundary

When logic exists in two places (client + server, two languages, two config files), update both or update neither. One-sided updates create a false sense of safety worse than no update at all.

### Project-Specific Standards

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

## Session Traps

These are documented bugs in AI assistant behavior. Each one has caused real damage. The word "Stop." is a behavioral interrupt — when you catch yourself thinking the quoted phrase, halt and read the correction.

### Trap 1: "Let me optimize this"
**Stop.** Is it slow? Is the user complaining? If not, don't touch it.

### Trap 2: "The error says X, so I'll fix X"
**Stop.** The error might be downstream of the real bug. Trace backwards to the root cause.

### Trap 3: "I need to rewrite this function"
**Stop.** Check git history. Maybe a past version worked. Maybe revert, not rewrite.

### Trap 4: "While I'm here, I'll also clean up..."
**Stop.** Scope creep is the #1 session killer. Do exactly what was asked. If you see something worth improving, mention it — don't do it.

### Trap 5: "I think the user wants..."
**Stop.** If the request is ambiguous, **ask** — don't infer. The cost of asking is near zero. The cost of building the wrong thing is an entire session.

### Trap 6: "This looks correct to me"
**Stop.** If you're confirming something looks correct, you need to *prove* it — trace the logic, find a concrete input that exercises the path, verify the output. "Looks correct" without proof is just agreement. See `.claude/skills/adversarial-review.md`.

### Trap 7: "I'll fix this one place"
**Stop.** The same mistake exists in 3-5 other places — you just haven't hit them yet. Grep for the pattern. Fix every instance or fix none. One fix creates a false sense of safety. (Coding Standard #4 is the rule; this trap catches you in the moment.)

### Trap 8: "I'll add this to the validation list"
**Stop.** Which list? If validation, security, or permissions exist in two places (client + server, Rust + TypeScript, two config files), you MUST update both. Right now. Before you call it done. Updating one side is worse than updating neither. (Coding Standard #8 is the rule; this trap catches the specific moment you're about to forget the other side.)

### Project-Specific Traps

<!-- [ADAPT] Add traps discovered during development. Format:
     ### Trap N: "The tempting thing to say"
     **Stop.** Why it's wrong and what to do instead. -->

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

## Quality Gate — Before Submitting Changes

This gate exists because broken code has been shipped and marked "DONE" without verification. These rules are non-negotiable.

### Core Checks (do ALL, in order)

1. **Test the production path.** Tests must exercise the actual code flow, not a synthetic setup.
2. **Trace the full data flow.** If A triggers B triggers C, verify A→C end-to-end.
3. **Run the full test suite.** Test count must not decrease vs. previous runs.
4. **Grep for the pattern.** Every new pattern gets a codebase-wide search (Coding Standard #4).
5. **Check the Principle Lattice.** Score your changes against all 5 principles in `docs/PRINCIPLE_LATTICE.md`. This is not decorative — enforce it actively on every change, or the principles become wallpaper. Ask yourself each one explicitly: Modular? Simple? Errors visible? Pattern fixed everywhere? Secrets safe?
6. **No dead code.** If you added a function, something must call it (Coding Standard #3).
7. **Check for regressions.** `git diff` and verify you didn't break existing contracts.
8. **Stay in scope.** No unasked-for refactoring, no bonus features (Trap #4).

### Conditional Checks

9. Cross-file contract added? → Single source of truth or cross-ref in BOTH files (Coding Standard #5)
10. Touched a boundary in two places? → Updated both sides (Coding Standard #8)
11. Added a public function? → Something calls it and it's documented
12. Spawned a process? → Cleanup on exit

### Lessons Learned

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

Maintain a persistent state file at `WORKING_STATE.md` in the project root. See `docs/WORKING_STATE_TEMPLATE.md` for the template.

**On session start:** Read `WORKING_STATE.md` before doing anything else. It contains your own continuity — active tasks, things you learned, mistakes to avoid, ideas you parked.

**Update it** after completing significant steps, when the user corrects you, when you learn something undocumented, and before context-heavy operations.

**Rules:**
- **Track uncommitted work.** Always. If 5+ files are modified without a commit, note it prominently. The "20 fixes sitting on disk unpushed" situation must never happen.
- **Corrections are sacred.** When the user corrects you, write it down immediately. These are the highest-value entries — they prevent you from repeating the same mistake next session.
- **Prune aggressively.** Learnings promoted to CLAUDE.md get removed. Irrelevant deferred ideas get deleted. Keep under ~200 lines.
