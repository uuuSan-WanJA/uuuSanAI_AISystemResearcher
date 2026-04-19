---
title: Hermes Agent (Nous Research) — deep-dive
tier: agent-framework
status: deep-dive + main-session-verification-pass
confidence: medium-high (after 2026-04-19 main-session verification)
rounds: 1 (sub-agent, constrained) + main-session verification pass (2026-04-19)
axes_used: [1, 2, 3, 4, 5, 6, 8, 11, 12, META-tier, SI-mechanism, DD-gossip (refuted), ACP-contract (refuted)]
axes_added: [META-tier (new), SI-mechanism (new)]
axes_dropped: [7 (HITL — not probed), 9 (empirical claims — benchmarks not in README), 10 (failure modes — not probed), DD-gossip (refuted by primary source — Hermes README has no gossip protocol), ACP-contract (refuted by primary source — Hermes README has no ACP)]
subject: Hermes Agent
primary_source: https://github.com/NousResearch/hermes-agent
docs: https://hermes-agent.nousresearch.com/docs/
license: MIT
version_verified: v0.10.0 (git tag `v2026.4.16`, released 2026-04-16)
repo_stats_verified_2026-04-19: 101,159 stars / 14,385 forks / 4,897 commits / created 2025-07-22 / default branch main
runtime_notes: |
  Sub-agent round was executed WITHOUT Agent/Task dispatch tool and WITHOUT WebFetch
  (nested sub-agent runtime constraint). The note was initially confidence=low, heavy
  on schema deltas but thin on Hermes internals. A main-session verification pass on
  2026-04-19 retrieved primary-source data via WebFetch + GitHub API (see "✅
  Main-session verification" block). Two schema candidates (DD-gossip, ACP-contract)
  are REFUTED by primary source. Confidence upgraded to medium-high.
---

## 0. Procedural note

Originally written 2026-04-19 by a harness-analyzer sub-agent running in constrained runtime (no Agent/Task dispatch, no WebFetch). That round produced the tier framing and schema deltas but could not verify Hermes internals — all specific claims were tagged `requires-codex-in-main`. On the same day, a main-session verification pass retrieved primary-source evidence via WebFetch + GitHub API and corrected the note (see next block). The original hedged sections are kept below as an audit trail; the verification block supersedes them where they conflict.

---

## ✅ Main-session verification (2026-04-19) — supersedes hedged claims below

### Verified identity & scale
- **Version**: **v0.10.0** (git tag `v2026.4.16`, released **2026-04-16**). The sub-agent's v0.7/v0.8 discrepancy is resolved: neither was current — actual latest is v0.10.0.
- **License**: **MIT** — confirmed via GitHub API.
- **Repo stats**: **101,159 stars / 14,385 forks / 4,897 commits**, created **2025-07-22**. This is the **largest-star agent framework in our corpus** (vs OMO 52.7k, OMC 29.9k, OMX 24.1k, openwork 13.9k). Active for 9 months before hitting 100k stars.
- **Self-description** (verbatim, [README](https://github.com/NousResearch/hermes-agent)): *"The self-improving AI agent built by Nous Research. It's the only agent with a built-in learning loop"* and *"creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past"*.

### Verified architecture
Hermes has **both an agent loop AND a gateway** — the sub-agent's "loop-first vs gateway-first" dichotomy was over-simplified. The README distinguishes:
- **Agent loop** — autonomous skill creation, periodic memory nudges, procedural learning. This is the distinguishing feature.
- **Gateway** — multi-platform messaging control plane for Telegram, Discord, Slack, WhatsApp, Signal, Email, Home Assistant.

So the correct corpus framing is: Hermes puts the **learning loop** (memory + skill curation) inside the agent runtime; it still has a gateway, but the gateway is the **I/O surface**, not the control plane. OpenClaw, by contrast, puts the gateway itself at the center as the "single control plane for sessions, channels, tools, events." The distinction is *what is primary*, not *presence/absence*.

### Verified memory substrate
Four-layer hybrid state:
1. **MEMORY.md** — bounded always-in-context (agent-curated).
2. **USER.md** — bounded always-in-context (user model, dialectic via Honcho).
3. **FTS5** — full-text session search for cross-session recall with LLM summarization.
4. **Honcho** — dialectic user modeling for user state.

The "SQLite + FTS5, ~10ms at 10k+ skills" claim in the sub-agent note is consistent with FTS5 layer; the specific numbers are from baseline facts and not re-verified here. Two-tier (bounded + unbounded) framing holds.

### Verified self-improvement mechanism
Verbatim [docs landing](https://hermes-agent.nousresearch.com/docs/): *"closed learning loop"* with four components — **"Agent-curated memory with periodic nudges, autonomous skill creation, skill self-improvement during use, FTS5 cross-session recall with LLM summarization"**. This matches the sub-agent's (a) + (a') + (d) classification. **Not (b) self-modifying code, not (c) weight updates.** Hermes is **compatible with `agentskills.io` open standard** per README — skills are a documented portable format, not private to Hermes.

### Verified tool surface
- **40+ tools** confirmed.
- **Messaging integrations**: Telegram, Discord, Slack, WhatsApp, Signal, Email, Home Assistant.
- **Subagents**: *"Spawn isolated subagents for parallel workstreams. Write Python scripts that call tools via RPC, collapsing multi-step pipelines into zero-context-cost turns."* — this is a distinctive "**zero-context-cost RPC**" primitive not seen elsewhere in corpus. Worth tagging as a transferable primitive.
- **v0.10.0 headline feature (Nous Tool Gateway)**: paid Nous Portal subscribers get web search (Firecrawl), image generation (FAL / FLUX 2 Pro), TTS (OpenAI), browser automation (Browser Use) via subscription — no additional API keys. Subscription-based tool economics is distinct from free-per-use corpus peers.

### Verified terminal backends (6)
**local, Docker, SSH, Daytona, Singularity, Modal** — confirmed verbatim from README "Runs anywhere" section. These are not TUI-layer choices (as the sub-agent speculated) but **execution-environment adapters** — where the agent's shell actions actually run. Modal = serverless containers, Daytona = dev-environment-as-a-service, Singularity = HPC/academic.

### REFUTED schema candidates
- **DD-gossip axis (agent discovery via gossip protocol)**: **REFUTED for Hermes.** The Hermes README contains no reference to gossip protocols or agent-to-agent discovery mechanisms. The sub-agent's task brief propagated this claim from a secondary source (dev.to / lushbinary / clawbot blogs) that appears to have conflated Hermes with a different system. Remove from P4 transferable primitives.
- **ACP-contract axis (Agent Communication Protocol)**: **REFUTED for Hermes.** No ACP references in README or docs landing page. However, Hermes has a **different relationship with OpenClaw**: a `hermes claw migrate` command that imports OpenClaw's settings, memories, skills, and API keys from `~/.openclaw`. This positions Hermes as an **OpenClaw replacement / migration target**, not as a peer that talks to OpenClaw via a shared protocol. The correct axis here is not ACP but "**migration-importer-from-competitor**" as a go-to-market/competitive primitive.

### New primitives confirmed for transferable list (supersede P4/P5 of Section 11)
- **P4-new. Zero-context-cost RPC subagent pattern** — subagents are spawned with isolated scratch Python scripts that call tools via RPC; the subagent's conversation is not absorbed into the parent turn, only the final result. This collapses multi-step pipelines without paying context. Distinct from Cline's read-only-fanout or OMC's staged-pipeline handoff.
- **P5-new. Migration-importer as positioning** — `hermes claw migrate` imports `~/.openclaw` contents. This is a go-to-market primitive: lower switching cost by automating competitor-data import. Worth tagging as a corpus-level observation.
- **Kept**: P1 (self-improvement via skill catalogue), P2 (two-tier memory), P3 (loop-first as stance — refined to "learning-in-loop, gateway-as-I/O" rather than "no gateway").

### Unresolved after verification (still open)
- **Gossip protocol** — baseline fact entry J mentions it. Not in README. Could exist in deeper docs under `/docs/developer-guide/architecture/` which WebFetch could not render on the landing page. If the claim came from an earlier Hermes version that has since removed the feature, entry J may need its own revision.
- **ACP** — same story. Possibly an earlier-version feature since removed, or a conflation with a different project.
- **40+ MCP integrations vs 40+ built-in tools** — README said "40+ tools" flat; the sub-agent brief claimed "40+ MCP integrations" additionally. These may be the same "40+" double-counted. Needs doc dive to disambiguate.

---

## 1. Identity & provenance

- **Project**: Hermes Agent
- **Author**: Nous Research
- **Repo**: https://github.com/NousResearch/hermes-agent
- **Docs**: https://hermes-agent.nousresearch.com/docs/
- **DeepWiki mirror**: https://deepwiki.com/NousResearch/hermes-agent
- **Self-description (task brief, unverified in primary source)**: "The agent that grows with you"
- **Launch**: February 2026 (task brief)
- **Version status**: Task brief says **v0.7.0 (2026-04-03)**; baseline facts file entry J says **v0.8.0** at 2026-04 sweep with **3,496+ commits**. Discrepancy unresolved. `requires-codex-in-main` → verify current tag + commit count via GitHub API.
- **Ecosystem signal (baseline facts J)**: `awesome-hermes-agent` curation list exists; `Hermes WebUI` is a separate ecosystem project.
- **License**: UNVERIFIED. `requires-codex-in-main`.

**Quote (baseline facts, not primary source — treat as summary)**: *"자기 개선 에이전트. 복잡 태스크 후 자율 스킬 생성, 사용 중 스킬 자가 개선, SQLite + FTS5로 크로스 세션 메모리(~10ms 검색, 10k+ 스킬 스케일), MEMORY.md 2,200자 / USER.md 1,375자로 바운디드 큐레이션."* — `notes/harness/_collected_facts_2026-04-13.md` entry J.

> Confidence: medium for the identity fields, low for any detail beyond what baseline facts already state.

## 2. Problem framing

The architectural claim in the task brief is that Hermes **"centers on the AIAgent loop rather than a gateway control plane"** — an explicit positioning against gateway-first architectures (OpenClaw is named as the counterexample).

Baseline facts entry J paraphrases this as **"에이전트 런타임 + 자기-성장 메모리"** — i.e. the framing unifies the agent's *runtime loop* and its *persistent memory* as a single architectural concern, rather than treating memory as an external service the agent calls into.

**Verbatim primary-source quote**: NOT YET OBTAINED. `requires-codex-in-main` → fetch the architecture section of https://hermes-agent.nousresearch.com/docs/ and capture the exact wording of the "AIAgent loop vs gateway control plane" positioning. Without this quote, Hermes's problem framing is hearsay.

> Confidence: low. We have the claim second-hand; we do not have the sentence Nous Research wrote.

## 3. Control architecture — the AIAgent loop

**Claim (unverified)**: The loop itself is a first-class architectural concern — the learning cycle is embedded in the loop, not bolted on via a separate gateway.

**What is known from baseline facts**:
- Hermes is an **agent runtime** (not a plugin, not a skill pack). It owns the loop.
- The loop integrates **memory updates** and **skill generation** as steps, not as post-hoc pipelines.

**What is NOT known**:
- The exact step sequence of the loop (tool-call → memory-update → skill-check → … ?).
- Where the learning step sits (inline vs async vs end-of-task).
- Whether the loop is a literal `while` loop, an event-driven FSM, or a graph executor.
- How tool approval / HITL gates (if any) fit into the loop.

`requires-codex-in-main` → trace the main loop in the Hermes Agent repo (entry point: likely `hermes_agent/main.py` or `src/agent/loop.*`). Codex-grade code reasoning needed because "loop architecture" is a structural claim that should be verified from multiple call-sites, not a single doc sentence.

> Confidence: low. The architectural claim is plausible and internally consistent with the self-improvement positioning, but unverified.

## 4. State & context model — memory backends + skill storage

This is the **strongest** cell of the note because baseline facts entry J provides concrete specifics:

- **Memory substrate**: SQLite + FTS5 (full-text search).
- **Performance claim**: ~10ms search latency.
- **Scale claim**: 10k+ skills.
- **Bounded curation artifacts**: `MEMORY.md` (~2,200 chars), `USER.md` (~1,375 chars). These are the short-lived, human-curated state surfaces that live alongside the long-tail SQLite store.

This pattern is important: **long-tail SQLite for scale** + **small, bounded Markdown files for primacy / always-in-context** is a hybrid state design. It parallels Anthropic Agent Skills' SKILL.md (always-short, on-demand-expandable) but extends it with a searchable durable layer.

`requires-codex-in-main`:
- Enumerate **all** pluggable memory backends in v0.7.0 (task asked "what backends are supported?"; baseline only names SQLite+FTS5 as the default).
- Resolve whether the MEMORY.md / USER.md sizes are **limits** (enforced) or **observed averages** (emergent).
- Trace how a skill flows from "generated at end of task" → "stored in SQLite" → "retrieved next session" — i.e. the read path and write path.

> Confidence: medium for the SQLite+FTS5 fact (it is in baseline facts with specific numbers — which tend to come from real docs). Low for "pluggable backends plural" — we only have evidence of one.

## 5. Prompt strategy / self-improvement mechanism ★

Per task brief, the self-improvement mechanism must be classified into one of:
- (a) skills-from-experience generation
- (b) self-modifying code
- (c) weight updates / fine-tuning
- (d) memory-based adaptation only

**Baseline facts evidence**: *"복잡 태스크 후 자율 스킬 생성, 사용 중 스킬 자가 개선"* — which maps to:

- **(a) Skills-from-experience generation**: YES. "After complex tasks, autonomous skill generation." A skill is authored by the agent at task completion.
- **(a') skill self-improvement in-use**: YES. "In-use skill self-improvement" means existing skills get edited when used. This is a stronger form of (a) — skills are not immutable once authored.
- **(b) Self-modifying code**: UNCLEAR. Skills in Hermes appear to be *prompts / instructions + optional scripts* (by analogy to Anthropic Agent Skills), not the agent's own runtime code. So (b) in the strict sense — rewriting the loop itself — is **probably not** happening, but `requires-codex-in-main` to confirm whether skill scripts can be executable Python that the agent imports.
- **(c) Weight updates**: Very unlikely. No fine-tuning infrastructure mentioned anywhere in baseline facts. Would be surprising for a client-side agent framework.
- **(d) Memory-based only**: NO. The memory layer exists, but the skill-generation step makes this richer than pure memory.

**Working classification**: Hermes is an **(a) + (a') skill-generation + skill-mutation** self-improvement mechanism backed by a **(d) memory-based adaptation** layer underneath. It is NOT weight-update or full self-modifying-code in the Rich Sutton / razzant/ouroboros sense.

This is a distinct architecture from:
- **Ouroboros (Q00)**'s `evolve` step — which edits the *spec*, not the agent's own skills.
- **Compound Engineering**'s `Compound` step — which feeds review output back into subsequent runs but doesn't author new durable skills.
- **Superpowers** — skills are hand-authored by humans; agent consumes but does not produce.

**Verbatim quote from Hermes docs on self-improvement**: NOT OBTAINED. `requires-codex-in-main`.

> Confidence: medium on the classification (well-constrained by the baseline fact's wording). Low on internal mechanics (where in the loop generation fires, what the skill file format is, how name-collision is handled in a 10k+ skill catalogue, whether the agent reviews its own generated skills).

## 6. Tool surface

**Reported surface (task brief, unverified)**: 40+ built-in tools plus an MCP adapter layer covering 40+ integrations.

**Categories task asked to enumerate**: communication, VCS, DB, payment, cloud.

**Baseline facts**: no tool enumeration. `requires-codex-in-main` → read `hermes-agent/tools/` (or equivalent) and enumerate.

**MCP adapter distinctive claim (task brief, unverified)**: Hermes's MCP layer is richer than a bare `@modelcontextprotocol/sdk` wrap. The likely meaning — unverified — is that Hermes presents MCP tools as first-class citizens alongside built-in tools, with unified name-spacing, permission model, and possibly skill-linking. `requires-codex-in-main` to verify.

**MCP server mode (task brief, unverified)**: Hermes itself exposes as an MCP server. The consumer is likely any MCP-speaking client (Claude Code, Cursor, etc.). This flips the usual arrow: instead of Hermes consuming MCP tools, Hermes *is* the tool for another agent. `requires-codex-in-main`.

**6 terminal backends (task brief)**: Exact list not in baseline facts. The number 6 is specific enough to be a design choice — likely reflects an abstraction over (xterm / iTerm2 / Warp / Ghostty / PowerShell / plain PTY?) but this is speculation until verified. `requires-codex-in-main`.

> Confidence: low across all of §6. This section should be filled by a probe round before use.

## 7. Human-in-the-loop — DROPPED (no evidence)

No baseline evidence on approval gates, autoplay defaults, or YOLO mode. Task brief did not prioritize this axis. Leave for a follow-up if relevant.

## 8. Composability — gossip protocol, ACP, MCP server mode

Three distinct composability surfaces are claimed:

### 8a. Gossip protocol (peer discovery)

**Task brief claim**: gossip-based agent-to-agent discovery; WebSocket is the default transport; transport is pluggable.

**Baseline facts evidence**: none specific. This is a feature on the task-brief hypothesis list.

**What "gossip protocol" typically means in distributed systems**: each node periodically exchanges partial membership views with random peers; eventually every node learns of every other node with probability → 1. It's decentralized (no central registry) and tolerant of partial failures.

**Why this is architecturally notable for an agent framework**: most agent frameworks assume a known counterparty (you register a tool/URL). Gossip implies Hermes is being designed for **a mesh of Hermes instances that find each other without pre-registration**. This is a different deployment model.

`requires-codex-in-main`:
- Confirm gossip implementation exists (look for `gossip/`, `discovery/`, SWIM / HyParView references).
- Enumerate pluggable transports (WebSocket is claimed default — what else: gRPC? libp2p? plain TCP?).
- Identify network topology (random peer sampling? structured? DHT?).

### 8b. ACP (Agent Communication Protocol)

**Task brief claim**: Hermes talks to OpenClaw via ACP; ACP is a defined contract.

**Baseline facts entry O**: gpters.org article "Claude Code + OpenClaw — 하네스 엔지니어링으로 스스로 진화하는 시스템" is the only mention of OpenClaw in our corpus. No technical specifics.

**Critical open question**: is ACP a **Nous-Research-internal convention** (coupling Hermes to OpenClaw) or a **broader community standard** (MCP-like, with multiple implementers)? The answer determines how "transferable" ACP is as a primitive.

`requires-codex-in-main`:
- Fetch the ACP spec / schema (likely at https://hermes-agent.nousresearch.com/docs/ under a "protocols" or "interoperability" section, or in the repo under `spec/acp/`).
- Identify other implementers (search GitHub for `agent-communication-protocol` / `implements ACP`).
- Capture verbatim: the message schema, the transport binding, the versioning posture.

### 8c. MCP server mode

Covered in §6 above. Cross-listed here because "Hermes-as-MCP-server" is a composability surface — it lets non-Hermes agents consume Hermes capabilities as tools.

> Confidence: low on all three sub-axes until probed. High-level framing (gossip ≠ registry, ACP ≠ MCP, MCP-server-mode flips the arrow) is sound.

## 9. Empirical claims & evidence — DROPPED (no baseline data)

No benchmark numbers, no adoption metrics beyond "Nous Research brand" and an awesome-list.
`requires-codex-in-main` to sweep the docs for any published evaluation.

## 10. Failure modes & limits — DROPPED (no baseline data)

`requires-codex-in-main`.

## 11. Transferable primitives ★

Even with low confidence on Hermes internals, the framework-level primitives Hermes exemplifies are extractable *at the category level*. Each primitive is listed with an honest standalone-extraction verdict.

### P1. Self-improvement via agent-authored skill catalogue (tier: agent-framework)
- **Description**: The agent's own successful runs produce durable skill artifacts that are stored in a searchable long-tail store (SQLite+FTS5 here) and retrieved on subsequent runs. Skills can be edited in-use, not just at authoring time.
- **Assumed context**: An agent runtime that owns the loop (not a plugin on a host CLI). Requires a memory substrate with fast full-text search at 10k+ entries.
- **Standalone-extractable?**: **partial**. The *concept* (self-authored skills + durable store) is extractable and has been partially prototyped elsewhere (AutoAgent does a weight-optimization analogue; Ouroboros does the spec-edit analogue). The *integration with the loop* is the hard part — requires decisions about *when* generation fires, *what* qualifies a successful run, *how* to avoid skill-catalogue rot.
- **Anti-pattern to avoid**: naive "log every turn as a skill" → catalogue pollution → retrieval quality collapse. The MEMORY.md / USER.md bounded-curation files suggest Nous Research has explicit limits on what gets promoted to always-in-context vs stays in the long tail.

### P2. Two-tier memory — bounded always-in-context + unbounded searchable
- **Description**: Short, human-readable, size-capped Markdown files (MEMORY.md ~2.2k chars, USER.md ~1.4k chars) hold the primacy slot; a SQLite+FTS5 store holds the long tail. The two tiers are managed distinctly (curation discipline on the small files; scale discipline on the big store).
- **Assumed context**: A long-running agent that has more memory than fits in a single prompt; users who want auditable curation of the "top slice" the agent always sees.
- **Standalone-extractable?**: **yes**. The tier separation and the specific byte budgets are portable to any agent framework. The *curation policy* (what gets promoted from tier 2 to tier 1) is the hard design question.
- **Why this is not the same as "RAG over a big corpus"**: RAG treats all chunks equally and retrieves by similarity. The two-tier design privileges a small handcrafted top layer that the model *always* sees, regardless of query.

### P3. AIAgent-loop-first (versus gateway-first) positioning
- **Description**: Architectural choice to make the agent's inner loop — including memory update and skill authoring — the single first-class concern, rather than deferring those to an external gateway / control plane / router service.
- **Assumed context**: Single-agent-or-small-mesh deployments where you own the runtime. Does not apply to multi-tenant SaaS where tenant isolation forces a gateway.
- **Standalone-extractable?**: **partial (conceptual)**. The *choice* is extractable — it is a design axis to name. The *implementation* is deeply coupled to the rest of the runtime and not portable as a module.
- **Relationship to the gateway-first pole**: the task brief names OpenClaw as the gateway-first exemplar. A full corpus should cover **both poles** and document the tradeoffs (gateway: control, observability, multi-tenancy; loop-first: integration density, self-improvement lives inline, lower deployment overhead).

### P4. Gossip-based decentralized agent discovery (tier: agent-framework)
- **Description**: Instead of a registry or a well-known URL, agents find peers via a gossip protocol. No central coordinator required.
- **Assumed context**: A deployment model where multiple Hermes instances run across a user's devices / a team's machines / a mesh. Not needed if you have one agent.
- **Standalone-extractable?**: **yes, conceptually**. Gossip protocols (SWIM, HyParView, plumtree) are well-studied and library-implementations exist. The agent-specific wrinkle is what gets gossiped (agent identity? skill catalogue hashes? capability advertisements?) — which is the novel design work.
- **Note**: this is unverified in baseline facts. Listed because the task brief treats it as a defining feature and because it is a genuinely distinct primitive vs the rest of our corpus (which assumes single-agent or CLI-substrate composition).

### P5. ACP (Agent Communication Protocol) as a distinct-from-MCP inter-agent contract
- **Description**: A protocol for agent-to-agent (as opposed to agent-to-tool) communication, presumed to cover capability advertisement, task handoff, and result return.
- **Assumed context**: Multi-agent deployments where agents need to negotiate, not just invoke tools.
- **Standalone-extractable?**: **unknown**. The answer depends entirely on whether ACP is a published spec with multiple implementers or a private Nous Research convention. This is probably the single highest-value thing to probe.
- **Why it matters**: MCP solved the tool-wire-format problem. The agent-to-agent wire format is currently a zoo (Letta's custom protocol, AutoGen's internal RPC, CrewAI's Python-only handoffs). If ACP is a serious contender for a community standard, it deserves to be tracked as a category-defining primitive.

### P6. MCP server mode (agent-as-tool flip)
- **Description**: An agent framework that exposes its own capabilities as an MCP server, so other agents can consume it as a tool.
- **Assumed context**: A mesh where Hermes is one agent among many, and sometimes the right design is to call into Hermes rather than to federate with it.
- **Standalone-extractable?**: **yes**. Any agent framework can add an MCP server adapter. The interesting design question is *what surface* to expose — the whole loop? individual skills? memory read-only?
- **Dual-role tension**: a system that is both "MCP server" (exposing tools) and "MCP client" (consuming tools) creates composition possibilities but also cycle risks (agent A calls agent B calls agent A…). Cycle detection is a needed primitive.

## 12. Open questions (load-bearing — parent should dispatch probes)

1. **Verbatim "AIAgent loop vs gateway control plane" quote** — still hearsay. Resolve first. `requires-codex-in-main`.
2. **Version clarification** — v0.7.0 (task brief) vs v0.8.0 (baseline facts). Resolve.
3. **ACP scope** — Nous-internal vs community standard? (Highest-leverage open question.) `requires-codex-in-main`.
4. **Skill file format** — prompt-only, or prompt+executable script? Determines whether self-improvement is (a) or (b).
5. **Loop implementation** — explicit `while` / FSM / graph? Where does skill-gen fire?
6. **Pluggable memory backends** — enumerate beyond SQLite+FTS5.
7. **6 terminal backends** — enumerate and understand why 6.
8. **Tool catalogue** — enumerate and categorize 40+ tools per the task brief's categories (communication, VCS, DB, payment, cloud).
9. **Gossip transport + topology** — confirm existence, enumerate transports, identify topology.
10. **LLM lock-in** — is Hermes Agent locked to the Hermes *LLM* family (Hermes 4, etc.), or model-agnostic? (Nous Research ships both; the name collision is a trap.)
11. **License** — not in baseline facts.

---

## 13. Corpus-level positioning (the real payload of this note)

The user's corpus so far is **harness-tier**: loop-shapers that sit on a substrate (Claude Code, Codex, Cursor, etc.). Hermes is something different — **agent-framework-tier**. It owns the runtime. This is a **tier distinction**, not just another axis.

### Why the tier distinction matters for schema

Current schema axes — Control architecture (3), Prompt strategy (5), Tool surface (6), Composability (8) — *mostly still apply* to Hermes, but they answer different questions:

| axis | harness-tier answer | agent-framework-tier answer |
|---|---|---|
| 3 (control arch) | "what loop does the harness impose on the host CLI?" | "what loop IS the agent?" |
| 5 (prompt strategy) | "what SKILL.md / slash commands are added?" | "what prompt scaffolding is hardcoded in the runtime?" |
| 6 (tool surface) | "what tools does the harness grant/restrict on the host?" | "what tools does the runtime ship natively + via MCP adapter?" |
| 8 (composability) | "does it stack with other harnesses on the same host?" | "does this agent talk to other agents?" |

The axes are *the same words* but the *scope they cover* shifts by an order of magnitude. Without a tier field in frontmatter, cross-tier comparison silently drops meaning.

### Does Hermes test existing candidate axes?

| axis | applies to Hermes? |
|---|---|
| Δ1 (iteration-boundary semantics) | partially — the "end-of-task skill generation" event is an iteration boundary, but the boundary isn't marked by context-wipe or git-commit the way Ralph/GSD define it |
| Δ5 (headless-mode output contract) | **no**. Hermes is a runtime, not a plugin that needs a headless mode |
| Axis C (mode splitting) | **maybe** — if there are "run modes" (interactive / server / MCP) those are different modes in a different sense than Ralph's plan/build split |
| Axis F (skill as unit of discipline) | **partially**. Hermes has skills, but they are agent-authored and stored in a DB — Superpowers' SKILL.md *convention* isn't the unit here |
| Axis G (execution environment as constraint) | **partially**. Memory budgets, 6 terminal backends, and bounded MEMORY.md sizes are environment constraints |
| Axis K (role perspective as constraint) | **no evidence** |
| Axis L (instinct learning as harness layer) | **yes, strongly**. Self-improving skills = instinct learning. This is the closest existing axis fit |
| Axis T (out-of-loop productization surface) | **maybe** — MCP-server-mode is arguably a productization surface |
| Axis U (server-routed fs mutation) | **no** |
| Axis V (mode-as-prompt+tool-allowlist bundle) | **no evidence** |
| Axis W (multi-tier model auto-select) | **no evidence** |

Axis L (instinct learning) is the single existing axis that *really* fits Hermes. Everything else is either tangential or needs a tier-adjusted interpretation.

---

## 14. Proposed schema deltas (for meta/harness_schema.md `## Candidate additions`)

### META-tier axis (proposal)
- **Proposed by**: Hermes Agent deep-dive (2026-04-19)
- **Rationale**: The corpus is silently mixing tiers (harness / agent-framework / infra-gateway / technique). Cross-tier comparison is currently reader-confusing because axes like "control architecture" mean different scopes at different tiers. A frontmatter `tier:` field disambiguates.
- **Proposed values**: `harness` | `agent-framework` | `infra-gateway` | `technique`
- **Proposed form**: *"What tier does this subject occupy? (harness = loop-shaper atop a host CLI; agent-framework = owns the runtime; infra-gateway = routes/gates between LLMs and agents; technique = prompt/context pattern without a product artifact). Cross-tier comparison requires tier-adjusted interpretation of other axes."*
- **Status**: proposed by a single subject (Hermes is the first `agent-framework` entry; OpenClaw pending). Promotion threshold is 1-axis-fits-all vs 2-subjects-tagged. Recommend promoting *immediately* because it is a meta-classification, not a content axis — waiting for a second instance defeats the purpose.

### SI-mechanism axis — Self-improvement mechanism (proposal)
- **Proposed by**: Hermes Agent deep-dive (2026-04-19)
- **Rationale**: Several corpus entries claim "self-improvement" but the mechanisms are non-comparable: Ouroboros edits the spec, Compound Engineering feeds review output back into subsequent runs, AutoAgent does weight-adjacent optimization of harness code, razzant/ouroboros rewrites its own code, Hermes authors durable skills. Without a subtype axis these are all flattened to "improves itself" and the differences are invisible.
- **Proposed values**: `skill-generation` | `self-modifying-code` | `weight-update` | `memory-only` | `spec-iteration` | `harness-code-search` (AutoAgent-style)
- **Proposed form**: *"Does this subject claim self-improvement? If so, by what mechanism: (a) agent-authored durable skills, (b) rewriting its own code, (c) weight updates/fine-tuning, (d) memory accumulation without generation, (e) spec iteration (user-visible artifact), (f) outer-loop harness code search. Mechanisms are not comparable without this subtype."*
- **Status**: Hermes (skill-generation) + Ouroboros (spec-iteration) + Compound Engineering (memory-only or spec-iteration depending on reading) + AutoAgent (harness-code-search) = **4 subjects already differentiated**. Promotion threshold hit; strong recommend.

### DD-gossip axis — Decentralized agent discovery (proposal)
- **Proposed by**: Hermes Agent deep-dive (2026-04-19)
- **Rationale**: Hermes is the first corpus entry to assume a *mesh* of agent instances that discover each other without a registry. This is a primitive that simply does not exist in any harness-tier entry (harnesses run one instance at a time on one host CLI).
- **Proposed form**: *"Does the subject assume peer discovery? If so: (a) central registry, (b) well-known URL / DNS, (c) gossip protocol, (d) not applicable (single-instance). What is the transport? What is the topology? What is gossiped (identity / capabilities / state)?"*
- **Status**: 1 subject. Hold until a second mesh-aware subject appears. OpenClaw probe may be the second.

### ACP-contract axis — Agent-to-agent protocol (proposal)
- **Proposed by**: Hermes Agent deep-dive (2026-04-19)
- **Rationale**: MCP solved agent-to-tool. Agent-to-agent is currently ad hoc. If ACP is a serious contender, the axis should exist. Even if ACP turns out to be Nous-internal, naming the axis lets us track other entrants.
- **Proposed form**: *"Does the subject expose or consume an agent-to-agent protocol that is distinct from MCP? If yes: published spec URL? other implementers? message schema (capability advertisement / task handoff / result return)? transport binding? versioning posture?"*
- **Status**: 1 subject. Hold pending OpenClaw probe and community scan.

---

## 15. Notes for the parent agent

- This note should **not** be read as a finished deep-dive. It is a scaffold plus schema-delta payload.
- Before any graft-evaluator stage uses Hermes as a comparator, run a probe round from the main thread against the `requires-codex-in-main` markers. At minimum resolve: (1) verbatim AIAgent-loop quote, (2) ACP scope, (3) skill file format (determines SI-mechanism classification), (4) version reconciliation.
- The `META-tier` axis and `SI-mechanism` axis are the real output of this cycle — those improve the corpus's analytical resolution regardless of Hermes specifics.
- OpenClaw should be the next `agent-framework`-tier (actually: probably `infra-gateway`-tier) entry, because the tier distinction sharpens once we have both poles named.
