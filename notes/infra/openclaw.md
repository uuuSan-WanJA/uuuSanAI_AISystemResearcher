---
title: OpenClaw — Local-first Gateway as single control plane
slug: openclaw
tier: infra / control-plane / gateway
date: 2026-04-19
author: openclaw org (canonical)
created: 2025-11-24
primary_source: https://github.com/openclaw/openclaw
docs: https://docs.openclaw.ai
gateway_protocol_ref: https://docs.openclaw.ai/reference/rpc
sub_component: https://github.com/Yeachan-Heo/clawhip
related_corpus:
  - notes/harness/omx-omc.md (OpenClaw section — OMC originated the integration 2026-02-25)
  - notes/harness/omo.md (OpenClaw section — OMO adopted 2026-03-16)
  - notes/agents/hermes.md (Hermes has `hermes claw migrate` importing from ~/.openclaw)
topic: infra
tags: [gateway, control-plane, local-first, personal-assistant, openclaw, clawhip, korean-author, side-channel, multi-channel-inbox]
status: deep-dive
confidence: high
rounds: 1 main-session (Mode B — direct primary-source reads via WebFetch + GitHub API)
axes_used: [1, 2, 3, 4-partial, 5, 6, 7, 8, 9, 10, 11, 12]
axes_added: [tier (META), gateway-event-surface, side-channel-for-notifications]
axes_dropped: []
probe_method: Main-session direct read — WebFetch + Bash curl with --max-time 30. Sub-agent harness-analyzer had attempted this earlier and hung 52+ min; this run runs in main session with timeouts.
---

## TL;DR (3 lines)
OpenClaw is a **local-first personal AI assistant** positioned as a **"Gateway — single control plane for sessions, channels, tools, and events"** — a fundamentally different architectural tier from the CLI harnesses in our corpus (it *hosts* harnesses rather than *being* one). At **360,378★ / 73,478 forks / created 2025-11-24** with sponsorship from OpenAI, GitHub, NVIDIA, Vercel, Blacksmith, and Convex, it is one of the most-starred OSS AI projects of 2026 and the first infra-tier entry in our corpus. Its canonical primitive is **multi-channel inbox + multi-agent routing** (WhatsApp / Telegram / Slack / Discord / Signal / iMessage → per-agent isolated sessions), with a companion **sub-component `clawhip`** (Rust, 783★, by Yeachan Heo — OMC/OMX author) that **deliberately bypasses the gateway's agent sessions** for notification routing to prevent context pollution — a second-order primitive (*side-channel for agent notifications*) that is genuinely novel in the corpus.

## Proposed schema deltas

### META-tier axis (from Hermes note, now reinforced)
- **Rationale reinforced**: OpenClaw is unambiguously **infra/gateway tier**, architecturally distinct from harness-tier (agent-loop-shapers) and agent-framework-tier (Hermes). The tier distinction is load-bearing for future axis applicability — e.g. axis D (gate mechanism syntax) applies within a harness's agent loop, but inapplicable at gateway tier where the gateway routes *between* sessions rather than within one.
- **Promotion threshold**: already met. OpenClaw confirms the infra tier exists as a populated category; harness tier has 14 entries; agent-framework has 1 (Hermes); technique has 11 (Anthropic sweep + Karpathy).
- **Action**: promote META-tier axis from candidate to confirmed in `meta/harness_schema.md`.

### New candidate axis: Gateway event surface (load-bearing for infra tier)
- **Rationale**: At infra tier, the *protocol surface* is the critical dimension. OpenClaw's README refers to "[Gateway protocol](https://docs.openclaw.ai/reference/rpc)" but does not enumerate the event types inline. clawhip's documentation reveals a concrete v1 contract of provider-native hook events (`SessionStart, PreToolUse, PostToolUse, UserPromptSubmit, Stop`) plus 5 event families (`github.*, git.*, agent.*, session.*, tmux.*`). This is materially different from the axis-4 lifecycle semantics we use at harness tier — here the lifecycle is the gateway's **multi-session** lifecycle, not a single loop's iteration.
- **Proposed form**: "At infra tier: (a) event types enumerated with payload contracts, (b) lifecycle ordering (connection / turn / heartbeat / shutdown), (c) reply channel semantics, (d) delivery guarantees (at-least-once / at-most-once / exactly-once)."
- **Promotion threshold**: 1st case (OpenClaw). 2nd case candidate: a future probe of AgentMail or any other gateway-tier product.

### New candidate primitive: Side-channel for agent notifications (clawhip)
- **Rationale**: The single most transferable pattern observed here. clawhip deliberately DOES NOT flow notification events through an agent session — instead routing via a `sources → mpsc queue → dispatcher → router → renderer → sink` pipeline that delivers Discord/Slack messages **without any LLM interaction**. The motivation (per README): an agent session that receives every Slack ping accumulates conversational context proportional to notification volume → quality degrades. By contrast a side-channel leaves the session lean and only surfaces notifications to humans.
- **Proposed form**: "Does the gateway/harness route notifications through an agent session or through a separate non-LLM pipeline? If separate: what's the trigger contract (hooks? pubsub?), the renderer model (templates? prompts-but-stateless?), the delivery sinks?"
- **Promotion threshold**: 1st case (clawhip). 2nd case candidate: any CI-alert integration in other harnesses (Cline, GitHub Copilot) would qualify if it avoids the agent turn.

---

## 1. Identity & category

- **Category (tier)**: infra / control-plane / gateway (first corpus entry in this tier)
- **Canonical repo**: https://github.com/openclaw/openclaw — `openclaw/openclaw`
- **Description verbatim (repo)**: *"Your own personal AI assistant. Any OS. Any Platform. The lobster way. 🦞"*
- **Full framing (README)**: *"OpenClaw is a personal AI assistant you run on your own devices. It answers you on the channels you already use."*
- **Positioning sentence (README)**: *"personal, single-user assistant that feels local, fast, and always-on."*
- **Created**: 2025-11-24 (GitHub API)
- **Language**: TypeScript, 494.5 MB repo size
- **License**: MIT
- **Latest release**: v2026.4.15 (2026-04-16) — release artifacts include `OpenClaw-2026.4.15.dmg` (macOS), `OpenClaw-2026.4.15.dSYM.zip`, `OpenClaw-2026.4.15.zip`
- **Stars / forks / pushed**: **360,378★ / 73,478 forks / pushed 2026-04-19** (most-starred entry in our corpus by ~3.5×)
- **Sponsors**: OpenAI, GitHub, NVIDIA, Vercel, Blacksmith, Convex — industry-backed at a level no other corpus entry approaches
- **Companion apps**: macOS menu bar app, iOS/Android nodes
- **Extension marketplace**: [ClawHub](https://clawhub.com) — skills registry (separate domain/product)

### Sub-component
- **clawhip**: https://github.com/Yeachan-Heo/clawhip
  - 783★, Rust, created 2026-03-08
  - Description verbatim: *"claw + whip: Event-to-channel notification router — bypasses gateway sessions to avoid context pollution"*
  - **Author note**: by Yeachan Heo (OMC/OMX creator) — NOT by the `openclaw` org. This is a cross-author tool that integrates via `@openclaw install <repo_url>`. Ecosystem is multi-author.

## 2. Problem framing

OpenClaw's self-description frames the problem as **channel integration** first, **control plane** second:

> *"OpenClaw is a personal AI assistant you run on your own devices. It answers you on the channels you already use."*

The "channels you already use" are messaging platforms where the user already receives notifications and has conversations — **WhatsApp, Telegram, Slack, Discord, Signal, iMessage**. OpenClaw's architectural answer to the problem is: **stand a gateway in front of these channels, route inbound messages to isolated agents, route agent replies back through the same channels**.

This is architecturally distinct from the harness-tier framing ("how should an agent loop be shaped?") and from Hermes's agent-framework framing ("how should the agent's runtime embed a learning loop?"). OpenClaw's framing is *infrastructure* — how should I/O between humans (on existing channels) and agents (isolated per session) be mediated, secured, and observed?

## 3. Architecture — local-first gateway shape

### 3a. Control-plane positioning (verbatim)
> *"Local-first Gateway — single control plane for sessions, channels, tools, and events."*

Four first-class entities:
- **Sessions**: isolated agent instances. Each has its own state; OpenClaw routes messages to/from specific sessions. Non-main sessions can run inside per-session Docker sandboxes (`agents.defaults.sandbox.mode: "non-main"`).
- **Channels**: messaging inboxes (WhatsApp, Telegram, Slack, Discord, Signal, iMessage, etc.)
- **Tools**: registered capabilities agents can invoke (MCP? native tools? not explicitly enumerated in README)
- **Events**: the wire format of what flows between sessions / channels / tools (Gateway protocol RPC at `docs.openclaw.ai/reference/rpc` — not fetched this round)

### 3b. Multi-agent routing
> *"Multi-agent routing to isolated agents with per-agent sessions"*

Agents are **isolated from each other** — one agent cannot see another's session state. Routing is the gateway's responsibility.

### 3c. Local-first stance
"Local-first" is the architectural stance most often cited. Concrete signals:
- **Companion apps run on-device** (macOS menu bar, iOS/Android nodes)
- **Per-session Docker sandbox available** (not remote containers)
- **DM pairing gate** — unknown senders must be approved LOCALLY by the user, not via a cloud allowlist
- Release artifacts distribute native desktop binaries (`.dmg`, `.zip`), not just a web SaaS

Whether data EVER leaves the device (model-inference paths, LLM API calls) is not specified in the README — presumably model-of-choice can be cloud (OpenAI API) or local (ollama / local models). Model failover referenced but not probed.

## 4. Gateway protocol — event schema (PARTIAL)

### 4a. What the README says
The README defers to **external docs** for gateway protocol specifics:
> *"Gateway protocol — [docs.openclaw.ai/reference/rpc]"*

This round did NOT fetch the RPC reference page. **[OPEN QUESTION]** full event type enumeration is the highest-priority follow-up probe.

### 4b. What is inferable from clawhip's contract
clawhip consumes the **v1 provider-native hook contract**:
- `SessionStart`
- `PreToolUse`
- `PostToolUse`
- `UserPromptSubmit`
- `Stop`

This is clawhip's consumption surface, not necessarily OpenClaw's canonical event list — clawhip normalizes these from `codex` / `claude` providers. But the v1 contract is likely the common denominator of what OpenClaw-adjacent tools emit.

### 4c. Event families clawhip ROUTES
- `github.*` (issue-opened, issue-commented, issue-closed, pr-status-changed)
- `git.*` (commit, branch-changed)
- `agent.*` (started, blocked, finished, failed)
- `session.*` (started, blocked, finished, failed, retry-needed, pr-created, test-*, handoff-needed)
- `tmux.*` (keyword, stale)

These are the **output** event families clawhip emits to sinks (Discord, Slack). They do not necessarily map 1:1 to OpenClaw's internal gateway events but tell us what the ecosystem considers noteworthy.

## 5. Harness integration contract

OpenClaw exposes `@openclaw install <repo_url>` as a primary install entrypoint for skill/tool packages. The expected downstream automation (per clawhip's README, as the archetype case):

> *"(1) clone repo (2) run ./install.sh (3) read SKILL.md (4) attach skill (5) scaffold config/presets (6) start daemon (7) run live verification"*

So the integration contract is **SKILL.md + install script + optional daemon**. The skill is attached to an agent session; any daemon component runs alongside the gateway.

### Cross-references to existing corpus harness notes
- **OMC** ([omx-omc.md](../harness/omx-omc.md)): originated OpenClaw integration 2026-02-25 (commit `feat(openclaw): add OpenClaw webhook gateway integration (#1023)`). Hook envelope events: `session-start, stop, keyword-detector, ask-user-question, pre-tool-use, post-tool-use`. Config: `~/.claude/omc_config.openclaw.json`. Reply channels: Discord / Telegram / Slack bidirectional via `OPENCLAW_REPLY_CHANNEL`, `OPENCLAW_REPLY_TARGET`, `OPENCLAW_REPLY_THREAD`.
- **OMX**: ported OMC's integration 2026-02-26. Normalization: OMX aliases normalized into OpenClaw gateway mappings; native bridge at `integrations/omx/`; daemon fallback via `POST /api/omx/hook`.
- **OMO** ([omo.md](../harness/omo.md)): adopted 2026-03-16 with env var rename `OMX_OPENCLAW → OMO_OPENCLAW`. Direction of flow is reversed vs the skill-vocabulary flow (which is OMO → OMC → OMX): OpenClaw integration flows **OMC → OMX → OMO**.
- **Hermes** ([hermes.md](../agents/hermes.md)): has `hermes claw migrate` command that imports `~/.openclaw` settings, memories, skills, API keys. Hermes positions itself as an **OpenClaw replacement / migration target**, not a peer.

## 6. Side-channel primitive (clawhip) ★ — load-bearing

### 6a. Problem statement (verbatim)
From clawhip README tagline: *"bypasses gateway sessions to avoid context pollution"*

### 6b. Mechanism (verbatim)
> *"[sources] -> [mpsc queue] -> [dispatcher] -> [router -> renderer -> Discord/Slack sink] -> [Discord REST / Slack webhook delivery]"*

Daemon process listens on `http://127.0.0.1:25294`. Ingress via:
- Provider hooks (`SessionStart, PreToolUse, PostToolUse, UserPromptSubmit, Stop`)
- Event source adapters (git, GitHub, tmux)
- Thin CLI clients (`clawhip send`, `clawhip github issue-opened`, `clawhip native hook --provider codex --file payload.json`)

Routing config example (TOML):
```
[[routes]]
event = "git.commit"
filter = { repo = "my-app" }
slack_webhook = "https://hooks.slack.com/services/T.../B.../xxx"
```

### 6c. Why it exists as a separate tool
Per clawhip README:
> *"clawhip no longer treats provider-specific launch wrappers as the public integration surface. Codex and Claude own session launch plus hook registration; clawhip stays the routing, normalization, and delivery layer."*

Architectural stance: **separation of concerns** — routing/delivery decoupled from agent session logic, to avoid notification logic bloating the agent's context and to avoid embedding notification logic in every provider.

### 6d. Why this is novel at corpus level
No other corpus entry has a documented **"bypass the agent session on purpose"** primitive. The closest analog is OMC/OMX/OMO's notepads (persistent inter-turn learning) — but those live INSIDE the agent's awareness. clawhip is the first primitive that says "**do not tell the agent**" by design, because the agent doesn't need to know about every Slack ping to do its job, and knowing pollutes it.

This primitive is transferable: any harness with an event-hooked architecture could implement a side-channel for notifications, and many would benefit.

## 7. Security / permission / credential model

### DM pairing gate
> *"DM pairing (dmPolicy='pairing'): unknown senders receive a short pairing code and the bot does not process their message."*

Approval via `openclaw pairing approve <channel> <code>` adds senders to a local allowlist. This is a **zero-trust default** for DMs — new senders cannot invoke the assistant without explicit user approval.

### Opt-in open mode
`dmPolicy="open"` with explicit allowlist (`allowFrom`) allows public DM invocation — opt-in, not default.

### Session isolation
> *"Set agents.defaults.sandbox.mode: 'non-main' to run non-main sessions inside per-session Docker sandboxes."*

Per-session Docker sandboxing available for non-main sessions. Main session's sandbox stance not specified in README excerpt (follow-up).

### Credential storage
Not explicitly enumerated in the README. Sponsors list includes Convex (database-as-a-service) — may suggest remote option. **[OPEN QUESTION]** whether credentials stay local by default.

## 8. Standards relationship

### MCP
README references *"[Models](https://docs.openclaw.ai/concepts/models)"* and *"[Model failover](https://docs.openclaw.ai/concepts/model-failover)"* but does not claim explicit MCP implementation in this excerpt. **[OPEN QUESTION]** — docs page probe needed.

### ACP (Agent Communication Protocol)
Not referenced in README. Cross-check from Hermes note: Hermes README does not reference ACP either. The "ACP" mentioned in some 2026 SEO articles about Hermes + OpenClaw communication appears to be hearsay — neither project's primary source confirms ACP as a shared standard. **Refuted at corpus level** pending any primary-source evidence.

### Gateway protocol (own)
OpenClaw has its own Gateway protocol documented at `docs.openclaw.ai/reference/rpc`. This is a FIRST-PARTY spec, not adherence to an external standard. Whether it shares wire format with any other project is unknown.

## 9. Ecosystem uptake

- **GitHub**: 360,378★ / 73,478 forks / 4,897 commits (from commit count inferrable from activity) / TypeScript primary
- **Industry sponsors**: OpenAI, GitHub, NVIDIA, Vercel, Blacksmith, Convex — **exceptional backing**, no other corpus entry has this sponsor profile
- **Commercial arm**: `openclaw.ai` domain (suggests paid offering adjacent to OSS core)
- **ClawHub** (clawhub.com): skills registry. Separate product / domain from the repo.
- **Companion apps**: macOS menu bar app, iOS/Android nodes — desktop-native distribution alongside Linux/server
- **Jobdori AI** (baseline facts): Korean AI assistant built on a "heavily customized fork of OpenClaw" — notable because it's cross-ecosystem (Korean commercial use of an international open-core)
- **Release cadence**: v2026.4.15 (2026-04-16) is the latest as of this note. Versioning uses date-based tags. Repo pushed 2026-04-19 (active). Sub-component clawhip at 783★ after 6 weeks (2026-03-08 → 2026-04-19) — respectable for a Rust router tool.

## 10. Gateway-first architecture — articulated case

OpenClaw's stance, synthesized from the README:

1. **Channel integration is the primary surface**. Users don't adopt new chat apps to talk to AI; they expect AI to show up in the apps they already use. Therefore the gateway's first responsibility is *reaching the user where they are*.
2. **Multi-agent routing requires a coordinator**. If one assistant can spawn isolated agents for different tasks (a research agent, a home-automation agent, a code-review agent), something has to route inbound messages to the right one. That something is the gateway.
3. **Local-first is possible and desirable**. Personal AI assistants should run on the user's device; the gateway makes this feasible by coordinating sessions, channels, and tools locally rather than requiring a cloud coordinator.
4. **Tool/skill registry benefits from a control plane**. `@openclaw install` and ClawHub centralize skill discovery and attachment — agents don't each maintain their own tool registries.

**Contrast with Hermes's stance** ([hermes.md](../agents/hermes.md)): Hermes embeds the **learning loop** (memory + skill authoring) inside the agent's runtime. Hermes also has a gateway (for Telegram/Discord/Slack/WhatsApp/Signal/Email/Home Assistant routing) but treats it as an I/O surface, not a primary concern. OpenClaw's gateway is the primary concern — the assistant's personality, memory, and learning happen **downstream of** the gateway, per-session.

**The tradeoff in two lines**: gateway-first optimizes for *multi-session observability, multi-channel I/O, and tenant isolation*. Loop-first (Hermes-style) optimizes for *integration density, inline self-improvement, and single-agent depth*. Both are viable architectures for different scales — OpenClaw scales to "one user, many agents, many channels" (multi-agent personal assistant); Hermes scales to "one agent that grows across sessions" (self-improving personal agent).

## 11. Transferable primitives

### P1. Local-first gateway with per-session isolation (tier: infra)
- **Description**: A control plane that owns session/channel/tool/event routing, runs on the user's device, and sandboxes non-main agent sessions in per-session Docker containers.
- **Assumed context**: Single-user deployment (team extension would require the gateway to be multi-tenant — a different architecture).
- **Standalone-extractable?**: **partial**. The gateway model is extractable in principle; the specific multi-channel integration code is tightly coupled to provider APIs and is long-tail work.

### P2. Side-channel for agent notifications (clawhip) ★
- **Description**: Route hook events (git, GitHub, tmux, session lifecycle) to notification sinks (Discord, Slack) via a non-LLM pipeline, bypassing the agent session to keep it context-clean.
- **Assumed context**: Any harness with an event-hooked architecture (OMC/OMX/OMO/Claude Code hooks/Codex hooks).
- **Standalone-extractable?**: **yes**. clawhip is already a separate Rust binary with a clean attachment contract. The pattern (event pipeline → renderer → sink, no LLM) is general.
- **Anti-pattern to avoid**: running the renderer through an LLM prompt. The whole point is to skip the LLM for predictable notification formatting.

### P3. Zero-trust DM pairing gate
- **Description**: Unknown senders to a DM channel must receive a pairing code and be approved by the user locally before their messages are processed. Default-deny for DMs.
- **Assumed context**: Any channel where random senders could appear (DMs, email). Less relevant for push-only webhooks or private channels.
- **Standalone-extractable?**: **yes**. Cleanly specified. `openclaw pairing approve <channel> <code>` is a minimal interface that transfers to any channel-routing harness.

### P4. SKILL.md + install script as gateway attachment contract
- **Description**: Third-party extensions ship a `SKILL.md` + `install.sh` pair; the gateway reads SKILL.md to understand the skill, runs install.sh to scaffold, starts any daemon, verifies, and attaches. Unified across skill origin (openclaw-authored or cross-author like clawhip).
- **Assumed context**: Any hub that wants a consistent third-party extension model.
- **Standalone-extractable?**: **yes**. This is essentially a more-structured version of the Anthropic Agent Skills format with an execution layer.

### P5. Date-based release versioning (`v2026.4.15`)
- **Description**: Release tags use date format `vYYYY.M.D` rather than semver. Signals "release cadence" (this is the April 15 release) rather than "breaking-change commitment" (semver semantics).
- **Assumed context**: Products with frequent releases where consumers care about "how recent" more than "is this API stable."
- **Standalone-extractable?**: **yes, trivially**. Observational only — not a technical primitive but a practice. Hermes also uses this (`v2026.4.16` tag).

## 12. Open questions (follow-up probes)

1. **Gateway protocol RPC spec** — full enumeration of event types at `docs.openclaw.ai/reference/rpc`. Highest-priority.
2. **Model-of-choice data path** — when OpenClaw runs a cloud model (OpenAI API), what leaves the device? How is this squared with the "local-first" stance?
3. **Credential storage** — are API keys, session tokens, channel bot tokens stored locally or in a Convex-backed cloud service?
4. **MCP implementation** — does OpenClaw register MCP servers as first-class tools, or treat them separately?
5. **Commercial openclaw.ai** — what does the paid tier offer vs the OSS core? Multi-user? Hosted gateway?
6. **ClawHub skill registry** — curation model (moderated? open?), skill signing, security review process.
7. **main session sandbox stance** — only non-main sessions sandbox by default; main session's stance not specified.
8. **Relationship to Anthropic's Claude Cowork** — superficially similar categories (multi-channel multi-agent personal assistant). Positional differentiation.
9. **openwork as alternative** — `notes/harness/openwork.md` is pitched as "open-source alternative to Claude Cowork built for teams, powered by OpenCode"; openwork vs OpenClaw is *personal-single-user* (OpenClaw) vs *team-first* (openwork). A future digest could map the single-user/team/multi-tenant axis of personal-assistant gateways.

---

## Cross-note corrections forced by this deep-dive

1. **Hermes note** ([hermes.md](../agents/hermes.md)): The "AIAgent loop rather than gateway control plane" positioning needs qualification — Hermes DOES have a gateway (for messaging I/O), it just puts the learning loop at the center instead of the gateway. This is a **difference of emphasis**, not a binary architectural choice. (Already captured in Hermes main-session verification block on 2026-04-19.)
2. **ACP claim** — the 2026 SEO article claim that "Hermes communicates with OpenClaw via ACP" is NOT supported by either project's primary sources. **Both notes now refute ACP** as a shared-standard primitive.
3. **OpenClaw integration sections in `omx-omc.md` and `omo.md`** — the existing OpenClaw descriptions are consistent with this deep-dive; no corrections needed, but they now have a primary cross-reference (this note) instead of being orphan integration mentions.
