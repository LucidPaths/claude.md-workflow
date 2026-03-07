# Principle Lattice

**Decision framework for software that doesn't rot.**

---

## What This Is

These are axiomatic principles — non-negotiable values that guide every design decision, every line of code, every architectural choice. They aren't features. They aren't goals. They're the DNA.

When you're stuck on a decision, check it against the lattice. If a choice violates a principle, it's wrong — even if it "works." If it honors multiple principles simultaneously, it's probably right.

Each principle has **instantiations** — concrete proof that the principle lives in the codebase, not just on paper. A principle without instantiations is a wish. We don't do wishes.

---

## The Five Principles

### 1. Modularity

> *Lego blocks, not monoliths.*

Every component should be self-contained. Pull one out — that specific thing stops working. The rest stands. No module should be load-bearing for something unrelated to its purpose.

When two systems need to talk, build a bridge — don't duplicate. If data already lives somewhere, reference it. Don't maintain two copies of anything.

**Instantiations:**
<!-- [ADAPT] Add concrete examples as your project grows. Examples:
     - "API routes are independent — auth failing doesn't break health checks"
     - "Components use props, not global state — any component is replaceable"
     - "Shared types live in types.ts — single source of truth"
-->
*None yet — add concrete examples as the project grows.*

**Demands:**
- Each component fails independently — one breaking doesn't cascade
- No hidden coupling between unrelated modules
- Shared types and interfaces live in a single location
- Modules own their own state — they call APIs directly instead of threading state through a central orchestrator
- Plugin/extension points where future growth is expected

---

### 2. Simplicity Wins

> *Don't reinvent the wheel. Code exists to be used.*

The best code is code someone else already debugged. Use battle-tested libraries. If something already works — in your own git history, in someone else's MIT repo, in a standard library — use it. Only write novel code for novel problems.

Complexity is a cost, not a feature. Three clear lines beat one clever abstraction. A working simple solution beats an elegant broken one. Always.

**Instantiations:**
<!-- [ADAPT] Add examples of simplicity wins. Examples:
     - "Using Zod for validation instead of hand-rolled checks"
     - "localStorage for settings (not a custom database)"
     - "Standard fetch() instead of a custom HTTP wrapper"
-->
*None yet — add concrete examples as the project grows.*

**Demands:**
- Before writing a new system, search for existing solutions first
- Before rewriting a function, check git history — maybe the old version worked
- If a dependency does 80% of the job, use it and handle the 20%
- Don't create abstractions for one-time operations

---

### 3. Errors Are Answers

> *Every failure teaches. Errors must be actionable.*

An error message that says "something went wrong" is itself a bug. Every error must say what happened, why, and what the user can do about it. Logs aren't optional — they're the program's memory of its own behavior.

**Instantiations:**
<!-- [ADAPT] Add examples. Examples:
     - "API errors include HTTP status + response body + suggested fix"
     - "Build failures show the exact file and line"
     - "Startup checks verify all required env vars before proceeding"
-->
*None yet — add concrete examples as the project grows.*

**Demands:**
- Every error message is actionable (says what to do, not just what happened)
- Logs exist at key lifecycle events (startup, shutdown, errors, state changes)
- No silent failures — if something goes wrong, someone (user or developer) knows
- Maintain an honest status table in CLAUDE.md (Working / PARTIAL / MISSING / BROKEN) — never pretend something works when it doesn't

---

### 4. Fix The Pattern, Not The Instance

> *Cure the root cause. Don't treat symptoms.*

When you find a bug, the bug is never alone. The same mistake that caused it exists in 3-5 other places — you just haven't hit them yet. Search for the pattern. Fix every instance. If you only fix the one you found, you're treating symptoms while the disease spreads.

This applies to architecture too. If a design keeps producing the same class of bug, the design is wrong — not the individual bugs.

**Instantiations:**
<!-- [ADAPT] Add examples. Examples:
     - "Found missing null check — grepped for all `.property` accesses, fixed 4 more"
     - "Same validation bug in 3 endpoints — extracted shared validator"
-->
*None yet — add concrete examples as the project grows.*

**Demands:**
- Every bug fix includes a search for the same pattern across the codebase
- If a pattern produces bugs twice, add it to CLAUDE.md as a Trap so it never happens again
- Root cause analysis before fix — the error might be downstream of the real bug
- When you discover a cross-file contract (same string/format in two files), add it to the contracts table in CLAUDE.md

---

### 5. Secrets Stay Secret

> *Nothing left open to exploitation.*

API keys are not config — they're secrets. They belong in environment variables or encrypted storage, never in localStorage, never in plaintext, never logged, never in error messages. Security is not a feature you add later. It's a property of every line of code.

**Instantiations:**
<!-- [ADAPT] Add examples. Examples:
     - "API keys in .env, never committed (in .gitignore)"
     - "Error messages never include credentials or tokens"
     - "HTTPS enforced for all external API calls"
-->
*None yet — add concrete examples as the project grows.*

**Demands:**
- **Closed by default** — empty allowlists mean "deny all", not "allow all." Permissions, access lists, feature flags: the safe default is always "no"
- Audit any new storage mechanism for secret leakage
- Never log API keys, tokens, or credentials (even in debug mode)
- Environment variables for secrets, never committed to git
- `.env` files in `.gitignore` from day one
- When security logic exists in two layers (client + server), both MUST be updated together — one-sided updates are worse than none

---

## Using The Lattice

### For Design Decisions

When stuck between two approaches, score them against the principles:

| Approach A | Approach B |
|-----------|-----------|
| Violates #1 (couples two modules) | Honors #1 (clean separation) |
| Honors #2 (simpler) | Violates #2 (complex) |
| **Mixed — needs thought** | **Mixed — needs thought** |

If one approach cleanly honors more principles without violating any, it wins. If both violate something, find a third approach.

### For Code Review

Every PR can be checked: *does this change violate any principle?* Not "is this code clean" — that's subjective. "Does this violate the lattice" — that's answerable.

### For New Sessions

Read this document first. If Claude understands these 5 principles, it understands how this project thinks. The codebase is the implementation; the lattice is the intent.

---

*Lattice concept adapted from [vincitamore/claude-org-template](https://github.com/vincitamore/claude-org-template). Principles distilled from the [HIVE](https://github.com/LucidPaths/HiveMind) project.*
