---
title: Effective context engineering for AI agents
date: 2026-04-17
source_url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
source_type: blog
topic: techniques
tags: [anthropic, context-engineering, agent, compaction, sub-agent, few-shot, tool-design, long-horizon]
status: processed
---

## 요약 (3줄 이내)

Context engineering은 프롬프트 엔지니어링의 자연적 진화로, 단일 프롬프트 제작에서 벗어나 LLM 추론 전 구간에 걸친 토큰 집합 전체(시스템 지시, 도구, MCP, 외부 데이터, 메시지 히스토리)를 최적 상태로 유지하는 전략 체계다. 핵심 원리는 "원하는 결과를 최대화하는 최소 고신호(high-signal) 토큰 집합 찾기"이며, 컨텍스트가 커질수록 모델 정밀도는 감소하는 "context rot" 문제를 중심 제약으로 삼는다.

---

## 핵심 포인트 (5~10개)

1. **Context engineering 정의**: "LLM 추론 중 최적 토큰(정보) 집합을 선별·유지하는 전략의 총체 — 프롬프트 외부에서 컨텍스트에 유입되는 모든 정보를 포함."
2. **4대 컨텍스트 레이어**: 시스템 프롬프트, 도구(Tools), 예시(Examples / Few-shot), 메시지 히스토리 & 메타데이터.
3. **Context rot**: 트랜스포머 구조상 n개 토큰은 n² 쌍별 관계를 생성하며, 컨텍스트가 길어질수록 장거리 추론 정밀도가 점진적으로 저하된다.
4. **Just-in-time 컨텍스트 로딩**: 에이전트가 모든 데이터를 사전에 로드하지 않고 경량 식별자(파일 경로, 링크 등)만 유지한 뒤, 런타임에 도구로 필요 데이터를 동적으로 로드한다.
5. **Compaction**: 컨텍스트 한계에 도달 시 대화 히스토리를 요약·압축해 재시작. 핵심 보존 대상: 아키텍처 결정, 미해결 버그, 구현 세부사항. 저비용 최적화로 "tool result clearing"(캐시 후 원본 결과 제거)이 권장된다.
6. **구조화 메모(Agentic Memory)**: NOTES.md 등 컨텍스트 외부에 지속 기록을 유지, 복잡한 장기 태스크에서 상태를 추적한다. Anthropic의 memory tool(공개 베타)이 이를 지원.
7. **서브에이전트 아키텍처**: 전문 서브에이전트가 수만 토큰을 소비하지만 1,000–2,000 토큰의 압축 요약만 메인 에이전트에 반환 → 관심 분리(separation of concerns) 실현.
8. **도구 설계 원칙**: 기능 중복 최소화, 자기완결성, 오류 견고성, 입력 파라미터의 명확한 설명. 엔지니어 자신이 상황별 적합 도구를 고르기 어렵다면 에이전트도 어렵다.
9. **시스템 프롬프트 원칙**: 단순·직접적 언어, XML 태그 또는 마크다운 헤더로 섹션 구분, 최소 시작 후 실패 모드에서 점진적 추가.
10. **핵심 격언**: "Do the simplest thing that works" — 팀에 대한 최선의 조언으로 명시됨.

---

## 저자의 프레임워크 / 명시적 주장

### 레이어 모델
| 레이어 | 핵심 지침 |
|--------|-----------|
| 시스템 프롬프트 | 추상화 수준 적절히, 너무 경직되거나 모호하지 않게 |
| 도구 | 중복 제거, 자기완결, 파라미터 명확성 |
| 예시(Few-shot) | 다양하고 전형적인 예시, edge case 과적재 금지 |
| 메시지 히스토리 | 경량 식별자 + just-in-time 로딩, 메타데이터 활용 |

### 장기 태스크 3대 전략
1. **Compaction** — 대화 요약 후 재시작
2. **Structured Note-taking** — 외부 지속 기록
3. **Sub-agent 아키텍처** — 압축 요약만 상위로 전달

### 상위 원리
> "Find the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."

### 모델 지능과의 관계
스마트한 모델일수록 덜 처방적인 엔지니어링으로 더 많은 자율성을 허용할 수 있다. 복잡성을 엔지니어링 단계가 아닌 모델 추론으로 위임하는 방향이 바람직하다.

---

## 구체적 패턴·체크리스트·숫자

- **서브에이전트 반환 토큰**: 작업당 수만 토큰 소비 → 요약 1,000–2,000 토큰만 반환
- **Claude Code 구현 예시**: CLAUDE.md는 naive하게 컨텍스트에 투입, `glob`·`grep` 도구로 just-in-time 탐색. Bash `head`·`tail`로 대용량 데이터를 컨텍스트에 적재하지 않고 분석.
- **Compaction 튜닝 순서**: recall 최대화로 시작 → precision 개선 방향으로 반복
- **Tool result clearing**: 캐시된 결과는 원본 제거 가능 — 저비용 compaction 최적화
- **시스템 프롬프트 작성 순서**: 최소 시작 → 테스트 중 발견한 실패 모드를 기반으로 추가
- **Hybrid 전략**: 속도를 위한 사전 검색 + 에이전트 자율 탐색 결합

---

## 인용 가치 있는 구절

> "Context, therefore, must be treated as a finite resource with diminishing marginal returns."

> "Like humans, who have limited working memory capacity, LLMs have an 'attention budget' that they draw on when parsing large volumes of context."

> "The guiding principle remains the same: find the smallest set of high-signal tokens that maximize your desired outcome."

> "Smarter models require less prescriptive engineering, allowing agents to operate with more autonomy."

> "Do the simplest thing that works will likely remain our best advice for teams building agents."

---

## 이식 가능한 원시요소

- **P1. Just-in-time 컨텍스트 로딩 패턴** — 경량 식별자 유지, 런타임 동적 로드 — standalone-extractable: yes
- **P2. Compaction + tool result clearing 루틴** — 컨텍스트 한계 도달 시 요약·재시작, 캐시 후 원본 제거 — standalone-extractable: yes
- **P3. Sub-agent 압축 반환 패턴** — 수만 토큰 처리 후 1,000–2,000 토큰 요약만 상위 에이전트에 전달 — standalone-extractable: yes
- **P4. NOTES.md / 외부 지속 기록 패턴** — 에이전트 메모리 도구 없이도 파일 기반으로 구현 가능 — standalone-extractable: yes
- **P5. 최소 시스템 프롬프트 → 점진적 확장 원칙** — 실패 모드 기반 추가, over-engineering 방지 — standalone-extractable: yes
- **P6. Context rot 인식 프레임** — n² 관계 비용, 장거리 추론 정밀도 감소 — standalone-extractable: partial (이론 배경 필요)
- **P7. Hybrid 검색 전략** — 사전 인덱싱(속도) + 런타임 자율 탐색(유연성) — standalone-extractable: yes

---

## 기존 하네스 노트와의 연결

- **ralph-wiggum**: 하네스 실행 컨텍스트 구조와 직결. 시스템 프롬프트 레이어 설계 원칙(단순·직접·섹션 분리)이 ralph-wiggum의 에이전트 지시 구조에 그대로 적용 가능.
- **ouroboros**: Compaction + sub-agent 아키텍처의 "압축 요약만 상위로 반환" 패턴은 ouroboros의 자기참조적 루프 관리 메커니즘과 연결됨. 컨텍스트 재초기화 시 무엇을 보존·폐기할지 결정 기준을 제공.
- **gsd** (Get Stuff Done): "Do the simplest thing that works" 원칙 및 최소 시작 후 점진적 확장 접근은 gsd 하네스의 실행 철학과 직접 정렬됨.
- **compound-engineering**: Sub-agent 아키텍처와 관심 분리(separation of concerns) 패턴은 compound-engineering 노트의 다중 에이전트 조합 전략과 보완적.
- **ecc** (Effective Context Control, 있을 경우): 본 포스트 자체가 ecc 범주의 원천 자료. Just-in-time 로딩 및 hybrid 검색 전략은 ecc 노트의 핵심 레퍼런스로 적합.

---

## 후속 조사 / 빈틈

1. **Context rot의 정량적 벤치마크**: n² 관계 비용과 실제 성능 저하 간 수치 데이터가 포스트에 없음. Needle-in-a-haystack 류 실험 결과가 보완 자료로 필요.
2. **Memory tool 구체 사양**: Anthropic 공개 베타 memory tool의 API 인터페이스, 저장 용량, 검색 방식이 미공개 상태.
3. **Compaction precision 튜닝 기준**: "recall 최대화 후 precision 개선"이라는 방향만 제시되었고, 실제 메트릭이나 평가 방법은 언급 없음.
4. **Few-shot 예시 수 최적값**: "diverse, canonical examples"가 권장되나 구체적 개수 기준 없음.
5. **MCP(Model Context Protocol) 레이어 심화**: 포스트에서 MCP를 컨텍스트 구성 요소로 언급하나 MCP 고유의 컨텍스트 관리 전략은 별도 조사 필요.
6. **Pokémon 에이전트 사례 원문**: "수천 게임 스텝에 걸친 정밀 추적"이 언급되나 구체 논문·포스트 링크 부재.
