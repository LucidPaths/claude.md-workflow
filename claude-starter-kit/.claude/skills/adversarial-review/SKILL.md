---
name: adversarial-review
description: Three-pass adversarial verification that finds real bugs in a change before merge — an overclaiming bug-hunt, an overclaiming disproof, then adjudication. Use when the user runs /adversarial-review or asks to adversarially review, stress-test, or prove the correctness of a diff, function, smart contract, or PR before merging. Mandatory before merging smart-contract / fund-release changes.
---

# Adversarial Review — Three-Pass Verification

Exploit sycophancy bias against itself to find *real* bugs. Models find what they think you want, so run two opposing passes that each overclaim in opposite directions, then adjudicate. The intersection of "Bug Hunter couldn't miss it" and "Disprover couldn't kill it" is remarkably accurate.

## Before you start — ground the review

Do this first, every time. Skipping it is how reviews miss the obvious.

1. **Read the actual code.** Pull the real `git diff`, open the changed files, read the function signatures and callers. Never review from memory, from the PR description, or from how similar code "usually" looks.
2. **Define "correct" for *this* change.** State the concrete success conditions and the invariants it must not break — not generic ones. (e.g. "90/10 split stays exact," "no state transition skips Verified," "no revert path leaves funds locked.")
3. **List the high-risk surfaces it touches:** money / fund release, access control, state machines, external calls & reentrancy, integer math / overflow, error and revert paths, concurrency, auth flows, anything recently refactored.

## Pass 1: Bug Hunter (overclaim bias)

Adopt an aggressive bug-finding stance. Be exhaustive — cast the widest net you can; over-reporting here is the point, Pass 2 will prune it. Report every potential issue with:
- **File and line**
- **Severity** (low / medium / critical)
- **What could go wrong**
- **Proof** — a concrete scenario or input that triggers it. No proof, no entry.

## Pass 2: Adversarial Disprover (underclaim bias)

Switch roles. For each Pass-1 issue, try to **disprove** it:
- Is it actually handled elsewhere (guard, modifier, earlier check)?
- Is the scenario unreachable given the code's real constraints?
- Does a framework / library / compiler guarantee already prevent it?

Be skeptical but honest: only disprove what you can actually disprove, with a citation to the specific code that handles it. Bias toward caution — wrongly dismissing a real bug is far more expensive than carrying a false positive into Pass 3, so when you can't cleanly kill an issue, let it survive to the verdict.

## Pass 3: Final Verdict

| Issue | Bug Hunter said | Disprover said | Verdict |
|-------|-----------------|----------------|---------|
| #1 | Critical: X | Disproved: line N handles it | **False positive** |
| #2 | Critical: Y | Could not disprove | **Confirmed** |

Then output a clean report of **confirmed issues only**, ranked by severity. For each confirmed issue give the concrete triggering input and the minimal fix.

Run this final pass **as the person who inherits the code and gets paged when it breaks at 3am** — not as its author. The author wants it to be done; the inheritor wants it to be right.

Separate the three categories explicitly and keep them separate in the report:
- **Verified** — you traced it in the actual code and can point to the line.
- **Inferred** — follows from premises you've stated, but you didn't run it.
- **Assumed** — depends on something unverified; flag it as a residual risk.

## Done when

The defined success conditions are demonstrably met — every confirmed issue has a concrete triggering input and a fix, and every "disproved" issue cites the code that handles it. Stop when you can *show* it's right, not when it looks finished.
