---
title: Cline — v3.58 native subagents + CLI 2.0 headless (with v3.59–v3.79 extensions)
slug: cline-v3-58
date: 2026-04-19
author: Cline Bot Inc. (GitHub org `cline`, originally `saoudrizwan/claude-dev` a.k.a. Saoud Rizwan)
first_public_repo: 2024-07-06 (repo `cline/cline` creation)
v3_58_release: 2026-02-12 (v3.58.0)
v3_57_cli20_release: 2026-02-10 (v3.57.0 — "Cline CLI 2.0 now available")
v3_55_subagent_preview: (release undated in grep but appears in CHANGELOG line 786–787 as "Added Subagent support (Experimental)" alongside "Added Cline CLI (Preview)")
current_head_version: v3.79.0 (2026-04-16) — 22 minor releases past v3.58 in ~2 months
primary_sources:
  - https://github.com/cline/cline (60,439★ / 6,180 forks on 2026-04-19; Apache-2.0; TypeScript)
  - https://github.com/cline/cline/blob/main/CHANGELOG.md
  - https://github.com/cline/cline/releases/tag/v3.58.0
  - https://github.com/cline/cline/blob/main/docs/features/subagents.mdx
  - https://github.com/cline/cline/blob/main/docs/features/deep-planning.mdx
  - https://github.com/cline/cline/blob/main/docs/features/auto-approve.mdx
  - https://github.com/cline/cline/blob/main/docs/features/memory-bank.mdx
  - https://github.com/cline/cline/blob/main/docs/features/worktrees.mdx
  - https://github.com/cline/cline/blob/main/docs/features/focus-chain.mdx
  - https://github.com/cline/cline/blob/main/docs/features/auto-compact.mdx
  - https://github.com/cline/cline/blob/main/docs/cline-cli/overview.mdx
  - https://github.com/cline/cline/blob/main/docs/cline-cli/three-core-flows.mdx
  - https://github.com/cline/cline/blob/main/docs/cline-cli/cli-reference.mdx
  - https://github.com/cline/cline/blob/main/.clinerules/general.md
  - https://github.com/cline/cline/blob/main/.clinerules/cli.md
  - https://github.com/cline/cline/blob/main/cli/README.md
  - https://docs.cline.bot/llms-full.txt (consolidated docs, 22,161 lines)
topic: harness
tags: [harness, cline, vscode-extension, jetbrains, cli, headless, ci-cd, subagents, hooks, skills, acp, mcp, worktrees, memory-bank, focus-chain, plan-act, apache-2, typescript]
status: deep-dive
confidence: high
rounds: 2 (initial + integration)
axes_used: [1,2,3,4,5,6,7,8,9,10,11,12,13]
axes_added: [13-substrate-variant-matrix]
axes_dropped: []
candidate_axis_proposals: [Δ1_substrate_feature_gap_TESTED_EXTENDED, Δ2_consensus_planning_gate_REFINED, Δ3_stage_handoff_NA, Δ4_category_skill_orthogonal_REFUTED_FOR_CLINE]
probe_method: coordinator fetched primary sources via curl / GitHub API (Agent/Task tool unavailable in this sub-agent context; codex:rescue explicitly forbidden by user directive)
---

## Proposed schema deltas

### Δ1 (Substrate feature-gap exploitation) — supports & extends the axis
Cline is a **single-runtime, multi-substrate emitter** in the opposite configuration from OMC/OMX: one TypeScript core + gRPC/protobuf message bus that drives *six* surfaces — VS Code extension, Cursor, JetBrains (via ACP), Zed, Neovim (via `agentic.nvim`/`avante.nvim`), and the `cline` CLI (React Ink TUI). The **Agent Client Protocol (ACP)** is the substrate-abstraction layer: "Cline CLI supports the Agent Client Protocol (ACP), an open standard that enables AI coding agents to work across different editors and IDEs. This means you can use the full Cline agent—with all its capabilities including Skills, Hooks, and MCP integrations—in your preferred development environment" (docs/cline-cli/acp-editor-integrations). This is a **substrate-inversion** relative to OMC/OMX: instead of re-implementing primitives per substrate, Cline factors the agent logic into a host-neutral core and exposes a narrow adapter protocol. Axis Δ1 as originally framed (OMX/OMC case) was about *hand-re-implementing missing primitives in a host-specific runtime*. Cline demonstrates a **second-use but dual pattern**: rather than port-and-reinvent, export-via-adapter-protocol. **Recommend refining Δ1** into two sub-patterns: (a) "substrate-port with hand-reinvention" (OMC↔OMX), (b) "substrate-agnostic via adapter protocol" (Cline/ACP).

### Δ2 (Consensus planning as execution gate) — refuted for Cline
Cline has two distinct planning surfaces — **Plan Mode** and **Deep Planning** (`/deep-planning`) — but neither is a *gate that rejects underspecified prompts and redirects*. Plan Mode is a user-toggled mode ("Plan mode lets you explore and strategize without changing files. Act mode executes against your plan" — docs/core-workflows/plan-and-act). Deep Planning is an *opt-in slash-command workflow*. Cline does NOT intercept under-specified prompts like OMC/OMX's `$ralplan` Pre-Execution Gate; it is user-selected, not detector-triggered. Δ2 remains a 1-use axis (OMX/OMC) until a detector-triggered case appears.

### Δ3 (Stage handoff as RPC protocol) — NOT applicable
Cline's subagents do not hand off to each other via fixed-schema artifacts. They are **stateless research fanout**: main agent → N parallel subagents → each returns a report string → main agent reads. No intermediate artifacts, no chained stages. Δ3 promotion count unchanged.

### Δ4 (Category × Skill × Persona orthogonality — OMO axis) — partially refuted / different shape
Cline does not factor subagent delegation into orthogonal dimensions. Subagents in v3.58+ are **instances of a single role** (read-only researcher) with the only user-configurable variance being **custom prompt + optional `modelId` + optional skills** (CHANGELOG v3.67.0: "Add support for skills and optional modelId in subagent configuration"). No category system. No persona table. What Cline has is **Plan Mode model ≠ Act Mode model** (docs: "You can configure separate models for Plan and Act modes") — a 2-way model assignment tied to mode, not a 3-dimensional delegation factor. Δ4 remains OMO-specific.

### New candidate Δ5 — "Headless-mode-as-first-class output contract"
- **Proposed by**: Cline v3.57/v3.58 deep-dive
- **Rationale**: Cline CLI 2.0 treats "non-interactive execution" as a *typed output contract* with automatic mode detection by TTY/pipe/flag: `cline -y` → plain text + auto-approve + exit on completion; `cline --json` → newline-delimited JSON matching `ui_messages.json` schema (`{type: "ask"|"say", text, ts, reasoning?, partial?}`); piped stdin → headless auto-activates. Chain composition is an advertised first-class pattern: `git diff | cline -y "explain these changes" | cline -y "write a commit message for this"` (docs/cline-cli/three-core-flows verbatim). Different from Ralph's bash-loop-over-prompt (one input contract, no output contract) and from GSD's file-based state machine. Cline's model is pipe-composable agents with a stable serialization. Distinct enough to be a candidate axis.
- **Proposed form**: "Does the harness treat headless/non-interactive execution as a first-class output contract? If yes: (a) what triggers the mode switch (flag / TTY detect / pipe detect / all), (b) what output formats are guaranteed (plain text / JSON schema / both), (c) is chain composition (stdout of one → stdin of next) documented/supported, (d) what is the exit contract (exit-on-complete vs long-running)?"
- **Promotion threshold**: 2 independent cases. GSD's batch phase commands are a weak near-match but don't advertise pipe composition. Compound Engineering's `/lfg` is not pipeable. Likely waits for a second clean case.
- **Pointers**: `notes/harness/cline-v3-58.md` §5 (prompt strategy — CLI 2.0), §11 (primitives).

---

## TL;DR (3 lines)
Cline v3.58 (2026-02-12) collapsed an earlier experimental subagent implementation into **a single native `use_subagents` tool** that dispatches **read-only parallel research agents** each with isolated context windows but *shared filesystem*, paired with v3.57's **CLI 2.0** that makes headless mode auto-detected (TTY/pipe/`-y`/`--json` flags) and pipeline-composable. The v3.58 architecture is **explicitly narrow** — subagents cannot edit files, use browsers, talk to MCP, or nest — which is the opposite end of the axis from OMC/OMX's staged heterogeneous pipelines or OMO's 8-category × 11-agent orthogonal matrix. Distinguishing trait from the Korean-author harness cluster: Cline factors portability via **Agent Client Protocol (ACP)** as a host-neutral substrate-adapter (VS Code / JetBrains / Zed / Neovim / CLI all run one TypeScript core), whereas OMC↔OMX hand-reinvent primitives per substrate.

## 1. Identity & provenance

- **Repo**: https://github.com/cline/cline — 60,439 stars / 6,180 forks / 274 subscribers / 688 open issues (2026-04-19 via GitHub API) — TypeScript, Apache-2.0. Original VS Code Marketplace slug `saoudrizwan.claude-dev`, now reskinned under `cline/cline` org (org id 184127137 per API).
- **Repo created**: 2024-07-06T07:28:10Z (GitHub API `created_at`). Description: *"Autonomous coding agent right in your IDE, capable of creating/editing files, executing commands, using the browser, and more with your permission every step of the way."*
- **v3.58.0 release**: 2026-02-12T01:13:44Z. Release body lists the subagent consolidation as headline: **"Subagent: replace legacy subagents with the native `use_subagents` tool"** (CHANGELOG.md line 300; release body verbatim).
- **v3.57.0 release** (2 days earlier): "**Cline CLI 2.0 now available. Install with `npm install -g cline`**" (CHANGELOG.md line 339, verbatim).
- **Earlier subagent preview**: CHANGELOG line 787 (appearing in what looks like a v3.36 range based on context — exact tag unconfirmed in this pass) reads verbatim: *"Added Cline CLI (Preview) / Added Subagent support (Experimental) / Added Multi-Root Workspaces support"*. So **v3.58 is a consolidation, not the initial introduction**.
- **Release cadence**: From v3.58 (2026-02-12) to v3.79 (2026-04-16) = **22 minor releases in ~63 days**, about one per 2.9 days. Minor bumps ship mixed feature/fix. No separate RFC/design doc trail visible from the release pages; discussions use GitHub Discussions (`has_discussions: true`).
- **User-claim verification**: The task prompt's "5M+ installs across IDEs" figure is **UNVERIFIED** from primary sources — README does not cite an install number. VS Marketplace link is `saoudrizwan.claude-dev`; the actual install count would require the Marketplace API (not probed this round). Star count 60k confirms very-top-tier adoption but is not an install number.
- **Author posture**: Corporate (Cline Bot Inc., Apache-2.0, has Enterprise page with SSO/SAML/on-prem). Contrast the single-developer Korean-author cluster (Yeachan Heo / YeonGyu-Kim / Q00 / affaan-m / revfactory) and the solo-blogger Ralph/Superpowers lineage.

## 2. Problem framing

Verbatim from README: *"Cline can handle complex software development tasks step-by-step. With tools that let him create & edit files, explore large projects, use the browser, and execute terminal commands (after you grant permission), he can assist you in ways that go beyond code completion or tech support. … While autonomous AI scripts traditionally run in sandboxed environments, this extension provides a human-in-the-loop GUI to approve every file change and terminal command, providing a safe and accessible way to explore the potential of agentic AI."*

Subagents-specific framing (docs/features/subagents.mdx L7): *"Subagents let Cline spawn focused research agents that run in parallel. Each subagent gets its own prompt and context window, explores the codebase independently, and returns a detailed report to the main agent. **This keeps the main agent's context clean while gathering broad information fast.**"*

CLI 2.0 framing (docs/cline-cli/overview.mdx L28): *"The CLI operates in two distinct modes, automatically selecting the appropriate one based on how you invoke it"* — Interactive (TTY) or Headless (pipe/`-y`/`--json`).

Core pain named: (a) context-window pollution during broad codebase exploration, (b) needing a human-in-the-loop safety rail while still getting agentic autonomy, (c) extending the same agent to CI/CD without building a separate product.

## 3. Control architecture

**Core loop**: classic ReAct/agent loop. Main agent takes user prompt → streams reasoning + tool calls → tools return to agent → loops until `attempt_completion` tool fires or user stops.

**v3.58 subagent dispatch shape**:
- Tool name: `use_subagents` (docs/features/subagents L12). Main agent invokes the tool with N subagent prompts.
- Dispatch is **parallel spawn-and-join fan-out**: *"When Cline uses the `use_subagents` tool, it launches independent agents simultaneously"* (subagents.mdx L14). No explicit upper bound on N published in docs; per-subagent cost is tracked separately (*"Subagent costs (tokens and API spend) are tracked separately per subagent and rolled into the task's total cost"* — L22).
- Each subagent has its own context window, own token budget, own model invocation.
- Subagents **cannot spawn nested subagents** (L18: *"Cannot edit files, use the browser, access MCP servers, or spawn nested subagents"*). Single-level fan-out only.
- Subagents are **not auto-invoked** by Cline; the user must mention them or describe a task that benefits from parallel exploration (L27: *"Cline does not automatically decide to use subagents. You need to ask for them in your prompt"*).
- v3.67.0 CHANGELOG adds *"support for skills and optional modelId in subagent configuration"* + *"AgentConfigLoader for file-based agent configs"* — meaning each subagent can optionally be pinned to a different model than the main agent. v3.70.0 adds *"Improve subagent context compaction logic"* + *"Subagent stream retry delay increased to reduce noise from transient failures"*.

**Architecture taxonomy (Anthropic)**: hybrid. Main loop is **agent** (LLM directs its process + tool use). Subagents invocation is a **parallelization / sectioning** pattern embedded as one tool call. Plan/Act toggle is a **workflow** (user-driven mode switch). Deep Planning `/deep-planning` is a **prompt-chained workflow**: Silent Investigation → Discussion → Plan Creation → Task Creation (deep-planning.mdx §"How It Works").

**Termination**: `attempt_completion` tool call; task-timeout flag (`--timeout <seconds>`) in CLI headless; user cancel in UI; optional `--max-consecutive-mistakes` CLI flag introduced v3.58.

## 4. State & context model

Cline has **four layered state substrates**, each with a distinct role:

a. **Task directory** (per-task): `~/.cline/data/tasks/<id>/ui_messages.json` holds conversation history. CLI `--json` output is explicitly documented as following the same schema (three-core-flows.mdx: *"JSON output follows the same format as task files in `~/.cline/data/tasks/<id>/ui_messages.json`"*).

b. **Checkpoints** (per-task, file-state): Git-backed file snapshots at each step, with "Compare" diff UI and "Restore Task and Workspace" / "Restore Workspace Only" buttons (README §Checkpoints).

c. **Memory Bank** (per-project, user-maintained knowledge): 6-file markdown hierarchy in `memory-bank/` — `projectbrief.md` (foundation), `productContext.md` (why), `activeContext.md` (current focus, updates most often), `systemPatterns.md` (architecture), `techContext.md` (tech stack), `progress.md` (status/milestones). Opt-in via custom instructions. Triggered by "initialize memory bank" / "update memory bank" / "follow your custom instructions" user utterances (memory-bank.mdx).

d. **`.clinerules/`** (per-project, Cline-read instructions): always-active project rules (analogue of `CLAUDE.md` / `.cursor/rules`). Cline's own repo uses `@.clinerules/general.md`, `@.clinerules/network.md`, `@.clinerules/cli.md` — the root `CLAUDE.md` is just 3 lines that include them. Hooks live at `.clinerules/hooks/` (project) or `~/Documents/Cline/Hooks/` (global). Skills live at `.cline/skills/` (project, recommended), `.clinerules/skills/`, `.claude/skills/`, or `~/.cline/skills/` (global). Global takes precedence over project when names collide (skills.mdx §"Where Skills Live").

**Context window management**: 
- **Auto-Compact** (docs/features/auto-compact) — when approaching context limit, Cline summarizes the conversation and continues. LLM-based summarization for Claude 4 / Gemini 2.5 / GPT-5 / Grok 4; rule-based truncation fallback for other models.
- **Focus Chain** — todo-list markdown file that persists across context-compactions (*"Focus Chain pairs well with Auto Compact. When Focus Chain is enabled, todo lists persist across summarizations"*).
- **`/smol`** command = compact conversation in-place. **`/newtask`** = distill to clean new task.

**Subagent state**: Each subagent gets its own context window + token budget. Subagents are **not isolated at the filesystem level** — they can `read_file` the same working tree as the main agent. Isolation is only at *context* and *write-permission* levels. No worktree/sandbox is spawned for them.

**Worktrees (different mechanism, user-driven)**: Git worktrees are a separate Cline feature (docs/features/worktrees) that lets *the user* open parallel VS Code windows, each a worktree on a different branch, each running its own main Cline agent. Used for parallel top-level task isolation, not subagent isolation. A `.worktreeinclude` file (union-intersected with `.gitignore`) specifies files to copy into new worktrees (e.g., pre-built `node_modules/`).

## 5. Prompt strategy

**No slash-command bundle shipped by Cline itself** — unlike Superpowers / GSD / Spec Kit / gstack / ECC, Cline does not ship a library of pre-authored slash commands covering a workflow DAG. The chat commands that exist are:
- `/deep-planning` — initiate a four-step architect-first workflow (Silent Investigation → Discussion → `implementation_plan.md` → Task Creation).
- `/newtask` — start a clean task distilling current state.
- `/smol` — compress current conversation in-place.
- `/mcp:<server>:<prompt>` (v3.55+) — surface MCP server prompts as slash completions.
- `/skills` (v3.65+) — CLI command to view/manage installed skills.
- `/q` (v3.67+) — quit CLI.

**User-authorable surfaces**:
- **Skills** (progressive disclosure, SKILL.md + YAML frontmatter, skill description max 1024 chars, load on-demand via `use_skill` tool) — same-family structure as Anthropic Agent Skills, Superpowers, OMO, OMC (but shipped as a *mechanism*, not a library).
- **Hooks** (8 types: TaskStart, TaskResume, TaskCancel, TaskComplete, PreToolUse, PostToolUse, UserPromptSubmit, PreCompact) — executable scripts with JSON stdin/stdout interface. Platform-specific filenames (`HookName.ps1` Windows / extensionless on macOS/Linux). Global hooks run before workspace hooks; either can return `cancel: true` to block. **Cline ships hooks as a mechanism, not as pre-authored workflow content** — a contrast with Superpowers/Compound Engineering which ship opinionated skill libraries.
- **Memory Bank** — 6-file Markdown template (see §4).
- **`.clinerules/*.md`** — always-on project rules.

**CLI 2.0 prompt shape** — a new prompt-strategy surface: the *shell pipeline itself* is the composition medium. `git diff | cline -y "explain these changes" | cline -y "write a commit message for this"` (three-core-flows.mdx, verbatim). This makes Cline **fluent in Unix-pipe discipline**, which no other harness in this corpus advertises as a first-class pattern.

## 6. Tool surface & permission model

**Main-agent tools** (inferred from changelog + docs — not an enumeration target this round): `read_file`, `write_to_file`, `replace_in_file`, `list_files`, `search_files`, `list_code_definition_names`, `execute_command`, browser tools, MCP tools, `use_skill`, `use_subagents`, `new_task`, `attempt_completion`.

**Subagent tool sub-set** (explicitly from subagents.mdx §"What Subagents Can Do" table):

| Tool | Purpose |
|---|---|
| `read_file` | Read file contents |
| `list_files` | List directory contents |
| `search_files` | Regex search across files |
| `list_code_definition_names` | List top-level classes, functions, methods |
| `execute_command` | Run read-only commands (`ls`, `grep`, `git log`, `git diff`, etc.) |
| `use_skill` | Load and activate skills |

Explicit exclusions: *"Subagents cannot write files, apply patches, use the browser, access MCP servers, or perform web searches. They also cannot spawn their own subagents"* (L69).

**Permission model** — Auto Approve (auto-approve.mdx) is a **per-tool-category grant system**:
- Base toggles: Read project files / Edit project files / Execute safe commands / Use the browser / Use MCP servers.
- Expansion toggles (require base): Read all files (outside workspace) / Edit all files / Execute all commands.
- Safe-vs-approval-required command split is *model-marked per invocation*: *"Cline does not use a fixed allowlist. The model marks each command with a `requires_approval` flag based on the command and arguments"* (auto-approve.mdx §"Safe vs Approval-Required Commands"). Examples: `npm install <pkg>` / `rm -rf` / `mv` / `sed -i` are commonly approval-required; `git status` / `ls -la` / `npm test` are commonly safe.
- **YOLO mode** (a.k.a. headless `-y` in CLI) = auto-approve everything including mode transitions. UI-dangerous; CLI-mandatory for CI.
- **Subagent approval inheritance** — explicitly not independent: *"Subagents follow the **Read project files** auto-approve permission. If you have 'Read project files' enabled in Auto Approve, subagent launches will be auto-approved. In YOLO mode, subagents are always auto-approved. If auto-approve is off, Cline will ask for your approval before launching subagents, showing you the prompts it plans to send"* (subagents.mdx L48-52, verbatim).
- **CLI headless restriction**: `CLINE_COMMAND_PERMISSIONS` env var takes a `{"allow": [...glob], "deny": [...glob]}` JSON — a secondary deterministic allowlist layer *outside* the model's `requires_approval` flag.

**Hooks as deterministic permission layer**: `PreToolUse` hook receives `{taskId, hookName, clineVersion, workspaceRoots, userId, model, preToolUse: {tool, parameters}}` JSON on stdin and returns `{cancel: true|false}` on stdout. Cancel blocks the tool call. This is an orthogonal second-gate layer that Cline offers as the permission primitive for policy enforcement in regulated environments. Related: v3.77 introduces *"Lazy Teammate Mode"* (experimental toggle) — purpose not documented in README/CHANGELOG yet; name suggests conservative approval behavior.

## 7. Human-in-the-loop points

Six distinct checkpoint types:

1. **Per-tool approval prompt** (VS Code UI modal or CLI interactive prompt) — default unless auto-approved or YOLO.
2. **Plan / Act mode toggle** — user explicitly decides when to move from Plan (no file changes) to Act. Explicit mode change tracked in Auto Approve as its own permission ("mode transitions" are auto-approved only in YOLO mode per auto-approve.mdx §YOLO).
3. **Diff-view editor** — user can edit or revert Cline's changes *directly in the diff view* before accepting (README §"Create and Edit Files").
4. **Checkpoint restore** — user can roll back file state with "Restore Workspace Only" (keep the task, discard file changes) or "Restore Task and Workspace" (both).
5. **Subagent approval** — if auto-approve is off, user sees and approves the planned subagent prompts before launch.
6. **Deep Planning handoff** — user reviews `implementation_plan.md` and explicitly approves before Cline converts it to a task with trackable items (deep-planning.mdx Step 4).

## 8. Composability

**Multi-substrate via Agent Client Protocol (ACP)**: Cline explicitly supports JetBrains IDEs, Zed, Neovim (via `agentic.nvim`/`avante.nvim`) *by exposing the CLI's agent core over the Agent Client Protocol open standard* — "enables AI coding agents to work across different editors and IDEs. … you can use the full Cline agent—with all its capabilities including Skills, Hooks, and MCP integrations—in your preferred development environment" (llms-full.txt §ACP L1167).

**MCP client**: Full Model Context Protocol client (README §'add a tool that...'). Supports streamable HTTP MCP with reconnection handling (v3.73.0). v3.55.0 added MCP prompts-as-slash-commands (`/mcp:<server>:<prompt>`). **Remote config** (v3.56+): centrally provisioned MCP server list with custom headers, synced deletions. v3.67.0 adds "MCP enterprise configuration details". This is a *meaningfully more enterprise-oriented* MCP posture than any other corpus entry.

**API provider abstraction**: OpenRouter, Anthropic, OpenAI, OpenAI Codex (via ChatGPT OAuth, v3.52+), Google Gemini, AWS Bedrock, Azure, GCP Vertex, Cerebras, Groq, Moonshot, ZAI/GLM, Fireworks, W&B Inference/CoreWeave (v3.73), Vercel AI Gateway, Cline API, SambaNova, LM Studio, Ollama, OpenAI-compatible. `.clinerules/general.md` documents a **6-file update protocol** to add a provider without silent proto-serialization reset-to-Anthropic (§"Adding a New API Provider"). This is not a casual extension surface — it is a full-scale abstraction with protobuf schema, dual handler registration, and validation layers.

**gRPC-over-message-passing internal architecture**: `.clinerules/general.md` verbatim: *"The extension and webview communicate via gRPC-like protocol over VS Code message passing. Proto files live in `proto/` (e.g., `proto/cline/task.proto`, `proto/cline/ui.proto`)"*. This is the internal mechanism that lets Cline factor one TypeScript core across many UI substrates — the webview, the CLI (React Ink), and ACP consumers all talk to the same gRPC surface.

**SDK** (v3.67.1 added `ClineAgentOptions`): *"Added Cline SDK API interface for programmatic access to Cline features and tools, enabling integration into custom applications"* — a **third-party-embeddable agent runtime**, not just an editor plugin.

**Provider × subagent interaction**: v3.67 confirmed cross-cut: *"Add support for skills and optional modelId in subagent configuration"* → each subagent can be pinned to a specific model. Same mechanism as Plan mode ≠ Act mode model. No explicit "category" abstraction (contrast with OMO's 8-category matrix).

## 9. Empirical claims & evidence

- **No SWE-bench / TerminalBench / internal benchmark claims** appear in the primary sources fetched. The docs ship marketing screenshots and videos but not numeric evaluations.
- **Scale proxies**: 60,439★ on GitHub (2026-04-19), 6,180 forks, 274 subscribers, 688 open issues, claimed 5M+ installs (UNVERIFIED from primary source this round — would require Marketplace API).
- **Pace proxies**: v3.58→v3.79 = 22 releases in 63 days (see §1).
- **Design provenance** is explicit for at least one primitive: *"Thanks to Claude Sonnet's agentic coding capabilities, Cline can handle complex software development tasks step-by-step"* (README line 35) — the agent loop was built around Claude Sonnet's tool-use reliability. Browser tool is explicitly attributed to *"Claude Sonnet's new Computer Use capability"*.
- **Extensive provider-diversity claim** is primary-source-verified by the in-tree provider list (§8 enumeration).

## 10. Failure modes & limits

Observed from GitHub issues and CHANGELOG (2026-04-19 snapshot):

- **Extended thinking + subagents incompatibility** (open issue #9278): "`use_subagents` tool fails with HTTP 400 when extended thinking is enabled (claude-sonnet-4-5-20250929)" — a concrete v3.58-era failure mode confirming *the new subagent tool is not fully compatible with extended-thinking models*.
- **Subagent manual-invocation required** (documented): Cline does not decide on its own to use subagents. Users who don't prompt for them never benefit — a usability limit, not a bug.
- **Subagents cannot nest**: hard architectural limit. Tree depth fixed at 2 (main + 1 level of workers).
- **Context rot via auto-compact**: the docs acknowledge *"As you work, this window fills with conversation history, file contents, and tool results. When the context window approaches its limit, Cline automatically compresses older parts of the conversation"* — but compression is LLM-based only for Claude 4 / Gemini 2.5 / GPT-5 / Grok 4; everything else uses rule-based truncation, losing data.
- **Provider add-pitfall** (self-documented in .clinerules/general.md): *"Without these [three proto-conversion places], the provider string hits the `default` case and returns `ANTHROPIC`. The webview, provider list, and handler all work fine, but the state silently resets when it round-trips through proto serialization. **No error is thrown.**"* — a self-declared silent-failure mode tied to the gRPC abstraction.
- **Hook toggle not cross-platform yet**: *"On Windows, hooks are executed with PowerShell and run whenever the hook file exists. In this foundation PR, hook enable/disable toggling is not yet supported on Windows"* (hooks.mdx).
- **CHANGELOG v3.76.0 admits loop risk**: *"Add repeated tool call loop detection to prevent infinite loops wasting tokens"* — confirming a known failure class (infinite retry loops were previously possible; v3.55.1 also added *"Prevent infinite retry loop when write_to_file fails"*).
- **Repeated tool-call failure fragility**: v3.73.0 fix: *"Tool handlers (`read_file`, `list_files`, `list_code_definition_names`, `search_files`) now return graceful errors instead of crashing"* — acknowledging previous crash-on-invalid-arg pattern.

## 11. Transferable primitives ★

### P1. Native parallel read-only research subagents with single-level-fanout + shared filesystem + isolated context
- **Description**: `use_subagents` dispatches N parallel workers, each a fresh context window + token budget, all sharing the same working tree but **gated to a read-only tool subset** (read_file, list_files, search_files, list_code_definition_names, execute_command-read-only, use_skill). Each returns a string report; main agent synthesizes. No nesting.
- **Assumed context**: any agent loop with (a) tool-calling, (b) multi-agent spawn capability, (c) fileshare-by-default runtime, (d) a story for bundling subagent cost accounting.
- **Standalone-extractable?** **Yes** — this is a well-defined fanout shape with crisp boundaries. The axis of novelty is *gate the worker tool set, not the worker context*. Cleaner than spinning worktrees; cheaper than sandboxing. Transplants to any harness with tool-level permission granularity.

### P2. Auto-mode-detection headless CLI with pipeline-composable output
- **Description**: Single `cline` binary chooses Interactive vs Headless by examining stdin-TTY / stdout-redirect / flag presence (`-y`, `--json`). Headless output respects an explicit JSON schema (`{type, text, ts, reasoning?, partial?}`) that matches the same serialized shape as UI messages. Chain-composable: `cline -y "x" | cline -y "y"` is advertised.
- **Assumed context**: any agent tool that wants a CLI affordance AND needs to be scriptable in CI without re-architecting.
- **Standalone-extractable?** **Yes, partial** — the mode-detection logic is generic and portable (any stdio-literate runtime). The output-contract-stability part requires the agent to have a stable internal message schema; OMC/OMX/Ralph-style runtimes without such a schema would need one introduced first.

### P3. ACP (Agent Client Protocol) as host-neutral substrate adapter
- **Description**: Factor the agent's capabilities behind a single open-standard RPC so any editor/IDE/terminal can host the same agent. Cline uses ACP to expose Skills + Hooks + MCP to JetBrains / Zed / Neovim without per-host ports. Contrast OMC↔OMX's reinvent-per-host pattern.
- **Assumed context**: multi-substrate ambition; the willingness to freeze a public RPC contract; the external standard (ACP) or a private equivalent.
- **Standalone-extractable?** **Partial** — the *pattern* is extractable and broadly useful for any harness author planning to expand substrates. The concrete ACP library is external but open; adopting it requires accepting its message schema. A harness that does *not* want to expose internals publicly cannot use ACP directly but can still emulate the factoring locally.

### P4. 8-event hook lifecycle as deterministic policy substrate
- **Description**: Eight well-named hook points (TaskStart, TaskResume, TaskCancel, TaskComplete, PreToolUse, PostToolUse, UserPromptSubmit, PreCompact) each invoking user-authored scripts with JSON stdin / JSON stdout, returning `{cancel: bool}`. Per-project + per-global location, both fire if present, either can block. Platform-aware filenames.
- **Assumed context**: a host runtime with a defined control-flow graph whose edges you can tap. Willingness to put policy in scripts not in the agent.
- **Standalone-extractable?** **Yes** — transplant to any harness by (a) naming the edges in your own graph, (b) defining one JSON schema per edge, (c) shipping a simple script-discovery/exec layer. The exact 8 events chosen by Cline are a reasonable minimum set (start/resume/cancel/complete bookends + pre/post tool execution + user-prompt-arrival + pre-context-compaction).

### P5. `requires_approval` as LLM-marked per-call flag (not fixed allow-list)
- **Description**: Cline's command permission isn't a static allow/deny pattern; the model itself tags each command invocation with `requires_approval: bool` based on command+arguments. User-configurable YOLO/auto-approve layers ride on that tag. A secondary deterministic layer (`CLINE_COMMAND_PERMISSIONS` env JSON) can *additionally* restrict.
- **Assumed context**: tool-calling agents with structured command output; trust in the model's classification (bounded by the deterministic second layer).
- **Standalone-extractable?** **Partial** — the design requires your tool-call protocol to support model-emitted metadata flags. Harnesses where the model only emits the command itself (pure string) cannot do this without a wrapper. Useful as *a pattern*: "ask the model to justify why a call is dangerous, then gate on the justification."

### P6. Memory Bank 6-file typed markdown hierarchy
- **Description**: Six fixed-role markdown files (`projectbrief.md` / `productContext.md` / `activeContext.md` / `systemPatterns.md` / `techContext.md` / `progress.md`) with explicit "activeContext.md updates most frequently" flag, triggered by natural-language commands ("initialize memory bank", "update memory bank", "follow your custom instructions").
- **Assumed context**: agent with a persistent working directory and a "read these files at session start" hook.
- **Standalone-extractable?** **Yes** — the 6-field schema is a reusable vocabulary. Maps crisply against GSD's monolithic `STATE.md`, OMC's `.omc/handoffs/`, OMO's `.sisyphus/notepads/` (candidate axis R). This is candidate-axis-P (stage handoff) or candidate-axis-R (wisdom notepad) territory; Cline's contribution is specifically a **human-authored persistent-knowledge** layer distinct from **agent-generated cumulative** layers.

### P7. `.worktreeinclude` ∩ `.gitignore` file-copy-at-worktree-creation pattern
- **Description**: When spawning a new Git worktree for parallel work, automatically copy files that match *both* `.worktreeinclude` globs AND `.gitignore` globs — i.e., files you want duplicated precisely because they *aren't* tracked by Git but are expensive to regenerate (`node_modules/`, build caches, IDE settings). The set-intersection is the key trick: it prevents accidentally duplicating tracked files.
- **Assumed context**: Git-worktree-aware harness; willingness to document the union rule.
- **Standalone-extractable?** **Yes** — a 5-line shell primitive. The insight is the union rule, not the implementation.

### P8. Single-config two-model assignment (Plan model ≠ Act model)
- **Description**: User can configure separate models for Plan vs Act mode (stronger reasoner for Plan, faster cheaper for Act). Documented cost/quality/speed presets (docs: *"GLM 4.6 / Grok Code Fast"*, *"Claude Opus / Claude Sonnet"*, *"Gemini 3 Flash / Cerebras"*).
- **Assumed context**: harness with a mode/phase split where the phases have asymmetric cognitive needs.
- **Standalone-extractable?** **Yes** — simple to implement on any harness with a mode system. Worth borrowing specifically because it converts an expensive-always pattern into expensive-when-thinking.

### P9. Four-step Deep Planning as discoverable long-form workflow
- **Description**: `/deep-planning` slash command triggers a 4-step workflow: (1) Silent Investigation — Cline reads files, traces deps, builds mental model without asking anything, (2) Discussion — Cline asks *specific* questions informed by what it found (not generic), (3) Plan Creation — writes `implementation_plan.md` with file-by-file changes + dependencies + edge cases + testing strategy, (4) Task Creation — user approves, plan becomes tracked-item task. Model-family-optimized prompts.
- **Assumed context**: harness with slash-command surface; agent with adequate code-reading skill for Step 1.
- **Standalone-extractable?** **Yes** — the step sequence is reusable. The specific insight is **Step 1 is deliberately silent** (context-gather before question-ask) — a commitment to "ask better questions because you understand the codebase first" that most brainstorm/interview patterns (Ouroboros, OMX `$deep-interview`) don't enforce.

## 12. Open questions

- **v3.58 initial subagent PR / commit trace**: The CHANGELOG says "replace legacy subagents with the native `use_subagents` tool" but doesn't link the PR. A next-round probe could grep the git log for "use_subagents" around Feb 2026 to find the authoring commit and see what "legacy" looked like. Would likely require requires-codex-in-main.
- **Concurrency cap for parallel subagents**: Docs don't specify an upper N. Is there a hard cap? Is it per-provider rate-limited? Depends on provider API concurrency policy.
- **v3.77 "Lazy Teammate Mode"**: Only named in CHANGELOG, no docs page found in this sweep. What behavior does it enable?
- **"5M+ installs" claim**: Not verified from primary source; Marketplace API probe needed.
- **Subagent and MCP interaction**: Subagents explicitly cannot access MCP. Does that mean MCP-resource-only or including MCP-prompts-as-slash? Not clarified.
- **Remote config schema**: v3.56 onwards references "remote config" and "enterprise MCP configuration" but does not document the endpoint or schema publicly. Enterprise-tier surface.
- **Explicit benchmarks**: No SWE-bench / internal eval scores appear in docs. Whether internal unpublished evaluations exist is unknown.
- **Repo has `evals` and `testing-platform` directories**: presumably an internal eval framework. Public contents not explored this round.
- **Cline CLI 1.0 (Preview) vs 2.0 breaking changes**: Only partial info (three-core-flows.mdx mentions `cline instance new/list/kill` were removed in 2.0). Full migration shape unexplored.

## 13. Substrate variant matrix (new axis added this analysis)

Cline exists across **six substrates** from one TypeScript core. Matrix of what primitive rides native / is re-implemented / is unique:

| Primitive | VS Code ext | JetBrains (via ACP) | Zed (via ACP) | Neovim (via ACP) | CLI (React Ink TUI) | Cursor / Windsurf |
|---|---|---|---|---|---|---|
| `use_subagents` tool | native | via ACP | via ACP | via ACP | native | native |
| Plan/Act mode toggle | UI button | keybind via ACP | via ACP | via ACP | `Tab` shortcut | same as VS Code |
| Auto-approve UI | VS Code settings panel | IDE settings via ACP | same | same | `/settings` + `Shift+Tab` | same |
| Hooks | `.clinerules/hooks/` + `~/Documents/Cline/Hooks/` | same, platform-aware | same | same | same | same |
| Skills | `.cline/skills/` + global | same | same | same | `/skills` CLI cmd | same |
| MCP | full client | full via ACP | full via ACP | full via ACP | full client | same |
| Worktrees | "New Worktree Window" button | (likely partial) | (likely partial) | (likely partial) | not advertised | same as VS Code |
| Memory Bank | rules-file based | rules-file based | rules-file based | rules-file based | rules-file based | same |
| Headless pipe mode | N/A (GUI-only) | N/A | N/A | N/A | native first-class | N/A |
| Checkpoints | native + Timeline | via ACP | via ACP | via ACP | file-state only (no Timeline) | same as VS Code |
| Enterprise config (SSO/SAML/VPC) | yes | via ACP | via ACP | via ACP | yes | yes |

**Interpretation**: Cline's substrate strategy is **centralized core + universal adapter (ACP) + host-native interaction primitives**. This is a different point in the design space from OMC/OMX (per-host hand-reinvention) or OMO (single-substrate + bespoke inbound Claude Code compatibility). Axis Δ1 ("substrate feature-gap exploitation") now has **three distinguishable patterns** across the corpus:

1. **Per-host hand-reinvention** (OMC↔OMX) — same vocabulary, two independent substrate-specific implementations.
2. **Single-substrate + inbound compatibility loaders** (OMO) — one primary substrate (OpenCode) with targeted loaders for import.
3. **Core + adapter protocol** (Cline/ACP) — one core, one open protocol, N hosts.

Cline v3.58's subagent consolidation illustrates the strength of pattern 3: the `use_subagents` rework could ship to all six substrates in a single release because only the core changed. Contrast OMC/OMX where every `$team`/`$ralph` evolution requires mirrored work in both `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` (Claude Code native) and Rust `omx-runtime-core`.

---

## Verdict on confidence

**High.** Primary sources (GitHub API metadata, release bodies, CHANGELOG, `docs/**/*.mdx` files, `.clinerules/*.md` files, consolidated `llms-full.txt`) are sufficient to map axes 1–10 with direct quotes. Open questions in §12 are specifically about internals not exposed to public docs, not about gaps in my reading. Confidence **medium** on the "5M+ installs" figure (primary source unverified) and on the 2026-02 claim of v3.58 being first-ever subagent introduction (CHANGELOG shows an earlier "Added Subagent support (Experimental)" line at position 787, meaning v3.58 is a consolidation of a pre-existing experimental feature rather than the original addition).
