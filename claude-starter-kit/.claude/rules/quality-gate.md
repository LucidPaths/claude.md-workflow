# Quality Gate — Before Submitting Changes
#
# This gate exists because broken code has been shipped and marked "DONE"
# without verification. These rules are non-negotiable.
#
# Loaded automatically by Claude Code. Apply to every project.

## Core Checks (do ALL, in order)

1. **Test the production path.** Tests must exercise the actual code flow, not a synthetic setup.
2. **Trace the full data flow.** If A triggers B triggers C, verify A→C end-to-end.
3. **Run the full test suite.** Test count must not decrease vs. previous runs.
4. **Grep for the pattern.** Every new pattern gets a codebase-wide search (Coding Standard #4).
5. **Check the Principle Lattice.** Score your changes against all 5 principles in `docs/PRINCIPLE_LATTICE.md`. This is not decorative — enforce it actively on every change, or the principles become wallpaper. Ask yourself each one explicitly: Modular? Simple? Errors visible? Pattern fixed everywhere? Secrets safe?
6. **No dead code.** If you added a function, something must call it (Coding Standard #3).
7. **Check for regressions.** `git diff` and verify you didn't break existing contracts.
8. **Stay in scope.** No unasked-for refactoring, no bonus features (Trap #4).

## Verification Language Rule

**Unverified claims are lies, not estimates.** No completion claims without fresh verification evidence.

```
BEFORE claiming any status:
1. IDENTIFY — What command proves this claim?
2. RUN — Execute the command (fresh, complete, in this response)
3. READ — Full output, check exit code, count failures
4. REPORT — State claim WITH the evidence: "Ran X → Y → [claim]"

Skip any step = the claim is unverified.
```

**Forbidden phrases** (if you catch yourself typing these, STOP and run the command):
- "Should work now" / "This should fix it"
- "Looks correct" / "Seems right"
- "Done!" / "Fixed!" / "All good!" (before verification)
- "I'm confident this works" (confidence ≠ evidence)
- "I believe this fixes it"

## Rationalization Patterns

Every shipped bug was preceded by a thought that felt reasonable. If you catch yourself thinking any of these, you are about to repeat history:

| Rationalization | Defense |
|---|---|
| "I tested it locally and it works" | Test the ACTUAL deployment/production path, not dev setup. |
| "`let _ =` / `catch {}` is fine here" | If the operation failing breaks the feature, handle the error. |
| "I'll wire up the caller later" | If nothing calls it NOW, it's dead code. Wire it or don't write it. |

## Conditional Checks

9. Cross-file contract added? → Single source of truth or cross-ref in BOTH files (Coding Standard #5)
10. Touched a boundary in two places? → Updated both sides (Coding Standard #8)
11. Added a public function? → Something calls it and it's documented
12. Spawned a process? → Cleanup on exit
