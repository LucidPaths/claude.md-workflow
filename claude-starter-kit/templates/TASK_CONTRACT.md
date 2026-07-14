# Task Contract — [Task Name]

> Copy this template for any non-trivial task — and for every agent spawned by
> `/parallel-roadmap`, where it is the agent's entire coordination mechanism.
> A task is not complete until every acceptance criterion is verifiably
> satisfied via `/verify`.

## Objective

<!-- One sentence: what does this task accomplish? -->

## Decision (if research was needed)

<!-- What approach was chosen and why? Be specific: "Use X library with Y
     config", not "implement the feature". -->

## Acceptance Criteria

<!-- Every item must be checkable by a command or observation — no subjective
     criteria like "code is clean". -->

- [ ] <!-- e.g., All existing tests pass (`npm test`) -->
- [ ] <!-- e.g., New endpoint returns 200 for valid input -->
- [ ] <!-- e.g., No new type errors (`npx tsc --noEmit`) -->

## Protected Files (do NOT modify)

<!-- Files that must not change. For hard enforcement, also list them in
     .claude/protected-paths.txt (see guards/install-guards.sh). -->

## Verification Steps

<!-- Concrete commands proving the criteria — what /verify will run. -->

1. <!-- e.g., `npm test` — all green, count not lower than baseline -->
2. <!-- e.g., `curl -X POST /api/login` — 200 with token -->

## Scope Boundaries

<!-- Explicitly OUT of scope. This is what prevents scope creep. -->
<!-- e.g., "Do NOT refactor existing auth middleware" -->
<!-- e.g., "Do NOT add new dependencies" -->
