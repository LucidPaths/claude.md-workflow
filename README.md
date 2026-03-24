# Claude.md Workflow

A governance framework for AI-assisted development with [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Drop it into any repo to turn Claude from a raw coding assistant into a disciplined, self-auditing development agent.

Distilled from battle-tested patterns in the [HIVE](https://github.com/LucidPaths/HiveMind) project.

---

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
│   ├── hooks/
│   │   ├── session-start.py           # Auto-injects git state at session start
│   │   ├── maintenance-check.py       # Blocks session end if docs not updated
│   │   ├── pre-compact.py             # Snapshots state before context compaction
│   │   ├── session-end.py             # Auto-persists working state on exit
│   │   ├── precommit-doc-check.py     # Blocks commits missing doc updates
│   │   └── _state_utils.py            # Shared utilities for state hooks
│   └── skills/
│       ├── structured-reasoning.md    # Decision framework + priority hierarchy
│       ├── project-status.md          # /project-status — quick state overview
│       ├── research-then-implement.md # /research-decide — two-phase task pattern
│       ├── adversarial-review.md      # /adversarial-review — 3-pass bug verification
│       └── codebase-audit.md          # /codebase-audit — systematic health check
└── docs/
    ├── PRINCIPLE_LATTICE.md           # 5 axiomatic design principles
    ├── TASK_CONTRACT_TEMPLATE.md      # Per-task acceptance criteria template
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

- **8 coding standards** — simple solutions over complex ones, actionable error messages, no dead code, fix ALL instances of a pattern, single source of truth for cross-file contracts, User-Agent headers on API calls, closed-by-default security, update both sides of a boundary
- **10 documented behavioral traps** — real failure modes with "Stop." interrupts (premature optimization, scope creep, single-instance fixes, sycophantic agreement, retry loops, verification language, etc.) plus an anti-rationalization table
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

### 4. Skills (the frameworks)

Five reusable decision patterns invoked as slash commands:

| Skill | Command | What It Does |
|-------|---------|--------------|
| **Structured Reasoning** | *(reference)* | Priority hierarchy (correctness > security > performance > maintainability > elegance), scope guard, stuck protocol, decomposition triggers |
| **Project Status** | `/project-status` | Quick state overview from ROADMAP, TODO, git log, uncommitted changes, and health checks |
| **Research Then Implement** | `/research-decide` | Two-phase pattern: research and write a decision file first, then implement with fresh context. Prevents context bloat from mixing exploration and coding |
| **Adversarial Review** | `/adversarial-review` | Three-pass code review: Pass 1 aggressively hunts bugs (overclaims), Pass 2 tries to disprove each finding (overclaims disprovals), Pass 3 adjudicates. The intersection is accurate. Exploits model sycophancy as a feature |
| **Codebase Audit** | `/codebase-audit` | Systematic health check: silent failures, dead code, contract drift, security gaps. Produces actionable findings, not vague warnings |

## How It Works

```
1. Drop claude-starter-kit/ contents into your repo root
2. Commit so Claude Code picks up the files
3. Start a Claude Code session

First session:
  → session-start.py injects git state + next steps
  → Claude reads CLAUDE.md, fills in [ADAPT] sections
  → Future sessions build on that foundation

Every session:
  → Orientation at start (branch, commits, changes, next steps)
  → Standards enforced during work (8 coding standards, 10 trap interrupts)
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
| Scope creep ("while I'm here, I'll also...") | Trap #4 + scope guard in structured-reasoning |
| Sycophantic code review ("this looks correct") | Adversarial 3-pass review exploits the bias |
| Context bloat from mixing research and coding | research-then-implement separates phases |
| Single-instance fix creates false safety | Coding Standard #4: fix ALL instances or none |
| Cross-file values drift silently | Cross-file contracts table + Coding Standard #5 |
| Vague acceptance criteria, gold-plating | Task contract template with explicit done conditions |
| Two-layer validation updated on one side only | Coding Standard #8 + Trap #8 |

## Benefits for Claude

1. **Immediate orientation** — no wasted turns asking "what are we working on?"
2. **Behavioral guardrails** — the 10 traps + anti-rationalization catch real failure patterns before they cause damage
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

### Mitigations

**For weaker models (Haiku-class, smaller open-source):**
- **Reduce CLAUDE.md scope** — 8 standards + 10 traps is too much for smaller context windows. Pick the 3-4 most critical for your project and cut the rest
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

This applies to all models, all tiers, all context lengths. It's not a weakness of small models — it's a property of LLMs that surfaces more often under load.

## Requirements

- **Python 3** — for session hooks (stdlib only, no pip packages)
- **Git** — for orientation and maintenance checks
- **Claude Code** — the CLI tool this kit is designed for

## Changelog

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
