---
title: Scaling Managed Agents: Decoupling the Brain from the Hands
date: 2026-04-17
source_url: https://www.anthropic.com/engineering/managed-agents
source_type: blog
topic: agents
tags: [anthropic, managed-agents, architecture, brain-hands-separation, session-log, security, context-management, stateless-harness, sandbox, scaling]
status: processed
---

## 요약 (3줄 이내)

Anthropic의 Managed Agents 서비스는 에이전트 하네스에서 **Brain(Claude + Harness)**, **Hands(Sandbox + 툴)**, **Session(이벤트 로그)** 세 컴포넌트를 완전히 분리함으로써, 모델 역량이 향상될 때마다 발생하던 기술 부채를 구조적으로 제거했다. 이 분리는 보안 경계 재설계, P95 TTFT 90% 이상 감소, 무상태 하네스의 수평 확장이라는 세 가지 실질적 이득을 동시에 달성했다. 핵심 철학은 운영체제의 가상화 전략 — 인터페이스는 고정하되 구현은 언제든 교체 — 을 에이전트 인프라에 적용한 것이다.

---

## 핵심 포인트

- **단일 컨테이너 설계의 함정**: 초기 아키텍처는 세션·하네스·샌드박스를 하나의 컨테이너에 결합했다. 컨테이너 충돌 = 세션 전체 손실. 네트워크 문제·하네스 크래시·컨테이너 크래시가 WebSocket 이벤트 스트림에서 구분 불가능해 디버깅을 위해 컨테이너 내부에 접근해야 했고, 이는 사용자 데이터 노출 위험을 수반했다.
- **Brain은 무상태(stateless)로 외부화**: Harness가 컨테이너 밖에서 작동하며, 크래시 후 `wake(sessionId)` + `getSession(id)` 호출만으로 마지막 내구성 이벤트부터 재개한다. Brain은 세션 로그를 쿼리해 컨텍스트를 재구성하므로 컨테이너 수명에 묶이지 않는다.
- **Hands는 단일 인터페이스로 추상화**: `execute(name, input) → string`. 컨테이너·폰·MCP 서버·커스텀 인프라 관계없이 동일 인터페이스. Brain은 어떤 Hands에 어떤 작업을 줄지 추론하며, Brain이 Hands를 다른 Brain에 위임하는 것도 가능하다.
- **Session은 외부화된 불변 이벤트 로그**: Claude 컨텍스트 창 바깥에 존재하는 내구성 append-only 레코드. `getEvents()`는 위치 슬라이스, 특정 시점 이전 되감기, 시퀀스 재읽기 등 유연한 쿼리를 지원한다.
- **보안 경계 근본 재설계**: 결합 아키텍처에서는 프롬프트 인젝션 하나면 Claude가 환경 변수를 읽어 크리덴셜을 탈취할 수 있었다. 분리 후 두 패턴으로 크리덴셜이 샌드박스에 절대 도달하지 않도록 강제한다.
- **TTFT 극적 개선**: Brain이 오케스트레이션 레이어에서 세션 로그를 즉시 쿼리해 추론을 시작하므로, 컨테이너 프로비저닝 완료를 기다릴 필요가 없다. 컨테이너는 실제로 툴 콜이 발생할 때만 프로비저닝된다.

---

## 저자의 프레임워크 / 명시적 주장

### "Brain vs. Hands" 분리의 구조적 의미

저자들은 이 아키텍처를 **meta-harness** 라고 명명한다. Managed Agents 자체는 특정 하네스에 대해 무관심(unopinionated)하지만, 범용 인터페이스에 대해서는 강한 의견을 가진다. 이는 운영체제의 가상화 전략과 동형이다 — `read()` 시스템 콜은 1970년대 디스크팩이든 현대 SSD든 변하지 않는다.

**핵심 통찰**: 기존 하네스들은 "Claude가 혼자서 X를 할 수 없다"는 가정을 코드에 박아 넣었다. 모델이 향상되면 그 가정이 죽은 코드(dead code)가 된다. Claude Sonnet 4.5에서 추가한 컨텍스트 리셋 로직이 Claude Opus 4.5에서 불필요해진 것이 실제 사례. 해법은 **가정을 인터페이스로 대체** — 구현은 언제든 교체 가능하되 인터페이스는 안정적으로 유지.

### "Pets vs. Cattle" 문제 인식

단일 컨테이너 = 인프라를 "pet"처럼 다루는 것. 컨테이너 하나가 죽으면 수동 개입이 필요해진다. 분리 아키텍처는 컨테이너를 "cattle"로 — 언제든 교체 가능한 대체 가능 인프라로 — 취급하게 해준다.

### 스케일링의 두 축

1. **Many Brains**: 무상태 하네스는 컨테이너 인프라와 결합 없이 수평 확장. 고객 VPC 내부에서 네트워크 피어링 없이 Brain 실행 가능.
2. **Many Hands**: 각 실행 환경이 동일 인터페이스 의미론을 가진 툴이 된다. Brain이 어떤 Hands에 어떤 작업을 할당할지 추론하며, Hands를 다른 Brain에 위임하는 것도 가능.

---

## 구체적 패턴·체크리스트·숫자

### 보안 패턴 (2가지)

**패턴 1 — Bundled Authentication**
- 액세스 토큰을 샌드박스 초기화 시점에 주입 (예: Git 토큰을 로컬 리모트에 클론)
- 이후 작업은 토큰 없이 수행 → Claude에 토큰이 노출되지 않음

**패턴 2 — Vault + Proxy Pattern**
- OAuth 토큰을 샌드박스 외부의 보안 Vault에 저장
- Claude는 전용 프록시를 통해 MCP 툴 호출 → 프록시가 서버사이드에서 크리덴셜 페치
- 에이전트가 시크릿에 절대 접근 불가

### 핵심 인터페이스 (API 시그니처)

| 인터페이스 | 설명 |
|---|---|
| `execute(name, input) → string` | Hands의 단일 추상화 인터페이스 |
| `wake(sessionId)` | 크래시 후 하네스 복구 진입점 |
| `getSession(id)` | 마지막 내구성 이벤트 기반 세션 재구성 |
| `emitEvent(id, event)` | Session 로그에 이벤트 기록 |
| `provision({resources})` | 표준 레시피 기반 샌드박스 프로비저닝 |
| `getEvents()` | 위치 슬라이스 / 되감기 / 재읽기 지원 쿼리 |

### 성능 수치

- **P50 TTFT**: 약 60% 감소
- **P95 TTFT**: 90% 이상 감소
- **원인**: Brain이 세션 로그를 즉시 쿼리해 추론 시작 — 컨테이너 프로비저닝 완료 불필요

### 용어 정리

| 용어 | 정의 |
|---|---|
| Harness | Claude를 호출하고 툴 콜을 라우팅하는 제어 루프 |
| Meta-harness | Managed Agents 자체 — 특정 하네스에 무관심, 범용 인터페이스에 의견 보유 |
| Brain | Claude + 해당 하네스 |
| Hands | 샌드박스 및 툴 실행 환경 |
| Session | 에이전트 이벤트 전체의 내구성 append-only 로그 |
| Sandbox | Claude가 코드를 실행하고 파일을 편집하는 실행 환경 |

---

## 인용 가치 있는 구절

> "Traditional agent harnesses encode assumptions about what Claude cannot do alone. These assumptions become obsolete as models improve, creating technical debt."

> "The architecture virtualizes agent components into durable interfaces that can be replaced independently."

> "Just as the `read()` command remains unchanged whether accessing 1970s disk packs or modern SSDs, Managed Agents maintain stable interfaces while swapping implementations."

> "Brains can even delegate hands to other brains since no hand is tied to any specific brain."

> "We are opinionated about interfaces, not implementations."

---

## 이식 가능한 원시요소

- **P1. Brain/Hands/Session 3-레이어 분리 패턴** — 단일 컨테이너를 Brain(무상태)·Hands(교체 가능)·Session(외부화 로그)으로 분해하는 아키텍처 템플릿 — standalone-extractable: **yes**

- **P2. `execute(name, input) → string` 단일 Hands 인터페이스** — 샌드박스·MCP 서버·커스텀 툴을 동일 인터페이스로 추상화하는 어댑터 패턴 — standalone-extractable: **yes**

- **P3. Vault + Proxy 크리덴셜 격리 패턴** — OAuth 토큰을 에이전트 실행 컨텍스트 밖 Vault에 보관하고, 전용 프록시가 서버사이드에서만 크리덴셜을 처리하는 보안 패턴 — standalone-extractable: **yes**

- **P4. `getEvents()` 기반 유연 컨텍스트 재구성** — 세션 로그를 외부화해 irreversible compaction 없이 위치 슬라이스·되감기·재읽기로 컨텍스트를 동적으로 구성하는 패턴 — standalone-extractable: **yes**

- **P5. `wake(sessionId)` 크래시 복구 패턴** — 무상태 하네스가 마지막 내구성 이벤트부터 재개하는 복구 진입점 — standalone-extractable: **yes**

- **P6. "인터페이스는 고정, 구현은 교체" 설계 철학 (meta-harness 원칙)** — 모델 역량이 향상돼도 하네스가 기술 부채를 쌓지 않도록 가정을 인터페이스로 대체하는 설계 원칙 — standalone-extractable: **partial** (철학적 원칙이므로 도메인 맥락 필요)

---

## 기존 하네스 노트와의 연결

**ouroboros** — EventStore 기반 상태 외부화와 직접 대응. Ouroboros는 MCP 서버 + EventStore로 상태를 분리하고, Brain/Hands/Session 분리는 그 원리의 인프라 레벨 일반화. `wake(sessionId)` 복구 패턴은 Ouroboros의 `ooo ralph` 영속 루프 개념과 동형이다.

**gsd** — GSD의 체크포인트·재개 메커니즘은 Session 이벤트 로그의 `getEvents()` 쿼리 패턴과 목적이 같다. 다만 GSD는 파일 기반, Managed Agents는 외부화된 로그 서비스로 구현 매체가 다르다.

**compound-engineering** — Compound Engineering의 `docs/solutions/` 누적 루프는 Session 로그의 "모든 이벤트를 잃지 않는다"는 철학과 공명한다. 단, Compound는 지식 누적이 목적이고 Session은 내구성·복구가 목적.

**ralph-wiggum** — Ralph의 "boulder never stops" 영속 루프는 `wake(sessionId)` 복구 패턴의 사용자 경험 레벨 표현. Ralph가 하네스 사용자에게 중단 없는 진행을 제공하듯, Brain 크래시 후 재개가 사용자에게 투명하게 이뤄진다.

**superpowers** — Superpowers의 에이전트 역할 분화(여러 특화 에이전트)는 "Many Brains / Many Hands" 스케일링 축과 직접 연결. Brain이 Hands를 다른 Brain에 위임하는 패턴은 Superpowers의 서브에이전트 위임 체계와 구조적으로 동형이다.

**ecc** — ECC의 `/learn`→`/evolve` 사이클이 모델 개선에 따라 하네스 로직을 진화시키는 것처럼, Managed Agents는 "모델 가정을 인터페이스로 대체"해 모델 개선이 하네스 기술 부채를 만들지 않도록 한다. 목표는 같고 접근 레벨이 다르다.

---

## 후속 조사 / 빈틈

1. **`getEvents()` 쿼리 전략의 구체적 구현** — 위치 슬라이스·되감기·재읽기가 실제 프로덕션에서 어떤 휴리스틱으로 선택되는지 공개된 정보가 없다. 캐시 히트율 최적화를 위한 이벤트 슬라이싱 알고리즘이 존재하는가?

2. **Many Brains의 VPC 배포 상세** — Brain이 고객 VPC에서 네트워크 피어링 없이 실행된다고 언급되었으나, 인증·신뢰 경계 설계가 공개되지 않았다.

3. **Vault + Proxy 패턴의 MCP 통합 상세** — 전용 프록시가 MCP 서버로 구현되는지, 별도 사이드카 서비스인지 불명확. MCP 인증 확장(2025 MCP Auth spec)과의 관계가 궁금하다.

4. **"meta-harness" 개념의 외부 채택 가능성** — Anthropic이 Managed Agents API를 외부에 공개할 계획이 있는지, 또는 이것이 순수 내부 인프라인지 명확하지 않다.

5. **컨텍스트 압축(compaction) 완전 회피 주장 검증** — 충분히 긴 세션에서 `getEvents()`만으로 모든 컨텍스트를 커버할 수 있는지, 또는 여전히 어느 시점에서 압축이 필요한지 실증 데이터가 없다.
