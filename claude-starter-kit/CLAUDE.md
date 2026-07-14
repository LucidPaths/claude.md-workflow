# Project Instructions for Claude Code

> Universal rules live in `.claude/rules/core.md` (auto-loaded by Claude Code).
> This file holds project-specific facts only. Fill in the `[ADAPT]` sections on
> your first session — read the code first, then document what you found.

## Project Overview

<!-- [ADAPT] 2-3 sentences. What does it do? And explicitly: what is it NOT?
     Being clear about what the project ISN'T is the best defense against
     scope creep in AI suggestions. -->

## Key Directories

<!-- [ADAPT] Annotated tree of the directories that matter. -->

## Commands (the verify contract)

The `/verify` skill runs these commands and will not accept completion claims
without their output. Keep them current — stale commands make verification
silently meaningless.

<!-- [ADAPT]
- Build:     `npm run build`
- Test:      `npm test`
- Lint:      `npx eslint .`
- Typecheck: `npx tsc --noEmit`
-->

## Cross-File Contracts

Values that must stay in sync across files. One source of truth each
(Standard 5 in `.claude/rules/core.md`).

<!-- [ADAPT]
| Contract | Source of Truth | Mirror | Sync Method |
|----------|----------------|--------|-------------|
-->

## Lessons Learned

Bugs that prompted rules — the project's immune system.

<!-- [ADAPT]
| Bug | Root Cause | Rule Added |
|-----|-----------|------------|
-->

## Git Workflow

Fetch before pushing. Conventional commits: `feat:`, `fix:`, `docs:`,
`refactor:`, `chore:`. Hard don'ts (protected branches, protected files) are
enforced by git hooks, not by these instructions — run
`bash guards/install-guards.sh` once per clone.

## Session Continuity

`WORKING_STATE.md` in the project root is your curated memory: Corrections,
Codebase Insights, Deferred Ideas (template: `templates/WORKING_STATE.md`).
You maintain it directly — no automation ever writes to it. Corrections are
sacred: record them the moment they happen, never delete one without a
superseding entry. Keep the whole file under 100 lines.
