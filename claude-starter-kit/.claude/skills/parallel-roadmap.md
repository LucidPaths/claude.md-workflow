# /parallel-roadmap — Fan Out Roadmap Items to Isolated Agents

Map N independent roadmap items across isolated agents; reduce in an
orchestrator pass. Shared rules — not shared context — keep the outputs
architecturally compatible. This is the pattern the v1 README described as
"agentic MapReduce"; this skill is the implementation.

## Preconditions (check before fanning out)

- The items are genuinely independent: no shared files, or a clean partition
  of who owns what. Overlapping items go sequential, not parallel.
- Each item's acceptance criteria can be stated up front.
- `ROADMAP.md` or `TODO.md` exists, or the user names the items explicitly.

## Steps

### 1. Contract each item
For every item, write a task contract from `templates/TASK_CONTRACT.md`:
objective, checkable acceptance criteria, protected files, scope boundaries.
Protected-files lists of concurrent items must not overlap — if they do, the
partition is wrong; fix it before spawning anything.

### 2. Map
Spawn one agent per item with **worktree isolation** (each works on its own
copy — no cross-contamination of working trees). The agent's prompt is its
task contract verbatim, plus two standing orders:
- run `/verify` and report evidence before finishing
- touch nothing outside the contract's scope

Agents never communicate with each other. The contract and the shared rules in
`.claude/rules/core.md` are the entire coordination mechanism.

### 3. Reduce (orchestrator — you)
For each returned branch/diff:
1. Run `/adversarial-review` on the diff
2. Check the CLAUDE.md cross-file contracts table for drift across items —
   this is the one failure mode no single agent can see
3. Merge sequentially, re-running `/verify` after **each** merge, not just the
   last one

### 4. Handle failures
Anything failing review or verify goes back to a **fresh** agent with the
failure evidence appended to its contract. Do not patch it yourself in the
orchestrator context — the orchestrator that starts fixing leaf work stops
being able to judge it.

## Rules

- Contracts, not conversation: if two agents need to talk, the partition is wrong.
- The orchestrator merges; agents never push to the integration branch.
- Scale honestly: 2-3 items is usually the sweet spot. Ten parallel agents on
  a tangled codebase produces ten merge conflicts, not ten features.
