---
title: How we built our multi-agent research system
date: 2026-04-17
source_url: https://www.anthropic.com/engineering/multi-agent-research-system
source_type: blog
topic: agents
tags: [anthropic, multi-agent, orchestrator-worker, research, claude-opus-4, claude-sonnet-4, parallel-agents, evaluation, token-cost, citation-agent]
status: processed
---

## 요약 (3줄 이내)

Anthropic이 직접 구축·운영한 orchestrator-worker 멀티에이전트 리서치 시스템의 설계 원칙과 실전 경험을 공개한 글. Claude Opus 4(lead) + Claude Sonnet 4(subagents) 구조로 단일 에이전트 대비 90.2% 성능 향상을 달성했으며, 토큰 비용은 일반 채팅 대비 ~15×에 달한다. 프롬프트 엔지니어링, 실패 모드, 평가 방법론, 프로덕션 배포 챌린지를 수치와 함께 상세히 다룬다.

## 핵심 포인트

- **90.2% 성능 향상**: 멀티에이전트(Opus 4 lead + Sonnet 4 subagents) vs 단일 Opus 4 에이전트 (BrowseComp 기준)
- **토큰 분산이 성능의 대리 지표**: BrowseComp 평가에서 토큰 사용량 단독으로 성능 분산의 **80%** 설명
- **경제성 전제조건**: "For economic viability, multi-agent systems require tasks where the value of the task is high enough to pay for the increased performance"
- **프로토타입→프로덕션 갭**: "The last mile often becomes most of the journey"
- **검색 시간 단축**: 복잡한 쿼리 기준 연구 시간 최대 **90% 단축** (병렬화 효과)

## 시스템 아키텍처

### 전체 플로우

```
사용자 쿼리
  → Lead Agent (Claude Opus 4): 전략 수립 + 플랜 메모리 저장
    → Subagents (Claude Sonnet 4) × N: 병렬 탐색 + 도구 호출
      ← 결과 수집
  → CitationAgent: 출처 처리 및 인용 정리
  → 최종 리포트 (인용 포함)
```

### 역할 분할

| 컴포넌트 | 모델 | 책임 |
|---|---|---|
| Lead Agent | Claude Opus 4 | 쿼리 분석, 탐색 전략, subagent 지시, 결과 통합 |
| Subagents | Claude Sonnet 4 | 병렬 웹 검색, 도구 호출, 중간 결과 반환 |
| CitationAgent | (별도) | 수집된 소스에서 인용 추출·포맷팅 |

### 병렬도 스케일 규칙 (프롬프트 내 임베드)

| 쿼리 복잡도 | Subagent 수 | 도구 호출 수 |
|---|---|---|
| 단순 사실 확인 | 1 | 3–10 |
| 직접 비교 | 2–4 | 각 10–15 |
| 복합 리서치 | **10+** | 분업 구조 |
| 실패 케이스 (과잉) | 50+ | — |

### 메모리 관리

- Context window 200,000 토큰 초과 시 **자동 truncation** → Lead Agent가 플랜을 외부 메모리에 먼저 저장하는 것으로 대응
- Subagents는 **interleaved thinking** 사용: 도구 결과 수신 후 품질 평가 → 갭 식별 → 다음 쿼리 정제

### 병렬 실행 현황

- 현재: **동기식(synchronous)** — 각 subagent 세트 완료를 기다린 후 다음 진행
- 미래 작업: 비동기 실행(asynchronous execution)

## 저자의 프레임워크 / 명시적 주장

1. **Research ≠ retrieval**: "Research demands the flexibility to pivot or explore tangential connections as the investigation unfolds" — 정해진 경로가 아닌 동적 탐색이 핵심
2. **검색의 본질은 압축**: "The essence of search is compression: distilling insights from a vast corpus"
3. **집단 지성 우위**: "Even generally-intelligent agents face limits when operating as individuals; groups of agents can accomplish far more"
4. **경제성 임계점**: 태스크 가치가 토큰 비용(~15× chat)을 상회해야 멀티에이전트가 정당화됨
5. **Mental model 우선**: 프롬프트 작성 전 Anthropic Console에서 정확한 프롬프트·도구 시뮬레이션으로 에이전트 동작 예측
6. **위임의 명시성**: 각 subagent에게 "objective, output format, guidance on tools and sources, clear task boundaries" 4요소를 명시해야 함

## 구체적 패턴·체크리스트·숫자

### 토큰 비용

| 비교 기준 | 토큰 배수 |
|---|---|
| 단일 에이전트 vs 일반 채팅 | ~4× |
| 멀티에이전트 vs 일반 채팅 | **~15×** |

### 프롬프팅 Heuristic

- **도구 우선 탐색**: "examine all available tools first, match tool usage to user intent"
- **검색 전략**: "Start with short, broad queries → evaluate what's available → progressively narrow focus"
- **Extended thinking**: instruction-following, reasoning, efficiency 향상에 효과적
- **Parallel tool calling**: subagent가 **3개 이상 도구를 병렬 호출**하도록 유도
- **도구 설명 품질**: 도구 설명 개선 후 **태스크 완료 시간 40% 단축** (tool-testing agent 실험)

### 실패 모드 목록

1. 충분한 결과 확보 후에도 계속 탐색 (early stopping 부재)
2. 과도하게 장황한 검색 쿼리
3. 잘못된 도구 선택
4. Subagents 간 중복 작업 (태스크 경계 불명확 시)
5. 모호한 지시로 인한 방향 불일치
6. SEO 최적화 콘텐츠 팜을 권위 있는 출처보다 우선 선택
7. 시간적 맥락 혼동 ("2021 automotive chip crisis" ≠ "current 2025 supply chains")
8. 존재하지 않는 출처를 무한 탐색
9. Subagents 간 과도한 업데이트로 서로 방해

### 평가 방법론 (LLM-as-judge)

- **구조**: 단일 프롬프트, 단일 LLM 호출 → 0.0–1.0 스코어 + pass/fail
- **평가 차원**: 사실 정확도, 인용 정확도, 완결성, 소스 품질, 도구 효율
- **초기 규모**: ~20개 테스트 케이스로 시작 ("With effect sizes this large, you can spot changes with just a few test cases")
- **핵심 발견**: 단일 LLM 판단이 앙상블보다 인간 판단과 더 일치

### 프로덕션 엔지니어링

- **Rainbow deployment**: 구 버전 유지하며 트래픽을 점진 전환 (실행 중인 에이전트 중단 방지)
- **Durable execution**: 장기 실행 에이전트의 상태 관리 + 오류 복구
- **비결정성 디버깅**: 동일 프롬프트에도 실행마다 다른 결정 → 재현 불가능한 버그

## 인용 가치 있는 구절

> "Research demands the flexibility to pivot or explore tangential connections as the investigation unfolds"

> "The essence of search is compression: distilling insights from a vast corpus"

> "Even generally-intelligent agents face limits when operating as individuals; groups of agents can accomplish far more"

> "For economic viability, multi-agent systems require tasks where the value of the task is high enough to pay for the increased performance"

> "The last mile often becomes most of the journey"

## 이식 가능한 원시요소

- **P1. 스케일 규칙 프롬프트 임베딩** — 쿼리 복잡도별 subagent 수 + 도구 호출 수를 시스템 프롬프트에 직접 명시 — standalone-extractable: **yes**
- **P2. 4요소 위임 명세** — objective / output format / tool & source guidance / task boundary를 subagent 지시에 항상 포함 — standalone-extractable: **yes**
- **P3. 외부 메모리 플랜 저장 패턴** — context truncation 전에 핵심 플랜을 외부 메모리에 저장 — standalone-extractable: **yes**
- **P4. Interleaved thinking 루프** — 도구 결과 → 품질 평가 → 갭 식별 → 쿼리 정제의 소형 반성 루프 — standalone-extractable: **yes**
- **P5. 단일-프롬프트 LLM 판단 평가기** — 다차원 스코어(0.0–1.0) + pass/fail를 단일 호출로 — standalone-extractable: **yes**
- **P6. 도구 설명 품질 게이트** — 도구 설명 개선만으로 40% 속도 향상 → 도구 메타데이터를 1급 프롬프트 공학 대상으로 취급 — standalone-extractable: **yes**
- **P7. Rainbow deployment for agents** — 장기 실행 에이전트를 깨지 않는 점진적 배포 전략 — standalone-extractable: **partial** (인프라 의존)

## 기존 하네스 노트와의 연결

### ralph-wiggum
Ralph의 **N readers : 1 writer 비대칭 backpressure** 패턴과 직접 연결. Anthropic 시스템도 subagent 결과가 lead agent 단일 컨텍스트로 수렴하는 구조적 병목이 동일하다. Ralph가 plan/build 2-모드로 분리하는 것처럼, Anthropic 시스템도 전략 수립(lead)과 실행(subagents)을 모델 수준에서 분리(Opus vs Sonnet).

### ouroboros
Ouroboros의 500 parallel Sonnet 읽기/검색 아키텍처와 비교 가능. Anthropic 시스템은 10+ subagent 상한이 명시적이며 동기식인 반면, Ouroboros는 비동기 대규모 병렬을 목표로 한다. 토큰 버킷 공유 문제(Issue #371)는 Anthropic의 "경제성 임계점" 논의와 직접 연결.

### superpowers
Superpowers의 orchestrator–workers 패턴(코디네이터 → 구현 subagent → 리뷰 subagent)이 Anthropic 구조와 동형. 단, Superpowers는 v5.0.6에서 subagent 리뷰를 인라인으로 되돌렸는데, 이는 Anthropic의 "~15× 토큰 비용" 경제성 문제와 같은 원인으로 추정됨. P6(도구 설명 품질)은 Superpowers의 SKILL.md 표준화와 동일한 원리.

### gsd
GSD의 **웨이브 병렬 + 의존성 그래프** (parallelization toggle)는 Anthropic의 스케일 규칙과 상보적. GSD는 의존성 기반으로 병렬 그룹을 자동 결정하고, Anthropic은 쿼리 복잡도 기반으로 수동 규칙을 임베딩한다. 두 접근의 하이브리드가 더 강건할 수 있음.

### compound-engineering
Compound Engineering의 **"thin orchestrator"** 패턴이 Anthropic lead agent 역할과 일치. 오케스트레이터는 최소 로직만 갖고, 무거운 작업은 전부 worker로 위임. Extended thinking + interleaved thinking은 Compound Engineering이 강조하는 "reasoning at the seam" 개념의 구체적 구현.

### ecc
ECC의 self-modifying / self-evaluating 루프와 Anthropic의 LLM-as-judge 단일 프롬프트 평가기 비교 가능. ECC는 평가를 에이전트 루프 내부에 두는 반면, Anthropic은 외부 판정자 구조.

### revfactory-harness
RevFactory의 14 parallel specialized review agents (P4) 패턴이 Anthropic CitationAgent의 역할 분리와 유사. 후처리를 전용 에이전트로 분리하는 설계 원칙 공유.

### openspec / gstack
직접적인 multi-agent 패턴 연결은 약함. 단, gstack의 spec-driven context engineering이 Anthropic의 "명시적 4요소 위임 명세"와 XML 프롬프트 구조화 원칙에서 교차.

## 후속 조사 / 빈틈

1. **비동기 실행 아키텍처**: 현재 동기식 한계를 극복하는 async subagent 설계 — Anthropic이 "future work"로 남긴 핵심 미결 과제
2. **CitationAgent 상세**: 인용 처리 전용 에이전트의 내부 구조·프롬프트 미공개
3. **BrowseComp 벤치마크 세부 사항**: 90.2% 개선 수치의 측정 방법, baseline 조건, 샘플 크기
4. **토큰 비용 분해**: ~15× 중 lead agent vs subagents vs CitationAgent 각 비중
5. **실패 모드 빈도 데이터**: 9가지 실패 모드 중 실제 발생 비율 미공개
6. **Rainbow deployment 구현 상세**: 에이전트 상태 직렬화/복원 방법론
7. **도구 설명 40% 개선 실험**: 어떤 도구, 어떤 변경이 효과를 냈는지 구체적 데이터 없음
8. **Opus 4 vs Sonnet 4 비용 트레이드오프**: lead에 Opus, subagents에 Sonnet을 쓰는 결정의 정량적 근거
