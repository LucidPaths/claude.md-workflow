# Claude.md Workflow

A governance kit for AI-assisted development with [Claude Code](https://docs.anthropic.com/en/docs/claude-code).
Drop `claude-starter-kit/` into any repo to get deterministic session
orientation, an executable quality gate, git-level guardrails, and a small set
of behavioral rules that still earn their context cost on modern models.

Distilled from the [HIVE](https://github.com/LucidPaths/HiveMind) project.

## Design Principle (v2)

Every rule lives at the lowest enforceable layer:

```
prompt ritual → executable check → hook that verifies state → git hook that physically prevents
```

v1 of this kit enforced almost everything at the prompt layer — long rule
files, self-reported compliance, magic escape phrases. v2 rotates the stack:
instructions are kept short enough to never compete with project context, and
everything that *can* be checked deterministically *is* — the quality gate runs
commands, the doc reminder fires on observable git state, and hard don'ts live
in git hooks that no model can talk its way past.

## What's Inside

```
claude-starter-kit/
├── CLAUDE.md                      # Project facts, [ADAPT] sections, <60 lines
├── .claude/
│   ├── rules/core.md              # 6 standards + 5 traps + anti-rationalization, <100 lines
│   ├── settings.json              # Hook registration
│   ├── hooks/
│   │   ├── session-start.py       # Git orientation + working state injection
│   │   └── change-check.py        # One evidence-based doc reminder per session
│   └── skills/
│       ├── verify.md              # /verify — executable quality gate
│       ├── adversarial-review.md  # /adversarial-review — subagent-isolated 3-stage review
│       └── parallel-roadmap.md    # /parallel-roadmap — contract-driven parallel agents
├── guards/install-guards.sh       # Git-level hard don'ts (protected branches/paths)
├── templates/
│   ├── TASK_CONTRACT.md           # Per-task acceptance criteria + scope boundaries
│   └── WORKING_STATE.md           # Curated memory: Corrections, Insights, Deferred Ideas
├── samples/                       # Filled-in examples from a real 39K-line project
└── tests/test_hooks.py            # Smoke tests for hooks, guards, and structure
```

## Quick Start

1. Copy the contents of `claude-starter-kit/` into your repo root
2. Run `bash guards/install-guards.sh` once per clone
3. Commit and start a Claude Code session — on the first session, Claude
   fills in the `[ADAPT]` sections of CLAUDE.md from your actual codebase

## What Changed From v1 (and Why)

| v1 | v2 | Why |
|----|----|-----|
| 8 standards + 13 traps across 6 overlapping files | 6 standards + 5 traps in one file under 100 lines | Instruction volume is context tax; only rules that still change behavior on current models survived |
| Transcript-parsing "session transcendence" hooks (~400 lines of Python) | Deleted | Parsed a transcript schema that didn't match reality; native compaction handles continuity better |
| Stop hook unblocked by saying "No maintenance needed" | `change-check.py`: fires once per session, on git evidence, no magic phrase | A check satisfiable by saying something is not a check |
| Verification as a markdown checklist | `/verify` runs the project's actual commands and reports evidence | Make unverified claims impossible to submit, not just discouraged |
| 3-pass adversarial review role-played in one context | Subagent-isolated stages; skeptics see claims only | In one context, pass 2 anchors on pass 1 — isolation must be structural |
| "Never push to main" as a markdown rule | `guards/install-guards.sh` pre-push/pre-commit hooks | Models forget instructions; git hooks don't |
| "Agentic MapReduce" as a README diagram | `/parallel-roadmap` skill with contracts, worktree isolation, reduce phase | Implement it or cut it |
| Auto-written WORKING_STATE.md with path ambiguity (root vs `docs/`) | Curated-only, model-maintained, one canonical location (root) | Automation wrote worse notes than the model; two locations split the memory |

## Requirements

- **Python 3** — hooks (stdlib only)
- **Git + Bash** — orientation, change check, guards
- **Claude Code** — hooks and skills; the rules and templates work with any
  agent that reads project instruction files

## Verifying

```bash
python3 claude-starter-kit/tests/test_hooks.py
```

## Credits

- Hook patterns and lattice concept adapted from [vincitamore/claude-org-template](https://github.com/vincitamore/claude-org-template) (MIT)
- Distilled from the [HIVE](https://github.com/LucidPaths/HiveMind) project by [LucidPaths](https://github.com/LucidPaths)
- v1 history (including the fuller trap catalog, principle lattice template,
  and role/router templates) is preserved in git history prior to the v2 redesign
