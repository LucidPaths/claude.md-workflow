---
name: proof
description: Verify a data operation without being fooled by your own checks — the discipline for migrations, dedups, reconciliations, mass-edits, backfills, and "is it actually done?" claims over real data. Chase mismatched numbers, verify the verifier, match by natural key, prove on a clone, confirm-before-delete. Use when the user runs /proof or is about to run or trust a destructive or large-scale data operation.
---

# Proof — Verify a Data Operation Without Being Fooled by Your Own Checks

The thesis: **"the check passed" is not "the thing is true."** Most data-op disasters aren't a missing check — they're a check that *silently lied*. This is the discipline for any migration, dedup, reconciliation, mass-edit, backfill, or "is it really done?" verdict over real data.

## The one reflex

**When a number doesn't match what you expected, that is the most valuable thing on the screen.** Chase it — don't round it off, don't explain it away, don't move on. Every bug worth catching first showed up as a count that was slightly wrong: 130 vs 98, 39 edits vs 4, 112 rows vs the real ~4. The discrepancy *is* the finding.

## Verify the verifier — before you trust a passing check

A check that can only pass is not a check.

- **Confirm the query ran against what you think it did:** real column / identifier names (a clean zero from the *wrong column name* is worse than no query at all), the **specific** table or scope (not "the field exists somewhere"), the right database / pod / cluster.
- **A null join, an empty result, a "skipped" is NOT a pass.** Make checks assert loudly. Before trusting that a check passed, prove it *can* fail — feed it a known-bad case and watch it catch.
- **Count with real `count(*)`, never an estimate** (`reltuples` / `n_live_tup` are stale by design).

## Match reality, not your assumptions

- **Identify rows by a stable natural key** (name / email / code), never by position or a mutable property. "`id == id`" across two systems is the assumption that overwrites the wrong rows.
- **Never validate a snapshot against a moving source.** Freeze the source, then compare the whole frozen window — two coincidentally-unchanged tables look like perfect parity and aren't.
- **Exclude re-serialized or intentionally-divergent columns** from parity hashes, or you'll "find" edits that were never made — and a gate must understand *intended* difference, not flag it as drift.

## Prove it on a clone before prod

Rehearse the operation on a throwaway clone that **matches the target's real config** — a clone missing prod's settings hides exactly the bug that only fires in prod. Assert every invariant on the clone, re-run once to prove idempotency, *then* run for real under sign-off.

## Before you destroy anything

- **Back up first**, and verify the backup is non-empty and restorable.
- **Canonical-confirmed-then-delete:** confirm the correct entry is in place, *then* remove the wrong one. Deletion after confirmation isn't dataloss — but hoarding tagged zombies isn't cleanup either.

## Done when

One invariant over the **full set** (never a sample) is provably **0 / N** — zero rows lost, zero dead links, zero mismatches you can't explain. Treat docs, prior session notes, and your own earlier claims as **stale until re-verified against live**. In the result, keep separate what you **measured against live data** versus what you're **trusting from a doc or estimate** — they are not the same confidence. "Looks done" is not done; show the invariant.

## State the close in this form — otherwise you asserted it, you did not prove it

```
INVARIANT    the one statement that must hold ("0 rows lost", "43/43 pins present")
POPULATION   what it ran over, with its count — the FULL set. A sample is not a proof.
COMMAND      the exact query that produced it, and its raw output
FAIL-PROOF   how you know the check could have failed — the known-bad case you fed it
TRUSTED      what you did NOT measure, taken from a doc, an estimate, or a prior claim
```

FAIL-PROOF is the load-bearing line. A check with no demonstrated failure mode is the exact
thing this skill exists to catch, and it is invisible in a passing result.
