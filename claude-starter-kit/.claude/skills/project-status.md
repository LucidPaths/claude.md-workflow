# /project-status — Quick Project State Overview

Show the current state of the project at a glance.

## Instructions

When this skill is invoked, do the following:

1. **Project State** — Check for these files and report relevant sections:
   - `ROADMAP.md` — what's done, what's next
   - `TODO.md` — outstanding tasks
   - `CHANGELOG.md` — recent changes
   - `WORKING_STATE.md` — continuity notes from last session

2. **Git State** — Run these commands and report results:
   - `git log --oneline -10` — recent activity
   - `git status --short` — uncommitted work
   - `git branch --show-current` — current branch

3. **Health Check** — Quick verification:
   - Are there uncommitted changes that should be committed?
   - Is the branch behind origin/main?
   - Are there any TODO/FIXME comments in recently modified files?

Present results concisely. Focus on actionable info: what's done, what's blocked, what's next, what's in progress right now.
