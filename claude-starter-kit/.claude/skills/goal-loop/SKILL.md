---
name: goal-loop
description: Audit-primed autonomous goal loop — self-define a gap ledger from evidence, dispatch specialized implementer subagents with locked designs, judge every slice (yourself, or through slice managers in fleet mode: gates + diff review + negative control + blind adversarial critic), loop agents back on violations, and terminate only on programmatic truth. Use when the user asks to close a set of gaps/points/backlog items end-to-end, says "run the goal loop", or invokes /goal-loop. Not for a fix that closes a single gap (just do it), not for planning without execution, not for reviewing one outward deliverable.
---

# Goal Loop — Designer, Judge, Verifier, Support

You are the orchestrator. Subagents implement; **you decide**. You never delegate the final
judgment (in fleet mode slice managers run the per-slice judgment protocol, and your scripted
check accepts or rejects), and you never accept an agent's self-report as proof. The loop
terminates only when every gap has machine-checkable evidence of being closed.

Invocation: `/goal-loop <gap list | "self-define from audit"> [budget hint]`

## When not to use

- Planning without a build: `/blueprint` plans it, and is the plan phase of fleet mode (below).
- Model routing, critic tiers, the verification ladder or token rules on their own:
  `/fleet-economics` is the single source for them.

---

## Phase 0 — Prime (no goal without evidence)

A self-defined goal from a cold start is hallucination bait. Before defining anything:

1. **Start in the right place.** Memories and project-scoped MCP servers bind to the folder
   the session was started in (for example, a tracker MCP configured only in the project's
   folder). If the session started elsewhere, say so and restart in the project's folder
   before anything else.
2. Audit first, unless this session has already done all three: read the real code (not just
   docs), read the governance/architecture docs, and run the repo's existing verification gates
   to confirm the baseline is green. **A baseline you did not run
   is a claim.** Docs, comments, PR texts and status notes are clues; only executable code and
   a run prove behaviour. An inventory made with one search idiom is not an inventory (a
   route check that greps `pathname ===` misses the regex routes).
3. Anchor the goal in the repo's **own stated priorities** wherever they exist (roadmap,
   status snapshots, ADR open risks, "next improvement targets", the signed contract or the
   task's Definition of Done). Your job is to sharpen the codebase's backlog, not invent one.
4. If the user supplied gap points, map each to concrete evidence (file:line, doc bullet,
   missing test) before accepting it into the goal. A point that maps to no concrete evidence
   is reformulated until it does (the reformulation shown in the plan) or, when no wording
   does, rejected and reported to the user.

## Phase 1 — Goal = gap ledger with programmatic truth

Write the goal as a table of gaps. Every gap MUST carry its termination proof and its negative
control up front:

| Gap | Design decision (locked) | Programmatic truth | Negative control |
|---|---|---|---|
| … | one-paragraph design you commit to | the exact command/gate/grep/browser assertion that proves it closed | how that proof is shown to go red without the fix |

Rules:
- "Programmatic truth" means: a command exits 0, a new/updated automated check asserts the
  behavior in CI, a grep proves zero references, or a scripted browser run asserts the UX.
  "The agent said so" and "looks right" never count, and neither does a check that could not
  read its input (a checker exiting with a usage or read error is not a pass).
- **A proof that has never failed proves nothing.** The negative control is decided here,
  before dispatch, not remembered at judgment (Phase 4 runs it).
- If a gap cannot be given machine-checkable proof, reshape it until it can; a gap for which
  no reshaped form carries one is surfaced to the user as out of scope for the loop.
- Among candidate gaps the repo's own priorities (Phase 0, item 3) do not order, a gap whose
  fix **grows the test surface** (adds or tightens an automated check) ranks first — the loop
  should leave the repo more provable than it found it.

## Phase 2 — Slice plan

1. **Slices**: group gaps into slices of one feature each with clean file boundaries: each
   slice names the files it may touch, and two slices that share a file run in sequence
   (item 6). One slice = one implementer dispatch = one feature PR. The implementer may
   commit more than once on its slice branch (the implementation, then each correction
   round); publication happens once, after judgment. One PR per feature does not mean one
   commit.
2. **Order**: dependency-driven. Default **sequential** — parallel agents in one worktree
   race on build artifacts, shared files, and doc edits. Go parallel only for provably
   disjoint file sets, using worktree isolation, and accept the merge-judging cost.
   **Shared ledgers are written by the orchestrator only**: `WORKING_STATE.md`, the loop
   ledger, backlogs, release notes, registries, tracker comments, time records. The
   implementer reports the text; you merge it. Parallel writers on one ledger overwrite
   each other's rows.
3. **Model per slice, critic tier, test level** (capability follows design risk, not
   prestige): classify every slice (mechanical, standard, complex) and staff and prove it by
   `/fleet-economics` (§1 classes, §2 roles and models, §3 the verification ladder).
   Standalone default: a slice is mechanical when its brief fixes every edit and names the
   guarding test, complex when it crosses modules or changes a contract, schema, guardrail,
   permission or persistence, standard otherwise; the fast tier builds a fully specified
   (mechanical) slice, the balanced tier a standard one, the flagship tier a complex one;
   critics only on the strongest tier; the test level is the narrowest one whose check goes
   red without the fix. If `/fleet-economics` is installed, it replaces this default. You
   stay on the session model as judge.
4. **Token budget and shared usage:** `/fleet-economics` §0 and §4. Standalone default: a
   fan-out of more than `DEFAULT fanout_probe = 3` parallel agents starts as one probe agent
   and widens only after the probe finished without a quota error; stop on the first quota
   error; every agent reports in a file plus a message of at most 150 words. If
   `/fleet-economics` is installed, its §0 and §4 replace this default. If the user granted
   budget ("have tokens", "+Nk"), spend it in priority order on (a) stronger builders for
   complex slices (item 3), (b) critic passes, (c) loop-backs instead of orchestrator
   shortcut fixes. If budget is unstated, run lean and say so in the plan: no builder above
   item 3's tier, no critic pass beyond Phase 4's, and gaps that touch the same files share
   one slice (fewer, merged slices).
5. Present the plan as one table, one row per slice (slice → point → locked design → class
   → models → test level), plus item 4's lean note when the budget is unstated, then start
   immediately. Track slices with the task tools.
6. **Isolation and integration:**
   - **One git worktree per implementer**, one slice branch each (`<wave>/s1-<slug>` →
     `<repo-parent>/<repo>-<wave>-s1`), cut from `main` (a dependent slice from the branch
     it depends on, see publication below). Real dependency installs in every worktree
     (`npm ci` or the equivalent) — never symlinks or junctions to a shared `node_modules`:
     a worktree teardown follows junctions and deletes the shared install. Agents commit
     scoped work on their own slice branch, as the repo's identity, but never push, never
     open the PR and never merge until the orchestrator has judged the slice (Phase 4).
   - **The integration branch** (`feat/<wave>`, from `main`) collects the accepted slices
     for the orchestrator's final full-tree gate run and the deploy rehearsal. It gets its
     own worktree too. Never run a merge from the main checkout: `git merge` acts on
     whatever branch that checkout is on, and it is on `main` (a merge run there once moved
     local `main`; it was reset from origin before anything was pushed).
   - **Never switch the branch of a checkout something loads live.** `~/.claude/skills` is
     read by every session on the machine, and a clone that a running server or page serves
     from is live too: work in a worktree, never `checkout` there (a live skills checkout
     was once briefly switched to an unreviewed branch).
   - **Publication follows the repo's rule:**
     - **Repos published by pull request: ONE PR PER FEATURE, always** (review,
       documentation and the tracking of billable work all key on the PR). Each slice
       branch opens its own PR with **base `main`**; a slice that depends on another (same
       file, same contract) branches from that slice's branch and opens its PR with that
       branch as base (stacked); GitHub retargets it to main when the prerequisite merges.
       The local integration branch exists ONLY for the final full-tree gate run and the
       deploy rehearsal — it is never pushed and never the PR. Never a single wave PR.
     - **Repos owned by someone else** (a client, another team): their contract governs
       (branch names, task ids in commits, reviewer and merge rules, protected branches,
       what a commit may name); read the project's repository contract before the first
       commit: its `CLAUDE.md`, its rules and contribution files, and the team overlay the
       workspace names.
     - **Local-only repos** (the user names them, for example `~/.claude`): commit locally,
       never add a remote.
   - **The agent opens its PR, after judgment.** Order: agent reports "done" → orchestrator
     judges (diff, own gate run, negative control, critic) → loop-backs on the same agent's
     open pipe → when accepted, the orchestrator sends the commit message and the agent
     commits (as the repo's identity), pushes and opens the PR with the repo's template →
     the pipe stays open until the PR is green → close the agent. Agents never merge; the
     user merges.
   - Parallel only across provably disjoint file sets (a shared file such as a message
     catalogue is an accepted, orchestrator-resolved conflict). Slices on the same file run
     sequentially on top of each other.
   - **Machine and repo traps, each one hit for real:** check free disk BEFORE creating
     worktrees, and create them only while free disk exceeds
     `DEFAULT install_pair_disk = 1 GB` per pair of real installs they will hold (a machine
     once ran out of disk mid-wave and the installs died with `ENOSPC`); when reclaiming,
     delete only a `node_modules` that is a real directory (on Windows, `Get-Item` reports
     an empty `LinkType`), never a junction. Run ONE test suite at a time across agents on
     an 8 GB machine (background watchers were killed by memory pressure). Staging paths with
     `[id]` segments needs `git --literal-pathspecs add --`; plain `git add` treats the
     brackets as globs and skips the files silently. A stacked PR gets NO checks if the
     workflow's `pull_request` trigger is filtered to base `main`; the fix lives in the
     workflow on the HEAD branch (GitHub evaluates `pull_request` workflows from the merge
     ref), so a one-line commit on the stacked branch queues the run. Agents' background CI
     monitors die with the machine; the orchestrator confirms check states with
     `gh pr checks` itself.

## Phase 3 — Dispatch: locked-design prompts

The quality ceiling of this loop is the design pass, not the agents. **You make every
design decision before dispatch; agents execute.** A vague prompt produces mush with green
checkmarks.

Every implementer prompt must contain, in this order:
1. **Context reading list** — the repo laws/conventions and exact files to read first.
2. **The gap** — why it exists, citing repo evidence.
3. **Design (locked — implement exactly)** — data shapes, endpoints, schemas, naming,
   error codes, fallback semantics, exact assertion lists for new tests. Resolve every design
   question yourself; a micro-decision you delegate is named in the prompt as delegated.
4. **Constraints** — no new deps unless granted, files allowed to touch, files forbidden
   (shared ledgers, live checkouts, settings and credentials), style-matching, docs that must
   be updated in the same slice (same-PR doc law), what is OUT of scope, the commit identity
   the repo requires, and **no call that writes to an external system** (mail, tracker, time
   records, CRM, code host) unless the user approved exactly that write.
5. **Verification commands** the agent must run and pass before reporting, including the
   negative control from the ledger.
6. **Report format** — "raw data for the orchestrator": per-file diff summary + rationale,
   exact new assertions, verification tails, the negative-control run, **deviations with
   reasons** (deviations are allowed only with justification; silent deviation is a
   violation), and the texts meant for shared ledgers.
7. **Commit locally, never publish.** Commit scoped work on the slice branch with honest
   messages; do not push, open a PR, merge or deploy. Publication is the orchestrator's
   call after judgment; merge and deploy need separately established authority.

## Phase 4 — Judgment protocol (per slice)

Run all of these yourself (in fleet mode the slice manager runs them, Fleet mode item 3); an
agent's green report is a claim, not evidence.

1. **Diff review**: read the actual diff. Check it against the locked design AND the
   repo's standards/laws (contract single-sourcing, validation-before-canon, no dead code,
   doc truthfulness, no secrets, prompt/product-genericity — whatever the repo's lattice
   or conventions demand). Watch specifically for: doc self-contradictions, authoring
   guidance leaked into runtime prompts/fixtures, test assertions weakened to pass, and
   scope creep.
2. **Gates**: run the slice's proof yourself at the level its change type requires
   (`/fleet-economics` §3.2-3.3): the gap's programmatic truth, the static checks, the slice's
   new checks, and the one full-suite log for the exact candidate head (the builder's; in
   fleet mode the slice manager's), never a second run of the same head; your own full run
   is on the final tree (Phase 5). Where
   automated gates can't reach (client UX, visual behavior), verify directly — e.g. drive the
   real app with a scripted browser and assert the exact copy/DOM states; send the user
   screenshots as evidence — and only for the change types the ladder names.
   Standalone default: every change type gets the checks this item lists, and the browser
   check runs only for a change a UI renders. If `/fleet-economics` is installed, its
   §3.2-3.3 replace this default.
   **Identity gate on every judged head:** `git log --format='%an <%ae> | %cn <%ce>'
   <base>..HEAD` shows only the identity the repo requires (the project's rules name it,
   author and committer). A commit under any other identity is a defect and is rewritten
   before anything is pushed (a personal identity once ended up on hundreds of commits
   across six branches; a reviewer found it, and every one had to be rewritten).
   **Negative control for every fix that closes a ledger gap or a confirmed finding** (item
   4's single-character/formatting trivia excepted): a test that has never failed proves
   nothing. Demand (from the agent, or do it yourself) one run with the fix reverted or
   the guard removed, and the exact assertion that went red. "Restoring the old route
   fails 26 tests" is evidence; "the suite is green" is not. Same for parity/fixture
   checks: perturb one side and show the other side's test fails (two parity tests once
   held duplicated literals and would have passed a coordinated one-sided edit; a
   cross-file byte comparison replaced them). A checker that reports zero findings must be
   shown to fire on a planted defect.
3. **Adversarial critic**: spawn a separate agent whose ONLY job is refutation. It is always a
   **fresh agent, never a fork** of the orchestrator (a fork inherits your context and your
   assumptions, and then agrees with them); it receives only the spec, the diff and what it
   may execute:
   > "Here is a spec and a diff. Try to refute that the diff satisfies the spec and the
   > repo's laws. Hunt for: behavior changes outside the spec, edge cases the new tests
   > miss, contract drift, silent regressions, standards violations. Report findings as
   > file:line + concrete failure scenario. If you cannot construct a concrete failure,
   > say so — do not manufacture noise."
   Verify each critic finding yourself before acting — critics can be wrong; you arbitrate.
   Tell the critic what it may execute (the suites, single-file probes against the real
   installed libraries, read-only queries) and require the probe output in the report: a
   claim reproduced against the installed library in the worktree beats a claim reasoned
   from a docs page. Require a closing section "suspicions I could not turn into a failure"
   — the absence of noise is part of the signal. Verify by MEASUREMENT where a finding rests
   on data ("there are no such rows": query each environment, put the counts in the PR). A
   DO NOT SHIP verdict is the loop working, not the loop failing.

   Example: one critic stopped a submit path that could never finish for large uploads and a
   resume path that fingerprinted files the operator could not see; both had green suites.
4. **Loop-back rule**: any confirmed violation → **send a corrective message to the same
   implementer** (SendMessage in Claude Code; it retains context): name the violated
   standard, quote the exact offending lines, state the expected end state, and scope the
   re-verification by the fix's change type (item 2; docs-only fix ≠ full suite). Do not
   silently fix it yourself — loop-back preserves provenance and keeps the fix reasoned.
   Exception: single-character/formatting trivia may be fixed inline if noted in the commit.
5. **Iteration cap**: 3 loop-backs per slice. If still failing, stop and re-examine your own
   design first (three corrections against one spec did not converge, so the spec is the
   first suspect). Re-design + fresh dispatch when the re-examination names the design fault
   (for example the signal of fleet mode item 11: the confirmed findings of every round break
   the same rule at a different place) and its fix stays inside the user's rulings and the
   gap's locked programmatic truth; otherwise escalate to the user with the diagnosis.
6. **Relay nothing unverified.** A claim about a system that you pass to the user, another
   session or another agent (a route exists, a tool covers a store, a row is closed) is
   checked against the source first. An agent's report is relayed only as the agent's report
   (a relayed "this covers your case" once cost another session a correction round; a "no
   such route exists" taken from a single grep had to be retracted).
7. **Accept and publish**: the orchestrator accepts the exact candidate (the commit sha it
   judged), keeps the implementer's commits (the implementation and each correction round,
   Phase 2 item 1), and sends publication instructions down the pipe (push, open the PR with
   the repo's template, base per Phase 2). Commit messages state the mechanism and the
   verification actually run; never claim a result that was not re-run.

## Phase 5 — Ship & truth table

1. Final full gate run on the final tree (slices interact; per-slice green ≠ final green).
2. Push; open a PR following the repo's template exactly; watch CI (including any CI jobs
   the loop itself added — their first green run IS the programmatic truth for that gap).
3. Merge only if the user authorized merging (in this session or durably); otherwise stop
   at green PR and hand over. After merge: remote read-back before claiming completion.
   **Deploy is a separate go**: a merge authorization never covers a deploy; deploy only when
   the user says deploy (in this session or by a standing rule for exactly that target).
4. Close with the **programmatic truth table** (the closing block below), then list what was
   deliberately deferred, so the next loop starts primed.
5. **Hand the user only what is theirs**: decisions (options they can judge, recommendation
   first) kept apart from todos (numbered, in execution order, each with its owner and the
   exact command). Findings meant for the user to read go into a page or document they read,
   not into the loop's input folder; the loop's roadmap, ledger, PRDs and slice prompts go
   where the project keeps loop input (its instructions file names the folder); a handoff
   goes to the project's handoff location, and the session record (`WORKING_STATE.md` in
   this kit) is brought up to date before the session closes.

## Fleet mode (large work, long runs, the orchestrator's context must last)

Proven on a run of 10 slices plus an integration over 17 hours: the orchestrator ended at
67 % context, and every slice was judged with its own negative control. Use it when the work
has more than `DEFAULT fleet_slices = 3` slices, or when the user asks for a run that survives a
context compaction.

1. **Three files every agent reads first** (in the project's loop folder): a **primer** (goal,
   the user's rulings verbatim, measured facts, sources), a **protocol** (local-only rules,
   machine limits, repo law, proof rules, report shape), and its **own PRD**. No agent needs
   the orchestrator's context; the orchestrator re-reads no diff, full report or transcript
   (item 3 names what it checks).
2. **Plan phase as a team (full procedure: `/blueprint`):** an inventory manager with workers
   (facts with file:line, plus a verbatim requirements extract), a planner (plan, gap ledger,
   one PRD per slice), an **advisor** (strongest tier; may read the primer and the orchestrator
   transcript), one **blind critic** (strongest tier; reads only the protocol's rules, the
   requirements extract, the artifact and the code, never the primer, ledger, reports or
   transcripts), and a checker of every choice against the tracker's current AND future-dated
   items and the signed contract.
   Revise until the blind critic clears; the user approves the plan.
   Standalone default: this team and this stop condition. If `/blueprint` is installed, its
   procedure replaces this default.
3. **Slice managers judge, the orchestrator checks.** One manager per slice spawns the
   implementer, reads the diff, runs the gates and every negative control itself, spawns a
   FRESH blind reviewer per round, loops back at most 3 times, writes the full report to a
   file and sends at most 150 words. The orchestrator's final check per slice is scripted
   and holds only these: the static checks and typecheck, the slice's own test files,
   identity, EOL, nothing on a remote, the manager's full-suite log for the exact head, and
   ONE negative control of its own on the slice's key fix (the ledger's negative control for
   the slice's first gap row; item 10, `/fleet-economics` §3.3).
   Standalone default: this list, and no second full-suite run on a head that already has
   its log. If `/fleet-economics` is installed, its §3.3 replaces this default. Then
   "accepted at <sha>", ledger line, next slice.
4. **Durability:** report file per slice, a ledger written by the orchestrator only with
   clock-read stamps, a RESUME file with a state table (slice, branch, worktree, accepted
   head, state), a commit for the implementation and for each correction round (Phase 2, item 1). A compaction or a lost agent costs
   nothing: a fresh manager continues from the branch and the report file.
5. **Nothing is dropped:** a finding outside a slice's files goes as a "Carried" section into
   the PRD of the slice that owns those files; a loop-back budget spent on a slice moves its
   last wording fixes into the next slice touching them.
6. **Disputes between agents** (critic versus planner, reviewer versus implementer) are
   settled by a probe on the real data shape, never by argument; the probe output goes into
   the report.
7. **Machine guard, adapt per machine:** measure free memory before every heavy job (an
   install, a build, a test-suite run, a browser run); start one only while free memory is
   above the floor and a slot is free, with lock directories (`mkdir` is atomic) as the
   slots; both change only through the ASK below (on an 8 GB laptop the floor was
   1.5 to 2 GB and the slots one or two; the defaults take the stricter end:
   `DEFAULT memory_floor = 2 GB`, `DEFAULT heavy_slots = 1`). Worktrees and installs go on a
   disk with more than `install_pair_disk` free per pair of real installs (Phase 2, item 6).
   ASK when the user says their own load changed: "Memory floor and heavy-job slots are <current values>. New values?" → new values: use them / unchanged: keep them / nobody to ask: keep the current values and report the question.
8. **Discipline per role:** workers apply `/rigor` and `/proof`; reviewers and critics
   `/adversarial-review`; managers and critics run `/paranoia` over their own output before
   reporting; the orchestrator runs `/paranoia` before the handoff.
   Standalone default: workers mark every claim verified, inferred or assumed and show each
   check they cite failing once on a known-bad case; reviewers and critics run a bug hunt,
   then try to disprove each finding, and report each as confirmed (with its triggering
   input), disproved (citing the code) or unresolved; managers, critics and the orchestrator
   re-check their own output one defect class per pass until a pass finds only cosmetics.
   Each of these skills, if installed, replaces its part of this default.
9. **Local first:** no push, PR, tracker task or time record until the user has gone through
   the whole line; every tracker move the user approved for the orchestrator is logged in
   the ledger.
10. **Test economy:** `/fleet-economics` §3 (change type → cheapest proving level; the full
    suite once per candidate, run by the slice manager on the builder's clean committed head
    (the builder does not run it), once on the whole line by the orchestrator before any PR;
    browser and live-model runs only at the release candidate, for the change types that need
    them). The final assurance is unchanged: a full run exists for every candidate and for the
    whole line. Standalone default: while working, the narrowest level whose check goes red
    without the fix; the two full runs named here; at the release candidate a browser run
    only for a change a UI renders and a live-model run only for a changed prompt. If
    `/fleet-economics` is installed, its §3 replaces this default.
11. **Agent lifetime** (one slice ran ten review rounds; its manager's context neared 800 k
    tokens and one worker overflowed; an agent that keeps running gets slow on every turn
    and loses detail). Standalone default: retire a manager or worker when its reported
    token use reaches 60 % of its context window, when it has delivered and its next job is
    a new deliverable, or when its slice reached 3 review rounds and the third still has a
    confirmed finding; resume it only for a bounded loop-back on its own deliverable (named
    findings, no new reading). If `/fleet-economics` is installed, its §2.1 agent-lifetime
    rule replaces this default. The FRESH manager's brief is built only from durable files
    (current head, what each round closed, what is open, the locked design), never the old
    transcript. The same 3 rounds are the signal to re-examine the design itself: when the
    confirmed findings of every one of those rounds break the same rule at a different place,
    stop enumerating bad forms and switch to allowed (canonical) forms that fail closed, or
    to a structure that makes the defect impossible (for model output: code fills facts into
    placeholders, the model never writes the figure).

## Hard rules

- Agents implement; the orchestrator designs, judges, verifies, supports. In fleet mode slice
  managers run the per-slice judgment and the orchestrator's scripted check is the acceptance.
- **The shape of the loop:** task → brainstorm with the user until the orchestrator provably
  understands it (the user confirms the orchestrator's written restatement of the task) →
  orchestrator scopes the roadmap → segments it into pedantically scoped
  single features → writes ONE locked PRD per feature → dispatches ONE implementer per
  feature in its own worktree → keeps every agent's pipe open → does nothing to a slice
  until that agent reports done → distrusts "done" (judge, gates, negative control, critic)
  → corrections go down the same pipe into the same session → loop until the critic is
  satisfied against the spec both sides agreed on → agent opens its PR → close.
- One agent, one feature, one worktree, one PR. An agent never merges, never deploys and
  never writes a shared ledger.
- No gap is "done" without its pre-declared programmatic proof and a negative control that
  went red.
- Never trust agent self-reports; re-run every check your acceptance rests on (Phase 4 item 2;
  in fleet mode, fleet mode item 3); relay nothing unverified.
- Every judged head carries only the repo's required commit identity.
- No external write (tracker, mail, time records, code host) without the user's approval of
  exactly that write.
- Sequential by default; parallelism must be justified by disjointness.
- Deviations from locked designs require stated reasons; accept one only when you confirmed
  its stated reason yourself (a probe, a read of the source) and the gap's proof and negative
  control still hold; otherwise loop back (Phase 4 item 4).
- The loop ends at proof, not at fatigue and not at context length.

## Closing block (required) — the programmatic truth table

```
GAP       <gap>  PROOF <command or test + its output>  NEG-CONTROL <the assertion that went red without the fix>  STATUS <✓ proven | ✗ failing: <check> | ? not checked>
          ...
DEFERRED  <what was deliberately left out, and why, so the next loop starts primed>
```

A gap with no NEG-CONTROL is not ✓, and a ✓ rests on the run against the final tree
(Phase 5, item 1), never on a slice's earlier green.
