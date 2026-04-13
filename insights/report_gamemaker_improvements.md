---
title: Bundle_GameMaker 개선 리포트
date: 2026-04-13
based_on:
  - insights/project_map_gamemaker.md
  - insights/graft_tier1_to_gamemaker.md
  - insights/synthesis_tier1.md
---

# Bundle_GameMaker 개선 리포트

---

## 1. 번들 전체를 한 눈에

Bundle_GameMaker는 두 개의 상호 보완적인 시스템이 하나의 목표를 향해 작동하는 구조다. **GameMaker**는 제품 측이다. 7개 부서(Design, Narrative, Programming, Art, Sound, LevelAssembly, QA)로 구성된 AI 워크포스가 Creative Director의 지휘 아래 Unreal Engine 5 게임 프로젝트를 5단계 파이프라인으로 생산한다. **GameMakerEngine**은 연구개발 측이다. Arena(R1 빠른 필터 + R2 심층 LLM 심사관)에서 에이전트 간 경쟁 토너먼트를 돌리고, Evolver가 6가지 돌연변이 전략으로 우승 에이전트를 변이시켜 champion을 Bridge로 배포하면 GameMaker가 다음 실행부터 그 에이전트를 자동으로 사용한다. 두 시스템을 감시하는 **CollabMonitor_Codex**와 **EngineHelper_Codex** 레이어가 다음 액션을 결정하고 인간 오퍼레이터에게 경과를 보고한다. **bridge/**와 **uuuSanAI_bridge-types/**는 이 모든 흐름의 교환 계층과 TypeScript 스키마 계약을 담당한다.

현재 번들은 북극성(The Last Rite 플레이어블 전투 루프 산출)을 향해 구조 설계는 완성됐지만 실행은 멈춰 있는 상태다. Engine 스냅샷이 604분째 오래됐고, Helper 스냅샷은 699분이다. Monitor의 최근 추천 액션은 `helper-review`이며 helper_efficacy는 `low`다. GameMaker의 핵심 컴포넌트 4개(Director, Shared Infrastructure, Human Interface, Engine Adapter)는 미착수다. 번들이 완성된 피드백 루프를 갖추고 있음에도 path 마이그레이션 미해결이라는 단일 블로커가 루프 전체를 막고 있다.

---

## 2. 이미 잘 되어 있는 것들

9개 하네스를 수평 비교했을 때 Bundle_GameMaker가 업계 수준 이상으로 갖추고 있다고 판단되는 패턴들이다. 각 판단 근거는 project_map_gamemaker.md의 축 인벤토리와 synthesis_tier1.md의 교차 분포를 기반으로 한다.

**파일 기반 비동기 핸드오프(Bridge protocol, P1)**: Bridge는 로직 없는 순수 파일 저장소다. Engine이 `agents/{version}/`에 쓰고, GameMaker가 읽는다. `manifest.json`은 temp file → rename 방식으로 atomic 갱신된다. 9개 하네스 중 GSD·Compound-Engineering·OpenSpec이 구조화 파일을 상태 매체로 사용하지만, 두 하위 시스템 사이의 교환 계층을 이 수준으로 명시적으로 설계한 하네스는 없다. Bridge는 하네스 공간에서 고유하게 성숙한 패턴이다.

**Manager-Worker subagent 3단계 위임 프로토콜(P3)**: 메인 세션이 계획하고, implementation Agent(worktree)가 실행하고, validation Agent가 리뷰한 후 200자 요약 + PASS/FAIL만 메인으로 돌아온다. 메인은 코드를 직접 읽지 않는다. Superpowers·GSD·gstack이 유사한 sub-agent 패턴을 쓰지만, worktree 격리까지 결합한 3단계 프로토콜을 CLAUDE.md에 명시화한 것은 이 번들이 앞서 있다.

**경쟁적 진화 루프(Arena + Evolver, P8)**: 6가지 돌연변이 전략(exploitation / exploration / crossover / focused / guided_exploration / adaptation)이 9차원 복합 점수를 기준으로 경쟁하고, champion 승진에 +2.0 마진 임계값을 요구한다. synthesis_tier1.md는 L축(Instinct learning as harness layer)에 2개 하네스만 해당된다고 기록한다. ECC의 `/learn`→`/evolve`와 Compound-Engineering의 genetic search가 그것이다. GameMakerEngine의 Arena+Evolver는 이 두 하네스와 동등한 수준의 메타루프를 이미 구조화 코드로 구현했다.

**Preflight 결정 게이트(P6) + Helper cooldown(P9)**: 60초 이상 걸리는 명령 전에 반드시 서면 preflight를 작성해야 하고, 암묵적 진행은 blocking consent로 간주되지 않는다. Helper는 신선한 스냅샷 변화가 없으면 steady-state로 전환해 새 Engine 태스크 발행을 멈춘다. synthesis_tier1.md D2 분석에서 "HITL 내부 강제 극"에 해당하는 하네스는 Superpowers와 Ouroboros뿐이다. 이 번들의 preflight gate는 Superpowers의 HARD-GATE와 동등한 역할을 한다.

**Rule-persistence discipline(P10)**: Monitor CLAUDE.md는 "memory-only promise"를 금지하고, 새 행동 규칙은 발견한 턴 안에 CLAUDE.md에 기록하도록 강제한다. 이 규칙 자체가 CLAUDE.md에 명시돼 있어 자기 강화적이다. synthesis_tier1.md에서 이 수준의 자기강화 규칙 지속 원칙을 명시한 하네스는 없다.

**Provider Router + cross-review(P7)**: Engine은 `RoutedLlmClient`로 Claude/Codex 간 교차 리뷰를 수행하고, `ProviderIntelligence` 레이어가 데이터 기반 라우팅 추천을 제공한다. 9개 하네스 중 multi-provider 라우팅을 이 수준으로 설계한 하네스는 없다.

---

## 3. 개선 기회 영역

graft 판정 결과(GRAFT 또는 PARTIAL)를 사람이 이해할 수 있는 언어로 풀어 설명한다. 각 항목은 지금 왜 아쉬운지, 어느 하네스에서 검증됐는지, 적용하면 무엇이 달라지는지, 난이도를 포함한다.

---

### 3-A. SKILL.md 위임 프로토콜 (Primitive #1, #4, #9)

**지금 왜 아쉬운가**: `GameMakerEngine/CLAUDE.md:82-97`과 `GameMaker/CLAUDE.md:43-62`에는 3단계 위임 프로토콜이 프로즈로 서술돼 있다. "vitest를 메인 스레드에서 직접 실행하지 말 것"이라는 규칙도 같은 방식으로 기록돼 있다. 프로즈 규칙은 에이전트가 실행 전에 조회하는 것이 아니라 실행 중에 참고하는 것이기 때문에, 같은 anti-pattern이 반복된다. graft 평가는 이것을 Pain Point 8로 명시하고 있다.

**어느 하네스에서 검증됐는가**: Superpowers(P4), gstack, revfactory(P4), ECC(P1) — synthesis_tier1.md 축 F 분포에서 5개 하네스가 독립적으로 SKILL.md 컨벤션을 수렴 구현했다는 것은 이 패턴이 Claude Code 런타임 위에서 보편성을 가진다는 신호다.

**적용하면 무엇이 달라지는가**: `.claude/skills/delegate-implementation.md`에 `anti-trigger: "never run vitest directly from main session"`을 명시하면 에이전트가 태스크 실행 전에 anti-trigger를 체크한다. 더불어 `allowed-tools: [Task, Read]` frontmatter가 메인 스레드에서 호출 가능한 툴을 제한해, worktree 격리가 코드 레벨이 아닌 permission 레벨에서도 강제된다. 향후 Helper가 새 패턴을 만들면 skill 파일 하나를 추가하는 것으로 충분하고, 같은 패턴이 Engine과 GameMaker 양쪽에 일관되게 적용된다.

**난이도**: 낮음. 코드 변경 없음. 기존 CLAUDE.md 프로즈는 fallback으로 유지 가능. 파일 2개 생성 + CLAUDE.md 2개 참조 추가.

---

### 3-B. Monitor 액션 타입 Typed Gate Enum (Primitive #6)

**지금 왜 아쉬운가**: Monitor의 4가지 액션 타입(`engine-self-progress`, `engine-helper-followup`, `helper-review`, `pause`)은 현재 프로즈로만 설명된다. "모호한 진행 = blocking consent"라는 실패 모드가 CLAUDE.md에 명시돼 있지만, 어떤 액션이 blocking인지 non-blocking인지를 프로즈 없이 판단할 수 없다. 오퍼레이터가 `helper-review` 추천을 받았을 때 이것이 blocking consent가 필요한지 아닌지 명확하지 않다.

**어느 하네스에서 검증됐는가**: Superpowers의 HARD-GATE XML 태그 패턴. synthesis_tier1.md D2에서 내부 강제 HITL의 대표 구현체로 인용됐다.

**적용하면 무엇이 달라지는가**: `CollabMonitor_Codex/CLAUDE.md`에 typed enum 블록 하나를 추가하면, Monitor가 액션을 추천할 때 NON-BLOCKING / HARD-GATE 레이블을 함께 표기하게 된다. `human-review` 추천이 나올 때 오퍼레이터 리포트에 "HARD-GATE: explicit operator confirmation required before proceeding"이 나타나야만 다음 단계로 진행 가능해진다. 실제 코드 변경 없이 Monitor의 의사결정을 감사 가능하게 만든다.

**난이도**: 매우 낮음. CLAUDE.md 5줄 수정.

---

### 3-C. Monitor 상태 파일 명명 규칙 (Primitive #3)

**지금 왜 아쉬운가**: `CollabMonitor_Codex/state/`에는 `monitor_brief.md`, `next_work_brief.md`, `operator_report.md`, `state_digest.md`, `operator_memory.md`, `north_star.md`, 그리고 복수의 `*_handoff.md` 파일이 혼재한다. 파일을 열지 않으면 어느 파일이 오래됐는지, 어느 파일이 현재 태스크와 연관됐는지 알 수 없다. 스냅샷이 604분째 오래된 상황(Pain Point 6)에서 어느 파일을 먼저 봐야 하는지가 파일명으로 드러나지 않는다.

**어느 하네스에서 검증됐는가**: GSD(G2)의 `{PHASE}-{WAVE}-{TYPE}.md` 명명 컨벤션. synthesis_tier1.md H축에서 GSD만 강하게 이 패턴을 사용한다고 기록됐으나, 파일 수가 많은 Monitor 상태 디렉터리에는 적합도가 높다.

**적용하면 무엇이 달라지는가**: 새 파일부터 `{ROLE}-{LIFECYCLE}.md` 규칙을 적용하면(기존 파일 이름 변경 없이 forward-only), 오퍼레이터가 `state/` 디렉터리 목록만 봐도 어느 파일이 stale인지, 어느 파일이 active인지 파악할 수 있다. 디버깅 시간이 단축되고, path migration 블로커(Pain Point 1)가 어느 상태 파일에 기록돼 있는지 즉시 식별 가능해진다.

**난이도**: 낮음. 기존 파일 이름 변경 없음. 컨벤션 문서를 `state_digest.md` 헤더에 추가하고 CLAUDE.md에 참조.

---

### 3-D. Phase-0 상태 감사 3분기(3-way branch) (Primitive #10)

**지금 왜 아쉬운가**: Monitor는 세션 시작 시 상태 파일을 읽고 액션을 결정한다. 그러나 현재 상태 파일 읽기 이후에 "이번 세션이 신규인가, 진행 중인 태스크를 연장하는 것인가, 아무것도 달라지지 않은 steady-state인가"를 명시적으로 분류하지 않는다. 그 결과 동일한 상태(path migration 미해결)에서 동일한 추천(`helper-review`)이 반복 발행되고, helper_efficacy가 `low`로 기록된다(Pain Point 5).

**어느 하네스에서 검증됐는가**: revfactory의 Phase-0 state audit 패턴. graft 평가에서 Fit 4/5로 평가됐다.

**적용하면 무엇이 달라지는가**: `CollabMonitor_Codex/CLAUDE.md`에 4줄을 추가해 "FIRST-RUN / ACTIVE-EXTEND / STEADY-STATE" 분류를 의무화하면, STEADY-STATE로 분류되는 세션에서 Monitor가 기본적으로 `pause`를 선택하게 된다. helper_efficacy 지표가 이미 오래된 상태를 반복 리뷰하는 낭비를 줄인다. 오퍼레이터 리포트 첫 줄에 분류가 표기되므로 이력 추적도 가능해진다.

**난이도**: 낮음. CLAUDE.md 4줄 추가.

---

### 3-E. Helper 세션 학습 artifact — Compound step (Primitive #2)

**지금 왜 아쉬운가**: GameMakerEngine의 Evolver는 cross-cycle 진화를 담당하지만, 단일 세션 내에서 발생한 실패(path migration, zero-task materialization)는 다음 세션에 자동으로 전달되지 않는다. Helper가 새 세션을 시작할 때마다 동일한 실패를 재발견할 가능성이 있다. 이것이 helper_efficacy 저하의 구조적 원인 중 하나다.

**어느 하네스에서 검증됐는가**: Compound-Engineering(P1)의 `docs/solutions/` YAML 태깅 루프, ECC(P2)의 `/learn`→`/evolve` instinct capture. graft 평가는 ECC의 자동화 버전을 reject하고(오퍼레이터 레이어가 불투명함), Compound-Engineering의 수동 YAML 마크다운 방식을 Fit 4/5로 채택 추천했다.

**적용하면 무엇이 달라지는가**: `EngineHelper_Codex/docs/solutions/`에 YAML frontmatter 스키마를 정의하고, Helper cycle 종료 시 새 실패 모드나 해결 패턴을 `.md` 파일로 기록하면 두 가지 효과가 생긴다. 첫째, path migration(Pain Point 1)은 `category: path-issue, resolved: false`로 태깅되어 Monitor의 다음 오퍼레이터 리포트에 "미해결 학습 항목"으로 요약된다. 둘째, Evolver의 cross-cycle 진화와 두 개의 학습 계층(per-session + cross-cycle)이 공존하게 된다. 이것이 synthesis_tier1.md L축의 partial gap을 완전히 채운다.

**난이도**: 낮음. 디렉터리 생성, README.md 스키마 정의, CLAUDE.md 2곳에 한 줄 추가. 기존 코드 수정 없음. 단, Primitives #1-#4가 먼저 안정화된 후 적용을 권장한다(graft 평가 의존성 기록).

---

### 3-F. GameMaker Provider Router 완성 (Pain Point 3)

**지금 왜 아쉬운가**: Engine에는 `RoutedLlmClient`, `ProviderIntelligence`, `quality-signals.ts`, `review-prompts.ts`, Intelligence types가 모두 있다. GameMaker에는 router/tracker/log만 있고 나머지 4개 컴포넌트가 없다. `bridge/routing-upgrade-spec.md`에 10단계 이식 작업 지시서가 있다. Engine과 GameMaker가 동일한 Provider Router를 사용할 때까지 cross-review의 품질 신호가 Bridge를 통해 일관되게 흐르지 않는다.

**어느 하네스에서 검증됐는가**: 하네스 공간에 직접 대응하는 패턴은 없다. 이것은 번들 자체의 내부 gap이다. 다만 synthesis_tier1.md G축(Execution environment as constraint surface)과 일치한다 — 어떤 LLM이 어떤 태스크를 실행하는지를 명시적으로 제어하는 것이 3개 하네스에서 확인된 패턴이다.

**적용하면 무엇이 달라지는가**: `bridge/routing-upgrade-spec.md`의 10단계 작업 완료 시 GameMaker의 7개 부서가 Engine과 동일한 cross-review quality signal을 발행하게 되고, Evolver가 GameMaker 실행 결과를 더 정확하게 피드백 받는다. Bridge의 metrics 흐름이 완전해진다.

**난이도**: 중간. 코드 이식 작업이 포함된다. Director가 미착수인 상태에서 선행할 수 있는 작업이지만, Engine쪽 구현을 참조 구현으로 사용하면 이식 위험이 낮다.

---

## 4. 적용 순서 제안

### Quick win — 한 세션에서 완료 가능

이 세 가지는 코드 변경 없이 CLAUDE.md와 state 파일 수정만으로 완료되며, 서로 의존성이 없다.

1. **Typed gate enum in Monitor CLAUDE.md (Primitive #6)** — 5줄 수정. `CollabMonitor_Codex/CLAUDE.md:17-22`에 ACTION_TYPES 블록 추가 및 HARD-GATE 마커 도입. 다음 Monitor 실행에서 즉시 효과 확인 가능.
2. **Phase-0 상태 감사 (Primitive #10)** — 4줄 추가. `CollabMonitor_Codex/CLAUDE.md:13-15`에 3-way 분류 지시 추가. helper_efficacy 저하 원인 중 하나인 반복 추천 문제를 구조적으로 개선.
3. **vitest anti-trigger SKILL.md (Primitive #1, 범위 축소)** — `GameMakerEngine/.claude/skills/delegate-implementation.md` 파일 하나 생성. anti-trigger 1개 + allowed-tools frontmatter. 가장 자주 반복되는 behavioral trap을 즉시 차단.

이 세 가지를 Quick win으로 묶는 이유: 모두 `CollabMonitor_Codex/CLAUDE.md`와 `GameMakerEngine/CLAUDE.md`를 타겟으로 하며, 이 두 파일이 번들에서 가장 많은 documented behavioral trap을 갖고 있다. 부작용 없이 reversible하고, 다음 Monitor 사이클에서 효과를 즉시 측정할 수 있다.

### 다음 단계 — Quick win 안정화 후

4. **SKILL.md 풀 롤아웃 (Primitive #1, #4, #9 전체)** — `GameMaker/.claude/skills/delegate-implementation.md` 추가, "pushy" description과 allowed-tools frontmatter를 Engine + GameMaker 양쪽에 적용. Quick win의 vitest 단독 파일이 효과가 있음이 확인되면 이 단계로 확장.
5. **Monitor 상태 파일 명명 규칙 (Primitive #3)** — forward-only 컨벤션. 기존 파일 rename 없음. 다음에 생성되는 state 파일부터 적용.
6. **GameMaker Provider Router 완성** — `bridge/routing-upgrade-spec.md` 10단계 작업. Engine 구현을 참조 구현으로 사용. 블로커(path migration)가 해소된 후 착수 권장.

### 장기 — Director 컴포넌트가 완성된 후

7. **Compound step 세션 학습 artifact (Primitive #2)** — Primitives #1-#4 안정화 후 적용. `EngineHelper_Codex/docs/solutions/` 생성. 이 단계에서 두 개의 학습 계층(per-session instinct + cross-cycle evolution)이 완성된다.
8. **Role-specialized review subagent (Primitive #5)** — GameMaker Director가 완성된 후에만 의미 있다. 7개 부서별 `.claude/agents/` 파일을 정의하면 generalist LLM 동작을 부서 스코프로 제한할 수 있다.
9. **Wave-parallel subagent execution (Primitive #8)** — Director 완성 후. 7개 부서를 병렬 웨이브로 실행하면 GameMaker 5단계 파이프라인 속도가 크게 향상된다. 단, 현재 DEFER 판정이며 Director 없이는 오케스트레이션 표면이 없다.

---

## 5. 지금 막혀있는 블로커들

### 블로커 1: Bundle_GameMaker path migration 미해결

Monitor의 현재 최우선 태스크는 "Bundle_GameMaker 마이그레이션 후 이동된 path 정규화"다. Engine과 Helper 양쪽에 동일한 high-priority 오픈 태스크가 있다. 하네스 관점에서 보면, 이것은 Primitive #2(세션 학습 artifact)가 없기 때문에 동일한 블로커가 매 Monitor 사이클에 재발견되는 구조다. path migration이 해결되지 않으면 Engine 사이클이 실행될 수 없고, 실행되지 않으면 GameMaker가 새 champion 에이전트를 받지 못하고, 피드백 루프 전체가 정지한다. 이 블로커는 기술 문제이기 전에 상태 추적 문제다 — `state/next_work_brief.md`에 "high priority"로 표기돼 있지만, 어느 파일에 해결 절차가 기록돼 있는지 state 파일 명명 규칙(Primitive #3)이 없어 새 세션마다 재확인이 필요하다.

### 블로커 2: followup-once zero-task materialization

Engine planner가 "Unblock followup-once zero-task materialization"을 두 번째 active 태스크로 표면화하고 있다. 이전 Engine 진행 시도가 실패했고 helper-review 태스크가 오픈 상태다. 하네스 관점에서 이 블로커는 Primitive #6(typed gate enum)의 부재와 관련이 있다. Monitor가 이 태스크를 blocking이 필요한 HARD-GATE 항목으로 표기하지 않으면, 다음 사이클에서 다시 non-blocking helper-review로 위임되고 같은 결과가 반복될 수 있다. followup-once가 시스템 내부 플래그인지, 오케스트레이션 버그인지에 따라 접근이 달라지지만, 현재 Monitor가 이 태스크의 성격을 typed gate로 분류하지 않아 에스컬레이션 경로가 모호하다.

### 블로커 3: MCP 권한 미부여

Phase 6 auto-task 로그에 "MCP 권한 미부여로 도구 호출 건너뜀"이 기록됐다. UE5 Unreal Editor가 실행됐지만 MCP 연결이 승인되지 않았다. 이것은 Primitive #6(typed gate enum)이 없을 때 발생하는 전형적인 패턴이다 — blocking consent가 필요한 MCP 권한 부여가 HARD-GATE 없이 진행을 시도하다가 건너뛰어졌다. `human-review` 액션 타입에 HARD-GATE 마커가 붙으면, MCP 권한 부여가 필요한 시점에 오퍼레이터가 명시적 확인을 요청받게 된다.

### 블로커 4: GameMaker 핵심 컴포넌트 미착수

Director, Shared Infrastructure, Human Interface, Engine Adapter — 4개 컴포넌트가 모두 미착수다. 하네스 관점에서 이것은 Primitives #5(role-specialized review subagent)와 #8(wave-parallel execution)이 적용될 수 없는 전제 조건 미충족 상태를 의미한다. path migration과 MCP 블로커가 해소된 후, 다음 Engine champion이 배포되는 사이클에서 Director 착수 타이밍을 검토할 것을 권장한다. 단, Director 미착수 상태가 지금 당장 Quick win 적용을 막지는 않는다.

### 블로커 5: Engine + Helper 스냅샷 staleness

Engine 스냅샷 604분, Helper 스냅샷 699분. Monitor가 STEADY-STATE 분류(Primitive #10 미적용)를 하지 않기 때문에 stale 상태에서도 helper_efficacy low 상태로 helper-review 추천이 반복된다. 이것은 독립적 기술 블로커가 아니라 Quick win Primitive #10이 해결하는 운영 상태 문제다. Phase-0 분류가 적용되면 STEADY-STATE 세션에서 자동으로 `pause`가 선택되어 low-value cycle 낭비가 줄어든다.

---

*이 리포트는 insights/project_map_gamemaker.md, insights/graft_tier1_to_gamemaker.md, insights/synthesis_tier1.md 세 파일에 기록된 관찰과 판정에만 근거한다. 리포트에 포함된 모든 평가는 해당 파일의 [observed] 귀속 항목으로 추적 가능하다.*
