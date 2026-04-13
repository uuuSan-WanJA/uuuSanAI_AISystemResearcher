---
project: uuuSanAI_GameMakerEngine
path: D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMakerEngine\
priority: high
estimated_effort: quick-win
---

# Improvement Tasks: uuuSanAI_GameMakerEngine

## Context
GameMakerEngine runs competitive Arena tournaments and Evolver mutations to produce better agents, publishing winners via Bridge. Two recurring behavioral traps are documented in CLAUDE.md: the vitest re-run anti-pattern (running vitest on the main thread after a worktree already ran it) and ad-hoc delegation protocol that exists only as buried prose. Converting these to a SKILL.md with explicit anti-triggers makes the rules auditable and pre-execution visible.

## Task 1: Create delegation SKILL.md with vitest anti-trigger
**Source primitive**: Superpowers P4 / axis-F — SKILL.md when-only skill description with anti-trigger test
**Why**: The vitest re-run prohibition (Pain Point 8) is buried in prose at CLAUDE.md:94-97. Every new session must re-read the full file to discover the rule. A SKILL.md with an explicit `anti-trigger` makes the prohibition visible before execution, not after.
**Insertion point**: `D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMakerEngine\.claude\skills\delegate-implementation.md` (new file)
**Current state** (from `CLAUDE.md:86-97`):
```
**2단계: 서브에이전트 팀 위임 (무조건 — 컨텍스트 보호 최우선)**
- 메인은 직접 코딩/diff 읽기/테스트 실행 안 함. 규모 무관.
- 구현 Agent(worktree) → 검증 Agent → 메인은 요약된 판정만 수신
- 서브에이전트 보고 형식: 200자 이내 요약 + PASS/FAIL + 수정 파일 목록 + 발견 문제

**3단계: 워크트리 결과 수령 (메인의 후처리)**
- 워크트리 Agent가 tsc+vitest 통과 보고 → 검증 Agent가 APPROVE → 메인은 패치 적용
- 패치 적용 후: `tsc --noEmit`만 foreground로 확인 → 커밋
- **vitest 전체 재실행 금지** — 워크트리에서 동일 코드로 이미 통과했으므로 중복
- 테스트가 불가피하면 반드시 foreground 실행 (background + polling 금지)
```
**Target state** (new file `.claude/skills/delegate-implementation.md`):
```markdown
---
name: delegate-implementation
description: >
  Use when implementing any non-trivial change (3+ files, logic change, new feature).
  Delegates to worktree Implementation Agent → Validation Agent → main receives 200-char
  summary + PASS/FAIL only. Main never reads code directly or runs tests itself.
  ANTI-TRIGGER: never invoke vitest directly from the main session thread —
  worktree already ran identical code; re-running duplicates work and violates
  context-protection protocol.
allowed-tools: [Task, Read]
---

## Protocol

1. **Implementation Agent** (worktree): receives task + context slice only. Runs `tsc + vitest`. Returns: 200-char summary, PASS/FAIL, modified file list, issues found.
2. **Validation Agent**: receives Implementation Agent output. Issues APPROVE or REJECT with reason.
3. **Main session**: receives APPROVE/REJECT only. If APPROVE, apply patch, run `tsc --noEmit` foreground, commit. No vitest re-run.

## Prohibited on main thread
- Direct coding or diff reading
- `vitest run` or `vitest` (any form) after worktree validation
- `background + polling` for tests — foreground only if unavoidable
```
**Acceptance criteria**:
- [ ] File exists at `D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMakerEngine\.claude\skills\delegate-implementation.md`
- [ ] File contains `anti-trigger` text referencing vitest prohibition
- [ ] File contains `allowed-tools: [Task, Read]` frontmatter
- [ ] `CLAUDE.md:86-97` prose block is updated to add: "See `.claude/skills/delegate-implementation.md` for the structured skill definition."
**Dependencies**: none

## Task 2: Add `allowed-tools` frontmatter to delegation skill (fold into Task 1 if done together)
**Source primitive**: GSD G8 / axis-G — `allowed-tools:` frontmatter per-phase permission declaration
**Why**: The Codex delegation protocol (CLAUDE.md:99-113) lists three agent types (Implementation, Validation, Exploration) with different tool access needs. Formalizing `allowed-tools` per agent type prevents the main thread from accidentally invoking a restricted tool.
**Insertion point**: `D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMakerEngine\.claude\skills\delegate-implementation.md` (same file as Task 1, extension)
**Current state** (from `CLAUDE.md:102-105`):
```
- **구현 Agent**: `/codex:rescue`로 코드 생성을 Codex에 위임. Claude는 오케스트레이션(파일 읽기, 컨텍스트 파악, 결과 검증)만 담당.
- **검증 Agent**: `/codex:review`로 코드 리뷰를 Codex에 위임. tsc/vitest 실행은 여전히 Claude.
- **탐색 Agent**: Codex 위임 불가 (Grep, Read 등 Claude 도구 접근 필수).
```
**Target state** (additions to the skill file body):
```markdown
## Agent tool access

| Agent role | Allowed tools | Codex delegation |
|---|---|---|
| Implementation Agent | Task, Write, Edit | `/codex:rescue` when routing.enabled |
| Validation Agent | Read, Bash (tsc/vitest only) | `/codex:review` when routing.enabled |
| Exploration Agent | Read, Grep, Glob | Never delegate to Codex |
| Main session | Task, Read | No implementation tools |
```
**Acceptance criteria**:
- [ ] Skill file includes an agent tool access table or equivalent structured section
- [ ] Main session row lists only `Task, Read` — no Write, Edit, Bash
- [ ] Exploration Agent row explicitly marks Codex delegation as prohibited
**Dependencies**: Task 1 (same file)

## Task 3: Add Phase-0 state audit (3-way branch) to CLAUDE.md opening protocol
**Source primitive**: revfactory P2 — Phase-0 state audit before execution (first-run / extend / maintain)
**Why**: The Engine currently starts each session without an explicit classification step, leading to the "identical recommendation across cycles" failure (Pain Point 5: low helper efficacy). An explicit 3-way classification at session start makes the opening assessment auditable and prevents low-value steady-state cycles from triggering engine work.
**Insertion point**: `D:\ClaudeCode\Projects\Bundle_GameMaker\uuuSanAI_GameMakerEngine\CLAUDE.md:81-82`
**Current state** (lines 81-82):
```
### 세션/테스트 절차
- 세션 시작: `git pull` + `git log --oneline -5`
```
**Target state**:
```markdown
### 세션/테스트 절차
- 세션 시작: `git pull` + `git log --oneline -5`
- **Phase-0 분류 (필수)**: 세션 첫 응답에 아래 세 가지 중 하나를 명시한다:
  - `FIRST-RUN`: 이전 상태 파일 없음 — 상태 디렉토리 초기화
  - `ACTIVE-EXTEND`: 진행 중 태스크 존재 — 중복 없이 연장
  - `STEADY-STATE`: 마지막 사이클 이후 새 스냅샷 없음 — 명시적 지시 없으면 pause
```
**Acceptance criteria**:
- [ ] Lines 81-82 of `CLAUDE.md` now include the Phase-0 classification block
- [ ] The three state names (`FIRST-RUN`, `ACTIVE-EXTEND`, `STEADY-STATE`) appear verbatim
- [ ] In the next Engine session, the operator response opens with one of these three classifications
**Dependencies**: none (standalone prose addition)
