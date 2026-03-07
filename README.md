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
│   │   └── maintenance-check.py       # Blocks session end if docs not updated
│   └── skills/
│       ├── structured-reasoning.md    # Decision framework + priority hierarchy
│       ├── project-status.md          # /project-status — quick state overview
│       ├── research-then-implement.md # /research-decide — two-phase task pattern
│       └── adversarial-review.md      # /adversarial-review — 3-pass bug verification
└── docs/
    ├── PRINCIPLE_LATTICE.md           # 5 axiomatic design principles
    └── TASK_CONTRACT_TEMPLATE.md      # Per-task acceptance criteria template
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

- **9 coding standards** — simple solutions over complex ones, actionable error messages, no dead code, check git history before rewriting, fix ALL instances of a pattern, no cross-file string contracts without a shared source, User-Agent headers on API calls, closed-by-default security, dual-layer changes must update both sides
- **9 documented behavioral traps** — real failure modes with "Stop." interrupts (premature optimization, scope creep, single-instance fixes, sycophantic agreement, premature abstraction, etc.)
- **Cross-file contract tracking** — a table for tracking values that must stay in sync across files
- **`[ADAPT]` sections** — placeholders Claude fills in as it learns your specific project (overview, key directories, build commands, architecture patterns, gotchas)
- **Session continuity** — `SESSION_NOTES.md` pattern for handing off context between sessions

The adaptive design means the kit grows with your project instead of being static boilerplate.

### 3. Automation (the hooks)

Two lifecycle hooks registered in `.claude/settings.json`:

**Session Start** (`session-start.py`):
- Injects current branch, last 5 commits, uncommitted changes
- Pulls next steps from `ROADMAP.md` or `TODO.md` if they exist
- Claude starts every session oriented, not asking "what are we working on?"

**Session Stop** (`maintenance-check.py`):
- Detects if code files were modified during the session
- If yes, **blocks session end** until documentation is confirmed up-to-date
- Prevents documentation rot — the #1 cause of stale project context

### 4. Skills (the frameworks)

Four reusable decision patterns invoked as slash commands:

| Skill | Command | What It Does |
|-------|---------|--------------|
| **Structured Reasoning** | *(reference)* | Priority hierarchy (correctness > security > performance > maintainability > elegance), scope guard, stuck protocol, decomposition triggers |
| **Project Status** | `/project-status` | Quick state overview from ROADMAP, TODO, git log, uncommitted changes, and health checks |
| **Research Then Implement** | `/research-decide` | Two-phase pattern: research and write a decision file first, then implement with fresh context. Prevents context bloat from mixing exploration and coding |
| **Adversarial Review** | `/adversarial-review` | Three-pass code review: Pass 1 aggressively hunts bugs (overclaims), Pass 2 tries to disprove each finding (overclaims disprovals), Pass 3 adjudicates. The intersection is accurate. Exploits model sycophancy as a feature |

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
  → Standards enforced during work (9 coding standards, 9 trap interrupts)
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
| Scope creep ("while I'm here, I'll also...") | Trap #5 + scope guard in structured-reasoning |
| Sycophantic code review ("this looks correct") | Adversarial 3-pass review exploits the bias |
| Context bloat from mixing research and coding | research-then-implement separates phases |
| Single-instance fix creates false safety | Coding Standard #5: fix ALL instances or none |
| Cross-file values drift silently | Cross-file contracts table + Coding Standard #6 |
| Vague acceptance criteria, gold-plating | Task contract template with explicit done conditions |
| Two-layer validation updated on one side only | Coding Standard #9 + Trap #6 |

## Benefits for Claude

1. **Immediate orientation** — no wasted turns asking "what are we working on?"
2. **Behavioral guardrails** — the 9 traps catch real failure patterns before they cause damage
3. **Explicit done conditions** — task contracts prevent both under-delivery and over-engineering
4. **Structured decision-making** — priority hierarchy and research-then-implement prevent flailing
5. **Session continuity** — `SESSION_NOTES.md` bridges context between sessions

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

## Requirements

- **Python 3** — for session hooks (stdlib only, no pip packages)
- **Git** — for orientation and maintenance checks
- **Claude Code** — the CLI tool this kit is designed for

## Credits

- Principle lattice concept and hook patterns adapted from [vincitamore/claude-org-template](https://github.com/vincitamore/claude-org-template)
- Distilled from the [HIVE](https://github.com/LucidPaths/HiveMind) project by [LucidPaths](https://github.com/LucidPaths)
