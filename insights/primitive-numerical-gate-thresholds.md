---
title: Numerical gate thresholds primitive
date: 2026-04-17
based_on: [ouroboros.md, anthropic-effective-harnesses-long-running-agents.md, anthropic-managed-agents.md, superpowers.md, compound-engineering.md, digests/2026-04-17-anthropic-sweep-vs-community-harnesses.md]
confidence: high
tags: [gates, thresholds, premature-completion, primitive]
---

## 한 줄 요약

에이전트의 조기 완료 선언을 막으려면 "완료"는 기본값이 아니라 **증명해야 얻는 것**이어야 하며, 이를 Boolean·수치 임계값·증거 아티팩트 세 레이어로 구조화하면 각 레이어가 서로 다른 실패 모드를 차단한다.

---

## 패턴 / 주장

에이전트가 "완료"를 자기 선언하는 문제(premature victory declaration)는 하네스 설계에서 반복적으로 등장하는 핵심 실패 모드다. 소스들에서 확인된 구조적 해법은 단일 게이트가 아니라 **3종류 게이트의 AND 조합**이다.

### 게이트 유형 1 — Boolean 게이트 (`passes: false` 기본값)

Anthropic의 `effective-harnesses-long-running-agents`는 200+ 피처 항목을 담은 JSON에서 모든 피처를 `"passes": false`로 초기화한다. 에이전트는 E2E 검증을 완료한 후에만 `passes: true`로 전환할 수 있다. 이 설계의 핵심은 **기본값이 실패**라는 점이다. 에이전트가 아무것도 하지 않으면 항상 미완료 상태이므로, 완료를 주장하려면 능동적으로 증명해야 한다.

포맷을 Markdown이 아닌 JSON으로 선택한 이유도 게이트 보호와 연결된다. Anthropic은 명시적으로 "모델이 JSON 파일을 부적절하게 변경하거나 덮어쓸 가능성이 낮음"이라고 밝혔다(ref: `anthropic-effective-harnesses-long-running-agents`). 즉, JSON 자체가 상태 조작에 대한 소극적 저항 레이어다.

적합한 상황: 명세가 이미 완성된 피처 리스트 형태로 존재하고, 각 항목이 독립적으로 검증 가능한 경우.

### 게이트 유형 2 — 수치 임계값 게이트 (Numerical threshold)

Ouroboros(`ouroboros.md`)는 Anthropic이 개념만 제시한 "프로그래밍 방식 게이트"를 숫자로 구체화한 유일한 사례다. 세 임계값이 서로 다른 진행 조건을 차단한다.

- **ambiguity ≤ 0.2** — 인터뷰 단계. 모호성 점수가 0.2를 초과하면 코드 생성 진입 자체를 차단.
- **ontology similarity ≥ 0.95** — 진화 루프. `converged` 상태가 되어 다음 단계로 넘어가려면 온톨로지 유사도가 0.95 이상이어야 한다.
- **drift ≤ 0.3** — 런타임 모니터링. Goal 50% + Constraint 30% + Ontology 20% 가중합으로 계산되며, 이 값이 0.3을 초과하면 세션이 원래 의도에서 이탈했다는 신호가 된다.

다이제스트 D섹션(교차강화 D2)은 이를 명확히 평가한다: "Anthropic 원 포스트에 숫자 임계값 gate 사례가 부재하므로, Ouroboros의 구현이 일반 Prompt Chaining 설계 지침으로 역수입할 가치가 있다"(ref: `digests/2026-04-17-anthropic-sweep-vs-community-harnesses.md`). Anthropic과 Ouroboros는 서로 다른 방향에서 같은 원리에 도달했고, 각자가 상대의 빈틈을 채운다.

적합한 상황: 진행 여부를 이진 판단으로 내리기 어렵고, 연속값으로 측정 가능한 품질 차원이 존재할 때. 예: 모호성, 유사도, 테스트 커버리지, 오류율.

### 게이트 유형 3 — 증거 바운드 게이트 (Evidence artifact)

Anthropic의 Puppeteer MCP E2E 게이트가 이 유형의 원형이다. "코드만 봐서는 불분명한 버그를 식별·수정"했고 "성능이 극적으로 향상(dramatically improved)"했다는 주장의 근거는, 코드 리뷰가 아닌 실제 브라우저 자동화 증거다(ref: `anthropic-effective-harnesses-long-running-agents`). Superpowers의 `<HARD-GATE>` XML 태그 역시 같은 계열이다: "User approves design?" 다이아몬드를 통과하기 전 어떤 구현 액션도 허용하지 않으며, 설계 승인이라는 인간 판단 아티팩트가 요구된다(ref: `superpowers.md`).

증거 아티팩트의 종류: 스크린샷, E2E 로그, PR URL, 사람의 명시적 승인, 테스트 통과 로그.

적합한 상황: Boolean이나 수치만으로는 실제 동작이 보장되지 않는 경우. UI 버그, 사용자 시나리오 검증, 회귀 테스트 등.

---

## 근거가 되는 관찰

- Anthropic `passes: false` 기본값 — 모든 피처가 미완료에서 출발. 에이전트는 E2E 검증 완료 후에만 `passes: true` 전환 가능(ref: `anthropic-effective-harnesses-long-running-agents`).
- Ouroboros 숫자 임계값 구현 — ambiguity ≤ 0.2 / similarity ≥ 0.95 / drift ≤ 0.3 세 개의 수치 게이트가 각각 인터뷰 진입, 진화 종료, 세션 이탈 조건을 차단(ref: `ouroboros.md`, 섹션 3·5·12).
- Superpowers `<HARD-GATE>` — 프롬프트 레벨에서 XML 태그로 구현 차단. "This applies to EVERY project regardless of perceived simplicity"라는 무조건성이 Boolean 게이트의 프롬프트 레벨 표현(ref: `superpowers.md`).
- Puppeteer MCP E2E 게이트 — 코드 수준 리뷰만으로는 잡히지 않는 UI 버그를 브라우저 자동화로 포착. 증거 바운드 게이트의 가장 강한 사례(ref: `anthropic-effective-harnesses-long-running-agents`).
- Compound Engineering P1/P2/P3 우선순위 — 14개 병렬 리뷰 에이전트가 결과를 P1(critical)/P2(major)/P3(minor)로 분류하여 P1 미해결 시 머지 차단. 이것은 수치 임계값의 간접 형태다: "P1 이슈 0개"가 완료 조건이 된다(ref: `compound-engineering.md`).

---

## 구성 요소 (이식 가능한 단위)

### 1. Default-false 원칙
모든 피처·태스크·체크포인트를 기본값 `false`(미완료)로 초기화한다. 완료 주장은 항상 증명 의무를 동반한다. JSON 포맷이 Markdown 대비 에이전트의 임의 수정에 대한 저항성이 높다. standalone-extractable: **yes**.

### 2. Threshold numerical
연속 측정값에 명시적 임계값을 붙여 게이트로 만든다. Ouroboros의 0.2/0.95/0.3이 현재 코퍼스에서 가장 구체적인 구현 사례다. 임계값 자체보다 "어떤 차원을 게이트 기준으로 삼을 것인가"를 먼저 정의하는 것이 설계 핵심이다. standalone-extractable: **partial** (측정 함수 구현 필요).

### 3. Evidence artifact
Boolean이나 수치 게이트를 통과하더라도 실제 동작 증거를 요구하는 레이어. 스크린샷, E2E 로그, 사람 승인 등 외부 아티팩트가 게이트 통과 조건이 된다. standalone-extractable: **partial** (도구 의존성 있음).

### 4. Multi-gate composition
세 유형의 게이트를 AND 조합으로 사용하면 서로 다른 실패 모드를 각각 차단한다. Boolean 게이트는 "아무것도 안 했을 때", 수치 임계값은 "불충분한 품질일 때", 증거 아티팩트는 "코드는 맞지만 실제 동작이 틀릴 때"를 잡는다. standalone-extractable: **yes** (조합 패턴으로).

---

## 반례 또는 한계

- **게이트 인플레이션**: 게이트가 너무 많아지면 개발 속도가 저해된다. Superpowers v5.0.4에서 "max review iterations 5→3"으로 리뷰 루프 상한을 축소한 것, v5.0.6에서 서브에이전트 리뷰를 비용 문제로 인라인 self-review로 롤백한 것이 게이트 과잉의 실증 사례다(ref: `superpowers.md`).
- **숫자 임계값의 gaming (Goodhart's law)**: Ouroboros의 ambiguity 0.2 게이트는 측정 방법이 MCP 서버 구현부에 있어 스킬 사용자에게 불투명하다. "왜 0.19인가"를 에이전트나 사용자가 설명할 수 없다면 게이트를 조작하거나 맹목적으로 통과시키는 유인이 생긴다(ref: `ouroboros.md`, 섹션 9·10).
- **E2E gate의 flakiness**: Puppeteer MCP는 "네이티브 브라우저 alert 모달 같은 일부 UI 요소를 감지하지 못한다"는 한계가 명시되어 있다(ref: `anthropic-effective-harnesses-long-running-agents`). 증거 바운드 게이트의 신뢰성은 사용하는 도구의 신뢰성에 종속된다.
- **수치 임계값의 측정 비용**: drift ≤ 0.3 계산은 embedding 기반 거리 함수를 요구하고, similarity ≥ 0.95도 마찬가지다. 경량 환경에서 이 게이트는 계산 비용 자체가 병목이 될 수 있다.

---

## 전제 / 선행 조건

- 측정 대상 차원이 정의되어 있어야 한다(무엇을 게이트로 쓸 것인지).
- Boolean 게이트는 피처 목록이 사전에 완성된 상태를 전제한다.
- 수치 임계값은 측정 함수가 존재해야 하고, 그 함수의 신뢰성이 게이트 신뢰성과 직결된다.
- E2E 증거 게이트는 검증 도구(Puppeteer 등)와의 통합이 선행되어야 한다.

---

## 적용 난이도

- **Boolean 게이트 (passes: false)**: 낮음. JSON 스키마 정의 + 기본값 설정만으로 즉시 적용 가능.
- **수치 임계값**: 중간~높음. 측정 함수 설계 및 구현이 핵심 작업이고, 임계값 튜닝도 필요하다.
- **E2E 증거 게이트**: 중간. Puppeteer MCP 등 외부 도구 통합 필요. 도구가 준비된 환경에서는 낮음.
- **Multi-gate 조합**: 각 게이트의 합산. 단, 게이트 수를 최소화해야 인플레이션을 피할 수 있다.

---

## 내 프로젝트에 적용한다면 (Phase 2 후보)

Phase 2에서 harness를 구성할 때 다음 순서로 도입한다.

1. **즉시**: 모든 태스크 목록을 `passes: false` JSON으로 정의. Anthropic 패턴을 그대로 이식하며, 이 단계에서 Markdown 기반 체크리스트를 대체한다.
2. **중기**: 측정 가능한 차원이 생기면(커버리지, 오류율 등) 수치 임계값을 명시. Ouroboros의 0.2/0.95/0.3은 레퍼런스로 사용하되, 측정 함수를 먼저 확보하고 임계값을 후행으로 설정한다.
3. **고부가가치 체크포인트에만**: E2E 증거 게이트는 모든 태스크가 아닌, 사용자 접촉면이 있는 기능에 한정. 게이트 인플레이션 방지가 최우선이다.

---

## 관련 primitive 카드

- `primitive-shift-handoff-state.md` (예정) — `passes: false` JSON이 속하는 상태 외재화 패턴
- `primitive-default-false.md` (이 카드의 Boolean 게이트 단독 추출 버전으로 분리 가능)
- `primitive-evaluator-optimizer-loop.md` (예정) — 수치 임계값이 루프 종료 조건으로 사용되는 패턴
