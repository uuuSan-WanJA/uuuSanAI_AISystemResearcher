---
project: uuuSanAI_GameMakerCollabMonitor_Codex
path: D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMakerCollabMonitor_Codex\
priority: high
estimated_effort: quick-win
---

# Improvement Tasks: uuuSanAI_GameMakerCollabMonitor_Codex

## Context
CollabMonitor is the orchestration supervisor that decides whether Engine, Helper, or the human should act next. Its CLAUDE.md has 51 lines of dense prose guardrails but no typed enum for its 4 action types and no opening-assessment classification step. The result: "vague proceed = blocking consent" failures (Pain Point: CLAUDE.md:38) and repeated low-value helper-review recommendations when snapshots are stale (Pain Point 5: low helper_efficacy). Both fixes are pure prose additions — no code changes.

## Task 1: Add typed gate enum with HARD-GATE markers to action dispatch section
**Source primitive**: Superpowers P8 / axis-D — typed gate enum, explicit HARD-GATE syntax
**Why**: CLAUDE.md:38 explicitly prohibits treating vague prompts as blocking consent, but the 4 action types (lines 17-22) are still plain prose. Promoting them to a typed enum with explicit `[HARD-GATE]` vs `[NON-BLOCKING]` markers makes the consent boundary machine-readable and prevents Monitor from silently treating a soft suggestion as an approved blocking action.
**Insertion point**: `D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMakerCollabMonitor_Codex\CLAUDE.md:17-22`
**Current state** (lines 17-22):
```
- trigger `engine-self-progress` when Engine should choose the next bounded milestone step itself
- trigger `engine-helper-followup` when a Helper-raised Engine task is the best next bounded move
- trigger `helper-review` when Engine has changed or failed and Helper has not yet reviewed it
- escalate to the human when the monitor recommends `human-review`
```
**Target state**:
```markdown
ACTION_TYPES (replace the four bullet lines above):
  - `engine-self-progress`    [NON-BLOCKING — may proceed without explicit consent]
  - `engine-helper-followup`  [NON-BLOCKING — may proceed without explicit consent]
  - `helper-review`           [NON-BLOCKING — may proceed without explicit consent]
  - `human-review`            [HARD-GATE — write "HARD-GATE: human-review required" verbatim in operator response; do not proceed until human confirms]
  - `pause`                   [DEFAULT — when utility is low, snapshot is stale, or no action type clearly fits]

Rule: when emitting a HARD-GATE action, the gate marker must appear as the first line of the operator response before any other content.
```
**Acceptance criteria**:
- [ ] Lines 17-22 of `CLAUDE.md` now contain the `ACTION_TYPES` block with `[NON-BLOCKING]` and `[HARD-GATE]` markers
- [ ] The string `HARD-GATE` appears in the file
- [ ] The existing preflight gate rule at line 39 is updated to reference the typed enum: add "see ACTION_TYPES above for the blocking/non-blocking classification"
**Dependencies**: none

## Task 2: Add Phase-0 session classification to opening read protocol
**Source primitive**: revfactory P2 — Phase-0 state audit before execution (3-way branch)
**Why**: Monitor reads `state/monitor_brief.md` first (lines 17-18), but makes no explicit classification before deciding action. This means STEADY-STATE sessions (stale snapshot, same gap as last cycle) can still trigger `helper-review` rather than `pause`, explaining the `helper_efficacy: low` pattern in Pain Point 5.
**Insertion point**: `D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMakerCollabMonitor_Codex\CLAUDE.md:13-15`
**Current state** (lines 13-15):
```
## Default priorities

- prefer reading `state/monitor_brief.md` and `state/monitor_snapshot.json` first
```
**Target state**:
```markdown
## Default priorities

- prefer reading `state/monitor_brief.md` and `state/monitor_snapshot.json` first
- **Phase-0 classification (mandatory before any action)**: after reading state files, classify the current session as exactly one of:
  - `FIRST-RUN`: no prior state files exist — initialize state directory
  - `ACTIVE-EXTEND`: an in-progress task exists with fresh snapshot since last cycle — extend without duplicating
  - `STEADY-STATE`: no new snapshot since last cycle, same gap as previous assessment — default to `pause` unless operator gives explicit directive
- State the Phase-0 classification on the first line of every operator response.
```
**Acceptance criteria**:
- [ ] Lines 13-15 of `CLAUDE.md` now include the Phase-0 classification block
- [ ] The three state names (`FIRST-RUN`, `ACTIVE-EXTEND`, `STEADY-STATE`) appear verbatim
- [ ] `STEADY-STATE → pause` logic is explicit in the file
- [ ] Over the next 3 Monitor sessions, each operator response opens with one of the three Phase-0 labels
**Dependencies**: none (standalone; can be done in the same edit as Task 1)

## Task 3: Add artifact naming convention to state_digest.md header
**Source primitive**: GSD G2 / axis-H — `{PHASE}-{WAVE}-{TYPE}` artifact naming protocol
**Why**: The `state/` directory has 6+ ad-hoc-named files (`monitor_brief.md`, `next_work_brief.md`, `operator_report.md`, etc.). When snapshots are stale (Pain Point 6: 604-minute staleness), an operator cannot tell which file is current without opening each one. Encoding lifecycle state in filenames makes staleness visible at a directory listing.
**Insertion point**: `D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMakerCollabMonitor_Codex\collab\state\monitor_brief.md` (header addition only — do NOT rename existing files)

Note: The state directory lives under `collab/state/` in this project (confirmed: `collab\state\monitor_brief.md` exists). The naming convention should be established as a forward-only standard for new files only.

**Current state** (top of `collab/state/monitor_brief.md` — the primary state file read first):
```
(read the file to get exact current header — insert convention block at top)
```
**Target state** (add block at very top of `collab/state/monitor_brief.md`):
```markdown
<!-- STATE FILE NAMING CONVENTION (forward-only — do not rename existing files)
  New state files should follow: {ROLE}-{LIFECYCLE}.md
  ROLE values: brief | digest | north_star | memory | report | next | handoff
  LIFECYCLE suffixes: _active | _stale_NNNmin | _pending
  Example: brief-stale_604min.md signals a stale brief without opening the file.
  Existing files keep their current names; apply convention to new files only.
-->
```
**Acceptance criteria**:
- [ ] The naming convention comment block appears at the top of `collab/state/monitor_brief.md`
- [ ] Convention defines at minimum: ROLE values and LIFECYCLE suffixes
- [ ] No existing state files are renamed
- [ ] The next new state file created in this directory uses the `{ROLE}-{LIFECYCLE}.md` pattern
**Dependencies**: none
