---
title: oh-my-openagent (OMO) — OpenCode-native multi-model harness, the origin of `ultrawork` and `Ralph Loop`
slug: omo
date: 2026-04-19
author: "@code-yeongyu (YeonGyu-Kim, Sionic-AI, Seoul) — NOT the same person as Yeachan Heo (OMC/OMX author)"
primary_sources:
  - https://github.com/code-yeongyu/oh-my-openagent
  - https://ohmyopenagent.com/
  - https://sisyphuslabs.ai/
topic: harness
tags: [harness, opencode, multi-model, ralph, ultrawork, sisyphus, korean-author, hashline, intent-gate]
status: deep-dive
confidence: high
rounds: 2
axes_used: [1,2,3,4,5,6,7,8,9,10,11,12,13-authorship-and-provenance-delta,14-transferable-primitives-moved-from-11]
axes_added: [13-authorship-and-provenance-delta]
axes_dropped: []
candidate_axis_proposals_tested: [Δ1-substrate-feature-gap (refuted — OMO is not a multi-substrate variant), Δ2-consensus-planning-as-gate (partially refined — different mechanism), Δ3-stage-handoff-as-RPC (refuted — OMO's handoff is single-session context compaction, not stage-to-stage)]
probe_method: primary-source reads via GitHub REST + Search APIs, raw.githubusercontent.com. Per user directive, codex:rescue NOT used and NOT available in this sub-agent.
---

## TL;DR (3 lines)
OMO (oh-my-openagent, formerly oh-my-opencode) is a **52,694★ OpenCode plugin by @code-yeongyu (YeonGyu-Kim / Sionic-AI)** — a **different author** from OMC/OMX's Yeachan Heo. Git history proves OMO is the **origin** of `ultrawork` (2025-12-13), `Ralph Loop / /ulw-loop` (2025-12-30), the **Greek-mythology agent roster** (Sisyphus/Prometheus/Hephaestus/Atlas/Oracle/Metis/Momus), **boulder-state**, **IntentGate** (multi-lingual keyword classifier), **Hashline** (LINE#ID content-hash edit tool), and the 3-layer Prometheus→Atlas→Sisyphus-Junior orchestration — while OMC was explicitly launched 2026-01-09 as a "**Complete port of oh-my-opencode to Claude Code**" (commit `cd98f12fac` message verbatim). However, OMO does **NOT** have `$deep-interview` (OMC invention, Ouroboros-inspired, 2026-03-02) or `$ralplan` (OMC invention, 2026-01-22); those are genuine OMC additions. The **OpenClaw** external-notification gateway travels in the reverse direction (OMC 2026-02-25 → OMX 2026-02-26 → OMO 2026-03-16 with env var rename `OMX_OPENCLAW → OMO_OPENCLAW`). Verdict: **OMO and OMC/OMX are two loosely-coupled ecosystems by two different authors who cross-port each other's primitives**, not a single-author family. The shared vocabulary is a **mixed-origin patchwork**, not a single lineage.

## Proposed schema deltas — corrections and refinements

### Δ1. "Substrate feature-gap exploitation" — REFUTED for OMO (still valid for OMC↔OMX)
- **Finding**: OMO is a single-substrate harness (OpenCode plugin only). It does NOT provide a Claude Code port or Codex port of itself. Rather, OMO declares **Claude Code compatibility** ("Your hooks, commands, skills, MCPs, and plugins? All work here unchanged. Full compatibility, including plugins." — README) as an **inbound** adapter. This is a different architectural posture: OMO is a "sink" that absorbs Claude Code ecosystem artifacts, not a "source" that emits the same harness to multiple substrates.
- **Implication for Δ1**: The candidate axis remains valid specifically for OMC↔OMX as the natural experiment, but OMO refutes the more general claim that "multi-stars Korean-authored harnesses are all multi-substrate." OMO is a prime example of **substrate commitment as strategy** (explicit choice of OpenCode because "OpenCode won" — author's note in README).
- **Refined form**: "When a harness operates on a single substrate, does it position itself as (a) substrate-bound (OMO — OpenCode only, with inbound adapters), (b) substrate-agnostic layer (OMC/OMX — same vocabulary on two substrates), or (c) host-of-substrates (CE — can emit to multiple IDEs)? This is a useful typological axis in its own right."

### Δ2. "Consensus planning as execution gate" — REFINED
- **Finding**: OMO has a **different shape** of pre-execution gating. OMC/OMX's `$ralplan` is a lexical-specificity heuristic that rejects under-specified prompts. OMO's equivalent is **two-layered**:
  1. **IntentGate** (multi-lingual regex keyword classifier in `src/hooks/keyword-detector/`) — routes messages into `ultrawork / search / analyze` modes based on detected intent keywords (including Korean, Japanese, Chinese, Vietnamese variants). This is **intent routing**, NOT specificity gating. No rejection — just mode switching.
  2. **Ultrawork-mode system prompt** (`src/hooks/keyword-detector/ultrawork/default.ts`) — once ultrawork is triggered, the agent is **caps-yelled** into absolute-certainty discipline before implementation: "ABSOLUTE CERTAINTY REQUIRED - DO NOT SKIP THIS. YOU MUST NOT START ANY IMPLEMENTATION UNTIL YOU ARE 100% CERTAIN." Gating happens **inside** the model's reasoning via prompt shape, not as a hard reject.
  3. **Prometheus planner** (explicit `@plan` / press-Tab entry) — OMO's true equivalent to `$ralplan`. Interview-mode, Metis gap analysis, Momus reviewer loop (≥100% file refs verified, ≥80% clear ref sources, ≥90% concrete acceptance criteria). But Prometheus is **opt-in**, not an auto-redirect from under-specified prompts.
- **Implication for Δ2**: Axis remains valid. OMO is the **first pure prompt-shape gate** case (different from OMC's lexical heuristic and Ouroboros's numeric threshold). Three different gating strategies now observed.
- **Refined form for Δ2**: "If a gate exists, is it (a) lexical-specificity heuristic + redirect (OMC/OMX), (b) numeric-threshold + mandatory qualitative readiness (Ouroboros, OMC deep-interview), (c) prompt-shape discipline + opt-in formal planner (OMO), (d) XML hard-gate tag (Superpowers), (e) enum phase sentinel (Ralph, GSD), or (f) CAPS yelling (Ralph-Huntley)? The six forms span a spectrum from fully deterministic (b, e) to fully model-mediated (c, f)."

### Δ3. "Stage handoff as RPC protocol" — REFUTED for OMO
- **Finding**: OMO has a `/handoff` slash command (`src/features/builtin-commands/templates/handoff.ts`), but **it is single-session context compaction**, not stage-to-stage RPC. Verbatim from source:
  > "Use /handoff when: The current session context is getting too long and quality is degrading; You want to start fresh while preserving essential context from this session; The context window is approaching capacity. This creates a detailed context summary that can be used to continue work in a new session."
- **The template produces a single `HANDOFF CONTEXT` block** with fields `USER REQUESTS (AS-IS) / GOAL / WORK COMPLETED / CURRENT STATE / PENDING TASKS / KEY FILES / IMPORTANT DECISIONS`. It's copy-pasted by the user into a new session. It is NOT written to `.omo/handoffs/` and NOT consumed by a next-stage agent.
- **Implication for Δ3**: Axis remains valid for OMC (which does have true stage-to-stage `.omc/handoffs/<stage>.md`) and GSD (`{PHASE}-{WAVE}-{TYPE}.md`). OMO does NOT count as a 2nd independent instance. Axis still needs a 2nd case beyond OMC to reach promotion threshold.
- **Related OMO artifact worth noting**: `.sisyphus/notepads/{plan-name}/{learnings,decisions,issues,verification,problems}.md` — **wisdom accumulation across Atlas's subagent calls**. This is structurally similar to handoff (persisted across agent spawns, typed fields) but the direction is orthogonal: it's inter-turn learning within one plan, not inter-stage RPC between pipeline phases. Not the same primitive.

### New candidate: Δ4. "Category-as-skill-orthogonal-selector" (OMO-originated)
- **Proposed by**: OMO deep-dive (2026-04-19)
- **Rationale**: OMO explicitly separates two orthogonal dimensions for subagent delegation: **Category** ("what kind of work is this?" → determines model, temperature, prompt mindset) × **Skill** ("what tools and knowledge are needed?" → injects MCP tools, workflows). Stated verbatim in features doc: "By combining these two concepts, you can generate optimal agents through `task`." Built-ins: 8 categories (`visual-engineering / ultrabrain / deep / artistry / quick / unspecified-low / unspecified-high / writing`) × N skills. A `task(category="visual-engineering", load_skills=["frontend-ui-ux"])` call composes model choice and tool grant independently. This is **different from** the 1-slot stage routing we saw in OMC (`team-plan → team-prd → team-exec → team-verify → team-fix`) where model and role are fused into a single choice.
- **Proposed form**: "Does the harness factor subagent invocation into orthogonal dimensions (model/category × tool/skill × persona/role)? If yes, how many orthogonal dimensions? Is the composition N×M or tied? Does it prevent accidental N×M explosion via defaults?"
- **Status**: 1st strong use (OMO). ECC's category-free skills + agent system is a related but **non-orthogonal** case (skills and agents overlap). Weak 2nd-candidate: Compound Engineering's agent × skill split. Possibly 2+ promotable.
- **Promotion threshold**: 2 independent uses.

### New candidate: Δ5. "Wisdom accumulation notepad system" (OMO-originated)
- **Proposed by**: OMO deep-dive (2026-04-19)
- **Rationale**: OMO's Atlas orchestrator maintains `.sisyphus/notepads/{plan-name}/{learnings.md / decisions.md / issues.md / verification.md / problems.md}` — **5 typed notepads** updated **after every subagent call**, categorized as Conventions / Successes / Failures / Gotchas / Commands. Every subsequent subagent sees the current notepad contents. This is a **lifecycle primitive** that sits between axis A (iteration boundaries) and axis L (instinct learning) but is neither: it's not per-iteration reset (ralph), it's not cross-project skill extraction (CE / ECC /learner). It's **intra-plan cumulative memory during execution** — what the orchestrator "learned" while conducting workers.
- **Proposed form**: "Does the orchestrator maintain structured cumulative memory during execution of a single plan, passed forward to every subsequent sub-delegation? What fields (learnings / decisions / issues / verification / problems)? Is the write policy deterministic (after every sub-call) or model-discretion?"
- **Status**: 1st strong use (OMO). GSD STATE.md is a near-match but more monolithic. OMC's `.omc/handoffs/` is stage-level, not task-level. Quick 2+ promotion possible if GSD is re-examined.
- **Promotion threshold**: 2 independent uses.

---

## 1. Identity & provenance

- **Creator**: **@code-yeongyu** (GitHub id 11153873). Real name **YeonGyu-Kim**. Company: **@sionic-ai**. Location: Seoul. Twitter: `@q_yeon_gyu_kim`. Blog: `code-yeongyu.tistory.com`. Bio: "Hacker." Account created 2015-02-23. 2,889 followers.
- **Evidence (author identity)** — GitHub API `https://api.github.com/users/code-yeongyu`:
  ```json
  { "login": "code-yeongyu", "id": 11153873, "name": "YeonGyu-Kim",
    "company": "@sionic-ai", "blog": "code-yeongyu.tistory.com",
    "location": "Seoul", "twitter_username": "q_yeon_gyu_kim", "bio": "Hacker." }
  ```
- **@justsisyphus** (X/Twitter handle mentioned in README) — "my X account ... [@justsisyphus] now posts updates on my behalf" — suggesting a helper/successor account after the original `@yeon_gyu_kim` account was suspended.
- **NOT the same person as Yeachan Heo (OMC/OMX)**:
  - Yeachan-Heo: id 54757707, name "Bellman", company "@Layoff-Labs", blog "bellman.tistory.com", bio "Dedicated Algorithmic Trader / Leader of Quant.start()". Account created 2019-09-01. 3,916 followers.
  - **Different GitHub id, different name, different company, different blog domain, different self-description.**
- **Repo**: https://github.com/code-yeongyu/oh-my-openagent
  - Created **2025-12-03** (over a month before OMC's creation 2026-01-09).
  - **52,694★, 4,240 forks, 557 open issues**. Size 56.5 MB.
  - License: "SUL-1.0" (custom; the LICENSE.md file shows "license: other" in API).
  - Language: TypeScript. Runtime: Bun only. npm package name: `oh-my-opencode` (dual-published as `oh-my-openagent` during transition — both names currently work).
  - Default branch: **`dev`** (not `main`). `main` returns 404. This is unusual — OMO ships from the dev branch.
- **Current version**: v3.17.4 (2026-04-16). v3.17.2 (2026-04-13) was what the brief cited.
- **Release cadence**: 60+ releases in ~4.5 months (Jan 20 first v3.x → Apr 16 latest). ~10-15 releases per month. Higher cadence than OMC.
- **Community**: **Same Discord** as OMC/OMX — `https://discord.gg/PUwSMR9XNk`, guild id **1452487457085063218** (confirmed identical invite code in OMO README). This suggests deliberate community-sharing between the two ecosystems despite different authors.
- **Related commercial brand**: **Sisyphus Labs** (sisyphuslabs.ai) — "We're building a fully productized version of Sisyphus to define the future of frontier agents." Jobdori (AI assistant) is "built on a heavily customized fork of OpenClaw" (from README self-promotion block). OMO is the open-source foundation for Sisyphus Labs' commercial product.
- **Top contributors**: `code-yeongyu` (3,409 commits), `github-actions[bot]` (517), `sisyphus-dev-ai` (252 — AI agent), `justsisyphus` (239 — likely code-yeongyu's second account), `acamq` (77), `kdcokenny` (69), `MoerAI` (57), `RaviTharuma` (33), `junhoyeo` (22), `devxoul` (19). **`junhoyeo` is a shared contributor** (also appears in OMC maintainer list — the one cross-contributor between ecosystems).
- **Evidence quote (OMO self-identity)**:
  > "omo; the best agent harness - previously oh-my-opencode" — GitHub repo description

## 2. Problem framing (verbatim author voice)

Author's verbatim framing of the problem OMO solves (from README and manifesto):

> "You're juggling Claude Code, Codex, random OSS models. Configuring workflows. Debugging agents. We did the work. Tested everything. Kept what actually shipped. Install OmO. Type `ultrawork`. Done." — README

> "HUMAN IN THE LOOP = BOTTLENECK. Think about autonomous driving. When a human has to take over the wheel, that's not a feature. It's a failure of the system... Oh My OpenAgent is built on this premise: Human intervention during agentic work is fundamentally a wrong signal." — docs/manifesto.md

> "Goal: Code written by the agent should be indistinguishable from code written by a senior engineer. Not 'AI-generated code that needs cleanup.' Not 'a good starting point.' The actual, final, production-ready code." — docs/manifesto.md

> "We don't do lock-in here. We ride every model. Claude / Kimi / GLM for orchestration. GPT for reasoning. Minimax for speed. Gemini for creativity. The future isn't picking one winner — it's orchestrating them all. Models get cheaper every month. Smarter every month. No single provider will dominate." — README

**Central claim: multi-model anti-lock-in + zero-hand-holding.** The adversarial tone toward Anthropic is explicit: "Anthropic [blocked OpenCode because of us.](https://x.com/thdxr/status/2010149530486911014)" and "Hephaestus is called 'The Legitimate Craftsman.' The irony is intentional."

## 3. Architecture / substrate

- **Substrate**: **OpenCode plugin** (single substrate, not multi-substrate). Attaches via `opencode.json` plugin array. Both `oh-my-openagent` and legacy `oh-my-opencode` entry names are accepted during rename transition.
- **Inbound adapters** (compat layer, NOT a substrate port):
  - **Claude Code compatibility**: "Your hooks, commands, skills, MCPs, and plugins? All work here unchanged. Full compatibility, including plugins." Loaders live at `src/features/claude-code-{agent,command,mcp,plugin}-loader/`. OMO **absorbs** Claude Code ecosystem artifacts into OpenCode, it does not **emit** itself to Claude Code.
- **Code surface (from AGENTS.md, authoritative)**:
  - **1,766 TypeScript source files, 377k LOC, 104 barrel index.ts files**.
  - **11 agents** (Sisyphus, Hephaestus, Oracle, Librarian, Explore, Atlas, Prometheus, Metis, Momus, Multimodal-Looker, Sisyphus-Junior)
  - **52 lifecycle hooks** (across `src/hooks/`)
  - **26 tools** (across `src/tools/`)
  - **3-tier MCP system** (built-in + .mcp.json + skill-embedded)
  - **19 feature modules** (including `background-agent`, `boulder-state`, `team-mode`, `tmux-subagent`, `skill-mcp-manager`, `openclaw`, `run-continuation-state`, `preemptive-compaction`)
  - **11 platform-specific compiled binaries** (darwin/linux/windows, AVX2 + baseline variants)
- **Init flow** (`src/index.ts` default export `pluginModule`):
  ```
  pluginModule.server(input, options)
    ├─→ loadPluginConfig()       # JSONC parse → project/user merge → Zod v4 validate → migrate
    ├─→ createManagers()          # TmuxSessionManager, BackgroundManager, SkillMcpManager, ConfigHandler
    ├─→ createTools()             # SkillContext + AvailableCategories + ToolRegistry (26 tools)
    ├─→ createHooks()             # 3-tier: Core(43) + Continuation(7) + Skill(2) = 52 hooks
    └─→ createPluginInterface()   # 10 OpenCode hook handlers → PluginInterface
  ```
- **OpenCode's 10 hook handlers used**: `config, tool, chat.message, chat.params, chat.headers, event, tool.execute.before, tool.execute.after, experimental.chat.messages.transform, experimental.session.compacting`.
- **Multi-level config**: Project (`.opencode/oh-my-opencode.jsonc`) → User (`~/.config/opencode/oh-my-opencode.jsonc`) → Defaults. Deep-merge for `agents/categories/claude_code`; set-union for `disabled_*` arrays; override for everything else. Migration is idempotent via `_migrations` tracking.
- **Runtime contract**: Bun only (1.3.11 in CI). `bun-types`, never `@types/node`. No path aliases. 200 LOC soft limit per file. No catch-all files (`utils.ts`/`helpers.ts` banned). 104 barrel exports establish module boundaries.

## 4. Core loop / keywords / agents / skills

### 4a. Top-level entry points
Three modes with intentional escalation of user effort vs determinism:

| Mode | Entry | When to use | Mechanism |
|---|---|---|---|
| **Simple** | Just prompt normally | Quick fixes, single-file changes | Default OpenCode behavior |
| **Ultrawork** | Type `ultrawork` or `ulw` | Complex tasks, explaining context is tedious | IntentGate detects keyword → `chat.message` hook injects ultrawork-mode system prompt → Sisyphus caps-yelled into discipline + told to delegate via categories + skills |
| **Prometheus (Precise)** | Press **Tab** (OpenCode's agent-tab cycling) OR `@plan "<task>"` | Multi-day projects, critical changes | Prometheus interviews user, Metis gap-analyzes, Momus reviews; writes `.sisyphus/plans/*.md` |
| **Atlas (Execute)** | `/start-work [plan-name] [--worktree <path>]` | Resume or execute a Prometheus plan | Reads `.sisyphus/boulder.json`, decomposes plan tasks into granular todos, delegates to Sisyphus-Junior by category |

### 4b. Canonical agent roster (11 agents, Greek mythology)
Stable tab-order enforced via `order` field (verbatim from features.md):

| Order | Agent | Default model | Role |
|---|---|---|---|
| 1 | **Sisyphus** | claude-opus-4-7 | Default orchestrator (main). 32k extended-thinking budget. "He rolls the boulder every day. Never stops." |
| 2 | **Hephaestus** | gpt-5.4 | "The Legitimate Craftsman." Autonomous deep worker, AmpCode-inspired |
| 3 | **Prometheus** | claude-opus-4-7 | Strategic planner, interview mode, READ-ONLY |
| 4 | **Atlas** | claude-sonnet-4-6 | Conductor. Executes Prometheus plans. Cannot delegate except via `task`/`call_omo_agent` |
| — | Metis | claude-opus-4-7 | Gap analyzer (pre-planning) |
| — | Momus | gpt-5.4 | Plan reviewer (post-planning) |
| — | Oracle | gpt-5.4 | Architecture/debugging consultant, READ-ONLY |
| — | Librarian | minimax-m2.7 | Docs/OSS code search, READ-ONLY |
| — | Explore | grok-code-fast-1 | Fast codebase grep, READ-ONLY |
| — | Multimodal-Looker | gpt-5.4 | Vision (PDFs/images/diagrams), `read`-only allowlist |
| — | Sisyphus-Junior | category-dependent | Task executor spawned via category. **Cannot re-delegate** (blocked: task, call_omo_agent) |

Tool restrictions (from features.md verbatim):
> "oracle: Read-only: cannot write, edit, or delegate (blocked: write, edit, task, call_omo_agent); librarian: Cannot write, edit, or delegate; explore: Cannot write, edit, or delegate; multimodal-looker: Allowlist: `read` only; atlas: Cannot delegate (blocked: task, call_omo_agent); momus: Cannot write, edit, or delegate"

### 4c. Categories (the orthogonal model-selection axis) — primitive Δ4
8 built-in categories mapped to default models, independent of which specific skill is loaded:

| Category | Default model | Use case |
|---|---|---|
| `visual-engineering` | google/gemini-3.1-pro | Frontend, UI/UX, design |
| `ultrabrain` | openai/gpt-5.4 (xhigh) | Deep logical reasoning, complex architecture |
| `deep` | openai/gpt-5.4 (medium) | Goal-oriented autonomous problem-solving |
| `artistry` | google/gemini-3.1-pro (high) | Creative/artistic tasks |
| `quick` | openai/gpt-5.4-mini | Trivial tasks — single-file changes, typo fixes |
| `unspecified-low` | anthropic/claude-sonnet-4-6 | Default low-effort fallback |
| `unspecified-high` | anthropic/claude-opus-4-7 (max) | Default high-effort fallback |
| `writing` | google/gemini-3-flash | Documentation, prose |

Invocation: `task(subagent_type="...", category="deep", load_skills=[], run_in_background=true, prompt="...")`. Category determines model; load_skills determines tool/knowledge injection; subagent_type determines persona/tool-restriction policy. **Three orthogonal dimensions** — this is primitive Δ4 (new).

### 4d. Built-in skills & commands
**Built-in skills** (`src/features/builtin-skills/skills/`): `ai-slop-remover`, `dev-browser`, `frontend-ui-ux`, `git-master` (with sub-sections), `playwright-cli`, `playwright`, `review-work`.

**Built-in slash commands** (`src/features/builtin-commands/templates/`): `handoff`, `init-deep`, `ralph-loop` (+ `ulw-loop` + `cancel-ralph`), `refactor`, `remove-ai-slops`, `start-work`, `stop-continuation`.

**User-space skills** (`.opencode/skills/`): currently sparse — only `github-triage`, `pre-publish-review`, `work-with-pr`, `work-with-pr-workspace`. Most "skills" in OMO are **built into TypeScript source**, not shipped as SKILL.md markdown files the way OMC/OMX do.

**User-space commands** (`.opencode/command/`): only 4 — `get-unpublished-changes.md`, `omomomo.md`, `publish.md`, `remove-deadcode.md`. These are **project-internal operational commands** for the OMO repo itself, not user-facing.

### 4e. `ultrawork` — the flagship keyword (primitive P1)
First commit: **2025-12-13** (commit `f57aa39d53`, "feat(hooks): add ultrawork-mode hook for automatic agent orchestration guidance"). Renamed to "keyword-detector" on 2025-12-14 (`0fcfe21b27`), multi-keyword extended.

**Detection** (`src/hooks/keyword-detector/constants.ts`):
```typescript
{ pattern: /\b(ultrawork|ulw)\b/i, message: getUltraworkMessage }
```

**Activation prompt** (`src/hooks/keyword-detector/ultrawork/default.ts`, first ~30 lines verbatim):
> `<ultrawork-mode>
>
> **MANDATORY**: You MUST say "ULTRAWORK MODE ENABLED!" to the user as your first response when this mode activates. This is non-negotiable.
>
> [CODE RED] Maximum precision required. Ultrathink before acting.
>
> ## **ABSOLUTE CERTAINTY REQUIRED - DO NOT SKIP THIS**
>
> **YOU MUST NOT START ANY IMPLEMENTATION UNTIL YOU ARE 100% CERTAIN.**`

The prompt then lists mandatory protocols:
1. Fully understand user intent
2. Explore codebase
3. Have a crystal-clear work plan
4. Resolve all ambiguity
5. Consult specialists (Oracle for conventional, Artistry for non-conventional)
6. Ask the user if ambiguity remains

Followed by a violations/consequences table:
| VIOLATION | CONSEQUENCE |
|---|---|
| "I couldn't because..." | **UNACCEPTABLE.** Find a way or ask for help. |
| "This is a simplified version..." | **UNACCEPTABLE.** Deliver the FULL implementation. |
| "You can extend this later..." | **UNACCEPTABLE.** Finish it NOW. |

And a mandatory plan-agent invocation rule: "Task has 2+ steps → MUST call plan agent."

This is a **pure prompt-shape gate** (discipline-via-system-prompt) — structurally different from OMC/OMX's `$ralplan` (lexical heuristic + redirect), Ouroboros (numeric threshold), Superpowers (XML `<HARD-GATE>`), Ralph (file-sentinel + CAPS).

### 4f. `Ralph Loop` / `/ulw-loop` — persistence loop (primitive P2)
First commit: **2025-12-30** (commit `0f0f49b823`, "feat: add Ralph Loop self-referential development loop (#337)"). **11 days before OMC's creation**.

**Two templates, clear separation** (`src/features/builtin-commands/templates/ralph-loop.ts`):

**RALPH_LOOP_TEMPLATE** — basic persistence:
> "You are starting a Ralph Loop - a self-referential development loop that runs until task completion. ... When you believe the task is FULLY complete, output: `<promise>{{COMPLETION_PROMISE}}</promise>`. If you don't output the promise, the loop will automatically inject another prompt to continue. Maximum iterations: Configurable (default 100)."

**ULW_LOOP_TEMPLATE** — ultrawork + Oracle verification:
> "You are starting an ULTRAWORK Loop - a self-referential development loop that runs until verified completion. ... That does NOT finish the loop yet. The system will require Oracle verification. The loop only ends after the system confirms Oracle verified the result. The iteration limit is **500 for ultrawork mode, 100 for normal mode**."

**Cancellation**: `/cancel-ralph` command. Exit conditions: Verified Completion (Oracle) or Cancel.

**Runtime** (`src/hooks/ralph-loop/`): hooks watch OpenCode's `Stop` event; detect `<promise>DONE</promise>` marker in transcript; inject continuation prompt; manage state across iterations. Key files:
- `completion-promise-detector.ts` — parses promise tag
- `oracle-verification-detector.ts` — verifies Oracle signed off for ULW mode
- `iteration-continuation.ts` — injects next-iteration prompt
- `loop-session-recovery.ts` — rebuild state if session crashes
- `loop-state-controller.ts` — state machine controller

**Vs Huntley's Ralph**: Like OMC/OMX, OMO's Ralph Loop is **not** `while true; do cat PROMPT.md | agent ; done`. It's a native hook-driven state machine inside one OpenCode session. Completion signaling via XML-tag embed (`<promise>DONE</promise>`), not file sentinel. Verification optional (normal Ralph) vs mandatory Oracle (ultrawork).

### 4g. `boulder-state` — active plan tracking (primitive P3)
First commit: **2026-03-18** (via `src/features/boulder-state`; ralph-parity commits predate). State file: `.sisyphus/boulder.json`.

**Schema** (`src/features/boulder-state/types.ts` verbatim):
```typescript
export interface BoulderState {
  /** Absolute path to the active plan file */
  active_plan: string
  /** ISO timestamp when work started */
  started_at: string
  /** Session IDs that have worked on this plan */
  session_ids: string[]
  session_origins?: Record<string, "direct" | "appended">
  /** Plan name derived from filename */
  plan_name: string
  /** Agent type to use when resuming (e.g., 'atlas') */
  agent?: string
  /** Absolute path to the git worktree root where work happens */
  worktree_path?: string
  /** Preferred reusable subagent sessions keyed by current top-level plan task */
  task_sessions?: Record<string, TaskSessionState>
}

export interface TaskSessionState {
  task_key: string      // Stable identifier for current top-level plan task (e.g. todo:1 / final-wave:F1)
  task_label: string
  task_title: string
  session_id: string    // Preferred reusable subagent session
  agent?: string
  category?: string
  updated_at: string
}
```

**Contrast with OMC's `.omc/handoffs/`**: OMC's handoffs are **between stages** (team-plan→team-prd→team-exec→…). OMO's boulder-state is **within one plan's lifespan across multiple sessions** (session_ids accumulate; sessions can be `direct` or `appended` origin). The design goal is **plan resumability** (you can close OMO, reopen later, `/start-work` continues where you left off). Not stage-to-stage RPC.

Named after Sisyphus's boulder: "Boulder State Storage: Handles reading/writing boulder.json for active plan tracking. Named after Sisyphus's boulder - the eternal task that must be rolled." — src comment.

### 4h. `team-mode` — NEW (2026-04-17/18, not yet in a released version as of dossier writing)
From `src/features/team-mode/types.ts` (verbatim):

```typescript
export const MESSAGE_KINDS = ["message", "shutdown_request",
  "shutdown_approved", "shutdown_rejected", "announcement"] as const

export const TASK_STATUSES = ["pending", "claimed", "in_progress",
  "completed", "deleted"] as const

export const RUNTIME_STATUSES = ["creating", "active", "shutdown_requested",
  "deleting", "deleted", "failed", "orphaned"] as const

// Members can be category-typed OR subagent_type-typed (discriminatedUnion)
// MAX 8 members per team
// Backend: "in-process" (default) or "tmux"
```

**Rich type-safe schema via Zod v4**. Messages have `messageId` (UUID), `from/to`, `body` (max 32KB), `correlationId` for request/reply. Tasks have `blocks/blockedBy` for dependency graphs.

**Implementation was added 1-2 days before this dossier**:
- `b00e22c2b8` 2026-04-17 `feat(team-mode): add core types (discriminatedUnion for members, D-41/D-42)`
- `f1268c0448` 2026-04-17 `feat(team-mode): add worktree manager (optional per-member isolation)`
- `e303feefd2` 2026-04-18 `feat(team-mode): add team-layout-tmux for focus+grid pane visualization`
- `f8a1a11bb7` 2026-04-18 `fix(team-mode): refactor layout to use testable spawn-process helper`

**Vs OMC's native `TeamCreate`/OMX's Rust runtime**: OMO's team-mode is **yet another reinvention** — this is now the **fourth** team-coordination implementation among {OMC riding Claude Code native, OMX Rust+tmux, OMO in-process/tmux, Claude Code native itself}. Strong evidence that no convergent cross-harness team contract exists yet.

### 4i. `background-agent` — parallel subagent execution
`src/features/background-agent/` — 20+ files. Orchestration via:
- `task(subagent_type="explore", load_skills=[], prompt="...", run_in_background=true)` — fire
- `background_output(task_id="bg_abc123")` — retrieve when ready
- System notifies on completion (via `task-toast-manager`)

Has: `concurrency.ts`, `default-message-staleness-timeout.ts`, `error-classifier.ts`, `fallback-retry-handler.ts`, `loop-detector.ts`.

**Background concurrency**: "5 concurrent per model/provider (configurable, circuit breaker support)" — AGENTS.md.

**Visual Multi-Agent with Tmux**: when `tmux.enabled: true`, background agents spawn in separate tmux panes ("Stable agent ordering: core-agent tab cycling is deterministic via injected runtime order field — Sisyphus: 1, Hephaestus: 2, Prometheus: 3, Atlas: 4" — features.md).

### 4j. `IntentGate` — multi-lingual regex classifier (primitive P4)
`src/hooks/keyword-detector/detector.ts` + `constants.ts`. Three detected intent types: `ultrawork / search / analyze`.

**Analyze-mode detection regex** (excerpt, covers English + Korean + Japanese + Chinese + Vietnamese):
```
/\b(analyze|analyse|investigate|examine|research|study|deep[\s-]?dive|inspect|audit|
  evaluate|assess|review|diagnose|scrutinize|dissect|debug|comprehend|interpret|
  breakdown|understand)\b|why\s+is|how\s+does|how\s+to|
  분석|조사|파악|연구|검토|진단|이해|설명|원인|이유|뜯어봐|따져봐|평가|해석|디버깅|어떻게|왜|살펴|
  分析|調査|解析|検討|研究|診断|理解|説明|検証|精査|究明|デバッグ|なぜ|どう|仕組み|
  调查|检查|剖析|深入|诊断|解释|调试|为什么|原理|搞清楚|弄明白|
  phân tích|điều tra|nghiên cứu|kiểm tra|xem xét|chẩn đoán|giải thích|tìm hiểu|gỡ lỗi|tại sao/i
```

Triggers inject prepended system-prompt fragment (pre-computed messages for each type). Crucially: this is **NOT** a gate that blocks execution — it's **mode-switching pre-context-injection**. No redirection, no rejection. Compare: OMC/OMX's `$ralplan` *rejects and redirects*.

**Code-block stripping** prevents false positives inside fenced/backticked code:
```typescript
const CODE_BLOCK_PATTERN = /```[\s\S]*?```/g
const INLINE_CODE_PATTERN = /`[^`]+`/g
function removeCodeBlocks(text) { return text.replace(CODE_BLOCK_PATTERN, "").replace(INLINE_CODE_PATTERN, "") }
```

### 4k. `Hashline` — LINE#ID content-hash edit tool (primitive P5)
`src/tools/hashline-edit/` — 26 files. Inspired by **oh-my-pi** (blog.can.ac): "Every line the agent reads comes back tagged with a content hash."

**Read output format**:
```
11#VK| function hello() {
22#XJ|   return "world";
33#MB| }
```

**Edit semantics**: agent references `LINE#ID` in its edit call; if file changed since last read, the hash won't match, **edit is rejected before corruption**. No whitespace reproduction, no stale-line errors.

**Empirical claim** (README verbatim): "Grok Code Fast 1: **6.7% → 68.3%** success rate. Just from changing the edit tool."

**Source files**: `hash-computation.ts`, `hashline-edit-executor.ts`, `hashline-chunk-formatter.ts`, `edit-deduplication.ts`, `edit-operation-primitives.ts`, `edit-ordering.ts`, `edit-text-normalization.ts`, `autocorrect-replacement-lines.ts`, `formatter-trigger.ts`.

**Why this matters**: Hashline addresses the *content-addressability* half of the "harness problem." Related hooks exist at `src/hooks/hashline-edit-diff-enhancer/`, `src/hooks/hashline-read-enhancer/`, `src/hooks/edit-error-recovery/`.

### 4l. `Prometheus planner` — opt-in consensus planning
Prometheus is **READ-ONLY** — can only create/modify markdown files within `.sisyphus/` directory. Interview process:
- Launches explore/librarian agents to gather codebase context
- Iterative clarification until 5-check clearance: "Core objective defined? Scope boundaries established? No critical ambiguities? Technical approach decided? Test strategy confirmed?"
- Calls **Metis** (gap analyzer) — "The plan author (Prometheus) has 'ADHD working memory' - it makes connections that never make it onto the page. Metis forces externalization of implicit knowledge."
- Optionally calls **Momus** (ruthless reviewer) — 4 criteria: Clarity / Verification / Context / Big Picture. OKAY only when: 100% file refs verified, ≥80% clear ref sources, ≥90% concrete acceptance criteria, zero business-logic assumptions, zero red flags. REJECT → Prometheus fixes → resubmit. **No maximum retry limit**.

**Output**: `.sisyphus/plans/{plan-name}.md` — checkbox-format plan consumed by Atlas via `/start-work`.

**Comparative position**: Prometheus is OMO's analogue to OMC `$ralplan`, but:
- Prometheus is **opt-in** (press Tab / `@plan`), not an auto-redirect from under-specified prompts
- Uses 3 agents (Prometheus/Metis/Momus) vs OMC's 3 agents (Planner/Architect/Critic) — same triangle pattern, different names
- Plan file lives in `.sisyphus/plans/` vs OMC's `.omc/plans/ralplan-*.md` — same idea, different path
- No numeric ambiguity threshold (OMO) vs OMX deep-interview's weighted score

### 4m. `Atlas` — execution orchestrator (primitive P6 — conductor pattern)
Atlas reads Prometheus plan, decomposes into granular todos, delegates to Sisyphus-Junior by category, accumulates wisdom, verifies completion.

**The Conductor Mindset** (verbatim from orchestration.md):
> "Atlas is like an orchestra conductor: it doesn't play instruments, it ensures perfect harmony."

**What Atlas CAN do**: Read files, run commands, lsp_diagnostics, grep/glob/ast-grep search.

**What Atlas MUST delegate**: Writing code, fixing bugs, creating tests, git commits.

**Wisdom accumulation** (`src/shared/notepad/` + features.md):
```
.sisyphus/notepads/{plan-name}/
├── learnings.md      # Patterns, conventions, successful approaches
├── decisions.md      # Architectural choices and rationales
├── issues.md         # Problems, blockers, gotchas encountered
├── verification.md   # Test results, validation outcomes
└── problems.md       # Unresolved issues, technical debt
```

After each subagent call, Atlas extracts learnings, categorizes into {Conventions, Successes, Failures, Gotchas, Commands}, and passes them forward to ALL subsequent subagents. This is candidate Δ5 (new).

## 5. State & context model

- **Per-project state**: `.sisyphus/` directory — owned by OMO, mimics Claude Code's `.claude/` or OMC's `.omc/`:
  - `.sisyphus/boulder.json` — active plan state (see §4g)
  - `.sisyphus/plans/{name}.md` — Prometheus-authored plans
  - `.sisyphus/notepads/{plan-name}/{learnings,decisions,issues,verification,problems}.md` — Atlas wisdom
  - `.sisyphus/rules/modular-code-enforcement.md` — architecture rules enforced by agents
- **Logger**: writes to `/tmp/oh-my-opencode.log` (single global log).
- **Hierarchical `AGENTS.md`** (Deep Initialization via `/init-deep`): generates `AGENTS.md` files throughout the project tree for context-injection. Directory scoring heuristic: files-per-dir, total-lines, max-depth, large-files count, monorepo-detection, multi-language. Background explore-agents fire in parallel to discover patterns. **Hierarchical context**: root-level file + per-subtree files. OMO agents auto-read relevant context.
- **Context injection hook** (`src/features/context-injector/`): injects AGENTS.md, README.md, and conditional rules into agent prompts based on CWD.
- **Session lifecycle**: OpenCode manages session IDs; OMO extends with multi-session-per-plan tracking in boulder.json's `session_ids[]`.
- **Preemptive compaction** (`src/hooks/preemptive-compaction*.ts` — 10 files): monitors context utilization, detects degradation, triggers compaction before hitting hard limit. Tracks model-specific context limits (AWS Bedrock variants handled separately). This is more sophisticated than OMC/OMX's compaction handling.
- **Session recovery** (`src/hooks/anthropic-context-window-limit-recovery/`, `src/hooks/runtime-fallback/`, `src/hooks/model-fallback/`, `src/hooks/json-error-recovery/`, `src/hooks/edit-error-recovery/`, `src/hooks/empty-task-response-detector.ts`): extensive layered recovery. **Two fallback systems**: `model-fallback` (proactive, chat.params) vs `runtime-fallback` (reactive, session.error) — noted as architecturally distinct in AGENTS.md.

## 6. Tool surface & permissions

### Tools (26 in `src/tools/`)
Key ones:
- `task` / `delegate-task` / `call-omo-agent` — sub-agent delegation (with category + skills + persona selector)
- `hashline-edit` — content-hash-validated edit tool (§4k)
- `grep` / `glob` / `ast-grep` — search (Windows drive-letter support added 2026-04-15)
- `lsp` — full LSP: `lsp_rename` / `lsp_goto_definition` / `lsp_find_references` / `lsp_diagnostics`
- `interactive-bash` — persistent bash sessions (REPLs, debuggers, TUIs)
- `look-at` — image/screenshot reading
- `session-manager` — list/read/search session history
- `skill` / `skill-mcp` — skill loader + skill-embedded MCP manager
- `slashcommand` — slash command dispatch
- `background-task` — fire-and-forget + completion polling

### Per-agent tool restrictions (explicit allowlist/blocklist)
Documented in §4b. Oracle/Librarian/Explore/Multimodal-Looker are **READ-ONLY**; Momus is READ-ONLY; Atlas cannot delegate; Sisyphus-Junior cannot re-delegate.

### MCP servers (3-tier)
1. **Built-in** (`src/mcp/` — 3 remote HTTP): `websearch` (Exa/Tavily), `context7` (docs), `grep_app` (GitHub search)
2. **Claude Code** (`.mcp.json`): `${VAR}` env expansion via `claude-code-mcp-loader`
3. **Skill-embedded** (SKILL.md YAML): managed by `SkillMcpManager`; stdio + HTTP per-session

### Tool-guard & permission hooks (14)
- `bash-file-read-guard.ts` — guard against dangerous reads
- `prometheus-md-only/` — enforce Prometheus read-only policy
- `no-sisyphus-gpt`, `no-hephaestus-non-gpt` — model-agent pairing rules
- `category-skill-reminder` — warn when category/skill misaligned
- `directory-agents-injector`, `directory-readme-injector` — hierarchical AGENTS.md injection
- `rules-injector` — inject `.sisyphus/rules/*.md`
- `agent-usage-reminder` — nudge when agent is being under-utilized
- `anthropic-effort` — clamp variant=max for github-copilot Claude models
- `comment-checker` — anti-AI-slop comment scanner (blocks AI-pattern comments before commit)
- `legacy-plugin-toast` — warn during rename transition

### CLI surface (Bun-based)
- `bunx oh-my-opencode install` — interactive setup
- `bunx oh-my-opencode doctor` — health diagnostics (checks plugin registration, config, models, environment)
- `bunx oh-my-opencode run` — non-interactive session
- `bunx oh-my-opencode mcp-oauth` — MCP OAuth flow

## 7. Human-in-the-loop

Explicit manifesto position: **human in the loop = bottleneck = failure signal**. Docs/manifesto.md quoted verbatim in §2.

Concrete HITL points present despite the ideology:
- **Prometheus interview** — mandatory questions until 5-check clearance
- **Momus review** — user can opt into high-accuracy review loop
- **User gateway** — `ask-user-question` (for genuine ambiguity); `background-task-notification-template` (completion toasts)
- **`/handoff` command** — user-initiated session-boundary compaction (§3 Δ3)
- **OpenClaw external reply channel** (§8) — bidirectional Discord/Telegram/webhook notifications and replies (async HITL over external channel)

The tension between manifesto ("never ask") and practice (Momus/Prometheus/`ask-user-question`) is resolved by restricting HITL to **planning-time only** — once execution starts in ultrawork or Atlas, the system prefers agent-to-agent consult (Oracle, Artistry) over user question.

## 8. Composability / ecosystem integration

### OpenClaw external-notification gateway
`src/openclaw/` — 20+ files. Originally named "OMX_OPENCLAW" (hence the initial env vars), renamed to "OMO_OPENCLAW" on 2026-03-16. Handles bidirectional Discord/Telegram/webhook/command integration. Key files: `dispatcher.ts`, `daemon.ts`, `reply-listener-discord.ts`, `reply-listener-telegram.ts`, `session-registry.ts`, `tmux.ts`, `gateway-url-validation.ts`.

**Event matrix** (same as OMC's): `session-start / stop / keyword-detector / ask-user-question / pre-tool-use / post-tool-use` events fire to external gateway URL.

**Provenance of OpenClaw across harnesses** (from git history):
- **OMC** (Yeachan-Heo): first commit `e745e20814` on **2026-02-25** — `feat(openclaw): add OpenClaw webhook gateway integration (#1023)`. **Origin.**
- **OMX** (Yeachan-Heo): first commit `e30649560a` on **2026-02-26** — `feat(notifications): integrate OMC 4.5.x notification engine enhancements (#373)`. **Ported 1 day later.**
- **OMO** (code-yeongyu): first commit `03b346ba51` on **2026-03-16** — `feat: implement OpenClaw integration`. Same-day followup `2c8813e95d` — `fix: rename OMX_OPENCLAW env vars to OMO_OPENCLAW`. **Ported ~3 weeks later.**

**Conclusion**: OpenClaw is an **OMC-originated primitive** that OMO adopted. The `OMX → OMO` env var rename is a telltale sign that code-yeongyu imported code/config structure from OMX, not from OMC directly. OpenClaw's commercial arm (`openclaw.ai`, plus Jobdori AI assistant "built on a heavily customized fork of OpenClaw") is referenced by OMO's README but is not an OMO product — it's cross-ecosystem infrastructure.

### Claude Code compatibility layer (inbound adapter)
`src/features/claude-code-agent-loader/`, `claude-code-command-loader/`, `claude-code-mcp-loader/`, `claude-code-plugin-loader/`, `claude-code-session-state/`. OMO **absorbs** Claude Code ecosystem into OpenCode. Claude Code `skills/*/SKILL.md`, `agents/*.md`, `commands/*.md`, plugin directories, `.mcp.json` all load. This is the analogue of OMC/OMX's `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` substrate-riding, but in reverse direction (OMC rides *Claude Code's* features; OMO *accepts Claude Code's* artifacts).

### Distribution
- **npm package**: `oh-my-opencode` (primary) + `oh-my-openagent` (alias, published in parallel during transition). Downloaded via `bunx`.
- **Platform binaries** (11): darwin/linux/windows × AVX2/baseline variants. Built via `bun compile` on `macOS` runners for darwin (not cross-compiled, to avoid Bun segfaults).
- **Website**: https://ohmyopenagent.com/ (API endpoint `/api/npm-downloads` for shields.io badge)
- **Sisyphus Labs commercial brand**: sisyphuslabs.ai

### Ecosystem cross-links (mutual with OMC/OMX)
- **Same Discord** (guild 1452487457085063218 / invite `PUwSMR9XNk`) shared between OMO and OMC/OMX communities.
- **`junhoyeo`** is a shared top-10 contributor to both ecosystems.
- **OpenClaw** spans both: originated in OMC, adopted in OMO.
- **Naming and skill-vocabulary cross-pollination**: OMO invented `ultrawork`/`ralph-loop`/`Sisyphus`-agent-name/`Prometheus`-planner-name/`IntentGate`/`Hashline`; OMC ported these 2026-01-09 onwards and added new skills (`deep-interview`, `ralplan`, `learner`). **The two harnesses maintain intentional parity in shared vocabulary while each innovates independently on new primitives.**

## 9. Empirical claims & evidence

### Author-stated claims
- "**Grok Code Fast 1: 6.7% → 68.3% success rate** (from changing the edit tool [to Hashline])." — README
- "**99% of this project was built with OpenCode. I don't really know TypeScript.**" — README "Author's Note"
- "**I burned through $24K in LLM tokens** on personal projects." — README "Author's Note"
- "**Anthropic blocked OpenCode because of us.** Yes this is true." — README, linked to https://x.com/thdxr/status/2010149530486911014
- "**Two ChatGPT Pro accounts** worth of tokens" burned to validate GPTPhus. — v3.11.0 release notes
- "It made me cancel my Cursor subscription. Unbelievable things are happening in the open source community." — Arthur Guiot, tweet
- "Knocked out 8000 eslint warnings with Oh My Opencode, just in a day" — Jacob Ferrari tweet

### Internal measurement culture
- No public SWE-bench/Terminal-Bench-style benchmark results surfaced in README.
- **Doctor command** (`bunx oh-my-opencode doctor`) runs health checks — see `src/cli/doctor/checks/`.
- **IntentGate mentions Terminal-Bench** by link (https://factory.ai/news/terminal-bench) — acknowledging external benchmark without claiming a result on it.
- **Extensive test suite**: co-located `*.test.ts`; CI test-split via `script/run-ci-tests.ts` auto-detects `mock.module()` usage and isolates heavy mocks. 100+ test files observed in the hooks/ tree alone.

### Adoption signal
- 52,694★ (largest of OMO/OMC/OMX; ~77% larger than OMC).
- 4,240 forks, 557 open issues.
- 60+ releases in ~4 months.
- ~3,400 commits from code-yeongyu; 30+ external contributors each with ≥5 commits.
- "Loved by professionals at: Indent, Google, Microsoft, ELESTYLE" — README self-claim (unverified but specific).
- Growing commercial backing: Sisyphus Labs waitlist.

## 10. Failure modes & limits

### Author-acknowledged
- **Windows considerations**: explicit handling for "drive-letter paths and CRLF in parseOutput" (recent fix PR #3321), "cross-platform path validation for Windows support" (PR #649), "Windows rename-over-existing in write-file-atomically" (#3222). Means Windows is supported but has been a continuous source of bugs.
- **Bun runtime dependency**: "Never use npm/yarn" — hard dependency on Bun. No Node.js fallback.
- **Codex CLI limitations**: author's note literally frames Codex as limited — "Pure Codex is single-model. OmO routes different tasks to different models automatically." (Marketing framing, but also an admission of Codex's constraints that OMX author Yeachan Heo has to work around.)
- **Telemetry on by default**: "Anonymous telemetry is enabled by default... PostHog with a hashed installation identifier... can be disabled with `OMO_SEND_ANONYMOUS_TELEMETRY=0` or `OMO_DISABLE_POSTHOG=1`." v3.17.3 had to disable exception autocapture because free-tier limit was exceeded (188K in 5 days vs 100K limit).
- **Dual-package rename transition**: "Both `oh-my-openagent.json[c]` and legacy `oh-my-opencode.json[c]` basenames are recognized" — soft-deprecation rather than clean break. Legacy warnings during transition.
- **Team-mode just landed** (2026-04-17/18): unreleased as of v3.17.4 which was 2026-04-16. Significant surface area added very recently.

### Observed (from commit/issue velocity)
- Recent 0.13.x-style hot bug-fix cadence: v3.17.2 (`Apr 13`) → v3.17.3 (`Apr 15`) → v3.17.4 (`Apr 16`) with multiple "fix:" commits per release. Similar to OMX's state-handling instability.
- `delegate-task` retry & `background-agent` error classification code is sprawling (`error-classifier.ts`, `fallback-retry-handler.ts`, `loop-detector.ts`, `sync-executor-leak.test.ts`). Strong signal that subagent delegation is the highest-failure-rate area of the system.
- `anthropic-context-window-limit-recovery/` hook specifically — dedicated hook for Anthropic-quota recovery. Indicates the Claude-path fallback is a high-volume failure mode.

### Derived concerns (observer)
- **Complexity**: 1,766 TS files / 377k LOC / 104 barrel exports / 52 hooks / 11 agents / 26 tools. **Much larger than OMC (42 MB, ~40 skills, 19 agents) and OMX (9.4 MB)**. Onboarding surface is very large.
- **Single-author bottleneck**: code-yeongyu owns 3,409 of ~3,800+ commits (~90%). Sisyphus Labs has `sisyphus-dev-ai` and `justsisyphus` acting as secondary identities, but the concentration is extreme. Bus-factor risk.
- **Dev-branch-is-default**: unusual. May indicate perpetual release-candidate posture.

## 11. Comparative position (vs existing corpus)

### vs OMC (oh-my-claudecode, Yeachan-Heo, 2026-01-09)
- **Origin relationship**: OMC's first 4 commits on day 0 are verbatim titled "**Complete port of oh-my-opencode to Claude Code**" / "Enhance persistence mechanisms with oh-my-opencode patterns" / "**Sync all prompts and patterns with oh-my-opencode**" / "Add hooks and skills system matching oh-my-opencode". OMC's origin is an **explicit declared port** of OMO.
- **Author**: DIFFERENT PEOPLE. `code-yeongyu` (YeonGyu-Kim, Sionic-AI) vs `Yeachan-Heo` (Bellman, Layoff-Labs). Different GitHub id / company / blog domain / bio. Same city (Seoul), same Korean-Romanization coincidence, but no evidence they're the same person.
- **Provenance of shared vocab**:
  - **OMO-originated**: `ultrawork`/`ulw` (2025-12-13), `Ralph Loop`/`/ulw-loop` (2025-12-30), `Sisyphus` agent name, `Hephaestus`, `Prometheus` (2026-01-09 in OMO, first commit), `Atlas`, `Oracle`, `Metis`, `Momus`, `IntentGate`, `Hashline`, `boulder-state`, `/init-deep`, `notepad` system.
  - **OMC-originated (imported to OMO later or not at all)**: `ralplan` (OMC 2026-01-22 — NOT in OMO), `deep-interview` (OMC 2026-03-02, "Ouroboros-inspired Socratic questioning" — NOT in OMO), `team`-as-staged-pipeline with `.omc/handoffs/` (OMC feature — OMO's team-mode is a different reimplementation without stage-level handoffs), `OpenClaw` (OMC 2026-02-25, ported to OMO 2026-03-16), `/learner` skill (OMC — OMO doesn't have an equivalent auto-skill-extraction layer).
  - **OMX-originated (of interest)**: Rust runtime `omx-runtime-core` (OMX-exclusive; OMO doesn't have a Rust runtime).
- **Substrate**: OMO is pure-OpenCode (with inbound CC adapter), OMC is pure-Claude-Code. Not a multi-substrate family with a shared core — they're two separate products with overlapping vocabulary.
- **Code structure**: OMO is TypeScript source-heavy (`src/features/`, `src/hooks/`, `src/tools/` — business logic lives in code), OMC is SKILL.md-heavy (`skills/*/SKILL.md` — business logic lives in markdown prompts). Fundamentally different engineering stance: OMO trusts code > prompts; OMC trusts prompts > code.

### vs OMX (oh-my-codex, Yeachan-Heo, 2026-02-02)
- OMX is substrate-sibling of OMC by the same author. Relation to OMO identical to OMC's — same different-author, same partial-vocabulary-overlap pattern.
- **Distinct primitive**: OMX's Rust runtime (`omx-runtime-core`) is unique to OMX. OMO stayed in TypeScript (though it does ship compiled binaries via `bun compile`).

### vs Huntley's Ralph Wiggum (2025-07)
- **Namesake borrowed, mechanism changed**: OMO's Ralph Loop is a **native hook-driven OpenCode state machine**, not `while true; do cat PROMPT.md | agent ; done`. Completion signaling: `<promise>DONE</promise>` XML-tag in transcript, not file sentinel. Iteration bound: 100 (normal) / 500 (ultrawork). Cancellation: `/cancel-ralph`.
- **ULW variant adds mandatory Oracle verification** — not just completion-promise but third-party verification step.
- **"No dangerously-skip-permissions"** posture: OMO has per-agent tool restrictions (oracle/librarian/explore read-only; momus cannot write/edit/delegate). Explicit opposite of Huntley's YOLO stance.

### vs Superpowers (obra, 2025-10)
- Both use Anthropic Agent Skills format — OMO via Claude-Code-compat layer. Different skill *content*: Superpowers ships personal-craft skills (tdd/brainstorming/systematic-debugging); OMO ships operational orchestration skills (ai-slop-remover/review-work/git-master/frontend-ui-ux/playwright).
- **Axis F (skill as unit of discipline) 7th independent use**: OMO's SKILL.md loader + YAML frontmatter + skill-embedded MCP is a further evolution. Promotion minor additional evidence.

### vs GSD (2026-02)
- Both orchestrators wrap plan-then-execute. GSD uses `{PHASE}-{WAVE}-{TYPE}.md` regex naming; OMO uses `.sisyphus/plans/{plan-name}.md` (single file per plan) + notepad subfolder.
- Different stage count: GSD is 5-phase (discuss/plan/execute/verify/ship); OMO is 3-layer (Planning/Execution/Worker) with variable sub-agent fan-out per plan task.
- **Axis C (mode splitting) 10th independent use**: OMO's 3-layer × 8-category × 11-agent × N-skill product is the largest mode-product observed. Promotion triple-confirmed.

### vs Compound Engineering (Every.to, 2026)
- Both pursue "learn during execution" — but OMO's wisdom notepads are **in-plan intra-session**, CE's `docs/solutions/` is **cross-session cross-project**.
- **Axis L (instinct learning)**: not a direct match. OMO's notepads are cumulative-during-execution, not auto-extracted-skills-for-future-use. OMO does NOT have ECC's `/skill-create` or CE's `/ce:compound` equivalent. The `/learner` auto-extraction skill is OMC's addition.

### vs Ouroboros (Q00, 2026-01)
- **Axis I (ambiguity-as-numeric-gate)**: OMO does NOT use a numeric threshold. Prometheus planner uses qualitative 5-check clearance; ultrawork uses prompt-shape CAPS discipline; no weighted ambiguity score. OMC's `deep-interview` (Ouroboros-inspired) is the numeric gate in the trilogy.
- OMO's approach is **non-numeric and non-evolutionary** — it does not auto-iterate ontology repair or evolve-step. Atlas's notepad accumulation is the closest analogue but it's per-plan, not cross-plan ontology evolution.

### vs ECC (2026-01)
- ECC's 47 specialized agents vs OMO's 11 + category-spawned Sisyphus-Junior. OMO consolidates specialization into the **category × skill product** (primitive Δ4 new), avoiding 47 distinct agent definitions.
- ECC's `/learn`→`/evolve`→confidence pruning has no OMO analogue.

## 12. Open questions

- **Bus-factor on code-yeongyu**: 90% of commits are from one person + two AI-secondary accounts. What happens to OMO if the author stops? Is Sisyphus Labs the hedge?
- **Team-mode maturity**: Team-mode landed 2026-04-17 with message/task/runtime schemas. Is this pre-release experimentation, or the new canonical team surface? Not yet in a released version.
- **Hashline empirical claim verification**: "Grok Code Fast 1: 6.7% → 68.3%" — does a reproducible benchmark script exist? Would need to read `src/tools/hashline-edit/hash-computation.test.ts` + locate the bench harness.
- **Claude Code compatibility depth**: README says "hooks, commands, skills, MCPs, plugins all work unchanged." How deep is this? Do Anthropic's `SubagentStop`, `PermissionRequest` hooks work end-to-end via OMO's claude-code-* loaders? (The architecture diagram lists 10 OpenCode hooks, not Claude Code's 5 — so Claude Code hook events are likely translated/mapped.)
- **Relation to Jobdori** (author's AI assistant, "heavily customized fork of OpenClaw"): Is Jobdori OMO-the-agent running in production, or a separate sibling product? Would need to check Sisyphus Labs waitlist page.
- **`justsisyphus` and `sisyphus-dev-ai` accounts**: are they bots, code-yeongyu's alts, or other humans? Concentration of commits is suspicious.
- **License SUL-1.0**: custom ("Sisyphus User License"?) — what does this allow/restrict? Repo returns `license: other / spdx_id: NOASSERTION`. May affect how components can be extracted.
- **Azure PostHog limits**: v3.17.3 disabled exception autocapture to stay within free tier (188K exceptions in 5 days). Does this mask real reliability issues?
- **Fourth team-coordination reinvention**: OMO team-mode is the 4th distinct team implementation observed (CC-native, OMX Rust, OMO in-process/tmux, …). Does the ecosystem ever converge on a shared team contract? Or is independent reinvention the steady state?

## 13. OMO vs OMC/OMX provenance & delta table (new axis)

| Primitive | Origin harness | Origin date | Traveled to | Status in OMO |
|---|---|---|---|---|
| `ultrawork` / `ulw` keyword mode | **OMO** | 2025-12-13 | OMC (skills/ultrawork/SKILL.md), OMX (`$ultrawork`) | **Native/Origin** |
| Ralph Loop / `/ulw-loop` slash command | **OMO** | 2025-12-30 | OMC `$ralph`, OMX `$ralph` | **Native/Origin** |
| `Sisyphus` agent name | **OMO** | 2025-12-xx | `oh-my-claude-sisyphus` npm name (OMC) | Native/Origin |
| `Prometheus` planner | **OMO** | 2026-01-09 | (not in OMC/OMX) | Native/Exclusive |
| `Hephaestus` agent | **OMO** | 2026-02-01 (v3.2.0) | (not in OMC/OMX) | Native/Exclusive |
| `Atlas` conductor | **OMO** | 2026-02-xx | (not in OMC/OMX) | Native/Exclusive |
| Metis/Momus/Oracle/Librarian | **OMO** | various | (not in OMC/OMX with these names) | Native/Exclusive |
| `IntentGate` (regex keyword classifier) | **OMO** | 2025-12-14 | OMC keyword-detector (ported) | Native/Origin |
| `Hashline` LINE#ID edit tool | **OMO** (inspired by oh-my-pi) | 2026-xx | (not in OMC/OMX) | Native/Exclusive |
| `boulder-state` / `.sisyphus/boulder.json` | **OMO** | 2026-03-18 | (not in OMC/OMX — different state layout) | Native/Exclusive |
| Notepad system (`learnings/decisions/issues/verification/problems.md`) | **OMO** | 2026-xx | (not in OMC/OMX with this structure) | Native/Exclusive |
| `/init-deep` hierarchical AGENTS.md | **OMO** | 2026-xx | (not in OMC/OMX) | Native/Exclusive |
| `$deep-interview` Socratic numeric gating | **OMC** | 2026-03-02 (Ouroboros-inspired) | OMX `$deep-interview` | **Absent in OMO** |
| `$ralplan` consensus planning auto-gate | **OMC** | 2026-01-22 | OMX `$ralplan` | **Absent in OMO** (Prometheus is opt-in analogue) |
| `$team` staged pipeline + `.omc/handoffs/` | **OMC** | 2026-xx | OMX `$team` (Rust) | **Absent in OMO** (team-mode is different architecture) |
| `/learner` auto-skill-extraction | **OMC** | 2026-xx | (not ported elsewhere) | **Absent in OMO** |
| `OpenClaw` webhook gateway | **OMC** | 2026-02-25 | OMX (02-26), OMO (03-16 with env var rename) | **Imported to OMO** |
| Rust runtime (`omx-runtime-core`) | **OMX** | 2026-02-xx | — | Absent (OMO stayed TypeScript) |
| Frozen state contracts (`docs/contracts/*.md`) | **OMX** | 2026-xx | — | Absent (OMO uses TS types + Zod, not frozen .md contracts) |
| Category × Skill orthogonality | **OMO** | 2026-xx | (partial in OMC via stage routing) | **Native/Origin** |

**Direction of vocabulary flow:**
```
OMO (Dec 2025) ─── ultrawork, ralph-loop, sisyphus, prometheus, hashline, intent-gate ──→ OMC (Jan 2026) ─── deep-interview, ralplan, team-staged, learner ──→ (not ported back to OMO)
      ↑                                                                                            │
      │                                                                                            ↓
      └─────────────────────────────── OpenClaw (Feb 2026, OMC origin) ──────────────────────→ OMX (Feb 2026) ─── Rust runtime (OMX-exclusive)
      │                                                                                            │
      └─────────────────────────────── OpenClaw (Mar 2026, env var renamed) ─────────────────────  ┘
```

Two different authors, one shared Discord, one shared contributor (`junhoyeo`), bidirectional primitive porting with attribution drift.

## 14. Transferable primitives ★

Each: name / 2-line description / assumed context / standalone-extractable?

### P1. Single-keyword entry mode with regex detector + caps-yelled system-prompt injection
- A single keyword (`ultrawork`/`ulw`) typed anywhere in user prompt activates a heavy-weight mode via hook-driven system-prompt prepending. The prompt uses extreme discipline language ("CODE RED", "UNACCEPTABLE", violation tables) to enforce pre-implementation certainty without a separate planner.
- **Assumed context**: host CLI exposes an `UserPromptSubmit` or equivalent hook that can inject system-prompt fragments; model respects CAPS yelling.
- **Standalone-extractable?** **YES**. Copy the regex + copy the prompt template + wire into any hook system. The specific capability ("one keyword = whole-session mode switch") is portable without the rest of OMO.

### P2. Multi-lingual intent classification regex (IntentGate)
- Single regex per intent type combining English verbs + Korean/Japanese/Chinese/Vietnamese equivalents, stripped-of-code-blocks before matching, outputs discriminated-union intent type. Used to auto-inject appropriate system-prompt fragment.
- **Assumed context**: multi-language user base, desire to route without explicit slash commands.
- **Standalone-extractable?** **YES**. The pattern (code-block strip → multi-lingual regex → intent type → message injection) is a 30-line primitive.

### P3. Hashline content-addressable edit tool (`LINE#ID`)
- Read output tags every line with a 2-char content hash (e.g., `42#VK|`). Edit calls reference the tag; if content hash no longer matches, edit is rejected before corruption. Eliminates whitespace-reproduction issues and stale-line errors.
- **Assumed context**: custom edit tool allowed; agent trained or prompted to reference LINE#ID.
- **Standalone-extractable?** **PARTIAL**. Concept is clean and implementation is ~500 LOC of hash + edit-executor code. Porting requires: (a) modifying the read tool to emit tags, (b) modifying the edit tool to validate tags, (c) prompt-engineering the model to use the format. Oh-my-pi originated the idea; OMO refined it. Attribution should be to both.

### P4. Category × Skill × Persona orthogonality in subagent delegation
- Three independent dimensions when spawning subagents: **category** (model + temperature + prompt_append), **load_skills** (tool + MCP grant), **subagent_type** (persona + tool restriction). `task(subagent_type="sisyphus-junior", category="visual-engineering", load_skills=["frontend-ui-ux"])`. Prevents combinatorial sprawl (no need for 11×8=88 agent definitions).
- **Assumed context**: subagent delegation is first-class; model diversity matters.
- **Standalone-extractable?** **YES**. The design principle (factor delegation dimensions orthogonally, define defaults that collapse N×M into a stable subset) is a ~50-line config schema + runtime resolver. This is primitive Δ4 (new schema candidate).

### P5. Wisdom-accumulation notepad system (5 typed notepads per plan)
- `.sisyphus/notepads/{plan}/{learnings, decisions, issues, verification, problems}.md`. Atlas writes after every sub-delegation; every subsequent sub-delegation reads current notepads. Categories: Conventions, Successes, Failures, Gotchas, Commands. Survives across iterations within one plan; doesn't survive across plans.
- **Assumed context**: orchestrator pattern (conductor delegates to workers); plan has multiple tasks; context window is not infinite.
- **Standalone-extractable?** **YES**. Directory structure + write-after-delegate policy + read-at-prompt-injection. ~100 LOC. This is primitive Δ5 (new schema candidate).

### P6. Boulder-state JSON for multi-session plan resumability
- Single `{active_plan, started_at, session_ids[], session_origins{}, plan_name, agent, worktree_path, task_sessions{}}` JSON file. Lets user close and reopen CLI, resume with `/start-work`, with automatic direct-vs-appended session classification and per-task session-reuse via `task_sessions` map.
- **Assumed context**: sessions are ephemeral, plans span multiple sessions, worktrees allow parallel work.
- **Standalone-extractable?** **YES**. Tiny schema; generalizable to any multi-session workflow. Contract is simpler than OMX's multi-file frozen state (`ralph-state-contract.md` etc.).

### P7. Hierarchical AGENTS.md injection via `/init-deep`
- Auto-generates AGENTS.md at project root + subdirectories. Scoring heuristic: files-per-dir, total-lines, max-depth, large-files count, monorepo-detection, multi-language detection determines how many AGENTS.md to emit and where. Inject hook reads relevant AGENTS.md based on CWD.
- **Assumed context**: large codebase with >10 subdirectories; context window budget concern; monorepo support wanted.
- **Standalone-extractable?** **YES**. The scoring function is portable. Requires: (a) writer agent (can be ad-hoc), (b) read-time CWD-based injector hook.

### P8. Read-only planner + mandatory gap-analyzer + optional ruthless reviewer triad
- Prometheus (planner) interviews user, then MUST call Metis (gap analyzer) to catch hidden intentions before finalizing. For high-accuracy mode, Momus (reviewer) runs with strict acceptance criteria (100% file ref verification, ≥80% clear refs, ≥90% concrete acceptance, zero business-logic assumptions, no max retry limit). Each role is a separate agent with tool restrictions.
- **Assumed context**: multi-agent spawn is cheap; decision-grade planning is valuable.
- **Standalone-extractable?** **YES**. The 3-role pattern is portable; the specific thresholds are tuning. OMC/OMX ralplan has a similar Planner→Architect→Critic triad — confirms this is a cross-harness pattern.

### P9. Conductor that cannot write code
- Atlas **cannot write/edit/task/call_omo_agent**. It can only read files, run commands, search, inspect diagnostics. All implementation is delegated. This enforces "conductor vs player" discipline at the tool-permission layer, not just via prompt.
- **Assumed context**: host supports per-agent tool restrictions (allowlist/blocklist).
- **Standalone-extractable?** **YES**. The restriction itself is a 1-line config. The implication (enforced separation of concerns) is a design primitive portable to any permission-aware harness.

### P10. Two-promise-tag completion contract (normal vs verified)
- Two Ralph-Loop templates. **Normal**: agent emits `<promise>DONE</promise>` → loop ends. **Ultrawork**: agent emits `<promise>DONE</promise>` → loop continues with Oracle verification prompt → Oracle verification detector confirms → loop ends. One is fast; the other is trust-but-verify. User picks via `/ralph-loop` vs `/ulw-loop`.
- **Assumed context**: a transcript-readable Stop hook; parsable promise tag; a verifier agent available.
- **Standalone-extractable?** **YES**. The two-variant completion pattern (self-signaled vs third-party-verified) is a portable termination-contract primitive.

### P11. Substrate-commitment strategy (inbound compatibility, not outbound portability)
- OMO commits to OpenCode as substrate and provides **inbound** Claude Code compat (loads CC skills/agents/commands/MCPs). Does NOT emit itself to CC. Strategy: "OpenCode won; port other ecosystems to us."
- **Assumed context**: substrate has its own plugin system; author has a strong substrate preference; competing ecosystems have loadable artifact formats.
- **Standalone-extractable?** **PARTIAL**. The strategy is portable; the implementation requires substrate-specific loaders (`claude-code-*-loader` in OMO's case).

### P12. Proactive + reactive fallback system separation
- **Model-fallback** (proactive, in `chat.params` hook): tries next model in chain on predicted unavailability. **Runtime-fallback** (reactive, in `session.error` hook): responds to actual errors. **Explicit architectural note** in AGENTS.md: "Two fallback systems: `model-fallback` (proactive, chat.params) vs `runtime-fallback` (reactive, session.error)". Documented separation.
- **Assumed context**: multi-provider world; both quota-exhaustion-before-call and mid-call-errors are common.
- **Standalone-extractable?** **YES**. The binary (pre-call vs post-error) is a portable architectural distinction.

### P13. Pre-emptive context compaction monitor
- 10-file `preemptive-compaction*` hook suite: monitors context utilization, tracks model-specific limits (AWS Bedrock variants distinct), detects quality degradation, triggers compaction before hitting hard limit. Includes "no-text-tail" detection, degradation monitor regression tests.
- **Assumed context**: agents run long sessions; context-rot is real; compaction hurts but hitting limit is worse.
- **Standalone-extractable?** **PARTIAL**. Concept is portable; implementation is non-trivial (~10 files of monitoring logic + model-specific limit table).

### P14. Dual-package transition with legacy-warning load path
- `oh-my-opencode` and `oh-my-openagent` both published simultaneously. Config files `oh-my-opencode.json[c]` and `oh-my-openagent.json[c]` both recognized. Legacy entries load with warning. Migration tool available (`migrateConfigFile()` with `_migrations` tracking, idempotent). Doctor command checks for legacy package name.
- **Assumed context**: product rebrand with existing user base; want zero-downtime transition.
- **Standalone-extractable?** **YES**. Pattern for any renamed open-source tool.

### Rejected as primitive
- **52-hook architecture with 3-tier classification** (Core+Continuation+Skill) — too implementation-specific; not a primitive but an architectural artifact.
- **Sisyphus/Hephaestus/Prometheus Greek-mythology naming** — branding choice, not a portable primitive.
- **Bun runtime dependency** — not a primitive, it's a constraint.
- **Dev-branch-is-default release posture** — engineering artifact, not a primitive.
- **Telemetry-on-by-default with PostHog** — not a primitive.
- **`@justsisyphus`/`sisyphus-dev-ai` secondary contributor accounts** — not a primitive, but worth noting as an operational signature.

## Sources

### Primary (repo metadata + user identity)
- https://api.github.com/repos/code-yeongyu/oh-my-openagent — repo metadata (id 1108837393, created 2025-12-03, 52,694 stars)
- https://api.github.com/users/code-yeongyu — author: YeonGyu-Kim (@sionic-ai, Seoul, Twitter @q_yeon_gyu_kim)
- https://api.github.com/users/Yeachan-Heo — contrast: Bellman (@Layoff-Labs, different person)
- https://api.github.com/repos/code-yeongyu/oh-my-openagent/releases — 60+ releases
- https://api.github.com/repos/code-yeongyu/oh-my-openagent/tags — v3.x tags from 2026-01-20
- https://api.github.com/repos/code-yeongyu/oh-my-openagent/branches — default branch: `dev`
- https://api.github.com/repos/code-yeongyu/oh-my-openagent/contributors — top contributors (code-yeongyu: 3,409, junhoyeo shared w/ OMC)

### Primary (README + docs)
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/README.md
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/AGENTS.md — the authoritative code map (11 agents, 52 hooks, 26 tools, 3-tier MCP, 377k LOC, 104 barrel exports)
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/docs/manifesto.md — "human in the loop = bottleneck"
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/docs/guide/overview.md
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/docs/guide/orchestration.md — Prometheus/Atlas/Sisyphus-Junior three-layer architecture w/ mermaid
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/docs/reference/features.md — 11 agents' tool restrictions, 8 categories, fallback chains

### Primary (source code — the load-bearing evidence)
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/src/features/builtin-commands/templates/ralph-loop.ts — RALPH_LOOP_TEMPLATE + ULW_LOOP_TEMPLATE + CANCEL_RALPH_TEMPLATE
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/src/features/builtin-commands/templates/start-work.ts — boulder.json schema, worktree flow, task decomposition mandate
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/src/features/builtin-commands/templates/handoff.ts — single-session compaction (NOT stage-to-stage RPC)
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/src/features/builtin-commands/templates/init-deep.ts — hierarchical AGENTS.md generation
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/src/features/boulder-state/types.ts — BoulderState + TaskSessionState + PlanProgress + TopLevelTaskRef
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/src/features/boulder-state/storage.ts — JSON read/write with prototype-pollution guards
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/src/features/team-mode/types.ts — Zod v4 schema: MESSAGE_KINDS, TASK_STATUSES, RUNTIME_STATUSES, max 8 members
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/src/hooks/keyword-detector/detector.ts — IntentGate detector
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/src/hooks/keyword-detector/constants.ts — KEYWORD_DETECTORS list + multi-lingual regex
- https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/src/hooks/keyword-detector/ultrawork/default.ts — ULTRAWORK_DEFAULT_MESSAGE verbatim (the "CODE RED" caps-yelled discipline prompt)

### Primary (git history — provenance evidence)
- `f57aa39d53` 2025-12-13 — `ultrawork` first commit
- `0f0f49b823` 2025-12-30 — `Ralph Loop` first commit
- `d13e8411f0` 2026-01-17 — `/ulw-loop` command added
- `3a02feb187` 2026-01-20 — v3.0.0 oh-my-opencode rebrand
- `03b346ba51` 2026-03-16 — OpenClaw integrated into OMO (imported from OMX)
- `2c8813e95d` 2026-03-16 — `fix: rename OMX_OPENCLAW env vars to OMO_OPENCLAW` (proof of OMX-origin for env vars)
- `b00e22c2b8` 2026-04-17 — team-mode first commit
- Release tag `v3.11.0` 2026-03-07 — repo renamed `oh-my-opencode → oh-my-openagent`

### Primary (OMC git history — for provenance cross-reference)
- OMC `cd98f12fac` 2026-01-09 — **"feat: Complete port of oh-my-opencode to Claude Code"** (OMC declares itself as OMO port)
- OMC `313688413f` 2026-01-09 — "feat: Sync all prompts and patterns with oh-my-opencode"
- OMC `f9a4afcba5` 2026-01-09 — "feat: Add hooks and skills system matching oh-my-opencode"
- OMC `739784905f` 2026-03-02 — **"feat(skills): add deep-interview skill with Ouroboros-inspired Socratic questioning"** (OMC deep-interview origin, not from OMO)
- OMC `e1a121af9c` 2026-01-22 — first ralplan commit (OMC origin, not in OMO)
- OMC `e745e20814` 2026-02-25 — first OpenClaw commit (OMC origin of the webhook gateway)

### Primary (release notes)
- https://github.com/code-yeongyu/oh-my-openagent/releases/tag/v3.11.0 — "First release as an oh-my-openagent. We have changed our name to make it less confused; OmO and Sisyphus is about the whole architecture — not just a plugin."
- https://github.com/code-yeongyu/oh-my-openagent/releases/tag/v3.17.3 — disabled PostHog exception autocapture due to free-tier overflow (188K in 5 days)
- https://github.com/code-yeongyu/oh-my-openagent/releases/tag/v3.17.2 — rename-transition hardening, delegate-task contract updates, 36+ bug fixes in one release

### Secondary (referenced in OMO README — not cross-checked, for context only)
- https://blog.can.ac/2026/02/12/the-harness-problem/ — Can Bölük, "The Harness Problem" (Hashline inspiration source)
- https://github.com/can1357/oh-my-pi — oh-my-pi (Hashline origin)
- https://x.com/thdxr/status/2010149530486911014 — thdxr tweet (Anthropic/OpenCode blocking claim)
- https://sisyphuslabs.ai/ — Sisyphus Labs commercial brand
- https://ohmyopenagent.com/ — OMO website
