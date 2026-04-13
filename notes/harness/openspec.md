---
title: OpenSpec
slug: openspec
date: 2026-04-13
primary_source: https://github.com/Fission-AI/OpenSpec
secondary_source: https://openspec.dev
topic: harness
tags: [harness, sdd, spec-driven, brownfield, delta-markers, fission-ai, claude-code]
status: deep-dive
confidence: high
rounds: 3
axes_used: [1,2,3,4,5,6,7,8,9,10,11,12]
axes_added: []
axes_dropped: []
candidate_axis_reuse: [C, D, E, H]
---

## Proposed schema deltas
None new. Existing candidate axes reused:
- **C (Mode splitting)**: propose → apply → archive은 수동 전환 명시 모드 분할 (7번째 독립 사용)
- **D (Gate mechanism syntax)**: artifact dependency graph + `/opsx:verify` — 소프트 게이트(완료 체크는 경고이지 차단이 아님). D의 소프트 변종으로 등록.
- **E (Authoritative process medium)**: 스펙이 Markdown + RFC 2119 키워드 + Gherkin 시나리오 — 프로세스 권위 매체로서 반구조화 Markdown.
- **H (Artifact naming schema as protocol)**: `openspec/specs/<domain>/spec.md` + `openspec/changes/<name>/` 구조 — 디렉토리 레이아웃이 상태 머신 프로토콜로 기능.

## TL;DR (3줄)
OpenSpec은 `openspec/specs/`를 소스 오브 트루스로, `openspec/changes/<name>/`을 변경 격리 단위로 유지하는 SDD(Spec-Driven Development) 프레임워크. **브라운필드 우선** 설계: "대부분의 도구는 처음부터 시작한다고 가정하지만 우리는 성숙한 코드베이스에 집중한다"가 저자의 핵심 포지션. `/opsx:propose → apply → archive`의 3단계 루프가 반복 단위이며, 델타 마커(`## ADDED / MODIFIED / REMOVED Requirements`)로 변경 전후를 명시한다.

---

## 1. Identity & provenance

- **Organization**: Fission-AI (GitHub org: github.com/Fission-AI)
- **Repo**: github.com/Fission-AI/OpenSpec — "Spec-driven development (SDD) for AI coding assistants"
- **Stars**: 39.6k stars, 2.7k forks, 197 watchers (2026-04-13 기준)
- **License**: MIT
- **First stable**: v1.0.0 released 2026-01-26 ("OpenSpec 1.0 marks the transition from experimental to stable")
- **Distribution**: npm 글로벌 패키지 (`npm install -g @fission-ai/openspec@latest`), openspec.dev 랜딩 페이지
- **Contact/teams**: teams@openspec.dev (Slack 접속), Workspaces 팀 기능 "In Development"
- **Tool support**: Claude Code, Cursor, Windsurf, Continue, Gemini CLI, GitHub Copilot, Amazon Q, Cline, RooCode, Kilo Code 등 21개+ 도구
- **Maintenance posture**: 활발히 개발 중 — v1.0.0이 major breaking change 포함(이전 `/openspec:*` 커맨드 → `/opsx:*`), CHANGELOG + Releases 페이지 유지

> "Spec-driven development (SDD) for AI coding assistants" — GitHub repo description

---

## 2. Problem framing

OpenSpec의 저자가 명명한 고통은 두 층위다:

**1층: 컨텍스트 소멸**
LLM 컨텍스트 창이 40% 이상 차면 이전 요구사항을 망각하거나 변형한다는 관찰. 세션이 닫히면 AI가 "왜 이 변경을 했는지"를 잃는다.

**2층: 브라운필드 외면**
"Most tools assume you're starting fresh. We focus on mature codebases where the real struggle is figuring out how the current system works." — openspec.dev

두 문제를 단일 메커니즘으로 공략: **스펙 파일을 코드와 함께 살아있는 문서로 유지**하고, 변경은 격리된 change 폴더에서 진행한 뒤 아카이브로 main spec에 병합.

heyuan110.com 비교 포스트의 포지션 요약:
> "OpenSpec solves the 'why did we make this change?' problem while Superpowers solves the 'is this code correct?' problem."

---

## 3. Control architecture

**분류**: Workflow(사람이 단계 전환 결정) + 내부는 LLM-directed artifact 생성. Anthropic 분류상 하이브리드.

**반복 단위**: 하나의 change 폴더 (`openspec/changes/<name>/`) = 하나의 스프린트 단위.

**기본 루프**:
```
/opsx:propose → (human review) → /opsx:apply → (human review) → /opsx:archive
```

**확장 루프**:
```
/opsx:explore → /opsx:new → /opsx:continue (한 아티팩트씩) | /opsx:ff (전부 한 번에)
→ /opsx:apply → /opsx:verify → /opsx:sync → /opsx:archive
```

**종료 조건**: `/opsx:archive`가 실행되어 delta specs가 main specs에 병합된 시점. 명시적 done-state가 파일시스템에 기록됨(변경 폴더가 `changes/archive/[TIMESTAMP-name]/`으로 이동).

**Artifact dependency graph**: proposal → (spec/design) → tasks 순서. 선행 아티팩트가 없으면 다음 생성이 block됨("Dependencies are enablers, not gates — workflow is fluid"). 하지만 `/opsx:archive`는 incomplete tasks에 대해 경고만 하고 차단하지 않음.

**Single-agent 모델**: bswen.com 분석이 지적 — "No built-in code review mechanism." 단일 에이전트가 순차 실행. 멀티에이전트 병렬화 내장 없음.

---

## 4. State & context model

**지속 상태의 이중 레이어**:

| 레이어 | 위치 | 역할 | 변경자 |
|---|---|---|---|
| Main specs | `openspec/specs/<domain>/spec.md` | 소스 오브 트루스 — 현재 시스템 동작 | archive 시 자동 병합 |
| Change artifacts | `openspec/changes/<name>/` | 제안 중인 변경 격리 단위 | AI agent (human review 후) |
| Archive | `openspec/changes/archive/[TS-name]/` | 완료된 변경 히스토리 | archive 명령 |

**모델이 매 턴 보는 것**: Claude Code 통합 기준 — `openspec/specs/` (현재 동작 계약) + 해당 change 폴더 내 proposal/design/tasks (현재 작업 컨텍스트). 이전 세션의 추론은 없으나 **파일에 기록된 결정 이력**이 지속된다.

**컨텍스트 경제성**: redreamality.com 분석에서 "load-on-demand" 방식으로 토큰 절약을 주장 — 관련 스펙만 로드. 40% 임계값 주장 인용("context usage exceeds 40%, AI performance significantly degrades")이나 1차 출처 미제공.

**변경 격리**: `changes/` 폴더 내에서 병렬 변경이 독립 진행 가능. `/opsx:bulk-archive`가 충돌 감지 후 코드베이스 검사로 해결. "OpenSpec's biggest advantage is its change isolation mechanism. SpecKit tends to directly modify main spec files, easily causing conflicts." — redreamality.com

---

## 5. Prompt strategy

**시스템 프롬프트 형태**: v1.0.0부터 `.claude/skills/` 단일 디렉토리(이전 8개 config 파일 통합). "Dynamic instructions assembled from context, rules, and templates with real-time CLI queries" — release notes.

**슬래시 커맨드 전체 목록** (v1.0.0 기준):

| 커맨드 | 목적 | 노트 |
|---|---|---|
| `/opsx:propose` | 변경 생성 + 기획 아티팩트 일괄 생성 | 기본 진입점, 최단 경로 |
| `/opsx:explore` | 아티팩트 없이 아이디어 탐색 | 커밋 전 조사용 |
| `/opsx:apply` | tasks.md 기반 구현 | 작업 목록 추적 |
| `/opsx:archive` | 변경 완료 + delta를 main spec에 병합 | incomplete tasks는 경고만 |
| `/opsx:new` | change 폴더 스캐폴드만 생성 | 수동 아티팩트 생성 시 |
| `/opsx:continue` | 다음 아티팩트 하나씩 생성 | 리뷰 후 진행 |
| `/opsx:ff` | 모든 기획 아티팩트 일괄 생성 | 요구사항 명확할 때 |
| `/opsx:verify` | 구현이 아티팩트와 일치하는지 검증 | 완전성/정확성/일관성 |
| `/opsx:sync` | delta specs를 main에 병합(아카이브 전) | archive가 자동 처리하므로 선택적 |
| `/opsx:bulk-archive` | 여러 변경 동시 아카이브 | 충돌 감지 포함 |
| `/opsx:onboard` | 완전한 워크플로 인터랙티브 튜토리얼 | 15-30분, 실제 코드베이스 사용 |

**도구별 구문 차이**:
- Claude Code: `/opsx:propose`
- Cursor/Windsurf/Copilot: `/opsx-propose`
- Trae: `/openspec-propose`

**스펙 문서 포맷 (메타-프롬프팅)**:
- RFC 2119 키워드: MUST / SHALL / SHOULD / MAY
- Gherkin 시나리오: GIVEN / WHEN / THEN
- 델타 마커: `## ADDED Requirements` / `## MODIFIED Requirements` / `## REMOVED Requirements`

**프롬프트 실패 패턴** (heyuan110 지적):
> "Over-detailed specs constrain AI choices" — specs가 구현 가이드가 되면 AI가 대안적 해법을 못 고른다.
> "Specs that are actually pseudocode" — GIVEN/WHEN/THEN이 아닌 구현 단계로 쓰면 best practice 위반.

---

## 6. Tool surface & permission model

**권한 모델**: 명시적 YOLO 없음. `/opsx:apply` 중 Claude Code의 기본 권한 모델 따름. 
- Plan Mode에서 직접 파일 조작 불가 — CLI로 아카이브 수동 실행 필요(redreamality.com 지적).
- `--dangerously-skip-permissions` 언급 없음 — Ralph와 대비되는 보수적 기본값.

**CLI 도구 표면**:
- `openspec init` — 프로젝트 초기화
- `openspec update` — 스펙 업데이트
- `openspec config profile` — 확장 워크플로 설정

**스키마 검증**: 커맨드 실행 전 schema 존재 여부 확인. `--schema <name>` 플래그로 커스텀 스키마 지정 가능.

**파일시스템 전용**: 외부 SaaS 의존 없음. "Free, no APIs" — redreamality.com 비교표. OpenSpec Dashboard 존재 언급되나 코어 워크플로는 파일 기반.

---

## 7. Human-in-the-loop points

OpenSpec의 HITL은 **명시적으로 설계된 게이트 3개**:

1. **Proposal review**: 인텐트/스코프 합의. 에이전트가 proposal.md 초안 후 사람이 검토.
2. **Spec/design validation**: 구조가 명확한지 확인 후 구현 진행.
3. **Archive decision**: delta를 main spec에 병합하는 의식적 결정.

> "The framework assumes humans guide scope and agents draft documents for human approval before specs lock in." — concepts.md

Ralph와 대조: Ralph는 실행 중 HITL 없음, OpenSpec은 각 단계 전환에 사람 리뷰를 설계 원칙으로 내세움.

bswen.com 분석의 약점 지적: "The framework assumes I'm disciplined enough to write [tests]" — 검증 의존도가 사람 자기절제에 높음. TDD 강제 없음.

---

## 8. Composability

**21개 AI 도구 지원**: Claude Code, Cursor, Windsurf, Continue, Gemini CLI, GitHub Copilot, Amazon Q, Cline, RooCode, Kilo Code, Auggie, CodeBuddy, Qoder, Qwen, CoStrict, Crush, Factory, OpenCode, Antigravity, iFlow, Codex.

**Superpowers와의 통합 포지션** (heyuan110 권고):
> "OpenSpec handles planning, Superpowers handles coding discipline, Claude Code executes. They don't conflict — each owns its stage."

사용 권고 매트릭스 (heyuan110):
| 규모 | 권고 스택 |
|---|---|
| 2시간 이하 | Claude Code only |
| 2–8시간(개인) | Claude Code + Superpowers |
| 4–16시간(팀) | 풀스택 (Claude Code + Superpowers + OpenSpec) |
| 병렬 피처 | 풀스택 + worktrees |

**스펙 충돌 해결**: `/opsx:bulk-archive`가 동시 변경 감지 후 코드베이스 검사로 자동 해결. 이 기능이 팀 사용 사례의 핵심 가치 주장.

**Spec Kit과의 대비** (redreamality.com):
| 차원 | OpenSpec | SpecKit |
|---|---|---|
| 핵심 시나리오 | 브라운필드 (1→n) | 그린필드 (0→1) |
| 변경 관리 | `changes/` 중앙화 | 분산 스펙 직접 수정 |
| 경량성 | 매우 높음 | 중간 |

---

## 9. Empirical claims & evidence

**저자/공식 주장 (정성, 벤치마크 없음)**:
- "Fluid not rigid, iterative not waterfall" — openspec.dev
- "Structure before code enables long-term architectural consistency and business logic integrity" — redreamality.com 요약
- Token 절약(load-on-demand): "토큰 소비 감소" 주장, 수치 미제공
- 컨텍스트 40% 임계값 주장: "when context usage exceeds 40%, AI performance significantly degrades" — redreamality.com 인용, 1차 출처 미제공

**3자 평가 (정성)**:
- bswen.com: 대규모 엔터프라이즈 컴플라이언스 프로젝트에 적용, 수치 없음
- redreamality.com: "change isolation mechanism prevents merge conflicts in multi-person collaboration" — 경험담 수준
- heyuan110.com: 팀 레벨 권고표, 벤치마크 없음

**증거 유형**: 압도적으로 정성 + 주장. 통제된 벤치마크 없음. Ralph와 동일한 증거 질.

---

## 10. Failure modes & limits

### 프레임워크 설계 한계 (3자 관찰)

**TDD 미강제** (bswen.com):
> "I could skip tests entirely. The framework assumes I'm disciplined enough to write them."
테스트 작성은 사람 자기절제에 의존. Superpowers와 비교 시 가장 큰 약점으로 지적됨.

**단일 에이전트 모델** (bswen.com):
> "No built-in code review mechanism. I had to self-review using checklists."
멀티에이전트 리뷰 루프 내장 없음. `tasks.md` 체크리스트를 사람이 활용해야 함.

**수동 Git 워크플로** (bswen.com):
브랜치 격리나 자동 git 규율 강제 없음. 운영자 재량.

**Plan Mode 제한** (redreamality.com):
Claude Code의 Plan Mode에서 직접 파일 조작 불가 → 아카이브를 CLI로 수동 실행해야 함.

### 운영 실수 패턴 (heyuan110 지적)

- **`/opsx:archive` 스킵**: "Next session, AI read the old spec and reimplemented existing functionality." 아카이브를 빠뜨리면 다음 세션 AI가 이미 완료된 기능을 재구현한다.
- **과도하게 상세한 스펙**: 구현 세부사항을 스펙에 쓰면 AI의 해법 선택권을 제약.
- **계획 미확인 후 진행**: 제안 확인 없이 진행하면 잘못된 기술 선택.
- **30분짜리 작업에 풀 파이프라인**: 오버헤드가 이득보다 큼.

### UNVERIFIED
- 컨텍스트 40% 임계값 — 수치의 1차 출처 불명. redreamality.com이 인용했으나 OpenSpec 공식 문서에서 직접 확인 안 됨.
- 실제 토큰 절약 수치 — "load-on-demand"의 정량 효과 미검증.

---

## 11. Transferable primitives ★

### P1. Delta-marker spec format (ADDED / MODIFIED / REMOVED)
- 변경 사항을 전체 스펙 재작성 없이 diff로 기술. `## ADDED Requirements`, `## MODIFIED Requirements`, `## REMOVED Requirements` 섹션으로 구조화.
- 전제: Markdown 파일 r/w 가능 런타임, archive 시 파싱 로직 또는 에이전트 이해.
- **YES** — 도구 독립적. 어떤 AI 어시스턴트에도 컨벤션으로 이식 가능. 브라운필드 코드베이스에서 가장 가치 있는 단일 primitive.

### P2. Change-folder isolation unit
- 하나의 기능 변경 = 하나의 `changes/<name>/` 폴더. proposal + design + tasks + specs delta가 한 단위로 묶임. 완료 전까지 main spec과 독립.
- 전제: 파일시스템 접근, 사람이 archive 결정 내림.
- **YES** — 팀 협업에서 merge conflict 방지 패턴으로 직접 이식 가능. PR 브랜치와 자연스럽게 매핑.

### P3. Spec-as-behavior-contract (RFC 2119 + Gherkin)
- 스펙은 구현 방법이 아니라 **관찰 가능한 외부 동작**을 기술. MUST/SHALL/SHOULD + GIVEN/WHEN/THEN 구문.
- 전제: 에이전트가 요구사항/시나리오 구분 이해.
- **YES** — TDD 경계가 없어도 에이전트가 스펙을 acceptance test 기준으로 읽도록 유도. 어느 스펙 파일에도 이식 가능.

### P4. Artifact dependency enablement (proposal → specs/design → tasks)
- 선행 아티팩트가 후행 아티팩트를 **가능하게** 함 — 강제 차단이 아닌 enabler. "Dependencies are enablers, not gates — workflow is fluid."
- 전제: 사람이 순서 지킬 의향 있음.
- **PARTIAL** — 설계 원칙으로 이식 가능하나, 강제 gate 없으므로 규율 없는 팀에서는 실효성 낮음.

### P5. Archive-as-commit (delta merge + history preservation)
- archive가 delta를 main spec에 병합하고 원본 change 폴더를 타임스탬프 디렉토리에 보존. "Full context for historical reference."
- 전제: 파일시스템, archive 명령 실행 습관.
- **YES** — "왜 이 결정을 했는가"의 감사 추적. git blame보다 의도 수준의 히스토리.

### P6. Load-on-demand spec consumption (context economy)
- 모든 스펙을 한 번에 로드하지 않고 관련 도메인 스펙만 로드. 컨텍스트 창 절약.
- 전제: 스펙이 도메인별로 잘 분리되어 있고 에이전트가 관련 스펙 파일을 스스로 판단 가능.
- **PARTIAL** — 패턴 이식 가능하나 도메인 분리 품질에 강하게 의존. 단일 모노리스 스펙에서는 효과 없음.

### P7. Explore-before-commit ideation mode (`/opsx:explore`)
- 아티팩트를 생성하지 않고 아이디어를 탐색하는 무결과 모드. "Explore → commit"의 명시적 단계 분리.
- 전제: 모드 분리에 익숙한 운영자.
- **YES** — Ralph의 plan/build 분리, Superpowers의 phase gate와 같은 계열. 탐색과 실행의 분리 원칙.

### P8. Multi-tool slash command portability (25+ tools)
- 동일한 SDD 워크플로가 Claude Code, Cursor, Windsurf, Copilot 등 21개 도구에서 동작. 도구별 구문 매핑(`:` vs `-`) 레이어가 추상화.
- 전제: OpenSpec CLI가 설치된 환경.
- **PARTIAL** — 추상화 레이어 자체(구문 어댑터 패턴)는 이식 가능한 설계 아이디어. 특정 OpenSpec 커맨드와 묶여 있지 않음.

### Rejected as primitive
**"Archive warning, not block"** — `/opsx:archive`가 미완성 tasks에 경고만 하는 설계는 이식 가능한 primitive라기보다 **트레이드오프 선택**. 강제 gate가 필요한 컨텍스트에는 오히려 역적용 필요. 원시요소로 포팅하지 말 것.

---

## 12. Open questions

- **컨텍스트 40% 임계값의 1차 출처**: redreamality.com이 인용한 수치지만 OpenSpec 공식 문서에서 직접 확인 안 됨. Fission-AI 블로그 또는 연구 포스트에서 출처 확인 필요.
- **브라운필드 온보딩 실제 플로우**: `openspec init`이 기존 코드베이스 스캔 후 초기 스펙을 자동 생성하는지, 아니면 사람이 처음부터 스펙을 작성해야 하는지 — getting-started.md에 그린필드 only 케이스만 확인됨.
- **멀티에이전트 통합**: Claude Code의 subagent 기능과 `/opsx:apply` 연동 여부 — bswen.com은 단일 에이전트 모델로 분류했으나 공식 문서에서 subagent 지원 언급 있음.
- **OpenSpec Dashboard**: "Project management" 기능이 언급되나 구체적 기능 미확인. 클라우드 SaaS 여부, Workspaces 기능 범위 불명.
- **Fission-AI 팀 구성**: MAINTAINERS.md 언급되나 개인 프로젝트인지 팀 프로젝트인지 확인 안 됨.
- **Superpowers + OpenSpec 실전 통합 사례**: heyuan110이 권고하지만 실제 사용 리포트 없음.

---

## Sources

### Primary
- https://github.com/Fission-AI/OpenSpec — 공식 레포 (39.6k stars)
- https://openspec.dev — 공식 랜딩 페이지
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md — 개념 문서
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md — 커맨드 레퍼런스
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md — 온보딩 가이드
- https://github.com/Fission-AI/OpenSpec/releases/tag/v1.0.0 — v1.0.0 릴리즈 노트 (2026-01-26)

### Third-party analysis
- https://www.heyuan110.com/posts/ai/2026-04-09-claude-code-openspec-superpowers/ — Claude Code + OpenSpec + Superpowers 3-way 비교 (heyuan110, 2026-04-09)
- https://redreamality.com/garden/notes/openspec-guide/ — OpenSpec 아키텍처 딥다이브 (redreamality)
- https://docs.bswen.com/blog/2026-03-27-openspec-vs-superpowers/ — OpenSpec vs Superpowers 비교 (bswen, 2026-03-27)

### Secondary
- https://www.augmentcode.com/tools/best-spec-driven-development-tools — "6 Best SDD Tools for AI Coding in 2026"
