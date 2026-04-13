---
title: Harness Synthesis — Tier 1 Cross-Cutting Insights
date: 2026-04-13
source_notes:
  - notes/harness/ralph-wiggum.md
  - notes/harness/superpowers.md
  - notes/harness/gsd.md
  - notes/harness/ouroboros.md
  - notes/harness/gstack.md
  - notes/harness/ecc.md
  - notes/harness/compound-engineering.md
  - notes/harness/openspec.md
  - notes/harness/revfactory-harness.md
schema_ref: meta/harness_schema.md (v1, 2026-04-13)
status: tier1-synthesis
---

이 문서는 각 하네스의 요약이 아니다. 9개 노트를 함께 볼 때만 드러나는 구조적 패턴을 추출한다. 단일 노트의 주장은 "[하네스명]" 귀속으로, 3자 관찰은 "[관찰자명]" 귀속으로, 여기서의 추론은 "노트 추론"으로 표기한다.

---

## 1. 축별 분포 (Axis distribution)

schema v1의 12개 seed 축과 후보 추가 축(A–M)에 대한 9개 하네스의 분포.

### Seed 축 12개 (모든 노트가 1–12를 사용)

모든 하네스 노트가 축 1–12를 사용했으나 항목 밀도가 다르다.

**밀도 상위**: 축 4(State & context), 축 5(Prompt strategy), 축 11(Transferable primitives). 설계 핵심이 이 세 축에 집중된다.

**밀도 하위**: 축 9(Empirical claims). 9개 하네스 전체에서 통제된 벤치마크는 revfactory/harness가 유일하다(자기수행, 15 태스크, 10차원 평가). 나머지 8개는 일화·스타수·스크린샷 의존.

---

### 후보 축 A–M 분포

| 축 | 이름 | 하네스 수 | 사용 하네스 | 1줄 관찰 |
|---|---|---|---|---|
| **A** | Iteration-boundary semantics | 4 | Ralph, GSD, Ouroboros, Compound-Engineering | 매체만 다름(파일/스폰/이벤트/학습문서). 경계 처리 자체는 보편 |
| **B** | Backpressure mechanism | 2 | Ralph(N reader:1 writer), Ouroboros(Dialectic Rhythm Guard) | 희귀. 병렬화를 적극 쓰는 두 곳만 명시적 백프레셔 규칙 갖춤 |
| **C** | Mode splitting | 9 | 전체 | **유일하게 9개 모두 해당.** 단 2-way(Ralph)에서 7-way(Superpowers)까지 폭이 큼 |
| **D** | Gate mechanism syntax | 7 | Ralph, Superpowers, GSD, Ouroboros, gstack, OpenSpec, revfactory | 게이트 형태만 다름: CAPS호통/XML태그/숫자임계값/페이즈enum/allow-list |
| **E** | Authoritative process medium | 4 | Superpowers(DOT), OpenSpec(RFC2119+Gherkin), revfactory(SKILL.md 명령형), gstack(자연어 numbered steps) | 매체 선택이 Claude vs 다른 모델 범용성에 영향 가능성 |
| **F** | Skill as unit of discipline | 5 | Superpowers, gstack, ECC, Compound-Engineering, revfactory | 빠른 수렴. Anthropic Skills 기판 위 컨벤션 레이어로 5개가 독립 구현 |
| **G** | Execution environment as constraint surface | 3 | GSD, Ouroboros(입력측), ECC(hook profile) | tentenco의 3-축 프레임(Process/Environment/Perspective)에서 "Environment" 포지션 |
| **H** | Artifact naming schema as protocol | 2 | GSD(`{PHASE}-{WAVE}-{TYPE}.md`), gstack(`.tmpl` vs `.md` 역할 인코딩) | GSD만 강한 사용. H 승격 근거 약함 |
| **I** | Ambiguity-as-numeric-gate | 1 | Ouroboros 전용 | 정량 게이트는 현재 유일. 이식 시 측정 함수가 블랙박스임이 문제 |
| **J** | Deferred-tool loading protocol | 1 | Ouroboros 전용 | MCP late-binding 컨벤션. Claude Code 생태계 특이적 |
| **K** | Role perspective as constraint surface | 4 | gstack, ECC, Compound-Engineering, revfactory | tentenco 프레임의 "Perspective" 포지션. 빠른 수렴 |
| **L** | Instinct learning as harness layer | 2 | ECC(`/learn`→`/evolve`), Compound-Engineering(`/ce:compound`→genetic search) | 구현 매체 다름(신뢰도 수치 vs YAML 마크다운)이지만 메타루프 패턴 동일 |
| **M** | Meta-skill bootstrapping | 1 | revfactory/harness 전용 | 하네스가 하네스를 낳는 패턴. 현재 단독 |

**관찰**: C는 전체 커버, F·K는 5개 이상으로 빠른 수렴, A·L은 4·2개로 승격 임계값 충족. I·J·M은 단독으로 고유성 높은 실험.

---

## 2. 설계 공간의 주요 축 (Key design dimensions)

스키마 축과 다른 레이어다. 하네스 저자들이 실제로 선택을 해야 했던 설계 긴장점 5개.

---

### D1. Fresh context 확보 방식: 시간 vs 공간

**설명**: "컨텍스트 오염을 피하기 위해 fresh window를 언제 어떻게 만드는가"라는 선택.

**시간 극 (Ralph)**: `while true` bash 루프로 매 이터레이션 컨텍스트를 완전 와이프한다. 이터레이션은 시간축에서 직렬로 온다.
- 얻는 것: 극단적 단순성. bash 스크립트 1개면 충분. 어떤 런타임에도 이식.
- 잃는 것: 병렬화 불가. 진행이 느리고 비용이 선형 증가.

**공간 극 (GSD v2, Superpowers, Compound-Engineering)**: `Task()` 스폰으로 독립 컨텍스트를 공간적으로 분기한다. 병렬 웨이브가 가능하다.
- 얻는 것: 속도, 병렬화, 오케스트레이터 컨텍스트 보존.
- 잃는 것: 런타임 의존성(Task API, subagent 비용), 오케스트레이터-서브에이전트 통신 복잡도.

**중간 위치 (Ouroboros, OpenSpec)**: Ouroboros는 MCP 서버 EventStore를 통해 stateless evolve_step을 반복하는 혼합. OpenSpec은 change 폴더 단위로 격리하되 단일 에이전트 모델.

**노트 추론**: 두 극은 실제로 다른 문제를 풀고 있다. Ralph의 "시간 직렬"은 간단한 그린필드 반복에 최적. GSD의 "공간 분기"는 복잡한 단일 프로젝트의 병렬 진행에 최적. 스타 수 기준 양쪽 모두 대규모 채택(Ralph 1577, GSD 51.7k)이 공존하는 것이 이를 뒷받침한다.

---

### D2. HITL 위치: 세션 외부 vs 내부 강제 게이트 vs 내부 유연

**설명**: "사람의 판단이 에이전트 루프와 어떻게 맞물리는가"라는 선택.

**외부 극 (Ralph)**: HITL은 세션 사이에서만 일어난다. 실행 중 인간 개입 없음. "Wake up to a broken codebase"가 인정된 실패 모드다. (ralph-wiggum §7)

**내부 강제 극 (Superpowers, Ouroboros)**: Superpowers는 `<HARD-GATE>`로 디자인 승인 없이 구현을 물리적으로 차단한다. Ouroboros는 3연속 코드확인 후 강제로 사람에게 질문을 돌리는 Dialectic Rhythm Guard를 갖는다. (superpowers §7, ouroboros §5)

**내부 유연 극 (GSD, gstack, OpenSpec)**: GSD는 `AskUserQuestion` 툴로 결정 지점에서 질문하되 자동 차단은 아니다. gstack은 "User Sovereignty" 원칙을 선언하지만 각 단계 호출 자체는 사람이 수동으로 한다. OpenSpec은 propose → apply → archive 각 전환을 사람이 리뷰 후 결정한다. (gsd §7, gstack §7, openspec §7)

**중간 (Compound-Engineering)**: `/lfg`는 50+ 에이전트가 PR까지 자동으로 가지만, Plan 승인·Compound 단계 학습 선별은 사람 몫으로 남긴다. 자율성 레벨을 Stage 0→5로 사다리화해 팀이 선택하게 한다. (compound-engineering §7)

**ECC**: 명시적 게이트(`/plan` 승인 대기)가 있으나 장기 루프 중에는 Ralph와 같이 외부 모니터 패턴. (ecc §7)

**노트 추론**: HITL 위치는 "얼마나 자율화할 것인가"보다 "언제 사람의 판단이 가장 비싼가"의 문제다. Superpowers의 강제 게이트는 "설계 실수를 구현 후에 잡으면 비용이 기하급수적"이라는 Vincent의 판단을 반영한다. Ralph의 외부 HITL은 "반복 비용이 싸다"는 Huntley의 판단. 이 선택은 용도(그린필드 반복 vs 복잡한 단기 프로젝트)에 따라 맞는 극이 다르다.

---

### D3. 상태 지속 매체: 파일 하나 vs 구조화 파일 vs 이벤트 스토어

**설명**: "이터레이션 사이에 무엇이 기억을 이어주는가"라는 선택.

**최소 극 (Ralph)**: `IMPLEMENTATION_PLAN.md` 1개 + `AGENTS.md` 1개. 단순하나 파일이 비대해지면 컨텍스트 오염. (ralph-wiggum §4)

**구조화 파일 극 (GSD, OpenSpec, Compound-Engineering)**: GSD는 `.planning/` 아래 7+ 파일로 역할 분리. OpenSpec은 `specs/` + `changes/` 이중 레이어. Compound-Engineering은 `docs/solutions/` YAML 태깅 + `CLAUDE.md` 갱신. 공통점은 "파일명 자체가 상태 머신 노드"인 것. (gsd §4, openspec §4, compound-engineering §4)

**이벤트 스토어 극 (Ouroboros)**: 파일 대신 MCP 서버 EventStore. evolve_step은 stateless이고 상태는 이벤트 리플레이로 재구성. 이론상 rewind 가능. 운영 복잡도 높음. (ouroboros §4)

**혼합 (ECC)**: SQLite + instinct store + session adapter 중첩. 풍부하지만 디버깅 복잡. (ecc §4)

**노트 추론**: 구조화 파일이 현재 가장 많이 채택된 중간값이다. 완전 단순(Ralph)은 사용자 부담을, 완전 복잡(Ouroboros EventStore, ECC SQLite)은 운영 부담을 전가한다. GSD의 단순한 디렉토리 구조가 넓은 채택을 얻은 것이 이 중간값의 우위를 암시한다. 단, 인과관계는 확인 안 됨.

---

### D4. 프로세스 권위 표현: 자연어 vs 구조화 형식

**설명**: "에이전트에게 무엇을 하라고 말할 때 어떤 언어로 쓰는가"라는 선택.

**자연어 극 (Ralph, gstack)**: Ralph는 Markdown 프로즈. gstack의 CLAUDE.md 원칙은 "Express conditionals as English. Instead of nested if/elif/else, write numbered decision steps." (gstack §5)

**구조화 형식 극 (Superpowers, OpenSpec, Ouroboros)**: Superpowers는 GraphViz DOT을 프로세스의 권위적 표현으로 채택하고 prose를 주석으로 강등했다. "Claude is particularly good at following processes written in dot." (superpowers §5) OpenSpec은 RFC 2119 키워드(MUST/SHALL/SHOULD) + Gherkin(GIVEN/WHEN/THEN). Ouroboros는 SKILL.md frontmatter가 MCP 툴 콜 시그니처를 선언.

**중간 (GSD, Compound-Engineering, revfactory)**: XML 포맷(GSD), YAML frontmatter + 명령형 Markdown(revfactory), 패턴 YAML + CLAUDE.md(Compound-Engineering).

**노트 추론**: Superpowers의 DOT 선택은 "Claude 계열에서만 검증됨"이라는 명시적 제약을 안고 있다. (superpowers §11 P2 rejected 기준) 자연어는 모델 애그노스틱하지만 에이전트가 지시를 창의적으로 해석할 여지가 크다. 현재 이 tradeoff에 대한 통제된 증거는 없다.

---

### D5. 하네스 범위: 단일 문제 집중 vs 전방위 번들

**설명**: "하나의 고통 포인트에 집중할 것인가, 전체 개발 워크플로를 커버할 것인가"라는 선택.

**집중 극 (Ralph, Ouroboros, OpenSpec)**: Ralph는 "그린필드 자동 반복"만. Ouroboros는 "입력 모호성 해소"만. OpenSpec은 "브라운필드 스펙 관리"만. 각자 명확한 하나의 문제를 정의하고 그것만 푼다.
- 얻는 것: 선명한 포지셔닝, 이식성 높음, 다른 하네스와 스택 가능.
- 잃는 것: 단독으로는 전체 워크플로를 커버 못 함.

**번들 극 (ECC, gstack)**: ECC는 47개 에이전트, 181개 스킬, 72개 규칙, 20개+ 훅을 한 설치로 묶는다. gstack은 23+ 슬래시 커맨드로 Think→Reflect 7단계를 커버한다.
- 얻는 것: 설치 1회로 넓은 커버리지.
- 잃는 것: 복잡도, 디버깅 불투명, 토큰 bloat(gstack의 10K+ 토큰 선결비용이 대표 사례). (gstack §10, ecc §10)

**중간 (Superpowers, GSD, Compound-Engineering, revfactory)**: 자신의 핵심 포지션(프로세스 디시플린/컨텍스트 관리/복리 학습/팀 생성)을 갖되, 다른 하네스와 스택되도록 설계됨. tentenco의 "gstack thinks, GSD stabilizes, Superpowers executes" 3각 분업이 이를 대표한다. (gstack §8)

**노트 추론**: 스타 수만 보면 번들이 승리한 것처럼 보인다(ECC 140k, gstack 71k). 그러나 비판도 번들에 집중된다(ECC의 opacity 비판, gstack의 Build 단계 공백). 집중형이 스택의 레이어로 들어가는 패턴이 tentenco/imaginex 등 실무자들의 권고 패턴으로 수렴한다(3자 관찰).

---

## 3. 수렴하는 패턴 (Convergent patterns)

3개 이상의 하네스에서 독립적으로 나타난 패턴. "독립적"이라는 기준은 저자 간 명시적 교차 참조가 없거나 참조가 있더라도 구현 형태가 다른 경우.

---

### CP1. 파일시스템 기반 이터레이션 간 기억

**패턴**: 에이전트 컨텍스트가 리셋되더라도 파일이 기억을 이어받는다.

**하네스별 구현**:
- Ralph: `IMPLEMENTATION_PLAN.md` + `AGENTS.md`. "크로스 이터레이션 기억은 100% 파일 매개." (ralph-wiggum §4)
- GSD: `.planning/` 디렉토리 7+ 파일. STATE.md가 "지금 어디에 있는가"만 담당. (gsd §4)
- OpenSpec: `specs/` + `changes/` + `archive/`. 변경 히스토리의 "왜"까지 보존. (openspec §4)
- Compound-Engineering: `docs/solutions/` + `CLAUDE.md`. 매 이터레이션 학습 추출. (compound-engineering §4)
- revfactory: `.claude/agents/` + `.claude/skills/` + 최소 CLAUDE.md. (revfactory §4)

**왜 중요한가**: 에이전트가 망각해도 작업이 계속 진행될 수 있다는 것은 하네스가 해결하는 가장 근본적인 문제다. 이 패턴이 없으면 모든 세션이 0에서 재시작된다.

**수렴이 놀라운가**: 아니다. 당연한 해법이다. 놀라운 것은 매체 선택의 다양성 — 단일 파일(Ralph), 역할별 분리 디렉토리(GSD), 이중 레이어(OpenSpec), 학습 누적(Compound-Engineering) — 이 모두 파일시스템이라는 동일 기반 위에 세워졌다는 것이다.

---

### CP2. 모드 분리 (Plan/Build/Review를 다른 에이전트 컨텍스트로)

**패턴**: "기획"과 "구현"(그리고 "리뷰")을 같은 컨텍스트에서 혼합하지 않는다.

**하네스별 구현**:
- Ralph: `PROMPT_plan.md` vs `PROMPT_build.md`. plan 모드에서 구현 금지 명시. (ralph-wiggum §5)
- Superpowers: 7-phase DAG. brainstorm → writing-plans → subagent-driven-development 각각 별도 SKILL.md. (superpowers §3)
- GSD: discuss / plan / execute / verify / ship 5-way 분리. 각 phase가 다른 에이전트 타입을 스폰. (gsd §3)
- Ouroboros: interview / seed / execute / evaluate / evolve 5단계. interview가 코드 진입을 gates. (ouroboros §3)
- gstack: Think/Plan/Build/Review/Test/Ship/Reflect 7단계. Build 단계에 skill 없는 것이 역설적으로 이 관심사의 중요성을 드러냄. (gstack §3)
- Compound-Engineering: Brainstorm/Plan/Work/Review/Compound 5단계. (compound-engineering §3)
- OpenSpec: propose / apply / archive 3단계. (openspec §3)
- revfactory: 3-way mode split + Phase-2.1 실행 모드 분기. (revfactory §3)
- ECC: `/plan` vs `/tdd` vs `/code-review` 역할별 스킬. (ecc §5)

**왜 중요한가**: 모드 혼합이 만드는 실패 패턴이 여러 노트에서 보고됐다 — Ralph에서 에이전트가 기획과 구현을 뒤섞어 계획 없이 구현하다가 방향을 잃는 것, Superpowers의 "simple projects are where unexamined assumptions cause the most wasted work." 각 모드는 다른 실패 모드를 막는다: plan-only 모드는 조기 구현을 막고, build-only 모드는 재기획 루프를 막는다.

**수렴이 놀라운가**: 패턴 자체는 전통 소프트웨어 공학(분석-설계-구현-테스트)의 반영이라 놀랍지 않다. 놀라운 것은 **9개 하네스 모두**가 이를 독립적으로 재발견했다는 것이다. 이것은 모드 분리가 "유행하는 아이디어"가 아니라 실제 실패를 막는 load-bearing primitive라는 강한 수렴 증거다.

---

### CP3. 서브에이전트에 "필요한 것만" 전달

**패턴**: 상위 오케스트레이터의 히스토리를 서브에이전트에게 상속시키지 않는다. 서브에이전트는 해당 태스크를 실행하기 위한 최소 컨텍스트만 받는다.

**하네스별 구현**:
- Superpowers: "Each receives 'exactly what they need' without inheriting session history." (superpowers §4)
- GSD: executor 서브에이전트는 `N-M-PLAN.md`만 읽고 `N-M-SUMMARY.md`만 쓴다. 오케스트레이터는 서머리만 읽는다. (gsd §4)
- Compound-Engineering: 14개 리뷰 에이전트 각각이 역할 범위만 리뷰. `/lfg`도 plan 문서가 서브에이전트의 전체 입력. (compound-engineering §3)
- revfactory: "소규모 데이터: Task/Message, 대형 아티팩트: 파일, Subagent 결과: return value." 정보 전달이 분류돼 있다. (revfactory §4)

**왜 중요한가**: Dex/HumanLayer의 Ralph 리프레임("carve off small bits of work into independent context windows")이 이 패턴의 이론적 정당화를 가장 잘 표현한다. (ralph-wiggum §11 P10) 컨텍스트 오염이 서브에이전트 품질 저하의 주요 원인이라면, 격리는 품질 보호의 1차 수단이다.

**수렴이 놀라운가**: 부분적으로 놀랍다. 이 패턴은 직관에 반한다 — 더 많은 히스토리가 더 나은 성능을 줄 것이라는 가정을 뒤집는다. 4개 하네스가 독립적으로 "히스토리 없이 보내는 것이 낫다"는 결론에 도달했다는 것은 컨텍스트 오염 문제가 실질적이고 재현 가능하다는 것을 시사한다.

---

### CP4. SKILL.md 컨벤션 레이어

**패턴**: Anthropic Agent Skills 기판 위에 자체 SKILL.md 포맷 컨벤션을 얹는다. YAML frontmatter + when-only description + 본문이 기본 구조.

**하네스별 구현**:
- Superpowers: `name + description(when-only) + DOT flowchart + HARD-GATE + prose`. (superpowers §5)
- gstack: `name + preamble-tier + version + description + allowed-tools + body`. (gstack §5)
- ECC: 181개 스킬 파일 + progressive disclosure(메타데이터 먼저, 본문 조건부). (ecc §4, §11 P1)
- Compound-Engineering: 13개 스킬 파일, 다중 IDE 변환 레이어. (compound-engineering §8)
- revfactory: "Pushy" description(트리거 상황 + near-miss 구별) + should-trigger 검증 8–10개. (revfactory §5)

**왜 중요한가**: SKILL.md는 현재 Claude Code 생태계의 사실상 표준이 되어가고 있다. 5개 하네스가 같은 기판 위에 서로 다른 컨벤션을 얹었는데, 이 컨벤션들의 공통 방향("when-only description", "body on-demand", "trigger precision")이 있다. 이것은 최적 컨벤션에 대한 수렴이 진행 중임을 의미한다.

**수렴이 놀라운가**: 기판이 같으니 컨벤션이 유사해지는 것은 자연스럽다. 놀라운 것은 revfactory의 "should-NOT-trigger 테스트"처럼 기판이 강제하지 않는 **규율**을 독립적으로 도입했다는 것이다.

---

### CP5. 역할 페르소나로 LLM 시선 고정

**패턴**: LLM에게 "일반 조수"가 아니라 특정 역할(CEO, security reviewer, QA, etc.)을 부여해 판단의 시선을 고정한다.

**하네스별 구현**:
- gstack: 23+ 슬래시 커맨드, 각각 하나의 엔지니어링 역할에 결박. "CEO role focuses on strategy, QA focuses on defects." (gstack §5)
- ECC: 47개 전문화 서브에이전트. code-reviewer 에이전트는 80% 이상 신뢰도 이슈만 리포트. (ecc §11 P5)
- Compound-Engineering: 14개 병렬 리뷰 에이전트 — security-sentinel, performance-oracle, dhh-rails-reviewer. DHH 페르소나는 "controversial suggestions force reconsideration of architectural choices." (compound-engineering §5)
- revfactory: harness-100 978개 에이전트 정의, 각각 도메인별 역할 + 협업 규약. (revfactory §8)
- Ouroboros: 5 lateral thinking personas(Hacker/Researcher/Simplifier/Architect/Contrarian) + 4 core agents + evaluator. (ouroboros §5)

**왜 중요한가**: 역할 고정이 방지하는 것은 "LLM이 모든 것을 동시에 고려하려다 아무것도 제대로 못 하는" 패턴이다. Agent Native의 관찰: "When Claude operates as an engineering manager reviewing code, it ignores feedback about UI colors and focuses on framework choices." (gstack §5) 이것이 리뷰 품질의 핵심 개선 기제다.

**수렴이 놀라운가**: 예상된 수렴이지만 규모가 놀랍다. gstack의 CEO부터 Compound-Engineering의 DHH까지, **실제 인물/직함을 페르소나로 사용**하는 구체적 접근이 수렴한다는 것이 흥미롭다. 추상적 역할명이 아닌 구체적 인물/직함이 모델의 행동을 더 잘 바운드한다는 암묵적 가설이 있는 것 같다.

---

### CP6. 학습의 아티팩트화 (Compound 루프)

**패턴**: 실행 후 "무엇이 작동했고 무엇이 안 됐는가"를 다음 이터레이션이 읽을 수 있는 파일로 추출한다.

**하네스별 구현**:
- Ralph: `AGENTS.md`에 운영 학습 기록. "새로운 운영을 배울 때만" 갱신. (ralph-wiggum §5)
- ECC: `/learn` → `/evolve` → instinct store. 신뢰도 점수화 후 high-confidence를 영속 instinct로 승격. (ecc §5)
- Compound-Engineering: `/ce:compound` → `docs/solutions/` YAML 태깅. 다음 `/ce:plan`에 genetic search로 관련 패턴 재주입. (compound-engineering §3)
- revfactory: Phase 7 "Harness Evolution" — 반복 실패·에이전트 오류·사용자 workaround를 감지해 하네스 자체를 진화. (revfactory §3)

**왜 중요한가**: Compound-Engineering이 이를 가장 명확히 표현한다: "Each unit of engineering work should make subsequent units easier—not harder." (compound-engineering §2) 이 패턴 없이는 모든 이터레이션이 동일한 실수를 반복할 수 있다. Tessmann의 관찰("Agents Don't Commit" 9번 중 1번만 성공)처럼 반복 실패가 프롬프트 튜닝으로도 안 잡히는 케이스가 이 패턴의 필요성을 보여준다.

**수렴이 놀라운가**: 패턴 자체보다 구현 다양성이 놀랍다. Ralph는 수동(운영자가 AGENTS.md를 편집), ECC는 반자동(에이전트가 패턴 추출, 사람이 prune), Compound-Engineering은 에이전트 검색 기반 재주입. 이 스펙트럼이 "자동화 수준 선택"이라는 독립적인 설계 결정임을 드러낸다.

---

## 4. 발산하는 패턴 (Divergent patterns)

반대 방향의 선택을 한 하네스들. 어느 쪽이 옳은가, 또는 컨텍스트 의존인가.

---

### DV1. 퍼미션 모델: YOLO vs Least-Privilege

**선택**: 에이전트에게 모든 툴 권한을 열어줄 것인가, 페이즈/스킬별로 좁힐 것인가.

**YOLO 베팅 (Ralph, Compound-Engineering)**:
- Ralph: `--dangerously-skip-permissions` 글로벌 bypass. "샌드박스는 운영자 책임." (ralph-wiggum §6)
- Compound-Engineering: `--dangerously-skip-permissions` 조건부 권장. "속도 우선, 프로세스 신뢰, 안전한 샌드박스일 때." (compound-engineering §6)

**Least-Privilege 베팅 (GSD, gstack, Superpowers, Ouroboros, OpenSpec)**:
- GSD: `allowed-tools: [Read, Bash, Write, Task, AskUserQuestion]` 페이즈 프론트매터 선언. (gsd §6)
- gstack: 각 skill의 `allowed-tools:` frontmatter + `/careful`, `/freeze`, `/guard` 파괴적 명령 방어벽. (gstack §6)
- Superpowers: 기본 Claude Code 퍼미션 모델 상속. 글로벌 bypass 없음. (superpowers §6)
- OpenSpec / Ouroboros: YOLO 언급 없음. 표준 권한 모델.

**증거**: YOLO 쪽의 실패 사례는 구체적으로 기록됐다. Dex/HumanLayer의 "Hook-brick" — Anthropic 공식 Ralph 플러그인이 state 파일을 삭제해 레포 내 Claude를 영구 브릭. (ralph-wiggum §10) Ralph의 "Wake up to a broken codebase." (ralph-wiggum §10) Devon의 "A numerical limit does not prevent an agent from deleting a database in the second iteration." (ralph-wiggum §10) Least-privilege 쪽의 구체적 비용/실패 사례는 노트에서 발견되지 않았다.

**노트 추론**: 증거의 비대칭이 뚜렷하다. YOLO의 실패 사례는 이름 붙여진 실제 사건(Hook-brick, broken codebase)이고, Least-privilege의 실패는 "느리다"는 이론적 불만 수준이다. 단, YOLO는 그린필드 + 빠른 반복 컨텍스트에서 합리적 선택일 수 있다. 사용 컨텍스트에 따라 다른 결론이 나오는 진정한 tradeoff다.

---

### DV2. 스펙 위치: 코드 위 vs 코드와 동등 vs 코드 아래

**선택**: 스펙(요구사항 문서)을 코드보다 권위 있는 소스 오브 트루스로 볼 것인가.

**스펙 우위 베팅 (OpenSpec, Ouroboros, GSD)**:
- OpenSpec: `specs/`가 소스 오브 트루스. "Structure before code enables long-term architectural consistency." (openspec §2) Archive 없이 다음 세션이 진행하면 이미 완료된 기능을 재구현하는 실패 모드가 보고됨. (openspec §10)
- Ouroboros: Seed YAML이 immutable. Interview를 통해 ambiguity ≤ 0.2 로 낮추기 전까지 코드 진입 금지. (ouroboros §3)
- GSD: `PROJECT.md` + `REQUIREMENTS.md` + `ROADMAP.md` 삼각 구조. 구현 전 require사항 ID 부여. (gsd §4)

**코드가 1차 아티팩트 베팅 (Ralph, gstack 일부)**:
- Ralph: specs는 존재하나 "완벽한 스펙을 쓰는 것보다 루프를 돌려 빠르게 발견하는 것"이 가치. Huntley는 스펙 완성을 루프의 전제조건으로 두지 않는다. (ralph-wiggum §2)
- gstack: "Boil the Lake" 원칙이 "스펙보다 빠른 완전 구현"을 지향. (gstack §5)

**코드와 스펙 동등 베팅 (Superpowers, Compound-Engineering)**:
- Superpowers: brainstorming phase가 design doc을 만들고 그것을 HARD-GATE로 사람이 승인한 뒤 구현 진입. 스펙이 선행하나 immutable이 아님. (superpowers §3)
- Compound-Engineering: "Plans are the new code." 80% 시간을 Plan+Review에 쓴다. 그러나 "95% garbage rate typical" — 첫 구현은 쓰레기가 당연하므로 스펙보다 반복이 1차. (compound-engineering §9)

**노트 추론**: 스펙 우위 vs 코드 우위의 선택은 프로젝트 복잡도와 관련 있다. OpenSpec이 명시적으로 "브라운필드 + 팀"을 타겟으로 하고, Ralph가 "그린필드 + 솔로"를 타겟으로 한다는 것이 이 분기를 설명한다. 복잡할수록 스펙이 앞서야 한다는 직관이 Ouroboros의 "bottleneck is clarity, not capability" 주장과 일치한다. (ouroboros §2)

---

### DV3. 하네스 학습 자동화 수준

**선택**: 하네스가 자신을 자동으로 개선할 것인가, 운영자가 수동으로 개선할 것인가.

**수동 베팅 (Ralph, OpenSpec, gstack)**:
- Ralph의 "tune like a guitar" — 운영자가 실패를 보고 PROMPT.md를 수정. 에이전트가 학습을 추출하지 않는다. (ralph-wiggum §5)
- OpenSpec: archive + 스펙 갱신이 학습이나, 이것도 사람이 주도. (openspec §4)
- gstack: ETHOS.md는 사람이 작성·유지. skill 진화는 maintainer 주도. (gstack §4)

**자동 베팅 (ECC, Compound-Engineering)**:
- ECC: 5-layer observer loop가 반복 패턴을 자동 추출 → instinct로 승격 → sycnhronization에 사용. (ecc §5)
- Compound-Engineering: `genetic search` 에이전트가 solutions를 자동 선별해 다음 plan에 주입. (compound-engineering §5)

**반자동 (revfactory, Superpowers)**:
- revfactory: Phase 7이 피드백 루프를 제공하나 "기회 제공" 수준이지 강제 자동화가 아님. (revfactory §7)
- Superpowers: `writing-skills` 스킬이 "새 스킬 작성법을 가르치는 스킬"로 존재. 반자동 self-improvement. (superpowers §5)

**노트 추론**: 자동 베팅 쪽의 실패 모드가 더 극적이다 — ECC의 NanoClaw v2 내부 불투명(instinct confidence scoring 함수 미공개), memory explosion 위험. (ecc §10) 자동화가 높을수록 디버깅이 어렵다. 수동이 느리지만 더 투명하다. 현재 어느 쪽이 장기 운영에서 더 나은지에 대한 데이터는 없다.

---

## 5. 공백 (Gaps)

9개 하네스 어디도 커버하지 못하는 문제 공간.

---

### GAP1. 멀티-사람 협업 하에서의 에이전트 조율

9개 하네스는 모두 **솔로 개발자 또는 작은 팀**을 암묵적으로 가정한다. OpenSpec이 `bulk-archive`로 충돌 감지를 제공하고 Compound-Engineering이 "Person A creates plan → AI implements → Person B reviews"를 언급하지만, 진짜 다인 개발 워크플로(10인 팀, 기능 브랜치 10개, PR 리뷰 관행, merge 전쟁)를 대상으로 설계된 하네스는 없다. 사람-사람 간 분업이 에이전트 루프와 어떻게 맞물리는지를 1차 설계 목표로 삼은 하네스가 필요하다.

**어떤 하네스가 이 공백을 채울 수 있을까**: HITL을 비동기 리뷰(PR, 코드 리뷰 댓글)와 연결하고, 에이전트가 human reviewer의 코멘트를 입력으로 받아 다음 이터레이션을 조정하는 구조. OpenSpec의 change-folder isolation이 가장 가까운 원시요소다.

---

### GAP2. 레거시 코드베이스 대규모 리팩터링

Ralph는 "There's no way in heck would I use Ralph in an existing codebase"라고 명시한다. (ralph-wiggum §10) OpenSpec이 브라운필드를 타겟으로 하지만 "mature codebase"를 가정하며, 100만 줄 레거시 + 테스트 커버리지 0% + 기술 부채 가득인 시스템에 대한 설계는 없다. GSD의 `/gsd:map-codebase`가 가장 먼 접근이지만 기존 CLAUDE.md 자동 통합도 안 된다. (gsd §8)

**어떤 하네스가 필요한가**: 기존 코드를 이해하고 변경 영향 범위를 추적하며 테스트 없이는 리팩터를 거부하는 구조. Ouroboros의 ambiguity gate를 코드 이해 수준에 적용하는 방향이 실마리가 될 수 있다.

---

### GAP3. 에이전트 비용 예산 관리

Ralph는 "cost escalation"을 실패 모드로 기록하면서 해결책을 제시하지 않는다. (ralph-wiggum §10, beuke.org 인용) Ouroboros의 PAL Router가 3-tier 비용 에스컬레이션을 구현하나 이것은 단일 실행의 비용이고, 멀티-이터레이션 예산("이 세션에서 최대 $X 쓸 것")을 강제하는 하네스는 없다. GSD가 Max ($100–200/month) 플랜을 권장하지만 이것은 가이드라인이지 메커니즘이 아니다. (gsd §10)

**어떤 하네스가 필요한가**: 비용 상한을 입력으로 받고, 남은 예산에 따라 에이전트 수/모델 tier/이터레이션 수를 동적으로 조정하는 budget-aware 오케스트레이터. revfactory의 팀 규모 휴리스틱(2-3/3-5/5-7)이 방향을 보여준다. (revfactory §11 P6)

---

### GAP4. 에이전트 행동의 감사 추적 및 설명가능성

gstack의 "User Sovereignty: AI recommends, Users decide"(gstack §5), Ouroboros의 EventStore(ouroboros §4), OpenSpec의 archive(openspec §4)가 단편적으로 접근하지만, "왜 에이전트가 그 코드를 생성했는가"를 나중에 재현 가능하게 추적하는 감사 인프라를 갖춘 하네스는 없다. 규제 환경(금융, 의료)에서는 이것이 필수다. Angelo Lima가 Compound-Engineering의 "less suitable for regulated environments"를 지적했다. (compound-engineering §10)

---

### GAP5. 실패 감지 및 자동 롤백

Ralph는 "max-iterations is not a safety control"이라는 Devon의 비판을 받았다. (ralph-wiggum §10) ECC의 NanoClaw v2 README에 "detect stuck loops, recover from crashes"가 언급되나 구체 구현은 불투명하다. GSD v2의 stuck loop 감지도 언급되나 v2는 아직 과도기다. (gsd §10) 루프가 발산하거나 코드베이스를 손상시키는 것을 자동으로 감지하고 알려진 양호 상태로 롤백하는 메커니즘이 9개 하네스 중 어디에도 완전히 구현되지 않았다.

---

## 6. 이식 우선순위 매트릭스 (Portability priority matrix)

전체 9개 노트의 "Transferable primitives" 섹션에서 수렴도·독립성·시도 비용 기준 상위 10개.

| Rank | Primitive 이름 | Source harness(es) | Standalone? | Try-cost |
|---|---|---|---|---|
| 1 | **Fresh context per iteration + file-mediated memory** | Ralph(P1), GSD(G4), Superpowers(P5), Ouroboros(P9) | YES | 매우 낮음 — bash 루프 또는 슬래시 커맨드 1개 + PLAN 파일 1개 |
| 2 | **Mode splitting (plan vs build 최소 2-way)** | Ralph(P4), Superpowers(P12), GSD(G3), Ouroboros(seed/execute), gstack, ECC, CE, OpenSpec, revfactory | YES | 매우 낮음 — 프롬프트 2개 파일 분리 즉시 적용 가능 |
| 3 | **Design approval gate before any implementation** | Superpowers(P8), OpenSpec(P4), GSD(G7), gstack(office-hours), Ouroboros(P2) | YES | 매우 낮음 — 시스템 프롬프트 1줄 추가 |
| 4 | **Subagent receives only what it needs (carve-off)** | Ralph(P10-Dex reframe), GSD(G4), Superpowers(P5), CE(P4) | YES | 낮음 — Task() API 있는 런타임에서 즉시 |
| 5 | **CLAUDE.md / AGENTS.md 역할 분리** (운영 학습 파일과 태스크 상태 파일 분리) | Ralph(P7+P8), revfactory(P7), CE(P5) | YES | 매우 낮음 — 파일 2개 만들고 분리 기준만 정하면 됨 |
| 6 | **When-only skill description** (discovery/body 분리) | Superpowers(P4), revfactory(P4 "Pushy"), gstack(description rule) | YES | 매우 낮음 — 기존 SKILL.md description 재작성만으로 |
| 7 | **Role-scoped review** (페르소나 고정 리뷰어) | gstack(P1+P10), ECC(P4+P5), CE(P4), Ouroboros(P7 lateral) | YES | 낮음 — 페르소나 정의 1개 + 프롬프트 수정 |
| 8 | **Compound step** (이터레이션 후 학습 아티팩트화) | CE(P1), ECC(P2 부분), Ralph(P2 수동 버전), revfactory(Phase 7) | YES | 낮음 — `docs/solutions/` 폴더 + 작성 규약만 정하면 됨 |
| 9 | **`allowed-tools:` frontmatter 페이즈별 권한 선언** | GSD(G8), gstack(P6) | YES | 낮음 — SKILL.md에 필드 1개 추가, 런타임이 지원하면 즉시 |
| 10 | **Delta-marker spec format** (ADDED/MODIFIED/REMOVED) | OpenSpec(P1) | YES | 매우 낮음 — 스펙 파일 작성 컨벤션 추가만으로 |

**선발 기준 보충**:
- Rank 1–3: 수렴도 4+ 이상이고 런타임 의존성 없이 Markdown 파일과 프롬프트만으로 즉시 테스트 가능.
- Rank 4–7: 수렴도 3+ 이상이고 Task() API 또는 SKILL.md 지원 환경에서 낮은 비용으로 시도 가능.
- Rank 8–10: 수렴도는 1–2이지만 독립 추출성이 높고 실제 실패 모드를 방지하는 가치가 확인됨.

**제외된 primitive** (이식 권장 안 함): `--dangerously-skip-permissions` (실패 사례 다수, ralph-wiggum §11 Rejected), 서브에이전트 리뷰 mandatory (Superpowers v5.0.6 인라인 롤백이 비용 문제 증명, superpowers §10), NanoClaw v2 블랙박스 채택 (내부 불투명, ecc §11 Rejected).

---

## 7. 메타 관찰 (Meta observations)

위 섹션에 들어가지 않는 하네스 landscape 전체 수준의 관찰.

---

### MO1. 저자 배경이 하네스 포지션을 거의 완벽하게 예측한다

Ralph (Huntley — 독립 개발자, 공개 선언 "I don't code, I vibe") → 최소주의, YOLO, 그린필드 반복.  
Superpowers (Vincent — 오픈소스 개발자, chardet 저자) → TDD 강제, 프로세스 디시플린, 실물 라이브러리 증거.  
gstack (Garry Tan — YC CEO) → 역할 분리, 의사결정 레이어, "스타트업 팀처럼 운영하라".  
Ouroboros (Q00 — 한국, 서울, ZEP 테크리드) → 입력 모호성 우선, 소크라테스적 면접, 정량 임계값.  
revfactory (황민호 — 카카오 AI Native Strategy 팀 리더) → 메타-스킬, 팀 아키텍처 자동화, 논문 수준 실험.  
Compound-Engineering (Klaassen/Shipper — Every.to, B2C SaaS 회사) → 학습 복리, 장기 프로덕트 운영, 사내 사례 중심.

**노트 추론**: 각 저자의 실제 작업 컨텍스트(기술 창업자/OSS 메인테이너/대기업 전략팀/미디어 SaaS)가 하네스의 핵심 설계 선택을 결정한다. 이것은 "어떤 하네스가 더 좋은가"라는 질문이 잘못 설정되어 있다는 것을 시사한다 — 어떤 컨텍스트에 있는 누가 쓰는가가 더 적절한 질문이다.

---

### MO2. 증거 품질이 채택 규모와 반비례하는 경향

채택 규모 순(노트 기준): ECC(140k stars) → Superpowers(150k+ but 94k 확인) → gstack(71k) → GSD(51k) → OpenSpec(39k) → Compound-Engineering(14k) → Ouroboros(2.3k) → revfactory(2.4k) → Ralph(1.6k playbook fork).

통제된 벤치마크 존재 여부: revfactory만 존재(15 태스크, 논문화). 나머지 8개는 일화 + 스타수 + 스크린샷.

**노트 추론**: 이것은 커뮤니티가 실증보다 저자 플랫폼(Garry Tan의 YC 대표직, Affaan의 X 바이럴)과 설치 편의성에 더 강하게 반응한다는 것을 보여준다. Hacker News가 gstack의 "600K LOC" 수치를 "would be considered a huge liability"라고 비판한 것은 (gstack §10) 메트릭 선택 자체가 커뮤니티와 불일치한다는 것을 드러낸다. 가장 증거가 약한 하네스가 가장 많이 채택된다는 역설이 지속되고 있다.

---

### MO3. 한국 저자 2명이 가장 독창적인 포지션을 차지

9개 하네스 중 한국 저자는 Ouroboros(Q00, 서울, ZEP)와 revfactory(황민호, 제주, 카카오) 2개다. 이 둘이 다른 7개 하네스와 가장 다른 포지션을 차지한다.

- Ouroboros: 다른 8개 하네스 중 어느 것도 "입력 모호성을 숫자로 스코어링해 임계값 이하면 코드 진입 금지"를 1차 문제로 설정하지 않는다. EventStore 기반 상태, 소크라테스 면접, 정량 게이트, MCP-first 아키텍처 모두 조합이 독특하다.
- revfactory: "하네스를 생성하는 하네스"는 다른 8개 어디에도 없다. 15 태스크 통제 실험 + 논문화도 유일. harness-100의 978개 에이전트 + 1808 파일 규모도 독보적.

**노트 추론**: 3자 커버리지는 두 하네스 모두 얇다 — Ouroboros는 재현/비평 블로그 포스트 없음, revfactory는 SkillsLLM에 "pending review" 상태. 채택 규모도 2k 대이다. 가장 혁신적인 접근이 가장 낮은 가시성을 가진다는 패턴이 반복된다.

---

### MO4. 타이밍 패턴: 2025 하반기 폭발, 2026 수렴

- 2025-07: Ralph (Huntley) — 원시적 while loop
- 2025-10: Superpowers (Vincent) — SKILL.md 컨벤션 확립
- 2025-12: Compound-Engineering (Klaassen) — 학습 루프 개념
- 2026-01: ECC, OpenSpec, Ouroboros — 다층 번들/스펙 관리/소크라테스 게이트
- 2026-02~03: gstack, GSD — 역할 페르소나/컨텍스트 관리 대중화
- 2026-04(분석 시점): revfactory — 메타-스킬 + 논문화

**노트 추론**: Ralph가 "최소주의 가능성"을 증명하자 6개월 내에 복잡도가 급증했다. Superpowers의 SKILL.md 컨벤션이 사실상 표준으로 자리 잡은 것이 2025-10 이후 5개 하네스가 같은 포맷을 채택한 것으로 보인다. 2026-03~04의 GSD/gstack 붐은 스타 수 경쟁으로 보이며, 그 배경에 저자 플랫폼(Garry Tan, Lex Christopherson의 소셜 마케팅)이 있다. revfactory의 논문화는 "바이럴이 아닌 증거로 승부"하는 다른 경로의 시작일 수 있다.

---

### MO5. 스태킹 담론이 커뮤니티에서 먼저 출현했다

하네스들 자신이 서로를 대체제로 포지션하지 않는다. 오히려 커뮤니티 관찰자(tentenco/Ewan Mak, dev.to imaginex, heyuan110)가 "gstack thinks, GSD stabilizes, Superpowers executes"(gstack §8), "OpenSpec handles planning, Superpowers handles coding discipline"(openspec §8) 같은 스태킹 레시피를 먼저 개발했다. 하네스 저자들은 자신의 사용 사례에 집중하고, 커뮤니티가 조합법을 발견한다.

**노트 추론**: 이것은 harness landscape이 하나의 winner-takes-all 경쟁이 아니라 레이어별로 특화된 도구들의 생태계로 수렴하고 있음을 시사한다. 가장 실용적인 사용자는 이미 단일 하네스를 선택하지 않는다.

---

### MO6. "완전한 워크플로"의 정의 불일치

"엔드투엔드 하네스"를 표방한 여러 하네스가 서로 다른 단계를 커버하지 못한다.

- gstack: Build 단계 skill 없음. 가장 중요한 실행 단계에서 Claude Code가 기본 모드로 돌아간다. (gstack §3, tentenco 3자 관찰)
- Ralph: 그린필드 90% ceiling. 마지막 10%는 사람이 마감. (ralph-wiggum §10)
- GSD 단독: "does not directly produce code, run tests, or open a PR." Context anchor 역할이지 shipping 도구가 아님. (gsd §8, tentenco)
- OpenSpec: 단일 에이전트 모델 + 코드 리뷰 내장 없음. (openspec §3, bswen)

**노트 추론**: 9개 하네스 중 어느 것도 "다 커버"하지 못한다. 이것은 설계 실패가 아니라 포지셔닝의 정직함일 수도 있다. 그러나 이 공백을 메우기 위해 사용자가 조합하거나 커버되지 않는 부분을 수동으로 처리해야 한다는 것은 채택 비용의 숨겨진 요소다.
