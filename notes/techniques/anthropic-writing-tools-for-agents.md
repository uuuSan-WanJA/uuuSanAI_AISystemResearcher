---
title: Writing effective tools for agents — with agents
date: 2026-04-17
source_url: https://www.anthropic.com/engineering/writing-tools-for-agents
source_type: blog
topic: techniques
tags: [anthropic, tool-design, mcp, agent-evaluation, token-efficiency, description-engineering]
status: processed
---

## 요약 (3줄 이내)

Tool을 agent가 소비하는 "계약서"로 재정의하고, 빌드→평가→에이전트와 협업 최적화의 3단계 반복 루프를 제안한다.
핵심 원칙은 도구 수를 줄이고, 설명을 신입사원 온보딩 문서처럼 작성하며, 에러 메시지가 actionable 가이드 역할을 해야 한다는 것이다.
내부 Slack/Asana MCP 서버 평가에서 사람이 작성한 버전 대비 Claude 최적화 버전이 held-out 테스트셋에서 눈에 띄는 정확도 향상을 보였다.

## 핵심 포인트

- **도구는 비결정론적 계약**: 기존 소프트웨어는 결정론적 시스템 간 계약이지만, tool은 결정론적 시스템과 비결정론적 agent 사이의 계약이다. agent는 hallucinate하고 도구를 오용할 수 있으므로 설계 원칙을 재검토해야 한다.
- **적을수록 좋다**: 단순 API wrapper를 나열하는 것보다 agent 워크플로에 맞춘 소수의 고수준 도구가 성능·토큰 효율 양면에서 우세하다.
- **Description = 문서**: tool description을 "신입 팀원에게 주는 온보딩 문서"처럼 작성해야 하며, 암묵적 컨텍스트(쿼리 형식, 용어, 리소스 관계)를 명시적으로 기술해야 한다.
- **에러 메시지도 프롬프트다**: 불투명한 traceback 대신 파라미터 형식 요건·유효 예시를 담은 actionable 에러 응답이 agent를 올바른 경로로 steering한다.
- **평가 주도 반복**: top-level 정확도, 런타임, 총 tool call 수, 토큰 소비, 에러율 5가지 지표로 평가하고 raw transcript를 직접 리뷰한다.

## 저자의 프레임워크 / 명시적 주장

### 3단계 반복 루프
1. **Build prototypes** — Claude Code와 `llms.txt` 등 LLM-friendly 문서를 활용해 빠르게 프로토타입 제작
2. **Run evaluations** — 다중 tool call이 필요한 실세계 시나리오로 체계적 측정
3. **Collaborate with agents** — Claude로 결과를 분석하고 tool을 자동 최적화

### 5대 설계 원칙
1. **Choose Intentional Tools** — 도구 통합: `list_users` + `list_events` + `create_event` → `schedule_event`처럼 affordance 기준 재설계
2. **Implement Strategic Namespacing** — 공통 prefix 그룹핑(`asana_projects_search`, `asana_users_search`); prefix vs. suffix 선택이 성능에 measurable 차이를 낸다
3. **Return High-Signal Context** — UUID·MIME type 대신 자연어 이름(`name`, `image_url`)을 우선; `ResponseFormat` enum(`"detailed"` / `"concise"`)으로 토큰을 유연하게 제어
4. **Optimize for Token Efficiency** — pagination, range selection, filtering, truncation 구현; Claude Code 기본값은 응답 25,000 tokens 제한
5. **Prompt-Engineer Descriptions and Specs** — 파라미터 이름은 `user` 대신 `user_id`처럼 unambiguous하게; MCP tool annotation으로 접근 수준·파괴적 변경 여부 명시

## 구체적 패턴·체크리스트·숫자

| 항목 | 내용 |
|---|---|
| 토큰 절감 예시 | Slack tool: detailed 응답 206 tokens → concise 응답 72 tokens (65% 절감) |
| 기본 응답 상한 | Claude Code: 25,000 tokens/응답 |
| SWE-bench 레퍼런스 | Sonnet 3.5 SWE-bench 성능이 tool description 정밀 수정 후 극적으로 향상됨 |
| 평가 지표 5종 | top-level accuracy, runtime/call, total call count, token consumption, tool errors |
| 응답 구조 포맷 | XML·JSON·Markdown 중 어느 것이 최적인지 평가로 결정(범용 정답 없음) |

**Tool description 작성 체크리스트 (글 기반 재구성):**
- [ ] 암묵적 컨텍스트(쿼리 언어, 필터 옵션, 관련 리소스)를 명시했는가?
- [ ] 파라미터 이름이 충분히 unambiguous한가? (`id` → `user_id`, `order_id`)
- [ ] 에러 응답에 파라미터 형식 요건과 유효 예시가 포함되어 있는가?
- [ ] 토큰 절감을 위한 `ResponseFormat` 또는 pagination이 구현되어 있는가?
- [ ] 도구가 실제 에이전트 워크플로 단위로 통합되어 있는가?
- [ ] MCP annotation으로 destructive 여부가 표시되어 있는가?

**Helpful error 패턴:**
```
❌ "TypeError: invalid param"
✓  "user_id must be an integer (e.g. 12345). 
    To look up a user ID, call get_user(email=...) first."
```

**도구 통합 예시:**
- `read_logs` → `search_logs`
- 여러 customer 조회 도구 → `get_customer_context`

## 인용 가치 있는 구절

> "Traditional software establishes contracts between deterministic systems. Tools represent a new paradigm: contracts between deterministic systems and non-deterministic agents."

> "Think of descriptions as onboarding documentation for new team members — make implicit context explicit."

> "Fewer, more thoughtful tools outperform comprehensive coverage."

> "Helpful error responses should provide actionable guidance, not opaque error codes."

> "Small refinements yield dramatic improvements — Sonnet 3.5's SWE-bench performance improvement followed precise tool description refinements."

## 이식 가능한 원시요소

- P1. **`ResponseFormat` enum 패턴** (`"detailed"` / `"concise"`) — tool 응답 구조에 그대로 적용 가능 — standalone-extractable: yes
- P2. **도구 통합 휴리스틱** — 동일 도메인 내 3개 이상의 CRUD-level 도구를 workflow 단위 1개로 축소 — standalone-extractable: yes
- P3. **Namespacing prefix 규칙** — `<server>_<resource>_<action>` 구조 — standalone-extractable: yes
- P4. **Actionable 에러 메시지 템플릿** — 형식 요건 + 유효 예시 + 다음 단계 제안 — standalone-extractable: yes
- P5. **평가 지표 5종 세트** — harness 평가 루프에 직접 통합 가능 — standalone-extractable: yes
- P6. **3단계 반복 루프(빌드→평가→에이전트 협업)** — 새 tool 개발 파이프라인으로 채택 — standalone-extractable: partial (평가 인프라 필요)

## 기존 하네스 노트와의 연결

- **compound-engineering**: "intentional tool selection = cognitive affordance 설계" 관점이 compound system의 task decomposition 원칙과 직접 연결됨. 에이전트가 소비하는 tool API를 compound 설계의 인터페이스 계층으로 볼 수 있음.
- **ouroboros**: 3단계 루프의 3단계("에이전트로 에이전트 최적화")가 ouroboros의 자기참조 개선 루프와 구조적으로 동일. tool description을 에이전트가 자동 rewrite하는 패턴이 직접 적용 가능.
- **superpowers**: `ResponseFormat` enum과 토큰 절감 전략이 "에이전트에게 적절한 정보 밀도 제공"이라는 superpowers의 컨텍스트 윈도우 관리 논의와 연결됨.
- **gsd**: 도구 통합 휴리스틱(`schedule_event`처럼 workflow 단위 설계)이 GSD의 task-oriented 분해와 일치. actionable error 메시지가 agent self-correction 루프를 지원하는 방식도 관련.
- **openspec**: MCP tool annotation(접근 수준, destructive 여부 명시)이 OpenSpec의 API contract 명세 원칙과 동일한 레이어를 다룸.

## 후속 조사 / 빈틈

- **ResponseFormat enum의 구체적 구현 예시**: 블로그에서 개념만 제시되고 실제 코드 패턴은 미공개. Anthropic Developer Guide 원문 확인 필요.
- **Prefix vs. suffix 성능 차이 수치**: "measurable difference"라고만 언급되고 구체적 수치 미공개. 내부 실험 결과 공개 여부 추적.
- **MCP tool annotation 스펙 전문**: 블로그는 개념만 언급; MCP 공식 스펙에서 annotation 필드 완전 목록 확인 필요.
- **held-out 테스트셋 구성 방식**: Slack/Asana 평가에서 "held-out" 데이터를 어떻게 구성했는지 방법론 미공개.
- **XML vs. JSON vs. Markdown 응답 구조 비교 실험**: "no universal solution" 주장의 근거 데이터 미공개; 독자적 재현 실험 가치 있음.
