# Claude Starter Kit (v2)

A portable folder you drop into any repo to bootstrap auditable AI-assisted
development. Rules stay short; enforcement is deterministic.

## Quick Start

1. **Copy** the contents of this folder into your repo root
2. **Install guards:** `bash guards/install-guards.sh` (once per clone)
3. **Commit** and start a Claude Code session — the first session fills in the
   `[ADAPT]` sections of CLAUDE.md from your actual codebase

## Contents

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project facts only — overview, directories, verify commands, contracts, lessons. All `[ADAPT]` sections |
| `.claude/rules/core.md` | The universal rules: 6 standards, 5 traps, anti-rationalization table, 5 principles. Auto-loaded, under 100 lines |
| `.claude/hooks/session-start.py` | Injects branch, commits, uncommitted changes, WORKING_STATE.md, and roadmap next-steps at session start |
| `.claude/hooks/change-check.py` | Stop hook: if code changed but no doc was touched, delivers one evidence-based reminder per session. No magic phrases, no nag loop |
| `.claude/skills/verify.md` | `/verify` — runs the project's real build/test/lint/typecheck commands; completion claims require their output |
| `.claude/skills/adversarial-review.md` | `/adversarial-review` — parallel finder subagents → claim-only skeptic subagents → adjudication. Isolation is structural |
| `.claude/skills/parallel-roadmap.md` | `/parallel-roadmap` — fan roadmap items out to contract-bound worktree agents, reduce with review + contract-drift check |
| `guards/install-guards.sh` | Git-level hard don'ts: pre-push (protected branches), pre-commit (protected paths). Human-only override via env vars |
| `templates/TASK_CONTRACT.md` | Per-task objective, checkable acceptance criteria, protected files, scope boundaries |
| `templates/WORKING_STATE.md` | Curated memory (Corrections / Codebase Insights / Deferred Ideas), maintained by the model, lives in project root |
| `samples/` | Filled-in examples from a real 39K-line project — the fastest way to see what "properly adapted" looks like |
| `tests/test_hooks.py` | Smoke tests: hooks parse and run, settings references resolve, guards script is valid bash, structure is intact |

## The Division of Labor

- **Prompts** carry only what must be judgment: the 5 traps, scope discipline,
  the anti-rationalization table.
- **Hooks** check observable state: git orientation in, evidence-based doc
  reminder out.
- **Skills** make verification and review executable processes, not vibes.
- **Git hooks** hold the hard don'ts. A rule a model can forget is a
  suggestion; a pre-push hook is a rule.

## Verifying

```bash
python3 tests/test_hooks.py
```

## Credits

Hook patterns adapted from [vincitamore/claude-org-template](https://github.com/vincitamore/claude-org-template) (MIT).
Distilled from the [HIVE](https://github.com/LucidPaths/HiveMind) project by LucidPaths.
