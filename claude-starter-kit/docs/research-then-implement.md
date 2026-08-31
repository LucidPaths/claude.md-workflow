# /research-decide — Two-Phase Task Execution

Separate research from implementation to prevent context bloat.

## Instructions

When this skill is invoked (or when a task clearly requires significant research before coding), execute in two phases:

### Phase 1: Research & Decide

1. **Explore** the relevant code, docs, and options
2. **Identify** tradeoffs, constraints, and dependencies
3. **Decide** on a concrete approach — be specific:
   - Which libraries/patterns to use (with versions if relevant)
   - Which files to modify and how
   - Which files to NOT touch (scope boundaries)
   - What the acceptance criteria are
4. **Write** the decision to a file:
   ```
   DECISION_[task-name].md
   ```
   Use this structure:
   ```markdown
   # Decision: [Task Name]
   ## Context
   What problem are we solving? What constraints exist?
   ## Options Considered
   1. Option A — [pros] / [cons]
   2. Option B — [pros] / [cons]
   ## Decision
   Option [X] because [reason].
   ## Implementation Plan
   1. Modify file X to add Y
   2. Create file Z with W
   3. Update tests in T
   ## Acceptance Criteria
   - [ ] Criterion 1
   - [ ] Criterion 2
   ```
5. **Stop.** Present the decision to the user for approval before proceeding.

### Phase 2: Implement

1. **Read** only the decision file + the specific source files listed in it
2. **Do not** re-explore or second-guess — execute the plan
3. **Verify** each acceptance criterion as you go
4. **Report** completion against the criteria

### When to Use This Pattern

- Task requires exploring 5+ files to understand
- Multiple viable approaches exist
- Architectural decisions are involved
- User said "research this" or "figure out how to..."
- You find yourself reading code for more than 3-4 turns without writing any

### When to Skip

- Task is clearly defined ("add a null check to line 42")
- Single file change with obvious implementation
- User provided a specific implementation plan already
