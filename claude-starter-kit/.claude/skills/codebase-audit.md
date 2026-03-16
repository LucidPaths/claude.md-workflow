# /codebase-audit — Systematic Codebase Health Check

Methodical audit that catches the bugs that accumulate silently in every codebase.

## Instructions

When this skill is invoked, run a systematic audit of the codebase (or specified area). This isn't a code review — it's a health check against known failure patterns.

### Phase 1: Discovery (Read Before Writing)

1. **Map the codebase** — understand the structure before judging it
2. **Identify key files** — entry points, config, shared types, security boundaries
3. **Read CLAUDE.md** — understand existing standards and known contracts

### Phase 2: Pattern Scan

Search for these categories of issues. For each, grep the relevant pattern across the entire codebase:

#### Category A: Silent Failures
```
- Swallowed errors (catch blocks that do nothing, let _ =, .catch(() => {}))
- Missing error handling on async operations
- Empty catch blocks or generic "something went wrong" messages
- Operations that silently return defaults on failure
```

#### Category B: Dead Code & Drift
```
- Exported functions/types that nothing imports
- Config values that nothing reads
- TODO/FIXME/HACK comments (are they still relevant?)
- Commented-out code (should be deleted or restored)
- Unused dependencies in package.json / Cargo.toml / etc.
```

#### Category C: Cross-File Contracts
```
- Same string/constant defined in multiple files (format drift risk)
- Enum/type that exists in two languages (e.g., TypeScript + Rust/Python/Go)
- Validation logic duplicated client + server side
- Hard-coded values that should be shared constants
```

#### Category D: Security Surface
```
- Secrets in code or config files (API keys, tokens, passwords)
- Missing input validation at system boundaries
- User-supplied paths without sanitization
- Empty allowlists that mean "allow all" (inverted security)
- HTTP where HTTPS should be used
- Missing User-Agent on external API calls
```

#### Category E: Code Quality
```
- Functions over 100 lines (candidates for decomposition)
- Deeply nested conditionals (3+ levels)
- Inconsistent naming conventions
- Missing error types (string errors instead of proper error types)
- Magic numbers without named constants
```

### Phase 3: Report

Output findings in this format:

```markdown
# Codebase Audit — [date]

## Summary
- X findings across Y files
- Critical: N | High: N | Medium: N | Low: N

## Critical Findings
[Issues that will cause bugs or security problems if not fixed]

### Finding 1: [title]
- **File:** path/to/file:line
- **Category:** [A-E]
- **Severity:** Critical
- **Issue:** What's wrong
- **Fix:** What to do
- **Pattern search:** Did you grep for this pattern elsewhere? Results?

## High Findings
[Same format]

## Medium Findings
[Same format]

## Recommendations
[Patterns to add to CLAUDE.md, traps to document, contracts to track]
```

### Phase 4: Fix or Track

For each finding:
1. **Critical/High** — fix immediately or create a clear tracking issue
2. **Medium** — add to CLAUDE.md as a pattern to watch
3. **Low** — mention in the report, fix if trivial

After fixing, grep for the same pattern to ensure ALL instances are caught (Principle 4: Fix The Pattern).

### Usage

```
/codebase-audit                    # Full codebase audit
/codebase-audit src/auth/          # Audit specific directory
/codebase-audit --category security  # Focus on security patterns only
```

### What Makes This Different From Code Review

Code review checks "is this change correct?" This audit checks "has the codebase drifted?" — it catches the slow accumulation of dead code, swallowed errors, contract drift, and security gaps that no individual PR introduces but every codebase develops over time.
