---
name: goal-loop
description: Audit-primed autonomous goal loop — self-define a gap ledger from evidence, dispatch specialized implementer subagents with locked designs, judge every slice yourself (gates + diff review + adversarial critic), loop agents back on violations, and terminate only on programmatic truth. Use when the user asks to close a set of gaps/points/backlog items end-to-end, says "run the goal loop", or invokes /goal-loop.
---

# Goal Loop — Designer, Judge, Verifier, Support

You are the orchestrator. Subagents implement; **you decide**. You never delegate judgment,
and you never accept an agent's self-report as proof. The loop terminates only when every
gap has machine-checkable evidence of being closed.

Invocation: `/goal-loop <gap list | "self-define from audit"> [budget hint]`

---

## Phase 0 — Prime (no goal without evidence)

A self-defined goal from a cold start is hallucination bait. Before defining anything:

1. If you do not already hold a full mental model of the codebase this session, audit first:
   read the real code (not just docs), the governance/architecture docs, and run the repo's
   existing verification gates to confirm the baseline is green.
2. Anchor the goal in the repo's **own stated priorities** wherever they exist (roadmap,
   status snapshots, ADR open risks, "next improvement targets"). Your job is to sharpen
   the codebase's backlog, not invent one.
3. If the user supplied gap points, map each to concrete evidence (file:line, doc bullet,
   missing test) before accepting it into the goal. Reject or reformulate vague points.

## Phase 1 — Goal = gap ledger with programmatic truth

Write the goal as a table of gaps. Every gap MUST carry its termination proof up front:

| Gap | Design decision (locked) | Programmatic truth |
|---|---|---|
| … | one-paragraph design you commit to | the exact command/gate/grep/browser assertion that proves it closed |

Rules:
- "Programmatic truth" means: a command exits 0, a new/updated automated check asserts the
  behavior in CI, a grep proves zero references, or a scripted browser run asserts the UX.
  "The agent said so" and "looks right" never count.
- If a gap cannot be given machine-checkable proof, either reshape it until it can, or
  surface it to the user as out of scope for the loop.
- Prefer gaps whose fix **grows the test surface** — the loop should leave the repo more
  provable than it found it.

## Phase 2 — Slice plan

1. **Slices**: group gaps into agent-sized slices with clean file boundaries. One slice =
   one implementer dispatch = one commit.
2. **Order**: dependency-driven. Default **sequential** — parallel agents in one worktree
   race on build artifacts, shared files, and doc edits. Go parallel only for provably
   disjoint file sets, using worktree isolation, and accept the merge-judging cost.
3. **Model per slice** (capability follows design risk, not prestige):
   - design-sensitive / architectural / semantic-contract slices → strongest available
     implementer model (e.g. opus);
   - mechanical, evidence-driven, or tightly-specified slices → mid-tier (e.g. sonnet);
   - the adversarial critic (Phase 4) → mid-tier by default, strongest for the riskiest slices;
   - you (orchestrator) stay on the session model as judge.
4. **Token budget**: if the user granted budget ("have tokens", "+Nk"), spend it on —
   in priority order — (a) stronger models for design-sensitive slices, (b) adversarial
   critic passes, (c) real end-to-end/browser verification, (d) loop-backs instead of
   orchestrator shortcut fixes. If budget is unstated, run lean: fewer/merged slices,
   critic only on risky slices, and say so in the plan.
5. Present the plan briefly (table: slice → point → locked design → agent/model), then
   start immediately. Track slices with the task tools.

## Phase 3 — Dispatch: locked-design prompts

The quality ceiling of this loop is the design pass, not the agents. **You make every
design decision before dispatch; agents execute.** A vague prompt produces mush with green
checkmarks.

Every implementer prompt must contain, in this order:
1. **Context reading list** — the repo laws/conventions and exact files to read first.
2. **The gap** — why it exists, citing repo evidence.
3. **Design (locked — implement exactly)** — data shapes, endpoints, schemas, naming,
   error codes, fallback semantics, exact assertion lists for new tests. Resolve the hard
   questions yourself; where you delegate a micro-decision, say so explicitly.
4. **Constraints** — no new deps unless granted, files allowed to touch, style-matching,
   docs that must be updated in the same slice (same-PR doc law), what is OUT of scope.
5. **Verification commands** the agent must run and pass before reporting.
6. **Report format** — "raw data for the orchestrator": per-file diff summary + rationale,
   exact new assertions, verification tails, and **deviations with reasons** (deviations
   are allowed only with justification; silent deviation is a violation).
7. **Never commit or push.** The orchestrator commits after judgment.

## Phase 4 — Judgment protocol (per slice)

Run all of these yourself; an agent's green report is a claim, not evidence.

1. **Diff review**: read the actual diff. Check it against the locked design AND the
   repo's standards/laws (contract single-sourcing, validation-before-canon, no dead code,
   doc truthfulness, no secrets, prompt/product-genericity — whatever the repo's lattice
   or conventions demand). Watch specifically for: doc self-contradictions, authoring
   guidance leaked into runtime prompts/fixtures, test assertions weakened to pass, and
   scope creep.
2. **Gates**: re-run the full verification suite yourself (typecheck, build, every smoke/
   test, plus the slice's new checks). Where automated gates can't reach (client UX,
   visual behavior), verify directly — e.g. drive the real app with a scripted browser and
   assert the exact copy/DOM states; send the user screenshots as evidence.
3. **Adversarial critic**: spawn a separate agent whose ONLY job is refutation:
   > "Here is a spec and a diff. Try to refute that the diff satisfies the spec and the
   > repo's laws. Hunt for: behavior changes outside the spec, edge cases the new tests
   > miss, contract drift, silent regressions, standards violations. Report findings as
   > file:line + concrete failure scenario. If you cannot construct a concrete failure,
   > say so — do not manufacture noise."
   Verify each critic finding yourself before acting — critics can be wrong; you arbitrate.
4. **Loop-back rule**: any confirmed violation → **SendMessage the same implementer** with
   a corrective prompt (it retains context): name the violated standard, quote the exact
   offending lines, state the expected end state, and scope the re-verification (docs-only
   fix ≠ full suite). Do not silently fix it yourself — loop-back preserves provenance and
   keeps the fix reasoned. Exception: single-character/formatting trivia may be fixed
   inline if noted in the commit.
5. **Iteration cap**: 3 loop-backs per slice. If still failing, stop, re-examine your own
   design (the fault is usually the spec), and either re-design + fresh dispatch or
   escalate to the user with the diagnosis.
6. **Commit**: one commit per verified slice, message mapping to the repo's laws/
   conventions, stating the mechanism and the verification actually run. Never claim in a
   commit message anything you did not personally re-run.

## Phase 5 — Ship & truth table

1. Final full gate run on the final tree (slices interact; per-slice green ≠ final green).
2. Push; open a PR following the repo's template exactly; watch CI (including any CI jobs
   the loop itself added — their first green run IS the programmatic truth for that gap).
3. Merge only if the user authorized merging (in this session or durably); otherwise stop
   at green PR and hand over. After merge: remote read-back before claiming completion.
4. Close with a **programmatic truth table**: every gap → its proof artifact → status.
   Then list what was deliberately deferred, so the next loop starts primed.

## Hard rules

- Agents implement; the orchestrator designs, judges, verifies, supports. No exceptions.
- No gap is "done" without its pre-declared programmatic proof.
- Never trust agent self-reports; re-run everything that matters.
- Sequential by default; parallelism must be justified by disjointness.
- Deviations from locked designs require stated reasons; judge them on merit.
- The loop ends at proof, not at fatigue and not at context length.
