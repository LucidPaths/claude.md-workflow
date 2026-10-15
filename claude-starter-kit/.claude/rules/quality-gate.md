# Quality Gate — Before Submitting Changes
#
# This gate exists because broken code has been shipped and marked "DONE"
# without verification. These rules are non-negotiable.
#
# Loaded automatically by Claude Code. Apply to every project.

## Core Checks (apply to the changed behavior)

1. **Test the production path.** Tests must exercise the actual code flow, not a synthetic setup.
2. **Trace the full data flow.** If A triggers B triggers C, verify A→C end-to-end.
3. **Select checks by risk.** Run focused regressions and affected boundary checks; run the full suite for broad impact or a repository release requirement. Preserve relevant evidence for unchanged behavior. Removing obsolete tests can be correct; test-count growth is not a quality invariant.
4. **Grep for the pattern.** Every new pattern gets a codebase-wide search (Coding Standard #4).
5. **Check the Principle Lattice.** Score your changes against all 5 principles in `docs/PRINCIPLE_LATTICE.md`. This is not decorative — enforce it actively on every change, or the principles become wallpaper. Ask yourself each one explicitly: Modular? Simple? Errors visible? Pattern fixed everywhere? Secrets safe?
6. **No dead code.** If you added a function, something must call it (Coding Standard #3).
7. **Check for regressions.** `git diff` and verify you didn't break existing contracts.
8. **Stay in scope.** No unasked-for refactoring, no bonus features (Trap #1).

## Verification Language Rule

**Unverified claims are lies, not estimates.** No completion claims without fresh verification evidence.

```
BEFORE claiming any status:
1. IDENTIFY — What command proves this claim?
2. RUN — Execute against the candidate being claimed; rerun evidence invalidated by edits
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

## Evidence relevance

Trust evidence according to the claim it can falsify, the target exercised, and its failure
controls—not whether it is automated. A passing mock cannot establish installed-host behavior;
a source trace supports an inference, not an execution claim. Exercise the real entry point
when runtime compatibility is part of the deliverable. Report what remains untested.

Use independent review when consequence or unfamiliar complexity makes fresh judgment useful,
or when the user/repository requires it. Review the exact candidate, stop concurrent writers,
and re-review affected changes after any material edit. A trivial wording edit does not require
an adversarial-review ceremony.

## Conditional Checks

9. Cross-file contract added? → Single source of truth or cross-ref in BOTH files (Coding Standard #5)
10. Touched a boundary in two places? → Updated both sides (Coding Standard #8)
11. Added a public function? → Something calls it and it's documented
12. Spawned a process? → Cleanup on exit
