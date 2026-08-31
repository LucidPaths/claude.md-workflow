---
name: paranoia
description: Iterative adversarial self-verification at the end of a work session or before a handoff — hunt one unexhausted defect class per pass, fix with proof, stop at convergence. Use when the user runs /paranoia, asks to "assume it's wrong and recheck", or before declaring a large multi-artifact work session done.
---

# Paranoia — Convergent Adversarial Self-Verification

Born 2026-07-23: five consecutive passes over an 11-hour build each found real defects — a different class (or a swept class in an unswept document) every time, with severity decaying monotonically: architecture → records → contradictions → stale lines → clerical digits. The method is the class catalog + the convergence rule. The thesis: **"I checked it" exhausts nothing; a CLASS of defect is exhausted per document, per tree — and done is when the finds decay to cosmetics across a fully-swept artifact×class matrix.** One irreducible residual is accepted and named: the record always lags its own last correction by one cosmetic step — chasing it is infinite regress, not diligence.

## The rules

1. **One pass = one or two unexhausted classes.** Never re-run the previous pass's greps and call it a new pass — repetition finds nothing and manufactures false confidence.
2. **Classes exhaust PER DOCUMENT / PER TREE, not globally.** Purging stale claims from the repo does not clean the PRD; checking the main repo does not check the fork. Enumerate the artifact set first (every file touched or written today, every tree, every live system), then sweep the class across ALL of it.
3. **Fresh checks only.** Your own read-backs from earlier in the session are stale. Re-read live state (git ls-remote, DB rows, file bytes) — never cite memory or a prior claim as verification.
4. **Every find gets: fix + machine proof the class is now dry** (a grep that returns empty, a count that matches, a re-run that passes). A fix without a dry-proof leaves the class open.
5. **Fix-tooling discipline:** backslash-bearing edits via Write-tool script files (inline heredocs mangle escapes on some hosts); explicit `&&` after any heredoc; assert-anchored replaces (`assert count==1`) so a missed anchor fails loudly instead of silently no-oping.
6. **Stop at convergence, honestly.** When a pass finds only cosmetics, declare the classes exhausted, and write the residual-risk line INTO the handoff (e.g. "this document is stale until re-verified live") — the handoff must distrust itself. Do not run passes past convergence to perform diligence.
7. **The artifact set = everything you TOUCHED this session, not everything you created** — including yesterday's documents you appended addenda to, memory files, PR comments, and the skill you are running. (Pass 6 of the origin session found its real defects exactly here: morning addenda gone stale by evening, in a folder outside the enumerated set.)
8. **Your own pass notes are artifacts.** A find noted mid-pass and not fixed is an OPEN find — close it within the pass or carry it explicitly onto the next pass's hunt list. Dropped notes are how "converged" sessions ship known defects. (Origin session: a memory-staleness find was noted during pass-5 planning, dropped, and only closed in pass 6 when the user forced the re-run.)
9. **Truth-sync is never regression — and only regression is forbidden.** Updating any artifact (PR bodies, READMEs, specs, memory, skills — including this one) to newfound truth is ALWAYS in scope for a paranoia pass; what is forbidden is regression: losing content, weakening verified claims, or rewriting append-only records (session audits and filed records get dated addenda, never edits to what was recorded). If a scope instruction ("don't touch X this pass") collides with a truth-fix, the fix goes to the TOP of the verdict as a loud carried item with its blast radius stated ("X currently misleads cold readers") — never buried mid-list. (Origin session: a stale PR body — the review's front door — was carried quietly under a scope bound for one pass; the user rightly escalated: a company-standard PR description that misleads cold readers is never an acceptable carry.)

## The class catalog (hunt in this order; extend when a new class is discovered)

| # | Class | How to hunt |
|---|---|---|
| 1 | **Un-persisted head-knowledge** | Ask: what would die if this session ended now? Operational recipes, expected first-run readings, activation orders, undocumented assumptions inside prompts/instructions (an instruction with no capability/skill path behind it is a defect — verify the path EXISTS, e.g. read the actual SKILL.md). |
| 2 | **Counts, hashes, totals vs reality** | Every number in every doc (commit counts, test counts, row counts) re-derived from source (`git log --oneline main..HEAD \| wc -l`, run the suite, count the rows). Session-mortal artifacts: anything load-bearing living in scratchpad/temp gets copied into the durable folder. |
| 3 | **Cross-file / cross-claim consistency** | Grep the whole artifact set for superseded states ("blocked on X", "needs Y", "TODO", old route counts, old plans) that later work resolved. Hunt direct contradictions between sibling docs (spec §A vs spec §B vs the script that implements them). |
| 4 | **Repo hygiene + far-side trees** | `git ls-files` for junk (`__pycache__`, `.pyc`, temp files); `git grep` for absolute user paths / scratchpad references in committed files; `git status` clean on EVERY clone incl. the ones you touched hours ago; local head == remote head on every branch (`git ls-remote`). |
| 5 | **Live-system re-read** | Every prod mutation made today re-read from the live system now (rows, statuses, cards, memberships). Prior read-backs are stale by rule 3. |
| 6 | **The handoff's own navigability** | Read the primary handoff doc TOP-DOWN as a cold agent: does anything early contradict anything late? Do the "next steps" reference decisions that no longer exist? Are all companion files listed in Artifacts? Structural skim of headings for numbering/section gaps. |

## Output per pass

End every pass with a verdict line: `Pass N: hunted classes [..] across [artifact set] — found K defects (list), fixed with proofs (list), classes now exhausted for (scope).` When K only contains cosmetics, declare convergence and stop.

## Relationship to siblings

`/proof` is the discipline for a single data operation; `/rigor` for a single reasoning chain; **`/paranoia` is the end-of-session sweep that assumes the session itself accumulated drift** — including in the documents the other two disciplines produced. It typically ends by finalizing `/session-audit` (the audit is only trustworthy AFTER the sweep).
