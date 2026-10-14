---
name: blueprint
description: Rigorous team planning before a complex build or deliverable — intake of the user's rulings, a fact inventory by parallel workers (system, own code, neighbours' contracts, verbatim requirements), locked design principles, a full plan with gap ledger and per-step PRDs, then a review triad (advisor, blind critic, contract-and-tracker checker), revision rounds until the blind critic clears, a verified questions file for other owners, and the user's approval. Use when the user asks to plan, scope or design work that spans 3 or more steps, owners, contracts or tickets, says "plan this properly", "blueprint", "before we build", or invokes /blueprint; also as the plan phase of /goal-loop in fleet mode. Not for a change that stays inside one step, one owner, one contract and one ticket (just do it), and not for executing the build (that is /goal-loop). For work that spans exactly 2, ask the user "plan this as a team, or just do it?" and follow the answer (nobody to ask: report the question, and plan or build nothing yet).
---

# Blueprint — plan it as a team before anyone builds

Run before any build, this plan phase catches what a build would otherwise ship — a requirement the design violates (one
user could list another user's records), a request that crashes on an input shape nobody measured, identifiers counted as
figures, a test whose premise is false, a guardrail edit hidden inside a build step — and it works for any complex job:
software, migrations, infrastructure, proposals, deliverables for a client.

**Outputs:** three shared files (primer, protocol, one PRD per job), a fact inventory, a verbatim requirements extract,
a plan with a gap ledger and one PRD per step, three review files, the orchestrator's revision decisions, a verified
questions file for other owners, and the user's approval. The build follows in section 9.

---

## 0. Principles (each exists because its absence cost something)

1. **Facts before design, design before code, refutation before approval.** A plan reviewed only by its author is a
   wish list.
2. **The orchestrator decides; agents measure, draft and refute.** Design calls, finding verdicts and routing are never
   delegated. Measuring, drafting and refuting always are.
3. **The user's words are law, verbatim.** Rulings go into the primer word for word, with the time they were given.
   Paraphrase drifts; quotes do not.
4. **Blind review is the strongest review.** One critic never sees the orchestrator's reasoning, the primer or other
   reports: it judges the artifact against the requirements and the code.
5. **Nothing is decided silently and nothing is dropped.** Every open choice is surfaced with options and evidence; every
   finding gets a verdict and a destination.
6. **Never ask a person what a source already answers**, and never present a question to an owner that a source shows as
   answered.
7. **Local first.** Nothing is pushed, opened, created or booked in a shared system until the user approves the plan and,
   later, the build.
8. **Durable files, short messages, clock reads.** Every ruling, fact, decision, acceptance, measurement, finding and
   report lives in a file; agents send summaries of at most 150 words; every time written is a time read from the clock.

---

## 1. Intake (orchestrator, with the user)

The user explains; the orchestrator listens, reads the sources the user names, and then **explains back and stops**
("before we start working, we discuss"). No agent is dispatched before the user confirms the understanding.

Settle, and write down verbatim:
- **Goal and target**: what exists at the end, and by when ("a prototype heading towards X by the end of the week").
- **In and out**: what the user explicitly excludes ("no feature creep", "the export is not scope"), and what is
  somebody else's (another team's UI, a client's infrastructure).
- **Lane**: which ticket or work package every part books on (records its time and cost against), and where a part
  fits better on a card (another ticket) it cannot book on (note it, never book on another person's card). No lane,
  no work.
- **Owners**: who decides what (the user, the product owner, the client). Commercial, contractual and scope points are
  the user's; technical design is the orchestrator's within the user's rulings.
- **Constraints**: local only, which machine and disk, memory limits, which models for which roles, deadlines.
- **What must not happen**: writes into other people's documents, secrets in files, client names in outgoing artefacts.

Questions to the user only for what no source answers. Before asking, check: the tickets, the minutes, the repository,
the contract, the user's earlier words in this session.

---

## 2. The three shared files (written by the orchestrator)

Every agent reads them first, so a dispatch points to them instead of repeating their content in the orchestrator's
context.

### 2.1 Primer (`<date>-<job>-primer.md`) — shared context, never given to the blind critic
1. Who and what: people by role (and name if internal), the product, the repositories, the trackers.
2. The goal of this team, numbered, including the future it must not block ("later there will be sessions, multi-agent
   runs ... do not cement a door shut").
3. Out of scope, explicitly.
4. **The user's rulings, verbatim**, each with its time.
5. **Measured facts**, each with **who measured it, how and when** (a fact without its measurement is a premise). When an
   agent corrects one, the orchestrator corrects the primer at once and logs it.
6. Sources and access: paths, tools, how to read the tracker, what is **forbidden to read** (a transcript holding a
   secret, other sessions' credentials).

### 2.2 Protocol (`<date>-<job>-protocol.md`) — binding rules for every agent
1. Local-only list: no push, no merge request, no ticket, no status move, no time entry, no mail, no message to a person;
   reads allowed.
2. Machine guard: where worktrees, installs and logs go (the disk settled at intake); the free-memory floor (from the
   memory limits settled at intake); lock directories (`mkdir` is atomic) for every install, build, full-suite and
   end-to-end run, and how to release them in the same command; one shell per job; no watch loops.
3. Repository law: the repo's own rules files to read, commit identity, commit message form, line endings, language,
   no secrets, no customer data, stage by path, same-change documentation rules, contract versioning.
4. Proof rules: measured / read / inferred per claim; a negative control for every gap of the gap ledger (section 5,
   item 5); a checker shown to fire on a planted defect; `/paranoia` before every report by managers and critics.
   Standalone default: before reporting, one pass per defect class over everything the agent wrote (every number
   re-derived from its source, contradictions between the files, instructions that name no path), each find fixed,
   repeated until a pass finds nothing. If `/paranoia` is installed, it replaces this default.
5. Models and test economy: the instance of `/fleet-economics` for this job — the roles and models of its §2 with the
   user's effort rulings, and this repository's verification levels discovered per its §3.1 (the commands named).
   Standalone default: every builder on the flagship tier and every critic on the strongest tier available; the
   levels are the check commands in the repository's scripts, task runner and CI file, and the full suite runs once on
   each step's final commit. If `/fleet-economics` is installed, it replaces this default.
6. Roles: orchestrator, managers, workers, advisor, blind critic, checker; who may read what.
7. Report shape: steps, results with evidence, deviations with reasons, open points, files written; a report file plus a
   message of at most 150 words.

### 2.3 PRD (one per job, `<date>-<ID>-prd.md`)
Role and model; read-first list; **why** (with evidence); the job, numbered, pedantically scoped; inputs with paths;
outputs with exact paths; constraints (files allowed and forbidden, what is out); verification commands including the
negative control; report format and length. A PRD is self-contained: a fresh agent with only the three files must be
able to execute it.

---

## 3. Inventory (a manager with workers, read-only)

Dispatch one inventory manager that spawns parallel workers and judges them. The default split is W1 to W4 below; a
worker whose question has no subject in this job (nothing external to depend on, no neighbour) is dropped, a source
named at intake that none of them reads gets its own worker, and the inventory PRD names each drop and addition with
its reason:

| Worker | Question it answers | Output |
|---|---|---|
| W1 the system's real surface | What does the thing we depend on actually serve, at the version deployed and at the newest line? What exists but is not reachable? | facts with file:line or measured output |
| W2 our side today | What does our code or system do now, step by step; where are ids, state, persistence; every place it assumes one user, one session, one provider, a fixed list (the **seams**); baseline gates run once | facts, seams list, gate tails |
| W3 the neighbours | What does each consumer or neighbour expect (types, payloads, actions, endpoints, auth); where do we diverge | divergences with file:line on both sides |
| W4 requirements, verbatim | Every requirement that bears on the job, quoted word for word with its source (ticket and section, spec path:line, contract clause), no opinion | the **requirements extract** |

Rules:
- Every load-bearing claim is spot-checked by the manager (open the file:line, rerun the command); a worker is looped
  back on any gap.
- The requirements extract is verified by script: every repo quote matches its file, a planted wrong quote fails; a
  coverage check shows every section of each requirement source either quoted or listed with a one-line reason why it
  does not bear on the job, and a planted gap fails.
- The extract carries no opinion and no design: it is the blind critic's spec.

The orchestrator accepts the inventory after its own spot checks of `DEFAULT orchestrator_spot_checks = 3` facts that
the design will rest on (the stricter end of a two-to-three range), and corrects the primer immediately where the
inventory contradicts it.

When draft questions for other owners exist at this point, a **questions manager** starts verifying them in parallel
(section 8).

---

## 4. Locks (orchestrator)

From the rulings and the inventory, write 5 to 8 locked design principles, numbered (lock 1 to lock n), into the
planner's PRD. Each lock names its basis: a ruling, a requirement line, or "orchestrator lock, no requirement line".
Always include an explicit **out** lock. Check each pattern below against the job: each one the job touches is
covered by a lock (one lock may cover more than one), and the planner's PRD names each one that does not apply, with the
reason:
- one source of truth, everything else generated from it, nothing written twice, nothing left dead;
- only what is actually served or available enters the design (availability computed, not hard-coded);
- every fact carries its source in a form the consumer can open or check;
- the core loop and where verification sits in it;
- the seams for the future, threaded now but not built out, and no new persistent store without its entry in the
  project's data register;
- tests and checks that need no external dependency (stand-ins that replay recorded behaviour);
- fault isolation: a failing part (a source, a tool, a neighbour) degrades only its own capability, detected at run
  time; the start and the request continue;
- every error says what happened, why, and what to do, for its audience (the end user one plain sentence; the record or
  log the code, cause and remedy); no empty-on-error and no silent fallback (`/unverified` hunts both).
  Standalone default for the hunt: search the change for fallbacks and defaults (`||`, `??`, `catch`, default
  values, demo or mock modes) and check on each error path that a failed read yields an error, never an empty or
  plausible value. If `/unverified` is installed, it replaces this default;
- boxes with one job each, explicit and versioned contracts between them, one composition root, dependencies pointing
  inward, and an architecture test that enforces what is today held only by convention;
- the out list.

A planner may challenge a lock only with evidence.

---

## 5. The plan (one planner, flagship tier per `/fleet-economics`)

The planner reads the three files, the inventory and the extract in full, reads the code itself for every inventory
claim marked inferred (not measured or read) that the plan rests on, measures baselines (digests, counts, test totals)
and writes the plan file with these sections, in this order:

1. **Summary for the user**: at most 15 lines, one point each: what gets built, the order, what stays out, what the user
   must know (limits, consequences such as "with the model off, this path answers nothing until X").
2. **Moving parts, now and later**: a component table (today, with file:line; what changes; what is new) and the
   interfaces between them; a table of future parts (sessions, multi-agent, sub-agent runs, more providers, more data,
   writes later, measurement) with the seam each plugs into; a list **"what could cement a door shut, and how the plan
   avoids it"**.
3. **Design detail per lock**: data shapes, file locations, names, error codes and the sentences a user sees, contract and
   schema diffs with their version step, persisted-data changes with their register rows, and every requirement relied
   on, quoted with its extract line.
4. **Open design choices**: a table `choice | option A | option B | evidence | recommendation`. The planner recommends; the
   orchestrator or the user decides, by the owners settled at intake (section 1). Never decided silently.
5. **Gap ledger**: `gap | locked design | programmatic truth (the exact command, or test name and assertion) | negative
   control (how that proof goes red without the change)`. A gap without both is reshaped or moved out.
6. **Steps**: dependency order (sequential by default; parallel only on disjoint files, with the integration step and its
   expected conflicts named), files allowed and forbidden, the risk class with the implementer and critic model and the
   test level per `/fleet-economics` (plus any level deliberately not run, with its reason), size, the commit prefix or
   ticket, the booking line and where it fits another card better, and baseline facts each step must keep green.
   Standalone default: every step is classed complex, built on the flagship tier, critiqued on the strongest tier, and
   proved by its gap-ledger command plus the full suite once on its final commit, no level skipped. If
   `/fleet-economics` is installed, it replaces this default.
7. **One PRD per step**, self-contained (section 2.3), written as separate files.

The planner runs `/paranoia` over the plan before reporting (consistency of numbers, instructions without a path,
design traps, schema mechanics, stale wording) and may consult the advisor. Standalone default: the self-check of
section 2.2 item 4, with the classes in the parenthesis added. If `/paranoia` is installed, it replaces this default.

---

## 6. The review triad (in parallel, all read-only)

### 6.1 Advisor (strongest tier per `/fleet-economics`; may read the primer and the orchestrator transcript)
Answers, with evidence, ranked by impact:
1. Does the plan build what the user asked for, in the user's own words? Where does it fall short or overreach?
2. The data or environment question: does the plan really use what the user expects (for example real data), and if not,
   what is the smallest in-scope way?
3. Weak points in each lock as detailed; anything that cements a door.
4. The open choices: agree or challenge each with evidence.
5. Slicing: order, size, file boundaries; can each PRD be executed by a fresh agent; are proofs and controls real?
6. Machine and time: realistic for the deadline and the hardware? What to merge or cut.

### 6.2 Blind critic (strongest tier; the strongest review)
- **Must not open**: the primer, the ledger, the inventory's opinions, any agent report, the advisor's file, the
  orchestrator's revision files, any transcript. If a PRD says "read the primer", the critic ignores it.
- **Reads**: the protocol (rules only), the requirements extract (its spec), the plan and the step PRDs (the artifact),
  and the code and data directly, running read-only probes that need no install, build, full-suite or end-to-end run.
- **Hunts**: a requirement contradicted or dropped; a claim about today's code that the code does not support; a proof that
  passes without the change or a control that cannot go red; a PRD a fresh agent cannot execute; an unversioned contract
  change; persisted data without its register entry; dead code; duplicated sources of truth; behaviour changes outside
  scope (especially what users see today); scope beyond the requirements.
- **Format**: findings as file:line plus a concrete failure scenario and the probe output; a closing section "suspicions
  I could not turn into a failure"; a verdict: SHIP / FIX FIRST (list) / REDESIGN. Loads `/adversarial-review`, runs
  `/paranoia` over its own findings. Standalone default for the review: each finding is first attacked against the
  code (a guard elsewhere, an unreachable path); it stands only with a concrete failing input, and one that can be
  neither shown nor disproved goes to the suspicions section. If `/adversarial-review` is installed, it replaces this
  default. Standalone default for the self-check: section 2.2 item 4. If `/paranoia` is installed, it replaces this
  default.

### 6.3 Contract and tracker checker (flagship tier or above; may spawn a tracker worker and a contract worker)
- Checks **every open choice, every seam and the out list** against all tickets the work touches, **current and
  future-dated**, and against the **signed** contract and its annexes. Finds the contract; never guesses; separates
  signed documents from drafts.
- Per choice: fits / conflicts / needs a change, with the verbatim clause or ticket line and its source.
- Lists **"future items the foundation must serve"**: item, what it will need, which seam serves it, or "gap".
- Never copies commercial figures (rates, totals). Local copies of contract text are deleted when the check is done, or
  never written; quotes of at most two sentences per clause stay in the check file.

---

## 7. Revision rounds

1. The orchestrator reads the three review files and verifies the findings it relies on (open the source, or run the
   probe).
2. It writes **`<date>-P-revision-N.md`**: **Decided** points, numbered, each naming the finding it answers; **PENDING
   USER** points for scope, contract and money, each with a recommendation and an alternative, designed for the
   recommendation and marked so they can be switched.
3. It loops back to the **same planner** (it keeps its context), which revises the plan and the PRDs in place and keeps a
   changelog ("Revision N") at the top of the plan. When the planner's retire signal has fired, a fresh planner briefed
   only from the plan, the PRDs and the review and revision files does this instead. Standalone default: the signal
   is its reported token use reaching `DEFAULT retire_at = 60 %` of its context window, or a context error from the
   harness. If `/fleet-economics` is installed, its agent-lifetime rule replaces this default.
4. The user decides the pending points; the orchestrator relays the decisions verbatim with the clock time and corrects
   any premise the user's answer changes (an answer that redefines a scope term can move work to another booking line).
5. The **same blind critic** re-checks (it keeps its unbiased view): a status table for each of its findings (closed,
   partly, open, with evidence) and a fresh refutation pass over the changed sections only, appended as "Re-check N".
   When the critic's retire signal has fired, a fresh blind critic briefed only from its predecessor's review file, the
   protocol, the extract, the plan and the PRDs re-checks instead. Standalone default: the signal of item 3. If
   `/fleet-economics` is installed, its agent-lifetime rule replaces this default.
6. **Disputes** between critic and planner are settled by a probe on the shape the production path really uses, run by
   one side and rerun by the other when it contests the first run; the probe outputs go into the files; the side the
   probe contradicts withdraws.
7. Stop when the critic's verdict is SHIP, or only items remain that are routed to a named later step. After three rounds
   that end without meeting this stop condition, the orchestrator re-examines its own locks before the planner's work:
   a round that finds the same problem again in a new form points at a lock, not at the plan.

These late findings each take another revision round, never a routing to a later step: a build step that edits a
guardrail or another owner's rule (route it to that owner as a question instead), a summary that hides a user-visible
consequence, a test premise measured on the wrong data shape.

---

## 8. Questions file for other owners

A manager verifies every question before it reaches a person:
- **Sources per item**: tickets and their comments, minutes, documents, the repository, the planning tool, the internal
  notes, the mailbox the user has access to, measured live state. Unreadable sources are reported, never worked around.
- **Drop** every item a source already answers, listed in an appendix with the answering source.
- **Structure**: a header (date, purpose, what it supersedes); Part A for the product owner or the user's own lead (with
  the item whose answer blocks the earliest plan step first, marked); Part B for the client; Part C for third parties
  (through their lead); appendices with actionable lists (for example a corrected configuration key list) and the
  dropped items.
- **Each item**: the question in one sentence; why (one line); "open as of" with the source and date that shows it open.
- Fold in the user's own answers given meanwhile; never present the user's decision as a question.
- Internal names only where the audience is internal; nothing that reveals secrets; customer-facing wording marked as a
  proposal where a separate owner approves it.
- Publication only on the user's ask, into the user's **own** document, then read back (word diff) and fix rendering.

---

## 9. Approval, then the build

Present the final plan in the form of the closing block below:
- a step table: what each step builds, the implementer model, what it books on;
- "know before you say go": status moves the plan needs, user-visible limits, what the user must do (paste a secret into
  a launcher, send the questions file, decide a booking);
- the questions file path.

After the user's go: write the ledger's first entry and the RESUME state table, then build with `/goal-loop` in fleet
mode (slice managers, scripted final checks with one own negative control per step). Standalone default: build the
steps in plan order, one fresh builder per step working from its PRD; the orchestrator accepts a step only when its
gap-ledger command passes on the committed head, its negative control goes red with the change reverted, and its critic
reports no open finding; a rejected step goes back to its builder with the findings. If `/goal-loop` is installed, it
replaces this default.

---

## 10. Durability and the lean orchestrator

- **Ledger** (orchestrator only): every decision, acceptance and measurement with a clock-read time; agent ids of live
  managers for resumption; corrections as new lines, never silent edits.
- **RESUME file**: where the truth lives, a state table (step, branch or location, accepted head, state), how to continue a
  step, what happens after the last one. Read it first after any compaction or restart.
- **Report files** per job, plus messages of at most 150 words.
- **Lean reads by the orchestrator**: of a state file, only the RESUME section or state table at its top; tracker reads
  without bulk fields; a ticket read once per session; never a full transcript; full documents only when the
  orchestrator makes a design call, a finding verdict or a routing decision on them (principle 2).
- **Scripts for every check run more than once** (identity, line endings, remote state, gates in a lock slot), run in
  the background, ten lines of output.

---

## 11. Failure modes seen, and the countermeasure built in

| Seen | Countermeasure in this skill |
|---|---|
| The planner missed a contract requirement (one user could list other users' records) | verbatim requirements extract as the blind critic's spec; contract checker over signed clauses |
| A primer premise was wrong ("search works", "X is outside the signed scope", "a colleague is away") | facts carry "measured by, how, when"; immediate primer correction |
| A proof that could pass without the change | gap ledger requires a negative control decided before dispatch |
| A critic and a planner contradicted each other | probe on the production shape decides; outputs recorded |
| A build step quietly edited a guardrail | routed to its owner as a question; the step's PRD forbids the file |
| A summary hid a user-visible consequence | the summary must state consequences plainly; the critic checks it |
| Times written without reading the clock | clock reads only; corrections logged |
| Contract text copied to the laptop | quotes only; local copies deleted after the check |
| The orchestrator's context filled during priming | lean reads; managers absorb diffs and logs |

---

## 12. Worked example (unnamed)

Intake and rulings (primer section 4) → primer, protocol → inventory manager with four workers: W1 the host system's
surface, W2 our own core and its seams, W3 the UI contract, W4 291 verbatim requirement quotes (script-verified) →
questions manager in parallel → seven locks in the planner PRD → plan (37 gaps, 8 steps, PRDs) → advisor, blind critic
(FIX FIRST), contract checker (signed offer and annexes found; two conflicts) → revision 1 (15 decided points, 2 pending
the user) → the user's decisions → planner revisions 1 to 3 (two more steps added) → blind critic re-checks 2 and 3 (one
finding withdrawn by its own probe) → questions file (13 items for the product owner, 7 for the client, 3 for a
colleague, 11 dropped) published to the user's own document on request → approval → the build of section 9 in fleet
mode.

---

## Closing block (required, as the plan-approval summary of §9)

```
STEPS      <n>. <what it builds>  builder <model tier>  critic <model tier>  books on <ticket or work package>
           ...
KNOW       <status moves the plan needs; user-visible limits and consequences; what the user must do before or after go>
QUESTIONS  <path of the verified questions file, or "none: every question answered by a source">
CRITIC     <the blind critic's last verdict: SHIP, or each remaining item with the later step it is routed to>
```

CRITIC is the load-bearing line: a plan presented for approval before the blind critic cleared it is the wish list of
principle 1, and without this line nobody can tell which one they are approving.
