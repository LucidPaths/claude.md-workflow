#!/usr/bin/env python3
"""Skill lint: checks a folder of skills against docs/SKILL-STANDARD.md.

Usage:
  python skill_lint.py [--skills-dir DIR]

DIR defaults to the kit's .claude/skills; point it at any folder of skill folders
(for example ~/.claude/skills) to lint your own set. Prints one line per finding,
exits 1 when there is any and 0 when the folder is clean. Four checks, on each
skill's SKILL.md:

  frontmatter  SKILL.md is missing, or its frontmatter lacks name or description
  closing      no "Closing block" heading with a fenced template under it
  vague        a decision-rule line carries a banned vague term outside a quoted span
  reference    a reference to another skill has no standalone default in its block,
               or names a skill that is not a folder in DIR

What counts as a decision-rule line, an explanation zone and a block is defined in
SKILL-STANDARD.md section 3; the banned terms are its table in section 2, and
tests/test_skill_lint.py fails when that table and BANNED below drift apart.
"""
import argparse
import os
import re
import sys

KIT_SKILLS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".claude", "skills")

I = re.IGNORECASE
NUM_WORDS = r"(\d|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|thirty|forty|" \
            r"fifty|sixty|hundred|half|a hundred|a dozen|a third|a quarter)\b"

# (term exactly as SKILL-STANDARD.md lists it, regex). Order follows the standard's table.
BANNED = [
    ("about N", re.compile(r"\babout\s+" + NUM_WORDS, I)),
    ("around N", re.compile(r"\baround\s+" + NUM_WORDS, I)),
    ("roughly", re.compile(r"\broughly\b", I)),
    ("approximately", re.compile(r"\bapproximately\b", I)),
    ("~N", re.compile(r"(?<![\w~])~\s?\d")),
    ("or so", re.compile(r"\bor so\b", I)),
    ("usually", re.compile(r"\busually\b", I)),
    ("typically", re.compile(r"\btypically\b", I)),
    ("generally", re.compile(r"\bgenerally\b", I)),
    ("often", re.compile(r"(?<!\bhow )\boften\b", I)),
    ("sometimes", re.compile(r"\bsometimes\b", I)),
    ("probably", re.compile(r"\bprobably\b", I)),
    ("a few", re.compile(r"\ba few\b", I)),
    ("several", re.compile(r"\bseveral\b", I)),
    ("a handful", re.compile(r"\ba handful\b", I)),
    ("a lot", re.compile(r"\ba lot\b", I)),
    ("if needed", re.compile(r"\bif needed\b", I)),
    ("as needed", re.compile(r"\bas needed\b", I)),
    ("if necessary", re.compile(r"\bif necessary\b", I)),
    ("as appropriate", re.compile(r"\bas appropriate\b", I)),
    ("where sensible", re.compile(r"\b(where|when|if) sensible\b", I)),
    ("when it makes sense", re.compile(r"\bwhen it makes sense\b", I)),
    ("consider", re.compile(r"\bconsider\b", I)),
    ("reasonable", re.compile(r"\breasonabl[ey]\b", I)),
    ("use judgment", re.compile(r"\b(use|using|with|by)\s+(your\s+|plain\s+|good\s+|own\s+)?judge?ment\b", I)),
    ("judgment call", re.compile(r"\bjudge?ment[ -](call|heavy)\b", I)),
    ("that matters", re.compile(r"\b(that|when it|where it|if it) matters\b", I)),
]
# Size words count as vague only on a line that carries no digit.
SIZE_TERM = "large/small without a number"
SIZE = re.compile(r"\b(large|small|big|huge|tiny|long-lived|long-running|non-trivial|trivial|significant|"
                  r"substantial)\b", I)

# Harness commands that are not skills: a slash reference to one of these is not a skill reference.
HARNESS_COMMANDS = {"effort", "compact", "clear", "code-review", "init", "model", "loop", "schedule", "resume",
                    "help", "config"}

# Explanation zones: a section whose nearest heading starts with one of these words, or a block
# whose first word is one of these labels followed by a colon.
EXPLANATION_HEADINGS = ("origin", "why", "where this came from", "background", "example", "worked example")
EXPLANATION_LABEL = re.compile(r"^\s*(?:[-*+]|\d+[a-z]?[.)])?\s*(?:\*\*)?(origin|why|background|example)s?:", I)
# Sections in which a routing-only mention of another skill needs no standalone default.
ROUTING_HEADINGS = ("when not to use",)

QUOTED = [re.compile(r'"[^"\n]*"'), re.compile("“[^”\n]*”"), re.compile(r"`[^`\n]*`")]
BACKTICK = re.compile(r"`([^`\n]*)`")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
LIST_ITEM = re.compile(r"^\s*([-*+]|\d+[a-z]?[.)])\s+")
SPAN_REF = re.compile(r"^/([a-z][a-z0-9-]*)(?:\s|$)")
TEXT_REF = re.compile(r"(?:^|(?<=[\s(\[*]))/([a-z][a-z0-9-]*)(?![\w/-])")
THE_SKILL = re.compile(r"\bthe\s+`?/?([a-z][a-z0-9-]*)`?\s+skill\b", I)


def strip_quoted(text):
    for rx in QUOTED:
        text = rx.sub(" ", text)
    return text


def split_frontmatter(lines):
    """Return (frontmatter lines, index of the first body line), or (None, 0) without frontmatter."""
    if not lines or lines[0].strip() != "---":
        return None, 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], i + 1
    return None, 0


def body(lines, start):
    """Yield (line_no, line, section, in_code, block_id) for every non-blank body line.

    A block is one table row, one list item with its continuation lines, or one paragraph.
    """
    in_code, section, block, prev_blank = False, "", 0, True
    for idx in range(start, len(lines)):
        line, s = lines[idx], lines[idx].strip()
        if s.startswith("```"):
            in_code = not in_code
            block += 1
            yield idx + 1, line, section, True, block
            prev_blank = False
            continue
        if in_code:
            yield idx + 1, line, section, True, block
            continue
        m = HEADING.match(line)
        if m:
            section = m.group(2).strip().lower()
            block += 1
            yield idx + 1, line, section, False, block
            prev_blank = True
            continue
        if not s:
            prev_blank = True
            continue
        if s.startswith("|") or LIST_ITEM.match(line) or prev_blank:
            block += 1
        prev_blank = False
        yield idx + 1, line, section, False, block


def check_frontmatter(skill, lines):
    fm, _ = split_frontmatter(lines)
    if fm is None:
        return [f"{skill}/SKILL.md:1: frontmatter: no '---' frontmatter block at the top"]
    return [f"{skill}/SKILL.md:1: frontmatter: '{key}' missing or empty"
            for key in ("name", "description") if not any(re.match(rf"^{key}:\s*\S", l) for l in fm)]


def check_closing(skill, lines, start):
    level = None
    for l in lines[start:]:
        m = HEADING.match(l)
        if m and m.group(2).strip().lower().startswith("closing block") and len(m.group(1)) in (2, 3):
            level = len(m.group(1))
            continue
        if level is not None:
            if m and len(m.group(1)) <= level:
                level = None
            elif l.strip().startswith("```"):
                return []
    return [f"{skill}/SKILL.md:0: closing: no '## Closing block' heading with a fenced template under it"]


def check_vague(skill, lines, start):
    out, rows = [], list(body(lines, start))
    first = {}
    for n, line, section, in_code, b in rows:
        first.setdefault(b, line)
    seen_table = False
    for n, line, section, in_code, b in rows:
        s = line.strip()
        if not s.startswith("|"):
            seen_table = False
        if (in_code or HEADING.match(line) or s.startswith(">")
                or any(section.startswith(h) for h in EXPLANATION_HEADINGS) or EXPLANATION_LABEL.match(first[b])):
            continue
        text = line
        if s.startswith("|"):
            cells = s.strip("|").split("|")
            if cells and cells[0].strip().lower() == "seen":
                seen_table = True
            if seen_table:
                text = "|".join(cells[1:])
        text = strip_quoted(text)
        for term, rx in BANNED:
            m = rx.search(text)
            if m:
                out.append(f"{skill}/SKILL.md:{n}: vague: '{m.group(0)}' ({term}) | {s[:100]}")
        if not re.search(r"\d", text):
            m = SIZE.search(text)
            if m:
                out.append(f"{skill}/SKILL.md:{n}: vague: '{m.group(0)}' ({SIZE_TERM}) | {s[:100]}")
    return out


def references_in(line, skill, names):
    refs = set()
    for m in BACKTICK.finditer(line):
        r = SPAN_REF.match(m.group(1))
        if r:
            refs.add(r.group(1))
        elif m.group(1).strip() in names:
            refs.add(m.group(1).strip())
    for m in TEXT_REF.finditer(BACKTICK.sub("\x00", line)):
        refs.add(m.group(1))
    for m in THE_SKILL.finditer(line):
        if m.group(1).lower() in names:
            refs.add(m.group(1).lower())
    for k in names:
        if "-" in k and re.search(rf"(?<![\w/-]){re.escape(k)}(?![\w-])", line):
            refs.add(k)
    refs.discard(skill)
    return refs - HARNESS_COMMANDS


def check_references(skill, lines, start, names):
    out, rows = [], list(body(lines, start))
    text = {}
    for n, line, section, in_code, b in rows:
        text.setdefault(b, []).append(line)
    for n, line, section, in_code, b in rows:
        if HEADING.match(line) or any(section.startswith(h) for h in ROUTING_HEADINGS):
            continue
        has_default = "standalone default" in " ".join(text[b]).lower()
        for r in sorted(references_in(line, skill, names)):
            if r not in names:
                out.append(f"{skill}/SKILL.md:{n}: reference: '/{r}' is not a skill in this folder | {line.strip()[:100]}")
            elif not has_default:
                out.append(f"{skill}/SKILL.md:{n}: reference: '/{r}' has no standalone default in its block | "
                           f"{line.strip()[:100]}")
    return out


def lint(skills_dir):
    names = set(d for d in os.listdir(skills_dir)
                if os.path.isdir(os.path.join(skills_dir, d)) and not d.startswith((".", "_")))
    findings = []
    for skill in sorted(names):
        path = os.path.join(skills_dir, skill, "SKILL.md")
        if not os.path.isfile(path):
            findings.append(f"{skill}/SKILL.md:0: frontmatter: SKILL.md missing")
            continue
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        _, start = split_frontmatter(lines)
        findings += check_frontmatter(skill, lines)
        findings += check_closing(skill, lines, start)
        findings += check_vague(skill, lines, start)
        findings += check_references(skill, lines, start, names)
    return findings, len(names)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Lint a folder of skills against SKILL-STANDARD.md.")
    ap.add_argument("--skills-dir", default=KIT_SKILLS, help="folder that holds one folder per skill")
    a = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    if not os.path.isdir(a.skills_dir):
        print(f"skill_lint: no such folder: {a.skills_dir}. Pass --skills-dir with the folder that holds your "
              f"skill folders.")
        return 2
    findings, count = lint(a.skills_dir)
    for f in findings:
        print(f)
    print(f"RESULT {'FAIL' if findings else 'PASS'}: {len(findings)} finding(s) in {count} skill folder(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
