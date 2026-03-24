# Samples

Samples carry the teaching load — they show the pattern better than instructions can describe.

These examples are extracted from a real 39K-line Tauri desktop application (Rust + React/TypeScript) that has been actively developed with the claude.md-workflow methodology. They show what each file looks like when properly filled in — not generic placeholders, but real project content.

## Sample Files

| File | What It Demonstrates |
|------|---------------------|
| [CLAUDE-md-filled-example.md](CLAUDE-md-filled-example.md) | A condensed CLAUDE.md (~150 lines vs the original 918). Shows filled-in project overview, directory tree, development guidelines, cross-file contracts table, key files table, current state tracker, architecture patterns, session traps, and lessons learned. |
| [WORKING-STATE-filled-example.md](WORKING-STATE-filled-example.md) | A WORKING_STATE.md mid-project — active multi-phase task, conversation context with user intent, accumulated learnings, corrections (mistakes caught by user), self-improvement observations, deferred ideas, and codebase insights. |
| [PRINCIPLE-LATTICE-filled-example.md](PRINCIPLE-LATTICE-filled-example.md) | A principle lattice with 5 principles, each having 3-5 concrete instantiations proving the principle lives in code. Shows the pattern of axiom → instantiations → demands. |

## How to Use These

1. **Read the examples first** — understand the pattern before trying to fill in your own
2. **Notice the specificity** — entries reference real files, real commands, real bugs. Generic entries ("follow best practices") are useless
3. **Notice the honesty** — the Current State table has "MISSING" entries. The Corrections section documents real mistakes. The Traps section documents thoughts that preceded bugs
4. **Adapt the depth** — a 5K-line project needs less than a 39K-line project. Start with Project Overview, Key Directories, Common Tasks, and 2-3 Traps. Add more as the project grows

## Source

These examples are extracted and condensed from [HiveMind](https://github.com/LucidPaths/HiveMind), a Tauri v2 desktop app for AI orchestration. The original CLAUDE.md is 918 lines — these samples show the essential patterns without the project-specific depth.
