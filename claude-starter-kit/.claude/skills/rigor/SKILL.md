---
name: rigor
description: Verification-first reasoning discipline — reason from the specifics in front of you, ground every claim in the actual source before relying on it, expose the inference chain, adversarially self-check each step as the person who inherits the work, and keep verified / inferred / assumed separate through to the output. Use when the user runs /rigor or asks for rigorous, grounded, first-principles reasoning on a specific problem.
---

# Rigor — Grounded, Verification-First Reasoning

Apply this discipline to the current task:

Reason from the specifics in front of you, not from the shape of similar problems you've seen. First, restate the task in your own words and define what makes an answer correct *here* — the concrete success conditions for this case, not generic ones.

Ground every factual claim: read the actual source, signature, file, or data before relying on it. Never substitute memory for verification. When you reason, expose the chain — state each inference and the premise it rests on, so a wrong premise is visible rather than buried inside a conclusion.

Surface assumptions the moment you make them. Any step depending on something unverified gets marked and resolved before you build further on it.

After each substantive step, run one adversarial pass before continuing: name the 2–3 most likely ways it's wrong or incomplete, and the strongest objection a sharp reviewer would raise. Address what survives. Run this pass as the person who inherits the work and gets paged when it breaks — not as its author.

Check scope continuously: confirm you're solving the actual task, not a narrower or broader one you drifted into. Where the task underdetermines a choice, commit to the most defensible interpretation, state it, and proceed — don't stall, don't silently guess.

Keep three categories separate and carry the distinction into your output: what you verified, what you inferred, what you assumed. Treat confidence as earned per-claim, not applied in bulk.

Stop when the success conditions are met and you can demonstrate they are — not when the work merely looks finished.

## Close with the ledger — this is the mechanism, not a formality

End every run with the three lists, labelled, even where one is empty:

```
VERIFIED   claim -> the source you actually read (file:line, command + its output, the row)
INFERRED   claim -> the premises it rests on
ASSUMED    claim -> what would have to be true, and what breaks if it is not
```

A claim that fits none of the three is not a claim, it is a guess — cut it, or move it to
ASSUMED with its cost attached. If ASSUMED is empty on a non-trivial task you did not look
hard enough: name the thing you are taking on trust.
