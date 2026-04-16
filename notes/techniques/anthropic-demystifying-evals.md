---
title: Demystifying evals for AI agents
date: 2026-04-17
source_url: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
source_type: blog
topic: techniques
tags: [anthropic, evaluation, benchmarks, agent-eval, graders, pass-at-k, regression, capability, swe-bench, non-determinism]
status: processed
---

## 요약 (3줄 이내)

Agent eval은 단순 LLM eval과 근본적으로 다르다 — multi-turn 자율성, 상태 변이, 오류 전파 때문에 기존 단일 입출력 측정 패러다임이 무너진다. Anthropic은 Code/Grader/Human 3종 grader 분류, Capability vs. Regression eval 이분법, pass@k vs. pass^k 이중 지표를 제시하며 "0→효과적 eval" 8단계 로드맵으로 구체화한다. 핵심 교훈: grader 설계 실패(지나치게 rigid한 step-checking)가 agent 자체의 무능보다 훨씬 자주 낮은 점수의 원인이다.

---

## 핵심 포인트

- **Eval 단위 정의의 중요성**: Task(단일 테스트) / Trial(1회 시도) / Grader(채점 로직) / Transcript(전체 궤적) / Outcome(최종 환경 상태)을 명확히 구분해야 한다. "Outcome은 transcript와 다르다"는 구분이 agent eval 설계의 출발점.
- **Grader 3분류**: Code-based(빠름·재현 가능·brittle), Model-based(유연·비결정적·비쌈), Human(gold standard·느림·비쌈). 현실에서는 hybrid scoring이 표준.
- **Capability eval vs. Regression eval 수명주기**: Capability eval은 낮은 통과율에서 시작해 개선 신호를 추출하고, 포화 후 Regression eval로 전환되어 ~100% 유지. SWE-Bench Verified는 1년 만에 40%→80%+ 도달해 포화 문제가 현실화됨.
- **Non-determinism 이중 지표**: pass@k(k회 중 ≥1회 성공, 상향 곡선)와 pass^k(k회 모두 성공, 하향 곡선)를 상호보완적으로 사용. customer-facing 신뢰성 측정에는 pass^k가 적합.
- **8단계 로드맵**: 20–50개 소규모 태스크로 시작 → 실제 버그/지원 큐 채굴 → 애매하지 않은 task 작성 → 균형 문제셋(positive/negative) → 안정 환경 격리 → 신중한 grader 설계 → transcript 직독 → 포화 모니터링.
- **Swiss Cheese 모델**: 자동 eval 단독으로 충분하지 않다. 프로덕션 모니터링, A/B 테스트, 유저 피드백, 수동 transcript 검토, 전문가 human study — 각 레이어가 서로 다른 실패를 잡는다.

---

## 저자의 프레임워크 / 명시적 주장

### Agent eval ≠ LLM eval — 이유

LLM eval의 전통적 구조는 "입력 → 출력 → 채점"의 단순 루프다. Agent eval은 이 가정이 모두 깨진다:

1. **Multi-turn 자율성**: 에이전트는 반복적으로 행동하며 환경을 수정한다. "올바른 출력"이 단일 응답이 아니라 환경의 최종 상태다.
2. **상태 변이와 오류 전파**: 중간 도구 호출 실패가 후속 단계 전체에 cascading하게 전파된다.
3. **창의적 우회**: 에이전트는 eval 설계자가 상상하지 못한 경로로 정답에 도달하기도 한다 — rigid한 step-sequence grader는 이를 "실패"로 오판한다.
4. **비결정성의 규모화**: 동일한 태스크에 동일한 에이전트를 반복 실행해도 다른 경로를 밟는다.

### 명시적 분류 체계

| 분류 | 정의 | 목적 |
|------|------|------|
| Capability eval | 낮은 통과율, 도전적 태스크 | 개선 신호 추출 |
| Regression eval | ~100% 통과율 유지 | 역회귀 방지 |
| Code-based grader | 결정론적 코드 채점 | 속도·재현성 |
| Model-based grader | LLM rubric 채점 | 유연성·뉘앙스 |
| Human grader | 전문가 직접 평가 | gold standard |

### Agent 유형별 eval 전략

- **Coding agent**: 결정론적 grader 우선(단위 테스트 통과/실패), transcript 부가 채점(코드 품질·static analysis). 벤치마크: SWE-Bench Verified, Terminal-Bench.
- **Conversational agent**: 상태 검증 + 대화 제약(턴 제한) + LLM 루브릭(톤/품질). 유저 시뮬레이션 2차 LLM 필요. 벤치마크: τ-Bench, τ2-Bench.
- **Research agent**: Grader 혼합(근거 검증·커버리지·출처 품질). 전문가 의견 불일치와 부유하는 ground truth가 핵심 난제. 벤치마크: BrowseComp.
- **Computer use agent**: 실제/샌드박스 환경에서 파일시스템·앱 설정·DB·UI 상태 직접 검증. DOM 추출(토큰 무거움·빠름) vs. 스크린샷(느림·효율적) 트레이드오프. 벤치마크: WebArena, OSWorld.

---

## 구체적 패턴·체크리스트·숫자

### Eval 설계 8단계 로드맵 (체크리스트)

- [ ] **Step 0 — 일찍 시작**: 개발 초기에 20–50개 태스크. "Evals get harder to build the longer you wait."
- [ ] **Step 1 — 수동 테스트 채굴**: 기존 버그 리포트·지원 큐 실패 사례를 테스트 케이스로 변환. 유저 임팩트 기준 우선순위화.
- [ ] **Step 2 — 애매하지 않은 태스크 작성**: "두 도메인 전문가가 독립적으로 동일한 pass/fail 판정에 도달할 수 있어야 한다." 참조 솔루션 포함으로 풀 수 있음을 증명할 것. 0% 통과율이 지속되면 태스크가 broken인지 먼저 의심.
- [ ] **Step 3 — 균형 문제셋**: Positive(행동해야 할 때)와 Negative(행동하지 말아야 할 때) 케이스 모두 포함. 클래스 불균형 금지. 예: 웹 검색 eval — "날씨 쿼리(검색해야 함)"와 "기초 지식(검색 불필요)" 양쪽 포함.
- [ ] **Step 4 — 안정적 eval 하네스**: 에이전트가 프로덕션과 동일하게 작동하도록 보장. 각 trial을 깨끗한 환경으로 격리. 잔류 파일·캐시 데이터로 인한 상관 실패 방지.
- [ ] **Step 5 — 신중한 grader 설계**: 결정론적 grader 우선. Step-sequence 체크 금지(rigid). 다중 컴포넌트 태스크에 부분 점수 구현. LLM grader는 반드시 human expert와 calibrate. "Unknown" 탈출구 제공. grader bypass/hack 저항성 확보.
- [ ] **Step 6 — Transcript 직접 읽기**: "You won't know if your graders are working well unless you read the transcripts and grades from many trials." 점수 정체 시 에이전트가 아닌 eval을 의심.
- [ ] **Step 7 — 포화 모니터링**: Capability eval이 ~100%에 근접하면 개선 신호가 사라짐. 더 어려운 태스크로 교체 또는 새 벤치마크 도입.
- [ ] **Step 8 — 장기 유지**: 전담 인프라 팀 구성. 도메인 전문가·제품팀이 직접 기여할 수 있는 구조. "Eval-driven development" — 에이전트 개발 전에 eval을 먼저 작성.

### 핵심 지표 공식

- **pass@k**: P(k회 시도 중 ≥1회 성공). k가 늘어날수록 상승. 단일 솔루션 시나리오에 적합.
- **pass^k**: P(k회 시도 모두 성공) = (per-trial 성공률)^k. k가 늘어날수록 하락. customer-facing 신뢰성 측정에 적합.
- 예시: 75% per-trial 성공률, 3회 시도 → pass^3 = (0.75)³ ≈ 42%.

### 실패 모드 사례 (구체적)

| 사례 | 문제 | 결과 |
|------|------|------|
| CORE-Bench / Opus 4.5 | Rigid grading: "96.12" vs "96.124991…" 오답 판정 + 모호한 spec + stochastic 태스크 | 42% → 95% (grader 수정 후) |
| METR Time Horizon | Task 잘못 설정: 목표 무시하는 모델에 보상, 지시 따르는 모델에 패널티 | 벤치마크 신뢰성 붕괴 |
| Terminal-Bench | filepath 미지정 태스크 → 테스트가 특정 경로 가정 | 에이전트 억울한 실패 |
| τ2-Bench / Opus 4.5 | 항공편 예약 정책 허점 발견, eval 기준으로는 "실패" | 실제로는 더 나은 솔루션 |
| Qodo / Opus 4.5 | 단일 시도 eval이 장기 태스크 이점 미포착 | 성능 과소 측정 |

---

## 인용 가치 있는 구절

> "The capabilities that make agents useful also make them difficult to evaluate."

> "A good task is one where two domain experts would independently reach the same pass/fail verdict."

> "There is a common instinct to check that agents followed very specific steps like a sequence of tool calls in the right order. We've found this approach too rigid."

> "Like the Swiss Cheese Model from safety engineering, no single evaluation layer catches every issue."

> "As a rule, we do not take eval scores at face value until someone digs into the details of the eval and reads some transcripts."

> "Teams without evals get bogged down in reactive loops—fixing one failure, creating another, unable to distinguish real regressions from noise."

---

## 이식 가능한 원시요소

- **P1. Grader 3분류 체계 (Code / Model / Human)** — standalone-extractable: **yes**. 어떤 agent 하네스에도 채점 레이어 설계 시 직접 적용 가능. hybrid scoring 가중치 설계 패턴 포함.
- **P2. Capability→Regression eval 수명주기 패턴** — standalone-extractable: **yes**. 초기 도전적 태스크 풀 → 포화 시 regression suite 승격 → 더 어려운 capability eval로 교체. 이터레이션 경계 관리에 직접 이식 가능.
- **P3. pass@k / pass^k 이중 지표** — standalone-extractable: **yes**. 코드 한 줄로 계산. 신뢰성 요구사항에 따라 어느 지표를 primary로 쓸지 결정 기준 제공.
- **P4. 8단계 eval 로드맵** — standalone-extractable: **yes**. 새 agent 시스템 구축 시 eval-driven development 초안으로 즉시 활용 가능. Step 2 (애매하지 않은 task 작성 기준)와 Step 5 (grader 설계 원칙)가 핵심 추출 가치.
- **P5. Step-sequence grader 금지 원칙** — standalone-extractable: **yes**. "에이전트가 특정 도구 호출 순서를 따랐는지 검사하지 마라" — 창의적 솔루션 탐색 공간 보존을 위한 설계 제약으로 모든 harness eval에 적용.
- **P6. Swiss Cheese 다층 eval 모델** — standalone-extractable: **partial**. 자동 eval + 프로덕션 모니터링 + A/B + 유저 피드백 + 수동 검토 + human study 6층 구조. 조직 규모에 따라 서브셋만 채택 가능.
- **P7. Balanced problem set (positive/negative) 원칙** — standalone-extractable: **yes**. 클래스 불균형이 false confidence를 유발한다는 경고와 함께 웹 검색 eval 예시가 직관적 설계 가이드 역할.

---

## 기존 하네스 노트와의 연결

### ECC (`notes/harness/ecc.md`)
ECC의 **Instinct Learning 레이어** (NanoClaw v2의 신뢰도 기반 라우팅)는 사실상 암묵적 "모델 기반 self-grader"다. 이 포스트의 Model-based grader 설계 원칙 — 특히 "LLM grader를 human expert와 calibrate해야 한다" — 이 ECC instinct scoring의 검증 공백을 정확히 지적한다. ECC는 자체 eval 인프라를 공개하지 않으므로, 이 포스트의 8단계 로드맵은 ECC 기반 시스템의 eval 레이어를 추가할 때 직접 참조 가능한 청사진이 된다.

### Compound Engineering (`notes/harness/compound-engineering.md`)
Compound Engineering의 14개 병렬 리뷰 서브에이전트 구조는 이 포스트의 **multi-judge consensus** Model-based grader 패턴과 직접 대응된다. 14개 역할(security-sentinel, dhh-rails-reviewer, performance-oracle 등)은 각각 독립적인 "dimensional grader"로 볼 수 있으며, 이 포스트가 권고하는 "isolated dimensional grading" 원칙을 실제로 구현한 형태다. 단, Compound Engineering은 이 리뷰 결과를 regression suite로 전환하는 메커니즘이 없어 **Capability→Regression 수명주기 패턴(P2)** 이식이 유력한 개선 포인트다.

### 공통 교훈 — Reactive Loop vs. Eval-Driven
ECC와 Compound Engineering 모두 반복 이터레이션 품질을 높이기 위한 메모리/학습 레이어를 갖추지만, 이 포스트가 말하는 "teams without evals get bogged down in reactive loops" 경고는 양 하네스 모두에 해당한다. 공식적인 eval suite 없이 운영될 경우, 하네스의 자체 학습 루프(ECC `/evolve`, Compound `docs/solutions/`)가 노이즈와 실제 회귀를 구별하지 못하는 위험이 있다.

---

## 후속 조사 / 빈틈

- **τ2-Bench 상세 구조**: Conversational agent eval을 위한 유저 시뮬레이션 LLM 설계 원칙이 포스트에서 약술만 됨. τ-Bench와 τ2-Bench 원문 논문 직접 분석 필요.
- **Harbor 프레임워크 내부**: Anthropic이 직접 언급한 오픈소스 eval 하네스 Harbor의 task/grader 포맷 명세와 cloud-scale trial 관리 방식 상세 조사.
- **METR Time Horizon Benchmark 사고 원인 분석**: "목표를 무시하는 모델에 보상" 사고의 구체적 grader 설계 결함 역추적 — eval 안전성 설계 원칙으로 정리 가능.
- **Eval 포화 이후 전략**: SWE-Bench Verified >80% 포화 상태에서 Anthropic이 실제로 어떤 next-level benchmark로 이동했는지 추적 필요.
- **Human calibration 프로토콜**: Model-based grader를 human expert와 calibrate하는 구체적 방법론(인원 수, 불일치 해소 절차, inter-rater reliability 임계값)이 포스트에서 언급되지 않음.
- **ECC + Compound Engineering eval 레이어 추가 실험**: P2(Capability→Regression 수명주기)와 P5(step-sequence grader 금지)를 두 하네스에 이식하는 구체적 프로토타입 설계 가치 있음.
