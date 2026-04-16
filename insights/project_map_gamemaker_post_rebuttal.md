---
project_path: D:\ClaudeCode\Projects\Bundle_GameMaker
slug: gamemaker
version: post_rebuttal
supersedes: project_map_gamemaker.md
note: v2 slot reserved for future revision
rounds: 2
confidence: high
date: 2026-04-15
axes_used: [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, A, B, C, D, E, F, G, H, K, L]
axes_dropped: [9-empirical-claims, I, J, M]
corrections_from_v1: [router-file-count, director-status, gamemaker-owner-classification, missing-component-table, snapshot-staleness, active-focus-task]
---

# Project Map — Bundle_GameMaker (post-rebuttal, fresh)

## 0. Why this rewrite exists

The original map (`project_map_gamemaker.md`, 2026-04-13) took several claims from `uuuSanAI_GameMaker/docs/00_system_overview.md` at face value and inherited stale entries. The live repository and the Monitor's own protocol disagree with those claims in several specific ways. The rebuttal document at `CollabMonitor_Codex/state/report_gamemaker_improvements_rebuttal.md` flagged the problem; this post-rebuttal pass verifies every disputed claim directly against files in `Bundle_GameMaker/`.

**Corrections landed in this pass** (each re-verified):

1. **GameMaker Provider Router is not "incomplete"** — 8 files present in `uuuSanAI_GameMaker/src/router/`, not 3. v1 echoed `bridge/routing-upgrade-spec.md` without checking current code.
2. **Director is not "unbuilt"** — 4 files present in `uuuSanAI_GameMaker/src/director/` with a full `Director` class wired into the entry point.
3. **`uuuSanAI_GameMaker/docs/00_system_overview.md` design-status table is stale** — it still lists "Director / Shared Infrastructure / Human Interface / Engine Adapter ⬜ 미착수", but live `src/` contradicts this. v1 treated the doc as ground truth; v2 treats the code as ground truth.
4. **GameMaker is not a 1st-class execution owner** — Monitor rules explicitly route `uuuSanAI_GameMaker` code work to `engine` owner. v1 framed GameMaker as an independent execution target.
5. **Active focus task has drifted** — v1 recorded "path migration" as top. Live `next_work_brief.md` now leads with "Restore clean Engine build and typecheck health", and `engine_snapshot_age_minutes` is ~2117 (v1 recorded 604). The loop has been paused for longer than v1 implied.
6. **Director / Human Interface / Engine Adapter / Shared Infrastructure are not empty-axes** — they are partially built; the docs just have not been updated.

---

## 1. Sub-project inventory (live file evidence)

### 1.1 `uuuSanAI_GameMaker` (product side)

**Layer map (actual `src/` layout, not docs):**

| Layer | Path | Key files |
|---|---|---|
| Entry | `src/index.ts` | `Main` logger, phase orchestration, SIGTERM handler [observed: src/index.ts:1-46] |
| Director | `src/director/` | `director.ts` (Director class, 633 lines), `workflow.ts` (WorkflowManager, 5 phases), `scheduler.ts` (topological TaskScheduler), `task-manifest.ts` (TaskManifestStore) [observed] |
| Creative Director | `src/creative-director/` | `auto-director.ts`, `human-director.ts`, `interactive-director.ts`, `types.ts` — 3 modes confirmed [observed: src/director/director.ts:8-9, 494] |
| Router | `src/router/` | `routed-llm-client.ts`, `provider-intelligence.ts`, `provider-router.ts`, `quality-signals.ts`, `review-prompts.ts`, `routing-log.ts`, `usage-tracker.ts`, `index.ts` — **8 files** [observed: src/router/index.ts:1-10] |
| Departments | `src/departments/` | 8 dept dirs: `design/`, `narrative/`, `programming/`, `art/`, `sound/`, `level_assembly/`, `qa/`, `deploy/` — each with `index.ts`, `tasks.ts`, `evaluator.ts`, `tools.ts` [observed] |
| Executor | `src/executor/` | `executor/index.ts`, `manifest.ts`, `sub-step-runner.ts`, `strategies/` (design, qa, level-assembly), `gameplay-systems.ts`, `prompts/cpp-codegen.ts` [observed] |
| Unreal Export | `src/unreal-export/` | `exporter.ts`, `project-scaffold.ts`, `cpp-generator.ts`, `artifact-mapper.ts`, `behavior-tree.ts`, `save-system.ts`, `datatable-csv.ts`, `animation.ts`, `asset-layout.ts`, `feedback.ts`, `packaging.ts`, `ue-build.ts`, `templates/` [observed] |
| Asset Pipeline | `src/asset-pipeline/` | `index.ts`, `manifest.ts`, `generators/{stability,suno,meshy}.ts` [observed] |
| Bridge I/O | `src/bridge/` | `reader.ts`, `writer.ts`, `sync.ts`, `result-writer.ts` [observed] |
| Plugin | `src/plugin/` | `registry.ts`, `loader.ts`, `mcp-loader.ts` [observed] |
| Infrastructure | `src/infrastructure/` | `knowledge-base.ts`, `glossary.ts`, `consistency-checker.ts` (+ `artifact-store.ts` imported by Director) [observed: src/director/director.ts:22] |
| Metric / Agent / Util / Types | `src/metric/`, `src/agent/`, `src/util/`, `src/types/` | present; Agent Runtime implemented (imported as `createAgentRuntime, AgentRuntimeImpl`) [observed: src/director/director.ts:7] |

**Core interface — Director runPhase** [observed: src/director/director.ts:184-398]:
- Loads previous-phase gate result, rejects if previous gate failed unless `options.force`
- Collects tasks from enabled departments for phase
- `TaskScheduler.schedule` → topological batches
- `TaskManifestStore` deduplicates already-succeeded tasks (incremental execution)
- CLI backend runs with concurrency 1 (MAX subscription); API with concurrency 3 [observed: director.ts:278]
- Interactive mode supports up to 3 re-runs with injected user feedback [observed: director.ts:495-544]
- Per-task `TaskUsabilityRecord` (rerun_count, feedback_injected, accepted) emitted to `MetricCollector.collectWithUsability`
- `handleGate` fails fast at >30% task failure rate [observed: director.ts:412], otherwise delegates to `CreativeDirector.decide({type:'gate'})`
- Optional `Executor.materializePhase` call writes C++/UE files [observed: director.ts:348-375]

**Router — exposed surface** [observed: src/router/index.ts:1-10]: `UsageTracker`, `ProviderRouter`, `wildcardMatch`, `appendRoutingDecision`, `readRoutingLog`, `RoutedLlmClient`, `ProviderIntelligence`, `buildQualitySignals`, `buildReviewPrompt`, `buildRevisionPrompt`. Matches Engine's router exports.

**Stale doc note — CORRECTED FROM V1**: `docs/00_system_overview.md:86-89` still lists "Director / Shared Infrastructure / Human Interface / Engine Adapter" as "⬜ 미착수". This is documentation drift; the code is present. v1 replicated the stale claim.

### 1.2 `uuuSanAI_GameMakerEngine` (R&D side)

**Layer map:**

| Layer | Path | Evidence |
|---|---|---|
| Orchestrator | `src/orchestrator/orchestrator.ts` | Wires Monitor, Arena, Evolver, AgentRegistry, BridgeReader/Writer, ActionRegistry, SeasonManager, McpClient. Builds `cyclesDir = {state_path}/orchestrator/cycles` [observed: orchestrator.ts:30-50] |
| Orchestrator adjunct | `orchestrator/runner.ts`, `progress.ts`, `gamemaker-runner.ts` | runGameMaker subprocess interface [observed: orchestrator.ts:7] |
| Arena | `src/arena/` | `arena.ts`, `quick-judge.ts`, `deep-judge.ts`, `detection-judge.ts`, `playtest-scorer.ts`, `static-analyzer.ts`, `trial-catalog.ts`, `trial-executor.ts`, `judge-personas.ts`, `human-gate.ts`, `approval-history.ts`, `build-play-judge.ts` [observed] |
| Evolver | `src/evolver/` | `evolver.ts`, `feedback-mutator.ts`, `sub-step-mutator.ts` [observed] |
| Planner | `src/planner/` | `planner.ts`, `scanner.ts`, `scoring.ts` + 11 rule files in `rules/` (asset-generators, fallback-outputs, game-asset-completeness, missing-systems, pipeline-execution-status, strategy-coverage, stub-tools, ue-project-integrity, unreal-modules, usability-metrics, engine-execution-status) [observed] |
| Monitor | `src/monitor/monitor.ts` | singleton [observed] |
| Router | `src/router/` | Same 8 + `codex-advisor.ts` (= GameMaker router + codex advisor) [observed] |
| Season | `src/season/` | `game-director.ts`, `season-manager.ts` [observed] |
| Advisor | `src/advisor/` | `goal-advisor.ts`, `state-collector.ts`, `gm-capability-advisor.ts` [observed] |
| Action Registry | `src/action-registry/` | `registry.ts`, `builtin-actions.ts`, `mcp-actions.ts`, `executor.ts`, `validator.ts` [observed] |
| Services | `src/services/service-registry.ts` | DI / provider swap-in (used by orchestrator) [observed] |
| Helper Integration | `src/util/helper-collaboration.ts`, `src/followup/focus-resolver.ts`, `src/ask/engine-request.ts` | bridge into Helper collab layer [observed] |
| Registry | `src/registry/registry.ts` | candidate → active → published → deployed → archived [observed + engine CLAUDE.md:30] |

**Role boundary (hard rule)** [observed: Engine/CLAUDE.md:15-19]: Engine owns Arena/Evolver/Monitor/Registry/Planner/Playtest Scorer. Engine explicitly does NOT own MCP deployment, widget gen, C++ codegen, Build.cs, DataTable CSV, game-loop code. Those belong to GameMaker. Claude never builds them directly.

### 1.3 `uuuSanAI_GameMakerCollabMonitor_Codex` (Monitor layer)

**Scripts** [observed]: `monitor_cycle.py`, `monitor_preflight.py`, `monitor_launch_status.py`, `build_engine_request.py`, `build_execution_packet.py`, `build_next_work_decision.py`, `engine_ask_contract.py`, `execution_strategy.py`, `set_startup_model_profile.py` + PowerShell `trigger_collab_action.ps1`, `execute_monitor_decision.ps1`.

**Action surface** [observed: scripts/trigger_collab_action.ps1:2]:
`assess, preflight, launch-status, observe-engine, engine-self-progress, engine-helper-followup, helper-review, helper-self-progress, run-engine, run-helper, run-session, launch-observe-engine, launch-engine-self-progress, launch-engine-helper-followup, launch-gamemaker-run, ask-engine-advise, ask-engine-gm-advise, ask-engine-gm-guide, ask-engine-plan, ask-engine-custom`

**Owner classification rule — CORRECTED FROM V1** [observed: scripts/monitor_cycle.py:226-241]:
```
engine_tasks = [task for task in tasks if task.get("target_agent_role") == "engine"]
helper_tasks = [task for task in tasks if task.get("target_agent_role") == "helper"]
```
Only two owner classes: `engine`, `helper`. `gamemaker` is **not** a 1st-class execution owner. v1 implied a three-way routing.

**State directory** [observed]: 18 files under `state/` including: `monitor_brief.md`, `state_digest.md`, `operator_report.md`, `next_work_brief.md`, `north_star.md`, `operator_memory.md`, `launch_status.md`, plus 8 `*_handoff.md` task-scoped files (engine_path_cleanup, engine_zero_task_materialization, engine_build_health, engine_deprecated_image_provider, helper_artifact_triage, helper_subagent_review, helper_path_cleanup, operator-active-gamemaker-improvements), context-compression snapshots, and `report_gamemaker_improvements_rebuttal.md`.

**CLAUDE.md rules of note** [observed: CollabMonitor_Codex/CLAUDE.md]:
- Line 20: `when the requested implementation target is uuuSanAI_GameMaker, route that work to engine as the execution owner by default; do not create or imply a separate GameMaker execution owner`
- Line 37: `when the desired code change lives in uuuSanAI_GameMaker, prefer an Engine-owned bounded task that names the GameMaker files`
- Line 26: `NON-BLOCKING`=pause/helper-review/helper-self-progress/ask-engine-*/task preparation; `DELEGATED-OR-CONSENT`=engine-self-progress/engine-helper-followup/run-*/launch-*; `HARD-GATE`=human-review
- Line 32: rule-persistence discipline (no memory-only promises)
- Line 45-47: >60s preflight written decision; never skippable
- Line 51-54: path-cleanup requests must NOT satisfy via followup/make/cycle/production runs

### 1.4 `uuuSanAI_GameMakerEngineHelper_Codex` (Helper layer)

**Scripts** [observed]: `helper_cycle.py`, `helper_self_progress.py`, `helper_ask.py`, `monitor_collab.py`, `collab_runtime.py`, `analyze_projects.py`, `artifact_triage.py`.

**Role contract** [observed: docs/collaboration_protocol.md:163-186]:
- Engine = Primary autonomous executor — responsible for "modify Engine and GameMaker code"
- Helper = External supervisor / reviewer / strategist / optional intervener
- This confirms Engine as the code-owner for GameMaker edits, independent of Monitor's routing rule

**Collab directory spec** [observed: collaboration_protocol.md:33-53]:
`collab/{protocol,events,queues/{open,claimed,done,blocked},state,decisions,sessions/{active,expired}}`

**Cooldown** [observed: docs/automatic_collaboration_loop.md:223]: `review_mode: steady-state` + no new Engine follow-up emission when no durable evidence change detected.

### 1.5 `bridge/` + `uuuSanAI_bridge-types/`

**`bridge/`** [observed: Glob]: pure file repo, no scripts. Contains `agents/S001-v{023,024,011,012,016,019}/` directories each with `agent.json` + `meta.json`, plus `metrics/YYYY-MM-DD_NNN.json` (lots of 2026-03-29 entries), `CLAUDE.md` (brief — Git-backed private repo). Manifest-based coordination. v1's description of atomic-write manifest remains correct.

**`uuuSanAI_bridge-types/`** [observed: src/index.ts:1-60]: shared TypeScript types package (`@uuusan/bridge-types`). Exports `AgentVersion`, `MetricId`, `BridgeDepartment`, `SchemaVersioned`, `BridgeManifest` (deployed_agent, latest_agent, candidates, last_metric_id, updated_at), `UsabilityTelemetry` (rerun_count, feedback_injected, gate_rejected, time_to_decision_ms, acceptance_rate, modification_depth), `MetricRecord`, `AgentPackage`, `AgentMeta`.

---

## 2. Current live state (2026-04-14 snapshot)

From `CollabMonitor_Codex/state/monitor_brief.md` [observed, all lines cited]:

- `generated_at: 2026-04-14T14:05:44Z` (line 2)
- `engine_snapshot_age_minutes: 2117.0` (line 3) — ~35 hours stale
- `helper_snapshot_age_minutes: 2211.5` (line 4) — ~37 hours stale
- `helper_review_mode: fresh` (line 5) — but `helper_efficacy: low` (line 6)
- `open_engine_tasks: 4`, `open_helper_tasks: 0` (lines 10-11)
- Decision: `helper-review` (high confidence, source = monitor-rules) — because engine snapshot is newer than helper review

**Open engine tasks** [observed: monitor_brief.md:56-59]:
1. Normalize Engine and GameMaker moved paths after Bundle_GameMaker migration
2. Restore clean Engine build and typecheck health
3. Roll out repo-local delegation guardrails in Engine and GameMaker where still missing
4. Engine self-progress should consume active milestone directly

**Next Work Brief** [observed: next_work_brief.md:2-22]:
- recommended_owner: `engine`
- recommended_action_family: `engine-helper-followup`
- recommended_task_title: **Restore clean Engine build and typecheck health** (high priority, 60min timebox)
- Alternative #1 (score 95): `engine-self-progress` — explicit note "Keep routing GameMaker code changes through Engine, and only add a separate GameMaker owner after explicit monitor/helper/Engine protocol changes"

**Engine Ask output** [observed: monitor_brief.md:46-53]:
- `canonical_recommended_action: engine-self-progress`, confidence `high`
- Summary: "The better-supported current protocol is to route uuuSanAI_GameMaker code changes as Engine-owned work; there is no separate GameMaker execution owner surfaced in the live Engine workflow today."

**Zero-task blocker details** [observed: state/engine_zero_task_materialization_handoff.md:16-29]:
- `followup-once` run on 2026-04-13 returned `Success: true` but `Phase production completed: 0 tasks, 0 artifacts` with `31 tasks skipped (already succeeded)`
- Pipeline diagnosis: `Overall: 69%`, `Playable: NO`, `Genre coverage: 29%`
- Missing UI surfaces: `WBP_CardWidget`, `WBP_HandDisplay`, `WBP_CombatScreen`, `EnemyTable`, `BalanceTable`
- Active milestone: `Implement CardSystem BP draw, hand, energy, and card activation flow`
- DALL-E 3 deprecated warning now non-terminal (downgraded from blocker → warning)

---

## 3. Workflow (corrected)

Normal cycle, reconstructed from live state + scripts:

1. **Monitor assesses** → reads `state/monitor_brief.md` + `state/monitor_snapshot.json` [observed: CLAUDE.md:17]
2. **Classify session** → `first-run` / `active-extend` / `steady-state`; default to `pause` under `steady-state` without new durable evidence [observed: CLAUDE.md:18]
3. **Validate external insights** → before converting any outside claim into a durable task, verify against live repo/open tasks/snapshots [observed: CLAUDE.md:19] — this rule was added precisely to avoid the failure mode v1 participated in
4. **Route GameMaker work to engine owner** [observed: CLAUDE.md:20,37]
5. **Decide action family**: `pause` / `engine-self-progress` / `engine-helper-followup` / `helper-review` / `human-review` with blocking classification [observed: CLAUDE.md:22-28]
6. **Preflight gate for any >60s command** [observed: CLAUDE.md:47]
7. **Dispatch via sub-agent pair** (runner+watcher 1:1) [observed: state_digest.md:37-56]
8. **Engine executes bounded cycle** via `npm run engine:cycle` or `StartEngineSession.bat` [observed: Engine/CLAUDE.md:41-45, 144-146]
9. **Helper reviews** via `helper_cycle.py` when Engine snapshot is newer than helper review; Helper cools to steady-state if no fresh change [observed: automatic_collaboration_loop.md:220-228]
10. **Metrics flow** GameMaker → `bridge/metrics/` → Engine reads on next cycle [observed: bridge structure]

**Active focus task (today)**: `Restore clean Engine build and typecheck health` + `Unblock followup-once zero-task materialization` (both engine-owned). Path normalization task is still open but no longer the lead recommendation.

---

## 4. Primitives ground-truth inventory

These are harness-engineering primitives **confirmed to exist in live code or config**, regardless of what docs say:

| ID | Primitive | Evidence |
|---|---|---|
| P1 | File-based async handoff (Bridge) | bridge/agents/, bridge/metrics/, bridge/CLAUDE.md, uuuSanAI_bridge-types/src/index.ts |
| P2 | Structured state directory | CollabMonitor_Codex/state/ (18 files w/ role-typed names) |
| P3 | Manager-Worker (3-step delegation) | Engine/CLAUDE.md:81-97; GameMaker/CLAUDE.md:43-62 |
| P4 | Runner-Watcher 1:1 topology | state/state_digest.md:37-56 |
| P5 | Bounded cycles w/ explicit count consent | Engine/CLAUDE.md:79 |
| P6 | Preflight written decision gate (>60s rule) | CollabMonitor_Codex/CLAUDE.md:47 |
| P7 | Provider Router w/ cross-review | Engine/src/router/*.ts (9 files incl codex-advisor); **GameMaker/src/router/*.ts (8 files) — corrected** |
| P8 | Competitive Arena + Evolver | Engine/src/arena/*, Engine/src/evolver/*, 6 mutation strategies |
| P9 | Helper cooldown → steady-state | automatic_collaboration_loop.md:223 |
| P10 | Rule-persistence discipline | CollabMonitor_Codex/CLAUDE.md:32-34 |
| P11 | Advisor cross-project loop (`advise`/`gm-advise`) | GameMaker/CLAUDE.md:29-33; Engine/src/advisor/* |
| P12 | **Director with topological scheduler + task manifest** (NEW post-rebuttal) | GameMaker/src/director/{director,scheduler,task-manifest,workflow}.ts |
| P13 | **Creative Director 3-mode decision interface** (confirmed) | GameMaker/src/creative-director/{auto,human,interactive,types}.ts, used in director.ts:494,525 |
| P14 | **Incremental execution via TaskManifestStore** (NEW post-rebuttal) | director.ts:243-270 — succeeded task keys skipped on re-run |
| P15 | **Gate failure-rate threshold (30%)** | director.ts:412-420 |
| P16 | **Action Registry + MCP action binding** | Engine/src/action-registry/*, registry.ts, mcp-actions.ts |
| P17 | **Owner-class routing (engine/helper only)** | monitor_cycle.py:226-241 |
| P18 | **Engine Ask contract (canonical action families)** | monitor_cycle.py:11 (CANONICAL_ACTION_FAMILIES), engine_ask_contract.py |

---

## 5. Pain points & open blockers (live-verified)

1. **Engine snapshot staleness > 35h** — `engine_snapshot_age_minutes: 2117` [observed: monitor_brief.md:3]. The cycle has been paused significantly longer than at v1 time. [observed]

2. **Engine build/typecheck health is broken** — top-of-brief task [observed: monitor_brief.md:57, next_work_brief.md:4]. Until this is cleared, no autonomous progress path.

3. **`followup-once` zero-task materialization bug** — Success:true but 0 tasks / 0 artifacts / 31 skipped; misses CardSystem/WBP_*/EnemyTable/BalanceTable [observed: engine_zero_task_materialization_handoff.md:17-29]. Root cause in incremental-execution cache or task-selection rules.

4. **Path migration incomplete** — Engine-owned references still point at pre-Bundle absolute paths [observed: engine_path_cleanup_handoff.md:6-25]. Listed as explicitly maintenance-only; must NOT be satisfied via followup/make/cycle runs.

5. **Helper efficacy low** — `helper_efficacy: low` [observed: monitor_brief.md:6]. Same gaps repeat across cycles.

6. **Delegation-guardrail rollout incomplete** — open engine task: "Roll out repo-local delegation guardrails in Engine and GameMaker where still missing" [observed: monitor_brief.md:58]

7. **`uuuSanAI_GameMaker/docs/00_system_overview.md` status table is stale** — lists Director/Shared Infra/Human Interface/Engine Adapter as 미착수 [observed: docs/00_system_overview.md:86-89] but code contradicts. Documentation drift itself is a pain point: downstream consumers (including v1 of this map) were misled.

8. **Active milestone unreached** — `The Last Rite playable Unreal combat loop` still `Playable: NO`, 69% overall, 29% genre coverage [observed: engine_zero_task_materialization_handoff.md:27-29]

9. **DALL-E 3 deprecated warning still surfacing** — downgraded to non-terminal warning, but noise stays in every run [observed: engine_zero_task_materialization_handoff.md:24]

10. **MCP permission gating** (carried from v1, not re-verified in this pass — v1 cited Engine CHANGELOG)

---

## 6. Axis Inventory (using synthesis_tier1.md schema)

| Axis | Status | Notes (corrected where needed) |
|---|---|---|
| **1. Identity & provenance** | YES | 5 sub-projects (GameMaker, GameMakerEngine, CollabMonitor_Codex, EngineHelper_Codex, bridge + bridge-types). TypeScript + Python (Monitor/Helper) + PowerShell. |
| **2. Problem framing** | YES | Product: UE5 game from 7 depts. Meta: Arena+Evolver improves the product. North star = playable Last Rite combat loop. [observed: state_digest.md:14-16] |
| **3. Control architecture** | YES | Graph pipeline: Monitor (LLM-directed) → Engine cycle (code-directed w/ LLM sub-calls) → Bridge → GameMaker Director (code-directed w/ Creative Director LLM gates). |
| **4. State & context model** | YES | File-based throughout. `bridge/` shared repo, `CollabMonitor_Codex/state/` (18 files), `collab/` event log + queues, `state/orchestrator/cycles/*.json`, GameMaker `state_path` for workflow+task manifest persistence. |
| **5. Prompt strategy** | PARTIAL | Per-sub-project CLAUDE.md + AGENTS.md mirror rule. Codex delegation is prose-documented. No SKILL.md convention. Producer brief → per-dept design brief injection [observed: director.ts:152-162]. |
| **6. Tool surface & permission model** | YES | Claude CLI (MAX sub default), Anthropic API, Codex CLI, PowerShell launchers, MCP (Unreal Editor — permission gating noted). Provider Router routes per-task. [observed: Engine/CLAUDE.md:46-55] |
| **7. Human-in-the-loop points** | YES | Preflight >60s written gate; explicit cycle-count consent; `human-review` as HARD-GATE; operator approval for blocking actions; "continue/proceed" explicitly forbidden as blocking-consent [observed: CLAUDE.md:46]. |
| **8. Composability** | YES | Bridge schema-versioned exchange; Monitor+Helper stackable; GameMaker runnable standalone; Router swappable (Claude/Codex presets under `config/routing-presets/`). |
| **9. Empirical claims** | N/A | Internal project, no external benchmark. |
| **10. Failure modes** | YES | Explicit anti-patterns in CLAUDE.md (vitest re-run, background polling, memory-only promises, vague consent, path-cleanup via runtime surface). Concrete active failures: zero-task no-op, snapshot staleness, typecheck break. |
| **11. Transferable primitives** | YES | 18 primitives enumerated §4 above. |
| **12. Open questions** | YES | 10 pain points §5 above. |
| **A. Iteration-boundary semantics** | YES | Multiple boundaries: Engine cycle (Arena→Evolver→Bridge publish + cycles/*.json), GameMaker phase (WorkflowManager persistence + TaskManifestStore incremental keys), Monitor cycle (monitor_brief regen + last_action_family). Director phase-completion commits `gate_result` to workflow state [observed: director.ts:393]. |
| **B. Backpressure** | PARTIAL | `pause` default under low utility; Helper cooldown (steady-state); 60s preflight as temporal backpressure. No N-reader:1-writer model. |
| **C. Mode splitting** | YES | Creative Director 3 modes (auto/persona/human+interactive); GameMaker 5 phases; Engine 3 run modes; Monitor 6+ action families; session classification (first-run/active-extend/steady-state). |
| **D. Gate mechanism syntax** | YES | Typed blocking classification NON-BLOCKING / DELEGATED-OR-CONSENT / HARD-GATE [observed: CLAUDE.md:26-28]; numeric 30% failure-rate gate [observed: director.ts:412]; preflight prose gate; `pause` enum default. Mixed styles. |
| **E. Authoritative process medium** | PARTIAL | Markdown CLAUDE.md + AGENTS.md + `docs/NN_*.md` prose + JSON state. No DOT/Gherkin. `engine_ask_contract.py` + `CANONICAL_ACTION_FAMILIES` is the only structured-vocabulary layer. |
| **F. Skill as unit of discipline** | NO | No SKILL.md. Codex delegation is prose rule, not structured skill file. Recurring behavioral traps cited in CLAUDE.md are precisely what structured skills could enforce. |
| **G. Execution environment as constraint** | PARTIAL | Provider Router routes per-task; MCP permission surface; worktree isolation; `preferred_execution_surface: subagent-owned-bounded-run` published into state [observed: monitor_brief.md:16]. |
| **H. Artifact naming schema as protocol** | PARTIAL | `*_handoff.md` per task lifecycle (8 live files), `agents/v{NNN}/` version dirs, `metrics/YYYY-MM-DD_NNN.json` date-ordered, `context_compression_YYYY-MM-DD.md`. Not as strict as GSD's `{PHASE}-{WAVE}-{TYPE}`. |
| **I. Ambiguity-as-numeric-gate** | NO | 30% failure-rate gate is the only numeric gate found — it's a failure-proportion gate, not an ambiguity gate. |
| **J. Deferred-tool loading** | NO | Not observed. |
| **K. Role perspective as constraint** | PARTIAL | 8 named departments (design/narrative/programming/art/sound/level_assembly/qa/deploy) each w/ tasks.ts + evaluator.ts + tools.ts. 2 owner roles (engine/helper) hard-coded in `monitor_cycle.py`. Creative Director 3 modes. Not SKILL.md-backed. |
| **L. Instinct learning as harness layer** | PARTIAL | Arena+Evolver = structural cross-cycle evolution (6 mutation strategies, 9-dim composite, +2.0 champion margin). Session-level `/learn→/evolve` instinct loop absent. Advisor loop (`advise`/`gm-advise`) is a separate guidance surface. |
| **M. Meta-skill bootstrapping** | NO | Not observed. |

---

## 7. Owner routing rules (explicit, for graft-evaluator)

From live Monitor protocol:

```
target_agent_role ∈ {engine, helper}
  (no gamemaker class)          [monitor_cycle.py:226-227]

if code_change.target_repo == uuuSanAI_GameMaker:
    route to: engine (Engine-owned bounded task naming GameMaker files)
                                  [CollabMonitor_Codex/CLAUDE.md:20, 37]
                                  [next_work_brief.md:21 alternative #1]

Helper contract: Engine = "Primary autonomous executor, modify Engine and GameMaker code"
                                  [collaboration_protocol.md:167, 173]

Monitor contract: Monitor does NOT directly edit Engine/Helper/GameMaker code
                  unless human explicitly asks
                                  [CollabMonitor_Codex/CLAUDE.md:34, 38]
```

Consequence: any insertion of a new harness primitive into GameMaker must be framed as an **Engine-owned bounded task whose acceptance criteria name specific GameMaker files**. Grafts that assume "run it in GameMaker directly" will short-circuit the protocol.

---

## 8. Evidence log (every major claim)

| Claim | File : line |
|---|---|
| 8 router files in GameMaker | uuuSanAI_GameMaker/src/router/index.ts:1-10 (re-exports 8 modules) |
| 4 director files in GameMaker | uuuSanAI_GameMaker/src/director/{director,workflow,scheduler,task-manifest}.ts |
| Director class size + phase orchestration | src/director/director.ts:72-633 |
| Incremental execution via TaskManifestStore | src/director/director.ts:243-270 |
| Concurrency = 1 on CLI, 3 on API | src/director/director.ts:278 |
| 30% failure-rate gate | src/director/director.ts:412-420 |
| Interactive 3-rerun loop | src/director/director.ts:495-545 |
| Creative Director 3 modes wired | src/director/director.ts:101-102, 494 |
| Workflow phases = concept/pre_production/production/polish/release | src/director/workflow.ts:12 |
| Executor materialization hook | src/director/director.ts:348-375 |
| Stale status table in docs | uuuSanAI_GameMaker/docs/00_system_overview.md:86-89 |
| Engine role boundary hard rule | uuuSanAI_GameMakerEngine/CLAUDE.md:15-19 |
| Engine manager-worker 3-step rule | uuuSanAI_GameMakerEngine/CLAUDE.md:81-97 |
| Engine Orchestrator wiring | src/orchestrator/orchestrator.ts:29-60 |
| Engine 11 planner rules | src/planner/rules/*.ts (Glob) |
| Engine 6 mutation strategies | uuuSanAI_GameMakerEngine/CLAUDE.md:29 |
| Engine router 9 files incl codex-advisor | uuuSanAI_GameMakerEngine/src/router/*.ts (Glob) |
| Monitor owner-class routing | CollabMonitor_Codex/scripts/monitor_cycle.py:226-241 |
| GameMaker-to-engine routing rule | CollabMonitor_Codex/CLAUDE.md:20, 37 |
| Engine-self-progress alternative preserves rule | state/next_work_brief.md:21 |
| Engine Ask canonical summary | state/monitor_brief.md:46-53 |
| Blocking class taxonomy | CollabMonitor_Codex/CLAUDE.md:26-28 |
| Preflight >60s rule | CollabMonitor_Codex/CLAUDE.md:47 |
| Rule-persistence discipline | CollabMonitor_Codex/CLAUDE.md:32-34 |
| Path-cleanup must-not-launch-runtime rule | CollabMonitor_Codex/CLAUDE.md:51-54 |
| Helper Engine as primary executor | EngineHelper_Codex/docs/collaboration_protocol.md:167-174 |
| Helper steady-state cooldown | EngineHelper_Codex/docs/automatic_collaboration_loop.md:222-224 |
| Helper collab directory layout | collaboration_protocol.md:33-53 |
| Monitor action surface (19 actions) | scripts/trigger_collab_action.ps1:2 |
| State dir (18 files, 8 handoff) | CollabMonitor_Codex/state/ (Glob) |
| Engine snapshot age 2117min | state/monitor_brief.md:3 |
| Helper snapshot age 2211min | state/monitor_brief.md:4 |
| Helper efficacy low | state/monitor_brief.md:6 |
| 4 open engine tasks | state/monitor_brief.md:10, 56-59 |
| Lead task: Restore Engine build health | state/next_work_brief.md:4-6 |
| Zero-task materialization details | state/engine_zero_task_materialization_handoff.md:16-29 |
| Playable: NO, Overall 69% | state/engine_zero_task_materialization_handoff.md:27-28 |
| Missing UI: WBP_*, EnemyTable, BalanceTable | state/engine_zero_task_materialization_handoff.md:29 |
| DALL-E warning downgraded | state/engine_zero_task_materialization_handoff.md:23-24 |
| Path cleanup maintenance-only rule | state/engine_path_cleanup_handoff.md:19 |
| Bridge types (BridgeManifest, MetricRecord, UsabilityTelemetry) | uuuSanAI_bridge-types/src/index.ts:14-57 |
| Bridge git-backed private repo | bridge/CLAUDE.md:5-6 |
| Bridge agents dirs present | bridge/agents/S001-v{011,012,016,019,023,024}/ (Glob) |

---

## 9. Notes for graft-evaluator (minimal — not recommendations)

Things the map makes explicit that downstream evaluation will depend on:

- **GameMaker has a Director and a Router.** Any graft proposing "add a Director" or "add routing" must be framed as an upgrade/replacement of existing code, not a greenfield insertion. Evaluate existing `Director` interface (runPhase/handleGate/executeTask) before proposing alternatives.
- **There is no `gamemaker` owner.** Grafts targeting GameMaker must land as Engine-owned bounded tasks.
- **Docs drift is a known and ongoing risk.** Any graft that cites `uuuSanAI_GameMaker/docs/` as ground truth needs to be double-checked against `src/`.
- **Axis F (SKILL.md) is a real empty-axis.** The recurring behavioral traps (memory-only promises, vague consent, vitest re-run, path-cleanup-via-runtime) are exactly what structured skill files catch. Gap is clear and insertion point is the per-sub-project `CLAUDE.md`s.
- **Axis A is unusually rich here** — three independent iteration-boundary media (Engine cycle records, GameMaker TaskManifestStore, Monitor brief regen). Any primitive graft on axis A should acknowledge this richness rather than treat the project as empty.
- **Axis L is PARTIAL but deep on one side** — Arena+Evolver is a fully-built cross-cycle evolutionary loop. Session-level instinct capture (ECC `/learn→/evolve`, Compound Engineering `docs/solutions/`) is the missing half.
- **Current blocker is operational, not architectural.** Engine build health + zero-task no-op are the real gate. Harness grafts that don't help those are not the highest-leverage move right now.
