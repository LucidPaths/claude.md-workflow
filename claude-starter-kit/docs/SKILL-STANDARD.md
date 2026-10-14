# Skill standard

A skill is a procedure an agent follows with nobody to ask what the author meant. This standard makes every decision
in it checkable: by the agent while it runs, by the user reading its output, and by `tests/skill_lint.py` before the
skill ships.

---

## 1. Every decision rule is one of three kinds

| Kind | Shape | Example |
|---|---|---|
| **DETERMINISTIC** | an observable signal, a threshold, the action, and a one-clause reason | "A slice reached 3 review rounds without converging → stop reviewing and re-examine the design (a fourth round repeats the third)." |
| **DEFAULT** | `DEFAULT <name> = <value>`: a named value the user may change, stated once and used by its name | `DEFAULT retire_at = 60 % of the context window` |
| **ASK** | `ASK <when>: "<question>"`, then what the agent does with each answer | `ASK when two skills claim the same phase: "Run A (plans) or B (builds)?" → A: plan only / B: build from the given plan` |

There is no fourth kind. A decision that cannot be written as DETERMINISTIC or DEFAULT is an ASK: the judgment goes to
the user, as a question with a fixed shape and a fixed consequence for each answer.

- **Observable** means a second agent could check the signal from the output, a file, a command result or a count,
  without asking the first agent what it thought.
- **ASK with nobody to answer.** A skill can run where no user is reachable: inside a subagent, in a scheduled job. There
  an ASK halts that one decision. The agent reports the question, the options and its evidence to whoever dispatched
  it, and never picks an answer itself; work that does not depend on the answer continues.

## 2. Terms banned in a decision rule

These terms leave a decision to feel. They are allowed in explanation (section 3 says where explanation is).

| Term | Write instead |
|---|---|
| `about N`, `around N`, `roughly`, `approximately`, `~N`, `or so` | the number, as a threshold or a DEFAULT |
| `usually`, `typically`, `generally`, `often`, `sometimes`, `probably` | the signal that decides, or an ASK |
| `a few`, `several`, `a handful`, `a lot` | a number |
| `if needed`, `as needed`, `if necessary`, `as appropriate`, `where sensible`, `when it makes sense`, `consider`, `reasonable`, `use judgment`, `judgment call`, `that matters` | the observable condition, or an ASK |
| `large/small without a number` (also big, huge, tiny, long-lived, long-running, trivial, non-trivial, significant, substantial, on a line that carries no number) | the threshold that defines the size |

The lint carries this list term for term, and `tests/test_skill_lint.py` fails when the two lists drift apart. The list
is a floor, not the definition: a rule that leaves a decision to feel breaks this standard whether or not it uses a
listed word.

## 3. Where the rules are, and where explanation is

Every line of `SKILL.md` below the frontmatter is a decision-rule line, except in these explanation zones:

- a section whose nearest heading starts with Origin, Why, Where this came from, Background, Example or Worked example;
- a paragraph or list item whose first word is `Origin:`, `Why:`, `Background:` or `Example:`;
- blockquotes, fenced code blocks, and text inside double quotes, curly quotes or backticks (quoted examples);
- the Seen column of a failure-modes table.

A **block** is one table row, one list item with its continuation lines, or one paragraph. Files a skill reads (a
reference sheet, a template) are its data; the rules live in `SKILL.md`.

## 4. Structure

1. **Frontmatter** with `name` and `description`. The description is a trigger condition ("Use when the user runs X or
   asks Y"), and it says when not to use the skill.
2. **Purpose** in at most two lines under the title.
3. **When to use and when not**, in a section when the description cannot hold both.
4. **Procedure**: numbered, imperative steps.
5. **Decision rules** inside the step they govern; a step that carries 3 or more puts them in a table.
6. **Closing block**: a heading `## Closing block (required)` with a fenced template of labelled lines the agent fills
   in at the end. A skipped block is visible in the output; a skipped intention is not.
7. **Failure modes**: a table `| Seen | Rule |`, each row an observed failure and the rule that now prevents it.

## 5. Standalone defaults and composition

A skill never depends on another skill to work. Where it would point to another skill for a rule, it carries the
smallest working version of that rule in the same block as the reference, and names the other skill as an optional
upgrade:

> Standalone default: run the full suite once on the final commit. If `/fleet-economics` is installed, it replaces this
> default.

- The full rule keeps one canonical home, the companion skill. The standalone default is the floor that keeps this skill
  working alone, never a second copy of the full rule.
- A mention that only routes (this skill does not do X; X is another skill's job) goes in the frontmatter description
  or in a "When not to use" section, and needs no default.
- A skill names only skills that exist in its own set; a reference to a skill that is not shipped is a defect.

## 6. Agent-agnostic wording

- Capability tiers, not model names: fast, balanced, flagship, strongest. Which model sits in which tier is discovered
  at run time.
- "A fresh subagent", "the subagent tool", "the skill, if installed": never one harness's internal tool names alone.
- Harness-specific syntax (a slash command, an effort flag, a tool name) only with a plain-words fallback beside it.

## 7. Size

- One job per skill. A second job is a second skill.
- Every sentence changes behaviour or carries the reason for a rule. History goes under an Origin heading or label and
  is kept to the incident and the rule it produced.

## 8. The lint

```bash
python claude-starter-kit/tests/skill_lint.py                          # the kit's skills
python claude-starter-kit/tests/skill_lint.py --skills-dir ~/.claude/skills   # any folder of skill folders
python -m unittest discover -s claude-starter-kit/tests                # the lint's own tests, with planted defects
```

It fails on four things, each with its file and line: a `SKILL.md` without `name` and `description` in its
frontmatter; no closing block; a banned term in a decision-rule line; a reference to another skill without a standalone
default in its block, or to a skill that is not a folder in the same set. Harness commands such as `/compact` or
`/effort` are not skills and are not checked. What the lint cannot judge (whether a rule without a banned word still
leaves the decision to feel) stays with the reviewer.
