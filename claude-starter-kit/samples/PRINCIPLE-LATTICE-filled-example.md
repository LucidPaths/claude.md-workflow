# Project Principle Lattice

> **This is a filled-in example of PRINCIPLE_LATTICE.md from a real project.**
> It shows 5 of the project's 8 principles, each with concrete instantiations —
> proof that the principle lives in the codebase, not just on paper.
> A principle without instantiations is a wish.

---

## What This Is

These are axiomatic principles — non-negotiable values that guide every design decision. They aren't features or goals. They're the DNA.

When stuck on a decision, check it against the lattice. If a choice violates a principle, it's wrong — even if it "works." If it honors multiple principles simultaneously, it's probably right.

Each principle has **instantiations** — concrete proof the principle exists in code, not just docs.

---

## Principles

### 1. Bridges and Modularity

> *One path, two systems. Lego blocks, not monoliths.*

Every component should be a self-contained block. Pull one out — that specific thing stops working. The rest stands. When two systems need to talk, build a bridge — don't duplicate.

**Instantiations:**
- Windows↔WSL `/mnt/c/` bridge: download once to Windows, WSL reads the same files (no duplicate download paths)
- Provider abstraction layer: swap Local/OpenAI/Anthropic/Ollama without touching UI code
- `wsl_cmd()` helper: single function encapsulates all WSL command spawning (CREATE_NO_WINDOW flag, error handling)
- 14 independent components: all props-only or self-contained, no shared React Context
- Tool registry: every tool implements `HiveTool` trait, self-registers, self-describes via JSON Schema

**Demands:**
- Each component fails independently — chat breaking doesn't kill model management
- Plugin architecture for future tool/skill modules

---

### 2. Provider Agnosticism

> *The interface is permanent. The backend is replaceable.*

The app doesn't care where intelligence comes from. Local llama.cpp, OpenAI, Anthropic, Ollama, or something that doesn't exist yet. The user picks a provider. The chat works. The UI is identical.

**Instantiations:**
- Six providers supported: Local (llama.cpp), OpenAI, Anthropic, Ollama, OpenRouter, DashScope
- Same ChatMessage type across all providers — no provider-specific message formats in UI
- Per-provider settings with graceful degradation (no API key = feature hides, doesn't crash)
- Memory session-injected as separate system message: never mutates the system prompt (works identically with any provider)
- OpenAI-compatible providers share unified `chat_openai_compatible()` dispatch — adding a new provider is a 1-line entry

**Demands:**
- New provider = new adapter, zero UI changes
- Provider health/status shown uniformly regardless of backend

---

### 3. Simplicity Wins

> *Don't reinvent the wheel. Code exists to be used.*

The best code is code someone else already debugged. Use battle-tested libraries. Three clear lines beat one clever abstraction. A working simple solution beats an elegant broken one.

**Instantiations:**
- localStorage for settings persistence (not a custom database)
- reqwest for HTTP (not custom networking)
- llama.cpp for inference (not a custom runtime)
- GGUF spec followed exactly for metadata parsing (not a custom format)

**Demands:**
- Before writing a new system, search for existing solutions first
- Before rewriting a function, check git history — maybe the old version worked
- If a dependency does 80% of the job, use it and handle the 20%

---

### 4. Errors Are Answers

> *Every failure teaches. Given a model, the program debugs itself.*

An error message that says "something went wrong" is itself a bug. Every error must say what happened, why, and what the user can do about it.

**Instantiations:**
- Actionable error messages: `"Chat failed (HTTP 500): model not loaded"` not `"Error: {}"`
- Dual-log system: 11 backend modules log lifecycle events to `hive-app.log`, frontend bridge auto-persists `[HIVE]` logs
- `check_logs` tool: model can read its own operational state (server crashes, VRAM events)
- Pre-send health checks: verify server is alive before sending a message
- Abort recovery: stop button works, next message works too, no broken state

**Demands:**
- Capture all process stdout/stderr (not /dev/null)
- Token/speed display so users can SEE if something is wrong
- Aspirational: model reads its own error logs and suggests fixes

---

### 5. Fix The Pattern, Not The Instance

> *Cure the root cause. Don't treat symptoms.*

When you find a bug, the bug is never alone. The same mistake exists in 3-5 other places. Search for the pattern. Fix every instance.

**Instantiations:**
- `.trim()` TypeError: found 3 vulnerable call sites, fixed all 3 (not just the one that crashed)
- localStorage hydration: `{ ...defaults, ...stored }` pattern applied everywhere (not just the one that broke)
- CLAUDE.md documents grep commands for each bug class: "found missing User-Agent? Check ALL HTTP clients"
- Coding standards encode patterns, not individual fixes

**Demands:**
- Every bug fix includes a grep for the same pattern across the codebase
- If a pattern produces bugs twice, add it to CLAUDE.md so it never happens again
- Root cause analysis before fix — the error might be downstream of the real bug

---

## Using The Lattice

### For Design Decisions
When stuck between two approaches, score them against the principles. If one cleanly honors more principles without violating any, it wins. If both violate something, find a third approach.

### For Code Review
Every PR can be checked: *does this change violate any principle?* Not "is this code clean" — that's subjective. "Does this violate the lattice" — that's answerable.

### For New Contributors
Read this document first. If you understand these principles, you understand how the project thinks. The codebase is the implementation; the lattice is the intent.
