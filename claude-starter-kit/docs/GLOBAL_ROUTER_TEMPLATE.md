# Global Harness — CLAUDE.md Router Template

> This is a **thin router** template for your top-level CLAUDE.md. Keep it under 150 lines.
> Detailed rules, standards, and traps live in the docs/ and skills/ files — loaded on demand.
> Copy this to your project root as `CLAUDE.md` and customize.

---

## Session Start Protocol

On first response each session:

1. Print status block: current branch, uncommitted file count, any blockers
2. Read `WORKING_STATE.md` for session continuity context
3. Load applicable role file from `docs/` if role-based workflow is used
4. Read coding standards and traps from CLAUDE.md (this file)
5. Proceed with the task

---

## Decision Priority

```
Correctness > Security > Performance > Maintainability > Elegance
Working Increment > Perfect Solution
Stated Intent > Inferred Intent
Existing Patterns > Novel Approaches
Understand > Delete > Refactor > Add
Minimal Scope > Comprehensive Scope
```

---

## Stuck Protocol

1. **Stop** the current approach
2. **State** what is known vs unknown
3. **Identify** the specific blocker
4. **Check git history** — maybe a past version worked
5. **Propose** a smaller step, or **ask** the user

Never retry a failed approach more than once without changing something.

---

## Scope Guard

Before every action: **"Was I asked to do this?"**
- Yes → do it
- No but blocking → minimum to unblock, explain why
- No and nice-to-have → mention it, do not do it

---

## Reference Documents (loaded on demand, NOT every turn)

| Document | When to Load | Path |
|----------|-------------|------|
| Principle lattice | Design decisions | `docs/PRINCIPLE_LATTICE.md` |
| Working state template | Creating WORKING_STATE.md | `docs/WORKING_STATE_TEMPLATE.md` |
| Task contract template | Starting complex work | `docs/TASK_CONTRACT_TEMPLATE.md` |
| Role template | Setting up role-based workflow | `docs/ROLE_TEMPLATE.md` |
| Structured reasoning | Complex decisions | `.claude/skills/structured-reasoning.md` |
| Adversarial review | Code review | `.claude/skills/adversarial-review.md` |
| Research then implement | Exploration tasks | `.claude/skills/research-then-implement.md` |
| Project status | Quick state check | `.claude/skills/project-status.md` |
| Codebase audit | Health check | `.claude/skills/codebase-audit.md` |

---

## Git Workflow

Sync with main before pushing: `git fetch origin && git merge origin/main --no-edit`
Never push without fetching. Commit messages: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`.

---

## Session Continuity

Maintain `WORKING_STATE.md` in the project root. Update after significant steps,
when corrected, when you learn something undocumented. Track uncommitted work.
Prune aggressively. Keep under 200 lines.
