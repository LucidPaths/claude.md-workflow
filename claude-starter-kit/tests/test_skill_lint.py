#!/usr/bin/env python3
"""Tests for tests/skill_lint.py: the shipped skills pass, and every check fires on a planted defect.

Run: python -m unittest discover -s claude-starter-kit/tests
"""
import os
import re
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skill_lint  # noqa: E402

STANDARD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "SKILL-STANDARD.md")


class SkillLintTests(unittest.TestCase):

    # Each planted test lints a copy of the shipped skills, plants one defect, and looks only at the
    # findings the plant added, so it tests the lint and not the current wording of the skills.

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.skills = os.path.join(self.tmp, "skills")
        shutil.copytree(skill_lint.KIT_SKILLS, self.skills)
        self.baseline = set(skill_lint.lint(self.skills)[0])

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def path(self, skill):
        return os.path.join(self.skills, skill, "SKILL.md")

    def append(self, skill, text):
        with open(self.path(skill), "a", encoding="utf-8") as f:
            f.write("\n" + text + "\n")

    def added(self):
        return sorted(set(skill_lint.lint(self.skills)[0]) - self.baseline)

    def assertFinding(self, needle):
        added = self.added()
        self.assertTrue([f for f in added if needle in f],
                        f"expected a new finding containing {needle!r}, the plant added: {added}")

    def assertNoFinding(self):
        added = self.added()
        self.assertEqual(added, [], f"the plant should add no finding, it added: {added}")

    # --- the shipped set -------------------------------------------------------------------

    def test_shipped_skills_pass(self):
        findings, count = skill_lint.lint(skill_lint.KIT_SKILLS)
        self.assertGreater(count, 0)
        self.assertEqual(findings, [], "\n".join(findings))

    def test_banned_list_matches_the_standard(self):
        with open(STANDARD, encoding="utf-8") as f:
            text = f.read()
        section = text.split("## 2.", 1)[1].split("\n## ", 1)[0]
        listed = set()
        for row in section.splitlines():
            if row.startswith("| `"):
                listed |= set(re.findall(r"`([^`]+)`", row.split("|")[1]))
        linted = {t for t, _ in skill_lint.BANNED} | {skill_lint.SIZE_TERM}
        self.assertEqual(listed, linted, "SKILL-STANDARD.md section 2 and skill_lint.BANNED differ")

    # --- check 1: frontmatter --------------------------------------------------------------

    def test_frontmatter_without_description_fails(self):
        with open(self.path("proof"), encoding="utf-8") as f:
            lines = f.read().splitlines()
        with open(self.path("proof"), "w", encoding="utf-8") as f:
            f.write("\n".join(l for l in lines if not l.startswith("description:")) + "\n")
        self.assertFinding("proof/SKILL.md:1: frontmatter: 'description' missing")

    def test_folder_without_skill_md_fails(self):
        os.makedirs(os.path.join(self.skills, "empty-skill"))
        self.assertFinding("empty-skill/SKILL.md:0: frontmatter: SKILL.md missing")

    # --- check 2: closing block ------------------------------------------------------------

    def test_skill_without_closing_block_fails(self):
        with open(self.path("rigor"), encoding="utf-8") as f:
            text = f.read()
        self.assertIn("## Closing block", text)
        with open(self.path("rigor"), "w", encoding="utf-8") as f:
            f.write(text.replace("## Closing block", "## The end"))
        self.assertFinding("rigor/SKILL.md:0: closing:")

    # --- check 3: vague terms in decision rules --------------------------------------------

    def test_vague_term_in_a_rule_fails(self):
        self.append("scalpel", "- Run the full suite again if needed.")
        self.assertFinding("vague: 'if needed'")

    def test_size_word_without_a_number_fails(self):
        self.append("scalpel", "- Split a large diff before review.")
        self.assertFinding("vague: 'large'")

    def test_vague_term_in_quotes_or_explanation_passes(self):
        self.append("scalpel", '- Never write "run it if needed" in a rule.')
        self.append("scalpel", "Why: a rule that says it usually works decides nothing.")
        self.assertNoFinding()

    # --- check 4: references to other skills -----------------------------------------------

    def test_reference_without_standalone_default_fails(self):
        self.append("scalpel", "- Then run `/proof` over the result.")
        self.assertFinding("reference: '/proof' has no standalone default")

    def test_reference_with_standalone_default_passes(self):
        self.append("scalpel", "- Standalone default: re-run the check once on the edited code. If `/proof` is "
                               "installed, it replaces this default.")
        self.assertNoFinding()

    def test_reference_to_a_skill_not_in_the_set_fails(self):
        self.append("scalpel", "- Standalone default: write the record yourself. If `/session-record` is installed, "
                               "it replaces this default.")
        self.assertFinding("reference: '/session-record' is not a skill in this folder")

    def test_harness_command_is_not_a_skill_reference(self):
        self.append("scalpel", "- Where the harness offers `/compact`, run it only between two slices.")
        self.assertNoFinding()


if __name__ == "__main__":
    unittest.main()
