---
title: Vault+Proxy 크리덴셜 격리 primitive
date: 2026-04-17
based_on:
  - notes/techniques/anthropic-managed-agents.md
  - notes/techniques/anthropic-code-execution-with-mcp.md
  - notes/harness/compound-engineering.md
  - notes/harness/ralph-wiggum.md
  - digests/2026-04-17-anthropic-sweep-vs-community-harnesses.md
confidence: high
tags: [security, credential-isolation, brain-hands-separation, primitive]
---

## 한 줄 요약

Brain(하네스)과 Hands(샌드박스)를 물리적으로 분리하고, OAuth 토큰과 API 키를 샌드박스 외부 Vault에 두어 프롬프트 인젝션이 성공해도 크리덴셜이 에이전트에 절대 노출되지 않도록 강제하는 보안 아키텍처 패턴.

---

## 패턴 / 주장

### 위협 모델: 왜 Brain에 크리덴셜을 두면 위험한가

Anthropic `managed-agents` 포스트는 결합 아키텍처(Brain + Hands + 크리덴셜이 단일 컨테이너 내 공존)의 구조적 취약점을 명시적으로 적시한다.

> "결합 아키텍처에서는 프롬프트 인젝션 하나면 Claude가 환경 변수를 읽어 크리덴셜을 탈취할 수 있었다."

이 공격 경로는 복잡하지 않다. Claude는 파일시스템 탐색, `env` 읽기, 셸 명령 실행 능력을 기본으로 갖는다. 에이전트가 외부 콘텐츠(웹페이지, 사용자 메시지, 파일 내용)를 처리하다 프롬프트 인젝션 공격을 받으면, 그 공격 코드가 "환경 변수를 읽어 외부로 전송하라"는 지시를 덮어쓸 수 있다. 크리덴셜과 실행 환경이 같은 프로세스 공간에 있는 한 이 위험은 구조적으로 제거 불가능하다.

`anthropic-code-execution-with-mcp` 포스트도 별도의 각도에서 같은 위험을 지적한다. 코드 실행 환경은 "중간 결과가 기본으로 실행 환경에 머문다"는 PII 격리 부산물을 이야기하지만, 동시에 "보안 실행 환경, 적절한 샌드박싱, 리소스 제한, 모니터링이 필요하다"는 구현 경고를 명시적으로 발령한다. 샌드박스 설계 없이 코드 실행을 열어두면 인젝션 경로가 코드 실행 권한까지 포함하게 된다.

### Vault+Proxy 패턴 구조

Anthropic이 제시한 두 번째 패턴이다 (`managed-agents`의 보안 패턴 §2).

**구조**:
- OAuth 토큰, API 키 등 크리덴셜을 샌드박스 **외부**의 보안 Vault에 저장
- Claude는 전용 Proxy를 통해 MCP 툴 호출을 수행
- Proxy가 서버사이드에서 Vault로부터 크리덴셜을 페치해 외부 서비스에 인증
- Claude(Brain)는 Proxy URL과 툴 시그니처만 알뿐, 실제 시크릿에 접근 불가

흐름을 요약하면:

```
[Brain: Claude + Harness]
    ↓ execute("github_push", {...})        ← 크리덴셜 없음
[Proxy Layer]
    ↓ Vault에서 GitHub 토큰 페치           ← 서버사이드만 접근
[External Service: GitHub API]
```

Brain이 받는 것은 `execute(name, input) → string` 형식의 결과뿐이다. 이 인터페이스 계약이 Brain과 Hands 사이의 유일한 경계면이며, 여기에 크리덴셜은 등장하지 않는다.

### Bundled Authentication 변형과의 차이

Anthropic `managed-agents`는 더 단순한 첫 번째 패턴도 제시한다: **Bundled Authentication**. 샌드박스 초기화 시점에 단 한 번 액세스 토큰을 주입(예: Git 토큰을 로컬 리모트에 클론)하고, 이후 작업은 토큰 없이 수행한다. Claude에는 토큰이 노출되지 않는다.

두 패턴의 차이:

| 항목 | Bundled Authentication | Vault+Proxy |
|---|---|---|
| 크리덴셜 주입 시점 | 샌드박스 초기화 1회 | 매 툴 콜마다 런타임 페치 |
| 토큰 수명 | 세션 시작 시 소진 | 세션 전체에 걸쳐 중앙 관리 |
| 적합한 케이스 | 단순 단일 리소스 접근 | 다중 서비스, 장기 세션, 권한 위임 |
| 구현 복잡도 | 낮음 (시간 단위) | 높음 (주 단위) |

Bundled Auth는 "샌드박스가 시작되면 토큰은 이미 소모된다"는 논리로 노출 창(window)을 제로에 가깝게 줄이는 반면, Vault+Proxy는 토큰을 아예 실행 컨텍스트 바깥에 영구히 격리한다.

---

## 근거가 되는 관찰

- **Anthropic 명시 위협 모델**: "프롬프트 인젝션 한 번이면 환경 변수를 읽어 크리덴셜 탈취 가능" — `anthropic-managed-agents` 핵심 포인트 §보안 경계 근본 재설계
- **커뮤니티 9/9 전면 미구현(C2 gap)**: `2026-04-17-anthropic-sweep-vs-community-harnesses` 다이제스트 §C2는 Ralph, Superpowers, gstack, GSD, revfactory, OpenSpec, ECC, Compound, Ouroboros 모두 Vault+Proxy에 상응하는 크리덴셜 격리 레이어가 없음을 확인
- **`--dangerously-skip-permissions`가 취약점을 증폭**: Ralph(`ralph-wiggum` §6)와 Compound Engineering(`compound-engineering` §6)은 속도를 위해 이 플래그를 권장하는데, 이는 모든 Claude Code 툴을 열어두는 것으로 크리덴셜과 실행 권한이 동시에 노출된다
- **Ralph의 크리덴셜 처리 방식 미명시**: `ralph-wiggum` 전체 소스에서 크리덴셜 격리에 관한 명시적 언급이 없다. 파일시스템을 유일한 지속 기억으로 사용하므로, 크리덴셜이 필요한 작업은 환경 변수 또는 설정 파일에 의존할 것으로 추정되나 구체적 처리 전략은 **미명시**
- **샌드박스 경고의 구체성 부재**: `anthropic-code-execution-with-mcp`는 보안 실행 환경 필요성을 경고하지만 구현 방법, 비용, 크리덴셜 격리 전략에 대한 수치나 구체적 레시피를 제공하지 않는다

---

## 구성 요소 (이식 가능한 단위)

### 1. Vault 컴포넌트 — 크리덴셜 저장 위치, 접근 API

크리덴셜은 에이전트 실행 프로세스 공간 외부에 존재하는 저장소에 보관된다. `anthropic-managed-agents`는 "보안 Vault"라고만 명시하며 구체 구현체를 특정하지 않는다(HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager 등이 후보). Vault 접근은 Proxy만 가능하도록 네트워크/IAM 정책으로 제한한다. Brain은 Vault의 존재를 알 필요도 없다.

### 2. Proxy 컴포넌트 — 샌드박스 도구 콜을 가로채 인증 주입

Brain이 `execute("github_push", input)`을 호출하면 Proxy가 이를 인터셉트한다. Proxy는 Vault로부터 해당 서비스의 크리덴셜을 런타임에 페치해 외부 API 호출을 수행하고, 결과만 Brain에 반환한다. `anthropic-managed-agents`는 이 Proxy가 MCP 서버로 구현되는지 사이드카 서비스인지를 명시하지 않는다(**미명시**). MCP 인증 확장(2025 MCP Auth spec)과의 관계 또한 불명확하다.

### 3. Bundled Authentication 변형 — 언제 이 단순 방식이 충분한가

단일 서비스, 단기 세션, 로컬 개발 환경에서는 Bundled Auth가 충분할 수 있다. 초기화 시점에 토큰을 소비(예: `git clone --depth 1 https://token@repo.git`)하고 이후 작업이 토큰 없이 진행되면, 프롬프트 인젝션이 성공해도 읽을 크리덴셜이 컨텍스트에 없다. 다중 서비스 접근, 토큰 갱신 필요, 사용자별 권한 위임이 요구되면 Vault+Proxy로 업그레이드해야 한다.

### 4. Brain/Hands 인터페이스 계약 — `execute(name, input) → string` 고정 시그니처

`anthropic-managed-agents`의 핵심 설계 원칙 중 하나는 Hands의 단일 추상화 인터페이스다. 컨테이너든, 폰이든, MCP 서버든, 커스텀 인프라든 동일 시그니처를 노출한다. 이 고정 인터페이스가 크리덴셜 격리의 물리적 경계가 된다. Brain은 이 인터페이스 너머를 볼 수 없으며, Proxy가 그 너머에 위치한다.

---

## 반례 또는 한계

- **단일 사용자 로컬 개발에서 과도 엔지니어링**: Vault 서비스를 따로 운영하고 Proxy 레이어를 유지하는 비용이 로컬 개발의 공격 표면 위험보다 크다. Compound Engineering(`compound-engineering` §6)이 `--dangerously-skip-permissions`를 명시적으로 권장하는 조건("프로세스 신뢰, 안전한 샌드박스, 속도 우선")이 바로 이 케이스다
- **Proxy 레이어가 새로운 단일 실패 지점**: Proxy가 다운되면 모든 외부 서비스 접근이 차단된다. 고가용성 설계가 추가로 필요해진다
- **MCP 생태계의 기존 크리덴셜 전달 관행과 충돌**: 많은 MCP 서버가 환경 변수로 크리덴셜을 받는 관행을 채택하고 있다. Vault+Proxy를 도입하면 이 서버들을 래핑하거나 수정해야 한다
- **Vault+Proxy 구현 상세 비공개**: `anthropic-managed-agents` §후속 조사에서 저자들 스스로 "전용 프록시가 MCP 서버로 구현되는지, 별도 사이드카 서비스인지 불명확"하다고 인정한다. 외부 구현자는 이 결정을 직접 내려야 한다

---

## 전제 / 선행 조건

- 샌드박스 또는 컨테이너 실행 환경: Brain과 Hands가 물리적으로 분리된 프로세스 또는 네트워크 경계를 가져야 한다
- 도구 콜 가로채기 가능한 아키텍처: `execute(name, input) → string` 인터페이스 또는 MCP 프로토콜처럼 호출이 중간 레이어를 통과하는 구조가 필요하다
- 신원 체계: 다중 사용자 환경에서 사용자 ↔ 에이전트 세션 매핑이 있어야 올바른 크리덴셜 범위를 Vault에서 로드할 수 있다

---

## 적용 난이도

- **최소 구현 (Bundled Auth만)**: 시간 단위. 기존 하네스 초기화 코드에서 토큰을 먼저 소비하는 방식으로 리팩터링
- **Vault+Proxy 완전 구현**: 주 단위. Vault 서비스 선택, Proxy 서비스 구현(또는 기존 MCP 서버 래핑), Brain이 Proxy를 유일한 외부 접점으로 사용하도록 인터페이스 고정

---

## 내 프로젝트에 적용한다면 (Phase 2 후보)

- **로컬 개발 vs 원격 에이전트 실행 구분 기준**: 로컬 단일 사용자 + 신뢰할 수 있는 코드베이스 → Bundled Auth만으로 충분. 원격 실행, 다중 사용자, 외부 콘텐츠를 처리하는 에이전트 → Vault+Proxy 필수
- **최소 Proxy로 API 키 숨김부터 시작**: 모든 외부 API 호출을 단일 Python/Node 사이드카 서비스로 래핑하고, 크리덴셜은 환경 변수에서 사이드카로만 읽도록 제한. Brain은 이 사이드카의 HTTP 엔드포인트만 호출
- **`--dangerously-skip-permissions` 사용 조건 재정의**: Compound Engineering과 Ralph가 이 플래그를 권장하는 조건("안전한 샌드박스")을 실제로 충족하는지 먼저 점검. 충족되지 않는다면 Vault+Proxy 없이 이 플래그를 사용하는 것은 C2 gap을 그대로 안고 가는 것
- **단계적 도입 경로**: (1) 모든 크리덴셜 참조를 감사해 환경 변수 의존 목록 작성 → (2) Bundled Auth로 즉시 노출 창 제거 → (3) 원격 에이전트 필요 시 Proxy 레이어 추가

---

## 관련 primitive 카드

- `primitive-brain-hands-session-separation` (미작성) — Brain/Hands/Session 3-레이어 분리 전체 아키텍처. Vault+Proxy는 이 분리의 보안 레이어
- `primitive-execute-interface-contract` (미작성) — `execute(name, input) → string` 고정 인터페이스. 크리덴셜 격리의 물리적 경계가 되는 인터페이스 설계
- `primitive-bundled-authentication` (미작성) — Vault+Proxy의 경량 변형. 로컬 개발용 최소 크리덴셜 보호
