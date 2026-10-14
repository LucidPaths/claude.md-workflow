---
name: pick-skills
description: Choose the skills a task needs before starting it — read every skill this session can invoke, match them to the task's phases, state the chain and why, then run it, or say plainly that none fits. Use when the user runs /pick-skills (optionally with a task), says "which skill fits", "use the right skills for this", or starts a broad task without naming a method. Not needed when the user already named the skill.
---

# Pick skills — the right discipline for the task, chosen on purpose

Skills only help when the right one fires. Automatic loading is a guess made from one sentence of description; this
skill makes the choice explicit: read what is available, judge it against the task, say what will run and why, then
run it.

## 1. Pin the task

- One sentence: what must exist or be true at the end. Without a task in the invocation, take the open request of the
  conversation; if that is ambiguous, ask once.
- Its phases: understand, plan, build, verify, review, ship, record. Most tasks touch two or three.
- Its stakes: reversible or not, data or money at risk, shared or public output, size.

## 2. Read the bench

- List every skill this session can invoke: the skill list the harness shows, plus the skill folders of the project
  and the user (`.claude/skills/*/SKILL.md`) and of installed plugins. Names and descriptions first.
- Open a `SKILL.md` in full only when its description leaves the fit undecided: two candidates for one job, or a
  description that does not say when to use it.
- Only what this session lists can be invoked. A skill remembered from elsewhere does not exist here until it is listed.

## 3. Choose

For each phase, at most one skill: the most specific one that covers it.

- Specific beats general; a project's skill beats a personal one for the same job.
- A skill whose machinery exceeds the task is not used (a team planning procedure for a one-line fix). Say so.
- Skills compose in phase order: plan, then build, then verify, then record. Two skills claiming the same job in the same
  phase are a conflict: pick one and name the reason.
- A phase no skill covers is a gap. Say it and do that phase with plain judgment; never stretch a near-miss skill over
  it.
- A skill that writes to shared systems (trackers, repositories, messages, bookings) runs only within what the user has
  authorised.

## 4. Say it, then run it

State the chain with the closing block below, then invoke the first skill and the next ones as the work reaches their
phase. If the user asked only which skill fits, stop after the block.

## Closing block (required)

```
TASK      <one sentence>
CHAIN     1. /<skill>  <phase>  <what it contributes to this task>
          2. ...
NOT USED  /<skill>  <why it looked relevant, and why it does not apply>
GAPS      <phases no skill covers, or "none">
```
