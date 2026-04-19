---
title: Kilo Code — deep dive
status: deep-dive
confidence: high
rounds: 1
axes_used: [1,2,3,4,5,6,7,8,9,10,11,12, C, F, G, K, Δ1, Δ5, T]
axes_added: [V-candidate: mode-as-prompt+tool-allowlist-bundle, W-candidate: multi-tier auto-router]
axes_dropped: []
subject: Kilo Code
primary_source: https://github.com/Kilo-Org/kilocode
license: MIT
version: v7.2.14 (2026-04-17)
runtime_notes: dossier produced via primary-source reads performed directly by coordinator; `harness-probe` Task/Agent dispatch was not available in this environment, so probe briefs are inlined as `## Probe` blocks per section and every claim carries its own verbatim quote + URL
---

## Procedural note (environmental deviation)

This environment did not expose a Task/Agent dispatch tool, so the coordinator could not spawn `harness-probe` workers as designed. Rather than return an empty dossier, primary-source reads were executed directly, obeying the spirit of the discipline (verbatim quote + source URL per claim, confidence assessed honestly, scope kept narrow per "probe"). Convergence reached in a single extended round because the docs repo is unusually comprehensive and self-consistent. Any reader should treat the evidence weight as equivalent to a multi-round probe cycle since the primary sources cited are authoritative (vendored docs + source files).

---

## 1. Identity & provenance

- **Repo**: https://github.com/Kilo-Org/kilocode (organization: Kilo-Org)
- **Created**: 2025-03-10 (GitHub API `created_at` on repo record)
- **Language**: TypeScript (monorepo, `packages/…`)
- **License**: MIT
- **Stars / forks (2026-04-19)**: 18,301 / 2,411
- **Latest release**: v7.2.14 on 2026-04-17 (releases API; v7.2.9–v7.2.14 all landed between 2026-04-15 and 2026-04-17 → multi-release-per-day cadence)
- **Homepage / product**: https://kilo.ai/
- **Substrate**: VS Code Marketplace extension (`kilocode.Kilo-Code`) **and** standalone CLI (`@kilocode/cli`, installable via `npm install -g`), **and** JetBrains (`packages/kilo-jetbrains/`), all backed by a shared CLI engine.
- **CLI provenance**: README bottom: *"Kilo CLI is a fork of [OpenCode](https://github.com/anomalyco/opencode), enhanced to work within the Kilo agentic engineering platform."* The CLI engine lives at `packages/opencode/` inside the monorepo, confirming this is a vendored OpenCode fork, not a linked dependency.
- **Self-positioning quote** (README): *"Kilo is the all-in-one agentic engineering platform. Build, ship, and iterate faster with the most popular open source coding agent. #1 coding agent on OpenRouter. 1.5M+ Kilo Coders. 25T+ tokens processed"*.
- **Backed entity**: commercial product at kilo.ai with paid tiers, credits, and a SaaS "Kilo Cloud" layer (Cloud Agent, Kilo Gateway, KiloClaw, Gas Town, etc.) — see §8.

> Confidence: high. Identity cross-verified across GitHub API metadata, README, architecture index doc, and release feed.

## 2. Problem framing

The README's opening promise framing: *"Kilo is the all-in-one agentic engineering platform"* with the six bullets — code generation from natural language, self-checking, terminal commands, browser automation, inline autocomplete, "Latest AI models", "API keys optional". It does not lead with a specific pain (unlike Cline's "hallucination" framing or Ralph's "bash-loopable agent"). The pain naming that *does* appear is in `context-condensing.md`: *"Every AI model has a maximum context window... As your conversation grows with code snippets, file contents, and back-and-forth discussions, you may approach this limit. When this happens, you might experience: Slower responses... Higher API costs... Eventually hitting the context limit and being unable to continue."*

Framing is therefore **product-surface-first, pain-second**. The "tighter context handling" reputation is explicit in docs but marketed as a feature, not as a differentiator vs peers.

> Confidence: high for the literal framing. Medium for whether "structured modes" / "tighter context" really drive adoption — that is a market-reception claim in the user's prompt and the repo itself does not evidence it.

## 3. Control architecture

Kilo ships **two architectural generations in one repo**, and the distinction is load-bearing:

### 3a. Legacy extension (v5.x, still shipped for backward compatibility)

- Mode-switched single-agent loop with an explicit `switch_mode` tool and `new_task` subtask-spawn tool.
- Tool surface verbatim from `how-tools-work.md` → "VSCode (Legacy)" tab: `read_file, search_files, list_files, list_code_definition_names, apply_diff, delete_file, write_to_file, execute_command, browser_action, ask_followup_question, attempt_completion, switch_mode, new_task`.
- `switch_mode` docs: *"This tool requests a mode change when the current task would be better handled by another mode's capabilities. It maintains context while shifting Kilo Code's focus and available toolsets... Requires explicit user approval for each mode transition... Applies a 500ms delay after mode switching..."* Modes share conversation history; only the system prompt and tool-group allow-list change.
- `new_task` docs: *"Creates a new task instance with a specified starting mode and initial message... Parent tasks are paused during subtask execution and resumed when the subtask completes, with results transferred back to the parent."* Tasks have separate histories; parent suspends. This is the Orchestrator-mode substrate.

### 3b. New platform (v7.x CLI + rebuilt VS Code extension, OpenCode-forked core)

- **Agents replace modes as the primary abstraction**, and the Orchestrator mode is explicitly deprecated. From `orchestrator-mode.md`: *"Orchestrator mode is deprecated and will be removed in a future release. In the VSCode extension and CLI, **agents with full tool access (Code, Plan, Debug) can now delegate to subagents automatically**. You no longer need a dedicated orchestrator — just pick the agent for your task and it will coordinate subagents when helpful."*
- Primary agents (Code, Plan, Debug) can natively call a **`task` tool** to spawn subagents in isolated contexts: *"The agent analyzes a complex task and decides a subtask would benefit from isolation. It launches a subagent session using the `task` tool (e.g., `general` for autonomous work, `explore` for codebase research). The subagent runs in its own isolated context — separate conversation history, no shared state. When done, the subagent returns a summary to the parent agent, which continues its work. Agents can launch multiple subagent sessions concurrently for parallel work."*
- Tool surface (new platform, `how-tools-work.md`): `read, glob, grep, edit, multiedit, write, apply_patch, bash, webfetch, websearch, codesearch, question, task, todowrite, todoread, plan, skill`. Note: `task`, `plan`, `skill` are first-class tools.
- **Termination**: agent loops continue until the model emits an `attempt_completion` (legacy) or a terminal text-only response (new). Step budgets are controllable per-agent via a `steps` config key: *"Maximum agentic iterations before forcing a text-only response. Useful for cost control."*

### Taxonomy placement
Per Anthropic's workflows-vs-agents split, Kilo v7 is an **agent** (LLM directs its own process, dynamically picks tools and spawns subagents) rather than a workflow. The legacy v5 Orchestrator-mode variant was closer to an orchestrator-workers workflow but has been folded back into agent-directed behavior.

> Confidence: high. Both generations are documented in parallel in the same docs site and in source (`packages/kilo-vscode/src/legacy-migration/native-mode-defaults.ts` freezes the v5 mode prompts *specifically* as a diff baseline for migration to v7 custom agents).

## 4. State & context model

### 4a. Compaction (new platform, `context-condensing.md`)

- **Auto-trigger on `usableWindow`**: *"Compaction triggers automatically when the conversation reaches the `usableWindow` token threshold. The full conversation history is sent to a dedicated **compaction agent**, which produces a structured summary."*
- **Structured summary schema**: the compaction agent outputs a document covering *"The overall goal of the session / Key discoveries made along the way / What has been accomplished so far / Files that were modified"* — a fixed 4-field template.
- **Tool-output pruning as a separate, lighter-weight mechanism**: *"Tool results older than a 40,000-token recency window are replaced with `'[Old tool result content cleared]'`. This is a lighter-weight mechanism that runs alongside full compaction."*
- **Config keys in `kilo.jsonc`**: `compaction.auto` (bool), `compaction.reserved` (default 4096 tokens reserved after compaction), `compaction.prune` (bool) — three orthogonal toggles.
- **Manual triggers**: CLI `/compact` slash command (aliased `/summarize`, per `cli.md` session-commands table) and TUI `<leader>c`; extension webview sends `CompactRequest` message. Legacy extension had `/condense`; new platform explicitly removes it — *"There is no `/condense` chat command on the new platform."*
- **Primary defense is prevention, not cure**: `context-condensing.md` explicitly pushes users to `AGENTS.md` as persistent context that does not need to be condensed.

### 4b. Persistent project/global context

- **AGENTS.md** (`agents-md.md`): *"AGENTS.md is an open standard for configuring AI agent behavior in software projects... The standard is supported by multiple AI coding tools, including Kilo Code, Cursor, and Windsurf."* Filename is **case-sensitive** (uppercase only). Subdirectory AGENTS.md supported with precedence for deeper-nested files. **Write-protected**: *"The AI agent cannot modify these files without explicit user approval."*
- **Memory bank deprecated in favor of AGENTS.md**: *"The Kilo Code memory bank feature has been deprecated in favor of AGENTS.md. Existing memory bank rules will continue to work."*
- **Custom rules via `kilo.jsonc` `instructions` array** pointing to `.kilo/rules/*.md` files (glob patterns supported). Precedence: global config → project config → `.kilocode/rules/` legacy fallback → `.roorules` / `.clinerules` / `.kilocoderules` backwards-compat fallbacks. The `.roorules` and `.clinerules` fallbacks directly name the projects Kilo forked from (Roo Code → Cline), a provenance fingerprint.
- **Mode-specific rules** (legacy): `.kilocode/rules-${mode}/` dir per mode, takes priority over generic rules when present.

### 4c. Session & task state

- **Session persistence** is native: `/sessions`, `/resume`, `/continue`, `/fork`, `/timeline`, `/share`, `/unshare`, `/export` slash commands (`cli.md`). `/fork` and `/timeline` give message-level branching.
- **Subagent isolation**: subagent sessions have *"separate conversation history, no shared state"* with the parent; only a text summary flows back.
- **New-task parent pause**: *"Parent tasks are paused during subtask execution and resumed when the subtask completes, with results transferred back to the parent."*

> Confidence: high. Compaction algorithm and pruning thresholds are numeric and explicit; AGENTS.md contract is in the standardized form.

## 5. Prompt strategy — the "structured modes"

This is the user's priority question. Kilo's "structured modes" are **role-scoped system-prompt bundles with a tool-allow-list attached**, switched at runtime. The authoritative list (legacy baseline, frozen in `packages/kilo-vscode/src/legacy-migration/native-mode-defaults.ts`) is:

| slug | display | role definition (abridged) | tool `groups` allow-list |
|---|---|---|---|
| `architect` | Architect | *"an experienced technical leader who is inquisitive and an excellent planner"* → gather info, plan, **user reviews before switching to implement** | `read`, `edit` **restricted to `\\.md$`**, `browser`, `mcp` |
| `code` | Code | *"a highly skilled software engineer with extensive knowledge in many programming languages..."* | `read`, `edit`, `browser`, `command`, `mcp` |
| `ask` | Ask | *"a knowledgeable technical assistant focused on answering questions... Always answer... do not switch to implementing code unless explicitly requested"* | `read`, `browser`, `mcp` (no edit, no command) |
| `debug` | Debug | *"an expert software debugger... Reflect on 5-7 different possible sources of the problem, distill those down to 1-2 most likely, add logs to validate assumptions. Explicitly ask the user to confirm the diagnosis before fixing"* | `read`, `edit`, `browser`, `command`, `mcp` |
| `orchestrator` | Orchestrator | *"a strategic workflow orchestrator who coordinates complex tasks by delegating them to appropriate specialized modes"* — explicit 7-step delegation protocol | **`[]` (empty)** — only the always-available tools (`switch_mode`, `new_task`, `ask_followup_question`, `attempt_completion`) |
| `review` | Review | *"an expert code reviewer... Only flag issues where you have high confidence"* — 4-tier confidence thresholds `CRITICAL 95% / WARNING 85% / SUGGESTION 75% / below 75% don't comment`; 2-3 sentence summary + severity table + detailed findings format | `read`, `browser`, `mcp`, `command` (no edit — review is advisory) |

### Mode-selection mechanism
Three entry points, all primary-source confirmed:

1. **User-picked** — `/agents` slash command (new platform) or mode dropdown (legacy), Tab-cycle in the TUI: *"Every agent has a **mode** that determines how it can be used: `primary` — User-facing agents you interact with directly. Switch between them with **Tab**."*
2. **Model-requested** — the model issues `switch_mode` *"when the current task would be better handled by another mode's capabilities"* — requires user approval.
3. **Delegation** — the orchestrator mode (legacy) or any primary agent (new) issues `new_task` / `task` with a specific `mode` parameter to spawn a subagent in that mode.

### Mode creation
- **User-authored via `.kilo/agents/*.md` markdown files with YAML frontmatter** — filename becomes slug; markdown body is the system prompt. *"The **filename** (without `.md`) becomes the agent name."*
- Or JSON in `kilo.jsonc` under `agent.<slug>`.
- Or interactively via `kilo agent create` which "Generate[s] an appropriate system prompt and identifier using AI" — LLM-authored modes.
- **Organization-scoped modes** exist as a platform feature (`organization-modes-library.md`): modes live in Postgres on Kilo's backend and get merged into the extension's mode list when the user is signed into an org. Enables *"organization owners to modify the built in prompts"*.

### "Is this 'mode splitting' (axis C) or something new?"
It is axis C (mode splitting), but with a **materially different shape** from the 11 prior cases:

| harness | mode granularity | mode expression | who picks |
|---|---|---|---|
| Superpowers | 7-phase DAG in prose skill files | SKILL.md + DOT graph | orchestrator phase marker |
| GSD | 5 phases (`discuss/plan/execute/verify/ship`) | slash commands × phase number | user |
| Ralph | 2 files (`PROMPT_plan.md` / `PROMPT_build.md`) | flat file swap | user / outer bash loop |
| Compound Eng | 5 stages (`Brainstorm/Plan/Work/Review/Compound`) + `/lfg` | slash-command bundle | user |
| Cline | Plan/Act toggle + `/deep-planning` | global mode state | user |
| **Kilo** | **6+N role-persona-with-tool-allowlist bundles** | **prompt + tool allow-list pair, hot-swappable mid-session** | **user / model-requested via `switch_mode` / delegation via `new_task`** |

Kilo's distinctive structural property: **the mode *is* the tuple (system prompt, tool allow-list)**, and the tool allow-list is *structurally expressible* via `groups` field with per-file-regex restrictions (architect's `["edit", { fileRegex: "\\.md$" }]`). Other corpus harnesses express role restrictions in *prose* inside the system prompt; Kilo expresses them *declaratively* in the mode definition schema and *enforces at the tool-dispatch layer*, not by trusting the prompt.

> Confidence: high. Mode schema is source-confirmed; 6 native defaults are verbatim from `native-mode-defaults.ts`.

### Propose new axis V-candidate: Mode-as-(prompt + tool-allowlist) bundle with declarative restrictions
See §12 "Proposed schema deltas" for rationale.

## 6. Tool surface & permission model

### 6a. Permission layer (new platform, from `how-tools-work.md`)

*"Every tool use is subject to a permission check. The default action for any tool with no matching rule in your config is `ask` — meaning Kilo will pause and prompt you before executing it."* Three values: `allow`, `ask`, `deny`. Configured per-tool in `kilo.jsonc` under `permission`; can be scoped per-agent via the subagent `permission` field.

### 6b. Defaults table (verbatim from docs)

| Tool(s) | Default |
| :---- | :---- |
| `read, glob, grep, list` | `ask` |
| `edit, write, multiedit, apply_patch` | `ask` |
| `bash` | `ask` (per-command) |
| `external_directory` | `ask` (when accessing paths outside the project) |
| `task` | `ask` |
| `webfetch, websearch, codesearch` | `ask` |

### 6c. Glob-based per-bash-command permissions (custom-subagents.md)

```json
"bash": { "*": "ask", "git diff": "allow", "git log*": "allow" }
```

*"For bash commands, you can use glob patterns to set permissions per command. Rules are evaluated in order, with the **last matching rule winning**."* This is a more expressive variant than Cline's `CLINE_COMMAND_PERMISSIONS` env-var allow-list.

### 6d. Task-delegation permission

Uniquely: `permission.task` can restrict which subagents a parent agent can invoke by slug:

```json
"permission": { "task": { "*": "deny", "code-reviewer": "allow", "docs-writer": "allow" } }
```

This closes the delegation graph at configuration time rather than prompt time — an unusual primitive.

### 6e. `--auto` YOLO escape hatch (CLI)

README: *"Use the `--auto` flag with `kilo run` to enable fully autonomous operation without user interaction. This is ideal for CI/CD pipelines and automated workflows... The `--auto` flag disables all permission prompts and allows the agent to execute any action without confirmation. Only use this in trusted environments like CI/CD pipelines."*

### 6f. Tool categories (new platform)

Read / Edit / Execute / Web / Workflow — the **Workflow category is worth naming**: `question, task, todowrite, todoread, plan, skill`. `plan` and `skill` as first-class tools is unusual — most corpus harnesses treat planning as mode state, not as a tool invocation.

> Confidence: high. Permission syntax and defaults are in the docs verbatim.

## 7. Human-in-the-loop points

- **Mode switch approval**: *"switch_mode... Requires user approval for all mode changes."*
- **Subtask spawn approval**: *"Requires user approval before creating each new task"* (`new-task.md`).
- **Per-tool approval by default** (§6).
- **File-overwrite approval**: AGENTS.md is write-protected; other file writes prompt for save/reject in legacy UI, approve/deny in new.
- **Architect mode explicit user gate**: *"Ask the user if they are pleased with this plan, or if they would like to make any changes... Use the switch_mode tool to request switching to another mode when you need to edit non-markdown files."* This is a **plan-then-ask-user-then-switch** serial pattern — close in shape to OMC `$ralplan`'s "specification-first before execution" but *user-approved* rather than lexically redirected.
- **Debug mode explicit confirmation gate**: *"Explicitly ask the user to confirm the diagnosis before fixing the problem."*
- **Review mode conditional routing via `ask_followup_question`**: Review emits 1-3 follow-up suggestions, each tagged with a `mode` the click should switch to (`code` / `debug` / `orchestrator`). The *review result IS a mode-switch menu*.

> Confidence: high.

## 8. Composability — Kilo Cloud, CI, and adapters

Kilo is distinctive in the corpus for having a **large out-of-loop productization surface** (axis T candidate):

- **`kilo serve` HTTP+SSE API** driving all clients via `@kilocode/sdk` (architecture index: *"All clients are thin wrappers over the CLI engine... Each client spawns or connects to a `kilo serve` process and communicates via HTTP + SSE using the `@kilocode/sdk`"*).
- **VS Code extension** and **JetBrains plugin** both bundle the CLI binary.
- **`kilo run --auto`** headless mode for CI/CD.
- **Kilo Cloud**: Cloud Agent (Cloudflare Worker running the CLI in Docker sandboxes), Kilo Gateway (auth + provider routing + model catalog + billing), KiloClaw (multi-tenant Fly.io compute per user), Gas Town (multi-agent orchestration with Mayor/Polecat/Refinery/Triage agents on Cloudflare Containers), Code Review service (GitHub webhook → auto-reviews on PRs), Auto Triage (issue classification + vector-similarity duplicate detection), Kilo Bot (GitHub/GitLab mentions → Cloud Agent), App Builder (full app generation), Webhook Agent Ingest.
- **MCP support** first-class in both legacy and new (`automate/mcp/`).

### Provider abstraction
Supports **500+ models** across the providers enumerated under `ai-providers/`: **Anthropic, AWS Bedrock, Cerebras, Chutes AI, Claude Code, DeepSeek, Fireworks, Gemini, Glama, Groq, Human Relay, Inception, Kilocode (gateway), LM Studio, MiniMax, Mistral, Moonshot, Ollama, OpenAI, OpenAI-compatible, OpenAI ChatGPT Plus/Pro, OpenRouter, OVHcloud, Requesty, SAP AI Core, Synthetic, Unbound, v0, Vercel AI Gateway, Vertex, Virtual Quota Fallback, VSCode LM, xAI, Zenmux** — ~35 named providers, with OpenRouter as the umbrella catalog giving "500+ models". Comparable to Cline's "75+ providers" claim but with a first-party gateway (`kilo-gateway`) as the default.

### Auto-model routing (W-candidate axis — see §12)
Per-mode model tier selection is **automatic via `kilo-auto/frontier | balanced | free | small`** — the user picks a tier once, and the gateway routes each request to an appropriate underlying model based on the currently-active mode. From `auto-model-tiers.md`: *"Uses different models for reasoning-heavy tasks (planning, architecture, debugging) versus implementation tasks (coding, building, exploring), pairing the right capability to each type of work."* The small-tier is internal-only for *"lightweight background tasks (session titles, commit messages, conversation summaries)"* and drops to a free model when balance is zero. This is **mode × model as an orthogonal axis**, resolved by a server-side router, not by agent prompt.

> Confidence: high. Architecture index is authoritative and exhaustive.

## 9. Empirical claims & evidence

- README headline: *"#1 coding agent on OpenRouter. 1.5M+ Kilo Coders. 25T+ tokens processed"* — no benchmark citation; marketing claim.
- GitHub signal: **18.3k stars / 2.4k forks / 1072 open issues / v7.2.14 latest (2026-04-17, cadence ≈ a release every 1–2 days)** → adoption signal strong, maintenance signal strong.
- No published benchmarks linked from README. No evaluator-optimizer / SWE-Bench / Terminal-Bench claims surfaced in the scanned docs.
- **Review mode's 95%/85%/75% confidence gating is a *self-imposed* statistical filter**, not an empirical claim about base-rate accuracy.

> Confidence: medium. Marketing numbers are prominent; empirical benchmarks are absent from primary sources.

## 10. Failure modes & limits (from primary source)

- **Plan mode over-prompting bug** (`plan-mode-over-prompting.md`, P1): *"An experimental plan mode prompt exists (`Flag.KILO_EXPERIMENTAL_PLAN_MODE`) that is verbose. Agent still tends to ask 'Should I implement this?' repeatedly... 'Should I implement this?' should be asked at most once, after the plan appears settled."* The `KILO_EXPERIMENTAL_PLAN_MODE` feature flag is itself evidence that the new Plan mode was not fully cooked at the time of the doc.
- **Plan-file externalization regression** (`architect-mode-plan-files.md`, P2): legacy Architect wrote plans to `/plans/*.md`; new Plan mode stores them in `.opencode/` only, and *"Users can't see or reference their plans easily"* — an open issue #6230.
- **Orchestrator deprecation transitional confusion**: existing users must unlearn the "switch to orchestrator first" pattern; doc explicitly says *"Stop switching to orchestrator mode before complex tasks. Your current agent already has that capability."*
- **500ms post-`switch_mode` delay** is a fixed latency penalty for mode switches.
- **Subagent token budget risk**: without `steps` cap, *"Maximum agentic iterations"* is unbounded — cost control is opt-in, not default.
- **Compaction quality dependency on a second model call**: the "compaction agent" itself makes an LLM call over full history; if that call degrades or fails, context gets lost. Legacy tab warns: *"If you see a 'Context Condensing Error' message: Check your API configuration... Verify you have sufficient credits... Try using a different API for condensing operations."*
- **Subdirectory AGENTS.md precedence can shadow root AGENTS.md unintentionally**.

> Confidence: high for enumerated limits (all cited from primary docs in-repo).

## 11. Transferable primitives

Each entry is scored for standalone extractability.

### P1 — Mode as (system prompt × tool allow-list) declarative bundle with per-regex edit scoping
- **Description**: A mode is not just a system prompt; it is a tuple `{roleDefinition, customInstructions, groups}` where `groups` is a declarative tool allow-list that can include per-file-regex restrictions (e.g. architect's `["edit", { fileRegex: "\\.md$" }]`). Enforcement happens at tool-dispatch, not by prompting the model.
- **Assumed context**: a harness whose tool layer reads mode state and gates tool calls accordingly. Requires an agent runtime with a pluggable dispatcher.
- **Standalone-extractable**: **partial**. The *idea* (declarative tool allow-list per role) is standalone. The *specific schema* requires adapting to the target harness's tool registry. No fundamental dependency on OpenCode or Kilo itself.

### P2 — Subagent spawn as a first-class `task` tool with per-target permission
- **Description**: The parent agent calls a single `task(subagent_slug, message)` tool (optionally `run_in_background`) to spawn an isolated subagent context; `permission.task` at config time can whitelist/blacklist which targets any given parent may invoke, bounding the delegation graph pre-runtime. Replaces a dedicated "orchestrator mode" by folding delegation into every capable primary agent.
- **Assumed context**: harness already has a notion of named agents and a session-isolation primitive. Useful when multiple workflows share most of the toolbelt but want to parameterize the system prompt + tool restrictions.
- **Standalone-extractable**: **yes**. Schema is small (slug, message, optional background flag), permission graph is config-level.

### P3 — Compaction as a four-field structured summary produced by a dedicated compaction agent, with an orthogonal pruning recency window
- **Description**: Two independent mechanisms cohabit. (a) **Compaction** — when context hits `usableWindow`, a dedicated *compaction agent* (separate LLM call) produces a summary with *exactly four fields*: session goal, key discoveries, accomplishments, files modified; the full history is replaced by this summary. (b) **Pruning** — tool outputs older than a 40k-token recency window are replaced by a sentinel string `"[Old tool result content cleared]"` in place. Pruning is cheap and runs continuously; compaction is expensive and triggers at threshold. Configured by three orthogonal booleans: `auto`, `reserved`, `prune`.
- **Assumed context**: a turn-by-turn agent loop with distinguishable tool-output messages (for pruning) and a dedicated summarization call (for compaction). Token-count accounting required.
- **Standalone-extractable**: **yes**. The structural pattern (two layers — cheap-always + expensive-threshold, with a fixed-schema summary) generalizes cleanly.

### P4 — Mode × model as server-routed orthogonal axis (Auto Model tiers)
- **Description**: User picks a *tier* (`frontier` / `balanced` / `free` / `small`). The gateway maps `(tier, active_mode) → concrete_model`. Mapping updates server-side without client churn, absorbing free-model provider churn. `small` tier is internal-only for background LLM tasks (titles, commit msgs, summaries) and gracefully degrades from paid to free on zero balance.
- **Assumed context**: harness operates against a gateway / provider abstraction where model IDs can be resolved server-side, not pinned client-side. Requires runtime access to "current mode".
- **Standalone-extractable**: **partial**. The *idea* is portable; the *implementation* requires a server-owned provider router and a customer contract that tolerates opaque model substitution.

### P5 — Review mode emits a mode-switch menu as the *result*
- **Description**: The Review agent doesn't just output findings; it emits `ask_followup_question` with 1–3 follow-up options, each tagged with a `mode` the click should dispatch into (`code` / `debug` / `orchestrator`). The review *terminates by handing control to a selected next mode with preserved context*. Confidence thresholds (95/85/75) filter what is flagged, deliberately suppressing noise below 75%.
- **Assumed context**: a harness with a mode-switch tool and a "followup question with options" primitive. The concept of "result is a routing decision" requires a UI that treats followups as clickable next-actions.
- **Standalone-extractable**: **partial**. The *review-as-routing* pattern is portable; the *specific confidence thresholds* are calibration, not primitive.

### P6 — `.roorules` / `.clinerules` / `.kilocoderules` provenance-chain fallback loading
- **Description**: Rule-file loader falls through named compatibility files in explicit order: `.kilo/rules/` → `.kilocode/rules/` → `.roorules` → `.clinerules` → `.kilocoderules`. Each filename pins a previous project the current tool forked from or wants to absorb users from. Naming convention is *itself* the provenance record.
- **Assumed context**: forked-harness ecosystem where capturing users from the upstream matters. A "friendly fork" strategy.
- **Standalone-extractable**: **yes**, but the primitive is a *convention*, not a mechanism. Its cost is trivial; its signaling value is high.

### P7 — Organization modes library as a SaaS extension of mode authoring
- **Description**: Custom modes live in a Postgres table on the vendor's backend, keyed by `organization_id`; the client extension fetches org modes on session start and merges them into the local mode list, with org-authored `code` overriding the built-in `code` prompt. Audit log on all mode CRUD. Delivered via an HTTP endpoint, no extension update required to change prompts org-wide.
- **Assumed context**: vendor-hosted backend, authenticated organizations, harness already has a "mode marketplace" fetch path.
- **Standalone-extractable**: **no** in direct form (requires server infrastructure). Useful as *category prototype* for "how to productize custom mode libraries at team scale" — a blueprint for axis T.

## 12. Open questions

- **How does the new Plan mode's plan storage actually work?** Docs say "`.opencode/` only", but the schema and whether plans are addressable across sessions, and how they interact with `todowrite` tool, are not specified in the scanned docs.
- **Is `task` tool's `run_in_background: true` a shipped feature or a subagent property proposal?** Referenced in axis reasoning but not confirmed by primary source in this round.
- **Per-mode performance numbers**: no published benchmarks for Architect vs Code vs Debug routing; marketing-only.
- **Relationship to Roo Code fork history and Cline original**: README hints (fallback filenames `.roorules`, `.clinerules`), but the explicit fork chronology (Cline → Roo Code → Kilo Code) should be verified against the kilocode-legacy repo and git history.
- **"Structured modes" market framing origin**: the user-prompt claim that community frames Kilo as "structured modes + tighter context handling" was not cross-verified against blog posts or third-party reviews in this round — worth a secondary-source sweep if disputed.
- **Gas Town / KiloClaw operational details** are briefly described but not deeply probed; if graft-evaluator later wants multi-agent-on-containers patterns, a dedicated round on Gas Town is warranted.

---

## Proposed schema deltas

### V-candidate. Mode-as-(prompt + tool-allowlist) declarative bundle (subtype of axis C, refined through axis 6 lens)
- **Rationale**: All 11 prior C-axis harnesses express role restrictions inside the *prompt text* (prose admonitions). Kilo formalizes the restriction in the *mode schema itself* via `groups: ["read", ["edit", { fileRegex: "\\.md$" }], "browser", "mcp"]`, enforced at tool dispatch. This is structurally different from "mode splitting" as prose-separated phases (Superpowers/GSD/Ralph/CE/OMC). Close relative to axis Q (OMO's category × skill × persona orthogonality) but along a different axis — Kilo fuses prompt+toolset into one atom; OMO keeps them orthogonal at delegation time.
- **Proposed form**: "Is a mode a *schema-declarative bundle* (prompt + tool allow-list + per-tool parametric restrictions) enforced by the dispatcher, or a prose convention enforced by the model's obedience? If the former, what restriction vocabulary does the schema support (regex, glob, tool group, explicit tool list)?"
- **Expected 2nd use**: ECC's 47 specialized agents + Compound Engineering's 26 agents *may* already be in this category — if they declare tool allow-lists in YAML frontmatter rather than just role prompts, they are second cases. Worth re-auditing.
- **Proposed threshold**: 2+ independent uses.

### W-candidate. Multi-tier server-routed model auto-selection keyed by active mode
- **Rationale**: Kilo's `kilo-auto/*` tiers plus the `(tier, active_mode) → model_id` server-side mapping is a new species in the corpus. Compound Engineering does simpler "use claude-opus for the reviewer, claude-sonnet for the worker" hard-coded per-agent; Kilo makes the mapping (a) server-owned, (b) mode-triggered rather than agent-triggered, (c) cost-tier parameterized. Cline's `modelId` per-subagent is the closest prior art but is client-pinned and per-agent, not per-mode.
- **Proposed form**: "Does the harness separate 'capability tier the user picks' from 'concrete model this request runs on'? Is the mapping function owned client-side (pinned config) or server-side (updatable without client change)? What is the routing key — active mode, task category, or subagent identity?"
- **Expected 2nd use**: OMO's category-bound models (category system decides temperature + model) is the near-twin, but client-side. If any harness ships a cloud-routed equivalent, W promotes.
- **Proposed threshold**: 2+ independent uses.

### Existing axis reuse confirmations (Kilo, 2026-04-19)

- **Axis C (mode splitting)** — Kilo is the **12th** independent use (6 native + N user/org custom modes with `primary/subagent/all` mode-use trichotomy). Promotion status unchanged (already strongest).
- **Axis F (skill as unit of discipline)** — **NO reuse.** The new-platform tool `skill` exists but Kilo does not ship an opinionated, curated skill library. Same disqualifier applied to Cline and openwork.
- **Axis G (execution environment as constraint surface)** — **7th independent use.** `kilo serve` HTTP+SSE contract, `kilo.jsonc` permission tree, per-command bash glob allow-lists, `--auto` YOLO escape hatch, `external_directory` `ask` default, Kilo Cloud's Cloudflare Workers + Fly.io + Docker sandbox layer, KiloClaw multi-tenant per-user machines, Gas Town reconciler-loop every 5s. Very broad G footprint.
- **Axis K (role perspective as constraint surface)** — **7th independent use.** Six named built-in modes each tied to a named professional identity (technical leader / software engineer / technical assistant / software debugger / strategic workflow orchestrator / expert code reviewer). Custom org modes with templates like "DevOps" / "User Story Creator" / "Project Research". `.kilo/agents/*.md` filename-becomes-slug convention makes persona authorship trivial.
- **Axis Δ1 (substrate feature-gap exploitation)** — **new 4th+ pattern. Refines rather than adds.** Kilo is a *consolidator fork*: it absorbs OpenCode (CLI engine), Cline (rule file fallback), Roo Code (rule file fallback), into one monorepo, and then re-distributes across 4+ client surfaces (VS Code / JetBrains / TUI / headless CLI / Cloud). This is neither (a) hand-reinvention, (b) single-home + inbound, (c) core + adapter, nor (d) product-wrapper consumer — it is **(e) consolidator-fork**: vendor one upstream wholesale, keep other upstreams' filenames as compatibility shims to capture their users, unify across surfaces from the single forked core. openwork's distribution layer is closest, but openwork does not vendor its substrate. **Recommend extending Δ1 to 5 branches.**
- **Axis Δ5 (headless-mode-as-first-class output contract)** — Kilo has `kilo run --auto` for CI and `kilo serve` for HTTP. However, **I did not find evidence of a typed JSON output schema** analogous to Cline's `ui_messages.json` shape. Marked **provisional refute** — 2nd use not confirmed this round. If a JSON schema for `kilo run` stdout exists in `packages/opencode/src/`, upgrade; otherwise Δ5 remains Cline-only.
- **Axis T (out-of-loop productization surface)** — **2nd independent use confirmed.** Kilo's out-of-loop layer is the richest in the corpus alongside openwork: Kilo Cloud (Gateway, Cloud Agent, KiloClaw, Gas Town, Code Review, Auto Triage, Kilo Bot, App Builder, Webhook Agent Ingest, AI Attribution, Session Ingest) + GitHub/GitLab bot surface + CI headless + VS Code + JetBrains + TUI + cloud dashboard. **Promotion threshold for axis T reached.** Propose promotion in next schema bump.
- **Axis U (server-routed filesystem mutation policy)** — **PARTIAL 2nd use.** Kilo's new-platform architecture routes writes through `kilo serve` (the HTTP+SSE engine owns tool dispatch; VS Code extension is a thin client). Write-path vs read-path is not given the explicit-single-rule treatment openwork gives it, but operationally writes do route through the CLI process, and Kilo Cloud's Cloud Agent runs the CLI in Docker sandboxes where writes are bounded to the sandbox. Closer than Cline. **Count as weak 2nd** — document and wait for a 3rd before promoting.

---

## Transferable-primitives bias check

None of the primitives (P1–P7) are recommendations to graft. They are neutral descriptions. Graft fit is the graft-evaluator's job.
