# /adversarial-review — Isolated Three-Stage Review

Independent, oppositely-biased perspectives triangulate real bugs. The v1
version of this skill ran all three passes in one context — which let pass 2
anchor on pass 1's reasoning, quietly defeating the purpose. The isolation is
now structural: later stages receive **claims only**, never earlier stages'
reasoning.

## Stage 1 — Finders (parallel, mutually blind)

Spawn 3 subagents **in parallel**, each given the same scope (files or diff)
and a different lens:

1. **Correctness** — logic errors, edge cases, off-by-ones, broken contracts
2. **Security & failure paths** — injection, authz gaps, swallowed errors, leaks
3. **Data flow & state** — races, stale state, one-sided boundary updates

Each finder returns findings as bare claims:
`file:line · severity (low/medium/critical) · one-sentence defect · concrete failure scenario (inputs/state → wrong outcome)`.

Finders never see each other's output. A finding without a concrete failure
scenario is not a finding.

## Stage 2 — Skeptics (per finding, claim-only)

Deduplicate findings by file+line first — otherwise rejected findings resurface.

For each surviving finding, spawn a skeptic subagent that receives **only** the
claim and access to the code — not the finder's reasoning. Its instruction:

> Try to refute this claim. Check whether the scenario is unreachable, handled
> elsewhere, or guaranteed impossible by a framework/library. Default to
> **refuted** if the failure scenario cannot actually occur as described.

For a thorough review, use 2-3 skeptics per finding with distinct angles
(reachability, existing handling, framework guarantees) and kill the finding on
majority refutation.

## Stage 3 — Adjudicate (you, in this context)

A finding survives only if the skeptic(s) failed to refute it. For each
survivor report: file:line, severity, the defect, the failure scenario, and the
skeptic's strongest failed refutation attempt (this is the evidence the bug is
real). Rank by severity. Report **only** survivors — a clean report with three
real bugs beats a padded report with twelve maybes.

## Rules

- **Never run all three stages in a single context.** The anchoring you'd
  introduce is exactly what this process exists to remove.
- Best on: auth flows, data pipelines, error paths, fresh refactors, PR diffs.
- After confirming any bug, grep for the same pattern codebase-wide
  (Standard 4) before reporting the fix scope.
