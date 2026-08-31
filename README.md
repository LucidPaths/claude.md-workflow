# Claude.md Workflow

A governance framework for AI-assisted development with [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Drop it into any repo to turn Claude from a raw coding assistant into a disciplined, self-auditing development agent.

Distilled from battle-tested patterns in the [HIVE](https://github.com/LucidPaths/HiveMind) project, and from running these disciplines daily on production infrastructure.

**Two ways to use this repo, and both are first-class:**

1. **Install it.** Drop `claude-starter-kit/` into your repo root and it works - hooks, rules, skills, templates.
2. **Cannibalise it.** Point your agent at this repo and take the parts you want. Most of the value is in the *ideas*, and they transfer to any agent framework. Nothing here is load-bearing on the rest.

---

## The Skills

Eight invocable disciplines. **This is the part most worth stealing** — they work as prompts for
any model, with or without the rest of the kit.

**Start with these two.** They cover the two moments most work goes wrong.

| Skill | Use it when |
|-------|-------------|
| `/adversarial-review` | Before merging a diff. Two passes that overclaim in *opposite* directions, then adjudication. The intersection of "the bug hunter couldn't miss it" and "the disprover couldn't kill it" is remarkably accurate. |
| `/shippable` | Before submitting, demoing or handing over. There is the work you did and the work that *arrives* — the gap is invisible to exactly one person: you. |

**Then these four, as the situation calls for them.**

| Skill | Use it when |
|-------|-------------|
| `/proof` | Before trusting a migration, dedup, backfill or any "is it actually done?" claim over real data. "The check passed" is not "the thing is true" — most data disasters are a check that silently lied. |
| `/unverified` | On anything that produces claims from incomplete input. Systems fail by being confidently *complete*, filling the half of the answer they don't have with no seam a reader can see. |
| `/rigor` | On a reasoning problem with no artifact yet. Keeps verified, inferred and assumed separate all the way into the output. |
| `/scalpel` | When the right *size* of a fix is part of the question. Machinery scales with evidence of need, never with the gravity of the invocation. |

**These two are advanced.** They assume a large session or a multi-agent setup — skip them until you
want that.

| Skill | Use it when |
|-------|-------------|
| `/paranoia` | End of a long multi-artifact session, or before a handoff. "I checked it" exhausts nothing; a *class* of defect is exhausted per document, per tree. |
| `/goal-loop` | Closing a set of gaps end to end with subagents. Every gap declares its terminating proof *before* work starts; "the agent said so" never counts. |

### Why folder format matters

A skill must live at `.claude/skills/<name>/SKILL.md` with YAML frontmatter carrying `name` and
`description`. **A flat `.md` file directly inside `skills/` is never registered** — it silently does
nothing, forever. `tests/test_hooks.py` fails if one appears, because this is the easiest way to ship
a skill that cannot be invoked.

The `description` is the most important line in the file: it is what the model reads when deciding
whether the skill applies. Write it as a trigger condition ("Use when the user runs X or asks Y"),
not as a summary.

The two-phase research pattern that used to be `/research-decide` is now a reference doc at
`claude-starter-kit/docs/research-then-implement.md` — it is a way of working, not something you invoke.

## The Enforcement Problem

This is the hardest-won lesson in the repo, and it applies to any prompt-based framework
including this one.

**Instruction adherence decays, and more prose makes it worse.**

Two arguments get conflated here and only one of them still matters. The **capacity** argument — long
instructions eat your context budget — is largely dead. Against a million-token window a 16KB
instruction set is a rounding error. **Do not trim your rules to save tokens.**

The **attention** argument survives, because a bigger window did not make attention uniform. The
[memory docs](https://code.claude.com/docs/en/memory) are blunt about the status of these files: they
are context, not enforced configuration, and where two rules contradict, the model "may pick one
arbitrarily." Operating agent fleets, the shape matches — a rule holds best right after it is read
and worst after a resume or deep into a long session, and sustained adherence to one naming
convention measured closer to half than to the ninety-plus percent the instruction implied, on
machines with context to spare. That is one operator's observation rather than a benchmark, but it
is the number that changed how this repo is written.

So the lesson is not "write less to save room." It is that **a rule stated twice is not stated twice
as strongly**, and another paragraph telling the model to try harder buys nothing.

What works is making non-compliance **visible in the output**. Not "verify your claims," but
*"end with a table of every claim and the source you read for it."* An instruction the model can
satisfy by asserting it complied is not enforcement. An instruction that requires a filled-in
artifact is.

Every skill here ends with a required closing block for exactly this reason - `/proof` must print
its invariant, population, command, fail-proof and what it merely trusted; `/scalpel` must print
what it deliberately did not build. A skipped block is obvious. A skipped intention is not.

The strongest version is a check outside the model entirely: a git hook, a CI job, a test.
**If a model must never do X, enforce X with tooling, not with a markdown rule it can forget.**
That is what `.claude/hooks/` and `tests/test_hooks.py` are for.

## What This Is

The **claude-starter-kit** is not application code. It's an operating system for how Claude Code behaves inside your repository — rules, hooks, skills, and templates that shape every session into consistent, auditable, high-quality work.

Think of it as a constitution your AI agent follows, regardless of what it's building.

## What's Inside

```
claude-starter-kit/
├── CLAUDE.md                          # Main instruction file (the brain)
├── README.md                          # Quick start guide for the kit
├── .claude/
│   ├── settings.json                  # Hook registration
│   ├── PR_GUIDELINES.md               # PR description + commit format
│   ├── rules/
│   │   ├── coding-standards.md        # 8 universal coding standards
│   │   ├── traps.md                   # 8 behavioral traps + anti-rationalization
│   │   └── quality-gate.md            # Pre-submit verification checklist
│   ├── hooks/
│   │   ├── session-start.py           # Auto-injects git state at session start
│   │   ├── maintenance-check.py       # Blocks session end if docs not updated
│   │   ├── pre-compact.py             # Snapshots state before context compaction
│   │   ├── session-end.py             # Auto-persists working state on exit
│   │   ├── precommit-doc-check.py     # Blocks commits missing doc updates
│   │   └── _state_utils.py            # Shared utilities for state hooks
│   └── skills/                        # folder format - a flat .md never registers
│       ├── adversarial-review/SKILL.md
│       ├── proof/SKILL.md
│       ├── rigor/SKILL.md
│       ├── paranoia/SKILL.md
│       ├── scalpel/SKILL.md
│       ├── unverified/SKILL.md
│       ├── shippable/SKILL.md
│       └── goal-loop/SKILL.md
├── samples/                              # Filled-in examples from real projects
└── docs/
    ├── PRINCIPLE_LATTICE.md           # 5 axiomatic design principles
    ├── TASK_CONTRACT_TEMPLATE.md      # Per-task acceptance criteria template
    ├── research-then-implement.md      # Two-phase task pattern (reference)
    ├── WORKING_STATE_TEMPLATE.md      # Session-transcending memory template
    ├── ROLE_TEMPLATE.md               # Role-based workflow template
    └── GLOBAL_ROUTER_TEMPLATE.md      # Thin CLAUDE.md router template
```

## The Four Layers

### 1. Principles (the axioms)

Five non-negotiable design principles defined in `PRINCIPLE_LATTICE.md`:

| # | Principle | Axiom |
|---|-----------|-------|
| 1 | **Modularity** | Lego blocks, not monoliths |
| 2 | **Simplicity Wins** | Don't reinvent the wheel |
| 3 | **Errors Are Answers** | Every failure teaches; errors must be actionable |
| 4 | **Fix The Pattern** | Cure the root cause, not the symptom |
| 5 | **Secrets Stay Secret** | Closed by default; nothing left open to exploitation |

Every decision Claude makes is scored against these. If a choice violates one, it reconsiders.

### 2. Instructions (the brain)

`CLAUDE.md` is the heavyweight file. It contains:

- **8 coding standards** — simple solutions over complex ones, actionable error messages, no dead code, fix ALL instances of a pattern, single source of truth for cross-file contracts, User-Agent headers on API calls, closed-by-default security, update both sides of a boundary (also in `.claude/rules/coding-standards.md`)
- **8 documented behavioral traps** — real failure modes with "Stop." interrupts (premature optimization, scope creep, single-instance fixes, sycophantic agreement, retry loops, verification language, etc.) plus an anti-rationalization table (also in `.claude/rules/traps.md`)
- **Verification language rule** — forbidden phrases ("should work now", "looks correct") that require evidence from tool calls before any completion claim
- **Anti-rationalization patterns** — catches the model constructing arguments for why traps don't apply ("this is different because..." = it's not)
- **Cross-file contract tracking** — a table for tracking values that must stay in sync across files
- **`[ADAPT]` sections** — placeholders Claude fills in as it learns your specific project (overview, key directories, build commands, architecture patterns, gotchas)
- **Session transcendence** — `WORKING_STATE.md` pattern + pre-compaction snapshots for context that survives both session boundaries and context compaction

The adaptive design means the kit grows with your project instead of being static boilerplate.

### 3. Automation (the hooks)

Six lifecycle hooks registered in `.claude/settings.json`:

**Session Start** (`session-start.py`):
- Injects current branch, last 5 commits, uncommitted changes
- Pulls next steps from `ROADMAP.md` or `TODO.md` if they exist
- Restores pre-compaction snapshot if one exists (session transcendence)
- Claude starts every session oriented, not asking "what are we working on?"

**Session Stop** (`maintenance-check.py`):
- Detects if code files were modified during the session
- If yes, **blocks session end** until documentation is confirmed up-to-date
- Prevents documentation rot — the #1 cause of stale project context

**Pre-Compaction** (`pre-compact.py`):
- Fires before Claude Code compresses context in long sessions
- Auto-updates working state ephemeral sections from transcript
- Saves a full snapshot to disk so session-start.py can restore it
- Enables **session transcendence** — context survives compaction

**Session End** (`session-end.py`):
- Auto-persists working state on graceful session exit
- Updates ephemeral sections (Active Task, Conversation Context)
- Preserves curated sections (Corrections, Learnings) untouched

**Pre-Commit Doc Check** (`precommit-doc-check.py`):
- Fires before `git commit` via PreToolUse hook
- Blocks commits where code files are staged but no documentation is
- Catches doc rot at commit time, not just session end

**Shared Utilities** (`_state_utils.py`):
- Common functions for working state auto-maintenance
- Used by pre-compact.py and session-end.py

### 4. Skills (the disciplines)

Eight invocable disciplines, covered in **[The Skills](#the-skills)** above. They are listed last here
and first in the document on purpose: they are the layer you can lift out and use anywhere, while the
three layers below only matter if you adopt the kit itself.

## How It Works

```
1. Drop claude-starter-kit/ contents into your repo root
2. Commit so Claude Code picks up the files
3. Start a Claude Code session

First session:
  → session-start.py injects git state + next steps
  → Claude reads CLAUDE.md, fills in [ADAPT] sections
  → .claude/rules/ files are auto-loaded by Claude Code (no explicit import needed)
  → Future sessions build on that foundation

Every session:
  → Orientation at start (branch, commits, changes, next steps)
  → Standards enforced during work (8 coding standards, 8 trap interrupts)
  → Documentation check at end (blocks if code changed but docs didn't)

Per task:
  → Copy TASK_CONTRACT_TEMPLATE.md, define acceptance criteria
  → Task is NOT done until every criterion is verifiably satisfied
```

## Why It Works

The kit is **self-reinforcing**. Each component addresses a specific failure mode:

| Failure Mode | What Prevents It |
|-------------|-----------------|
| Claude drifts from project context | `[ADAPT]` sections in CLAUDE.md that grow with the project |
| Session starts cold, wastes turns exploring | session-start.py auto-injects git state |
| Documentation rots, future sessions hallucinate | maintenance-check.py blocks session end until docs updated |
| Scope creep ("while I'm here, I'll also...") | Trap #4 + `/scalpel` sizing the cut to the evidence |
| Sycophantic code review ("this looks correct") | `/adversarial-review` exploits the bias against itself |
| Context bloat from mixing research and coding | `docs/research-then-implement.md` separates the phases |
| A passing check that could never have failed | `/proof` - fail-proof the checker before trusting it |
| Confident output where the honest answer is "I don't know" | `/unverified` - the five seams where uncertainty dies |
| Work that only runs on the author's machine | `/shippable` - the cold-clone test |
| A long session accumulating silent drift | `/paranoia` - one defect class per pass, to convergence |
| Single-instance fix creates false safety | Coding Standard #4: fix ALL instances or none |
| Cross-file values drift silently | Cross-file contracts table + Coding Standard #5 |
| Vague acceptance criteria, gold-plating | Task contract template with explicit done conditions |
| Two-layer validation updated on one side only | Coding Standard #8 + Trap #8 |

## Benefits for Claude

1. **Immediate orientation** — no wasted turns asking "what are we working on?"
2. **Behavioral guardrails** — 8 traps + an anti-rationalization table, short enough to actually hold in context
3. **Explicit done conditions** — task contracts prevent both under-delivery and over-engineering
4. **Structured decision-making** — priority hierarchy and research-then-implement prevent flailing
5. **Session continuity** — `WORKING_STATE.md` bridges context between sessions

## Can Other AI Tools Use This?

Mostly yes. The principles, coding standards, and traps are universal to any LLM doing code generation:

- The Python hooks are plain scripts — any AI tool with lifecycle hooks could call them
- The skills are markdown prompts — they work as system prompts for any model
- The `[ADAPT]` pattern is transferable to any agent framework
- Only `.claude/settings.json` is Claude Code-specific (hook registration format)

## Parallel Multi-Session Architecture

The kit enables a powerful pattern: **multiple Claude sessions working in parallel on different tasks, unified by shared standards**.

```
                     ROADMAP.md (5 items)
                          │
           ┌──────┬───────┼───────┬──────┐
           ▼      ▼       ▼       ▼      ▼
        Branch1 Branch2 Branch3 Branch4 Branch5
        Claude1 Claude2 Claude3 Claude4 Claude5
           │      │       │       │      │
           │   Each session has:         │
           │   • Same CLAUDE.md (shared standards)
           │   • Same PRINCIPLE_LATTICE.md (shared axioms)
           │   • Own TASK_CONTRACT (scoped criteria)
           │   • Own DECISION.md (isolated decisions)
           │      │       │       │      │
           ▼      ▼       ▼       ▼      ▼
          PR1    PR2     PR3     PR4    PR5
           │      │       │       │      │
           └──────┴───────┼───────┴──────┘
                          ▼
                   Branch 6 (Orchestrator)
                   Claude 6 (Review + Merge)
                   • /adversarial-review each PR
                   • Resolve cross-PR conflicts
                   • Verify cross-file contracts
                   • Merge into unified commit
```

**Why this works:**

- **Modularity principle** — each task is a self-contained block by design
- **Task contracts** — explicit boundaries and done conditions prevent overlap between sessions
- **Cross-file contracts table** — the orchestrator can audit that contracts weren't violated across branches
- **Shared principles** — all sessions make decisions against the same axioms, so outputs are architecturally compatible without direct communication
- **Adversarial review** — the orchestrator runs 3-pass review on each PR before merging

This is essentially **agentic MapReduce** — map work across N isolated sessions, reduce in an orchestrator session. The sessions don't need to talk to each other. They share the same constitution, so their outputs converge.

**`/goal-loop` is the disciplined version of this pattern**, and if you steal one thing, steal that
one. It adds what the diagram is missing: the orchestrator locks every design decision *before*
dispatch, never accepts an agent's self-report as evidence, re-runs every gate personally, and
terminates only when each gap has a pre-declared machine-checkable proof.

## Edge Cases: Model Degradation and Weaker Models

> **Real-world observation:** Even top-tier models (Opus-class) exhibit behavioral degradation during long sessions — contradicting themselves, losing track of what they did, giving confidently wrong answers, and violating explicit instructions they acknowledged moments earlier. This section exists because it happened in practice while building this very kit.

### The Problem

The starter kit assumes a model that can:
1. Hold multiple constraints in working memory simultaneously
2. Self-check actions against stated rules before executing
3. Maintain accurate recall of what it did vs. didn't do in the current session

**Weaker or degraded models fail at all three.** When they do, the failures are invisible — the model doesn't say "I'm confused," it confidently fabricates a coherent-sounding but wrong answer.

### Known Degradation Patterns

| Pattern | What Happens | Example |
|---------|-------------|---------|
| **Constraint evaporation** | Explicit rules acknowledged early in the session get silently dropped | "Never push to main" → pushes to main |
| **Confident confabulation** | Model gives contradictory answers with equal confidence when challenged | "I pushed to both repos" → "I pushed to neither" → actually pushed to one |
| **Action amnesia** | Model loses track of what it actually did vs. planned to do | Claims no commits were made when git log shows otherwise |
| **Sycophantic self-correction** | When challenged, model agrees with the user's framing even if the original answer was correct | Changes a right answer to a wrong one because the user sounded upset |
| **Instruction bleed** | Instructions for repo A get applied to repo B in multi-repo contexts | Branch rules for one repo leaking into operations on another |
| **Broken self-verification** | Model writes a check to validate its own work, the check is malformed, and the meaningless result is reported as a finding | A grep whose pattern never expanded returns "0 matches" and is read as "clean" |

### Mitigations

**For weaker models (Haiku-class, smaller open-source):**
- **Reduce the always-loaded set further** — 8 standards + 8 traps is already trimmed, but it is still too much for a small context window. Pick the 3-4 traps your project actually hits and cut the rest
- **One repo per session** — multi-repo contexts dramatically increase confusion. Never give a weaker model access to repos it shouldn't touch
- **Hardcode don'ts in hooks, not instructions** — if a model must never push to main, enforce it with a pre-push git hook, not a markdown rule it can forget. Models forget instructions; git hooks don't
- **Shorter sessions** — degradation compounds over long conversations. End sessions early and rely on `WORKING_STATE.md` for continuity instead of marathon sessions
- **Skip skills that require self-adversarial reasoning** — `/adversarial-review` requires the model to argue against itself across 3 passes. Weaker models collapse into agreement by pass 2. Use human review instead

**For strong models showing degradation (long sessions, complex context):**
- **Watch for confident contradictions** — if the model gives you two different answers about what it did, trust `git log`, not the model
- **Re-anchor with explicit state checks** — ask the model to run `git log`, `git status`, `git branch` and report raw output before taking further action
- **Reduce active scope** — if working across multiple repos/branches, finish one completely before starting another
- **Fresh session over recovery** — if the model is visibly confused, starting a new session with `WORKING_STATE.md` context is cheaper than trying to re-orient the current one

### The Hard Rule

**Never trust a model's verbal claim about what it did. Verify with tool output.**

If a model says "I didn't push anything," check `git log --remotes`. If it says "I only modified one file," check `git diff --stat`. The model's self-report is the least reliable source of truth in any session — the git history is the actual record.

And the corollary, which is easier to miss: **verify the verifier.** A malformed check produces a
confident, meaningless result - an empty grep from a pattern that never expanded looks exactly like
a clean result. Before trusting that a check passed, feed it a known-bad case and watch it catch.
That discipline is `/proof`, and it applies to a model checking its own work as much as to any
migration.

This applies to all models, all tiers, all context lengths. It's not a weakness of small models — it's a property of LLMs that surfaces more often under load.

## Requirements

- **Python 3** — for session hooks (stdlib only, no pip packages)
- **Git** — for orientation and maintenance checks
- **Claude Code** — the CLI tool this kit is designed for

## Changelog

### 2026-08-31 — Subtraction Pass

A second pass, entirely cuts. The kit had accumulated four separate places telling the model to
verify its claims, all loaded simultaneously. The [memory docs](https://code.claude.com/docs/en/memory)
are explicit that longer instructions reduce adherence, so the fix was removal, not more prose.

**Changed:**
- **Traps 13 to 8**, by merging rather than deleting. "Let me optimize this" and "While I'm here"
  were one failure (unasked work); "This looks correct" and "This should work now" were one failure
  (assertion instead of proof); "I'll fix this one place" and "I'll add it to the validation list"
  were one failure on two axes (across files, across layers). Trap 5 now points at the Verification
  Language Rule in `quality-gate.md` instead of restating its forbidden-phrase list — that was the
  third of four duplicate coverages
- **Nothing was deleted, two things were relocated.** Position bias (Wang et al. 2023) moved into
  `/adversarial-review`, where you actually enumerate and rank many items. Instruction degradation
  (Liu et al. 2023) moved into CLAUDE.md's Context Discipline, which already governs how work is
  broken up. Both keep their citations
- **README leads with the skills.** They were at layer 4, below a principle table, a standards list
  and six hook descriptions. They are the part worth stealing, so they are now the first thing after
  the intro — and tiered, so a newcomer starts with two rather than eight. `/goal-loop` and
  `/paranoia` are labelled advanced instead of sitting next to a beginner placeholder
- **One rationalization table, not two.** `quality-gate.md` and `traps.md` each carried a
  "you're rationalizing" table with different rows and the same job, both loaded every session.
  Merged into the single table in `traps.md`, which is where behavioural catches belong
- **The Enforcement Problem separates two arguments that were being conflated.** The capacity
  argument (long instructions eat your context budget) is obsolete against a million-token window and
  is now explicitly disclaimed — *do not trim rules to save tokens*. The attention argument survives
  and is what the section now rests on, with the fleet number presented as one operator's observation
  rather than as a benchmark. The repo's own `/unverified` exists to catch the stronger phrasing

**Deliberately not done:** `paths:` frontmatter was *not* retrofitted onto the three shipped rules.
Coding standards, traps and the quality gate apply to any file in any language, so scoping them
would make them silently absent exactly when they matter. The mechanism is documented in the kit
README for project rules, where it belongs.

### 2026-08-31 — Skills Refresh

Five months on, the skills layer had fallen behind Claude Code and behind the practice the kit was
distilled from. The rules, hooks and templates added in March were untouched by this pass.

**Fixed:**
- **Skills were flat `.md` files in `skills/`, which Claude Code does not register.** All five
  silently did nothing when invoked. Verified against a live session's registered-skill listing.
  `tests/test_hooks.py` now fails if a flat `.md` reappears
- **Both `session-start.py` and `maintenance-check.py` resolved the project root by walking up
  from their own file location**, which breaks when a hook runs from a subdirectory. Now
  `git rev-parse --show-toplevel` with a cwd fallback
- `test_hooks.py` used an em-dash in its FAIL line - the same Windows cp1252 crash class fixed for
  the arrow in March, and it only renders when a test fails

**Changed:**
- **`session-start.py` emits the `hookSpecificOutput` envelope** rather than a flat top-level
  `additionalContext`. The envelope is what current Claude Code documents and what every recent
  hook feature builds on; whether the flat key is still honoured for `SessionStart` is unverified,
  so the kit ships the current shape and the tests assert it
- `maintenance-check.py` ignores lockfiles, and its trivial-session threshold rose from 15 to 100
- Skills 5 to 8, replaced entirely: `adversarial-review` (rewritten), `proof`, `rigor`, `paranoia`,
  `scalpel`, `unverified`, `shippable`, `goal-loop` - all in folder format
- `structured-reasoning` retired. Its Decision Priority and Stuck Protocol already live in
  `docs/GLOBAL_ROUTER_TEMPLATE.md`; its **Verification Hierarchy** was unique to it and has been
  relocated into `.claude/rules/quality-gate.md`, next to the Verification Language Rule it
  complements - the hierarchy ranks evidence, the rule governs claims
- `project-status` and `codebase-audit` retired as superseded by built-in commands and by
  `/paranoia` + `/unverified`
- `research-then-implement` moved to `docs/` - a reference pattern, not an invocable skill
- `test_hooks.py` 22 to 34 tests. Both new checks were fed a known-bad case and confirmed to fail
  before being trusted
- Added **The Enforcement Problem** - why prose instructions decay and what to do instead

### 2026-03-24 — Modular Architecture & Research-Backed Traps

Extracted universal standards into `.claude/rules/` for auto-loading, added 3 new research-backed traps, enriched principle lattice, added samples directory.

**Added:**
- `.claude/rules/coding-standards.md` — 8 coding standards extracted for auto-loading by Claude Code
- `.claude/rules/traps.md` — 13 behavioral traps (3 new: silent-dependency assumptions, stale-context anchoring, premature-abstraction) + anti-rationalization table
- `.claude/rules/quality-gate.md` — pre-submit verification checklist extracted for auto-loading
- `samples/` directory — filled-in examples from real projects showing what adapted files look like
- Modular architecture: CLAUDE.md for project-specific config, `.claude/rules/` for universal standards auto-loaded by Claude Code

**Improved:**
- `docs/PRINCIPLE_LATTICE.md` — added instantiation guidance and concrete examples for each axiom
- Trap count increased from 10 to 13 with research-backed additions

### 2026-03-24 — Session Transcendence & Publish Prep

Added 4 new hooks for full session lifecycle coverage, 2 new templates, and hardened behavioral traps.

**Added:**
- `pre-compact.py` — snapshots working state before context compaction (enables session transcendence)
- `session-end.py` — auto-persists working state on graceful exit
- `precommit-doc-check.py` — blocks commits missing documentation updates
- `_state_utils.py` — shared utilities for state management hooks
- `codebase-audit.md` skill — `/codebase-audit` systematic health check
- `ROLE_TEMPLATE.md` — template for role-based workflows (5 sections: domain expertise, traps, checks, patterns, boundaries)
- `GLOBAL_ROUTER_TEMPLATE.md` — thin CLAUDE.md router template for docs-heavy setups
- Trap 9 (retry loops) and Trap 10 (verification language) in CLAUDE.md
- Anti-rationalization self-check table in CLAUDE.md
- Verification Language Rule in quality gate
- MIT License

### 2026-03-23 — Audit & Fixes

Full harness review against CLAUDE.md source of truth and Claude Code hook documentation. Both hooks verified end-to-end in terminal.

**Fixed:**
- README counted "9 coding standards" and "9 traps" — actual count is 8 each
- Failure mode table cross-references pointed to wrong standard/trap numbers (#5→#4, #6→#5, #9+Trap#6→#8+Trap#8, Trap#5→Trap#4)
- 5 references to `SESSION_NOTES.md` (renamed to `WORKING_STATE.md` in the kit but README and `/project-status` skill still used the old name)
- `maintenance-check.py` markdown table had extra `|` in separator row, breaking rendering
- `test_hooks.py` used Unicode `→` arrow — crashes on Windows cp1252 terminals (`UnicodeEncodeError`)

**Verified:**
- `transcript_path` is confirmed in the Claude Code `Stop` hook stdin schema — maintenance-check.py receives it correctly
- Both hooks tested end-to-end: `session-start.py` outputs valid `additionalContext` JSON, `maintenance-check.py` correctly returns `"decision": "block"` when code files are modified
- All 10 smoke tests pass natively on Windows (no `PYTHONIOENCODING` workaround needed)

### 2026-03-17 — Initial Release

Starter kit extracted from [HiveMind](https://github.com/LucidPaths/HiveMind) `fix/audit-findings` branch. Includes CLAUDE.md, 2 hooks, 5 skills, principle lattice, and templates.

## Credits

- Principle lattice concept and hook patterns adapted from [vincitamore/claude-org-template](https://github.com/vincitamore/claude-org-template)
- Distilled from the [HIVE](https://github.com/LucidPaths/HiveMind) project by [LucidPaths](https://github.com/LucidPaths)
