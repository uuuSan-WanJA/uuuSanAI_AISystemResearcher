---
title: Evaluator-Optimizer 패턴 확산 primitive
date: 2026-04-17
based_on:
  - anthropic-building-effective-agents.md
  - anthropic-multi-agent-research-system.md
  - anthropic-demystifying-evals.md
  - ecc.md
  - ouroboros.md
  - superpowers.md
  - digests/2026-04-17-anthropic-sweep-vs-community-harnesses.md
confidence: high
tags: [evaluator-optimizer, pattern-diffusion, cost-control, primitive]
---

## 한 줄 요약

Evaluator-Optimizer는 품질을 끌어올리는 가장 강력한 워크플로 패턴이지만, ~15× 토큰 비용이라는 함정 때문에 커뮤니티 9종 하네스 중 4개만 명시 구현했고 그중 하나(Superpowers)는 실제로 롤백했다 — 도입 시 cost-quality 곡선을 처음부터 명시적으로 설계해야 한다.

---

## 패턴 / 주장

Anthropic의 `building-effective-agents`는 Evaluator-Optimizer를 "Generator LLM → 생성 → Evaluator LLM → 피드백 → Generator LLM → 반복"의 루프로 정의하며, 문학 번역이나 복잡한 다단계 검색처럼 "명확한 평가 기준이 존재하고 반복적 개선이 실질적 가치를 창출할 때" 사용하라고 권고한다. 구조는 단순하지만 작동 조건이 까다롭다. 평가자(Evaluator)가 얼마나 신뢰할 수 있는지, 루프당 비용이 태스크 가치에 비례하는지가 도입의 핵심 판단 기준이 된다.

커뮤니티는 이 패턴을 과소대표했다. A 매트릭스(`2026-04-17-anthropic-sweep-vs-community-harnesses.md`)에 따르면 9종 하네스 중 명시적으로 구현한 경우는 4개(Superpowers, Ouroboros, ECC, Compound Engineering)에 불과하다. Ralph Wiggum은 독립 평가자 없이 무한 루프하는 구조적 공백이 있고, GSD·gstack·OpenSpec은 부분 구현에 그쳤으며, revfactory는 Phase 7 Harness Evolution에서만 평가-최적화 루프를 쓴다. 그리고 4개 명시 구현체 중 하나인 Superpowers는 v5.0.6(2026-03-24)에서 서브에이전트 기반 리뷰를 인라인 self-review로 롤백했다 — 이것이 이 카드의 핵심 데이터 포인트다.

---

## 근거가 되는 관찰

**Anthropic 정의 — building-effective-agents**

`building-effective-agents`는 Evaluator-Optimizer의 종료 조건을 "평가자가 합격 판정 또는 최대 반복 횟수 도달"로 명시한다. 즉 루프를 닫는 두 개의 탈출구가 설계에 포함되어야 한다. 이를 생략하면 Ralph의 `while true` 무한 루프처럼 평가 기준 없는 실행이 된다.

**ECC Instinct Evaluator-Optimizer**

ECC(`ecc.md`)의 `/learn` → `/evolve` 사이클은 생성자(에이전트)와 평가자(instinct 신뢰도 스코어러)를 분리한 반복 루프다. 신뢰도 0.3–0.9 스케일로 패턴을 채점하고, 고신뢰도 패턴은 영속 instinct로 승격하며, 저신뢰도는 `/instinct-prune`으로 제거한다. 이 구조는 Anthropic 정의에 가장 충실한 커뮤니티 구현 중 하나이지만, 신뢰도 측정 함수 내부가 불투명하다는 grader 신뢰성 문제를 동시에 안고 있다.

**Ouroboros 다세대 Evaluator-Optimizer**

Ouroboros(`ouroboros.md`)는 `interview → seed → execute → evaluate → evolve` 5단계 사이클을 최대 30 generation까지 돌린다. 특히 종료 조건을 수치로 구현한 점이 주목할 만하다 — `ontology similarity ≥ 0.95`가 수렴 판정 기준이다. Anthropic 정의가 "평가자가 합격 판정"이라는 개념적 설명에 그친 반면, Ouroboros는 0.95라는 구체적 임계값으로 이를 운영화했다. 또한 `converged / stagnated / exhausted / failed` 4-action 상태 머신이 루프의 탈출 경로를 명시적으로 분기한다.

**Superpowers v5.0.6 롤백 — Anthropic 15× 경고 독립 확증 (digest 가장 놀라운 관찰)**

`superpowers.md`에 따르면 Jesse Vincent는 v5.0.6(2026-03-24) 릴리스 노트에 다음과 같이 기록했다: "Inline Self-Review Replaces Subagent Review Loops — removed expensive review delegation in favor of integrated checklists." 이것은 독립 서브에이전트 Evaluator가 감당 불가한 비용을 발생시킨다는 실제 자인이다. `multi-agent-research-system`은 멀티에이전트 시스템의 토큰 비용이 일반 채팅 대비 ~15×에 달한다고 명시적으로 경고했는데, Superpowers v5.0.6 롤백은 이 경고를 커뮤니티가 **독립적으로 실험하고 확증한** 사례다. digest는 이를 "가장 놀라운 관찰"로 지목한다 — 이론적 경고가 커뮤니티의 실전 회귀 결정으로 재현되었기 때문이다.

**Grader 신뢰성 이슈 — demystifying-evals**

`demystifying-evals`는 평가자 설계 실패가 에이전트 자체의 무능보다 훨씬 자주 낮은 점수의 원인이라고 지적한다. CORE-Bench에서 rigid grader가 "96.12" vs "96.124991..." 을 오답으로 처리해 42% 점수를 냈고, grader 수정 후 95%로 회복된 사례가 이를 증명한다. Evaluator-Optimizer를 도입할 때 Evaluator 자체의 품질이 전제 조건이지 부록이 아니다. "LLM grader는 반드시 human expert와 calibrate해야 한다"는 원칙은 ECC instinct 스코어러에도, Ouroboros qa-judge 에이전트에도 동일하게 적용된다.

---

## 구성 요소 (이식 가능한 단위)

**1. Generator-Evaluator 역할 분리 원칙**

Generator와 Evaluator는 서로 다른 컨텍스트에서 동작해야 한다. 같은 LLM이 자신의 출력을 평가하면 sycophancy bias가 발생하고, 실질적인 비판 루프가 작동하지 않는다. ECC의 `/learn`이 별도 신뢰도 스코어러를 두고, Ouroboros가 evaluator와 ontologist를 독립 에이전트로 분리하는 것은 이 원칙의 직접 구현이다. 단, v5.0.6 이후 Superpowers의 inline self-review는 비용 타협의 결과이며 — 독립 평가자의 이상에서 한 칸 물러선 실용적 선택이다.

**2. Evaluator scope 결정 트리 — full separate agent vs inline prompt vs rule-based**

세 가지 구현 경로가 현실에서 공존한다:

- **Full separate agent**: Ouroboros qa-judge, Compound Engineering 14 리뷰어, ECC instinct 스코어러. 비용이 가장 크지만 평가 품질도 가장 높다. 태스크 가치가 높고 반복 횟수가 제한적일 때 적합하다.
- **Inline prompt (HARD-GATE 방식)**: Superpowers v5.0.6 이후 방식. `<HARD-GATE>` XML 태그와 DOT 플로우차트로 평가 기준을 프롬프트에 내장한다. 비용은 낮지만 평가자의 독립성이 없다.
- **Rule-based**: 결정론적 코드 채점(단위 테스트 통과/실패, lint). `demystifying-evals`의 Code-based grader에 해당하며, 재현성이 높고 비용이 가장 낮다. 단, 창의적 우회 솔루션을 "실패"로 오판할 수 있다.

결정 기준: 태스크의 평가 기준이 수치로 표현 가능한가(→ rule-based 또는 임계값 기반), 아니면 주관적 품질 판단이 필요한가(→ full separate agent 또는 inline LLM).

**3. Cost-quality 모니터링 — 회당 비용 임계값 미리 설정**

루프를 시작하기 전에 "회당 최대 토큰 예산"과 "최대 반복 횟수"를 명시적으로 설계해야 한다. Ouroboros는 30 generation hard cap을 둔다. Superpowers는 v5.0.4에서 max review iterations를 5에서 3으로 하향했다. 이 수치들은 임의로 결정된 것이 아니라 실제 운영 중 발생한 비용 초과에서 역산된 안전 한계다. `multi-agent-research-system`이 제시한 "태스크 가치가 토큰 비용을 상회해야 멀티에이전트가 정당화된다"는 경제성 임계점 원칙을 수치로 미리 정하지 않으면, Superpowers v5.0.6과 동일한 롤백을 반복하게 된다.

**4. Grader 신뢰성 검증 — inline demotion 트리거 조건**

Evaluator가 신뢰할 수 없으면 루프 전체가 noise를 증폭한다. `demystifying-evals`가 권고하는 검증 절차: (a) step-sequence grader 금지 — 특정 도구 호출 순서를 강제하면 창의적 솔루션이 걸러진다, (b) LLM grader는 human expert와 반드시 calibrate, (c) transcript를 직접 읽어서 grader 출력과 비교하는 정기 점검, (d) 점수가 정체되면 에이전트가 아닌 grader를 먼저 의심. ECC의 `/instinct-prune` (저신뢰도 instinct 제거)은 (d)의 자동화 버전이지만, 자동 pruning 기준이 미문서화되어 있어 human calibration 절차가 부재하다는 위험을 안고 있다.

---

## 반례 또는 한계

**~15× 토큰 비용**

`multi-agent-research-system`은 멀티에이전트 시스템이 일반 채팅 대비 ~15×의 토큰을 소비한다고 명시했다. 단일 에이전트 대비로도 ~4×다. Evaluator-Optimizer 루프는 정의상 멀티-LLM 호출 구조이므로 이 비용 배율이 반드시 적용된다. 태스크 가치가 비용을 정당화할 수 있을 때만 도입을 고려해야 한다.

**Grader drift / 단일 grader bias**

LLM-based evaluator는 시간이 지남에 따라 평가 기준이 흔들리거나(drift), 자신이 선호하는 형식을 더 높게 채점하는 bias를 발생시킨다. `demystifying-evals`가 지적한 "유연하지만 비결정적"이라는 속성이다. 단일 grader에만 의존하면 Generator가 grader의 편향을 학습하고 최적화하는 역방향 압력이 생긴다. Compound Engineering이 14개 독립 리뷰어를 두는 이유가 여기에 있다.

**Inline fallback으로의 자연 퇴화 (Superpowers v5.0.6)**

이것이 가장 실천적인 경고다. 독립 서브에이전트 Evaluator는 비용·지연 압력이 누적되면 inline self-review로 자연스럽게 퇴화한다. Superpowers는 이 퇴화를 명시적 릴리스 결정으로 기록했지만, 다른 하네스는 암묵적으로 퇴화할 수 있다. 이를 방지하려면 "독립 평가자 유지 비용"을 미리 예산에 반영하거나, 처음부터 inline + rule-based 혼합 방식으로 설계해야 한다.

---

## 전제 / 선행 조건

- **명확한 평가 기준 존재**: Evaluator가 "좋다/나쁘다"를 판단할 수 있는 기준이 사전에 정의되어야 한다. 기준이 모호하면 평가자는 noise를 생성한다.
- **반복 가능한 태스크 구조**: 동일 입력에 대해 Generator가 다른 출력을 생성할 수 있어야 루프가 의미 있다. 결정론적 태스크에는 루프가 불필요하다.
- **비용 예산 사전 정의**: 최대 반복 횟수와 회당 토큰 상한이 설계 시점에 결정되어야 한다.
- **Grader calibration 절차**: Evaluator가 LLM 기반일 경우 human expert와의 초기 calibration 과정이 필요하다.

---

## 적용 난이도

**Full separate Evaluator가 필요한 시나리오**:
- 출력 품질 판단에 도메인 전문성이 요구되고(예: 법률 문서 검토, 미묘한 문학 번역), 태스크 가치가 높아 ~15× 비용을 정당화할 수 있을 때.
- 반복당 품질 개선 효과가 측정 가능하고, 수렴 임계값(Ouroboros의 similarity ≥ 0.95 방식)을 미리 정의할 수 있을 때.

**Inline Evaluator가 충분한 시나리오**:
- 평가 기준을 rule-based 체크(단위 테스트, lint, JSON schema 검증)로 표현할 수 있을 때.
- 비용 예산이 제한적이고 반복 횟수가 적을 때 (Superpowers HARD-GATE 방식).
- 고빈도·저비용 태스크에서 near-realtime 응답이 필요할 때.

**판단 기준 요약**: "평가 기준을 코드로 쓸 수 있는가?" → Yes이면 rule-based부터 시작. "아니오이면 LLM grader가 필요한데, 예산이 반복 루프를 허용하는가?" → Yes이면 full separate, No이면 inline.

---

## 내 프로젝트에 적용한다면 (Phase 2 후보)

Phase 2에서 Evaluator-Optimizer를 도입할 경우 권장 순서:

1. **먼저 rule-based grader로 시작**: 단위 테스트·lint·수치 임계값 등 결정론적 평가를 먼저 구현한다. `demystifying-evals`의 "Code-based grader 우선" 원칙.
2. **LLM grader 추가 시 calibration 필수**: 첫 20–50 케이스를 human expert와 함께 채점해 grader 출력이 human 판단과 일치하는지 확인한다.
3. **비용 임계값 선 설정**: 최대 반복 횟수를 Ouroboros(30 gen), Superpowers(3 iterations)처럼 명시적으로 코드에 박는다. 나중에 줄이는 것이 처음부터 없는 것보다 낫다.
4. **Superpowers의 교훈 내재화**: 독립 서브에이전트 Evaluator가 inline으로 퇴화하는 압력을 예상하고, 퇴화 허용 기준과 조건을 설계 문서에 미리 기록해 둔다.

---

## 관련 primitive 카드

- **regression-eval-lifecycle** (강하게 연결): Evaluator-Optimizer 루프의 학습 결과를 "어느 시점에 regression suite로 전환하는가"는 이 카드가 다루는 범위 밖이다. ECC `/learn`→`/evolve`와 Compound `docs/solutions/`의 학습 축적이 regression suite 승격으로 이어지지 않는 공백이 digest C1 gap으로 지목되었다. 두 카드는 함께 읽어야 한다.
- **cost-quality-tradeoff-in-multi-agent** (직접 연결): ~15× 비용 경고와 Superpowers v5.0.6 롤백은 멀티에이전트 비용 설계 카드의 핵심 데이터 포인트이기도 하다.
