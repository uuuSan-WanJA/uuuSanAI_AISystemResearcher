---
title: Superpowers
date: 2026-04-13
author: Jesse Vincent (obra, blog.fsck.com)
first_public: 2025-10-09
primary_source: https://blog.fsck.com/2025/10/09/superpowers/
topic: harness
tags: [harness, claude-code, plugin, skills, skill-md, tdd, subagent-driven, graphviz, hard-gate, obra, vincent]
status: deep-dive
confidence: high
rounds: 4
axes_used: [1,2,3,4,5,6,7,8,9,10,11,12]
axes_added: [gate_mechanism_syntax, authoritative_process_medium]
axes_dropped: []
candidate_axis_proposals: [gate_mechanism_syntax, authoritative_process_medium, skill_as_unit_of_discipline]
notes: |
  Dispatched via WebFetch/WebSearch in 4 rounds because Agent-dispatch tool was
  not available in this execution environment. All evidence cites primary sources
  (obra/superpowers repo, Jesse Vincent blog, marketplace PR) with secondary
  cross-checks (Medium, byteiota, heyuan110, deepwiki).
---

## TL;DR (3줄)
Superpowers는 Jesse Vincent가 2025-10-09 공개한 Claude Code **플러그인**으로, `SKILL.md` 파일 묶음 + 부트스트랩 시스템 프롬프트로 **brainstorm → spec → plan → TDD → subagent dev → review → finalize** 7단계 파이프라인을 에이전트에게 강제한다. 핵심 혁신은 (a) 스킬을 발견 가능·설명 가능·테스트 가능한 **자기완결 유닛**으로 표준화한 것, (b) `<HARD-GATE>` XML 태그와 **GraphViz DOT 플로우차트를 프로세스의 권위적 표현**으로 쓴 것, (c) 독립 컨텍스트 **서브에이전트로 구현·리뷰를 분리**한 것이다. 2026-01-15 Anthropic 공식 플러그인 마켓플레이스 등재 이후 150k+ 스타로 폭증, chardet 7.0 릴리스(41× 성능, 정확도 94.5→96.8%)가 대표 사례로 인용된다. v5.0.6(2026-03-24)에서 서브에이전트 리뷰가 비용 이슈로 **인라인 self-review로 되돌려진** 방향 전환이 실패 모드 및 설계 긴장 지점을 드러낸다.

## 1. Identity & provenance
- **Author**: Jesse Vincent (github: `obra`, blog: `blog.fsck.com`, Prime Radiant)
- **First public**: 2025-10-09 — `blog.fsck.com/2025/10/09/superpowers/` (레포 동일자 공개)
- **Direct ancestor**: 2025-10-05 Vincent 블로그 "How I'm using coding agents in September, 2025" — brainstorming/planning 프롬프트 원형
- **Current version**: v5.0.7 (2026-03-31)
- **Adoption**:
  - 150,000+ stars / 12,900+ forks (README 스냅샷, 2026-Q1)
  - 28+ 컨트리뷰터, 400+ 커밋
  - **2026-01-15 Anthropic 공식 마켓플레이스 등재** (`anthropics/claude-plugins-official` PR #148, by noahzweben)
  - 2026-03 기준 94,000 스타 돌파 후 3월말~4월 초 급등, 피크 시 일 2,000 스타
- **Language split**: Shell 58.8% / JS 29.6% / HTML 4.3% / Python 3.7% / TS 2.8% (README)
- **License**: MIT
- **Runtime coverage**: Claude Code (official), Cursor, Codex, OpenCode, GitHub Copilot CLI, Gemini CLI — 플러그인/마켓플레이스 배포

> "Superpowers is a complete software development workflow for your coding agents, built on top of a set of composable 'skills' and some initial instructions that make sure your agent uses them." — README

## 2. Problem framing
Vincent의 핵심 진단: vanilla Claude Code는 빠르지만 **모든 전문가 관행을 스킵**한다. 필요한 것은 "더 똑똑한 모델"이 아니라 **방법론을 강제하는 외곽 레이어**.

> "I've spent the past couple of weeks working on a set of tools to better extract and systematize my processes and to help better steer my agentic buddy." — Vincent, 2025-10-09

> "Skills are what give your agents Superpowers." — Vincent, 2025-10-09 (캡스톤 슬로건)

핵심 설계 가정(3자 관찰): "**Impose a strict development methodology and output quality stabilizes.**" (Ewan Mak, 2026-04). 즉 Superpowers는 **프로세스 디시플린을 제약으로 부과**하는 것이 본질이며, 컨텍스트 열화(GSD) 나 의사결정 거버넌스(OpenSpec/gstack) 가 아니다.

## 3. Control architecture
**7-페이즈 파이프라인을 DAG로 하드코딩한 하이브리드 워크플로.** 각 노드는 스킬 호출, 전이는 DOT 플로우차트로 명시. 워크플로(코드 경로)와 에이전트(LLM 자율)의 혼합: 페이즈 순서는 결정론, 페이즈 내부는 LLM 주도.

**7 페이즈** (README):
1. **Brainstorming** — 질문 기반 디자인 도출
2. **Using-git-worktrees** — 격리 작업공간
3. **Writing-plans** — 2–5분 단위 bite-sized 태스크
4. **Subagent-driven-development** — 구현은 독립 컨텍스트 서브에이전트
5. **Test-driven-development** — RED/GREEN/REFACTOR
6. **Requesting-code-review** — severity 기반 블로킹
7. **Finishing-a-development-branch** — merge/PR 결정

> "The agent checks for relevant skills before any task. Mandatory workflows, not suggestions." — README

**Anthropic 분류 매핑**: 외곽 파이프라인은 workflow(pre-wired code path), 각 스킬 내부의 구현 단계는 agent(LLM-directed). 명시적 **orchestrator–workers** 패턴: 코디네이터 세션이 서브에이전트에 isolated task를 dispatch. 루프는 리뷰 단계에만 존재("rerun code review after the implementer fixes the first code review" — Vincent, v4 post).

**Termination**: 각 페이즈는 HARD-GATE 통과 혹은 approval 시에만 진전. v5.0.4부터 "max review iterations 5→3" 으로 리뷰 루프 상한 도입.

## 4. State & context model
**디스크 기반 스펙/플랜 + 독립 서브에이전트 컨텍스트.** Ralph와 달리 한 세션 내 iteration이 아니라, 페이즈 간 **컨텍스트 자르기(carve-off)**가 핵심.

| 파일/경로 | 역할 | 작성자 | 비고 |
|---|---|---|---|
| `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` | 브레인스토밍 산출 디자인 스펙 | 코디네이터 세션 | v5.0.0부터 경로 표준화 |
| `docs/superpowers/plans/…` | 서브에이전트에 투입할 bite-sized 플랜 | 코디네이터 | 2–5분 태스크 단위 |
| `skills/*/SKILL.md` | 스킬 정의 (프로세스의 권위적 정의) | Superpowers 자체 + 사용자 | YAML frontmatter + DOT + 프로즈 |
| git worktree | 격리된 구현 브랜치 | subagent | using-git-worktrees 스킬 강제 |

**턴/페이즈 경계에서 모델이 보는 것**:
- **세션 부트스트랩**: SessionStart hook → `using-superpowers` meta-skill을 `<EXTREMELY_IMPORTANT>` 블록으로 **컨텍스트에 직접 삽입** (on-demand 아님). (DeepWiki)
- **스킬 호출**: 다른 스킬은 description 매칭 후 on-demand 로드.
- **서브에이전트 디스패치**: 상위 세션의 히스토리 **상속 없이** "exactly what they need" 만 받음.

> "The skill delegates tasks to specialized subagents with isolated context. Each receives 'exactly what they need' without inheriting session history." — subagent-driven-development SKILL.md (paraphrase)

**핵심 원칙**: 코디네이터 컨텍스트는 **오케스트레이션 용도로 보존**, 무거운 구현은 서브에이전트에 aus-lagern.

## 5. Prompt strategy
Superpowers의 프롬프트 전략은 **스킬 = 프로세스 문서 + XML 게이트 + DOT 플로우차트** 3각.

### 스킬 포맷 (표준)
```yaml
---
name: <hyphens-only>
description: Use when <trigger> — <one-line purpose, ≤500 chars>
---
```
본문은 **Overview → When to Use → Flowchart(DOT) → Core Process → HARD-GATE → Integration Points** 구조. (`writing-skills/SKILL.md` 템플릿 기반.)

### HARD-GATE (검증된 verbatim)
`brainstorming/SKILL.md`에 실제로 존재하는 태그:

> ```
> <HARD-GATE>
> Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it. This applies to EVERY project regardless of perceived simplicity.
> </HARD-GATE>
> ```

XML-스타일 앵글 브라켓 태그. `<SUBAGENT-STOP>` 등 변형도 존재("If you were dispatched as a subagent to execute a specific task, skip this skill." — DeepWiki).

### GraphViz DOT을 권위적 프로세스 표현으로
v4(2025-12-18) 에서 Vincent가 명시적으로 선언:

> "Superpowers is leaning more on the GraphViz 'dot' notation internally for process documentation... Claude is particularly good at following processes written in dot." — blog.fsck.com/2025/12/18/superpowers-4/

`brainstorming/SKILL.md`의 실제 DOT (verbatim 일부):
```dot
digraph brainstorming {
    "Explore project context" [shape=box];
    "Visual questions ahead?" [shape=diamond];
    ...
    "Invoke writing-plans skill" [shape=doublecircle];
    "User approves design?" -> "Present design sections" [label="no, revise"];
    "User approves design?" -> "Write design doc" [label="yes"];
    ...
}
```
— doublecircle가 **terminal state**, diamond가 decision point. 프로즈는 **DOT를 부연**하는 보조 역할.

### 각 스킬의 iron law (검증됨)
- **test-driven-development**: "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST" + "Delete any code written before its test exists."
- **brainstorming**: "'Simple' projects are where unexamined assumptions cause the most wasted work."
- **writing-skills**: "Writing skills IS Test-Driven Development applied to process documentation."

### Anti-rationalization 패턴
TDD 스킬은 "I'll test after", "Already manually tested", "Delete is wasteful", "Spirit not ritual" 4개 핑계에 대한 명시적 반박을 포함. Ralph의 CAPS-yelling과 다르게 **조용한 structured rebuttal**.

### 자기개선 (meta)
`writing-skills` 스킬 자체가 존재 — 사용자가 실패 관찰 후 새로운 스킬을 추가할 수 있게 함. Vincent:
> "One of the first skills I taught Superpowers was How to create skills... Claude put the pieces together." — 2025-10-09

### Description rule (v4)
v4에서 **스킬 description은 '언제 쓰는지'만** 포함하도록 재작성. "To prevent Claude from guessing functionality without reading details" — Vincent, 2025-12-18. **discovery와 body를 분리**하는 명시적 결정.

## 6. Tool surface & permission model
- **기본 Claude Code 퍼미션 모델을 상속**. Ralph의 `--dangerously-skip-permissions` 같은 글로벌 bypass 강제 없음.
- **SessionStart hook**으로 meta-skill을 자동 주입. hooks/는 리포 구조에 존재.
- **git worktree**: `using-git-worktrees` 스킬이 격리 작업공간을 강제 — 메인 브랜치 오염 방지.

> "Never start on main/master without explicit consent" — subagent-driven-development SKILL.md

- **마켓플레이스 배포**: `/plugin install superpowers@claude-plugins-official` — 플러그인 계약을 통해 툴 서피스가 **선언적**으로 정의됨. YOLO 스타일 아님.
- **Brainstorm server**: WebSocket 기반 "visual brainstorming companion" 이 v5.0.0에서 도입. v5.0.5에서 ESM 호환성 수정(`server.js → server.cjs`). 외부 프로세스와 상호작용.

## 7. Human-in-the-loop points
Ralph보다 HITL이 **내부 깊이 박혀 있음**. 최소 3개 명시적 approval 게이트:

1. **Design approval gate** — "User approves design?" (brainstorming DOT의 diamond)
2. **Spec review gate** — "User reviews spec?" (설계 문서 확정 전)
3. **Code review gate** — reviewer subagent가 severity-based 이슈를 raise, 코디네이터가 처리 결정

HARD-GATE는 사람의 approval을 **에이전트 진전의 전제조건**으로 엮는다. v5.0.6 회귀(인라인 리뷰)에서도 human gate는 유지. v5.0.5에서 "Restored user choice between subagent-driven and inline execution" — 사용자 선호가 실행 모델에 영향.

## 8. Composability
**플러그인 + 스킬** 두 레이어로 합성 가능:

| 합성 대상 | 방식 | 증거 |
|---|---|---|
| Cursor, Codex, OpenCode, Copilot CLI, Gemini CLI | 동일 스킬셋을 **런타임-애그노스틱**하게 재배포 | README 설치 섹션 |
| OpenSpec | Week 2 Superpowers + Week 3 OpenSpec 병용 권장 | heyuan110.com, Fission-AI/OpenSpec #780, #859 |
| GSD, gstack | **같은 문제를 다르게 제약** (프로세스 vs 환경 vs 거버넌스) — 직접 합성 사례 적음 | Ewan Mak, Medium 2026-04 |
| 사용자 커스텀 스킬 | `writing-skills` 스킬 경유 추가 | Vincent, 2025-10-09 |

> "Superpowers excels at execution quality. OpenSpec excels at decision traceability... bilingual is the right answer." — heyuan110.com, 2026-04-09

**런타임 이식성 비교**: Ralph는 bash 레이어 이식, Superpowers는 **플러그인 계약 + SKILL.md 포맷 이식**. 후자가 더 높은 abstraction.

## 9. Empirical claims & evidence
### Vincent 자신 주장
- "Claude went _hard_... it would strengthen the instructions... after each failure, ensuring future-Claude would actually search for skills." — pressure-testing 효과 (2025-10-09)
- v4 (2025-12-18): "basic end to end tests that make sure that the agent runs the full brainstorming - planning - implementing flow" — **자체 e2e 테스트 인프라 존재**

### 3자 정량 주장
- **chardet 7.0.0** (2026-03-04 릴리스, 저자 Vincent 본인): **41× 성능 개선, 정확도 94.5% → 96.8%** (byteiota; LinkedIn posts 인용)
- **"Test coverage jumps to 85-95%"** — 프레임워크가 테스트 스킵을 원천 차단 (byteiota)
- **"4 people × 6 months 프로젝트를 1인 2개월"** — 한 개발자 사례 (byteiota, 출처 불명확)

### 3자 질적 관찰
- "The pipeline makes autonomous multi-hour sessions viable. Claude works through each task, reviews its own output against the plan." — Ewan Mak, Medium 2026-04
- "Mandatory test-driven development. Other frameworks suggest testing. Superpowers deletes code written before tests exist." — Ewan Mak

### 증거 유형
벤치마크는 여전히 일화 + 자기보고 + 자기개발 라이브러리(chardet). 통제된 비교 실험 없음. **byteiota와 Medium critiques가 가장 실질적인 3자 신호**. Ralph와 유사한 증거 패턴이되 chardet 같은 **실물 납품 아티팩트**가 질적으로 더 강함.

## 10. Failure modes & limits
### 저자 자인 (로드맵 reversal)
- **v5.0.6 인라인 리뷰 회귀 (2026-03-24)**: "Inline Self-Review Replaces Subagent Review Loops — removed expensive review delegation in favor of integrated checklists." → **서브에이전트 리뷰 비용이 감당 불가**했다는 실질적 자인.
- **v5.0.4 루프 상한 하향 (2026-03-16)**: max review iterations 5 → 3, "Raised calibration bar for blocking issues" → 리뷰어가 지나치게 블로킹하는 경향 보정.
- **v5.0.5 user choice 복원**: 서브에이전트 강제가 사용자 환경에 따라 비용/지연 이슈 발생, 인라인/서브에이전트 **둘 다 선택지로 유지**.

### 3자 관찰
- **"Superpowers' interactive prompts blocking Claude Code's input stream."** — 다른 프레임워크와 합성 시 실패 모드 (Ewan Mak, Medium)
- **강제된 TDD가 개발 속도를 실제로 늦추는지**, 혹은 프로젝트가 프레임워크를 버리는 사례는 byteiota 기사에서는 **의도적으로 누락** — 긍정 bias 경고.
- **Brainstorm server Windows/MSYS2 불안정** → v5.0.5에서 Owner-PID 모니터링 Windows 비활성화. 크로스 플랫폼 성숙도 이슈.
- **ESM/CJS 호환성**: server.js → server.cjs 개명 (v5.0.5) — JS 에코시스템 파편화에 노출.

### 설계 긴장
- **스킬 수 폭발** 위험: v4에서 이미 "consolidate skills" 결정(test-driven-development가 testing-anti-patterns 흡수, systematic-debugging이 root-cause-tracing + defense-in-depth + condition-based-waiting 흡수).
- **Claude-specificity**: "Claude is particularly good at following processes written in dot" — 다른 모델에서 DOT 준수도 unverified.

### 아직 시험되지 않은 것
- 장기 legacy 코드베이스에서의 효과 (Vincent 예제는 대부분 그린필드 또는 중형 라이브러리)
- 팀 단위 운영에서의 충돌 해소

## 11. Transferable primitives ★ (load-bearing)

각 항목: 이름 / 설명 / 전제 컨텍스트 / standalone-extractable?

### P1. SKILL.md as a standardized self-contained unit of process documentation
- 스킬 = `name + description + when-to-use + DOT flowchart + HARD-GATE + prose`. 발견/로드/테스트가 가능한 **atomic process unit**.
- 전제: 스킬 로더(플러그인 시스템이나 수동 주입)가 있는 런타임, description 매칭 가능.
- **YES**. Anthropic Agent Skills(2025-10-16)이 상위 기판이지만, Superpowers의 컨벤션(DOT + HARD-GATE + when-only description)은 그 위의 **독립 계층**으로 이식 가능.

### P2. GraphViz DOT as the authoritative process medium (prose subordinate)
- 페이즈 전이와 게이트를 DOT 그래프로 **먼저** 작성, 프로즈는 DOT을 부연. "Claude is particularly good at following processes written in dot."
- 전제: long-context 모델, DOT 구문 파싱 능력 (Claude 계열에서 검증됨).
- **YES** — 다른 primitive 없이도 즉시 이식 가능한 프롬프트 엔지니어링 기법. 단 비-Claude 모델 효과는 미검증.

### P3. `<HARD-GATE>` XML-style blocking tags
- 게이트 조건을 XML 태그로 감싸 "이 조건이 충족될 때까지 진전 금지" 를 에이전트에게 명시. 단일 문장이 프로세스 흐름을 차단.
- 전제: 모델이 XML 태그 의미를 준수. Claude trained 잘 따름, 다른 모델은 미검증.
- **YES**, but 모델 의존 PARTIAL. 태그 이름(`<HARD-GATE>`, `<SUBAGENT-STOP>`)은 컨벤션이므로 자유 교체 가능.

### P4. When-only skill descriptions (discovery/body separation)
- 스킬 description은 **"언제 쓰는지"만** 포함. 본문의 "어떻게"를 description에 노출하면 모델이 읽지 않고 짐작.
- 전제: on-demand skill loading이 있는 런타임.
- **YES** — 강력한 정보 아키텍처 primitive. Skill system을 쓰는 모든 플랫폼에 즉시 적용.

### P5. Subagent-driven development with isolated context
- 구현 태스크는 상위 히스토리 없이 **"exactly what they need"만 받는 서브에이전트**에 위임. 코디네이터 컨텍스트는 오케스트레이션 전용으로 보존.
- 전제: subagent dispatch API (Claude Code Task/Agent, 동등 기능), bite-sized plan이 이미 준비.
- **YES**, but v5.0.6 인라인 회귀에서 드러나듯 **비용/지연 tradeoff 큼**. 저사양/고빈도 환경에서는 PARTIAL.

### P6. Bite-sized 2–5 minute tasks as the unit of plan granularity
- `writing-plans` 스킬이 플랜을 2–5분 태스크로 분해. Dex/HumanLayer의 "carve off small independent context windows" 와 **수렴하는 primitive**.
- 전제: 문제가 실제로 분해 가능, 각 태스크가 명확한 done-test를 가짐.
- **YES**. Ralph-P10과 동일 mental model의 **재현 증거**.

### P7. Two-stage review: spec compliance → code quality
- "Skip no reviews (spec compliance AND code quality both required). Spec compliance verification occurs before code quality review."
- 전제: 리뷰 시간·비용 예산, 에이전트 혹은 사람이 리뷰어 롤.
- **YES** — 리뷰 차원 분리 자체가 primitive. 서브에이전트 구현은 옵션.

### P8. Design approval HARD-GATE before any implementation action
- "DO NOT... write any code... until you have presented a design and the user has approved it." 단순해 보이는 프로젝트에도 예외 없이 적용.
- 전제: HITL approval을 허용하는 워크플로.
- **YES**. 가장 이식성 높은 primitive — 하네스 없어도 단순 시스템 프롬프트로 재현 가능.

### P9. Status-coded subagent outcomes (DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED)
- 서브에이전트가 돌려주는 상태를 enum화 → 코디네이터 디스패처 로직 결정론화.
- 전제: 서브에이전트 존재, 구조화 리턴 포맷 강제.
- **YES**.

### P10. RED/GREEN/REFACTOR with deletion as anti-rationalization enforcement
- "Delete any code written before its test exists" — 선구현 코드를 **쓰레기로 지정**. 명시적 반박 리스트로 핑계 차단.
- 전제: agent가 기꺼이 자기 코드 삭제, 사용자가 사이클을 신뢰.
- **YES** — discipline primitive의 강한 형태. Anti-rationalization prose는 Claude 외 모델에 미검증.

### P11. Model selection strategy embedded in the skill
- "simple/clear → cheap model, integration → standard, architecture/review → most capable." 경제성을 **스킬 본문**에 명시.
- 전제: 멀티-모델 라우팅 가능한 런타임.
- **YES, but** 런타임 의존 PARTIAL.

### P12. Three-phase worflow scaffolding: design → plan → implementation (with gates between each)
- brainstorming → writing-plans → subagent-driven-development. 각 경계는 HARD-GATE 혹은 approval. Ralph의 plan/build 2-모드를 **한 차원 확장**.
- 전제: 사람이 디자인 리뷰 감수, 플랜 산출물을 텍스트로 보관.
- **YES** — 가장 단순한 이식 가능 워크플로 템플릿.

### P13. Writing-skills as a meta-skill (self-improving skill library)
- 운영자가 실패를 보면 **새 스킬을 TDD 방식으로 작성**. 스킬 저작 자체가 스킬.
- 전제: 스킬 저장소 쓰기 권한, 피드백 채널.
- **YES**. Ralph의 AGENTS.md 진화와 유사하지만 더 구조화.

### Rejected as primitive
- **"서브에이전트로 모든 리뷰를 돌려라"** — v5.0.6 회귀가 증명했듯 비용/지연이 손익분기 아래로 떨어질 수 있음. **두 경로를 둘 다 지원**하는 것이 교훈이지, "서브에이전트 mandatory"는 이식하지 말 것.
- **"GraphViz가 모든 모델에 잘 통한다"** — Claude 계열에서만 검증됨. Sonnet/Opus 외 모델로 이식 시 A/B 필요.

### 새 schema 축 후보 (§11에서 발굴)
- **gate_mechanism_syntax** — HARD-GATE XML 태그 같은 "진전 차단 구문 장치"가 축 5(Prompt strategy) 내부에 묻힘. 별도 축으로 분리하면 Ralph의 CAPS-yelling, GSD의 phase gate, OpenSpec의 proposal 승인과 일관 비교 가능.
- **authoritative_process_medium** — "프로세스를 어떤 표현으로 쓰는가" (프로즈 / DOT / Mermaid / JSON schema / code). Superpowers가 DOT를 권위적 표현으로 쓰는 결정이 단독 축.
- **skill_as_unit_of_discipline** — Anthropic Skills 기판 위의 **컨벤션 레이어**로서 Superpowers가 제안하는 SKILL.md 구조 자체가 primitive. 축 1(Identity) 과 5(Prompt strategy) 어느 쪽에도 안 맞음.

## 12. Open questions
- v5.0.6 인라인 리뷰 회귀의 **정량적 비용 데이터** — Vincent 블로그/릴리스 노트에서 구체 수치 미공개
- DOT 플로우차트가 non-Claude 모델(Gemini, GPT-4/5)에서 **실제로 더 잘 따라지는지** A/B
- `writing-skills` 스킬로 사용자가 **실제 만든 커스텀 스킬 분포** — 어떤 카테고리가 가장 많이 생성되는지
- **엄격한 TDD 강제가 속도를 저하시키는 실증 사례** — byteiota류 기사에서 의도적 누락, 1차 사례 부재
- **Legacy 코드베이스 적용성** — 그린필드/중형 라이브러리 사례 위주, 대규모 레거시 시 HARD-GATE가 병목이 되는지 미확인
- **Brainstorm server WebSocket 아키텍처의 장애 모드** — Windows/MSYS2 이슈 이후 복구 상태
- **플러그인 보안 모델** — 공식 마켓플레이스 등재의 심사 기준, 악성 스킬 감지
- **한국어 커뮤니티 재현 및 번역** — 검색으로는 제한적 노출

## Sources

### Primary (Jesse Vincent)
- https://blog.fsck.com/2025/10/09/superpowers/ — 공개 원글, "Skills are what give your agents Superpowers"
- https://blog.fsck.com/2025/10/05/how-im-using-coding-agents-in-september-2025/ — 직계 조상, brainstorm/plan 프롬프트 원형
- https://blog.fsck.com/2025/12/18/superpowers-4/ — v4: DOT 플로우차트, 2-stage review
- https://blog.fsck.com/releases/2026/02/12/superpowers-v4-3-0/ — v4.3.0

### Primary (repo)
- https://github.com/obra/superpowers — README, v5.0.7, stars/contrib/license
- https://github.com/obra/superpowers/blob/main/RELEASE-NOTES.md — 버전 히스토리
- https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md — HARD-GATE verbatim + DOT 소스
- https://raw.githubusercontent.com/obra/superpowers/main/skills/test-driven-development/SKILL.md — "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"
- https://raw.githubusercontent.com/obra/superpowers/main/skills/subagent-driven-development/SKILL.md — 프로세스, 상태 enum, 제약
- https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md — 템플릿, TDD-for-process
- https://github.com/anthropics/claude-plugins-official/pull/148 — 2026-01-15 마켓플레이스 등재 PR (by noahzweben)
- https://claude.com/plugins/superpowers — Anthropic 플러그인 페이지

### Secondary (third-party critiques & reviews)
- https://medium.com/@tentenco/superpowers-gsd-and-gstack-what-each-claude-code-framework-actually-constrains-12a1560960ad — Ewan Mak, 2026-04, "constrains the development process" 프레이밍
- https://byteiota.com/superpowers-82k-stars-transform-claude-code-senior-dev/ — chardet 정량 주장, 비판 누락 경고
- https://www.heyuan110.com/posts/ai/2026-04-09-claude-code-openspec-superpowers/ — OpenSpec×Superpowers 병용 권고, "bilingual"
- https://www.heyuan110.com/posts/ai/2026-02-01-superpowers-deep-dive/ — 심층 리뷰
- https://docs.bswen.com/blog/2026-03-27-openspec-vs-superpowers/ — SDD 프레임워크 비교
- https://deepwiki.com/obra/superpowers/7.1-using-superpowers — SessionStart hook, `<SUBAGENT-STOP>`, `<EXTREMELY_IMPORTANT>` 주입 메커니즘
- https://timewell.jp/en/columns/superpowers-claude-code-plugin — 일본어 소개, 57K 스타 시점 스냅샷
- https://medium.com/@richardhightower/the-great-framework-showdown-superpowers-vs-bmad-vs-speckit-vs-gsd-360983101c10 — Rick Hightower, 4-프레임워크 비교
- https://github.com/Fission-AI/OpenSpec/issues/780 — OpenSpec을 Superpowers 스킬 팩으로 배포 요청
- https://github.com/Fission-AI/OpenSpec/issues/859 — 동일 주제 후속
- https://github.com/obra/superpowers/issues/200 — "Skill Grading Report: test-driven-development 87/100"
- https://www.termdock.com/en/blog/superpowers-framework-agent-skills — 프레임워크 소개

### Ecosystem context
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills — Agent Skills 기판 (2025-10-16)
- https://github.com/anthropics/claude-plugins-official — 공식 마켓플레이스 레포
