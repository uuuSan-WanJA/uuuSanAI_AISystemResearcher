---
title: "Code execution with MCP: Building more efficient agents"
date: 2026-04-17
source_url: https://www.anthropic.com/engineering/code-execution-with-mcp
source_type: blog
topic: techniques
tags: [anthropic, mcp, code-execution, efficiency, token-optimization, agent-architecture, tool-management]
status: processed
---

## 요약 (3줄 이내)

MCP 서버를 직접 tool call 방식이 아닌 코드 실행 API로 노출하면 에이전트의 토큰 소비를 극적으로 줄일 수 있다. 핵심 효율 논거는 두 가지—도구 정의 로딩 비용과 중간 결과의 컨텍스트 통과 비용—를 코드 실행 환경에서 흡수함으로써 해결한다는 것이다. Google Drive → Salesforce 예시에서 150,000 토큰 → 2,000 토큰(98.7% 절감)을 달성한 수치가 대표 근거로 제시된다.

## 핵심 포인트

- **도구 정의 과부하 문제**: MCP 서버가 수백 개의 tool을 노출하면, 에이전트는 요청을 처리하기 전에 "수십만 토큰"의 정의를 먼저 소비해야 한다.
- **중간 결과 중복 문제**: 순차 tool call 체인에서 각 결과가 모델 컨텍스트를 반복 통과하며 불필요한 토큰을 소비한다.
- **코드 실행으로 전환**: LLM이 코드 작성에 능하다는 강점을 활용해, 필터링·루프·조건 분기를 실행 환경에서 처리하고 최종 결과만 컨텍스트에 전달한다.
- **Privacy 부산물**: 중간 결과가 기본적으로 실행 환경에 머물러 PII의 모델 통과를 차단할 수 있다.
- **Skills 축적**: 작동하는 코드를 `./skills/` 디렉토리에 저장해 재사용 가능한 능력으로 전환한다.

## 저자의 프레임워크 / 명시적 주장

**"Code execution over many discrete tools"의 논리 구조:**

저자는 직접 tool call 방식에서 발생하는 두 가지 비효율을 먼저 정의하고, 코드 실행이 각각을 어떻게 해소하는지 대응시킨다.

| 문제 | 직접 tool call | 코드 실행 |
|------|--------------|----------|
| 도구 로딩 | 모든 정의를 사전 일괄 로딩 | Filesystem 탐색으로 필요 시점에 로딩 (progressive disclosure) |
| 데이터 필터링 | 원본 전체가 모델 컨텍스트 통과 | 실행 환경에서 필터 후 결과만 전달 |
| 제어 흐름 | 에이전트 루프를 n회 반복 | 코드 내 `for`/`while`/조건 분기로 처리 |
| 상태 관리 | 컨텍스트 의존 | 파일시스템(`./workspace/`) 영속 |

**Progressive Disclosure 원리**: "Models are great at navigating filesystems" — 에이전트가 `./servers/` 디렉토리를 탐색해 필요한 도구 정의만 동적으로 로드함으로써, 도구 정의 토큰 비용을 on-demand로 분산한다.

**효율 주장의 핵심 구조**: 토큰 절감은 단순한 최적화가 아니라 확장성의 문제다. 도구가 많아질수록 직접 tool call 방식의 사전 비용은 선형 이상으로 증가하지만, 코드 실행 방식에서는 실제 사용하는 도구의 정의 비용만 발생한다.

## 구체적 패턴·체크리스트·숫자

**핵심 수치:**
- Google Drive 스프레드시트(10,000행) → Salesforce 업로드 워크플로: **150,000 토큰 → 2,000 토큰 (98.7% 절감)**
- "Time to first token" latency 개선: 조건 분기를 코드로 처리해 모델 평가 대기 없이 진행

**패턴 카탈로그:**

1. **Filesystem-based tool discovery**: `./servers/google-drive/getDocument.ts` 구조로 도구를 파일로 정리, 에이전트가 `ls`/`read`로 필요한 것만 로드
2. **Context-efficient filtering**: 실행 환경에서 `allRows.filter(row => row["Status"] === 'pending')` 후 결과만 반환
3. **Native control flow**: `while (!found) { ... }` 루프로 MCP tool call + sleep 반복 없이 처리
4. **State persistence**: 중간 결과를 `./workspace/leads.csv`에 저장해 재개 가능한 워크플로 구현
5. **Skills accumulation**: 반복 가능한 코드를 `./skills/` 저장

**구현 비용(명시적 경고)**: "Code execution introduces its own complexity. Running agent-generated code requires a secure execution environment with appropriate sandboxing, resource limits, and monitoring."

## 인용 가치 있는 구절

> "MCP provides a universal protocol—developers implement MCP once in their agent and it unlocks an entire ecosystem of integrations"

> "The core insight is the same: LLMs are adept at writing code and developers should take advantage of this strength"

> "Code execution applies these established patterns to agents, letting them use familiar programming constructs"

> "Models are great at navigating filesystems" (progressive disclosure 원리의 근거)

> "Intermediate results stay in the execution environment by default" (privacy 부산물 설명)

## 이식 가능한 원시요소

- **P1. Progressive tool loading via filesystem** — 도구 정의를 파일시스템 계층으로 관리하고 에이전트가 on-demand로 읽는 패턴 — standalone-extractable: **yes**
- **P2. Context-efficient filtering (exec-side filter)** — 대용량 데이터를 실행 환경에서 필터 후 모델에 소결과만 전달 — standalone-extractable: **yes**
- **P3. Native control flow in code** — 에이전트 루프 반복 대신 코드 내 루프/조건으로 처리 — standalone-extractable: **yes**
- **P4. Workspace persistence pattern** — `./workspace/`에 중간 상태 저장, 재개 가능 워크플로 — standalone-extractable: **yes**
- **P5. Skills directory accumulation** — 작동 코드를 `./skills/`에 축적해 재사용 능력으로 전환 — standalone-extractable: **partial** (실행 환경과 결합)
- **P6. PII isolation via exec environment** — 중간 PII가 모델 컨텍스트를 통과하지 않도록 실행 환경에 격리 — standalone-extractable: **partial** (샌드박스 설계 필요)

## 기존 하네스 노트와의 연결

- **compound-engineering**: 코드 실행을 통한 multi-step 워크플로 효율화는 compound agent 아키텍처의 핵심 패턴과 직결. P3(native control flow)는 compound 에이전트가 각 단계를 별도 tool call로 분리하는 오버헤드를 제거하는 직접적 해법.
- **ouroboros**: Skills accumulation(P5)은 에이전트가 자신의 능력을 자기 참조적으로 확장하는 Ouroboros 패턴의 구체적 구현 예시.
- **gstack**: Filesystem-based tool discovery(P1)는 도구 레이어를 스택 구조로 관리하는 gstack 접근과 호환. 도구 정의를 디렉토리 계층으로 버전 관리하는 패턴 이식 가능.
- **ecc**: 98.7% 토큰 절감 수치는 ECC(Efficient Context Compression) 관련 노트의 efficiency baseline으로 인용 가능.
- **superpowers**: 코드 실행 환경이 에이전트에게 "superpower"로서 파일시스템 접근, 상태 영속, PII 격리를 부여한다는 프레임이 superpowers 하네스 노트와 연결.

## 후속 조사 / 빈틈

- **샌드박스 구현 비용의 정량화 부재**: 포스트는 샌드박스 필요성을 경고하지만 구현 비용(지연, 인프라 복잡도)에 대한 수치가 없다. 코드 실행 환경(e.g., E2B, Modal, Firecracker)별 latency 비교 필요.
- **Token 절감 수치의 일반화 한계**: 98.7% 절감은 10,000행 스프레드시트라는 특수 케이스. 일반 워크플로에서의 평균 절감률 데이터 없음.
- **Progressive disclosure의 실패 모드**: 에이전트가 잘못된 도구 파일을 로드하거나 필요한 도구를 탐색하지 못하는 경우의 fallback 전략 미제시.
- **Skills 디렉토리의 품질 관리**: 축적된 skills 코드의 obsolescence, 충돌, 버전 관리 전략 논의 없음.
- **MCP adoption 수치**: "thousands of community-built servers" 언급이지만 공식 생태계 규모 통계 부재. MCP 서버 레지스트리 현황 별도 조사 필요.
