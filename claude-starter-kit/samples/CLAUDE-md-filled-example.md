# HIVE Project Instructions for Claude Code

> **This is a filled-in example of CLAUDE.md from a real 39K-line Tauri project.**
> Use it as a reference for filling in your own [ADAPT] sections.
> The original is 918 lines — this is condensed to show the pattern, not every detail.

## Project Overview

HIVE (Hierarchical Intelligence with Virtualized Execution) is a persistent AI orchestration harness — a Windows desktop application that coordinates local and cloud LLMs as interchangeable cognitive resources. It's not a chatbot or model runner; it's the always-on brain that manages models (local GGUF, Ollama, OpenAI, Anthropic, OpenRouter), routes tasks to specialist agents, and maintains memory across sessions. The framework is permanent; the models are replaceable.

It consists of:
- **Desktop App**: Tauri v2 (Rust + React/TypeScript) in `HIVE/desktop/`
- **Launcher**: `START_HIVE.bat` for one-click Windows startup

## Key Directories

```
HIVE/
├── desktop/              # Tauri v2 app
│   ├── src/              # React: App.tsx (orchestrator) + components/
│   ├── src/lib/          # api.ts (TypeScript API layer + recommendation engine)
│   ├── src/components/   # 14 tab/utility components (props-only, no Context)
│   ├── src-tauri/        # Rust code (main.rs), tauri.conf.json
│   └── src-tauri/src/tools/  # Tool framework: file_tools, system_tools, web_tools
├── docs/                 # PRINCIPLE_LATTICE.md, architecture docs
claude-tools/             # Claude Code optimizations (mgrep, etc.)
.claude/                  # Hooks, skills, settings
```

## Development Guidelines

1. **Tauri v2 Config**: `nsis` settings go inside `bundle.windows.nsis`, not `bundle.nsis`
2. **No package-lock.json**: Use `npm install`, not `npm ci`
3. **Batch Scripts**: Use `!var!` (delayed expansion) not `%var%` inside blocks
4. **Shell Quoting in WSL**: Use double quotes `"{}"` when paths contain `$HOME`. Single quotes prevent variable expansion.

## Common Tasks

### Building the Desktop App
```bash
cd HIVE/desktop
npm install
npm run tauri build
```

### Running Development Mode
```bash
cd HIVE/desktop
npm run tauri dev
```

### Testing the Launcher
Double-click `START_HIVE.bat` — handles dependency checks and builds automatically.

## Things to Avoid

- Don't use `npm ci` (no lock file exists)
- Don't put Tauri NSIS config at `bundle.nsis` level (use `bundle.windows.nsis`)
- Don't frame HIVE as "just a model runner" — it's an orchestration harness
- Don't describe HIVE as "local-first" — it's provider-agnostic. A user with zero GPUs using only free API models is a first-class use case

## Cross-File Contracts

| Contract | Source of Truth | Mirror | Sync Method |
|---|---|---|---|
| Specialist port mapping | `server.rs::port_for_slot()` | `types.ts::SPECIALIST_PORTS` | Cross-ref comment |
| Dangerous tools list | `content_security.rs::is_dangerous_tool()` | `api.ts::DANGEROUS_TOOLS` | Cross-ref comment + "MUST stay in sync" |
| Tauri event names | Rust `emit("name", ...)` | TS `listen("name", ...)` | Convention (14 events, all verified) |

**When adding new cross-boundary contracts:**
1. First, try a single file (best — e.g., `channelPrompt.ts` has both builder + parser)
2. If Rust↔TS prevents that, add explicit cross-reference comments in BOTH files
3. Add the contract to this table

## What Each Key File Does

| File | Purpose | Touch carefully |
|------|---------|-----------------|
| `main.rs` | Tauri setup, tray icon, `perform_full_cleanup()` (shared shutdown), 148 command handler registrations | Yes - core logic |
| `memory.rs` | Memory system: SQLite + FTS5 + vector embeddings, hybrid search, daily logs | Yes - core data layer |
| `providers.rs` | Cloud provider chat + streaming (OpenAI, Anthropic, Ollama, OpenRouter, DashScope SSE) | Yes - provider-specific parsing |
| `App.tsx` | State orchestrator, imports tab components, VRAM pre-launch check, harness + memory session injection | Yes - all state lives here |
| `api.ts` | TypeScript API layer + recommendation engine + memory API + retry logic | Usually safe |
| `useChat.ts` | Chat logic: sendMessage, tool loop, chain policies, streaming, specialist routing | Yes - core chat engine |

## Current State

| Component | Status | Gap |
|---|---|---|
| Storage (SQLite + FTS5 + vectors) | Working | None |
| Hybrid search (BM25 + cosine) | Working | None |
| Auto-recall (session injection) | Working | Model can't actively query |
| Short-term → long-term promotion | **MISSING** | No memory lifecycle |
| Token-aware summarization | **MISSING** | Truncation instead of summarization |

## Architecture Patterns

### Tauri Data Flow

```
React (App.tsx)           Rust (main.rs)              External
     │                         │                          │
     │  invoke('command')      │                          │
     ├────────────────────────>│                          │
     │                         │  HTTP/spawn              │
     │                         ├─────────────────────────>│
     │                         │<─────────────────────────┤
     │  Result<T, String>      │                          │
     │<────────────────────────┤                          │
     │                         │                          │
     │  emit('event')          │                          │
     │<────────────────────────┤  (for progress updates)  │
```

**Pattern:** `invoke()` for request/response, `emit()` for streaming updates, errors are always `Result<T, String>`.

### State Management

```typescript
// Local state in App.tsx
const [models, setModels] = useState<LocalModel[]>([]);
const [serverRunning, setServerRunning] = useState(false);

// Persisted settings in localStorage
api.saveModelSettings(filename, { contextLength, kvOffload, gpuLayers });

// Secure storage (API keys) - encrypted file via Rust
api.storeApiKey('openai', key);  // → ~/.hive/secrets.enc
```

**Rule:** Settings → localStorage. Secrets → encrypted file. Memory → SQLite + markdown. Never mix them.

## Common Session Traps

### Trap 1: "Let me optimize this"
**Stop.** Is it slow? Is the user complaining? If not, don't touch it.

### Trap 2: "I'll fix this one place"
**Stop.** Search for the same pattern. Fix them all or none.

### Trap 3: "This should work now"
**Stop.** The words "should", "seems", "looks like" are NEVER acceptable. If you haven't run the verification command **in this response**, you cannot claim the result.

## Lessons Learned

| Bug | Root Cause | Rule |
|-----|-----------|------|
| SQLite `ln()` doesn't exist in bundled build | Used SQL math function without verifying availability | Test the production path, not synthetic setup |
| `access_count` never incremented | `let _ =` swallowed the `ln()` error | Audit `let _ =` on critical paths |
| `&content[..60]` UTF-8 panic | Byte-sliced a string without checking char boundaries | Use `.chars().take(N)` instead |
