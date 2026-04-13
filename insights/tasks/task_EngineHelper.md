---
project: uuuSanAI_GameMakerEngineHelper_Codex
path: D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMakerEngineHelper_Codex\
priority: medium
estimated_effort: half-day
---

# Improvement Tasks: uuuSanAI_GameMakerEngineHelper_Codex

## Context
EngineHelper reviews Engine and GameMaker state, emits bounded tasks, and cools down when no fresh snapshot is detected. The same failures (path migration, zero-task materialization) reappear across cycles without the system recording what it learned. Adding a `docs/solutions/` session-learning artifact — keyed to the Compound Engineering compound-step primitive — gives two-tier learning: per-session capture here, plus the existing cross-cycle Evolver. The Monitor can then surface unresolved entries in its operator report, closing the feedback loop.

## Task 1: Create `docs/solutions/` directory with YAML schema README
**Source primitive**: Compound-Engineering P1 / axis-L — compound step, session-level learning artifact
**Why**: The path migration gap (Pain Point 1) has been identified in multiple consecutive helper cycles without any session-level record of what was tried and why it failed. Without a persistent artifact, the helper re-discovers the same failure each cycle with no accumulated context.
**Insertion point**: `D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMakerEngineHelper_Codex\docs\solutions\` (new directory + README)
**Current state** (directory does not exist; confirmed by file listing showing only these docs):
```
docs/collaboration_protocol.md
docs/engine_onboarding.md
docs/monitor_agent.md
docs/automatic_collaboration_loop.md
```
**Target state** (new `docs/solutions/README.md`):
```markdown
# Solutions — Session Learning Artifacts

One entry per failure mode observed or resolved in a helper cycle.
Each entry is a `.md` file with the YAML frontmatter below.

## Frontmatter schema

---
date: YYYY-MM-DD
category: bug-fix | anti-pattern | path-issue | protocol-gap | config-issue
trigger: <what failure or observation prompted this entry — 1 sentence>
applies_to: engine | helper | monitor | gamemaker | bridge | multi
resolved: true | false
resolution_summary: <if resolved: true, 1-sentence description of what fixed it>
---

## Body

Free-form description of the failure, what was tried, and what the resolution was or why it remains open.

## Naming

Files: `YYYY-MM-DD-<slug>.md` (e.g., `2026-04-13-path-migration-bundle-gamemaker.md`)
```
**Acceptance criteria**:
- [ ] Directory `docs/solutions/` exists
- [ ] `docs/solutions/README.md` exists with the frontmatter schema block
- [ ] Schema contains at minimum: `date`, `category`, `trigger`, `applies_to`, `resolved`
- [ ] At least one seed entry is created for the path migration gap: `2026-04-13-path-migration-bundle-gamemaker.md` with `resolved: false`
**Dependencies**: none

## Task 2: Add solutions emit step to helper cycle documentation
**Source primitive**: Compound-Engineering P1 / axis-L — compound step triggered at iteration boundary
**Why**: The `docs/solutions/` directory is only useful if the helper actually writes to it. Documenting the emit step at the end of the helper cycle (after steady-state detection at line ~229 of `automatic_collaboration_loop.md`) creates the behavioral trigger that connects each cycle to the learning store.
**Insertion point**: `D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMakerEngineHelper_Codex\docs\automatic_collaboration_loop.md:229`
**Current state** (lines 221-229):
```
The helper now also cools down automatically when no fresh Engine snapshot or project fingerprint change is detected:

- `review_mode: steady-state`
- no new Engine follow-up task emission
- existing gaps stay visible, but with file hints and a "wait for fresh state" recommendation

When a fresh cycle does justify Engine follow-up work and the same Engine task is already open, the helper now refreshes that existing task instead of creating a duplicate.

Action items are now meant to be executable, not just descriptive.
```
**Target state** (insert after line 228, before "Action items are now meant to be executable"):
```markdown
## Session learning artifact (solutions emit)

Before switching to steady-state mode or closing a cycle, the helper should emit one `docs/solutions/` entry for any new failure mode observed or resolved in this cycle:

1. Check whether the failure already has an open entry in `docs/solutions/`.
2. If yes and it is now resolved: update `resolved: true` and add `resolution_summary`.
3. If yes and still open: do not create a duplicate — update `repeats` count in the body instead.
4. If no existing entry: create `docs/solutions/YYYY-MM-DD-<slug>.md` with the schema from `docs/solutions/README.md`.

This step runs even in steady-state mode — a steady-state cycle that finds the same open gap is itself evidence worth recording.
```
**Acceptance criteria**:
- [ ] The "Session learning artifact" section appears in `automatic_collaboration_loop.md` after line 228
- [ ] The section describes the 4-step check (existing entry / resolved / open repeat / new entry)
- [ ] After the next helper cycle, at least one file exists in `docs/solutions/`
**Dependencies**: Task 1 (directory and README must exist before this step can reference them)

## Task 3: Add Monitor cross-check rule for unresolved solutions
**Source primitive**: Compound-Engineering P1 + P5 — living system spec cross-referencing learning artifacts
**Why**: The `docs/solutions/` artifact is only actionable if the Monitor reads it. Adding one line to `CollabMonitor_Codex/CLAUDE.md` closes the feedback loop: Monitor operator reports will surface open unresolved entries, giving the human operator visibility into recurring failures without manually scanning the helper repo.
**Insertion point**: `D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMakerCollabMonitor_Codex\CLAUDE.md:50` (after the last guardrail bullet, before "## Preferred commands")
**Current state** (lines 49-54):
```
- if the monitor says `pause`, explain why before doing more work
- after running `ask-engine-*` actions, do not only report request ids or file paths; also summarize the Engine answer directly for the human with the key conclusion, recommended next action, and confidence when available

## Preferred commands
```
**Target state** (insert between lines 50 and 52):
```markdown
- when generating the operator report, scan `../uuuSanAI_GameMakerEngineHelper_Codex/docs/solutions/` for entries with `resolved: false`; include a 1-line summary of each unresolved entry in the operator report under "Open learnings"
```
**Acceptance criteria**:
- [ ] The `docs/solutions/` cross-check rule appears in `CollabMonitor_Codex/CLAUDE.md` before the `## Preferred commands` section
- [ ] Rule specifies the relative path `../uuuSanAI_GameMakerEngineHelper_Codex/docs/solutions/`
- [ ] Rule specifies the filter `resolved: false`
- [ ] Next Monitor operator report contains an "Open learnings" section listing at least the path migration entry
**Dependencies**: Task 1 (solutions directory must exist); Task 2 (at least one entry must exist for Monitor to find)
