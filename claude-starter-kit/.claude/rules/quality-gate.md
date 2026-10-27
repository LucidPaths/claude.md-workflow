# Quality Gate — Before Submitting Changes
#
# This gate exists because broken code has been shipped and marked "DONE"
# without verification. These rules are non-negotiable.
#
# Loaded automatically by Claude Code. Apply to every project.

## Core Checks (do ALL, in order)

1. **Test the production path.** Tests must exercise the actual code flow, not a synthetic setup.
2. **Trace the full data flow.** If A triggers B triggers C, verify A→C end-to-end.
3. **Run the full test suite once before submitting**; while working, the tests that import or name the changed files. The test count drops only with every removed or disabled test named in the PR with its reason; an unnamed drop fails the gate. Never delete, skip or loosen a failing test to get green; rerun it once on the base commit, and report a failure there as pre-existing.
4. **Find the siblings.** Every fix gets a codebase-wide search by meaning, not only by text (Coding Standard #4).
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

## Verification Hierarchy

When checking if something works, these are in order of trustworthiness:

```
1. A check shown to fail without the change and pass with it, both outputs quoted (highest)
2. The real entry point run on a concrete input, output observed (user-visible behaviour)
3. An automated test passes that exercises the changed path and was not edited in this task
4. Manual trace through the actual code path, with file:line
5. Reading the code and reasoning about it
6. "It looks correct to me", or any claim without quoted output (no evidence)
```

A check counts no higher than its weakest property: it reached the claim's target, it could fail,
and nobody edited it in the same task to make it pass. A passing test against the wrong target, an
empty population, a skipped or filtered run, or a test edited to pass is no result at all. For a
claim about an internal library, levels 2 and 3 are equal. Never stop at level 6; at minimum reach
level 4, and a bug fix or behaviour change reaches level 1 or 2. Why: a passing test is not proof —
29.6% of SWE-bench patches that passed the tests behaved differently from the developer's fix
("Are 'Solved Issues' in SWE-bench Really Solved Correctly?", 2025), and an agent with access to the
tests "may delete failing tests rather than fix the underlying bug" (ImpossibleBench, 2025).

Relocated here from the retired `structured-reasoning` skill. It ranks *evidence*;
the Verification Language Rule above governs *claims*. Use them together.

## Conditional Checks

9. Cross-file contract added? → Single source of truth or cross-ref in BOTH files (Coding Standard #5)
10. Touched a boundary in two places? → Updated both sides (Coding Standard #8)
11. Added a public function? → Something calls it and it's documented
12. Spawned a process? → Cleanup on exit
