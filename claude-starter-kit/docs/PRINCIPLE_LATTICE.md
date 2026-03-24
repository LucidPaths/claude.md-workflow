# Principle Lattice

**Five axioms. Every design decision checks against them.**

When stuck between two approaches, score them against the lattice. If one cleanly honors more principles without violating any, it wins. If both violate something, find a third approach.

### How to Write Good Instantiations

Instantiations are the bridge between abstract principles and daily decisions. They're what make the lattice *yours* instead of generic advice.

- **Write instantiations across domains:** code, infrastructure, process, communication
- **Each principle should have 3-8 concrete instantiations** — enough to show the pattern, not so many they become a checklist
- **Instantiations should be SPECIFIC and OPINIONATED, not generic truisms** — "use good variable names" is useless; "domain objects use ubiquitous language from the glossary" is useful
- **The compression test:** can one principle derive another? If yes, merge them. Five sharp principles beat ten fuzzy ones.

---

## 1. Modularity

> *Lego blocks, not monoliths.*

Every component should be self-contained. Pull one out — that thing stops working, the rest stands. When two systems need to talk, build a bridge — don't duplicate. If data already lives somewhere, reference it.

**The test:** Can you remove this component without breaking something unrelated?

**Instantiations:**
- API routes are independent — auth failing doesn't break health checks
<!-- [ADAPT] Add 2-7 more instantiations across domains. Think:
     - Code: how are your modules/packages/services separated?
     - Infrastructure: can you deploy one service without redeploying all?
     - Process: can one team's workflow change without blocking others?
     - Communication: are docs self-contained or do they require tribal knowledge?
-->

---

## 2. Simplicity Wins

> *Don't reinvent the wheel. Code exists to be used.*

The best code is code someone else already debugged. Complexity is a cost, not a feature. Three clear lines beat one clever abstraction. A working simple solution beats an elegant broken one.

**The test:** Is there a simpler approach that already works? Would three explicit lines beat this abstraction?

**Instantiations:**
- Using Zod/Pydantic for validation instead of hand-rolled checks
<!-- [ADAPT] Add 2-7 more instantiations across domains. Think:
     - Code: where do you use libraries instead of rolling your own?
     - Infrastructure: managed services over self-hosted where possible?
     - Process: one-step commands over multi-step procedures?
     - Communication: READMEs with copy-paste examples over lengthy docs?
-->

---

## 3. Errors Are Answers

> *Every failure teaches. Errors must be actionable.*

An error that says "something went wrong" is itself a bug. Every error says what happened, why, and what to do. No silent failures — if something goes wrong, someone knows.

**The test:** If this operation fails, would the developer (or user) know what happened and what to do?

**Instantiations:**
- API errors include HTTP status + response body + suggested fix
<!-- [ADAPT] Add 2-7 more instantiations across domains. Think:
     - Code: do error messages include what was expected vs. what was received?
     - Infrastructure: do health checks report WHY they failed, not just that they did?
     - Process: do CI failures link to the relevant log section?
     - Communication: do error docs include the fix, not just the symptom?
-->

---

## 4. Fix The Pattern

> *Cure the root cause. Don't treat symptoms.*

When you find a bug, the bug is never alone. The same mistake exists in 3-5 other places. Search for the pattern, fix every instance. If a design keeps producing the same class of bug, the design is wrong — not the individual bugs.

**The test:** Did you grep for the same mistake elsewhere? Did you fix all instances?

**Instantiations:**
- Found missing null check — grepped all `.property` accesses, fixed 4 more
<!-- [ADAPT] Add 2-7 more instantiations across domains. Think:
     - Code: when you fix a bug, do you search for the same class of bug?
     - Infrastructure: when a config issue hits one service, do you check all services?
     - Process: when a process fails, do you fix the process or just the output?
     - Communication: when a doc is wrong, do you check related docs for the same error?
-->

---

## 5. Secrets Stay Secret

> *Nothing left open to exploitation.*

API keys belong in environment variables or encrypted storage — never in localStorage, never in plaintext, never logged, never in error messages. Security is not a feature you add later. It's a property of every line of code.

**The test:** Could a log message, error output, or config file leak something sensitive?

**Instantiations:**
- API keys in `.env`, never committed (`.gitignore` enforced)
<!-- [ADAPT] Add 2-7 more instantiations across domains. Think:
     - Code: are secrets filtered from logs and error messages?
     - Infrastructure: are credentials rotated? stored in vault/secrets manager?
     - Process: can a new developer onboard without anyone sharing passwords in Slack?
     - Communication: do screenshots in docs have credentials redacted?
-->

---

## Using The Lattice

### For Decisions

| Approach A | Approach B |
|-----------|-----------|
| Violates #1 (couples two modules) | Honors #1 (clean separation) |
| Honors #2 (simpler) | Violates #2 (complex) |
| **Mixed — find a third option** | **Mixed — find a third option** |

### For Code Review

Every PR: *does this change violate any principle?* Not "is this code clean" (subjective) — "does this violate the lattice" (answerable).

### For Active Enforcement

The lattice only works if you check it actively. On every change, ask each principle explicitly: Modular? Simple? Errors visible? Pattern fixed everywhere? Secrets safe? If you treat it as a checkbox to skim past, it becomes wallpaper. If you treat it as a real constraint, it catches real bugs.

---

## Adding Your Own Principles

Not every team needs exactly these five. Add a principle when:

1. **You care about the same thing in different contexts** — it keeps coming up in code review, architecture discussions, incident retros
2. **A decision feels obviously right but you can't say why** — that's an unarticulated principle waiting to be named
3. **You disagree with conventional wisdom and can articulate why** — "we don't do X because Y" is a principle worth writing down

Before adding, apply the **compression test**: can the new principle be derived from an existing one? If "Don't Repeat Yourself" is just a special case of your "Modularity" principle, don't add it — add an instantiation under Modularity instead. Five sharp principles beat ten fuzzy ones.

---

*Lattice concept adapted from [vincitamore/claude-org-template](https://github.com/vincitamore/claude-org-template). Principles distilled from the [HIVE](https://github.com/LucidPaths/HiveMind) project.*
