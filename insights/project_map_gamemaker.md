---
project_path: D:\ClaudeCode\Projects\Bundle_GameMaker
slug: gamemaker
rounds: 2
confidence: high
axes_used: [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, A, B, C, D, F, G, H, K, L]
axes_dropped: [9-empirical-claims (internal project, no external benchmark evidence)]
date: 2026-04-13
---

# Project Map — Bundle_GameMaker

## System Purpose

Bundle_GameMaker is a self-improving AI game-studio system with two complementary tiers: **GameMaker** (the product, sold/deployed) generates full game projects for Unreal Engine 5 using a 7-department AI workforce directed by a Creative Director; **GameMakerEngine** (the internal R&D tool) runs competitive agent tournaments (Arena) and evolutionary mutation (Evolver) to continuously produce better agents, then publishes winners through a shared file repository (Bridge) so GameMaker automatically adopts them. A third operational tier — **CollabMonitor_Codex** (Monitor) + **EngineHelper_Codex** (Helper) — supervises the Engine/Helper collaboration loop, decides which side should act next, and keeps a human operator informed about spend vs. usefulness. Two shared libraries (**bridge/** and **uuuSanAI_bridge-types/**) provide the schema contract and physical exchange layer. The active north-star goal is for GameMaker to output a playable Unreal combat-loop project ("The Last Rite"). [observed: uuuSanAI_GameMaker/docs/00_system_overview.md:1-18, CollabMonitor_Codex/state/north_star.md:1-10]

---

## Sub-project Roles & Relationships

| Sub-project | Role | Reads from | Writes to |
|---|---|---|---|
| **uuuSanAI_GameMaker** | Product: 7-dept AI studio → Unreal project output | bridge/agents/ (deploys new agent versions) | bridge/metrics/ (task quality metrics) |
| **uuuSanAI_GameMakerEngine** | R&D: Arena tournament → Evolver mutation → better agents | bridge/metrics/ (perf data) | bridge/agents/ (evolved champions) |
| **bridge/** | Shared file repo: agent packages + metrics + manifest | — | manifest.json (atomic write) |
| **uuuSanAI_bridge-types/** | Shared TypeScript types (@uuusan/bridge-types npm pkg) | — | compiled dist/ |
| **uuuSanAI_GameMakerEngineHelper_Codex** | Supervisor/reviewer: inspects Engine & GameMaker state, emits bounded tasks | Engine collab/state/, GameMaker repo | collab/queues/, collab/decisions/ |
| **uuuSanAI_GameMakerCollabMonitor_Codex** | Orchestration monitor: decides next action (engine-self-progress / helper-review / pause) | collab/ state files, bridge manifest | state/monitor_brief.md, state/state_digest.md, state/operator_report.md |

```
Human
  │
  ▼
CollabMonitor (decides: engine-self-progress / helper-review / engine-helper-followup / pause)
  │                   ▲
  ├─────────────────→ Helper (reviews Engine + GameMaker, emits bounded tasks)
  │
  ▼
GameMakerEngine (Arena → Evolver → Registry → publish champion)
  │                                              │
  │  bridge/agents/ (champion agent)            │
  ▼                                             │
GameMaker (7 depts × 5 phases → Unreal output) ←┘
  │
  │  bridge/metrics/ (task quality data)
  └────────────────────────────────────→ Engine (feedback loop)
```

---

## Current Workflow

A normal work cycle, as reconstructed from Monitor state and Engine/Helper docs:

1. **Monitor assesses state** — reads `state/monitor_brief.md` + `state/monitor_snapshot.json` [observed: CollabMonitor_Codex/CLAUDE.md:13-15]
2. **Monitor decides action** — one of: `engine-self-progress`, `engine-helper-followup`, `helper-review`, `human-review`, `pause`. Default is `pause` when utility is low. [observed: CollabMonitor_Codex/CLAUDE.md:17-22]
3. **Human approves (explicit consent required for blocking actions)** — Monitor MUST obtain explicit blocking consent before running any command that may take >60 seconds on the main thread. [observed: CollabMonitor_Codex/CLAUDE.md:39-40]
4. **Execution is delegated to sub-agents** — Monitor spawns a runner sub-agent (PowerShell scripts) + optional watcher sub-agent. Preferred surface is `subagent-supervised-background`. [observed: state/state_digest.md:37-57]
5. **Engine runs a bounded cycle** — `npm run engine:cycle` → Monitor → Arena (R1 quick + R2 deep judge) → Evolver (6 mutation strategies) → Registry → publish to bridge/. [observed: GameMakerEngine/CLAUDE.md:41-46]
6. **Helper reviews** — `python scripts/helper_cycle.py` reads Engine snapshot, emits at most 1 new Engine follow-up task. Helper cools down if no fresh state change. [observed: EngineHelper_Codex/docs/automatic_collaboration_loop.md:196-229]
7. **GameMaker runs** — `npm run make [phases]` or triggered by Engine's `make` command. 5 phases: Concept → Pre-Prod → Production → Polish → Release. 7 departments each produce artifacts. [observed: GameMaker/docs/00_system_overview.md:42-61]
8. **Metrics flow back** — GameMaker writes to `bridge/metrics/`. Engine reads on next cycle start. [observed: GameMakerEngine/docs/02_bridge_spec.md:57-79]

**Current active focus task**: "Normalize Engine and GameMaker moved paths after Bundle_GameMaker migration" (high priority). Engine snapshot is 604 minutes old; last Monitor recommendation was `helper-review` with high confidence. [observed: state/monitor_brief.md, state/next_work_brief.md]

---

## Existing Harness Patterns

The following harness-engineering primitives are already in place in this project:

### P1. File-based async handoff (Bridge protocol)
Bridge is a pure file repository — no logic, no IPC. Engine writes `agents/{version}/`, GameMaker reads. GameMaker writes `metrics/{id}.json`, Engine reads. `manifest.json` is the single mutable coordination file, updated atomically (temp file → rename). [observed: bridge/CLAUDE.md, GameMakerEngine/docs/02_bridge_spec.md]

### P2. Structured state directory (Monitor state machine)
`CollabMonitor_Codex/state/` contains: `monitor_brief.md`, `state_digest.md`, `operator_report.md`, `next_work_brief.md`, `north_star.md`, `operator_memory.md`, plus multiple `*_handoff.md` files per task. Each file has a distinct role in the coordination protocol. [observed: directory listing]

### P3. Manager-Worker subagent pattern
Both GameMakerEngine and GameMaker CLAUDE.md mandate a strict 3-step delegation protocol: main session plans → implementation Agent (worktree) executes → validation Agent reviews → main receives 200-char summary + PASS/FAIL only. Main never reads code directly. [observed: GameMakerEngine/CLAUDE.md:82-97, GameMaker/CLAUDE.md:43-62]

### P4. Runner-Watcher sub-agent pair
Monitor dispatches a runner sub-agent (launch command) + watcher sub-agent (poll-status command) as a 1:1 pair. Runner and watcher are strictly task-scoped and closed on terminal state. [observed: state/state_digest.md:38-57]

### P5. Bounded cycles with explicit cycle-count consent
Engine CLI requires prior agreement on cycle count. "합의 없이 추가 사이클 금지" (no additional cycles without agreement). [observed: GameMakerEngine/CLAUDE.md:79]

### P6. Preflight decision gate (Monitor main-thread protection)
Before any blocking command (>60s), Monitor must perform a written preflight in the operator response: either ask for explicit blocking consent or choose a non-blocking/delegated path. Never skippable. [observed: CollabMonitor_Codex/CLAUDE.md:39]

### P7. Provider Router with cross-review
Engine has a `RoutedLlmClient` that transparently performs cross-review between providers (Claude/Codex). Quality signals are collected per call. A `ProviderIntelligence` layer provides data-driven routing recommendations. GameMaker has partial implementation (router/tracker/log present; `RoutedLlmClient` + `ProviderIntelligence` pending). [observed: bridge/routing-upgrade-spec.md:1-30]

### P8. Competitive evolutionary loop (Arena + Evolver)
6-mutation-strategy Evolver (exploitation/exploration/crossover/focused/guided_exploration/adaptation) feeds Arena (R1 quick filter + R2 deep LLM judge, 9-dimensional composite score). Champion promotion requires +2.0 margin. Season length 30 cycles. [observed: GameMakerEngine/CHANGELOG.md, GameMakerEngine/docs/05_evolver_spec.md]

### P9. Helper cooldown / steady-state mode
Helper auto-detects when no fresh Engine snapshot or project fingerprint change is available, switches to `review_mode: steady-state`, and stops emitting new Engine tasks. [observed: EngineHelper_Codex/docs/automatic_collaboration_loop.md:220-228]

### P10. Explicit rule-persistence discipline
Monitor CLAUDE.md forbids "memory-only promises" — every new behavioral rule must be written into CLAUDE.md/AGENTS.md in the same turn it is identified, before any reassurance. [observed: CollabMonitor_Codex/CLAUDE.md:26-28]

### P11. Advisor loop (cross-project guidance)
GameMaker's `advise` command collects project state, runs the goal advisor, writes `state/advisor-report.json`. Engine's `gm-advise` calls this and uses the report as cross-project guidance. [observed: GameMaker/CLAUDE.md:29-33]

---

## Pain Points & Open Gaps

All items below are explicitly flagged in state files or CLAUDE.md rules, tagged [observed].

1. **Bundle_GameMaker path migration is unresolved** — Both Engine and Helper have open high-priority tasks to normalize moved paths after the `Bundle_GameMaker` migration. Monitor's top recommended action is `engine-helper-followup` for this. [observed: state/next_work_brief.md:6-7, state/monitor_brief.md:56-58]

2. **`followup-once` zero-task materialization blocker** — Engine's planner surfaces "Unblock followup-once zero-task materialization" as the second active engine task. Confidence: medium. Prior Engine progress attempt failed; helper-review task is open. [observed: state/operator_report.md:17-19, state/monitor_brief.md:48-53]

3. **GameMaker Provider Router upgrade is incomplete** — `RoutedLlmClient`, `ProviderIntelligence`, `quality-signals.ts`, `review-prompts.ts`, and Intelligence types are missing from GameMaker; they exist in Engine. The routing-upgrade-spec.md is a 10-step work order for porting them. [observed: bridge/routing-upgrade-spec.md:12-20]

4. **Director, Shared Infrastructure, Human Interface, Engine Adapter are unbuilt** — GameMaker design status table shows all four as "⬜ 미착수" (not started). [observed: GameMaker/docs/00_system_overview.md:82-89]

5. **Monitor helper efficacy is low** — `helper_efficacy: low` in the latest monitor_brief. The same gap (path normalization) has been repeated across cycles without resolution. [observed: state/monitor_brief.md:8]

6. **Engine snapshot staleness** — Engine snapshot is 604 minutes old; helper snapshot is 699 minutes old at last monitor assessment. Active development loop appears paused. [observed: state/monitor_brief.md:2-3]

7. **MCP permission not yet granted** — Phase 6 of the auto-task log notes "MCP 권한 미부여로 도구 호출 건너뜀" (MCP tools skipped due to missing permission). UE5 Unreal Editor was launched but MCP connection was not authorized. [observed: GameMakerEngine/CHANGELOG.md:66]

8. **GameMaker vitest full-re-run prohibition** — A known anti-pattern: running `vitest` in full on the main thread after worktree already ran it. This is prohibited in CLAUDE.md but remains a recurring behavioral trap requiring explicit rule enforcement. [observed: GameMakerEngine/CLAUDE.md:94-95, GameMaker/CLAUDE.md:55-57]

---

## Axis Inventory

For each schema axis (seed 1–12 and candidate A–M):

| Axis | Status | Evidence |
|---|---|---|
| **1. Identity & provenance** | YES | 6 sub-projects clearly named, TypeScript + Claude CLI / Anthropic API / Codex CLI. |
| **2. Problem framing** | YES | "게임을 만드는 시스템을 더 잘 만드는 시스템" (system for improving game-making). North star: playable Unreal combat loop. |
| **3. Control architecture** | YES | Graph-like pipeline (Monitor → Engine Arena/Evolver → Bridge → GameMaker). Monitor is LLM-directed; Engine cycle is code-directed with LLM sub-calls. |
| **4. State & context model** | YES | File-based: `bridge/` shared repo + `collab/` state dir + `state/*.md` monitor files + `state/orchestrator/cycles/*.json` + worktree per task. |
| **5. Prompt strategy** | PARTIAL | CLAUDE.md per sub-project; Codex cross-review protocol defined; 3-step manager-worker delegation scripted. No SKILL.md convention yet. |
| **6. Tool surface & permission model** | YES | Claude CLI (MAX sub), Anthropic API, Codex CLI, PowerShell scripts, MCP (Unreal Editor). MCP permission issue noted above. |
| **7. Human-in-the-loop points** | YES | Preflight gate (P6), explicit cycle-count consent, operator must approve blocking actions, human-review escalation path. |
| **8. Composability** | YES | Bridge is composable exchange layer. Engine + Helper are designed as stackable collaborators. GameMaker runs standalone. Provider Router supports Claude/Codex substitution. |
| **9. Empirical claims** | NO | Internal project; no external benchmarks. CHANGELOG records concrete E2E outcomes (575 tests, 79 actors verified). |
| **10. Failure modes** | YES | CHANGELOG lists cold-start bug, Windows CLI compat, timeout underestimates, MCP permission denial. CLAUDE.md has anti-patterns. |
| **11. Transferable primitives** | YES | See P1–P11 above. |
| **12. Open questions** | YES | See Pain Points 1–8 above. |
| **A. Iteration-boundary semantics** | YES | Engine cycle = Arena run + Evolver mutation + Bridge publish + cycle record JSON commit. Clear what resets, what commits, what propagates. [observed: orchestrator_spec.md] |
| **B. Backpressure mechanism** | PARTIAL | `pause` is the Monitor default when utility is low. Helper cooldown (P9) is a backpressure rule. No explicit N-parallel:1-sequential rule like Ralph. |
| **C. Mode splitting** | YES | 3-mode Creative Director (auto/persona/human), 5-phase GameMaker workflow, 3 Engine trigger modes (scheduled/threshold/manual), Monitor 4-action dispatch. |
| **D. Gate mechanism syntax** | YES | Preflight written decision (prose gate), explicit cycle-count consent (numeric gate), `pause` default (status enum gate). |
| **E. Authoritative process medium** | PARTIAL | Markdown prose CLAUDE.md + JSON state files. No DOT/Gherkin. Agent specs in `docs/0N_*.md` are prose + diagrams. |
| **F. Skill as unit of discipline** | NO | No SKILL.md convention found. Codex delegation protocol is described in CLAUDE.md prose, not as structured skill files. |
| **G. Execution environment as constraint surface** | PARTIAL | Provider Router controls which LLM executes which task. MCP permission is an explicit environment constraint. Worktree isolation constrains implementation context. |
| **H. Artifact naming schema as protocol** | PARTIAL | `*_handoff.md` files in state/ encode task lifecycle. `agents/v{version}/` + `metrics/YYYY-MM-DD_NNN.json` encode time-ordered sequence. Not as strict as GSD's `{PHASE}-{WAVE}-{TYPE}.md`. |
| **I. Ambiguity-as-numeric-gate** | NO | No numeric threshold gates observed. |
| **J. Deferred-tool loading protocol** | NO | Not observed. |
| **K. Role perspective as constraint surface** | PARTIAL | 7 named departments (Design/Narrative/Programming/Art/Sound/LevelAssembly/QA) each have distinct input/output specs. Creative Director has 3 explicit modes. Monitor operator has a defined role. Not implemented as SKILL.md frontmatter roles. |
| **L. Instinct learning as harness layer** | PARTIAL | Competitive evolution loop (Arena → Evolver) is an automated meta-loop that extracts winning agent patterns and mutates them. Mutation log tracks lineage. But this is structural evolution of agent prompts, not session-level instinct capture (no `/learn`→`/evolve` pattern). |
| **M. Meta-skill bootstrapping** | NO | Not observed. |

---

## Notes for Graft-Evaluator

Based on what is already present and what is clearly missing, the following primitives from synthesis_tier1.md are most directly relevant:

**Highest relevance (gap is explicit + insertion point is clear):**

1. **CP1 / axis-A pattern** — File-based iteration-boundary semantics is already strong in Bridge and Engine cycle records. The gap is that GameMaker's workflow state (phase progression) does not have an equivalent durable artifact record. A Ralph-style or GSD-style iteration boundary record for GameMaker phases would close this gap.

2. **D1 "fresh context / spatial branching"** — The manager-worker worktree pattern (P3) is present but ad-hoc. A formal sub-agent spawning protocol (like GSD's `Task()` wave model) would give the Engine cycle parallel department execution rather than sequential.

3. **Axis-F (Skill as unit of discipline)** — The Codex delegation protocol is prose in CLAUDE.md. Converting it to structured SKILL.md files (with `when-trigger`, `anti-trigger`, and `tool-allow-list`) would make the delegation contract auditable and enforceable — directly addressing the recurring behavioral trap noted in Pain Point 8.

4. **Axis-L (Instinct learning)** — The Engine's Evolver performs structural agent evolution. ECC's `/learn`→`/evolve` instinct loop (session-level pattern capture) and Compound Engineering's `docs/solutions/` YAML tagging loop are both directly analogous. Grafting a session-level learning layer on top of the existing evolutionary loop would give two-tier learning: per-session (instinct) + cross-cycle (evolution).

5. **D3 "state persistence medium"** — Monitor state is files, but 6+ different state file types with no unified naming convention make it hard to debug. GSD's single-directory, role-typed naming convention (`{PHASE}-{WAVE}-{TYPE}.md`) would apply here.

**Moderate relevance:**

6. **Axis-D gate syntax upgrade** — The preflight gate is prose-based. Formalizing it as a typed enum (like Superpowers' `<HARD-GATE>`) would prevent the "vague proceed = blocking consent" failure mode explicitly noted in CLAUDE.md.

7. **Axis-K role perspective** — The 7 departments are role-defined but not enforced via slash-command routing. gstack's role-per-command model could be grafted to give explicit department-scoped execution surfaces.

**Lower relevance / already addressed:**

- Axis-B (backpressure): Monitor `pause`-by-default and Helper cooldown already implement this pattern functionally. A formal B primitive would be additive but not critical.
- Axis-G (execution environment): Provider Router already constrains which LLM executes which task. The MCP permission gap is an ops issue, not a harness design gap.
- Axis-C (mode splitting): Already present across Monitor, Engine, and GameMaker. No new primitive needed.

---

## Evidence Log

| Claim | File : line |
|---|---|
| System purpose / 2-project architecture | uuuSanAI_GameMaker/docs/00_system_overview.md:1-18 |
| North star: The Last Rite playable combat loop | CollabMonitor_Codex/state/north_star.md:1-10 |
| Bridge: no logic, schema + storage only | bridge/CLAUDE.md:3, docs/02_bridge_spec.md:8-10 |
| Bridge manifest atomic write | docs/02_bridge_spec.md:126-130 |
| Manager-Worker 3-step delegation | GameMakerEngine/CLAUDE.md:82-97 |
| Monitor 4-action dispatch protocol | CollabMonitor_Codex/CLAUDE.md:13-22 |
| Preflight gate rule | CollabMonitor_Codex/CLAUDE.md:39-40 |
| Runner-watcher pair topology | state/state_digest.md:38-57 |
| Provider Router routing presets | GameMakerEngine/CLAUDE.md:47-55 |
| Cross-review protocol (Engine) | bridge/routing-upgrade-spec.md:1-30 |
| Missing GameMaker components | GameMaker/docs/00_system_overview.md:82-89 |
| Arena R1/R2 + 9-dim score | GameMakerEngine/CLAUDE.md:28 |
| 6 mutation strategies | GameMakerEngine/CLAUDE.md:30 |
| Champion promotion +2.0 margin | GameMakerEngine/CHANGELOG.md:8 |
| Helper cooldown / steady-state | EngineHelper_Codex/docs/automatic_collaboration_loop.md:220-228 |
| Rule-persistence discipline | CollabMonitor_Codex/CLAUDE.md:26-28 |
| Advisor loop | GameMaker/CLAUDE.md:29-33 |
| Path migration open task (top priority) | state/next_work_brief.md:6-7 |
| Zero-task materialization blocker | state/operator_report.md:17-19 |
| Engine snapshot staleness (604 min) | state/monitor_brief.md:2 |
| MCP permission not granted | GameMakerEngine/CHANGELOG.md:66 |
| Vitest re-run prohibition | GameMakerEngine/CLAUDE.md:94-95 |
| Helper efficacy low | state/monitor_brief.md:8 |
| helper_snapshot_age 699 min | state/monitor_brief.md:3 |
