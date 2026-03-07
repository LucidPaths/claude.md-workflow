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
     - "NOT meant to support every database — PostgreSQL only. Don't abstract the DB layer."
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

## Principles

This project follows 5 axiomatic principles. See [`docs/PRINCIPLE_LATTICE.md`](docs/PRINCIPLE_LATTICE.md) for the full lattice with details.

| # | Principle | Axiom |
|---|-----------|-------|
| 1 | **Modularity** | Lego blocks, not monoliths |
| 2 | **Simplicity Wins** | Don't reinvent the wheel. Code exists to be used |
| 3 | **Errors Are Answers** | Every failure teaches. Errors must be actionable |
| 4 | **Fix The Pattern** | Cure the root cause. Don't treat symptoms |
| 5 | **Secrets Stay Secret** | Nothing left open to exploitation |

When making design decisions, check against these principles. If a choice violates one, reconsider.

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

## Architecture Patterns

<!-- [ADAPT] Document key architectural patterns as they emerge. Examples:
     - Data flow diagrams
     - State management approach
     - API request/response patterns
     - Authentication flow
-->

## Things to Avoid

These are universal anti-patterns that cause real damage. They apply every session.

- **Don't add features, refactoring, or "improvements" beyond what was asked.** A bug fix doesn't need surrounding code cleaned up. A simple feature doesn't need extra configurability.
- **Don't add error handling for scenarios that can't happen.** Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs).
- **Don't create helpers or abstractions for one-time operations.** Three similar lines of code is better than a premature abstraction. Don't design for hypothetical future requirements.
- **Don't add docstrings, comments, or type annotations to code you didn't change.** Touch only what's relevant to the task.
- **Don't use subagents/task tools for research.** Do research directly with Read/Grep/Glob. Subagents burn 5-10x more tokens for the same result. Only use subagents for truly independent parallel *write* tasks.
- **Don't leave backwards-compatibility shims.** No renaming unused `_vars`, no re-exporting dead types, no `// removed` comments. If it's unused, delete it completely.

<!-- [ADAPT] Add project-specific "don't" rules as you discover them. Format:
     - **Don't [thing].** [Why it's wrong and what to do instead.] -->

## Cross-File Contracts

When two files must agree on a string value, format, or list — there MUST be a single source of truth that both reference. This is the #1 source of silent bugs in every multi-file codebase.

**When you discover a cross-file contract:**
1. First, try to make it a single file (best — builder + parser in one place)
2. If language boundaries prevent that, add explicit cross-reference comments in BOTH files
3. Add the contract to this table
4. If the contract is security-sensitive, add a test asserting both sides match

<!-- [ADAPT] Track contracts here as you discover them.

     | Contract | Source of Truth | Mirror | Sync Method |
     |----------|----------------|--------|-------------|
     | Example: API routes | routes.ts | client.ts | Cross-ref comment |
-->

---

## Coding Standards (CRITICAL)

These patterns prevent bugs that occur in every codebase. **Follow them exactly.**

### 1. Simple Solutions Over Complex Ones

**ALWAYS prefer the simpler approach that already works.**

```
BAD:  "Let me add a complex retry mechanism with exponential backoff"
GOOD: "Just make the simple request work first"

BAD:  "Let me create an abstraction layer for this one-time operation"
GOOD: "Three similar lines of code is better than a premature abstraction"
```

If something worked before, check git history before rewriting it.

### 2. Error Messages Must Be Actionable

```
// WRONG — useless error
throw new Error("Something went wrong");

// RIGHT — says what happened, why, and what to do
throw new Error(`Failed to connect to ${url}: ${err.message}. Check if the server is running.`);
```

Every error must say what happened, why, and what the user (or developer) can do about it.

### 3. Don't Create Dead Code

If you replace a function or variable, **remove the old one.** Don't leave commented-out code, unused imports, or variables prefixed with `_` that nothing references. Dead code is a lie about the system.

### 4. Check Git History Before "Fixing"

If something used to work:
```bash
git log --oneline --all | grep -i "relevant-keyword"  # Find when it changed
git show <commit>:path/to/file                         # See old working version
```

Often the fix is reverting to what worked, not adding more code.

### 5. Fix ALL Instances of a Pattern

When you find a bug, **search for the same pattern everywhere**:

```bash
# Found a null check bug? Check ALL similar accesses
grep -rn "\.property" src/

# Found a missing validation? Check ALL endpoints
grep -rn "req.body" src/

# One bug usually means the same mistake exists in 3-5 other places.
```

Fix them all or none. Fixing one creates a false sense of safety.

### 6. No Cross-File String Contracts Without a Shared Source

If two files must agree on a string value, format, or list — there MUST be a single source of truth that both reference. Never rely on comments like "must match foo.ts".

```
BAD:  // File A defines format "user:123", File B parses with regex /user:(\d+)/
      // They will drift. Guaranteed.

GOOD: // shared/formats.ts — single file with builder + parser
      export function buildUserId(id: number) { return `user:${id}`; }
      export function parseUserId(str: string) { return parseInt(str.split(':')[1]); }
```

When you discover a cross-file contract, add it to the Cross-File Contracts table above.

### 7. Set User-Agent for External API Calls

External services block or rate-limit requests without proper User-Agent headers. Always set one.

```
// WRONG — many APIs will reject this
fetch('https://api.example.com/data')

// RIGHT
fetch('https://api.example.com/data', {
  headers: { 'User-Agent': 'MyApp/1.0' }
})
```

### 8. Closed By Default

Security boundaries must default to rejecting everything, not accepting everything.

```
// WRONG — empty allowlist means "allow all" (inverted security model)
if (allowedUsers.length > 0 && !allowedUsers.includes(user)) { reject(); }

// RIGHT — empty allowlist means "allow none" (closed by default)
if (!allowedUsers.includes(user)) { reject(); }
```

This applies to permissions, feature flags, API access, input validation — anything where the safe default is "no." Never make an empty list mean "accept all."

### 9. Dual-Layer Changes Must Update Both Sides

When logic exists in two places (client + server, frontend + backend, two config files), updating one without the other creates a silent bug that passes all obvious checks.

```
// If you add a new "dangerous" operation:
//   1. Add it to the server-side check    ← easy to remember
//   2. Add it to the client-side check    ← easy to forget
//   3. Add it to the cross-file contracts table above

// If validation exists in both API and UI:
//   Update BOTH. Test BOTH. Document the contract.
```

**Rule of thumb:** Before finishing any change, grep for the same constant/string/pattern in other files. If you find it in two places, update both.

### Project-Specific Standards

<!-- [ADAPT] Add standards specific to your tech stack as you discover them. Examples:
     - "Always use `const` assertions for TypeScript enums"
     - "Shell scripts must use `set -euo pipefail`"
     - "Python imports: stdlib, third-party, local (separated by blank lines)"
     - "All database queries use parameterized statements (never string interpolation)"
-->

---

## Git Workflow (MANDATORY)

**ALWAYS sync with main before pushing:**
```bash
git fetch origin
git merge origin/main --no-edit
git push -u origin <branch-name>
```

This prevents branches from falling behind and avoids merge conflicts. Never push without fetching first.

**Commit messages** follow conventional style:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code restructuring
- `chore:` Maintenance tasks

Keep the first line under 72 characters, add details in the body if needed.

---

## Common Session Traps

These are documented bugs in Claude's behavior. Each one has caused real damage in real projects. The word "Stop." is a behavioral interrupt — when you catch yourself thinking the quoted phrase, halt and read the correction.

### Trap 1: "Let me optimize this"
**Stop.** Is it slow? Is the user complaining? If not, don't touch it. Premature optimization is the root of all evil.

### Trap 2: "I'll fix this one place"
**Stop.** Search for the same pattern. Fix them all or none. One fix creates a false sense of safety.

### Trap 3: "The error says X, so I'll fix X"
**Stop.** The error might be downstream of the real bug. Trace backwards to the root cause before touching code.

### Trap 4: "I need to rewrite this function"
**Stop.** Check git history. Maybe a past version worked. Maybe revert, not rewrite. `git log` is your friend.

### Trap 5: "While I'm here, I'll also clean up..."
**Stop.** Scope creep is the #1 session killer. Do exactly what was asked. If you see something worth improving, mention it — don't do it. Unasked-for changes waste context, introduce risk, and make PRs harder to review.

### Trap 6: "I'll add this to the validation list"
**Stop.** If validation/security/permissions exist in two places (client + server, two config files, two languages), you MUST update both. Updating one side creates a false sense of safety worse than updating neither. Grep for the same string in other files before calling it done.

### Trap 7: "I'll wrap this in a helper for reuse"
**Stop.** Is it actually used more than once *right now*? If not, inline it. Premature abstraction is worse than duplication — it couples code that shouldn't be coupled and makes future changes harder, not easier. Wait until you have 3 real instances before abstracting.

### Trap 8: "I think the user wants..."
**Stop.** If the request is ambiguous, **ask** — don't infer. The cost of asking one question is near zero. The cost of building the wrong thing is an entire session wasted. Stated intent > inferred intent > assumed intent, always.

### Trap 9: "This looks correct to me"
**Stop.** Sycophancy alert. If you're confirming something looks correct, you need to *prove* it — trace the logic, find a concrete input that exercises the path, verify the output. "Looks correct" without proof is just agreement, not analysis. See `.claude/skills/adversarial-review.md`.

### Project-Specific Traps

<!-- [ADAPT] Add traps discovered during development. Format:
     ### Trap N: "The tempting thing to say"
     **Stop.** Why it's wrong and what to do instead. -->

---

## What Each Key File Does

The "Touch carefully" column tells you the blast radius. **Yes** = changes here cascade widely; read the whole file before editing. **Moderate** = self-contained but important. **Usually safe** = low-risk changes.

<!-- [ADAPT] Fill this in as you explore the codebase.

     | File | Purpose | Touch carefully? |
     |------|---------|------------------|
     | src/index.ts | Entry point, initializes app | Yes — core logic |
     | src/api/routes.ts | API route definitions | Moderate |
     | src/types.ts | Shared types and constants | Usually safe |
-->

## Current State (Honest Assessment)

<!-- [ADAPT] Track what works, what's broken, what's missing. Be honest — Claude
     should know what's incomplete, not just what exists. This prevents it from
     building on assumptions about features that don't work yet.

     | Component | Status | Gap |
     |-----------|--------|-----|
     | Auth flow | Working | None |
     | Email sending | PARTIAL | Templates not implemented yet |
     | Search | MISSING | Only placeholder, no real indexing |
     | Rate limiting | CRUDE | Fixed window, needs sliding window |

     Status values: Working, PARTIAL, MISSING, CRUDE, BROKEN
     Update this table as the project evolves. -->

## "When Editing X, Check Y" Rules

These conditional rules fire when you're working in specific areas. They prevent the most common cascade failures.

<!-- [ADAPT] Add conditional rules as you discover dangerous edit patterns. Format:

     ### When editing [area]:
     1. Check [thing that breaks if you forget]
     2. Verify [related invariant]
     3. Update [related file/config]

     Examples:
     ### When editing API routes:
     1. Update the client-side API wrapper if the endpoint signature changed
     2. Update API documentation/swagger if it exists
     3. Check if any tests reference the old endpoint

     ### When editing database schema:
     1. Create a migration — never edit the schema directly
     2. Check all queries that touch the modified table
     3. Verify seed data still matches the schema

     ### When adding a new feature:
     1. Add logging at lifecycle events (init, success, error)
     2. Add to the "Current State" table above
     3. Update ROADMAP.md or TODO.md if applicable
-->

---

## Context Discipline

### Research → Decision → Implement (Two-Phase Pattern)

Complex tasks benefit from separating thinking from doing. When a task requires significant research, exploration, or decision-making:

**Phase 1 — Research (separate session or early in session):**
- Explore options, read code, identify tradeoffs
- Output a concrete decision to a file (e.g., `DECISION.md` or task-specific notes)
- Be specific: "Use JWT + bcrypt-12 + 7-day refresh + HttpOnly cookies" not "implement auth"

**Phase 2 — Implement (fresh context, decision only):**
- Start from the decision file + only relevant source files
- No re-exploring, no second-guessing — just execute the plan

This prevents the #1 agent performance killer: context bloat from mixing research and implementation in one giant session.

### Task Contracts (Explicit Done Conditions)

Before starting complex work, define what "done" looks like. Create a contract file or state it explicitly:

```markdown
## Done when:
- [ ] All existing tests pass
- [ ] New endpoint returns 200 for valid input, 401 for missing token
- [ ] No new TypeScript errors (`npx tsc --noEmit`)
- [ ] Error messages include HTTP status + actionable fix suggestion
```

You may NOT consider a task complete until every condition is verifiably satisfied. If a condition can't be met, explain why and ask for revised acceptance criteria.

See `.claude/skills/adversarial-review.md` for a structured verification pattern.

### Neutral Phrasing for Accurate Analysis

When asking Claude to analyze code, use neutral language to avoid sycophantic confirmation bias:

```
BAD:  "Is there a bug in the auth flow?"         → biases toward finding one
BAD:  "The auth flow looks correct, right?"       → biases toward confirming

GOOD: "Trace the logic of each component in the auth flow and report your
       observations. Do not assume anything is broken unless you can prove it."
```

---

## Scaling Up — When This File Gets Too Long

As your project grows, this CLAUDE.md will accumulate project-specific patterns, traps, and standards. When it exceeds ~300 lines, restructure it into a **router** that conditionally loads separate files:

```markdown
# CLAUDE.md — entry point / router — always read first

Before you do ANYTHING in this codebase, read this file completely.

## Universal rules (always apply)
→ Read docs/RULES_universal.md

## Conditional routing
- If you are writing or changing code       → read docs/RULES_coding.md
- If you are writing tests                  → read docs/RULES_testing.md
- If tests are failing                      → read docs/RULES_debugging.md
- If the task involves frontend / UI        → read docs/SKILLS_ui-patterns.md
- If unsure about anything                  → STOP and ask for clarification
```

**Rules** = preferences and prohibitions (what to do / not do)
**Skills** = battle-tested recipes for recurring problems (how to do it)

The goal: Claude reads only what's relevant to the current task, not the entire project history on every turn.

---

## Before Submitting Changes

1. Did I test the happy path?
2. Did I search for similar patterns to fix? (Coding Standard #5)
3. Did I remove dead code? No commented-out code, no unused variables.
4. Did I check git history for regressions?
5. Is this simpler than what was there before? (If not, justify why complexity is necessary.)
6. If I added a cross-file contract, is there a single source of truth? (Standard #6)
7. If I touched a boundary that exists in two places, did I update BOTH sides? (Standard #9)
8. Did I stay within scope? No unasked-for refactoring, no bonus features. (Trap #5)
9. Are tests still passing?

---

## Session Continuity

When starting a session, look for `SESSION_NOTES.md` in the project root. If it exists, a previous session left continuity notes. Reference them to pick up where the last session left off.

When ending a session (or if the user is wrapping up), update SESSION_NOTES.md:

```markdown
# Session Notes — [date]
## What we worked on
- [brief description]
## Current state
- [what's done, what's in progress]
## Next steps
- [what the next session should pick up]
## Key decisions made
- [any architectural or design decisions]
```

This is the AI equivalent of a sticky note on the monitor. Simple. Effective.
