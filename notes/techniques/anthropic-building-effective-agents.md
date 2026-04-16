---
title: Building effective agents
date: 2026-04-17
source_url: https://www.anthropic.com/engineering/building-effective-agents
source_type: blog
topic: agents
tags: [anthropic, canonical, taxonomy, workflows, agents, augmented-llm, prompt-chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, aci, model-context-protocol]
status: processed
---

## 요약 (3줄 이내)

Anthropic이 수십 개 팀과의 실전 경험을 바탕으로 정리한 에이전트 시스템 설계 레퍼런스 포스트. **Workflow**(코드 경로로 LLM을 고정 배열)와 **Agent**(LLM 스스로 프로세스를 지시)를 분류하고, 5가지 workflow 패턴 + 1가지 autonomous agent 패턴의 구성·용도·한계를 기술한다. 핵심 메시지는 "복잡도는 성과가 입증될 때만 추가하라"는 단순성 우선 원칙이다.

---

## 핵심 포인트

- **Augmented LLM**이 모든 패턴의 기반: 검색(retrieval), 도구(tools), 메모리(memory)를 갖춘 LLM이 기본 빌딩블록.
- Workflow는 예측 가능성과 일관성이 장점; Agent는 유연성과 자율적 멀티스텝이 장점.
- 단일 LLM 호출 + retrieval + in-context 예시만으로 충분한 경우가 많다 — 먼저 단순하게 시도하라.
- 에이전트 시스템은 지연(latency)·비용(cost) 트레이드오프가 있으므로, 실질적 성과 개선이 있을 때만 복잡도를 도입한다.
- **ACI(Agent-Computer Interface)** 설계에 HCI만큼의 공을 들여야 한다 — 툴 문서화·테스트·poka-yoke 원칙 적용.
- 프레임워크 사용 전에 LLM API 직접 호출로 시작하라; 프레임워크가 프롬프트·응답을 가리면 디버깅이 어려워진다.

---

## 저자의 프레임워크 / 명시적 주장

### Workflow vs. Agent 정의

| 구분 | 정의 | 특성 |
|---|---|---|
| **Workflow** | 미리 정의된 코드 경로를 통해 LLM과 도구를 오케스트레이션하는 시스템 | 예측 가능·일관성↑, 유연성↓ |
| **Agent** | LLM이 자신의 프로세스와 도구 사용을 동적으로 지시하며 과제 수행을 스스로 결정하는 시스템 | 유연성·자율성↑, 비용·지연·오류 누적 위험↑ |

저자는 두 용어를 엄격히 분리하지 않는 생태계 현실을 인정하면서도, **설계 결정에서 이 구분이 실질적으로 중요**하다고 강조한다.

### Building Block: Augmented LLM

모든 패턴의 기반 단위. LLM이 다음을 능동적으로 제어한다:
- **Retrieval**: 검색 쿼리를 스스로 생성
- **Tools**: 적합한 도구를 스스로 선택
- **Memory**: 유지해야 할 정보를 스스로 결정

외부 도구 통합에는 **Model Context Protocol(MCP)** 사용 권장.

### 5가지 Workflow 패턴

| 패턴 | 구조 | 주요 용도 |
|---|---|---|
| **Prompt Chaining** | 순차 LLM 호출 체인; 선택적 중간 게이트("gates") | 마케팅 카피 → 번역, 개요 검증 후 본문 작성 |
| **Routing** | 입력 분류 → 전문 후속 태스크로 라우팅 | 고객 서비스 쿼리 유형별 분기, 난이도별 모델 선택 |
| **Parallelization** | 독립 서브태스크 병렬 실행(Sectioning) 또는 동일 태스크 다중 실행(Voting) | 콘텐츠 스크리닝 + 응답 생성 동시화, 코드 취약점 다중 검토 |
| **Orchestrator-Workers** | 중앙 LLM이 서브태스크 동적 분배 → 워커 LLM 실행 → 결과 종합 | 멀티파일 코드 변경, 복수 소스 정보 수집 |
| **Evaluator-Optimizer** | 생성 LLM + 평가 LLM 반복 루프 | 문학 번역 품질 향상, 복잡한 다단계 검색 |

#### Parallelization 세부 변형

- **Sectioning**: 태스크를 독립 서브태스크로 분해해 동시 실행 → 처리 속도↑
- **Voting**: 동일 태스크를 여러 번 독립 실행 → 다양한 출력 확보, 다수결 또는 임계값 표결

### Autonomous Agent 패턴

LLM이 도구 기반 피드백 루프에서 독립적으로 동작:
1. 사용자 명령 또는 대화로 시작
2. 독립적으로 계획·실행
3. 도구 결과를 통해 실세계 진실(ground truth) 유지
4. 검사 지점 또는 장애물에서 인간 피드백 요청을 위해 일시 정지

용도: SWE-bench 멀티파일 수정, 컴퓨터 사용(computer use) 구현.

---

## 구체적 패턴·체크리스트·숫자

### Prompt Chaining
- **구성**: LLM 호출 → (선택적 gate 검증) → 다음 LLM 호출
- **Gate**: 조건 실패 시 프로세스 중단하는 프로그래밍 방식 체크
- **예시 1**: 마케팅 카피 생성 → 대상 언어 번역
- **예시 2**: 문서 개요 작성 → 검증 gate → 전체 문서 생성

### Routing
- **구성**: 분류 LLM/로직 → 입력 유형 판별 → 전문화된 후속 처리로 전달
- **예시 1**: 고객 서비스 쿼리를 환불·기술지원·일반 문의로 분류
- **예시 2**: 단순 질문 → Claude Haiku 4.5, 복잡한 질문 → Claude Sonnet 4.5

### Parallelization
- **Sectioning 예시**: 안전 정책 위반 스크리닝 + 사용자 응답 생성 병렬 실행; 에이전트 성능 자동 평가 다면 동시 처리
- **Voting 예시**: 코드 취약점 리뷰를 서로 다른 프롬프트로 여러 번 실행; 콘텐츠 적절성 평가에 투표 임계값 적용

### Orchestrator-Workers
- **구성**: Orchestrator LLM이 입력 기반으로 서브태스크를 동적 결정 → Worker LLM 병렬/순차 실행 → 결과 통합
- Parallelization과의 차이: **서브태스크가 사전 고정되지 않고 오케스트레이터가 실시간 결정**
- **예시**: 여러 파일을 수정하는 복잡한 코딩 작업; 여러 소스에서 정보를 수집하는 검색 태스크

### Evaluator-Optimizer
- **구성**: Generator LLM → 생성 → Evaluator LLM → 피드백 → Generator LLM → 반복
- **종료 조건**: 평가자가 합격 판정 또는 최대 반복 횟수 도달
- **예시 1**: 미묘한 뉘앙스가 중요한 문학 번역 — 번역 생성 → 비평 → 재번역
- **예시 2**: 여러 라운드의 분석·검색이 필요한 복잡한 검색 태스크

### 에이전트 설계 핵심 원칙 (체크리스트)
1. **단순성 유지**: 에이전트 설계를 단순하게 시작
2. **투명성**: 계획 단계를 명시적으로 드러내기
3. **ACI 정교화**: 툴 문서화와 테스트에 충분히 투자

### Tool/ACI 설계 권장사항
- 모델이 "코너에 몰리기 전에 생각할" 충분한 토큰 제공
- 포맷을 인터넷에서 자연스럽게 발생하는 텍스트에 가깝게 유지
- 포맷 오버헤드 제거: 정확한 줄 수 계산이나 과도한 문자열 이스케이핑 요구 지양
- 예시 사용법, 엣지 케이스, 입력 포맷 요구사항, 명확한 툴 경계 포함
- 워크벤치에서 예시 입력으로 충분히 테스트
- **Poka-yoke 원칙**: 인자 설계로 실수 자체를 방지 (예: 절대 파일 경로 요구)

---

## 인용 가치 있는 구절

> "The most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns."

> "You should consider adding complexity only when it demonstrably improves outcomes."

> "For many applications, however, optimizing single LLM calls with retrieval and in-context examples is usually enough."

> "Think about how much effort goes into human-computer interfaces (HCI), and plan to invest just as much effort in creating good agent-computer interfaces (ACI)."

> "Frameworks can help you get started quickly, but don't hesitate to reduce abstraction layers and build with basic components as you move to production."

---

## 이식 가능한 원시요소

- **P1. Gate mechanism in Prompt Chaining** — 중간 단계에 프로그래밍 방식 검증 체크포인트 삽입. standalone-extractable: **yes**
- **P2. Voting via Parallelization** — 동일 태스크 다중 실행 후 임계값 기반 표결. standalone-extractable: **yes**
- **P3. Orchestrator-Workers dynamic decomposition** — 오케스트레이터가 입력에 따라 실시간 서브태스크 결정. standalone-extractable: **yes**
- **P4. Evaluator-Optimizer loop** — 생성자-평가자 분리 반복 루프. standalone-extractable: **yes**
- **P5. ACI poka-yoke tool design** — 인자 설계로 에이전트 실수를 사전 차단. standalone-extractable: **yes**
- **P6. Routing by complexity/type** — 입력 난이도나 유형에 따라 다른 모델/프롬프트 경로 선택. standalone-extractable: **yes**
- **P7. Augmented LLM as composable base unit** — retrieval·tools·memory를 장착한 LLM을 모든 패턴의 기반으로 재사용. standalone-extractable: **yes**
- **P8. 단순성 우선 + 복잡도 점진 도입** — 벤치마크 개선이 입증될 때만 복잡도 추가. standalone-extractable: **yes** (조직 원칙)

---

## 기존 하네스 노트와의 연결

### Compound Engineering (`notes/harness/compound-engineering.md`)
- **Orchestrator-Workers + Evaluator-Optimizer 결합**: `/ce:plan` (3개 병렬 연구 에이전트 → 통합)은 Orchestrator-Workers의 전형적 구현. `/ce:review` (14개 병렬 전문 심사 에이전트 + P1/P2/P3 종합)는 Parallelization(Sectioning) + Evaluator-Optimizer 혼합.
- **Evaluator-Optimizer**: `/ce:compound` 단계에서 학습을 추출·평가 후 다음 루프에 주입하는 구조가 다세대 evaluator-optimizer의 변형.
- **ACI poka-yoke**: `CLAUDE.md` 누적 학습이 다음 세션 에이전트에게 실수 방지 컨텍스트를 사전 제공 — 포스트의 "툴 문서 최적화"와 직결.

### ECC (`notes/harness/ecc.md`)
- **Orchestrator-Workers**: NanoClaw v2 오케스트레이터가 모델 라우팅·스킬 핫로드를 동적 결정 — Orchestrator-Workers 패턴의 구현체.
- **Parallelization(Voting)**: 14개 도메인 전문 에이전트가 동일 코드를 병렬 심사 후 신뢰도 임계값(80%)으로 필터링 — Voting 패턴의 직접 구현.
- **Evaluator-Optimizer**: `/learn` → `/evolve` 사이클이 생성자(에이전트)-평가자(instinct 신뢰도 스코어러) 반복 루프.
- **Augmented LLM**: 47개 전문화 서브에이전트 각각이 retrieval·tool 접근을 갖춘 augmented LLM 단위.

### Ouroboros (`notes/harness/ouroboros.md`)
- **Evaluator-Optimizer**: `interview → seed → execute → evaluate → evolve` 사이클 전체가 다세대 evaluator-optimizer. 특히 ontology similarity ≥ 0.95 수렴 조건이 포스트의 "종료 조건" 설계 권장을 수치로 구현.
- **Routing**: PAL Router(Frugal→Standard→Frontier)가 태스크 난이도에 따른 모델 라우팅 — 포스트의 "단순 질문은 소형 모델, 복잡한 질문은 대형 모델" 권장의 자동화 버전.
- **Prompt Chaining with Gates**: ambiguity ≤ 0.2 게이트가 코드 생성 단계 진입을 차단 — 포스트의 "gate" 개념을 수치 임계값으로 구현.

### GSD (`notes/harness/gsd.md`)
- **Prompt Chaining**: `/gsd:discuss-phase → plan-phase → execute-phase → verify-work → ship` 체인이 Prompt Chaining의 5단계 구현. 각 단계가 이전 출력을 입력으로 받음.
- **Routing**: 프레시 서브에이전트 컨텍스트로 카브오프(carve-off)하는 방식이 입력 복잡도에 따른 컨텍스트 라우팅.

### Ralph Wiggum (`notes/harness/ralph-wiggum.md`)
- **Autonomous Agent**: `while true` bash 루프 + `--dangerously-skip-permissions` = 포스트가 기술하는 "도구 기반 피드백 루프에서 독립적으로 동작하는 에이전트"의 극단적 단순 구현. 파일시스템이 ground truth.
- **Evaluator-Optimizer 부재**: Ralph의 핵심 한계 중 하나가 독립적인 평가자 없이 무한 루프한다는 점 — 포스트의 evaluator-optimizer 패턴이 Ralph의 취약점에 직접 대응.

### Superpowers (`notes/harness/superpowers.md`)
- **Prompt Chaining**: `brainstorm → spec → plan → TDD → subagent dev → review → finalize` 7단계 체인이 Prompt Chaining의 가장 정교한 구현체 중 하나.
- **Evaluator-Optimizer**: `<HARD-GATE>` XML 태그가 게이트 메커니즘, v5.0.6 이전 독립 서브에이전트 리뷰가 Evaluator-Optimizer의 직접 구현(비용 문제로 self-review로 롤백됨 — 포스트의 "cost 트레이드오프" 경고와 일치).
- **Orchestrator-Workers**: 구현 서브에이전트와 리뷰 서브에이전트 분리가 Workers 패턴.

### gstack (`notes/harness/gstack.md`)
- **Routing**: 23개 슬래시 커맨드가 각각 다른 역할(CEO/EM/Staff Engineer/QA Lead...)로 라우팅 — 입력 유형(의사결정 관점)에 따른 전문화 라우팅.
- **Parallelization(Sectioning)**: 동일 변경을 CEO 관점·엔지니어 관점·QA 관점으로 동시 평가 가능한 구조.

### OpenSpec (`notes/harness/openspec.md`)
- **Prompt Chaining with Gates**: `/opsx:propose → apply → archive` 체인 + `/opsx:verify` 소프트 게이트가 Prompt Chaining의 명시적 구현.
- **Evaluator-Optimizer**: 델타 마커(ADDED/MODIFIED/REMOVED Requirements)로 변경 전후를 추적하는 구조가 반복적 평가-개선 루프.

### revfactory/harness (`notes/harness/revfactory-harness.md`)
- **Orchestrator-Workers**: 6단계 파이프라인이 에이전트 팀 + 스킬 파일 전체를 동적 생성 — 메타 수준의 Orchestrator-Workers 패턴(오케스트레이터가 워커를 생성).
- **Parallelization**: 15개 소프트웨어 태스크 A/B 실험 자체가 Voting 패턴의 실험 설계와 유사.

---

## 후속 조사 / 빈틈

- **패턴 간 조합 기준**: 포스트는 각 패턴을 독립 설명하지만, 어떤 조건에서 어떤 패턴을 조합하는지(예: orchestrator-workers + evaluator-optimizer)에 대한 결정 기준이 불명확. 실전 기준 프레임워크 탐색 필요.
- **MCP 통합 깊이**: Model Context Protocol이 Augmented LLM 구현 방식으로 언급되나 패턴별 MCP 활용법은 별도 포스트/문서 확인 필요.
- **비용 측정 사례**: "latency and cost tradeoff" 언급이 있으나 구체적 수치 없음 — SWE-bench 케이스 스터디 등에서 실제 비용 데이터 추적 필요.
- **에이전트 안전 샌드박스**: "sandboxed environments with appropriate guardrails" 언급이 있으나 구체적 샌드박싱 아키텍처 미상. Anthropic의 별도 안전 문서 교차 확인 필요.
- **단일 LLM 호출 충분성 임계값**: "많은 애플리케이션에서 단일 호출로 충분하다"는 주장의 기준(태스크 복잡도, 정확도 요건 등) 미명시. 실무 결정 트리 부재.
- **Routing 분류기 설계**: 포스트는 routing의 효과를 기술하나 분류기 자체(LLM 기반 vs. 규칙 기반)의 설계 가이드라인 부재 — 후속 리서치 여지.
