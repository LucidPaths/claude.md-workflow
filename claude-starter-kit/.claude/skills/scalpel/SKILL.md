---
name: scalpel
description: Deep recon first, minimal cut second - determine the real mechanism, frequency, and blast radius of a problem from the live system, then ship the smallest change at the choke point, with proof proportional to the risk and machinery proportional to the evidence. Use when the user runs /scalpel, or hands over a fix/incident/change where the right SIZE of the solution is part of the question. The skill sizes itself - a small task gets a small pass.
---

# Scalpel - Full Imaging, Smallest Incision

Two phases: recon until the problem is *determined*, then the minimal cut. The core law:
**machinery scales with evidence of need, never with the gravity of the invocation.**
Being invoked ceremonially does not entitle the work to be ceremonial.

## Phase 0 - Size the invocation itself (do this in your head, in seconds)

Before anything: is this a question, a one-liner, or a system change? Answer questions as
questions. If the honest response is three sentences or a five-line diff, say so and do
exactly that - invoking this skill on a small task and responding big is the first
failure it exists to prevent. State your sizing in one line and move on.

## Phase 1 - Recon to determinism (never optional, never wasted)

Understand before designing. Read the LIVE system, not your memory of it:

- **Mechanism**: what actually happens, step by step, with evidence (file:line, config,
  log, census). A wrong mechanism model produces a correct-looking fix for a different
  problem.
- **Frequency and blast radius**: how often has this actually fired, and what did it
  actually cost? An observed once-a-month self-evident zero-loss failure and a silent
  daily corrupter deserve different machinery. Count real occurrences; don't imagine ones.
- **Existing machinery**: what already runs, schedules, alerts, enforces? The best fix
  usually lives INSIDE something that already exists. Inventory the choke points - the
  places everything already passes through.
- **Standing laws**: postmortems, forbidden operations, conventions of the repo/host you
  are about to touch. A fix that violates a paid-for law is a regression.

Recon spend is always recovered - it is what makes the small fix safe. Artifact spend is
not. If a big design gets killed later, the recon it triggered was still the value.

## Phase 2 - The cut

- **Choke point first**: prefer the one place everything already flows through over
  converting N callers. Prefer editing the existing file over creating a sibling system.
  Prefer deleting over adding.
- **Smallest change that removes the failure mode**: not the smallest that looks like a
  fix - the mechanism from Phase 1 must be provably interrupted.
- **Proof proportional to risk, discipline over artifact**: prove the actual change -
  replay the real incident against the edited code, feed the checker a known-bad case,
  show the invariant. Ship a permanent test artifact only where the repo's own
  conventions expect one; otherwise the reproducible proof run, documented where the
  change lives (PR body, commit), IS the deliverable. Proving is non-negotiable;
  shipping the proving machinery is a separate decision.
- **Name what you deliberately did not build**, with the reason, where the reviewer will
  see it. Restraint that isn't recorded looks like ignorance and gets "fixed" later.

## The overengineering tells (check the design against each before building)

1. **Self-justifying components**: a part whose necessity is created by another part,
   not by the problem (the lock that only protects against the trigger you added).
2. **Dead-justification shapes**: structure kept after its reason died (the shared
   primitive nobody calls anymore). If a design decision changed, re-derive what it
   was carrying.
3. **Evaporating packaging**: count what disappears if you drop ONE choice. If most of
   the artifact is packaging for a single optional decision, the decision is the design
   - question it directly.
4. **Latency/elegance vanity**: optimizing a rare state's speed or a working path's
   beauty at real artifact cost. Price improvements against observed frequency.
5. **Ceremony-shaped output**: PRDs, harnesses, roles, and fan-outs produced because the
   process was invoked, not because the risk demands them.

## Delegation calculus (subagents are machinery too)

Fan out only when it buys something real: genuinely parallel INDEPENDENT implementation
lanes, isolation of a heavy read that would drown your context, or an adversarial pass
on something you wrote yourself. One file's fix does not need an implementer; a
question does not need a researcher. When you do fan out: locked designs, disjoint
files, you judge everything personally. Killing agents whose design you've outgrown is
cheap BEFORE anything ships - pivot early, keep the recon, discard the artifacts
without sentimentality.

## Done means

The mechanism is interrupted and proven; the diff is as small as the mechanism allows;
existing laws are honored; what was deliberately not built is recorded with reasons;
and one honest sentence states frequency/blast-radius of what remains. If the fix grew
past what Phase 1's evidence supports, stop and re-derive - the fault is usually a
design carrying a dead justification.

## The close - four lines, printed

```
SIZE        what this turned out to be (question / one-liner / system change), from Phase 0
MECHANISM   the failure path from Phase 1, and the line that now interrupts it
PROOF       what you ran against the edited code, and its output
NOT BUILT   what you deliberately did not build, and why
```

NOT BUILT is never empty. If nothing was considered and rejected, Phase 1 did not
happen - go back and do it rather than writing "n/a".
