# Agent Roster

Project-local Claude Code subagents under `.claude/agents/`. Six roles total: two coordinator/worker pairs, one cross-joiner, and one writer. **Flexible axis schema is shared across the analysis agents** via `meta/harness_schema.md`.

## Architecture shape

```
user
  │
  ├──► harness-analyzer (coordinator, Phase 1+)
  │       │
  │       ├──► harness-probe  (worker: primary source reading)
  │       ├──► harness-probe  (...)
  │       └──► codex:rescue   (worker: second-opinion / deep code reasoning)
  │
  ├──► project-analyzer (coordinator, Phase 2 only)
  │       │
  │       ├──► project-probe  (worker: read-only code inspection)
  │       ├──► project-probe  (...)
  │       └──► codex:rescue   (worker)
  │
  ├──► graft-evaluator (Phase 2 only)
  │       │
  │       └── joins one harness note × one project map
  │
  └──► explainer-writer (post-analysis)
          │
          └── reads one finalized harness note → writes explainers/<slug>.md
```

## Design principles

1. **Coordinators don't read sources.** They plan, dispatch, integrate, decide convergence. This prevents one agent from carrying the whole analysis in its own context window and keeps each reading tightly scoped.
2. **Divide-and-conquer → consolidate → divide-and-conquer.** Every cycle: plan round → parallel probes → integrate findings → schema review → convergence check. Repeat until saturated. Round budget is a hard stop.
3. **Flexible schema.** `meta/harness_schema.md` is a seed, not a cage. Each analysis records its own axis list; global promotion is deliberate, not automatic.
4. **Phase gating.** `project-analyzer` and `graft-evaluator` are Phase-2 only to keep Phase 1 external research unbiased by the user's own code.
5. **Codex as a peer worker, not a chained layer.** Coordinator routes individual probes to `codex:rescue` when they benefit from deep code reasoning or a second opinion. Never put Codex inside a subagent's subagent — orchestrator loses visibility.

## The five agents

### `harness-analyzer` (coordinator) — Phase 1+
Entry point for "deep-dive harness X". Runs the divide-and-conquer cycle. Reads `meta/harness_schema.md` and `_collected_facts_*.md` only. Writes scratch dossier at `notes/harness/.wip/<slug>.md`, final note at `notes/harness/<slug>.md`. May propose schema deltas to `meta/harness_schema.md` under "Candidate additions".

### `harness-probe` (worker) — Phase 1+
Answers one narrow question by reading primary sources (blog posts, repos, READMEs, command files). Returns structured YAML with verbatim evidence quote, source URL, confidence, new_unknowns. Never writes to disk. Invoked in parallel batches by the coordinator.

### `project-analyzer` (coordinator) — Phase 2 only
Symmetric to harness-analyzer, applied to user's own project. Phase gate: stops immediately if invoked during Phase 1 without explicit user request. Writes scratch at `insights/.wip/`, final map at `insights/project_map_<slug>.md`.

### `project-probe` (worker) — Phase 2 only
Symmetric to harness-probe, applied to user's code. Read-only Bash (`ls`, `wc`, `git log`, `stat`). Returns structured YAML with `path:line` citations and `[observed]`/`[inferred]` tags. Redacts secrets.

### `graft-evaluator` — Phase 2 only
Joins one harness note with one project map. Ranks transferable primitives by fit, names insertion points, rejects primitives that shouldn't be grafted, defines confirmation signals for each GRAFT verdict. Writes to `insights/graft_<harness>_to_<project>.md`.

### `explainer-writer` — post-analysis
Turns a finalized harness note into a Korean narrative explainer (~8-min read) at `explainers/<slug>.md`. Reads only the note, collected_facts, and existing explainers (for tonal consistency) — no web access, no new research. Invoked by the orchestrator after `harness-analyzer` converges. Keeps the analysis context out of the main window so long explainer drafting doesn't burn orchestrator context.

## Convergence criteria (shared)

A coordinator stops iterating when:
- No unknowns remain at priority ≥ medium, OR
- Two consecutive rounds produced no new findings or new unknowns (saturation), OR
- Round budget reached (harness: 6, project: 5)

If the budget is hit with unresolved high-priority unknowns, the coordinator finalizes anyway with `confidence: low` on those axes, and records them in the note's "Open questions" section.

## Codex routing heuristics

Use `Skill(codex:rescue)` as a probe worker when:
- Subject has dense internal code worth a deep second read
- First probe return is suspicious, thin, or contradicts another source
- Subject is in a language or framework Claude tends to underperform on
- Two coordinator-level rounds both returned `confidence: low` on the same axis — second model may break the tie

Codex returns are integrated identically to probe returns — the coordinator doesn't care which model produced them.

## Status
- [x] v2 architecture: coordinator + worker split, flexible schema, Codex routing
- [x] First harness calibration run: **Ralph Wiggum** (2026-04-13) — converged in 1 round with 4 parallel probes, high confidence on axes 1–10, §11 yielded 12 transferable primitives + 1 explicit rejection. Proposed 3 schema candidate additions.
- [ ] Schema v2 bump decision (wait until ≥2 analyses complete — at least 1 more subject should independently use or reject the candidate axes)
- [ ] Phase 2 not yet opened
