---
name: fleet-economics
description: Size every slice of multi-agent work to its risk — which available model builds it, which model critiques it, at which effort, and the cheapest test level that proves it — so full suites, end-to-end and live-service runs happen only where they prove something. The single source for model routing, critic tiers, the verification ladder and token rules that planning and build-loop skills apply. Use when planning or running work with subagents, when assigning models or critics to slices, when deciding how much testing a change needs ("do we need e2e for this?", "full suite again?"), when usage or token cost is the question, or when the user invokes /fleet-economics. Works with whatever models the harness offers and whatever test levels the repository has, both discovered at run time.
---

# Fleet economics — staff and prove each slice in proportion to its risk

Multi-agent work spends most of its budget in two places: strong models doing work a smaller one could finish, and the
same proof run again by every layer that touches a slice. This skill routes each slice by risk and runs each check at
the one level where it proves something.

---

## 0. Principles

1. **Cost per finished slice, not per request.** A cheap model that needs three loop-backs costs more than a stronger
   one that needs none. Route by risk, then look at the rounds each slice actually took.
2. **Review where the slice leaves something to judge; on the strongest tier when it runs.** A mechanical or prose-only
   slice gets no critic: its brief fixed every edit, and the scripted gate, the guarding test and its negative control
   prove it. A critic that runs, and the advisor, the planner and the orchestrator, run on the flagship tier or above,
   because a weaker critic misses what a stronger one refutes. The savings come from builders on fully specified work,
   from no critic where nothing was left to judge, and from not re-running proof that already ran.
3. **The cheapest level that can prove the gap; everything wider once.** A check runs at a level because it proves
   something there. A wider run repeated per edit proves nothing new.
4. **Facts at run time.** Which models exist, what they cost and how they rank change faster than any skill. Discover
   them each job (§2.0); never route from memory. A model the user names is real, even when it is newer than your
   knowledge.
5. **Budget is shared.** A subscription or quota is still finite, and a fan-out draws on the same budget as the user's
   other running sessions. A fan-out of more than `DEFAULT fanout_probe = 3` parallel agents starts as one probe agent
   with the same brief, and widens only after the probe finished without a quota error; stop on the first quota error.

---

## 1. Classify every slice

The planner classifies each step; the orchestrator confirms before dispatch. When signals disagree, take the higher
class, or split the slice so its mechanical part can go down a tier.

| Class | Signals (any one of a higher class wins) | Typical work |
|---|---|---|
| **Mechanical** | the brief fixes every edit; the guarding test is named in advance; no design choice is left; one module; no contract, schema, persistence, security or guardrail change | moving strings into a catalogue; adding declared parameters copied from a source definition; register or changelog rows; fixtures; doc updates; tests written from a given assertion list; enumerations, searches, verbatim quote extraction |
| **Standard** | logic inside one module; reads an existing contract; the design is locked but the brief leaves edge cases or error paths to the builder | an adapter for a new endpoint; detecting what a dependency serves; a config-driven behaviour change; a new tool over an existing read |
| **Complex** | crosses modules; changes a contract or schema version, a guardrail, scope or permissions, persistence, or how components are wired together; open micro-decisions remain; or a wrong result would be silent because no existing test would notice | conversation state with verification; consolidating composition; a permission change; a data migration |

**Prose-only** is a mark on top of the class, read from the diff: every changed file is documentation (`.md`, `.rst`,
`.txt`) or every changed hunk is a comment or a catalogue string. It decides the critic (§2.1) and the test level (§3.2).

---

## 2. Roles and models

### 2.0 Know the bench

Before routing, list the models this harness can actually dispatch: the model options of the subagent or task tool,
the provider's model list, the user's configuration. Place each in a tier by the provider's own positioning (flagship,
balanced, fast) and by any current benchmark or price the user or provider documentation gives. Two models in one tier:
judgment roles take the one the provider positions higher. Where no source orders the two, ASK: "Which of <A> and <B>
do you rank higher for review work?" → the named one takes the judgment roles; nobody to ask (a subagent, a scheduled
run) → route no judgment role yet and report the question, with both models' sources, to whoever dispatched you. With
only one or two models, collapse the tiers: the classes still decide critic rounds and test levels, and the strongest
available model still does all judging.

### 2.1 Who does what

| Role | Tier | Effort | Notes |
|---|---|---|---|
| Spec keeper and the user's interface (the main session): roadmap → items → steps → features, the ledger, step acceptance by script | the session's model | as set | never reads whole diffs; the only role that talks to the user |
| Orchestrator of a build and advisor | strongest | default | runs the loop per step, settles disputes by probe, advises on design |
| Planner | flagship | default | |
| Builder, mechanical | fast | highest | only with a self-contained brief and the guarding test named; at the highest effort the fast tier is still cheap, and it saves loop-backs |
| Builder, standard | balanced | default | |
| Builder, complex | flagship | default | |
| Critic, mechanical and prose-only slices | none | | the scripted gate, the guarding test and its negative control are the proof; a critic runs only when the user asks for one |
| Critic, standard slices | flagship | default | never below flagship: critique is judgment |
| Critic, complex slices and the plan | strongest, blind | default | reads requirements, the artifact and the code; never the orchestrator's notes |
| Reading workers (inventories) | a script first, wherever a regex or a parser can do the extraction; fast for extraction by an explicit rule (enumerations, verbatim quotes, reformatting); balanced for reading that classifies or judges | highest for fast | the manager spot-checks every load-bearing claim |

- **Effort** follows the user's settings where they gave any; otherwise the model's default, and highest for the fast
  tier as above.
- **The fast tier never classifies, judges or decides.** It extracts, enumerates and transforms by an explicit rule
  that its brief states (a term list, a pattern, a field map, a template); where a regex or a parser suffices, a script
  does the job instead. Every verdict (is this line a rule, is this a defect, which kind, which class) comes from the
  balanced tier or above. A fast-tier output that carries a verdict anyway is used for its extractions only, after the
  manager's spot-check.
- **Critic rounds:** mechanical and prose-only none, unless the user asks for one; standard one round with probes;
  complex up to two. A further round only on a confirmed finding.
- **Escalate, do not repeat:** two failed rounds at one tier → re-dispatch the slice one tier up with the reports,
  instead of a third round.
- **Agent lifetime.** Precondition: every agent writes its deliverable to files as it goes, so retiring it loses
  nothing. Retire an agent (manager, builder, critic, worker; the same rule binds the manager's own workers) as soon as
  one signal fires:

  | Signal | Reason |
  |---|---|
  | its reported token use reaches `DEFAULT retire_at = 60 %` of its context window, or the harness reports a context error | past that point every turn is slower and detail starts to drop |
  | it has delivered, and its next job is a new deliverable | a new job starts in a clean context, not in the residue of the last one |
  | its slice reached 3 review rounds and the third still has a confirmed finding | a fourth round in the same context repeats the third |
  | its report repeats a finding already closed, or omits an item that its brief's report format requires or that its previous report listed as open | that is detail being lost |

  Resume the same agent only for a bounded loop-back on its own deliverable: named findings, no new reading. A fresh
  agent gets a brief built only from durable files (the PRD, the report files, the branch and its head), never the old
  transcript.

---

## 3. The verification ladder

### 3.1 Discover the levels, per repository, at plan time

Read the package scripts, Makefile or task runner, the CI configuration and the test folders; write the levels this
repository actually has, with their commands, into the job's protocol.

| Level | Meaning |
|---|---|
| **S** static | schema validation, type check, lint, reference checks |
| **U** unit | one unit, no I/O |
| **A** affected | the test files that import or name a changed file (search the tests for its path or module name), plus S |
| **C** contract | a boundary (port, adapter, route, schema) with stand-ins for its neighbours |
| **N** system end-to-end with stand-ins | the running service through its real entry point, external systems replayed |
| **F** full suite | everything above, as the repository's own check command runs it |
| **CI** pipeline | runs on push; costs no model tokens |
| **B** browser or UI end-to-end | through the real host application |
| **M** live external | a real model or service: real cost, real variance |

Example (a Node service): S = `npm run validate`, `npm run typecheck`; U, C, N = `test/unit`, `test/contract`,
`test/e2e`, all inside `npm test`; A = the test files `grep -rl <module> test/` lists; F = `npm run check`; CI = the merge-request pipeline; B = a Playwright set through
the host app; M = opt-in live tests with a real key.

### 3.2 Change type → level

| Change | While working (builder) | Once per slice candidate | At the release candidate |
|---|---|---|---|
| Wording, catalogue string, docs | U (string or snapshot) + S | nothing further | nothing: never B or M for wording |
| Validation or verification rule | U per accepted form, each with a negative pin (the same form, not given, stays refused) | A once | M only if a prompt changed with it |
| Prompt (new prompt version) | U (assembly and version) + C with a stand-in model | A once | M: one recorded sample of `DEFAULT live_sample = 5` cases |
| Adapter, external interface, detecting what a dependency serves | C with a recorded stand-in of the dependency | A once | live checks once, against the version that will run |
| Conversation or session flow, reply contract, anything a UI renders | C + N (multi-turn through the real entry point) | A once | B once after deploy, plus one manual check |
| Wiring, architecture rules, cross-module refactor | C + an architecture test | F once (wide blast radius) | nothing extra |
| Persistence, schema version | C + compatibility (an old record still reads) | F once | nothing extra |
| Security, scope, permissions | C with the refused paths as negative cases | F once | B if the UI exposes it |

A slice classified complex (§1) runs F once per candidate whatever its row says. A repository rule that demands more
(its contributing file, its instructions file) overrides this table.

### 3.3 Who runs what

- **Builder:** the narrow levels while working; the candidate level of §3.2 (A, or F for a complex slice) once on its
  clean committed head, with a log whose first line names that head; negative controls only on the test files that
  guard the fix. In fleet mode the slice manager runs this candidate run on the builder's head instead, and the builder
  does not.
- **Orchestrator, per slice:** the scripted gate only — the gap's programmatic proof, its negative control, commit
  identity, line endings, nothing pushed — plus the one candidate log for the exact head. Not again.
- **Integration line:** F once after the last slice, before any pull request (a line of one slice whose candidate run
  was already F on the same head reuses that log); CI at publication; B and M at the release candidate, only for the
  change types in 3.2 that call for them.
- **A skipped level is a decision, not an omission:** the plan names it ("B not run: wording only"), so the judge and the
  user can see it.

---

## 4. Token rules

- Briefs are self-contained; a worker reads only the sections of shared context its brief names.
- Test output is read as the counts line and the failing block; full logs go to files.
- Reports are a file plus a message of at most 150 words.
- Scripted gates run before any agent review; agents review what a script cannot judge.
- One shell per job; no poll loops or watchers; installs, builds, full suites, end-to-end and browser runs go to the
  background with a completion notice.
- A fan-out above `fanout_probe` agents starts with one probe agent (principle 5).

---

## 5. Failure modes this prevents

| Seen | Rule |
|---|---|
| The full suite ran three times per slice: builder, manager, orchestrator | §3.3 |
| A manager ran ten review rounds and its context grew until every turn was slow and lossy | §2.1 escalation and agent lifetime |
| Fast-tier census workers were briefed to decide which lines were rules; every verdict would have had to be made again | §2.1: the fast tier never classifies, judges or decides |
| A benchmark sweep emptied the shared budget of the user's running sessions | principle 5 |
| Browser end-to-end planned for a reworded string | §3.2, first row |
| Critics placed on a mid tier "to save tokens", missing what a stronger model would have refuted | §2.1: a critic that runs is never below flagship |
| A rewrite of skill text was wrapped in census workers, batches, a new lint and a planned critic round; the user called it a circus | §2.1: no critic on prose-only or mechanical slices; §3.2: no full suite for wording |

---

## Closing block (required, in the plan or before the first dispatch)

```
BENCH     <models available, by tier>
LEVELS    <S/U/A/C/N/F/CI/B/M with this repository's commands>
SLICE     <name>  class <M|S|C> [prose-only]  builder <model, effort>  critic <model, rounds | none: mechanical or prose-only>  proof <levels while working / per candidate / at RC>  not run <level: reason>
          ...
```
