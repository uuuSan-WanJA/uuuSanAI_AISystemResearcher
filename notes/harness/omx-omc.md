---
title: oh-my-claudecode (OMC) + oh-my-codex (OMX) — sibling harness bundle
slug: omx-omc
date: 2026-04-19
author: Yeachan Heo (@Yeachan-Heo) + core maintainers (HaD0Yun, Sigrid Jin, devswha, etc.)
first_public:
  OMC: 2026-01-09 (repo creation)
  OMX: 2026-02-02 (repo creation)
primary_sources:
  - https://github.com/Yeachan-Heo/oh-my-claudecode
  - https://github.com/Yeachan-Heo/oh-my-codex
  - https://oh-my-claudecode.dev
  - https://oh-my-codex.dev
topic: harness
tags: [harness, claude-code, codex-cli, agent-teams, hooks, hud, korean-author, plugin, tmux, rust-runtime, consensus-planning]
status: deep-dive + post-omo-correction-pass
confidence: high
rounds: 1 (+ correction pass 2026-04-19 after OMO note landed)
axes_used: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
axes_added: [13-omc-vs-omx-delta, 14-ecosystem-uptake, 15-transferable-primitives-moved-from-11]
axes_dropped: []
candidate_axis_proposals: [substrate_feature_gap_exploitation, consensus_planning_as_gate_to_execution, stage_handoff_as_rpc_protocol]
probe_method: inline bash/curl — Task/Agent tool not available in this sub-agent context; coordinator performed primary-source reads directly via GitHub API and raw content URLs; per user directive, codex:rescue NOT used
revised_after: notes/harness/omo.md (2026-04-19) — see "⚠️ Post-OMO correction pass" block below
---

## TL;DR (3 lines)
OMX and OMC are **sibling multi-agent orchestration layers by Yeachan Heo** that attach to **two different substrates** — OMC is a Claude Code plugin (v4.13.0, 29.9k★) launched 2026-01-09 **as an explicit port of `oh-my-opencode` (now OMO) to Claude Code** (commit `cd98f12fac` titled verbatim "Complete port of oh-my-opencode to Claude Code"), riding Anthropic's experimental `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` flag; OMX (v0.14.0, 24.1k★) ports the same vocabulary to OpenAI Codex CLI with a **Rust runtime** (`omx-runtime-core` with mailbox/dispatch/authority modules) to compensate for Codex's missing team primitive. The shared canonical skill vocabulary is **mixed-origin**: `$team`, `$ralph`, `$ultrawork` are inherited from OMO (code-yeongyu, different author, 2025-12-03 onwards); `$ralplan` (2026-01-22) and `$deep-interview` (2026-03-02, Ouroboros-inspired) are **genuine OMC inventions by Yeachan Heo**, later propagated to OMX. The genuinely novel primitives introduced by OMC/OMX are **(a) the `$ralplan → $team|$ralph` execution-entry gate** (lexical-heuristic rejection of underspecified prompts), **(b) the staged `team-plan → team-prd → team-exec → team-verify → team-fix` pipeline with mandatory `.omc/handoffs/*.md` stage-to-stage RPC documents**, and **(c) the two-layer HUD** (native Codex statusline + OMX `.omx/state/*.json` reader). Most other mechanics are recombinations of patterns from Ralph (Huntley), OMO, Compound Engineering, and Spec Kit.

## ⚠️ Post-OMO correction pass (2026-04-19)

This note was initially drafted before `notes/harness/omo.md` existed. After reading OMO's git history, the following claims in this document are **corrected / qualified**:

1. **Authorship framing**: OMC/OMX are Yeachan Heo's siblings (correct), but the ecosystem around them includes **OMO by `@code-yeongyu` (YeonGyu-Kim / Sionic-AI), a DIFFERENT author**. Earlier language that implied a "single author family" across all three harnesses is wrong. OMC and OMX share one author; OMO is a separate-origin harness in the same ecosystem.
2. **Skill-vocabulary provenance**: `$team`, `$ralph`, `$ultrawork` **originated in OMO** (2025-12-xx). OMC adopted them during its 2026-01-09 "Complete port of oh-my-opencode" launch commit. **`$ralplan` and `$deep-interview` are genuine OMC additions** — they do NOT appear in OMO. OMX inherited all four from OMC.
3. **`$ralph` name lineage**: the name `Ralph` in OMC/OMX arrives **via OMO's Ralph Loop (first commit 2025-12-30, `/ulw-loop → /ralph-loop`)**, not directly from Huntley's original Ralph-Wiggum bash pattern. The *mechanics* (frozen phase enum, state machine, Stop-hook continuation) are genuinely OMC's reinvention, but the *name* was borrowed through OMO.
4. **OpenClaw provenance flows the OTHER way**: The external-notification gateway **originated in OMC (2026-02-25), was ported to OMX (2026-02-26), and adopted by OMO (2026-03-16)** — visible in env-var rename `OMX_OPENCLAW → OMO_OPENCLAW`. This is a rare reverse-direction primitive flow (OMC → OMO) inside an otherwise OMO → OMC ecosystem.
5. **Δ1 ("substrate feature-gap exploitation") scope**: the axis remains valid **specifically for the OMC↔OMX natural experiment** (same author, same vocabulary, two substrates). It does **NOT** generalize to OMO — OMO is single-substrate (OpenCode) with inbound Claude Code compatibility, not a multi-substrate emitter. See `notes/harness/omo.md` Δ1 refutation.

All downstream axes/evidence in this note remain valid; only the provenance framing is adjusted. Cross-references: `notes/harness/omo.md` (full OMO dossier) and `meta/harness_schema.md` (new candidate Δ4 "category-as-skill-orthogonal-selector" introduced by OMO).

## Proposed schema deltas

### Δ1. "Substrate feature-gap exploitation" (new candidate axis)
- **Rationale**: OMX vs OMC is the cleanest natural experiment we have for asking *what a harness author does when the host CLI lacks a needed primitive*. OMC rides `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`; OMX re-implements the team coordination in Rust (`omx-runtime-core/src/{mailbox,dispatch,authority}.rs`) + tmux + mailbox JSON files. Existing axes (3 Control architecture, 8 Composability) don't cleanly capture "what the harness had to reinvent because the substrate didn't provide it."
- **Proposed form**: "If the subject harness exists in multiple-substrate variants, which primitives (a) ride native substrate features, (b) are re-implemented in harness code because the substrate lacks them, and (c) are substrate-exclusive and therefore absent in one port? Does this fork pattern converge or diverge over time?"
- **Promotion threshold**: independent use 2+. Ouroboros's multi-runtime (Claude/Codex/OpenCode) claim is a natural 2nd-case candidate.

### Δ2. "Consensus planning as execution gate" (subtype of candidate D — gate mechanism syntax)
- **Rationale**: OMC/OMX's `$ralplan` — specifically the **Pre-Execution Gate** that intercepts underspecified prompts like `ralph fix this` and redirects them through Planner/Architect/Critic consensus before execution starts — is a distinctive kind of gate: it doesn't gate *progress within execution* (Superpowers `<HARD-GATE>`, Ouroboros numeric thresholds) but **gate entry into execution at all**. Uses a lexical scoring heuristic (file paths, camelCase symbols, issue numbers, test runners ≥ 1 → pass; otherwise redirect to ralplan).
- **Proposed form**: "Does the harness reject underspecified execution requests and redirect to a specification-first subflow? What detection signal triggers the redirect (lexical heuristic / LLM classifier / embedding similarity)? What is the escape hatch (`force:`, `!`, explicit skill invocation)?"
- **Promotion threshold**: 1st observed use (OMX/OMC); track GSD `/gsd-discuss`, Ouroboros interview, Compound Engineering plan. Likely already latently satisfies 2+.

### Δ3. "Stage handoff as RPC protocol" (refinement of candidate A — iteration-boundary semantics)
- **Rationale**: OMC's `.omc/handoffs/<stage-name>.md` pattern (each stage of `team-plan → team-prd → team-exec → team-verify → team-fix` writes a 10-20-line `Decided / Rejected / Risks / Files / Remaining` doc BEFORE transitioning) is a cleaner form of GSD's `{PHASE}-{WAVE}-{TYPE}.md` — it's a structured RPC contract between agent stages that survives context compaction. Different from iteration-boundary (Ralph/GSD) because stages are heterogeneous roles, not homogeneous loop iterations.
- **Proposed form**: "Is the handoff between stages mediated by a structured artifact with a contract (fixed fields / name conventions / storage path) that the next stage reads before spawning its own agents? Does the handoff chain accumulate or rotate? What happens on cancellation?"
- **Promotion threshold**: 1st strong use (OMC). GSD's phase artifacts are 2nd candidate. Likely quick 2+ promotion.

---

## 1. Identity & provenance
- **Creator & Lead**: Yeachan Heo (@Yeachan-Heo, GitHub user id 54757707, Bellman / Layoff-Labs). Korean author. Solo creator pattern with growing maintainer team. **Distinct from @code-yeongyu (YeonGyu-Kim / Sionic-AI)** who created OMO. OMC's launch commit `cd98f12fac` (2026-01-09) is titled "Complete port of oh-my-opencode to Claude Code" — OMC's vocabulary inherits from OMO's, but the two projects are run by two different people in one loosely-coupled ecosystem.
- **OMC maintainers**: Ambassador Sigrid Jin (@sigridjineth), Document Specialist devswha, top collaborators JunghwanNA (65 commits), riftzen-bit (52), Seunggwan Song (20), BLUE (20), Junho Yeo (15).
- **OMX maintainers**: Yeachan Heo (creator), HaD0Yun (maintainer), Sigrid Jin (ambassador), contributors Junho Yeo, JiHongKim98, HyunjunJeon.
- **Repos**:
  - OMC: https://github.com/Yeachan-Heo/oh-my-claudecode — created 2026-01-09 — **29,922★**, TypeScript, MIT, npm package `oh-my-claude-sisyphus`, plugin v4.13.0, 42 MB repo size.
  - OMX: https://github.com/Yeachan-Heo/oh-my-codex — created 2026-02-02 — **24,116★**, TypeScript + Rust, MIT, npm package `oh-my-codex`, v0.14.0, 9.4 MB.
- **Release cadence** (evidence):
  - OMX v0.14.0 shipped **2026-04-19 (today)**. Prior 0.13.2 on 2026-04-18. Velocity: ~4-5 releases/week.
  - OMC last pushed 2026-04-19 09:15 UTC, v4.13.0 current.
  - OMX CHANGELOG shows 20+ versions in ~10 weeks (0.7.x through 0.14.0).
- **Evidence quote (OMX self-position)**: "OMX is a workflow layer for OpenAI Codex CLI. It keeps Codex as the execution engine and makes it easier to: start a stronger Codex session by default, run one consistent workflow from clarification to completion, invoke the canonical skills with `$deep-interview`, `$ralplan`, `$team`, and `$ralph`, keep project guidance, plans, logs, and state in `.omx/`." — OMX README [source](https://github.com/Yeachan-Heo/oh-my-codex/blob/main/README.md)
- **Evidence quote (OMC self-position)**: "Multi-agent orchestration for Claude Code. Zero learning curve. Don't learn Claude Code. Just use OMC." — OMC README [source](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/README.md)
- **Adoption signal**: Both repos among largest in Claude Code / Codex CLI plugin ecosystem. OMC sponsors page active (github.com/sponsors/Yeachan-Heo). Shared Discord server (1452487457085063218) for both communities.

## 2. Architecture / substrate
- **OMC substrate**: Claude Code plugin. Attaches via two paths:
  1. **Marketplace**: `/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode` + `/plugin install oh-my-claudecode`
  2. **npm CLI**: `npm i -g oh-my-claude-sisyphus@latest`
- **OMC file drops**: `.claude-plugin/plugin.json` declares `skills: ./skills/` + mcp servers. `hooks/hooks.json` registers 5 hook events (`UserPromptSubmit`, `SessionStart`, `PreToolUse`, `PermissionRequest`, `PostToolUse`) — each pointing at Node.js scripts under `$CLAUDE_PLUGIN_ROOT/scripts/*.mjs`.
- **OMC project state**: `.omc/` directory — `state/`, `plans/`, `interviews/`, `handoffs/`, `sessions/`, `artifacts/`, `skills/` (user skill extraction), `context/` snapshots.
- **OMX substrate**: OpenAI Codex CLI workflow layer. Attaches via:
  1. **npm package**: `npm install -g @openai/codex oh-my-codex`
  2. `omx setup` installs prompts, skills, AGENTS scaffolding, `.codex/config.toml` (`[features].codex_hooks = true`), and wrapper entries in `.codex/hooks.json`.
- **OMX file drops & ownership boundary** (primary-source contract):
  > "**Native Codex hooks**: `.codex/hooks.json` / **OMX plugin hooks**: `.omx/hooks/*.mjs` / **tmux/runtime fallbacks**: `omx tmux-hook`, notify-hook, derived watcher, idle/session-end reporters. OMX only owns the wrapper entries that invoke `dist/scripts/codex-native-hook.js`. User-managed hook entries in the same `.codex/hooks.json` file are preserved across `omx setup` refreshes and `omx uninstall`." — docs/codex-native-hooks.md [source](https://github.com/Yeachan-Heo/oh-my-codex/blob/main/docs/codex-native-hooks.md)
- **OMX project state**: `.omx/` — `state/`, `plans/prd-*.md`, `interviews/{slug}-{timestamp}.md`, `specs/deep-interview-*.md`, `context/{slug}-*.md`, `logs/hooks-*.jsonl`, `wiki/`.
- **Hybrid runtime (OMX only)**: TypeScript CLI + **Rust crates** (`crates/omx-runtime-core`, `crates/omx-runtime`, `crates/omx-mux`, `crates/omx-sparkshell`, `crates/omx-explore`). The Rust runtime provides the authoritative team coordination primitives. Key modules:
  - `crates/omx-runtime-core/src/mailbox.rs` — `MailboxRecord { message_id, from_worker, to_worker, body, created_at, notified_at?, delivered_at? }` with a 3-state lifecycle (created → notified → delivered) and `MailboxError::{NotFound, AlreadyDelivered}`.
  - `crates/omx-runtime-core/src/dispatch.rs` — dispatch request state machine.
  - `crates/omx-runtime-core/src/authority.rs` — runtime authority separation (who owns which state transitions).
  - `crates/omx-runtime-core/src/replay.rs` — replay infrastructure.
- **Why the substrate split matters**: OMC can ride Claude Code's `TeamCreate` / `TaskCreate` / `Task(team_name=...)` / `SendMessage` / `TeamDelete` native team tools (gated by `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). Codex has no equivalent today. OMX had to write the mailbox, dispatch queue, and leader-head containment logic from scratch in Rust.

## 3. Core loop / keywords / skills

### 3a. Canonical skill surface (shared)
Both harnesses expose the same 4 "canonical skills" as the onboarding lexicon:

| Skill | OMX form | OMC form | Purpose |
|---|---|---|---|
| `deep-interview` | `$deep-interview "..."` | `/deep-interview "..."` | Socratic clarification with numeric ambiguity gating before any execution |
| `ralplan` | `$ralplan "..."` | `/ralplan "..."` | Consensus planning (Planner → Architect → Critic) alias for `plan --consensus` |
| `ralph` | `$ralph "..."` | `/ralph "..."` | Persistence loop until task complete + architect-verified + deslopped + regression-green |
| `team` | `$team N:role "..."` | `/team N:role "..."` | N coordinated worker agents on a shared task list |

**Evidence (OMX)**: "invoke the canonical skills with `$deep-interview`, `$ralplan`, `$team`, and `$ralph`" — OMX README.

**Evidence (OMC)**: "Magic keywords - `ralph`, `ulw`, `ralplan`; Team stays explicit via `/team`" — OMC README.

### 3b. OMX full skill catalogue
From `skills/*/SKILL.md` listing: `ai-slop-cleaner`, `analyze`, `ask-claude`, `ask-gemini`, `autopilot`, `autoresearch`, `build-fix`, `cancel`, `code-review`, `configure-notifications`, `deep-interview`, `deepsearch`, `doctor`, `ecomode`, `frontend-ui-ux`, `git-master`, `help`, `hud`, `note`, `omx-setup`, `pipeline`, `plan`, `ralph-init`, `ralph`, `ralplan`, `review`, `security-review`, `skill`, `swarm` (legacy), `tdd`, `team`, `trace`, `ultraqa`, `ultrawork`, `visual-verdict`, `web-clone`, `wiki`, `worker`.

### 3c. OMC full skill catalogue
From `skills/` directory: `ai-slop-cleaner`, `ask`, `autopilot`, `autoresearch`, `cancel`, `ccg`, `configure-notifications`, `debug`, `deep-dive`, `deep-interview`, `deepinit`, `external-context`, `hud`, `learner`, `mcp-setup`, `omc-doctor`, `omc-reference`, `omc-setup`, `omc-teams`, `plan`, `project-session-manager`, `ralph`, `ralplan`, `release`, `remember`, `sciomc`, `self-improve`, `setup`, `skill`, `skillify`, `team`, `trace`, `ultraqa`, `ultrawork`, `verify`, `visual-verdict`, `wiki`, `writer-memory`.

### 3d. OMC agent roster (19 specialized agents)
`analyst`, `architect`, `code-reviewer`, `code-simplifier`, `critic`, `debugger`, `designer`, `document-specialist`, `executor`, `explore`, `git-master`, `planner`, `qa-tester`, `scientist`, `security-reviewer`, `test-engineer`, `tracer`, `verifier`, `writer` — each with stage-aware tier routing (Haiku/Sonnet/Opus).

### 3e. `$ralph` — semantics
Ralph in OMC/OMX is **NOT Geoffrey Huntley's bare `while true; do cat PROMPT.md | claude ; done`** — it's a structured persistence loop wrapped around multiple guarantees. Evidence from OMX skills/ralph/SKILL.md:

> "Ralph is a persistence loop that keeps working on a task until it is fully complete and architect-verified. It wraps ultrawork's parallel execution with session persistence, automatic retry on failure, and mandatory verification before completion."

Termination condition (OMX):
- Step 6: All pending/in_progress TODO items zero + fresh verification evidence (test/build/lint output read)
- Step 7: Architect verification at STANDARD tier minimum (tiered to THOROUGH for >20 files or security changes)
- Step 7.5: Mandatory `ai-slop-cleaner` deslop pass on changed files (unless `--no-deslop`)
- Step 7.6: Post-deslop regression re-verification must pass
- Step 8: `/cancel` clean state exit

OMC's ralph additionally supports `--critic=architect|critic|codex` reviewer selection and is **PRD-driven by default** — auto-generates `prd.json` scaffold, forces user to refine story acceptance criteria, then iterates story-by-story.

**Delta from Huntley's Ralph**: OMX/OMC's ralph is **not a shell loop** — it's a native skill that runs inside one session, delegating to sub-agents in parallel. The "persistence" property is implemented via:
1. State file at `.omx/state/{scope}/ralph-state.json` with frozen schema (`active`, `iteration`, `max_iterations`, `current_phase ∈ {starting,executing,verifying,fixing,complete,failed,cancelled}`, `started_at`, ownership metadata, tmux anchor fields)
2. Native Codex `Stop` hook continuation contract: "The boulder never stops" message triggers next iteration until terminal phase (evidence in `docs/codex-native-hooks.md`)
3. Visual task gate via `$visual-verdict` when screenshots present (score ≥90 required)

**Evidence (name kept, mechanism rebuilt)**:
> "Ralph runtime state is stored at `.omx/state/{scope}/ralph-state.json` and MUST use this schema... `current_phase` for Ralph MUST be one of: starting, executing, verifying, fixing, complete, failed, cancelled. Unknown phase values MUST be rejected." — docs/contracts/ralph-state-contract.md

### 3f. `$ralplan` — semantics
Full name: "**Ralplan**" = `ralph` + `plan`. Alias for `$plan --consensus` with a 5-agent deliberation protocol + a gating layer. Primary-source mechanics:

1. **Planner** writes initial plan + RALPLAN-DR summary (Principles 3-5, Decision Drivers top 3, Viable Options ≥2 with pros/cons; deliberate mode adds pre-mortem 3 scenarios + expanded test plan)
2. **Architect** review — "must provide the strongest steelman antithesis, at least one real tradeoff tension, and (when possible) synthesis — await completion before step 4" (MUST run sequentially, not parallel with Critic)
3. **Critic** evaluates for principle-option consistency, testable acceptance criteria; deliberate mode rejects missing/weak pre-mortem
4. **Re-review loop** bounded at 5 iterations; any non-APPROVE verdict triggers full closed loop (Architect+Critic→Planner revise→Architect→Critic)
5. **Final plan MUST include ADR** (Decision, Drivers, Alternatives considered, Why chosen, Consequences, Follow-ups)
6. **On approval**: `--interactive` mode presents user choice (Approve via ralph / Approve via team / Request changes / Reject); non-interactive mode outputs plan and stops

**Pre-Execution Gate** (the novel bit):
Bare prompts like `ralph fix this` or `team improve performance` get intercepted. Detection signals (OR logic — any one passes the gate):
- File path, issue/PR number, camelCase/PascalCase/snake_case symbol, test runner reference, numbered steps, acceptance criteria, error reference, code block, or escape prefix (`force:` / `!`).
- Otherwise: <=15 effective words triggers redirect to `$ralplan`.

**Evidence**:
> "The ralplan-first gate intercepts underspecified execution requests and redirects them through the ralplan consensus planning workflow. This ensures: Explicit scope, Test specification, Consensus, No wasted execution — agents start with a clear, bounded task." — skills/ralplan/SKILL.md

OMC's ralplan additionally supports `--architect codex` / `--critic codex` — the Architect or Critic pass can be delegated to Codex CLI as an independent model opinion.

### 3g. `$deep-interview` — semantics
Socratic clarification with **quantitative ambiguity gating**. Primary-source mechanics:

- **Depth profiles**: `--quick` (threshold ≤0.30, max 5 rounds) / `--standard` (≤0.20, 12 rounds, default) / `--deep` (≤0.15, 20 rounds) / `--autoresearch` (specialized for `$autoresearch` mission intake)
- **Greenfield formula**: `ambiguity = 1 - (intent × 0.30 + outcome × 0.25 + scope × 0.20 + constraints × 0.15 + success × 0.10)`
- **Brownfield formula**: `ambiguity = 1 - (intent × 0.25 + outcome × 0.20 + scope × 0.20 + constraints × 0.15 + success × 0.10 + context × 0.10)`
- **One-question-per-round rule**: "Ask ONE question per round (never batch). Target the weakest clarity dimension... Stay on the same thread until one layer deeper, one assumption clearer, or one boundary tighter."
- **Mandatory readiness gates**: `Non-goals` + `Decision Boundaries` must be explicit; a "pressure pass" (revisit an earlier answer with evidence/assumption/tradeoff follow-up) must be complete — even if weighted ambiguity is below threshold.
- **Challenge modes** (one-shot each): Contrarian (round 2+), Simplifier (round 4+), Ontologist (round 5+ when symptom-fixated).
- **Early exit**: allowed at round 4+ but with risk warning; not the default success path.
- **Output**: transcript summary at `.omx/interviews/{slug}-{timestamp}.md` + execution-ready spec at `.omx/specs/deep-interview-{slug}.md`.

**Evidence (quantitative gate)**:
> "Do not hand off to execution while ambiguity remains above threshold unless user explicitly opts to proceed with warning. Do not crystallize or hand off while Non-goals or Decision Boundaries remain unresolved, even if the weighted ambiguity threshold is met." — skills/deep-interview/SKILL.md

This is **the same numeric-threshold-gate pattern** catalogued in axis I (Ambiguity-as-numeric-gate) from Ouroboros — third independent use observed (after Ouroboros and Superpowers verification scores). Promotes axis I toward GA.

### 3h. `$team` — semantics
See Section 4 (it's the load-bearing Agent Teams axis).

### 3i. Supporting modes (shared vocabulary)
- `$autopilot` — full pipeline Phase 0 (expand) → 1 (plan) → 2 (execute) → 3 (QA) → 4 (validation) → 5 (cleanup). Auto-skips Phase 0-1 if a ralplan consensus plan already exists at `.omc/plans/ralplan-*.md`.
- `$ultrawork` / `ulw` — maximum parallelism, non-team (no shared state coordination).
- `$pipeline` — sequential staged processing.
- `$ecomode` — token-efficient mode.
- `$ultraqa` — test/build/lint cycle until green.
- `$cancel` — clean state teardown (`state_clear` across all modes).

## 4. Agent Teams implementation (the load-bearing axis)

### 4a. OMC — rides Claude Code's experimental native team primitive
**OMC's team skill explicitly uses Claude Code's native team tools**. From primary source:

> "Spawn N coordinated agents working on a shared task list using Claude Code's native team tools. Replaces the legacy `/swarm` skill (SQLite-based) with built-in team management, inter-agent messaging, and task dependencies -- no external dependencies required." — skills/team/SKILL.md

The specific native primitives referenced:
- `TeamCreate("fix-ts-errors")` — lead becomes `team-lead@fix-ts-errors`
- `TaskCreate` × N — creates subtasks with dependency graph
- `TaskUpdate` — pre-assign owners (`task #1 owner=worker-1`)
- `Task(team_name="fix-ts-errors", name="worker-1")` — spawns teammates **into the team**
- `SendMessage` — worker→leader and leader→worker (auto-delivered)
- `TaskList` — polling for progress
- `TeamDelete("fix-ts-errors")` + `rm .omc/state/team-state.json` — cleanup

Storage (managed by Claude Code itself, not OMC):
```
~/.claude/
  teams/fix-ts-errors/config.json     # Team metadata + members array
  tasks/fix-ts-errors/
    .lock                              # File lock for concurrent access
    1.json, 2.json, 3.json             # Subtasks
```

**The experimental flag requirement is explicit**:
> "Enable Claude Code native teams in `~/.claude/settings.json`:
> ```json
> { "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
> ```
> If teams are disabled, OMC will warn you and fall back to non-team execution where possible." — OMC README

**Verdict for the global CLAUDE.md catalog decision**: OMC is **direct evidence that a major harness (29.9k★, v4.13.0) treats `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` as its canonical orchestration surface** and actively distinguishes it from sub-agent parallelism. This is a concrete production case of the user's catalog entry being used in the wild, not a toy demo.

### 4b. OMC — staged pipeline on top of native teams
Team is not a single call — it's a **staged pipeline**:

`team-plan → team-prd → team-exec → team-verify → team-fix (loop)`

**Stage routing table** (evidence from skills/team/SKILL.md):

| Stage | Required Agents | Optional Agents | Routing logic |
|-------|-----------------|-----------------|---------------|
| team-plan | `explore` (haiku), `planner` (opus) | `analyst`, `architect` (opus) | analyst for unclear requirements, architect for complex boundaries |
| team-prd | `analyst` (opus) | `critic` (opus) | critic to challenge scope |
| team-exec | `executor` (sonnet) | `executor` (opus), `debugger`, `designer`, `writer`, `test-engineer` | match agent to subtask type |
| team-verify | `verifier` (sonnet) | `test-engineer`, `security-reviewer`, `code-reviewer` (opus) | always run `verifier`; add `security-reviewer` for auth/crypto; add `code-reviewer` (opus) for >20 files or arch changes |
| team-fix | `executor` (sonnet) | `debugger`, `executor` (opus) | debugger for type/build errors; opus executor for complex multi-file fixes |

**Rule**: "The lead picks agents per stage, not the user. The user's `N:agent-type` parameter only overrides the `team-exec` stage worker type."

### 4c. OMC — stage handoff contract (the candidate axis Δ3)
Between every stage, a 10-20-line markdown file is written to `.omc/handoffs/<stage-name>.md`. Primary-source contract:

```markdown
## Handoff: <current-stage> → <next-stage>
- **Decided**: [key decisions made in this stage]
- **Rejected**: [alternatives considered and why]
- **Risks**: [identified risks for the next stage]
- **Files**: [key files created or modified]
- **Remaining**: [items left for the next stage to handle]
```

**Rules**:
> "1. Lead reads previous handoff BEFORE spawning next stage's agents. The handoff content is included in the next stage's agent spawn prompts, ensuring agents start with full context.
> 2. Handoffs accumulate. The verify stage can read all prior handoffs (plan → prd → exec) for full decision history.
> 3. On team cancellation, handoffs survive in `.omc/handoffs/` for session resume. They are not deleted by `TeamDelete`.
> 4. Handoffs are lightweight. 10-20 lines max. They capture decisions and rationale, not full specifications."

### 4d. OMX — reimplements team coordination in Rust + tmux
OMX's team runs **outside** a single session. From primary source:

> "`omx team` is now the canonical launch path for coordinated execution. Workers spawn on-demand and die when their task completes — no idle resource usage. Requires `codex` / `gemini` CLIs installed and an active tmux session." — skills/team/SKILL.md

Mechanically (evidence verbatim from skills/team/SKILL.md Current Runtime Behavior):
1. Parse args (`N`, `agent-type`, task) → sanitize team name from task text
2. Initialize team state:
   - `.omx/state/team/<team>/config.json`
   - `.omx/state/team/<team>/manifest.v2.json`
   - `.omx/state/team/<team>/tasks/task-<id>.json`
3. Compose team-scoped worker instructions at `.omx/state/team/<team>/worker-agents.md` (uses project `AGENTS.md` + worker overlay, without mutating project `AGENTS.md`)
4. Resolve canonical shared state root from leader cwd (`<leader-cwd>/.omx/state`)
5. Split current tmux window into worker panes
6. Launch workers with env: `OMX_TEAM_WORKER=<team>/worker-<n>`, `OMX_TEAM_STATE_ROOT`, `OMX_TEAM_LEADER_CWD`, worker CLI from `OMX_TEAM_WORKER_CLI` (codex/claude/gemini) or `OMX_TEAM_WORKER_CLI_MAP` (per-worker mapping, e.g. `codex,claude`), optional worktree metadata envs when `--worktree` is used
7. Wait for worker readiness via `capture-pane` polling
8. Write per-worker `inbox.md` and trigger via `tmux send-keys`
9. Return control to leader; follow-up uses `omx team status` / `resume` / `shutdown`

### 4e. OMX — data plane vs control plane separation
**Control plane**: tmux panes/processes (one `OMX_TEAM_WORKER` per worker), leader notifications via `tmux display-message`.

**Data plane** (files on shared filesystem):
- `.omx/state/team/<team>/mailbox/leader-fixed.json`
- `.omx/state/team/<team>/mailbox/worker-<n>.json`
- `.omx/state/team/<team>/dispatch/requests.json` (durable dispatch queue, hook-preferred, fallback-aware)
- `.omx/state/team/<team>/workers/worker-<n>/{identity.json, inbox.md, heartbeat.json, status.json}`
- `.omx/state/team-leader-nudge.json`

### 4f. OMX — mailbox protocol (Rust source)
From `crates/omx-runtime-core/src/mailbox.rs`:

```rust
pub struct MailboxRecord {
    pub message_id: String,
    pub from_worker: String,
    pub to_worker: String,
    pub body: String,
    pub created_at: String,
    pub notified_at: Option<String>,
    pub delivered_at: Option<String>,
}

pub enum MailboxError {
    NotFound { message_id: String },
    AlreadyDelivered { message_id: String },
}
```

3-state lifecycle: **created** → `mark_notified()` → **notified** → `mark_delivered()` → **delivered**. Double-delivery throws `AlreadyDelivered`.

**Authority contract** (from docs/contracts/team-runtime-state-contract.md):
> "dispatch `status` is authoritative. Timestamp fields are supporting evidence and must not contradict `status`... a worker is only `integrated` after leader-head advancement / containment checks succeed. Mailbox delivery and tmux activity are not sufficient."

### 4g. OMX — explicit ban on tmux typing as control flow
Primary-source rule (skills/team/SKILL.md):

> "Required default path: Use `omx team ...` runtime lifecycle commands for orchestration. Use `omx team api ... --json` for mailbox/task mutations. **MUST NOT** use direct `tmux send-keys` as the primary mechanism to deliver instructions/messages. **MUST NOT** spam Enter/trigger keys without first checking runtime/state evidence. **MUST** prefer durable state writes + runtime dispatch (`dispatch/requests.json`, mailbox, inbox). Direct tmux interaction is **fallback-only**."

This is unusually disciplined for a tmux-based multi-agent system and contrasts with Ralph-Wiggum-community patterns that rely on send-keys driving.

### 4h. Termination contract
Both OMX and OMC require explicit terminal state before shutdown:
- Pending = 0, in_progress = 0, failed = 0 (or explicitly acknowledged failure)
- Then `omx team shutdown <team>` (OMX) / `/cancel` then `TeamDelete` (OMC)
- Terminal states (both): `complete`, `failed`, `cancelled`

**Active leader monitoring rule** (OMX): while a team is running, the leader must actively poll — "**Minimum acceptable loop**: `sleep 30 && omx team status <team-name>`". The leader "must not go blind."

## 5. Hooks system

### 5a. OMC hooks — layered on Claude Code's native hook surface
OMC's `hooks/hooks.json` registers **5 hook events** with Claude Code's plugin hook system:

| Event | Matcher | Handler script | Timeout |
|---|---|---|---|
| `UserPromptSubmit` | `*` | `keyword-detector.mjs` + `skill-injector.mjs` | 5s / 3s |
| `SessionStart` | `*` | `session-start.mjs` + `project-memory-session.mjs` + `wiki-session-start.mjs` | 5s each |
| `SessionStart` | `init` | `setup-init.mjs` | 30s |
| `SessionStart` | `maintenance` | `setup-maintenance.mjs` | 60s |
| `PreToolUse` | `*` | `pre-tool-enforcer.mjs` | 3s |
| `PermissionRequest` | `Bash` | `permission-handler.mjs` | 5s |
| `PostToolUse` | `*` | `post-tool-verifier.mjs` + `project-memory-posttool.mjs` | 3s |

(All scripts live under `$CLAUDE_PLUGIN_ROOT/scripts/`.)

OMC does NOT invent hooks — it **uses** Claude Code's stable plugin hook registry. Novelty is the per-hook keyword-detector and skill-injector pattern.

### 5b. OMX hooks — 3-layer ownership split
OMX hooks are more architecturally involved because Codex's native hook surface is newer and narrower. Primary-source ownership contract from `docs/codex-native-hooks.md`:

- **Native Codex hooks**: `.codex/hooks.json` (the wrapper entries invoke `dist/scripts/codex-native-hook.js`)
- **OMX plugin hooks**: `.omx/hooks/*.mjs`
- **tmux/runtime fallbacks**: `omx tmux-hook`, notify-hook, derived watcher, idle/session-end reporters

OMX's **hook mapping matrix** (the concrete mechanics table):

| OMC/OMX surface | Native Codex source | OMX runtime target | Status |
|---|---|---|---|
| `session-start` | `SessionStart` | `session-start` | native |
| wiki startup context | `SessionStart` | `session-start` | native (read-mostly) |
| `keyword-detector` | `UserPromptSubmit` | `keyword-detector` | native |
| `pre-tool-use` | `PreToolUse` (**Bash-only**) | `pre-tool-use` | native-partial |
| `post-tool-use` | `PostToolUse` (**Bash-only**) | `post-tool-use` | native-partial |
| Ralph persistence stop | `Stop` | `stop` | native-partial (uses `decision: "block"` + `reason` continuation contract) |
| Autopilot/Ultrawork/UltraQA continuation | `Stop` | `stop` | native-partial |
| Team-phase continuation | `Stop` | `stop` | native-partial (uses per-team `phase.json` as canonical) |
| ralplan/deep-interview skill-state continuation | `Stop` | `stop` | native-partial (blocks on active `skill-active-state.json`) |
| auto-nudge continuation | `Stop` | `stop` | native-partial (suppressed during interview states) |
| `ask-user-question` | none | runtime-only | runtime-fallback |
| non-Bash tool interception | none | runtime-only | runtime-fallback |
| `SubagentStop` | none | runtime-only | **not-supported-yet** (OMC-specific lifecycle extension) |
| `session-end` | none | `session-end` | runtime-fallback |
| `session-idle` | none | `session-idle` | runtime-fallback |

**Notable hook-specific behaviors**:
- Native `PreToolUse` for Bash "cautions on `rm -rf dist` and blocks inspectable inline `git commit` commands until Lore-format structure + the required `Co-authored-by: OmX <omx@oh-my-codex.dev>` trailer are present"
- `UserPromptSubmit` triage layer — when no keyword matches, classifies the prompt into PASS/LIGHT/HEAVY triage hints as *advisory prompt-routing context* (not skill activation). Users can suppress with "no workflow", "just chat", "plain answer".

### 5c. OMX extensibility — OpenClaw gateway
Both harnesses support forwarding hook events to an **OpenClaw gateway** (external service at openclaw.ai). Event matrix (from OMC README):

| Event | Trigger | Template variables |
|---|---|---|
| `session-start` | Session begins | `{{sessionId}}`, `{{projectName}}`, `{{projectPath}}` |
| `stop` | Claude response completes | `{{sessionId}}`, `{{projectName}}` |
| `keyword-detector` | Every prompt submission | `{{prompt}}`, `{{sessionId}}` |
| `ask-user-question` | Claude requests user input | `{{question}}`, `{{sessionId}}` |
| `pre-tool-use` | Before tool invocation (**high frequency**) | `{{toolName}}`, `{{sessionId}}` |
| `post-tool-use` | After tool invocation (**high frequency**) | `{{toolName}}`, `{{sessionId}}` |

Config lives at `~/.claude/omc_config.openclaw.json` / OMX equivalent. Env vars: `OMC_OPENCLAW=1`, `OMC_OPENCLAW_DEBUG=1`, `OMC_OPENCLAW_CONFIG`. Reply channel: Discord/Telegram/Slack with bidirectional messaging (`OPENCLAW_REPLY_CHANNEL`, `OPENCLAW_REPLY_TARGET`, `OPENCLAW_REPLY_THREAD`).

## 6. HUD

### 6a. OMX HUD — explicit two-layer architecture
Primary-source description (skills/hud/SKILL.md):

> "The OMX HUD uses a two-layer architecture:
> 1. **Layer 1 - Codex built-in statusLine**: Real-time TUI footer showing model, git branch, and context usage. Configured via `[tui] status_line` in `~/.codex/config.toml`. Zero code required.
> 2. **Layer 2 - `omx hud` CLI command**: Shows OMX-specific orchestration state (ralph, ultrawork, autopilot, team, pipeline, ecomode, turns). Reads `.omx/state/` files."

**Layer 1 items available** (Codex CLI v0.101.0+): `model-name`, `model-with-reasoning`, `current-dir`, `project-root`, `git-branch`, `context-remaining`, `context-used`, `five-hour-limit`, `weekly-limit`, `codex-version`, `context-window-size`, `used-tokens`, `total-input-tokens`, `total-output-tokens`, `session-id`.

**Layer 2 presets**:
- `minimal`: `[OMX] ralph:3/10 | turns:42`
- `focused` (default): `[OMX] ralph:3/10 | ultrawork | team:3 workers | turns:42 | last:5s ago`
- `full`: full preset + `autopilot:execution | pipeline:exec | total-turns:156`

**State sources** (Layer 2 reads):
- `.omx/state/ralph-state.json` — Ralph loop iteration
- `.omx/state/ultrawork-state.json`, `autopilot-state.json`, `team-state.json`, `pipeline-state.json`, `ecomode-state.json`
- `.omx/state/hud-state.json` — Last activity (from notify hook)
- `.omx/metrics.json` — Turn counts

**Color coding**: Green (normal), Yellow (ralph >70% of max), Red (ralph >90%).

**Wiring**: `omx hud` polls (`--watch` polls every 1s), `--json` outputs raw state for scripting. Not a TUI library interception; it's a stdout-writing CLI that reads persisted JSON state files. `omx setup` auto-configures both layers.

### 6b. OMC HUD — same concept, different substrate
OMC's HUD is a "statusline" widget that reads `.omc/sessions/*.json` and `.omc/state/agent-replay-*.jsonl`, exposed via `/oh-my-claudecode:hud setup`. Presets named `focused` etc. OMC uses env var `OMC_PLUGIN_ROOT` when launched via `claude --plugin-dir <path>` to keep the HUD bundle aligned with the plugin loader.

## 7. Context & memory model
- **Per-session state**: `.omc/` or `.omx/` directory trees. Session scope files override root scope files (ralph-state-contract: "Writes MUST target one scope (authoritative scope), never broadcast to unrelated sessions").
- **Scoped paths**: session-scope = `.omx/state/sessions/{session_id}/ralph-state.json`; root = `.omx/state/ralph-state.json`. Reconciliation via notify-hook, single-owner semantics enforced.
- **Cross-session learning**:
  - OMC `/learner` skill extracts reusable patterns with "strict quality gates"; stored in `.omc/skills/` (project) or `~/.omc/skills/` (user). Auto-inject by trigger matching.
  - Skill file schema (from OMC README):
    ```yaml
    ---
    name: Fix Proxy Crash
    description: aiohttp proxy crashes on ClientDisconnectedError
    triggers: ["proxy", "aiohttp", "disconnected"]
    source: extracted
    ---
    ```
  - Project scope overrides user scope.
- **AGENTS.md**: project-level persistent guidance (shared contract with Ralph-Wiggum pattern). OMX `omx setup` writes AGENTS.md scaffolding. Setup refresh preserves local AGENTS.md content per bug fix #1673.
- **Wiki layer (OMX)**: markdown-first, search-first (not vector-first). Lives at `.omx/wiki/`. `omx wiki list|query|lint|refresh` with JSON output. MCP server parity via `omx wiki`.
- **Context snapshots** (Pre-context Intake Gate): EVERY skill (ralph, team, ralplan, deep-interview) requires a snapshot at `.omx/context/{slug}-{timestamp}.md` with task statement / desired outcome / known facts / constraints / unknowns / codebase touchpoints BEFORE execution starts. If high ambiguity, run `explore` first + `$deep-interview --quick`.

## 8. State & persistence

### 8a. Frozen state contracts (OMX)
OMX has **frozen state contracts** (`docs/contracts/*.md`) that are non-negotiable schemas:
- `ralph-state-contract.md` — Ralph phase enum (`starting/executing/verifying/fixing/complete/failed/cancelled`), scope policy, owner metadata.
- `team-runtime-state-contract.md` — dispatch status enum (`pending/notified/delivered/failed`), integration authority, stale ownership.
- `team-delivery-state-contract.md`, `multi-state-transition-contract.md`, `ralph-cancel-contract.md`, `mux-operation-space.md`, `runtime-command-event-snapshot-schema.md`, `rust-runtime-thin-adapter-contract.md`.
- **Multi-state transition contract**: approved overlaps are `team + ralph` and `team + ultrawork`. Other overlaps are deny-by-default; require explicit `omx state ...` clearance.

### 8b. Dispatch status authority
From team-runtime-state-contract.md — "dispatch `status` is authoritative. Timestamp fields are supporting evidence and must not contradict `status`". Mailbox `notified_at`/`delivered_at` are derivative evidence only. `integrated` status requires leader-head advancement/containment checks (just mailbox delivery is not sufficient).

### 8c. State file hierarchy
```
.omx/
├── state/
│   ├── sessions/{session_id}/     # session scope (authoritative when session_id known)
│   │   ├── ralph-state.json
│   │   ├── ralph-progress.json
│   │   ├── autopilot-state.json
│   │   └── ...
│   ├── ralph-state.json           # root scope (compat fallback only)
│   ├── team/<team>/
│   │   ├── config.json
│   │   ├── manifest.v2.json
│   │   ├── tasks/task-<id>.json
│   │   ├── mailbox/{leader-fixed,worker-<n>}.json
│   │   ├── dispatch/requests.json
│   │   └── workers/worker-<n>/{identity,inbox.md,heartbeat,status}.json
│   ├── team-leader-nudge.json
│   ├── hud-state.json
│   └── session.json
├── plans/prd-{slug}.md
├── specs/deep-interview-{slug}.md
├── interviews/{slug}-{timestamp}.md
├── context/{slug}-{timestamp}.md
├── logs/hooks-*.jsonl
├── metrics.json
├── hud-config.json
└── wiki/
```

OMC's equivalent under `.omc/` + `~/.claude/teams/<team>/` + `~/.claude/tasks/<team>/` (native team storage).

## 9. Safety / permissions
- **OMC PermissionRequest hook**: `scripts/permission-handler.mjs` intercepts Bash permission requests (5s timeout).
- **OMX native PreToolUse hardening** (Bash-only):
  - Cautions on `rm -rf dist`
  - Blocks `git commit` unless message has Lore-format structure + `Co-authored-by: OmX <omx@oh-my-codex.dev>` trailer
- **OMX native PostToolUse**: command-not-found / permission-denied / missing-path guidance + informative non-zero-output review
- **Active team ban on tmux send-keys as primary control flow** — state-first discipline (see §4g)
- **Security hardening recent (OMX 0.13.2, 2026-04-18)**:
  - Path traversal in identifier handling (PRs #1658, #1674, issue #1650) — validated identifiers before team/session joins
  - HUD shell / regex injection — `execFileSync` replaced with async `execFile`; git helpers reject shell/regex metacharacters (PRs #1662, #1652)
  - Reply acknowledgement redaction (PR #1670)
  - Transitive CVE npm audit fix (PR #1669)
- **Enterprise deployment**: OMC has dedicated `SECURITY.md`.
- **No `--dangerously-skip-permissions` posture**: Unlike Ralph-Wiggum-community, OMC/OMX do not advocate YOLO mode. Safety posture is "gated, stage-verified, hook-hardened" — the opposite of Huntley's Ralph.

## 10. Economics / cost model
- **OMC cost claim**: "Smart model routing saves 30-50% on tokens" (README, unverified).
- **Cost mode**: OMC has a `cost mode: downgrade` that drops `opus → sonnet`, `sonnet → haiku` where quality permits; `team-verify` always at least `sonnet`.
- **Per-stage model routing** (OMC team): architect/critic = Opus; executor = Sonnet default, Opus for complex multi-file; writer = Haiku; debugger = Sonnet; verifier = Sonnet minimum.
- **OMX thinking-level rule**: NO model-name heuristic mapping. "Team runtime must **not** infer `model_reasoning_effort` from model-name substrings". Per-worker reasoning effort allocated dynamically from role (`low`, `medium`, `high`); explicit `-c model_reasoning_effort=...` in `OMX_TEAM_WORKER_LAUNCH_ARGS` wins.
- **OMC analytics**: built-in "analytics & cost tracking" per README; token usage across all sessions.
- **OMX env vars for defaults**: `OMX_DEFAULT_FRONTIER_MODEL`, `OMX_DEFAULT_SPARK_MODEL` (legacy alias `OMX_SPARK_MODEL`).
- **Benchmarks present**: OMC ships `benchmark/` + `benchmarks/code-reviewer/`, `/debugger/`, `/executor/`, `/harsh-critic/` with fixtures, ground-truth JSON, and `run-benchmark.ts` — suggests internal measurement culture (no public result claims yet visible in top-level README).

## 11. Comparative position (vs existing corpus)

### vs Ralph Wiggum (Huntley, 2025-07)
- **Namesake borrowed, mechanism changed**: `$ralph` keeps the "persistence until done" spirit but replaces bash `while true` with a native skill that runs in-session, delegates to sub-agents in parallel, mandates verification phases, and uses Codex native `Stop` hook continuation ("The boulder never stops") instead of shell loop.
- **Huntley's `--dangerously-skip-permissions` YOLO stance is explicitly abandoned**: OMC/OMX add `PreToolUse` enforcers, permission handlers, Lore-format git commit gates.
- **"Only one thing per loop" rule kept implicitly**: OMX ralph PRD mode forces story-by-story execution; each iteration picks the highest-priority story with `passes: false`.
- **Transferable primitive P1 from Ralph (fresh context per iteration + file-mediated memory) is preserved** via frozen state contracts: session-scope wins over root-scope; notify-hook reconciliation.

### vs Superpowers (obra, 2025-10)
- **Same SKILL.md substrate**: both use Anthropic Agent Skills format.
- **Different skill *content* layer**: Superpowers ships ~40 skills focused on personal craft (`brainstorming`, `tdd`, `using-git-worktrees`, `systematic-debugging`). OMC ships 40 skills focused on team orchestration (19 specialized agents with stage routing).
- **OMC's `/learner` skill mirrors Superpowers' "learn-from-session" pattern but extracts into a different storage layer** (`.omc/skills/` project vs `~/.omc/skills/` user, with YAML frontmatter triggers).
- **Axis F (skill as unit of discipline) reconfirmed**: this is OMC/OMX's **6th independent use** of the SKILL.md-plus-convention-layer pattern (after Superpowers, gstack, ECC, CE, revfactory-harness).

### vs GSD (2026-02)
- **Both use staged phase pipeline**: GSD `discuss/plan/execute/verify/ship`; OMC `team-plan/prd/exec/verify/fix`.
- **Both spawn fresh subagent contexts per phase** for context-rot mitigation.
- **GSD's `{PHASE}-{WAVE}-{TYPE}.md` naming regex is stricter than OMC's `.omc/handoffs/<stage-name>.md`** — GSD names encode process state, OMC names encode only which stage boundary.
- **Axis C (mode splitting) reconfirmed**: 9th independent use.

### vs Compound Engineering (Every.to, 2026)
- **Both implement "learn from iteration" pattern (axis L)**: CE has `/ce:compound`; OMC has `/learner`. OMX has `$autoresearch`. Third strong independent use of axis L — promotion locked in.
- **CE's `/ce:plan` is a similar gate to OMC's `$ralplan`** but CE doesn't have a pre-execution auto-gate; users have to explicitly invoke.
- **OMC's 19 agents + CE's 26 agents + ECC's 47 agents — converging on ~20-50 specialized agent rosters as the sweet spot.**

### vs Ouroboros (Q00, 2026-01)
- **Both use numeric ambiguity thresholds** (axis I): Ouroboros 0.2/0.95/0.3; OMX deep-interview 0.30/0.20/0.15. **Third independent use** — axis I promotion.
- **Ouroboros `interview → crystallize → execute → evaluate → evolve` maps partly to OMX `$deep-interview → $ralplan → $team|$ralph → $ultraqa → $learner`** but OMX isn't explicitly evolve-step-oriented.

### vs ECC (2026-01)
- ECC's 47 agents + instinct learning + 181 skills feels like the architectural predecessor of OMC's compactified 19 agents + `/learner` + ~40 skills. Consolidation.

### vs Claude Code native team feature
- **OMC is the single biggest *production* use of `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` observable in the wild**. Evidence for the global CLAUDE.md catalog's re-evaluation trigger ("short roundtrip verification loop pattern across 3+ harnesses"): OMC demonstrates this pattern in production at scale.

## 12. Limitations & open questions

### Known limitations (authored self-acknowledged)
- **OMX Windows support is secondary**: "Native Windows and Codex App are not the default experience, may break or behave inconsistently, and currently receive less support." psmux accepted as tmux binary on Windows.
- **OMX Intel Mac startup CPU spike**: `syspolicyd` / `trustd` during Gatekeeper validation of concurrent `--madmax --high` launches. Mitigations: `xattr -dr com.apple.quarantine`, lower concurrency.
- **OMX non-Bash tool interception is runtime-fallback only** — native PreToolUse/PostToolUse is Bash-only per Codex's current hook surface.
- **`SubagentStop` is OMC-specific**; not available in OMX (Codex has no equivalent lifecycle event).
- **Shift+Enter in tmux**: known issue where tmux extended-keys may not forward (docs/troubleshooting.md #1682).
- **Team-ralph combined mode deprecated** in OMX 0.4.4: `omx team ralph ...` removed; must launch separately.

### Derived concerns (observer)
- **Complexity budget**: OMX/OMC together add ~160+ SKILL.md files + 19-26 agents + 5+ lifecycle contracts + Rust runtime. Onboarding surface is non-trivial despite the "zero configuration" marketing.
- **Feature gap drift**: OMX maintains a `ralph-parity-matrix.md` and `ralph-upstream-baseline.md` — explicit that OMX and OMC diverge per-feature. The "same canonical skills" claim is aspirational, not fully enforced.
- **Heavy bug-fix cadence on state-handling**: CHANGELOG 0.13.2 (2026-04-18) fixed 6+ Ralph/runtime-authority issues in one patch. Indicates state contracts are genuinely hard to get right.

### Open questions (would need more probes to resolve)
- **Benchmark results**: OMC ships benchmark fixtures for code-reviewer / debugger / executor / harsh-critic. Results not surfaced in top-level README. Probe: read `benchmarks/*/run-benchmark.ts` + any `predictions/` checkpoint.json outputs to extract self-reported SWE-bench-like scores.
- **Comparative adoption**: 29.9k (OMC) vs 24.1k (OMX) stars — is star velocity converging or diverging? Star History chart exists (https://api.star-history.com/svg?repos=Yeachan-Heo/oh-my-codex).
- **`a2a-mcp.org`, `aitoolly.com`, `pyshine.com`, `htdocs.dev` external coverage**: SEO blog mechanisms not cross-checked for accuracy against repo source; treat as signal-amplification only per brief's guardrails.
- **Reserved for follow-up**: How do the OpenClaw template variables get sanitized? What's the actual auth model for the gateway?

## 13. OMC vs OMX delta table

| Feature | OMC (Claude Code) | OMX (Codex CLI) | Key divergence |
|---|---|---|---|
| **Substrate** | Claude Code plugin + npm package `oh-my-claude-sisyphus` | Codex CLI wrapper + npm package `oh-my-codex` | Host CLI |
| **Version** (2026-04-19) | v4.13.0 | v0.14.0 | OMC is older/more mature semver |
| **Stars** | 29,922 | 24,116 | OMC ~24% larger |
| **Language** | TypeScript | TypeScript + **Rust crates** | OMX has `omx-runtime-core` Rust for team internals |
| **Skill invocation** | `/skill-name` (Claude Code slash) | `$skill-name` (keyword) or `/skill-name` (Codex slash) | OMX uses `$` prefix, OMC uses `/` |
| **Team substrate** | Claude Code native `TeamCreate`/`TaskCreate`/`SendMessage` | Own Rust runtime + tmux panes + `.omx/state/team/` files + mailbox JSON | **Fundamental divergence** |
| **Team flag required** | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `~/.claude/settings.json` | None (self-owned runtime) | OMC fails over to non-team if flag unset |
| **Team storage** | `~/.claude/teams/<team>/config.json` + `~/.claude/tasks/<team>/*.json` (managed by Claude Code itself) | `.omx/state/team/<team>/{config.json,manifest.v2.json,tasks/,mailbox/,dispatch/,workers/}/` | OMC delegates, OMX owns |
| **Team stage pipeline** | `team-plan → team-prd → team-exec → team-verify → team-fix` with `.omc/handoffs/<stage>.md` | Similar staged pipeline; state contracts at `docs/contracts/team-runtime-state-contract.md` | OMX has frozen contracts, OMC has runbook prose |
| **Hook surface** | Claude Code native hooks (5 events: UserPromptSubmit, SessionStart, PreToolUse, PermissionRequest, PostToolUse) via `hooks/hooks.json` | 3-layer split: native Codex hooks / `.omx/hooks/*.mjs` plugin hooks / tmux+runtime fallbacks | OMX has explicit ownership contract (docs/codex-native-hooks.md) |
| **Hook native partial** | Full Claude Code surface | PreToolUse/PostToolUse **Bash-only**; `SubagentStop` not-supported-yet | Codex hook surface is narrower |
| **HUD architecture** | Single statusline via `omc hud` reading `.omc/sessions/*.json` + `.omc/state/agent-replay-*.jsonl` | **Two-layer**: Codex built-in `[tui] status_line` (Layer 1) + `omx hud` CLI reading `.omx/state/*.json` (Layer 2) | OMX explicit two-layer |
| **Agent roster** | 19 specialized agents under `agents/*.md` | 31 prompts under `prompts/*.md` (different packaging) | Different distribution model |
| **Worker CLI mixing** | Via `/ccg` skill (`/ask codex` + `/ask gemini` synthesis) | Via `OMX_TEAM_WORKER_CLI_MAP=codex,claude,gemini` env | Different composition axes |
| **PRD mode** | `ralph --prd` auto-generates `prd.json` scaffold, forces story refinement | `$ralph` + `--prd` flag, canonical at `.omx/plans/prd-{slug}.md`, legacy `.omx/prd.json` validation | Both present, slightly different storage |
| **Learner / skill extraction** | `/learner` extracts to `.omc/skills/` with YAML frontmatter + triggers | `$autoresearch` workflow (mission-driven, validator-gated) | OMC pattern-extraction-first, OMX mission-research-first |
| **Wiki** | Not mentioned as first-class; references exist | `.omx/wiki/` markdown-first, search-first; MCP server `omx wiki {list,query,lint,refresh}` | OMX has a wiki layer |
| **Launch command** | `omc --plugin-dir <path>` or `/plugin install` | `omx --madmax --high` (interactive leader), `omx --tmux --madmax --high` (tmux leader) | Different launch idioms |
| **Doctor readiness** | `/omc-doctor`, clears plugin cache | `omx doctor` + explicit "does not prove authenticated Codex request" warning + `omx exec --skip-git-repo-check -C . "Reply with exactly OMX-EXEC-OK"` smoke test | OMX has explicit 2-boundary check: setup readiness vs auth readiness |
| **Commit trailer enforcement** | Not explicit | Native PreToolUse requires `Co-authored-by: OmX <omx@oh-my-codex.dev>` trailer on inline `git commit` | OMX-specific identity gate |
| **Sparkshell** | N/A | `omx sparkshell <command>` — shell-native inspection crate | OMX Rust-only feature |
| **Explore** | `/deep-dive` skill | `omx explore --prompt "..."` Rust binary (`crates/omx-explore/`) | OMX Rust-backed |
| **Languages** | 7 README translations (en/ko/zh/ja/es/vi/pt) | 15 README translations (+de/fr/it/ru/tr/el/pl/uk/zh-TW) | OMX more international |

## 14. Ecosystem / uptake signals
- **OMC**: 29,922★, repo size 42 MB, top collaborators contribute 20-65 commits each. v4.13.0 current. Release cadence: bug-fix-heavy (4 PRs / latest release).
- **OMX**: 24,116★, repo size 9.4 MB, v0.14.0 current (released today 2026-04-19). 20+ versions in ~10 weeks.
- **Author**: Yeachan Heo, Korean, GitHub Sponsors-enabled.
- **Community**: Single shared Discord for both (invite `https://discord.gg/PUwSMR9XNk`, guild id 1452487457085063218).
- **Supporting packages (observed)**:
  - `oh-my-claude-sisyphus` on npm (OMC's npm name — branding split)
  - Homepage `https://oh-my-claudecode.dev` (OMC) + `https://oh-my-codex.dev` (OMX)
  - Website docs at `yeachan-heo.github.io/oh-my-claudecode-website` and `yeachan-heo.github.io/oh-my-codex-website`
- **Sponsor tiers**: `.github/SPONSOR_TIERS.md` present in OMC.
- **Commercial signal**: OpenClaw (openclaw.ai) is external paid(?) gateway that both OMC and OMX integrate with. Suggests a broader product ecosystem around `yeachan-heo`.
- **External coverage** (secondary sources — not cross-checked per guardrails):
  - https://a2a-mcp.org/blog/what-is-oh-my-codex
  - https://aitoolly.com/ai-news/article/2026-04-06-introducing-oh-my-codex-omx-enhancing-codex-with-hooks-agent-teams-and-hud-features
  - https://pyshine.com/oh-my-codex-AI-Coding-Harness/
  - https://htdocs.dev/posts/from-conductor-to-orchestrator-a-practical-guide-to-multi-agent-coding-in-2026/

## 15. Transferable primitives ★

Each primitive: name / 2-line description / assumed context / standalone-extractable?

### P1. Substrate-aware team abstraction with two implementations
- A single skill vocabulary (`$team`, `$ralph`, `$ralplan`, `$deep-interview`) with **two interchangeable substrate-specific implementations** — one riding the host CLI's native primitives, one reimplementing them. Same user-facing contract, different runtime.
- **Assumed context**: multiple target substrates (Claude Code + Codex CLI + Gemini CLI); author willingness to maintain parity; state contracts documented.
- **Standalone-extractable?** **Partial**. The pattern transfers (design skill vocabulary first, implement per-substrate); the Rust runtime engineering is substantial.

### P2. Pre-execution gate via lexical specificity heuristic
- Intercept bare prompts like `ralph fix this` when they have no concrete anchors (file path, symbol, issue number, test runner, numbered steps, code block), redirect to `$ralplan` consensus planning. Detection is purely lexical (fast, deterministic); escape via `force:` / `!` prefix.
- **Assumed context**: a distinct planning workflow exists to redirect TO; users have occasional need to bypass.
- **Standalone-extractable?** **YES**. The detection regex set (file path, camelCase, issue ref, etc.) is portable to any harness that exposes execution keywords. Copy-pasteable.

### P3. `.omc/handoffs/<stage>.md` — stage-to-stage RPC contract
- Every stage of a pipeline writes a fixed-schema markdown file (`Decided / Rejected / Risks / Files / Remaining`, 10-20 lines) BEFORE transitioning. Next stage reads previous handoffs before spawning its agents. Handoffs accumulate and survive cancellation.
- **Assumed context**: multi-stage pipeline; risk of context loss across stage boundaries.
- **Standalone-extractable?** **YES**. Pure convention + directory layout. No runtime dependency. Small enough to adopt in 30 min.

### P4. Frozen schema + enum phase vocabulary
- State files have schemas that are **explicitly marked "Frozen"** — `current_phase MUST be one of {starting,executing,verifying,fixing,complete,failed,cancelled}. Unknown phase values MUST be rejected.` Notify-hook reconciliation follows strict scope rules (session-scope > root-scope, single-owner, no cross-session broadcasts).
- **Assumed context**: long-running state across multiple processes/sessions; concurrency risk.
- **Standalone-extractable?** **YES**. Any harness maintaining phase state can adopt the "freeze the enum + document scope policy" discipline.

### P5. Two-layer HUD (built-in statusline + external CLI poller)
- Layer 1: leverage the host CLI's native statusline for always-visible primitives (model, branch, context used). Layer 2: separate `omx hud` CLI that reads persisted JSON state files and renders orchestration-specific widgets. Two-layer separates "terminal UX" from "workflow state."
- **Assumed context**: host CLI exposes a statusline config; workflow has persisted state.
- **Standalone-extractable?** **YES**. Pattern (not implementation) is fully portable.

### P6. Native hook ownership matrix (3-column ownership split)
- Every event has an explicit ownership column: **Native** (ride host CLI hook) / **Plugin** (harness's own hook scripts) / **Fallback** (tmux / notify / watcher for events the host doesn't expose). Documented in a single table with status column (`native` / `native-partial` / `runtime-fallback` / `not-supported-yet`).
- **Assumed context**: host CLI has some hook surface but it's not complete; harness adds features the host lacks.
- **Standalone-extractable?** **YES**. The ownership discipline (don't silently choose one; document the matrix) is the primitive.

### P7. Ambiguity as weighted numeric gate with mandatory qualitative readiness gates
- Weighted numeric ambiguity score (0.30 intent + 0.25 outcome + ...) + depth-specific thresholds — BUT gate also requires two qualitative gates: `Non-goals` explicit + `Decision Boundaries` explicit + "pressure pass" completed (revisit an earlier answer deeper). Numeric threshold alone is not sufficient.
- **Assumed context**: intent-first interview workflow precedes execution.
- **Standalone-extractable?** **YES**. Replicates and extends Ouroboros's numeric gate pattern (axis I, 3rd independent use).

### P8. Per-stage model-tier + reasoning-level allocation
- Each pipeline stage has a default model tier (Haiku/Sonnet/Opus) and reasoning level (low/medium/high) independent from any model-name heuristic. Explicit ban: "Team runtime must **not** infer `model_reasoning_effort` from model-name substrings (e.g., `spark`, `high-capability`, `mini`)." Per-worker reasoning effort allocated dynamically from resolved role.
- **Assumed context**: multi-tier model access; cost sensitivity.
- **Standalone-extractable?** **YES**. Pure policy primitive.

### P9. Mailbox with 3-state message lifecycle + authoritative status field
- Messages transition through `created → notified → delivered`; double-delivery returns `AlreadyDelivered`. Dispatch `status` is **authoritative**; timestamp fields (`notified_at`, `delivered_at`) are *derivative evidence*, never authoritative. Consumers must not infer integration from mailbox activity alone.
- **Assumed context**: multi-worker coordination over shared filesystem or queue.
- **Standalone-extractable?** **PARTIAL**. Concept transfers; implementation effort is non-trivial (see OMX Rust source).

### P10. State-first, tmux-last discipline
- Explicit primary-source rule: "MUST NOT use direct `tmux send-keys` as the primary mechanism to deliver instructions/messages. MUST NOT spam Enter/trigger keys without first checking runtime/state evidence. MUST prefer durable state writes + runtime dispatch. Direct tmux interaction is **fallback-only**."
- **Assumed context**: tmux-based multi-agent coordination.
- **Standalone-extractable?** **YES**. Anti-pattern avoidance rule.

### P11. PRD-driven ralph (story-by-story with refinable scaffold)
- Ralph auto-generates a `prd.json` scaffold if none exists; user is **forced to refine generic acceptance criteria** ("Implementation is complete") into task-specific ones ("Function X returns Y when given Z", "Test file exists at path P and passes") before execution continues. Then picks highest-priority story with `passes: false` each iteration; story-by-story completion.
- **Assumed context**: task complex enough to decompose; acceptance criteria are first-class.
- **Standalone-extractable?** **YES**. Template + selection rule, portable.

### P12. Pre-context intake gate across all execution modes
- EVERY heavy execution skill (ralph, team, ralplan, deep-interview) requires a context snapshot at `.omx/context/{slug}-{timestamp}.md` (task / outcome / facts / constraints / unknowns / touchpoints) BEFORE execution starts. If snapshot is stale or missing, run `explore` + `$deep-interview --quick` first.
- **Assumed context**: fresh sessions or resumed sessions can have stale context.
- **Standalone-extractable?** **YES**. Universal gate applicable to any multi-step agent system.

### P13. Doctor-vs-exec-smoke two-boundary readiness check
- `omx doctor` verifies install shape; `omx exec --skip-git-repo-check -C . "Reply with exactly OMX-EXEC-OK"` verifies auth + profile + provider base-URL + network. Primary-source rule: "Do not claim 'native hooks work' when only tmux or synthetic notify fallback paths were exercised. Likewise, do not claim real execution readiness from hook/install evidence alone; validate an actual Codex execution in the active runtime profile."
- **Assumed context**: wrapper over an API-authenticated CLI with multiple failure modes.
- **Standalone-extractable?** **YES**. Health-check discipline.

### P14. Canonical commit co-author gate (identity-level attribution)
- Native PreToolUse hook blocks `git commit` until message contains `Co-authored-by: OmX <omx@oh-my-codex.dev>` trailer + Lore-format structure. Identity attribution baked into tool enforcement.
- **Assumed context**: want to know which commits were harness-assisted; have hook authority.
- **Standalone-extractable?** **PARTIAL**. Concept portable; implementation requires `PreToolUse` hook on `Bash(git commit)`.

### P15. "The boulder never stops" — Stop hook continuation contract
- Native `Stop` hook returns `decision: "block"` + `reason` to continue non-terminal Ralph/Autopilot/Ultrawork/UltraQA sessions. Re-blocks on later fresh Stop replies. Avoids re-blocking once `stop_hook_active` is set (infinite-loop safety valve).
- **Assumed context**: host CLI exposes a Stop hook with decision semantics.
- **Standalone-extractable?** **PARTIAL**. Depends on host hook semantics; concept transferable.

### Rejected as primitive (important)
- **`OMX_TEAM_WORKER_CLI_MAP=codex,claude` mixed-CLI teams**: interesting engineering but not a generalizable primitive — it's a per-product feature that only makes sense when you have 3 major substrates to compose.
- **`.omx/wiki/` markdown-first search-first**: niche; many harnesses don't need a wiki.
- **`omx hud` color coding (green/yellow/red at 70%/90%)**: too low-level.
- **npm package name divergence (`oh-my-claude-sisyphus` vs repo name `oh-my-claudecode`)**: branding accident, not a primitive.

## Sources

### Primary (repos + docs)
- https://github.com/Yeachan-Heo/oh-my-claudecode — OMC repo
- https://github.com/Yeachan-Heo/oh-my-codex — OMX repo
- https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/README.md
- https://github.com/Yeachan-Heo/oh-my-codex/blob/main/README.md
- https://github.com/Yeachan-Heo/oh-my-codex/blob/main/CHANGELOG.md
- https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/CHANGELOG.md
- https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/.claude-plugin/plugin.json
- https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/hooks/hooks.json
- https://github.com/Yeachan-Heo/oh-my-codex/blob/main/package.json

### Primary (skills — the load-bearing evidence)
- https://github.com/Yeachan-Heo/oh-my-codex/blob/main/skills/team/SKILL.md
- https://github.com/Yeachan-Heo/oh-my-codex/blob/main/skills/ralph/SKILL.md
- https://github.com/Yeachan-Heo/oh-my-codex/blob/main/skills/ralplan/SKILL.md
- https://github.com/Yeachan-Heo/oh-my-codex/blob/main/skills/deep-interview/SKILL.md
- https://github.com/Yeachan-Heo/oh-my-codex/blob/main/skills/hud/SKILL.md
- https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/skills/team/SKILL.md
- https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/skills/ralph/SKILL.md
- https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/skills/ralplan/SKILL.md
- https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/skills/autopilot/SKILL.md

### Primary (contracts — the frozen schemas)
- https://github.com/Yeachan-Heo/oh-my-codex/blob/main/docs/codex-native-hooks.md
- https://github.com/Yeachan-Heo/oh-my-codex/blob/main/docs/contracts/ralph-state-contract.md
- https://github.com/Yeachan-Heo/oh-my-codex/blob/main/docs/contracts/team-runtime-state-contract.md

### Primary (Rust source — team runtime internals)
- https://github.com/Yeachan-Heo/oh-my-codex/blob/main/crates/omx-runtime-core/src/mailbox.rs
- https://github.com/Yeachan-Heo/oh-my-codex/blob/main/crates/omx-runtime-core/src/dispatch.rs
- https://github.com/Yeachan-Heo/oh-my-codex/blob/main/crates/omx-runtime-core/src/authority.rs

### Secondary (not cross-checked, treat as signal amplification)
- https://a2a-mcp.org/blog/what-is-oh-my-codex
- https://aitoolly.com/ai-news/article/2026-04-06-introducing-oh-my-codex-omx-enhancing-codex-with-hooks-agent-teams-and-hud-features
- https://pyshine.com/oh-my-codex-AI-Coding-Harness/
- https://htdocs.dev/posts/from-conductor-to-orchestrator-a-practical-guide-to-multi-agent-coding-in-2026/
