# Structured Reasoning - Quick Reference

## Operational Modes

| Mode | When | Focus |
|------|------|-------|
| **Architecture** | System design, planning | Boundaries, interfaces, not implementation |
| **Implementation** | Writing code | Clarity, correctness, minimal scope |
| **Diagnostic** | Debugging | Trace causation, don't guess, verify assumptions |
| **Review** | Code audit | Assume issues exist, check edge cases |
| **Refactoring** | Improving structure | Behavior preservation, test first |
| **Exploration** | Researching options | Breadth before depth, explicit tradeoffs |

## Priority Hierarchy

When concerns conflict, default order:

```
Correctness > Security > Performance > Maintainability > Elegance
Working Increment > Perfect Solution
Stated Intent > Inferred Intent > Assumed Intent
Existing Patterns > Novel Approaches (unless patterns are broken)
Minimal Scope > Comprehensive Scope (do what was asked, not what seems nice)
Delete > Refactor > Add (reduce complexity before adding it)
```

## Scope Guard

Before every action, ask: **"Was I asked to do this?"**

- If yes → do it
- If no but it's blocking the task → do the minimum to unblock, explain what you did and why
- If no and it's just "nice to have" → mention it, don't do it

Scope creep is the #1 session killer. A focused session that does one thing well beats a sprawling session that half-does three things.

## Boundary Audit

When touching code that enforces rules (validation, permissions, security, config):

1. **Grep** for the same constant/string/pattern in other files
2. If it exists in 2+ places → **update all of them**
3. If it's a new boundary → check if it should exist in multiple layers (client + server, frontend + backend)
4. Add to the cross-file contracts table in CLAUDE.md

One-sided updates are worse than no update — they create a false sense of safety.

## Stuck Protocol

1. Stop the current approach
2. State what's known vs. unknown
3. Identify the specific blocker
4. Check git history — maybe a past version worked
5. Propose a smaller verifiable step, or ask for help

**Never** brute-force through a blocker by retrying the same thing. If it failed twice, the approach is wrong.

## Decomposition Triggers

Break down the task when:
- 3+ files involved
- Sequential dependencies exist
- Unfamiliar code area
- Irreversible operations
- Can't confidently predict steps

## Escalation (Don't Decide Alone)

- Security implications
- Breaking API/data changes
- Architectural decisions
- Irreversible operations
- Ambiguous requirements (ask — don't guess)

## Commit Discipline

- **5+ modified files without a commit?** Stop and commit before continuing
- **Before risky operations** (refactoring, dependency upgrades): commit first
- **After each logical unit of work:** commit with a descriptive message
- **Track uncommitted work** in WORKING_STATE.md — the "20 fixes on disk unpushed" situation must never happen

## Verification Hierarchy

When checking if something works, these are in order of trustworthiness:

```
1. Automated test passes (highest confidence)
2. Manual trace through the actual code path
3. Running it and observing the output
4. Reading the code and reasoning about it
5. "It looks correct to me" (lowest — almost worthless)
```

Never stop at level 5. At minimum, reach level 2.

## Quick Checks

**Before starting:** Can I state the goal in one sentence? What does "done" look like? Am I about to do exactly what was asked, or am I adding scope?

**During:** Is this still aligned with the objective? Am I basing this on actual code or assumptions? Have I drifted from the original request? How many files have I changed without committing?

**Before completing:** Does this solve the stated problem? What should be verified? Did I stay within scope? Did I update both sides of any cross-file contracts? Is my working state file current?
