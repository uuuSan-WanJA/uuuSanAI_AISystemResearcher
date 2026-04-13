---
project: uuuSanAI_GameMaker
path: D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMaker\
priority: high
estimated_effort: quick-win
---

# Improvement Tasks: uuuSanAI_GameMaker

## Context
GameMaker is the commercial product that runs a 7-department AI workforce to generate Unreal Engine 5 game projects. Its CLAUDE.md contains the same delegation protocol and vitest re-run prohibition as GameMakerEngine, but has no SKILL.md structure to enforce them. The Director, Shared Infrastructure, Human Interface, and Engine Adapter components are not yet built (Pain Point 4), but the delegation harness that guards them should be in place before those components are constructed.

## Task 1: Create delegation SKILL.md with vitest anti-trigger
**Source primitive**: Superpowers P4 / axis-F — SKILL.md when-only skill description with anti-trigger
**Why**: The vitest full re-run prohibition (CLAUDE.md:57) is identical to the GameMakerEngine rule but lives in a garbled-encoding file with no SKILL.md enforcement surface. Creating the skill file gives the same pre-execution visibility as GameMakerEngine's version.
**Insertion point**: `D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMaker\.claude\skills\delegate-implementation.md` (new file)
**Current state** (from `CLAUDE.md:49-62`, encoding-garbled but semantically readable):
```
**2단계: 서브에이전트 팀 위임 (규모 기반 조건부)**
- 경량 작업 (파일 1~2개, 설정/문서 정정, 단순 버그 정정): 메인에서 직접 실행 허용
- 중량 작업 (파일 3개+, 로직 변경, 신규 기능): 구현 Agent(worktree) → 검증 Agent → 메인은 요약만 수신
- 서브에이전트 보고 형식: 200자 이내 요약 + PASS/FAIL + 수정 파일 목록 + 발견 문제
...
- **vitest 전체 재실행 금지** — 워크트리에서 동일 코드로 이미 통과했으므로 중복
```
**Target state** (new file `.claude/skills/delegate-implementation.md`):
```markdown
---
name: delegate-implementation
description: >
  Use for medium/heavy tasks (3+ files, logic changes, new features).
  Light tasks (1-2 files, config/doc edits, simple bug fix) may run on main directly.
  Delegates to worktree Implementation Agent → Validation Agent → main receives
  200-char summary + PASS/FAIL only.
  ANTI-TRIGGER: never invoke vitest directly from the main session thread —
  worktree already ran identical code; re-running is prohibited.
allowed-tools: [Task, Read]
---

## Protocol (medium/heavy tasks only)

1. **Implementation Agent** (worktree): single task, runs `tsc + vitest`. Returns: 200-char summary, PASS/FAIL, modified file list.
2. **Validation Agent**: APPROVE or REJECT with reason.
3. **Main session**: apply patch on APPROVE, run `tsc --noEmit` foreground, commit.

## Prohibited on main thread
- Direct coding or diff reading for medium/heavy tasks
- `vitest run` after worktree validation (any form)
- Detailed sub-agent result inspection on main (Validation Agent's job)
```
**Acceptance criteria**:
- [ ] File exists at `D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMaker\.claude\skills\delegate-implementation.md`
- [ ] Frontmatter contains `anti-trigger` text referencing vitest prohibition
- [ ] Frontmatter contains `allowed-tools: [Task, Read]`
- [ ] Light task exception (1-2 file direct execution) is preserved in the description
**Dependencies**: none

## Task 2: Fix CLAUDE.md encoding and add skill reference
**Source primitive**: Compound-Engineering P5 / axis-E — CLAUDE.md as living system spec, kept current
**Why**: The current `CLAUDE.md` is encoded incorrectly (garbled Korean UTF-8), making rules unreadable to agents that read it. This is the most critical maintenance blocker — any rule in the file is effectively invisible until the encoding is fixed.
**Insertion point**: `D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMaker\CLAUDE.md` (full file)
**Current state** (lines 1-5, representative sample):
```
# uuuSanAI GameMaker ??Project Memory

## ?�로?�트 개요
AI ?�이?�트가 게임??만드???�레?�워?? ?�매 ?�???�품.
GameMakerEngine??진화?�킨 ?�이?�트�?Bridge?�서 ?�신?�여 ?�행.
```
**Target state**:
- Re-save `CLAUDE.md` as UTF-8 without BOM (the display garbling is a BOM or encoding mismatch).
- After fixing, verify Korean text renders correctly (e.g., `프로젝트 개요` not `?�로?�트 개요`).
- Then append to the `### 핵심 개발 방법론` section: "구조화된 위임 스킬: `.claude/skills/delegate-implementation.md` 참조."
**Acceptance criteria**:
- [ ] `CLAUDE.md` re-read with Read tool shows Korean characters without `?` replacement characters
- [ ] File contains reference to `.claude/skills/delegate-implementation.md`
- [ ] `vitest 전체 재실행 금지` rule is still present and legible after encoding fix
**Dependencies**: Task 1 (skill file must exist before reference is added)
