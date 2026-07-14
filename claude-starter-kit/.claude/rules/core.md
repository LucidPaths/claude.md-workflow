# Core Rules

Every line here earns its context cost by changing behavior on a real,
recurring failure. If a rule stops doing that, delete it.

## Standards

1. **Simplicity first.** Prefer the approach that already works. Three clear
   lines beat one clever abstraction. Before rewriting anything, check git
   history — a past version may have worked.
2. **Actionable errors.** Every error says what happened, why, and what to do
   next. "Something went wrong" is itself a bug. No swallowed errors
   (`catch {}`, `let _ =`) on any path that matters.
3. **No dead code.** Replace a function → delete the old one. Add a function →
   something must call it now, not "later".
4. **Fix the pattern, not the instance.** Found a bug? Grep for the same
   pattern across the codebase. Fix every instance or fix none — one fix
   creates false safety.
5. **One source of truth, both sides of the boundary.** If two files must agree
   (client + server, two languages, two configs), either merge to one
   authoritative definition or add cross-reference comments in BOTH files and
   record the pair in the CLAUDE.md contracts table. Updating one side is
   worse than updating neither.
6. **Closed by default.** An empty allowlist means "deny all", never "allow
   all". Applies to permissions, feature flags, API access. Related hygiene:
   set a User-Agent on external API calls; keep secrets out of logs, errors,
   and committed files.

## Traps

Documented failure modes. "Stop." is an interrupt: when you catch yourself
thinking the quoted phrase, halt and read the correction. Violating the letter
of a trap is violating its spirit.

### "While I'm here, I'll also..."
**Stop.** Scope creep is the #1 session killer. Do exactly what was asked.
If you see something worth improving, mention it — don't do it.

### "This should work now"
**Stop.** Run `/verify`. Every completion claim needs evidence from a command
executed *after* the change, *in this turn*. Forbidden without fresh evidence:
"should work", "looks correct", "I'm confident", "Done!".

### "I'll fix this one place"
**Stop.** The same mistake exists in 3-5 other places you haven't hit yet.
Grep for the pattern before claiming the fix (Standard 4).

### "Let me try one more fix"
**Stop.** Three failed attempts on the same issue means you're guessing, not
debugging. State what you tried, what failed, and ask for direction.

### "The user pushed back, so my answer must be wrong"
**Stop.** Re-verify against actual state (run the command, read the file)
before changing your answer. Agreeing your way out of a correct answer is as
bad as defending a wrong one — both are settled by evidence, not deference.

## Self-Check: Am I Rationalizing?

Constructing an argument for why a trap doesn't apply to your situation IS the
trap firing.

| If you're thinking... | You're actually doing... |
|---|---|
| "This is different because..." | It's not. Apply the trap. |
| "I'm not refactoring, I'm *improving*" | Scope creep with a label swap. |
| "Just one small cleanup..." | Scope creep unless it's in the task contract. |
| "I already know the answer" | Then proving it takes 5 seconds. |

## Principles (tiebreakers for design decisions)

**Modular** (pull one block out, the rest stands) · **Simple** (don't reinvent
wheels) · **Errors are answers** (every failure teaches, visibly) · **Fix the
pattern** (root cause, all instances) · **Secrets stay secret** (closed by
default, never logged).

When two approaches tie, the one honoring more principles without violating
any wins. When both violate something, find a third approach.
