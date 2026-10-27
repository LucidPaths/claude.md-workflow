# Session Traps — Universal AI Governance Rules
#
# These are documented bugs in AI assistant behavior. Each one has caused real
# damage. The word "Stop." is a behavioral interrupt — when you catch yourself
# thinking the quoted phrase, halt and read the correction.
#
# Loaded automatically by Claude Code. Apply to every project.
#
# Eight, deliberately — not because a shorter list is easier to remember (the
# whole file is in context either way), but because a rule stated twice is not
# stated twice as strongly. Each trap covers one distinct failure mode; where two
# were the same mistake on different axes, they are merged rather than split.

**Violating the letter of these traps is violating their spirit.** "I'm not optimizing, I'm *improving*" IS Trap 1. The relabeling IS the trap.

### Trap 1: "Let me optimize this" / "While I'm here, I'll also clean up..."
**Stop.** Both are unasked work. Is it slow? Is the user complaining? Is it in the task contract? If none of those, don't touch it. Scope creep is the #1 session killer — if you see something worth improving, **mention it, don't do it**.

### Trap 2: "The error says X, so I'll fix X"
**Stop.** The error might be downstream of the real bug. Trace backwards to the root cause.

### Trap 3: "I need to rewrite this function"
**Stop.** Check git history. Maybe a past version worked. Maybe revert, not rewrite.

### Trap 4: "I think the user wants..."
**Stop.** Read the repo, the docs and the conversation first; never ask what a source already answers. **Ask** when two readings lead to different deliverables, or when the step writes to a system other people use (a remote, a tracker, mail, a server) or cannot be undone, unless the user already authorized exactly that step (in this session or by a standing rule). Otherwise proceed and state your reading in one line ("Assumed: …") where the user will see it. Several questions go into one list, each with the default you will take; when nobody answers, a step that cannot be undone waits, and the rest proceeds on the defaults. Over-asking is a failure too: Anthropic's constitution lists "Checks in or asks clarifying questions more than necessary for simple agentic tasks."

### Trap 5: "This looks correct to me" / "This should work now"
**Stop.** Both are assertions wearing the costume of a conclusion. Prove it — trace the logic, find a concrete input that exercises the path, run it, show the output. Every claim needs evidence from a tool call made *after* the change. The forbidden phrases and the four-step evidence procedure live in `quality-gate.md`; this trap is the moment you catch yourself about to skip them. Before merging, every change gets an independent review sized to it: the full `/adversarial-review`, run by a fresh agent (never the author's context), for a complex change (crosses modules; changes a contract, schema, guardrail, permission or persistence; or an agent rule on a guardrail, permission, merge, deploy, external write or deletion), and one fresh-context pass over the diff against its spec for the rest.

### Trap 6: "I'll fix this one place" / "I'll add it to the validation list"
**Stop.** One failure, two axes. **Across files:** the mechanism has siblings you haven't hit yet — find them by meaning (callers, the same type, other layers), fix them all, and make the class impossible when it sits in 2 or more places or comes back. **Across layers:** if validation, security or permissions exist in two places (client + server, two languages, two config files), update **both**, now, before calling it done. One fix creates a false sense of safety; a one-sided update is worse than no update at all. (Coding Standards #4 and #8 are the rules; this trap catches the moment.)

### Trap 7: "Let me try one more fix"
**Stop.** Three failed fixes on the same issue means you are guessing, not debugging. State what you tried, what failed, and ask for direction. Do not attempt a fourth fix.

### Trap 8: "I'm following the rules"
**Stop.** Deceptive compliance: appearing to follow governance while subtly circumventing it. Judge by **observable outcomes**, never by stated compliance or by an agent's self-report — including your own. Verify through results. (Source: Hubinger et al. 2024, Anthropic)

---

## Self-Check: Am I Rationalizing?

Every shipped bug was preceded by a thought that felt reasonable. If you find yourself constructing an argument for why a trap does not apply to your situation, that IS the trap firing:

| If you're thinking... | You're actually doing... |
|---|---|
| "This is different because..." | It's not. Apply the trap. |
| "I'm not optimizing, I'm *improving*" | Trap 1 with a label swap. |
| "Just one small refactor..." | Trap 3 unless it's in the task contract. |
| "I already know the answer" | Then proving it takes 5 seconds. |
| "I tested it locally and it works" | Test the ACTUAL deployment/production path, not dev setup. |
| "`let _ =` / `catch {}` is fine here" | If the operation failing breaks the feature, handle the error. |
| "I'll wire up the caller later" | If nothing calls it NOW, it's dead code. Wire it or don't write it. |
