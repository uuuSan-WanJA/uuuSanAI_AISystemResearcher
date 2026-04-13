---
title: Graft evaluation — Tier 1 synthesis → Bundle_GameMaker
date: 2026-04-13
harness_note: insights/synthesis_tier1.md (cross-cutting patterns across 9 harnesses)
individual_notes:
  - notes/harness/ecc.md
  - notes/harness/compound-engineering.md
  - notes/harness/revfactory-harness.md
  - notes/harness/gsd.md
  - notes/harness/superpowers.md
project_map: insights/project_map_gamemaker.md
constraints: []
---

## TL;DR

1. **SKILL.md convention for delegation protocol** (Fit 5/5) — converts the recurring vitest anti-pattern trap from prose rule to auditable SKILL.md with anti-trigger test, in `CollabMonitor_Codex/CLAUDE.md` + new `.claude/skills/` files.
2. **Compound step — session-level learning artifact** (Fit 4/5) — adds a `docs/solutions/` loop on top of the existing Evolver, giving two-tier learning (per-session + cross-cycle) without touching Engine internals.
3. **`{PHASE}-{WAVE}-{TYPE}` artifact naming protocol** (Fit 4/5) — makes Monitor's 6+ state-file zoo navigable by encoding lifecycle state in filenames, with zero code changes.

---

## Full evaluation table

| # | Primitive | Source | Applicable? | Already present? | Fills gap? | Insertion point | Risk | Effect | Depends on | Verdict | Fit |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **SKILL.md for delegation protocol** (CP4 / axis-F) | Superpowers P4, gstack, revfactory P4, ECC P1 | YES — Claude Code runtime is the active surface | NO — prose-only in CLAUDE.md files | YES — directly addresses Pain Point 8 (vitest re-run trap) and axis-F gap | New `.claude/skills/` dir in `uuuSanAI_GameMakerEngine/` + `uuuSanAI_GameMaker/`; move delegation rules out of `GameMakerEngine/CLAUDE.md:82-97` and `GameMaker/CLAUDE.md:43-62` into skill frontmatter | Low — additive, existing prose can remain as fallback | MED — vitest anti-pattern occurs because prose rule is buried; SKILL.md with explicit `anti-trigger: "never run vitest directly from main thread"` makes it visible pre-execution | None | **GRAFT** | 5/5 |
| 2 | **Compound step / session learning artifact** (CP6 / axis-L) | Compound-Engineering P1, ECC P2, Ralph P2 | YES — file system is the only requirement | PARTIAL — Evolver does structural agent evolution, not session-level instinct capture | YES — fills axis-L partial gap; adds per-session tier on top of existing cross-cycle Evolver | New `docs/solutions/` dir under `uuuSanAI_GameMakerEngine/`; trigger: at end of each helper review cycle (`EngineHelper_Codex/docs/automatic_collaboration_loop.md`), emit one YAML-tagged `.md` lesson | Very low — purely additive; no existing code touched | HIGH — prevents same failure (e.g., path migration, zero-task materialization) from being re-surfaced in each helper cycle without context | Primitive #1 (SKILL.md) unlocks clean trigger point | **GRAFT** | 4/5 |
| 3 | **`{PHASE}-{WAVE}-{TYPE}` artifact naming** (axis-H / GSD G2) | GSD G2 | YES — Monitor already uses `*_handoff.md` files | NO — Monitor state files are ad-hoc named (`monitor_brief.md`, `next_work_brief.md`, `operator_report.md`, etc.) | YES — directly addresses axis-H partial gap; makes 6+ Monitor state files navigable by encoding role in name | Rename/alias files in `CollabMonitor_Codex/state/`; update references in `CollabMonitor_Codex/CLAUDE.md`; establish convention in `state/state_digest.md` header | LOW — filenames only; content unchanged; must update any grep/read references in CLAUDE.md | MED — reduces the debug time when Monitor state is stale (Pain Points 5 & 6): operator can immediately tell which file is stale by filename without reading all 6 | None | **GRAFT** | 4/5 |
| 4 | **"Pushy" skill description with anti-trigger tests** (revfactory P4) | revfactory P4 | YES | NO | YES — precision trigger engineering reduces the "vague proceed = blocking consent" problem (axis-D partial gap) | Inside any new SKILL.md files created by Primitive #1; also update description of any future Monitor action skills | Very low — description text only | MED — prevents Monitor from triggering the wrong delegation path; observable via operator review of trigger precision over 5 cycles | Primitive #1 | **GRAFT** (fold into #1 rollout) | 5/5 |
| 5 | **Role-specialized review subagent** (CP5 / axis-K) | gstack P1, ECC P4, CE P4, Ouroboros P7 | YES — Engine already has worktree-level agent delegation | PARTIAL — 7 departments are named but not enforced as scoped execution surfaces | YES — fills axis-K partial gap; gives explicit department-scoped review surfaces | New `uuuSanAI_GameMaker/.claude/agents/` files per department (Design, QA, Programming at minimum); invoke from `GameMaker/CLAUDE.md` agent delegation paths | MED — GameMaker director is unbuilt (Pain Point 4); this would land in a partially unbuilt subsystem | HIGH (once Director is built) — prevents generalist LLM behavior in department reviews | Primitive #1; GameMaker Director component must exist | **DEFER** — wait until Director is built | 3/5 |
| 6 | **Typed gate enum / HARD-GATE syntax** (axis-D upgrade, Superpowers P8) | Superpowers P8 | YES | PARTIAL — preflight gate exists as prose prose; numeric gate for cycle count; no typed enum | YES — closes "vague proceed = blocking consent" failure | `CollabMonitor_Codex/CLAUDE.md:39-40` — formalize the 4 action types (`engine-self-progress / engine-helper-followup / helper-review / pause`) as a typed enum with explicit HARD-GATE markers for blocking actions | LOW — prose extension only; no runtime change | MED — prevents Monitor from silently treating a soft suggestion as blocking consent | None | **GRAFT** | 4/5 |
| 7 | **`.planning/` structured spec directory** (GSD G1) | GSD G1 | YES | PARTIAL — Monitor already uses `state/` with role-separated files but without formal taxonomy | PARTIAL — would formalize what P3 (artifact naming) starts | Add `state/` sub-taxonomy: `state/BRIEF.md`, `state/DIGEST.md`, `state/NORTH_STAR.md`, `state/MEMORY.md`, `state/REPORT.md` — aligning to GSD's PROJECT/STATE/CONTEXT/RESEARCH pattern | LOW | LOW — already functionally covered by P2 (structured state directory); benefit is primarily cosmetic | Primitive #3 | **PARTIAL** — absorb into #3 rollout as naming convention choice | 3/5 |
| 8 | **Wave-parallel subagent execution** (GSD G5, D1 "spatial branching") | GSD G4+G5, Superpowers P5, CE P4 | YES | PARTIAL — worktree subagent exists (P3) but GameMaker phases run sequentially | YES — addresses D1 gap; would allow parallel department execution in GameMaker phases | `uuuSanAI_GameMaker/CLAUDE.md` + `GameMaker/docs/00_system_overview.md:42-61`; requires Director component as orchestrator | HIGH — Director is unbuilt; parallelism introduces coordination surface | HIGH (potential) — 7 departments parallelized could dramatically accelerate phase completion | GameMaker Director must be built first | **DEFER** — depends on Director | 2/5 |
| 9 | **Allowed-tools frontmatter per phase** (GSD G8, DV1 least-privilege) | GSD G8, gstack P6 | YES — Claude Code SKILL.md supports `allowed-tools:` | NO | YES — would formalize permission model for delegation skill | Inside skill files created by Primitive #1; add `allowed-tools:` frontmatter to each delegation skill | Very low | MED — prevents main thread from accidentally invoking a tool that should only run in worktree | Primitive #1 | **GRAFT** (fold into #1 rollout) | 5/5 |
| 10 | **Phase-0 state audit before execution** (revfactory P2) | revfactory P2 | YES | PARTIAL — Monitor already reads state files before deciding; no formal 3-way branch (new/extend/maintain) | PARTIAL — would make Monitor's opening assessment more systematic | `CollabMonitor_Codex/CLAUDE.md:13-15` — add explicit 3-way branch: first-run / active-task-extend / steady-state-maintain | LOW | MED — reduces the "identical recommendation across cycles" failure (Pain Point 5 low efficacy) | None | **GRAFT** | 4/5 |
| 11 | **Compound step: CLAUDE.md as living system spec** (CE P5) | Compound-Engineering P5 | YES | PARTIAL — `CollabMonitor_Codex/CLAUDE.md` has P10 (rule-persistence discipline) which is the same principle | ALREADY-PRESENT as principle; not as regular update ritual | Reinforce P10 discipline in `CollabMonitor_Codex/CLAUDE.md`: add explicit "update this file at session end with any new anti-patterns discovered" instruction | Very low | LOW — already present in principle | None | **ALREADY-PRESENT** (P10 is this primitive) | — |
| 12 | **Meta-skill bootstrapper** (revfactory P1 / axis-M) | revfactory P1 | PARTIAL — system has 6 sub-projects, high complexity; bootstrapper would generate SKILL.md files automatically | NO | YES — would address the missing SKILL.md gap at scale | New `.claude/skills/bootstrap-skills.md` at repo root level | MED — risk of generating inconsistent skill files that conflict with existing CLAUDE.md prose | HIGH (if correct) — all 6 sub-projects get SKILL.md coverage from one run | Primitive #1 must be manually piloted first | **DEFER** — pilot manual SKILL.md first; bootstrap after pattern is validated | 3/5 |
| 13 | **Instinct-confidence learning loop** (ECC P2 / axis-L full automation) | ECC P2 | PARTIAL — concept yes; ECC's 5-layer observer loop is ECC-specific | NO | YES — would give automated per-session instinct promotion | `EngineHelper_Codex/` session adapter would need to track pattern frequency; emit to instinct store | HIGH — ECC's observer loop is a black box; automated promotion risks instinct store corruption | Uncertain — benefit depends on observer quality | Primitive #2 (simpler manual version) | **REJECT** — use manual Compound step (Primitive #2) instead; ECC's confidence scoring function is unpublished and the automation risk outweighs the benefit |
| 14 | **`--dangerously-skip-permissions` YOLO mode** (Ralph, CE) | Ralph, Compound-Engineering DV1 | NO — GameMaker is an AI-driven game studio with MCP and PowerShell; unrestricted permissions in this context is actively dangerous | — | NO | — | HIGH — "Hook-brick" failure mode directly documented in synthesis | NEGATIVE | — | **REJECT** — explicit failure cases documented; system already uses bounded least-privilege (P5 cycle-count consent, P6 preflight gate) |
| 15 | **EventStore / MCP-based state persistence** (Ouroboros, axis-J) | Ouroboros | NO — Monitor state is file-based and working; Bridge is already a file-based protocol; EventStore adds operational complexity | — | NO | — | HIGH — would require replacing the working Bridge + Monitor state model | — | — | **REJECT** — files are working and the system has 604-minute snapshot staleness (Pain Point 6); adding an EventStore layer now would worsen the active debugging problem |
| 16 | **Dialectic Rhythm Guard / numeric ambiguity gate** (Ouroboros, axis-I) | Ouroboros | PARTIAL — concept applicable; but measurement function is a black box | NO | PARTIAL — would provide quantified confidence threshold for Monitor's action gate | Would sit in `CollabMonitor_Codex/CLAUDE.md` action-gate logic | MED — ambiguity score measurement is opaque; risk of false confidence | Uncertain | None | **REJECT** — cannot confirm the graft worked without a transparent measurement function; downgrade to typed enum (Primitive #6) instead |
| 17 | **Fresh context per iteration (bash while-loop)** (Ralph P1) | Ralph P1 | PARTIAL — Engine already runs bounded cycles; Monitor already resets between sessions | ALREADY-PRESENT — Monitor's session-reset + Engine's bounded cycles already implement this | — | — | — | — | — | **ALREADY-PRESENT** |
| 18 | **`/lfg` end-to-end autonomous pipeline** (CE P6) | Compound-Engineering P6 | NO — GameMaker has a 5-phase pipeline with explicit HITL gates (P6 preflight); an autonomous pipeline would bypass those gates | — | NO | — | HIGH — would bypass existing consent gates | — | — | **REJECT** — the project's preflight gate discipline (P6) is load-bearing; an autonomous end-to-end pipeline contradicts it |

---

## Ranked rollout plan

### 1. SKILL.md convention for delegation protocol + allowed-tools + "pushy" description (Primitives #1, #4, #9)

**Why first**: This is the single highest-leverage primitive with the lowest risk. The vitest re-run anti-pattern (Pain Point 8) and the vague delegation protocol (axis-F gap) are recurring behavioral traps documented in two CLAUDE.md files. Converting prose rules to SKILL.md with anti-trigger tests is a pure-additive operation — no code changes, no new dependencies.

**Implementation steps**:
1. Create `uuuSanAI_GameMakerEngine/.claude/skills/` directory.
2. Extract the 3-step delegation protocol from `GameMakerEngine/CLAUDE.md:82-97` into `skills/delegate-implementation.md` with YAML frontmatter: `name: delegate-implementation`, `description: (pushy, with anti-trigger: never invoke vitest directly from main session)`, `allowed-tools: [Task, Read]`, body = the 3 protocol steps.
3. Repeat for `uuuSanAI_GameMaker/.claude/skills/delegate-implementation.md` from `GameMaker/CLAUDE.md:43-62`.
4. Update both CLAUDE.md files to reference the skill instead of repeating the prose.

**Confirmation signal**: Over the next 3 helper-review cycles, zero occurrences of the vitest re-run pattern in operator reports. If the anti-trigger is effective, the Monitor's operator report will not flag the vitest anti-pattern again.

**Rollback plan**: Prose rules remain in CLAUDE.md. If SKILL.md causes confusion, delete the skill files and revert to prose-only.

---

### 2. Typed gate enum / HARD-GATE markers in Monitor (Primitive #6)

**Why second**: The Monitor's 4-action dispatch already exists; this graft adds typed markers to make the existing prose gate auditable. It directly prevents the "vague proceed = blocking consent" failure and is a 5-line prose extension.

**Implementation steps**:
1. In `CollabMonitor_Codex/CLAUDE.md:17-22`, replace the prose action list with a typed enum:
   ```
   ACTION_TYPES:
     - engine-self-progress   [NON-BLOCKING, can proceed without consent]
     - engine-helper-followup [NON-BLOCKING, can proceed without consent]
     - helper-review          [NON-BLOCKING, can proceed without consent]
     - human-review           [HARD-GATE: requires explicit operator confirmation before proceeding]
     - pause                  [DEFAULT when utility is low or snapshot is stale]
   ```
2. Add a rule: "When emitting a HARD-GATE action, write the gate marker verbatim in the operator response before taking any action."
3. Update `CollabMonitor_Codex/CLAUDE.md:39-40` preflight gate rule to reference the typed enum.

**Confirmation signal**: The next time Monitor recommends `human-review`, the operator report contains the explicit HARD-GATE marker and does not proceed until confirmed. Verifiable in next `state/operator_report.md`.

**Rollback plan**: Revert the two CLAUDE.md lines. No state files are touched.

---

### 3. Artifact naming convention for Monitor state files (Primitive #3)

**Why third**: The Monitor has 6+ state files with ad-hoc names. This graft makes lifecycle state readable from filenames without opening files — critical when snapshot is stale (Pain Points 5, 6).

**Implementation steps**:
1. Establish the naming convention in `CollabMonitor_Codex/state/state_digest.md` header section:
   ```
   Naming convention: {ROLE}-{LIFECYCLE}.md
   Roles: brief (snapshot), digest (full state), north_star (goal), memory (operator history),
          report (operator output), next (pending work), handoff (task boundary)
   Lifecycle suffixes: _active, _stale_NNNmin, _pending
   ```
2. Update references in `CollabMonitor_Codex/CLAUDE.md` to acknowledge the naming schema.
3. Do NOT rename existing files in this step — add the convention as a forward-only standard for new state files.

**Confirmation signal**: New state files created in the next 2 Monitor cycles follow the naming convention. An operator looking at the `state/` directory can identify the stale vs. active files without reading any file.

**Rollback plan**: Remove the convention note from state_digest.md header. Zero existing files are renamed.

---

### 4. Phase-0 state audit (3-way branch) in Monitor (Primitive #10)

**Why fourth**: The Monitor's opening assessment is already "reads state files → decides action" (P2). Adding an explicit 3-way branch (first-run / active-task-extend / steady-state-maintain) makes the assessment logic auditable and prevents the "same recommendation across cycles" failure (Pain Point 5: low helper efficacy).

**Implementation steps**:
1. In `CollabMonitor_Codex/CLAUDE.md:13-15`, augment the opening read protocol with:
   ```
   Phase-0: Before recommending any action, classify the current session as one of:
     A. FIRST-RUN: No prior state files; initialize state directory.
     B. ACTIVE-EXTEND: Existing task in-progress; extend without duplicating prior work.
     C. STEADY-STATE: No new snapshot since last cycle; default to pause unless explicit operator directive.
   ```
2. Add: "State the classification in the first line of any operator response."

**Confirmation signal**: Over the next 3 Monitor assessments, each operator report opens with the Phase-0 classification. The `helper_efficacy: low` metric (Pain Point 5) should improve as STEADY-STATE classification prevents low-value helper-review recommendations.

**Rollback plan**: Remove the 4-line addition from CLAUDE.md. No structural change.

---

### 5. Compound step — session learning artifact in Helper (Primitive #2)

**Why fifth**: This is the most consequential structural addition but also the one with the most dependencies. It should land after the SKILL.md and Monitor gate improvements are stable (primitives #1–#4), because those create the clean session boundaries that the Compound step needs to hook into.

**Implementation steps**:
1. Create `uuuSanAI_GameMakerEngineHelper_Codex/docs/solutions/` directory.
2. Add a `README.md` in that directory defining the YAML frontmatter schema:
   ```yaml
   ---
   date: YYYY-MM-DD
   category: [bug-fix | anti-pattern | path-issue | protocol-gap]
   trigger: <what failure or observation prompted this entry>
   applies_to: [engine | helper | monitor | gamemaker | bridge]
   resolved: true|false
   ---
   ```
3. In `EngineHelper_Codex/docs/automatic_collaboration_loop.md`, at the end of the Helper cycle description (around line 229), add: "Before switching to steady-state, write one `docs/solutions/` entry for any new failure mode observed or resolved in this cycle."
4. In `CollabMonitor_Codex/CLAUDE.md`, add: "When generating the operator report, scan `EngineHelper_Codex/docs/solutions/` for unresolved entries and include a 1-line summary of open learnings."

**Confirmation signal**: After 3 helper cycles, `docs/solutions/` contains at least 2 entries. The path migration issue (Pain Point 1) has an entry tagged `category: path-issue, resolved: false`. The Monitor operator report mentions the unresolved entry — demonstrating the feedback loop closes.

**Rollback plan**: Delete `docs/solutions/` directory. No existing files modified.

---

## Quick wins (try in one session, low risk)

These three can be done in a single focused session without risk of disrupting any running loop:

1. **Typed gate enum in Monitor CLAUDE.md** (Primitive #6) — 5-line edit to `CollabMonitor_Codex/CLAUDE.md`. Immediately auditable. No state touched.
2. **Phase-0 state audit** (Primitive #10) — 4-line addition to `CollabMonitor_Codex/CLAUDE.md`. Observable in next Monitor run.
3. **SKILL.md for vitest anti-pattern** (Primitive #1, scoped to just the anti-trigger) — Create one skill file `GameMakerEngine/.claude/skills/delegate-implementation.md` with the vitest anti-trigger. Takes 15 minutes.

All three target `CollabMonitor_Codex/CLAUDE.md` and `GameMakerEngine/CLAUDE.md` — the two highest-leverage files with the most documented behavioral traps.

---

## Explicitly rejected

These primitives look appealing on the surface but should NOT be grafted:

| Primitive | Why rejected |
|---|---|
| **`--dangerously-skip-permissions` / YOLO mode** | The project uses bounded consent gates (P5, P6) as load-bearing safety primitives. The "Hook-brick" failure (state file deletion by an Anthropic plugin) is documented in the research. GameMaker's MCP-connected Unreal Editor makes unrestricted permissions actively dangerous. Adding YOLO mode would silently bypass the entire preflight gate protocol. |
| **ECC instinct-confidence loop (full automation)** | ECC's 5-layer observer loop and confidence scoring function are proprietary and opaque. Instinct promotion without a transparent scoring function creates an undebuggable hidden layer on top of an already-complex state machine. The manual Compound step (Primitive #2) gives 80% of the benefit at 10% of the risk. |
| **Ouroboros EventStore / MCP-based state** | Bridge is already a working file-based protocol. The active system has a 604-minute snapshot staleness problem (Pain Point 6) that needs to be diagnosed, not covered with an event replay layer. Replacing files with an EventStore would add operational complexity at exactly the moment the team is trying to stabilize a broken path migration. |
| **`/lfg` autonomous end-to-end pipeline** | GameMaker's preflight gate (P6) is the single most important safety primitive in the system — it prevents the Monitor from running blocking operations without human consent. An autonomous `/lfg`-style pipeline bypasses it by design. The benefit (speed) is outweighed by the cost (consent gate destruction). |
| **Numeric ambiguity gate (Ouroboros axis-I)** | The measurement function for ambiguity scoring is not published. A numeric gate without a transparent measurement function gives false confidence that a hard gate is being enforced. The typed enum gate (Primitive #6) achieves the same "unambiguous proceed/block" semantics without a black-box score. |

---

## Open questions for the user

1. **SKILL.md runtime behavior**: Do the Claude Code sessions running `CollabMonitor_Codex` and `GameMakerEngine` auto-discover `.claude/skills/` files? Or must skills be explicitly referenced in CLAUDE.md? The rollout of Primitive #1 depends on this.

2. **`docs/solutions/` ownership**: Should the Compound step learning artifact live in `EngineHelper_Codex/` (as proposed) or in a shared location accessible to both Engine and Monitor? If the Monitor should also learn from it, a `bridge/solutions/` path would be more visible.

3. **Monitor CLAUDE.md edit authority**: The `CollabMonitor_Codex/CLAUDE.md` has a rule (P10) that any new rule must be written in the same turn it is identified. If the user edits it manually (e.g., to add the typed gate enum), does that satisfy P10 or does P10 require the agent itself to write the rule? Clarify before rollout of Primitives #6 and #10.

4. **Director prerequisite**: Primitives #5 (role-specialized review) and #8 (wave-parallel execution) are both blocked by the unbuilt GameMaker Director component. Is there a timeline or priority for building Director? If yes, add Primitive #5 to the post-Director roadmap explicitly.
