# Principle Lattice

**Five axioms. Every design decision checks against them.**

When stuck between two approaches, score them against the lattice. If one cleanly honors more principles without violating any, it wins. If both violate something, find a third approach.

---

## 1. Modularity

> *Lego blocks, not monoliths.*

Every component should be self-contained. Pull one out — that thing stops working, the rest stands. When two systems need to talk, build a bridge — don't duplicate. If data already lives somewhere, reference it.

**The test:** Can you remove this component without breaking something unrelated?

**Instantiations:**
<!-- [ADAPT] Add concrete examples as your project grows. Examples:
     - "API routes are independent — auth failing doesn't break health checks"
     - "Components use props, not global state — any component is replaceable"
-->
*None yet — add concrete examples as the project grows.*

---

## 2. Simplicity Wins

> *Don't reinvent the wheel. Code exists to be used.*

The best code is code someone else already debugged. Complexity is a cost, not a feature. Three clear lines beat one clever abstraction. A working simple solution beats an elegant broken one.

**The test:** Is there a simpler approach that already works? Would three explicit lines beat this abstraction?

**Instantiations:**
<!-- [ADAPT] Add examples. Examples:
     - "Using Zod for validation instead of hand-rolled checks"
     - "localStorage for settings (not a custom database)"
-->
*None yet — add concrete examples as the project grows.*

---

## 3. Errors Are Answers

> *Every failure teaches. Errors must be actionable.*

An error that says "something went wrong" is itself a bug. Every error says what happened, why, and what to do. No silent failures — if something goes wrong, someone knows.

**The test:** If this operation fails, would the developer (or user) know what happened and what to do?

**Instantiations:**
<!-- [ADAPT] Add examples. Examples:
     - "API errors include HTTP status + response body + suggested fix"
     - "Startup checks verify all required env vars before proceeding"
-->
*None yet — add concrete examples as the project grows.*

---

## 4. Fix The Pattern

> *Cure the root cause. Don't treat symptoms.*

When you find a bug, the bug is never alone. The same mistake exists in 3-5 other places. Search for the pattern, fix every instance. If a design keeps producing the same class of bug, the design is wrong — not the individual bugs.

**The test:** Did you grep for the same mistake elsewhere? Did you fix all instances?

**Instantiations:**
<!-- [ADAPT] Add examples. Examples:
     - "Found missing null check — grepped all `.property` accesses, fixed 4 more"
     - "Same validation bug in 3 endpoints — extracted shared validator"
-->
*None yet — add concrete examples as the project grows.*

---

## 5. Secrets Stay Secret

> *Nothing left open to exploitation.*

API keys belong in environment variables or encrypted storage — never in localStorage, never in plaintext, never logged, never in error messages. Security is not a feature you add later. It's a property of every line of code.

**The test:** Could a log message, error output, or config file leak something sensitive?

**Instantiations:**
<!-- [ADAPT] Add examples. Examples:
     - "API keys in .env, never committed (in .gitignore)"
     - "Error messages never include credentials or tokens"
-->
*None yet — add concrete examples as the project grows.*

---

## Using The Lattice

### For Decisions

| Approach A | Approach B |
|-----------|-----------|
| Violates #1 (couples two modules) | Honors #1 (clean separation) |
| Honors #2 (simpler) | Violates #2 (complex) |
| **Mixed — find a third option** | **Mixed — find a third option** |

### For Code Review

Every PR: *does this change violate any principle?* Not "is this code clean" (subjective) — "does this violate the lattice" (answerable).

### For Active Enforcement

The lattice only works if you check it actively. On every change, ask each principle explicitly: Modular? Simple? Errors visible? Pattern fixed everywhere? Secrets safe? If you treat it as a checkbox to skim past, it becomes wallpaper. If you treat it as a real constraint, it catches real bugs.

---

*Lattice concept adapted from [vincitamore/claude-org-template](https://github.com/vincitamore/claude-org-template). Principles distilled from the [HIVE](https://github.com/LucidPaths/HiveMind) project.*
