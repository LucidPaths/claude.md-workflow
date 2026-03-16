# Working State Template

Copy this file to `WORKING_STATE.md` in the project root to enable session-transcending continuity. The AI assistant maintains this file across sessions — it's a working memory that survives context limits, session breaks, and model switches.

---

```markdown
# Working State
Last updated: [timestamp]

## Active Task
[What you're currently working on. Clear this when done.]

Task: [one-line description]
Branch: [git branch]
Started: [date]

### Current step
[What you're doing RIGHT NOW — specific enough to resume cold]

### Completed
- [Step — result]

### Remaining
- [Next step]

### Uncommitted work
[Modified files not yet committed/pushed. ALWAYS track this.]

---

## Conversation Context
[What's the current conversation about? What's the user's intent beyond
the literal request? What open questions exist?]

- Topic: [what we're discussing]
- User intent: [the bigger picture behind current requests]
- Open threads: [things mentioned but not yet addressed]

---

## Learnings
[Things discovered THIS SESSION that aren't documented anywhere.
Codebase behaviors, gotchas, undocumented patterns, surprising findings.
These are candidates for CLAUDE.md if they prove stable.]

- [date] [learning]

---

## Corrections
[Things the user corrected you on. These are mistakes you made and
must not repeat. Be specific — include what you did wrong and what
the right approach is.]

- [date] [what you got wrong → what's actually correct]

---

## Self-Improvement
[Meta-observations about your own work patterns. What approaches
were efficient? Where did you waste time? What broke a loop when
you were stuck? What should you do differently next time?]

- [date] [observation]

---

## Deferred Ideas
[Ideas, improvements, or observations that came up during work but
aren't actionable right now. A parking lot for future sessions.]

- [idea — context for why it matters]

---

## Codebase Insights
[Undocumented knowledge about this specific codebase. Things you
learned by reading code that aren't in any docs. File relationships,
implicit contracts, behavioral quirks.]

- [insight]
```

---

## Why Each Section Exists

| Section | Purpose | Lifespan |
|---------|---------|----------|
| Active Task | Resume work cold after a break | Ephemeral — cleared when task completes |
| Conversation Context | Understand the user's broader intent | Ephemeral — overwritten each session |
| Learnings | Capture undocumented codebase knowledge | Accumulates — promote to CLAUDE.md, then remove |
| Corrections | Never repeat the same mistake | Accumulates — the highest-value entries |
| Self-Improvement | Get better at being useful | Accumulates — prune when internalized |
| Deferred Ideas | Parking lot for good ideas at bad times | Accumulates — delete when irrelevant |
| Codebase Insights | Knowledge that only exists by reading code | Accumulates — promote to docs, then remove |

## Key Rules

1. **Corrections are sacred.** When the user corrects you, write it down immediately. Never argue, never rationalize — just record what was wrong and what's right.
2. **Track uncommitted work.** The "20 fixes sitting on disk unpushed" situation must never happen. If 5+ files are modified without a commit, note it prominently.
3. **Prune aggressively.** If a learning gets promoted to CLAUDE.md, remove it. If a deferred idea becomes irrelevant, delete it. Keep this file under ~200 lines.
4. **Be honest in Self-Improvement.** "I went in circles for 20 minutes because I didn't read the file first" is more useful than "consider reading files before editing."
