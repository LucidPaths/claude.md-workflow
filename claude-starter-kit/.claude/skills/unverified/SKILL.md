---
name: unverified
description: Hunt every place a system turns "I don't have this" into a confident answer — fallbacks, defaults, confidence thresholds, demo modes, empty states. Use when building or reviewing anything that produces claims from incomplete input, especially anything with a language model in it, and before shipping anything a person will act on.
---

# Unverified — make the system able to say "I don't know"

## The thesis

Most AI products do not fail by being wrong. They fail by being **confidently complete** — filling the
half of the answer they do not have with something plausible, in the same voice, in the same font, with
no seam a reader can see.

This is not a model problem. The model does what it is asked. It is a **design** problem: the system was
built with no first-class way to represent *absence*, so absence had to become something else on its way
to the screen.

The stance this skill puts you in: **treat every confident output as a suspect, and go find where the
uncertainty died.**

## When to run it

- Before shipping anything that produces a claim a human will act on
- On any code path that runs when a key, a network, a recording or a field is missing
- On any system where a model's output reaches a person without a human in between
- On your own review or analysis — the failure class applies to prose as readily as to code

## The hunt — five seams, in order

Uncertainty rarely dies in the schema. It dies at the joins. Go to them directly.

**1. Fallbacks.** Every `||`, every `catch`, every `if not api_key`, every "demo mode", "offline mode",
"mock", "sample". Grep for them. For each one: *when this fires, is the output distinguishable from a
real result — by the person looking at the screen?* Not by a developer reading the code. By the user.

**2. Defaults.** Default parameters, seed data, placeholder constants, `|| "Unknown"`, `?? 0`. A default
is an assertion with no author. Ask what it claims and who would believe it.

**3. Thresholds.** The quietest and most dangerous seam. Any confidence cutoff, any rounding, any
`if score > x: treat as known`. A rule like *"anything above 0.4 confidence counts as filled"* will
silently promote a guess to a fact and then stop asking about it — which means the guess is now
permanent and invisible. Find every threshold and ask what it *erases*.

**4. The empty state.** What the screen shows when there is genuinely nothing. If the empty state looks
finished, you have built a machine for producing convincing nothing. It should look unfinished.

**5. Provenance and evidence fields.** If a value carries a `source`, `evidence` or `citation`, check
what gets attached when there is no real source. Attaching the whole input as "evidence" for one extracted
claim is fabricated provenance — worse than no provenance, because it survives inspection.

## The traversal test — the one that finds what greps miss

Pick a single field the system genuinely cannot know. Follow it, by hand, end to end:

> ingest → schema → business logic → threshold → storage → API response → the screen

**Name the exact line where it stops being an unknown.** In a healthy system it never does: it arrives at
the screen still marked as missing. In most systems it dies somewhere in the middle, and everything
downstream inherits a fact that was never true.

Do this for three fields. It takes twenty minutes and it is the highest-yield review you can run.

## The naming test

Read your identifiers as a sceptic would. Does any name claim a property the code does not have?

`honestFallback`, `verifiedResult`, `groundTruth`, `confirmed`, `validated` — a name that asserts
trustworthiness *suppresses scrutiny* of the thing it names, including your own. A function that invents
a value is less dangerous when it is called `guessMissingFields` than when it is called `honestExtractor`,
because the first name warns the next reader and the second one disarms them.

## The verdict

For each finding, four lines. No prose essays.

```
WHERE      file:line — the seam
BECOMES    what the unknown turns into
WHO SEES   who receives it, and whether anything on their screen marks it
FIX        the smallest change that keeps the unknown visible
```

Rank by **who gets hurt**, not by how clever the finding is. An invented phone number in a demo is
noise; an invented revenue figure reaching a funding reviewer is the whole ballgame.

## What to build instead

The positive patterns below are all real, all taken from working code, and all cheap.

- **Give each kind of not-knowing its own value.** Not one `null`. A refusal is not a missing answer; a
  contradiction is not an absence; "the person declined" is not "we forgot to ask". Systems that
  distinguish `refused` / `unclear` / `not_established` / `contradicted` can act correctly on each.
- **Let a truthfulness bit travel.** Have every call report whether it *actually reached* the provider,
  thread that flag through to the interface, and show it. One team did this and it is the single best
  trust mechanism produced at the event: the page can say "transcribed live" only when it was.
- **Never let a threshold fill a gap.** A confidence cutoff may downgrade a value. It must never mark one
  as answered.
- **Record contradictions; do not resolve them.** Store both values with their sources and let a human
  adjudicate. A system that silently picks the more plausible number is inventing.
- **Put the arithmetic in code and the sentences in the model.** If a number can be re-derived
  deterministically, a decision based on it can be defended. If a model produced it, it cannot.
- **Write a test that enforces the placeholder staying a placeholder.** And understand what that test
  does *not* cover: it guards one seam. The other four are still open.

## Where this came from

This skill was distilled from a line-by-line review of seventeen repositories built at the AI Builder
Hackathon in Addis Ababa, August 2026, whose briefs demanded that every unverified field be **flagged
rather than guessed**.

Every failure pattern above appeared in real submitted code, and so did every fix — the refusal values,
the truthfulness bit, the confidence floor, the contradiction record, the code-owns-the-numbers split.
The good patterns were invented independently by teams under two days of time pressure, which is the
best evidence available that they are reachable rather than aspirational.

One deliberate rule in how it is written: **the working patterns are credited, the failures are
anonymous.** The teams who made the mistakes already received them in detail, by name, privately. A
document that will outlive the event has no business pinning them to anyone.

And the class is not limited to code. During that same review, the analysis itself produced a finding
that was true of one commit and false of the repository, and a credential scanner that reported
repositories "clean" when it had never been shown it could catch anything. Same failure: a confident
output where the honest one was *I don't know yet*.

That is the whole discipline. A system that cannot say "I don't know" will always say something else.
