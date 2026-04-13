---
title: revfactory/harness — Agent Team & Skill Architect
slug: revfactory-harness
author: Minho Hwang (황민호, @revfactory), Kakao AI Native Strategy Team Leader
canonical: https://github.com/revfactory/harness
companion: https://github.com/revfactory/harness-100
experiment_repo: https://github.com/revfactory/claude-code-harness
date: 2026-04-13
status: deep-dive
confidence: high
rounds: 3
axes_used: [1,2,3,4,5,6,7,8,9,10,11,12]
axes_added: [meta-skill_bootstrapping]
axes_dropped: []
candidate_axis_reuse: [C (mode_splitting), F (skill_as_unit_of_discipline), K (role_perspective_as_constraint_surface), A (iteration_boundary_semantics)]
---

## TL;DR (3줄)

revfactory/harness는 "하네스를 생성하는 하네스" — 단일 `SKILL.md`로 6단계 파이프라인을 실행해 도메인별 에이전트 팀과 스킬 파일 전체를 자동 생성하는 메타-스킬. 카카오 AI Native Strategy 팀 리더 황민호가 제작했으며 15개 소프트웨어 태스크 A/B 실험으로 +60% 품질 향상을 주장. 2.4k 스타(2026-04 기준)로 Claude Code 플러그인 생태계 한국 최상위 기여작이며, README_KO.md / README_JA.md 다국어 문서, harness-100 1808파일 동반 라이브러리까지 포함.

---

## Proposed schema deltas

### New local axis: Meta-skill bootstrapping
**Rationale**: Harness는 다른 하네스를 생성하는 메타-레이어 — 1회 실행이 `.claude/agents/*.md` + `.claude/skills/*/SKILL.md` 전체를 사이드이펙트로 산출. 이것은 현재 seed 축(1–12) 중 어디에도 맞지 않는 고유 패턴. "하네스가 실행의 결과물로 또 다른 하네스를 생성하는가, 있다면 생성 범위(에이전트 정의/스킬/CLAUDE.md)와 생성 품질 검증 방식은 무엇인가"를 묻는 독립 축. ECC의 `/skill-create`와 부분 겹침이 있지만 scope(전체 팀 아키텍처 vs 단일 스킬)가 다름.

---

## 1. Identity & Provenance

- **Author**: Minho Hwang (황민호, @revfactory). Kakao(@kakao) AI Native Strategy Team Leader. 2013년 입사 이후 Daum 검색 서비스, Moment 광고 플랫폼, OLIVE 오픈소스 관리 플랫폼 참여. 현재 AI 에이전트 트렌드 탐색 및 전략 수립.
- **Location**: Jeju Island, South Korea
- **First public**: 주 repo `revfactory/harness` (2.4k ⭐, 351 forks, Apache 2.0). 별도 실험 저장소 `revfactory/claude-code-harness` (89 ⭐, March 5, 2026 생성). 100-harness 라이브러리 `revfactory/harness-100` (547 ⭐, 206 forks).
- **Distribution**: Claude Code marketplace (`/plugin marketplace add revfactory/harness`) + GitHub 직접 설치. SkillsLLM 인덱스 등재.
- **언어 지원**: README.md (English), README_KO.md (Korean), README_JA.md (Japanese) — 3개국어 문서 동시 제공.
- **연구 출처**: Hwang, M. (2026). "Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality." (`claude-code-harness/paper/` 경로에 한국어·영어 PDF).
- **유지 상태**: 2026-04 기준 활발히 유지. Phase 7 "Harness Evolution" 사이클이 SKILL.md에 내장되어 있어 지속 진화 설계됨.

> "A meta-skill that designs domain-specific agent teams, defines specialized agents, and generates the skills they use." — GitHub repo description

---

## 2. Problem Framing

저자의 핵심 주장:

> "The bottleneck is structure, not capability. LLMs have sufficient knowledge — they lack project-specific structural guidance." — README (claude-code-harness)

황민호는 문제를 두 가지 차원에서 정의:
1. **단일 에이전트 한계**: 복잡한 도메인 작업을 하나의 에이전트에 맡기면 품질이 낮고 편차가 크다.
2. **팀 설계 복잡성**: 멀티에이전트 팀을 수동으로 구성하는 것 자체가 진입 장벽. 에이전트 역할 분리, 스킬 파일 작성, 오케스트레이션 프로토콜 정의 — 반복적 보일러플레이트.

해결책: "빌드 하네스" 한 마디로 이 설계 과정 전체를 자동화. **메타-스킬이 하네스를 만드는 구조**.

---

## 3. Control Architecture

**분류**: Phase-driven deterministic pipeline (6+1 단계), Anthropic 분류상 "workflow" 레이어 위에 "agent team" 조합.

**외곽 제어 흐름**:
```
사용자 트리거 ("Build a harness" 또는 "하네스 구성해줘")
→ SKILL.md Phase 0: 상태 감사 (기존 .claude/ 디렉토리 존재 여부)
→ Phase 1: 도메인 분석
→ Phase 2: 팀 아키텍처 설계
→ Phase 3: 에이전트 정의 생성
→ Phase 4: 스킬 생성
→ Phase 5: 통합 & 오케스트레이션
→ Phase 6: 검증 & 테스트
→ Phase 7: 하네스 진화 (피드백 루프, 유지보수 워크플로)
```

**Phase 0 분기 (3-way mode split)**:
- 신규 빌드: 전체 Phase 실행
- 확장: 선택적 Phase만 실행
- 유지보수: Phase 7-5 워크플로 (감사→변경→changelog→검증)

**실행 모드 (Phase 2.1)**:
- Default: **Agent Team** (실시간 TeamCreate + SendMessage 협업)
- Alternative: **Subagent** (직렬, 오버헤드 감소)
- Hybrid: **Phase별 모드 전환** (오케스트레이터에 문서화)

**종료 조건**: Phase 6 검증 완료 후 자연 종료. 반복 루프 없음 (Ralph 와 대비). 단, Phase 7이 피드백 기반 재실행 진입점으로 기능.

**Anthropic 분류 매핑**: SKILL.md 자체는 workflow (선형 Phase 파이프라인). 생성된 팀은 agent-based (TeamCreate + SendMessage). 메타-스킬이 agent 워크플로를 산출하는 2-레이어 구조.

---

## 4. State & Context Model

**생성물이 곧 상태 저장소**. Harness의 실행 결과는 다음 파일들로 영속:

| 경로 | 내용 | 생성자 |
|---|---|---|
| `.claude/agents/{name}.md` | 에이전트 역할 정의, 입출력 프로토콜, 협업 규약 | Harness (Phase 3) |
| `.claude/skills/{name}/SKILL.md` | 스킬 정의 (YAML frontmatter + Markdown body) | Harness (Phase 4) |
| `CLAUDE.md` (프로젝트 루트) | 트리거 규칙 + changelog만 — 에이전트/스킬 목록 금지 | Harness (Phase 5) |

**Phase 0 상태 감사**: 매 실행 시작에 기존 `.claude/` 구조와 `CLAUDE.md` 기록 사이의 **drift**를 감지. 상태 인식형 재진입.

**Progressive Disclosure (컨텍스트 모델)**:
- 메타데이터(YAML frontmatter): **항상 로드**
- 스킬 본문: **트리거 시만 로드**
- `references/`: **조건부 로드**
- `scripts/`: **자체 포함, 독립 실행**

이 계층적 로딩은 Ralph의 "결정론적 preload"와 다르다 — Harness는 필요에 따라 선택적으로 컨텍스트를 확장.

**생성된 팀의 상태 전달 (Phase 5)**:
- 소규모 데이터: Task/Message
- 대형 아티팩트: 파일
- Subagent 결과: return value

---

## 5. Prompt Strategy

**SKILL.md가 핵심 artifact**. `skills/harness/SKILL.md`는 Harness 자체의 동작 정의이자 생성된 스킬들의 포맷 규범이기도 함.

**SKILL.md YAML frontmatter**:
```yaml
name: harness
description: Constructs domain-specific harnesses by defining specialist agents and 
their associated skills. Triggered for harness setup, redesign, or operational 
maintenance requests.
```

**"Pushy" description 원칙 (Phase 4 지시)**:
- 트리거 상황 포함
- Near-miss 케이스와의 구별 포함
- "어떤 상황에 쓰이는지" 명시 — 자동 트리거 정확도를 위한 설계.

**스킬 본문 원칙**:
- Why 설명 (What/How보다 Why 우선)
- 린하게 유지 (<500줄)
- 규칙 일반화
- 반복 코드는 번들
- 명령형 어조

**트리거 검증 (Phase 6.4)**:
- should-trigger 쿼리 8–10개
- should-NOT-trigger 쿼리 8–10개 (near-miss 집중)

**모드 분기 (Phase 0)**:
- 상태 감사 결과에 따라 실행 경로 분기
- 이것은 사용자의 명시적 스위치가 아닌 **에이전트 자율 판단**

**특이사항**: Ralph의 CAPS 호통, Superpowers의 `<HARD-GATE>` 같은 명시적 진전 차단 구문이 없음. Harness는 Phase 구조 자체가 순서 보장 장치 역할.

---

## 6. Tool Surface & Permission Model

**실행 모드에 따른 도구 사용**:
- Agent Team 모드: `TeamCreate`, `TaskCreate`, `SendMessage`, 파일 I/O
- Subagent 모드: `Agent` 툴 (`run_in_background: true`)
- 공통: `.claude/agents/`, `.claude/skills/` 파일 생성/수정

**`allowed-tools` 없음**: SKILL.md frontmatter에 explicit tool restriction 미지정 — 표준 Claude 기능 범위 내 자율 사용.

**Permission posture**: 명시적 YOLO 없음. 표준 Claude Code 권한 모델. 단, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 환경변수 필요 (Agent Team 모드).

**생성 에이전트에 대한 모델 지정**: Phase 3 지시 — "모든 Agent 툴 호출에 `model: 'opus'` 지정". 에이전트 품질 우선.

**Progressive Disclosure를 통한 컨텍스트 제어**: 스킬 본문을 항상 로드하지 않음으로써 컨텍스트 오염 방지 — 암묵적 permission 설계.

---

## 7. Human-in-the-Loop Points

**생성 시점의 HITL 설계**:
- Phase 6.3: 2–3개 현실적 프롬프트로 스킬 실행 테스트 + with-skill vs. without-skill 비교 — 운영자 검토 암묵 권장
- Phase 7.1: 실행 후 피드백 요청 (강제 아님, "기회 제공")

**생성된 팀의 HITL**: SKILL.md가 지정하지 않음 — 생성된 에이전트 정의에 달림. Harness 자체는 팀 실행 중 중단점 없음.

**의도적 제약**: Phase 5.4 지시 — `CLAUDE.md`에 에이전트/스킬 목록, 디렉토리 구조, 상세 규칙을 **금지**하고 트리거 규칙 + changelog만. "과도한 문서화는 컨텍스트 오염".

**Phase 7 피드백 루프**: 반복 실패 패턴, 에이전트 오류 루프, 사용자 workaround 감지 시 진화 트리거. 사람의 암묵적 행동 패턴이 HITL 신호.

---

## 8. Composability

**1차 산출물이 곧 다음 하네스의 입력**: Harness로 생성된 에이전트 정의와 스킬이 다시 Harness의 Phase 0 감사 대상이 됨 — 재귀적 컴포지션.

**harness-100 라이브러리**: Harness 자체 실행으로 만들어진 200개 패키지(한국어/영어 각 100개). 10개 도메인, 978 에이전트, 630 스킬, 1808 마크다운 파일. 생성 증거이자 사용 템플릿.

**아키텍처 패턴 라이브러리 (6종)**:
1. Pipeline — 순차 의존성
2. Fan-out/Fan-in — 병렬 작업
3. Expert Pool — 컨텍스트 기반 선택
4. Producer-Reviewer — 생성+검증
5. Supervisor — 중앙 조율
6. Hierarchical Delegation — 재귀 위임

**플러그인 생태계 통합**: `/plugin marketplace add revfactory/harness` — Claude Code marketplace 정식 등재. 설치 후 모든 프로젝트에서 글로벌 스킬로 사용 가능.

**런타임 요구사항**: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` — 실험적 기능 플래그. 이식성 제약.

**harness-100 도메인 커버리지**: 콘텐츠 제작(YouTube/팟캐스트), 소프트웨어 개발/DevOps, 데이터·AI/ML, 비즈니스 전략, 교육, 법률, 건강, 커뮤니케이션, 운영, 특화(부동산/이커머스/ESG).

---

## 9. Empirical Claims & Evidence

**출처**: Hwang, M. (2026). "Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality." — `revfactory/claude-code-harness/paper/` (한국어·영어 PDF)

**실험 설계**:
- Baseline: Claude Code (프롬프트만)
- Treatment: Harness 구성된 Claude Code
- 태스크: 15개 소프트웨어 엔지니어링 태스크 (3 난이도: Basic / Advanced / Expert)
- 구조: `experiments/cases/` (15개 YAML), `experiments/results/case-{001-015}/` (baseline vs harness 각각), `evaluation.json` (10차원 평가)

**주요 수치**:
- 평균 품질 점수: 49.5 → 79.3 (+60%, 100점 만점)
- 승률: 15/15 (100%)
- 출력 분산: -32%

**난이도별 개선 (복잡도 스케일링)**:
- Basic: +23.8점
- Advanced: +29.6점
- Expert: +36.2점 (+52% effect size 증가)

**가장 큰 개선 차원 (10차원 중)**:
- Test Coverage: +4.9 (baseline 2.5 — 테스트 거의 없음)
- Architecture: +4.4 (baseline 단일 파일 경향)
- Error Handling: +3.0
- Extensibility: +3.0

**증거 유형**: 저자 직접 수행 통제 실험 + 10차원 정량 평가. 벤치마크 방법론 상세 논문화. 제3자 독립 재현 없음 (2026-04 기준).

---

## 10. Failure Modes & Limits

**저자 인정/설계상 제약**:
- **실험적 기능 의존**: Agent Team 모드는 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 필요. 안정적 프로덕션 환경에서 불안정 가능성.
- **생성된 팀 품질 = 메타-스킬 품질**: Harness가 잘못된 도메인 분석을 하면 생성된 팀 전체가 오염. "garbage in, garbage in × 팀 규모"
- **CLAUDE.md 오염 위험**: Phase 5.4에서 명시적으로 "목록/구조/상세 규칙 금지" 지시를 내린 것 자체가, 제약하지 않으면 오염이 발생한다는 방어 설계임.
- **Drift 탐지 의존**: Phase 0 감사가 `.claude/` 디렉토리 상태에 의존 — 외부 수동 편집 후 재실행 시 충돌 가능.

**미해결 질문**:
- 제3자 독립 재현 실험 없음 (2026-04 기준)
- 15개 태스크의 구체적 선택 기준/편향성 미공개
- harness-100 중 특정 도메인 하네스의 실전 품질에 대한 사용자 리뷰 부재 (SkillsLLM에 "pending review")
- Agent Team 모드의 비용(토큰) vs 품질 트레이드오프 미정량화
- 생성된 에이전트 수 × 복잡도 × 실행 비용 관계 미공개

---

## 11. Transferable Primitives ★ (load-bearing)

### P1. Meta-skill as harness bootstrapper
- 하나의 스킬 파일이 실행되어 도메인별 스킬·에이전트 파일 전체를 산출.
- 전제: Claude Code SKILL.md 런타임, 파일 생성 권한.
- **YES** (standalone-extractable). "내 도메인에 맞는 팀을 자동 생성하는 부트스트래퍼" 패턴은 어느 복잡한 멀티에이전트 시스템에도 적용 가능.

### P2. Phase-0 state audit before every execution
- 첫 Phase에서 기존 아티팩트(.claude/ 디렉토리 + CLAUDE.md 기록)를 감사하고, 신규/확장/유지보수 3가지 실행 경로 중 하나를 선택.
- 전제: 아티팩트가 파일시스템에 지속됨.
- **YES**. Ralph의 IMPLEMENTATION_PLAN.md 재독과 같은 계열이나, 3-way 분기와 드리프트 탐지가 추가.

### P3. Progressive Disclosure for context management
- 메타데이터 항상 로드 → 스킬 본문 트리거 시만 → references/ 조건부 → scripts/ 자체 포함.
- 전제: 스킬 파일 구조가 레이어로 분리되어 있음.
- **YES**. 어느 스킬 시스템에도 이식 가능한 컨텍스트 절약 계층 모델.

### P4. "Pushy" description as trigger precision engineering
- 스킬 description에 트리거 상황 + near-miss 구별을 명시 → 자동 호출 정확도 향상.
- 전제: 에이전트가 description을 기반으로 스킬을 자동 선택.
- **YES**. should-trigger / should-NOT-trigger 8–10개 검증 테스트와 조합하면 높은 트리거 정확도.

### P5. 6 architecture patterns as a design vocabulary
- Pipeline / Fan-out/Fan-in / Expert Pool / Producer-Reviewer / Supervisor / Hierarchical Delegation — 도메인 독립적 팀 구성 어휘.
- 전제: 멀티에이전트 시스템 설계 컨텍스트.
- **YES**. 어느 에이전트 오케스트레이터에도 설계 참고 어휘로 이식 가능.

### P6. Team size heuristics (2-3 / 3-5 / 5-7 + tasks per agent)
- 소(2–3), 중(3–5), 대(5–7). 에이전트당 3–6 태스크. 팀 규모와 작업 분배의 경험적 가이드라인.
- 전제: Agent Team 패턴.
- **PARTIAL** — 수치는 하네스 생성 컨텍스트에서 도출됨. 일반화 가능하나 벤치마크 없음.

### P7. CLAUDE.md as minimal pointer register (trigger + changelog only)
- CLAUDE.md에 에이전트/스킬 목록·디렉토리 구조·상세 규칙 금지. 트리거 규칙 + changelog만.
- 전제: 에이전트가 CLAUDE.md를 매 실행마다 읽는 구조.
- **YES**. Ralph의 AGENTS.md 분리 원칙과 같은 계열이지만 "더 작게" 제약.

### P8. Complexity-scales-benefit empirical claim
- Basic(+23.8) → Advanced(+29.6) → Expert(+36.2): 복잡할수록 구조 사전 설정의 효과가 커진다.
- 전제: 자신의 실험 데이터.
- **PARTIAL** (제3자 재현 대기). 직관적으로 타당하지만 독립 검증 없음.

### P9. QA agent as boundary-crossing comparator (not existence checker)
- Phase 3 명시 지시: QA 에이전트는 "경계 넘는 비교"를 해야 하며 단순 존재 확인에 그치면 안 됨. General-purpose 타입 사용.
- 전제: QA 에이전트를 멀티에이전트 팀에 포함할 때.
- **YES**. QA 에이전트 설계 원칙으로 독립 이식 가능.

### P10. Phase-7 evolutionary feedback routing
- 피드백 유형에 따른 라우팅: 결과 품질→스킬, 역할 공백→에이전트 정의, 워크플로→오케스트레이터, 구성→양쪽.
- 전제: 하네스가 진화해야 하는 맥락.
- **YES**. "피드백을 어디에 반영할지" 라는 결정 프레임으로 일반화 가능.

---

## 12. Open Questions

- **15개 태스크 선택 기준**: 어떤 소프트웨어 엔지니어링 태스크인지, 편향 제거 방법론 공개 여부 미확인 (실험 repo YAML 직접 열람 필요)
- **제3자 독립 재현**: 2026-04 기준 없음. 100% 승률 주장의 외부 검증 필요.
- **Agent Team 모드 비용**: 팀 실행의 토큰 비용 대비 품질 트레이드오프 미정량화.
- **harness-100 실전 품질**: 자동 생성된 100개 도메인 하네스에 대한 사용자 리뷰 없음.
- **한국 커뮤니티 독립 사용 사례**: Threads/choi.openai 언급(하네스 일반론), haandol.github.io(하네스 엔지니어링 개념) — revfactory 직접 언급 없음. 국내 기술 블로그 직접 적용 사례 미발견.
- **비-Agent-Team 모드 품질**: Subagent/Hybrid 모드 시 same 15-task 결과 미공개.
- **Kakao 내부 적용 여부**: 황민호가 Kakao 전략팀 리더이나, 내부 적용 여부 공개 불명.

---

## Sources

### Primary
- https://github.com/revfactory/harness — 메인 저장소 (README.md, SKILL.md, README_KO.md)
- https://github.com/revfactory/harness-100 — 100-harness 라이브러리
- https://github.com/revfactory/claude-code-harness — 실험 저장소 (experiments/, paper/)
- https://revfactory.github.io/harness/ — 공식 랜딩 페이지
- https://github.com/revfactory — 저자 프로필

### Secondary / Community
- https://skillsllm.com/skill/harness — SkillsLLM 인덱스 (2,386 ⭐ 기록)
- https://madplay.github.io/en/post/harness-engineering — 한국 개발자 하네스 엔지니어링 개념 설명 (revfactory 미언급)
- https://haandol.github.io/2026/03/15/harness-engineering-beyond-context-engineering.html — 한국 블로그 (revfactory 미언급)
- https://www.threads.com/@choi.openai/post/DVlRvk8jWdw/ — 한국 Threads 하네스 일반 논의

---

## Candidate Axis Reuse Notes

### 축 C (Mode splitting) — 재사용 확인
Harness의 Phase 0 3-way 분기(신규/확장/유지보수), Phase 2.1의 실행 모드(팀/서브에이전트/하이브리드) — 모드 분리의 **7번째 독립 사용** (Superpowers/GSD/Ouroboros/Ralph/gstack/ECC에 이어).

### 축 F (Skill as unit of discipline) — 재사용 확인
SKILL.md YAML frontmatter(`name`, `description`), Pushy description 원칙, Progressive Disclosure 레이어, 500줄 상한, near-miss trigger 검증 — 축 F의 **4번째 독립 사용** (Superpowers/gstack/ECC에 이어). **승격 최강**.

### 축 K (Role perspective as constraint surface) — 재사용 확인
Phase 3: 전문화 에이전트 역할 정의 (각 에이전트가 domain-specific 역할과 입출력 프로토콜을 가짐). harness-100의 978개 에이전트 정의 — 역할을 1차 제약 대상으로 삼는 구조. **3번째 독립 사용** (gstack, ECC에 이어).

### 축 A (Iteration-boundary semantics) — 약한 재사용
Phase 7 진화 사이클이 이터레이션 경계 의미론을 가짐 (피드백→라우팅→변경→changelog→검증). 단, Harness의 주 사이클이 단일-실행 파이프라인이므로 Ralph/GSD/Ouroboros의 반복 루프 패턴과 차이 있음. **약한 재사용** (카운트 보류).

### 신규 후보 축: Meta-skill bootstrapping
위 "Proposed schema deltas" 참조. ECC의 `/skill-create`와 부분 겹침이 있어 독립 후보 vs. ECC 축 L(instinct learning)의 변종인지 추가 비교 필요.
