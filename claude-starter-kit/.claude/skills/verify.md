# /verify — Executable Quality Gate

Prove the current change works. This replaces checklist-style verification:
the gate is commands you run, not promises you make.

## Instructions

1. **Read the "Commands (the verify contract)" section of CLAUDE.md.** Those
   are the project's verify commands (build, test, lint, typecheck).
   - If the section is empty, discovering the commands is part of this skill:
     find them in `package.json` scripts, `Makefile`, `Cargo.toml`, `pyproject.toml`,
     or CI config, run them, and fill the section in for next time.
2. **Run every applicable command, fresh, in this turn.** Output from an
   earlier turn — before your latest edit — proves nothing.
3. **Exercise the changed behavior end-to-end.** If no test covers the change,
   drive the real path once (run the CLI, hit the endpoint, trace A→C through
   the actual entry point) and show the observed output.
4. **Report claims with evidence, in this exact shape:**
   ```
   Ran <command> → <result summary (exit code, counts)> → <claim>
   ```
5. **Failures are reported verbatim.** A red test is a finding, not an
   embarrassment. Never soften "2 failed" into "mostly passing".

## Gate checklist (after the commands pass)

- Full data flow traced A→C, not just the unit you touched
- Test count did not decrease versus the previous run
- Pattern grep done for any bug class you fixed (Standard 4)
- No dead code added; both sides of any cross-file boundary updated (Standard 5)
- `git diff` reviewed for scope creep — nothing unasked-for in the diff

## Hard rule

If a verify command cannot be run (missing dependency, no test suite, sandbox
limits), say so explicitly and label the claim **UNVERIFIED**. Never substitute
reasoning for execution and present it as verification — an unverified claim
presented as verified is a lie, not an estimate.
