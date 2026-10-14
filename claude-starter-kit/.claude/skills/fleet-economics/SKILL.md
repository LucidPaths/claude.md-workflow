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
2. **Judgment is never economised.** Critics, the advisor, the planner and the orchestrator run on the strongest models
   available. The savings come from builders on fully specified work and from not re-running proof that already ran.
3. **The cheapest level that can prove the gap; everything wider once.** A check runs at a level because it proves
   something there. A wider run repeated per edit proves nothing new.
4. **Facts at run time.** Which models exist, what they cost and how they rank change faster than any skill. Discover
   them each job (§2.0); never route from memory. A model the user names is real, even when it is newer than your
   knowledge.
5. **Budget is shared.** A subscription or quota is still finite, and a fan-out draws on the same budget as the user's
   other running sessions. Probe a wide run with a limit first; stop on the first quota error.

---

## 1. Classify every slice

The planner classifies each step; the orchestrator confirms before dispatch. When signals disagree, take the higher
class, or split the slice so its mechanical part can go down a tier.

| Class | Signals (any one of a higher class wins) | Typical work |
|---|---|---|
| **Mechanical** | the brief fixes every edit; the guarding test is named in advance; no design choice is left; one module; no contract, schema, persistence, security or guardrail change | moving strings into a catalogue; adding declared parameters copied from a source definition; register or changelog rows; fixtures; doc updates; tests written from a given assertion list; enumerations, searches, verbatim quote extraction |
| **Standard** | bounded logic inside one module; reads an existing contract; the design is locked but edge cases and error paths need judgment | an adapter for a new endpoint; detecting what a dependency serves; a config-driven behaviour change; a new tool over an existing read |
| **Complex** | crosses modules; changes a contract or schema version, a guardrail, scope or permissions, persistence, or how components are wired together; open micro-decisions remain; or a wrong result would be silent because no existing test would notice | conversation state with verification; consolidating composition; a permission change; a data migration |

---

## 2. Roles and models

### 2.0 Know the bench

Before routing, list the models this harness can actually dispatch: the model options of the subagent or task tool,
the provider's model list, the user's configuration. Place each in a tier by the provider's own positioning (flagship,
balanced, fast) and by any current benchmark or price the user or provider documentation gives; when two are close,
take the stronger one for judgment roles. With only one or two models, collapse the tiers: the classes still decide
critic rounds and test levels, and the strongest available model still does all judging.

### 2.1 Who does what

| Role | Tier | Effort | Notes |
|---|---|---|---|
| Spec keeper and the user's interface (the main session): roadmap → items → steps → features, the ledger, step acceptance by script | the session's model | as set | never reads whole diffs; the only role that talks to the user |
| Orchestrator of a build and advisor | strongest | default | runs the loop per step, settles disputes by probe, advises on design |
| Planner | flagship | default | |
| Builder, mechanical | fast | highest | only with a self-contained brief and the guarding test named; at the highest effort the fast tier is still cheap, and it saves loop-backs |
| Builder, standard | balanced | default | |
| Builder, complex | flagship | default | |
| Critic, mechanical and standard slices | flagship | default | never below flagship: critique is judgment |
| Critic, complex slices and the plan | strongest, blind | default | reads requirements, the artifact and the code; never the orchestrator's notes |
| Reading workers (inventories) | fast for enumerations and verbatim quotes; balanced for judgment-heavy reading | | the manager spot-checks every load-bearing claim |

- **Effort** follows the user's settings where they gave any; otherwise the model's default, and highest for mechanical
  builders as above.
- **Critic rounds:** mechanical one round, diff and brief only; standard one round with probes; complex up to two. A
  further round only on a confirmed finding.
- **Escalate, do not repeat:** two failed rounds at one tier → re-dispatch the slice one tier up with the reports,
  instead of a third round. Rotate a long-lived manager after about three rounds: its context slows every turn and loses
  detail.

---

## 3. The verification ladder

### 3.1 Discover the levels, per repository, at plan time

Read the package scripts, Makefile or task runner, the CI configuration and the test folders; write the levels this
repository actually has, with their commands, into the job's protocol.

| Level | Meaning |
|---|---|
| **S** static | schema validation, type check, lint, reference checks |
| **U** unit | one unit, no I/O |
| **C** contract | a boundary (port, adapter, route, schema) with stand-ins for its neighbours |
| **N** system end-to-end with stand-ins | the running service through its real entry point, external systems replayed |
| **F** full suite | everything above, as the repository's own check command runs it |
| **CI** pipeline | runs on push; costs no model tokens |
| **B** browser or UI end-to-end | through the real host application |
| **M** live external | a real model or service: real cost, real variance |

Example (a Node service): S = `npm run validate`, `npm run typecheck`; U, C, N = `test/unit`, `test/contract`,
`test/e2e`, all inside `npm test`; F = `npm run check`; CI = the merge-request pipeline; B = a Playwright set through
the host app; M = opt-in live tests with a real key.

### 3.2 Change type → level

| Change | While working (builder) | Once per slice candidate | At the release candidate |
|---|---|---|---|
| Wording, catalogue string, docs | U (string or snapshot) + S | F once | nothing: never B or M for wording |
| Validation or verification rule | U per accepted form, each with a negative pin (the same form, not given, stays refused) | F once | M only if a prompt changed with it |
| Prompt (new prompt version) | U (assembly and version) + C with a stand-in model | F once | M: one small recorded sample |
| Adapter, external interface, detecting what a dependency serves | C with a recorded stand-in of the dependency | F once | live checks once, against the version that will run |
| Conversation or session flow, reply contract, anything a UI renders | C + N (multi-turn through the real entry point) | F once | B once after deploy, plus one manual check |
| Wiring, architecture rules, cross-module refactor | C + an architecture test | F once (wide blast radius) | nothing extra |
| Persistence, schema version | C + compatibility (an old record still reads) | F once | nothing extra |
| Security, scope, permissions | C with the refused paths as negative cases | F once | B if the UI exposes it |

### 3.3 Who runs what

- **Builder:** the narrow levels while working; F once on its clean committed head, with a log whose first line names
  that head; negative controls only on the test files that guard the fix.
- **Orchestrator, per slice:** the scripted gate only — the gap's programmatic proof, its negative control, commit
  identity, line endings, nothing pushed — plus the builder's F log for the exact head. Not F again.
- **Integration line:** F once after the last slice; CI at publication; B and M at the release candidate, only for the
  change types in 3.2 that call for them.
- **A skipped level is a decision, not an omission:** the plan names it ("B not run: wording only"), so the judge and the
  user can see it.

---

## 4. Token rules

- Briefs are self-contained; a worker reads only the sections of shared context its brief names.
- Test output is read as the counts line and the failing block; full logs go to files.
- Reports are a file plus a message of at most 150 words.
- Scripted gates run before any agent review; agents review what a script cannot judge.
- One shell per job; no poll loops or watchers; long jobs in the background with a completion notice.
- Fan-outs are probed with a limit before they run wide (principle 5).

---

## 5. Failure modes this prevents

| Seen | Rule |
|---|---|
| The full suite ran three times per slice: builder, manager, orchestrator | §3.3 |
| A manager ran ten review rounds and its context grew until every turn was slow and lossy | §2.1 escalation and rotation |
| A benchmark sweep emptied the shared budget of the user's running sessions | principle 5 |
| Browser end-to-end planned for a reworded string | §3.2, first row |
| Critics placed on a mid tier "to save tokens", missing what a stronger model would have refuted | §2.1: critics never below flagship |

---

## Closing block (required, in the plan or before the first dispatch)

```
BENCH     <models available, by tier>
LEVELS    <S/U/C/N/F/CI/B/M with this repository's commands>
SLICE     <name>  class <M|S|C>  builder <model, effort>  critic <model, rounds>  proof <levels while working / at RC>  not run <level: reason>
          ...
```
