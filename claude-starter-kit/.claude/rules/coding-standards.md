# Coding Standards — Universal Rules
#
# Each rule exists because a real bug prompted it. Follow them exactly.
#
# Loaded automatically by Claude Code. Apply to every project.

### 1. Simplicity First

Prefer the simpler approach that already works. Three clear lines beat one clever abstraction. Don't create helpers for one-time operations. If something worked before, check git history before rewriting it.

### 2. Actionable Errors

Every error must say what happened, why, and what the user can do about it. `"Something went wrong"` is itself a bug.

### 3. No Dead Code

If you replace a function, remove the old one. No commented-out code, no unused imports, no `_`-prefixed variables that nothing references. If you add a function, something must call it.

### 4. Fix the Cause, Then Every Instance

Name the mechanism that produced the bug in one sentence (commit message or task record); a sentence that only restates the symptom means the cause is not found yet. Find its siblings by meaning, not only by text (callers, the same type or contract, the same check in another layer, other branches and clients), and fix them all in the same change; "fix none" is never the answer. When the same defect sits in 2 or more places or comes back, make the class impossible (one source of truth, a type, a parser at the boundary, a lint or compile error): sweep the existing instances first, then turn the guard on, as Google does before it enables a new check ("we first need to clean up all instances of that problem in the codebase"). An instance you may not change gets a record (path, owner, the check that finds it), and the class stays open until it is fixed. This applies to security lists, validation, naming — everything.

### 5. Single Source of Truth for Cross-File Contracts

If two files must agree on a string, format, or list — there must be one authoritative definition that both reference. Never rely on comments like "must match foo.ts." When you discover a contract, follow this process:

1. **Try to make it a single file** (best — one builder + one parser in the same module)
2. **If cross-language prevents that**, add explicit cross-reference comments in BOTH files
3. **Add the contract** to the contracts table in CLAUDE.md
4. **If security-sensitive**, add a test asserting both sides match

### 6. User-Agent on External APIs

External services block requests without proper User-Agent headers. Always set one.

### 7. Closed By Default

Empty allowlists mean "deny all", not "allow all." This applies to permissions, feature flags, API access — anything where the safe default is "no."

### 8. Both Sides of the Boundary

When logic exists in two places (client + server, two languages, two config files), update both or update neither. One-sided updates create a false sense of safety worse than no update at all.
