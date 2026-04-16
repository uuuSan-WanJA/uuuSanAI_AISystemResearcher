---
title: Regression eval 수명주기 primitive
date: 2026-04-17
based_on:
  - anthropic-demystifying-evals.md
  - anthropic-multi-agent-research-system.md
  - compound-engineering.md
  - ecc.md
  - superpowers.md
  - digests/2026-04-17-anthropic-sweep-vs-community-harnesses.md
confidence: high
tags: [evaluation, regression-suite, capability-eval, primitive]
---

## 한 줄 요약

Capability eval(개선 신호 추출)과 Regression eval(역회귀 방지)을 분리하고, Capability가 포화되면 자동으로 Regression suite로 승격하는 수명주기를 설계하지 않으면 하네스는 노이즈와 실제 회귀를 구별하지 못한 채 반응적 루프에 갇힌다.

---

## 패턴 / 주장

Anthropic은 eval을 **목적에 따라 두 종류로 엄격히 분리**할 것을 요구한다 (anthropic-demystifying-evals.md §명시적 분류 체계).

**Capability eval**은 현재 에이전트가 풀지 못하는 도전적 태스크로 구성된다. 통과율이 낮은 것이 정상이며, 수치가 오를 때마다 개선 신호를 추출한다. 이 eval은 에이전트가 무엇을 할 수 없는지를 드러내는 탐침이다.

**Regression eval**은 이미 해결된 태스크를 고정해 ~100% 통과율을 항구적으로 유지하는 장치다. 코드 변경이나 모델 교체 후 "이전에 되던 것이 지금도 되는가"를 자동으로 검증한다. 이 eval은 에이전트가 무엇을 계속 할 수 있어야 하는지를 지키는 파수꾼이다.

두 eval의 역할이 다른 이유는 명확하다. 도전적 태스크는 언젠가 포화된다. SWE-Bench Verified는 실제로 1년 만에 40%→80%+에 도달해 개선 신호가 사라졌다 (anthropic-demystifying-evals.md §핵심 포인트 3번째 bullet). 포화된 Capability eval을 그대로 유지하면 수치는 높지만 정보가 없다. 따라서 포화 태스크를 Regression suite로 이관하고 새로운 Capability eval로 교체하는 수명주기 관리가 구조적으로 필요하다.

이 분리가 없으면 Anthropic이 직접 경고한 상황이 벌어진다: "teams without evals get bogged down in reactive loops — fixing one failure, creating another, unable to distinguish real regressions from noise" (anthropic-demystifying-evals.md §인용 가치 있는 구절).

---

## 근거가 되는 관찰

- **CORE-Bench 42%→95% 점프 사례**: Anthropic이 직접 경험한 사례로, 낮은 점수의 원인이 에이전트 무능이 아닌 rigid grader("96.12" vs "96.124991…" 오답 판정 + 모호한 spec)였음이 밝혀졌다. Grader 수정 후 동일 에이전트가 95%를 기록했다. 이 사례는 **eval 설계 자체가 신뢰성 검증 대상**임을 입증한다 (anthropic-demystifying-evals.md §실패 모드 사례 표). Digest 증거 앵커 B3에서도 grader 수정만으로 이 수치 이동이 일어났다는 것을 공백의 근거로 인용 (digests/2026-04-17-anthropic-sweep-vs-community-harnesses.md §B3).

- **커뮤니티 하네스 9/9 미구현 (C1 gap)**: ECC의 `/learn`→`/evolve` 사이클과 Compound Engineering의 `docs/solutions/` 누적 학습은 반복 경험을 축적하지만, "어느 태스크가 포화되어 Regression으로 강등되었는가"를 자동 판별하는 메커니즘이 전무하다. 결과적으로 커뮤니티 하네스의 반복 이터레이션은 노이즈와 실제 회귀를 구별하지 못한다 (digests §C1, ecc.md §10 Failure modes, compound-engineering.md §기존 하네스 노트와의 연결).

- **ECC Instinct scoring 검증 부재**: ECC의 NanoClaw v2는 0.3–0.9 신뢰도 스케일로 instinct를 채점하지만, 이 평가 함수 자체의 정확성이 검증된 적 없다. Anthropic의 원칙대로라면 "model-based grader는 반드시 human expert와 calibrate"해야 하지만, ECC instinct scoring의 calibration 프로토콜은 미공개이다 (ecc.md §10 Failure modes; anthropic-demystifying-evals.md §Step 5 신중한 grader 설계).

- **Compound Engineering 14 리뷰어에 Regression 전환 없음**: Compound Engineering의 14개 병렬 전문 리뷰 에이전트(security-sentinel, performance-oracle, dhh-rails-reviewer 등)는 dimensional grader 구조로 되어 있지만, 리뷰 결과를 Regression suite로 전환하는 메커니즘이 없다. 따라서 매번 동일한 리뷰를 반복하면서도 "이전에 통과한 패턴이 지금도 통과하는가"를 자동으로 보장하지 못한다 (compound-engineering.md §기존 하네스 노트와의 연결 §Compound Engineering, anthropic-demystifying-evals.md).

- **Superpowers HARD-GATE는 게이트이지 eval이 아님**: Superpowers의 `<HARD-GATE>` XML 태그와 DOT 플로우차트는 프로세스 진전을 차단하는 장치이지, 통과율을 측정하고 포화를 감지하는 eval 인프라가 아니다 (superpowers.md §P3 HARD-GATE). v5.0.6에서 서브에이전트 리뷰가 비용 문제로 인라인으로 롤백된 사례는 eval 인프라 없이 리뷰만 강화할 때의 경제적 한계를 보여 준다 (superpowers.md §10 Failure modes).

---

## 구성 요소 (이식 가능한 단위)

### 1. Capability eval
**언제**: 에이전트 개발 초기, 첫 구현 직후. "Evals get harder to build the longer you wait."  
**어떻게**: 현재 에이전트가 풀지 못하는 태스크를 중심으로 구성한다. 두 명의 도메인 전문가가 독립적으로 동일한 pass/fail 판정에 도달할 수 있어야 한다. Positive(행동해야 할 때)와 Negative(행동하지 말아야 할 때) 케이스를 균형 있게 포함한다.  
**시작 규모**: 20–50개 태스크. 실제 버그 리포트·지원 큐 실패 사례를 테스트 케이스로 변환하는 것이 가장 빠른 시작점이다.  
**운영 원칙**: 0% 통과율이 지속되면 태스크가 broken인지 먼저 의심하고 transcript를 직접 읽는다.  
(anthropic-demystifying-evals.md §Step 0–Step 2, §Step 3)

### 2. Regression eval
**언제**: Capability eval의 특정 태스크가 안정적으로 ~100% 통과율에 도달한 시점에 해당 태스크를 Regression suite로 이관한다.  
**무엇을 고정하는가**: 에이전트가 "이미 할 수 있는 것"으로 확인된 태스크 집합. 코드 수정, 모델 업그레이드, 프롬프트 변경 후에도 이 suite가 100%를 유지하지 못하면 회귀로 판정한다.  
**자동화 조건**: CI 파이프라인에 연결되어 매 변경 후 자동 실행. 실패 시 머지 차단. 새 Capability eval은 별도 파이프라인에서 실행해 개선 신호를 추적한다.  
**포화 감지**: 현재 Capability eval의 통과율이 95%+에서 3회 연속 안정되면 해당 태스크를 Regression으로 승격하고 더 어려운 태스크를 Capability eval에 추가한다.  
(anthropic-demystifying-evals.md §핵심 포인트, §Step 7 포화 모니터링)

### 3. Grader 신뢰성 검증 단계
**Transcript 직독**: eval 점수가 정체되거나 예상과 다를 때 에이전트 능력보다 grader를 먼저 의심한다. "As a rule, we do not take eval scores at face value until someone digs into the details of the eval and reads some transcripts." (anthropic-demystifying-evals.md §인용)  
**수정→재점수 cycle**: Grader를 수정한 후 동일 transcript 집합에 재채점하여 CORE-Bench 유형의 오판이 없는지 확인한다. 42%→95% 점프가 grader 수정만으로 가능했다는 사례가 이 단계의 필요성을 가장 직접적으로 증명한다.  
**Step-sequence grader 금지**: "에이전트가 특정 도구 호출 순서를 따랐는지 검사하지 마라." 창의적 우회 경로를 오판한다 (anthropic-demystifying-evals.md §Step 5, §P5).  
**Model-based grader calibration**: LLM grader를 사용할 경우 human expert와 주기적으로 calibrate하여 grader drift를 방지한다. ECC instinct scoring처럼 평가 함수 내부가 불투명하면 false confidence를 유발한다 (ecc.md §10 구조적 한계 §Instinct confidence scoring 불투명; anthropic-demystifying-evals.md §Step 5).

### 4. pass@k vs pass^k 이중 지표
비결정적 에이전트는 동일 태스크에도 매번 다른 경로를 밟는다. 단일 시도 통과율 하나로는 신뢰성을 측정할 수 없다.

- **pass@k**: k회 시도 중 ≥1회 성공. k가 늘어날수록 상승. 에이전트가 "할 수 있는가"를 탐색하는 Capability eval에 적합하다.  
- **pass^k**: k회 시도 모두 성공 = (per-trial 성공률)^k. k가 늘어날수록 하락. 실제 사용자가 경험할 신뢰성을 측정하는 Regression eval에 적합하다. 예: 75% per-trial × 3회 → pass^3 ≈ 42%. 이 수치는 single-trial 75%가 얼마나 과대평가인지를 보여 준다.

커뮤니티 하네스의 성능 주장 — Ralph "그린필드 90% 성공", revfactory "+60% 품질" — 은 모두 단일 시도 통과율 기반이다. pass^k로 측정하면 실제 신뢰도는 크게 낮아질 가능성이 있다 (digests §C5; anthropic-demystifying-evals.md §핵심 지표 공식).

---

## 반례 또는 한계

- **소규모 프로젝트에서 Regression suite 유지 비용**: 태스크 코퍼스가 20개 미만이거나 에이전트가 빠르게 진화하는 초기에는 suite가 오히려 속도를 낮출 수 있다. 이 primitive는 태스크 풀이 충분히 안정된 후에야 구조적 가치가 생긴다.

- **Grader 자체의 드리프트**: Model-based grader는 기반 모델이 업데이트되면 동일한 transcript에도 다른 점수를 줄 수 있다. Regression suite 자체가 grader drift 때문에 무결성을 잃는 역설이 발생한다. Anthropic 포스트에서 이 drift 방지 프로토콜은 "human calibration"으로만 언급되며 구체적 주기나 절차는 미명시이다 (anthropic-demystifying-evals.md §후속 조사 §Human calibration 프로토콜).

- **자동화가 만드는 false confidence**: Regression suite가 100% 통과한다는 것은 "지금까지 알려진 회귀가 없다"는 의미이지 "에이전트가 안전하다"는 의미가 아니다. Swiss Cheese 모델처럼 자동 eval은 여러 레이어 중 하나일 뿐이다. 프로덕션 모니터링, A/B 테스트, 유저 피드백, 수동 transcript 검토가 각각 다른 실패를 잡는다 (anthropic-demystifying-evals.md §핵심 포인트 §Swiss Cheese 모델).

- **포화 임계값의 임의성**: "95%에서 3회 연속 안정"이라는 포화 판정 기준은 이 카드에서 실용적으로 제안한 수치이다. Anthropic 포스트는 포화 감지의 구체적 임계값을 제시하지 않으며 ("~100%에 근접하면"), 실제 환경에 따라 조정이 필요하다.

---

## 전제 / 선행 조건

- **최소 20–50개 태스크 코퍼스**: 이 규모가 없으면 Capability eval을 구성할 수 없다. 실제 버그 리포트나 지원 큐 실패 사례를 채굴하는 것이 첫 번째 단계다.
- **Grader 분류(Code / Model / Human) 결정 필요**: 태스크 유형에 따라 결정론적 Code grader가 가능한지, 뉘앙스 평가가 필요한지 먼저 파악해야 한다. 코딩 에이전트는 Code grader 우선(단위 테스트 통과/실패)이 원칙이다.
- **Transcript 저장 인프라**: Transcript를 남기지 않으면 grader 오판을 소급해 검증할 수 없다. 최소 구현은 파일 시스템에 JSONL로 append하는 것으로 충분하다.
- **CI 파이프라인 연결 의지**: Regression suite는 자동 실행되어야 의미가 있다. 수동으로 돌리는 regression eval은 곧 실행되지 않는 regression eval이 된다.

---

## 적용 난이도

- **최소 구현 (1–2일)**: 기존 버그 리포트에서 20개 태스크 추출 → pass/fail 판정 가능한 Code grader 작성 → transcript JSONL 저장 → CI에 연결. Capability/Regression 구분 없이 단일 suite로 시작하되, 각 태스크에 "capability" 또는 "regression" 라벨만 붙여도 수명주기 관리의 기반이 만들어진다.

- **완전 구현 (3–5주)**: 50개+ 태스크 코퍼스 → Code/Model/Human 혼합 grader 체계 → Transcript 저장소 + transcript 직독 워크플로 → 포화 자동 감지 및 Capability→Regression 승격 파이프라인 → pass@k / pass^k 이중 대시보드 → model-based grader human calibration 프로토콜 정립.

---

## 내 프로젝트에 적용한다면 (Phase 2 후보)

1. **ECC `/learn`→`/evolve` 루프에 Regression 승격 레이어 추가**: 현재 ECC는 학습 패턴을 instinct로 승격하지만 "이 instinct가 포화되어 항상 통과하는가"를 추적하지 않는다. `/instinct-status`의 신뢰도 0.9+ 항목을 자동으로 Regression 태스크로 변환하는 훅을 추가하면 학습 루프가 eval 수명주기와 연결된다.

2. **Compound Engineering `docs/solutions/`에 포화 마커 도입**: `docs/solutions/` YAML frontmatter에 `eval_status: capability|regression|saturated` 필드를 추가하고, 특정 솔루션이 3회 이상 동일 결과로 확인되면 자동으로 `regression`으로 승격하는 베스트프랙티스 에이전트 수정.

3. **Superpowers HARD-GATE를 pass^k 기반 수치 gate로 보강**: 현재 HARD-GATE는 사람이 "승인했는가"를 조건으로 한다. TDD 스킬에서 생성된 테스트를 k회 반복 실행하여 pass^k ≥ 0.90 이상일 때만 finalize 단계로 진입하도록 DOT 플로우차트에 수치 game을 추가할 수 있다.

4. **어느 하네스에서든 적용 가능한 최소 출발점**: 기존 에이전트의 마지막 30회 실행 로그에서 매번 통과한 태스크를 식별하고, 그것을 최초 Regression suite의 후보로 지정한다. 이 작업은 하루 안에 끝나며, eval 인프라가 없어도 시작할 수 있는 현실적인 진입점이다.

---

## 관련 primitive 카드

- **numerical-gate-thresholds primitive** — Ouroboros의 ambiguity ≤ 0.2 / similarity ≥ 0.95 / drift ≤ 0.3 패턴; Capability→Regression 포화 임계값 결정 시 같은 원리가 적용된다 (digests §D2).
- **evaluator-optimizer-diffusion primitive** — Superpowers의 HARD-GATE + DOT 구조와 ECC의 `/learn`→`/evolve` 루프가 각각 evaluator-optimizer 역할을 부분적으로 수행하지만 공식 eval 인프라로는 미완성이다 (superpowers.md §P3; ecc.md §P2).
- **grader-taxonomy primitive** — Code / Model / Human 3분류 및 hybrid scoring 가중치 설계 패턴; Regression suite에 어떤 grader를 쓸지 결정하는 전제 카드 (anthropic-demystifying-evals.md §P1).
