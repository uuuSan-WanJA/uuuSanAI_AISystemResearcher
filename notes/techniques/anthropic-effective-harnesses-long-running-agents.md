---
title: Effective Harnesses for Long-Running Agents
date: 2026-04-17
source_url: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
source_type: blog
topic: harness
tags: [anthropic, harness, long-running, session-continuity, initializer-agent, coding-agent, feature-list, git-state, e2e-testing, incremental, shift-handoff]
status: processed
---

## 요약 (3줄 이내)

Anthropic Engineering 블로그가 long-running 에이전트의 핵심 문제를 "교대 근무 엔지니어가 전 교대 기억 없이 출근하는 것"으로 정의하고, Initializer Agent + Coding Agent 2-파트 분리 구조로 해결하는 패턴을 제시했다. 핵심 장치는 200+ 항목의 JSON 피처 리스트 + init.sh + claude-progress.txt 3종 영속 파일로, 에이전트가 세션마다 이 파일들을 읽어 컨텍스트를 재구성한다. 자기 선언 완료(premature victory declaration)와 검증 없는 마킹을 막기 위해 Puppeteer MCP 브라우저 자동화를 end-to-end 검증 게이트로 강제한 것이 성능 "극적 향상"의 핵심이다.

---

## 핵심 포인트

- **교대 엔지니어 메타포**: 에이전트의 세션 단절을 "전 교대 기억 없는 엔지니어"로 명명 — 해결책도 엔지니어링 현장에서 직접 차용
- **2-에이전트 분리**: Initializer Agent(최초 환경 구축)와 Coding Agent(반복 실행)를 역할별로 분리된 프롬프트로 운영
- **JSON 피처 리스트**: Markdown 대신 JSON을 선택한 이유 — "모델이 JSON 파일을 부적절하게 변경하거나 덮어쓸 가능성이 낮음"
- **200+ 피처 목록**: `category`, `description`, `steps`, `passes` 4필드 구조; `passes: false`가 기본값
- **원피처-원세션 원칙**: 한 번에 하나의 피처만 구현 — one-shotting 문제(컨텍스트 소진 전 전체 구현 시도)를 직접 차단
- **세션 시작 6단계 프로토콜**: pwd → git log + progress 파일 → 피처 리스트 선택 → init.sh 서버 기동 → E2E 기능 테스트 → 구현 착수
- **클린 스테이트 요구**: 세션 종료 시 "main 브랜치 머지 적합" 수준의 코드를 커밋 + progress 업데이트 — 프로덕션 준비 상태가 이터레이션 경계 조건
- **Puppeteer MCP 게이트**: 브라우저 자동화로 human-user 관점의 E2E 테스트 강제; "코드만 봐서는 불분명한 버그를 식별·수정"
- **테스트 제거 금지 규칙**: "테스트 제거·수정은 허용 불가 — 기능 누락 및 버그 발생 원인" — 하드 금지 규칙으로 프롬프트에 명시
- **git을 롤백 메커니즘으로**: 불량 변경 복구 및 작동 상태 복원 수단으로 git을 명시적 안전망으로 활용

---

## 저자의 프레임워크 / 명시적 주장

**핵심 설계 원리**: 에이전트는 상태를 기억하지 않는다 — 따라서 모든 상태는 파일시스템에 외재화되어야 한다. 이는 Ralph의 "파일시스템이 유일한 지속 기억"과 완전히 동일한 원리이나, Anthropic은 이를 구조화된 JSON 상태 파일로 더 정밀하게 구현한다.

**2-에이전트 아키텍처 정당화**:
- Initializer는 일회성 환경 구축 — 반복 불가한 작업(초기 커밋, init.sh 작성, 피처 리스트 생성)을 격리
- Coding Agent는 반복 가능한 단일 책임 루프 — "피처 1개 선택 → 구현 → 검증 → 커밋 → 진행 기록"

**4대 실패 모드와 그 해결책 (저자 명시적 매핑)**:

| 실패 모드 | Initializer 해결책 | Coding Agent 해결책 |
|---|---|---|
| 조기 완료 선언 | passes: false 기본값 피처 리스트 | 피처 리스트 읽기 + 1개씩 + 철저 검증 후 완료 마킹 |
| 미문서화된 환경 상태 | git 레포 + progress 노트 | git log 검토 → 베이스라인 서버 테스트 → 커밋 + 업데이트 |
| 검증 없는 완료 마킹 | 피처 리스트 구조 자체 | E2E 테스트 자기검증 후 상태 변경 |
| 앱 실행법 재학습 낭비 | init.sh 스크립트 작성 | 세션 시작 시 init.sh 읽기 |

**성능 주장**: Puppeteer MCP 도입으로 "성능이 극적으로 향상(dramatically improved)"

---

## 구체적 패턴·체크리스트·숫자

**숫자**:
- 피처 목록 규모: 200+ 항목
- 브라우저 자동화 제한: 네이티브 브라우저 alert 모달 같은 일부 UI 요소 미감지 — 버그 식별 능력 제한

**JSON 피처 항목 구조**:
```json
{
  "category": "functional",
  "description": "[피처 설명]",
  "steps": "[검증 단계 배열]",
  "passes": false
}
```

**세션 시작 체크리스트 (6단계)**:
1. `pwd` — 작업 디렉토리 확인
2. git log + progress 파일 읽기 — 최근 컨텍스트 재구성
3. 피처 리스트 읽기 → 우선순위 최상위 미완 피처 선택
4. init.sh로 개발 서버 기동
5. 기본 E2E 기능 테스트 실행
6. 피처 구현 착수

**Initializer가 생성하는 3종 영속 아티팩트**:
1. `init.sh` — 개발 서버 기동 스크립트
2. `claude-progress.txt` — 세션 간 활동 로그
3. 피처 리스트 JSON — 200+ 요구사항 + 완료 상태

**금지 규칙**: "테스트 제거·편집 불가 — 기능 누락/버그 원인"

---

## 인용 가치 있는 구절

> "Engineers working in shifts, where each new engineer arrives with no memory of what happened on the previous shift."

> "The model is less likely to inappropriately change or overwrite JSON files."

> "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."

> "Dramatically improved performance, as the agent was able to identify and fix bugs that weren't obvious from the code alone."

> "The kind of code that would be appropriate for merging to a main branch."

---

## 이식 가능한 원시요소

- **P1. Shift-Handoff State Trio** — `init.sh` + `progress.txt` + `feature-list.json` 3종 세트로 에이전트 세션 간 컨텍스트를 완전 외재화하는 패턴 — standalone-extractable: **yes**

- **P2. Initializer/Coding 역할 분리** — 일회성 환경 구축 에이전트와 반복 실행 에이전트를 별도 프롬프트로 분리하는 2-tier 구조 — standalone-extractable: **yes**

- **P3. JSON 피처 리스트 (passes: false 기본값)** — 조기 완료 선언 방지 장치: 모든 피처가 기본적으로 미완료이며 E2E 검증 후에만 `passes: true`로 전환 — standalone-extractable: **yes**

- **P4. 원피처-원세션 제약** — 컨텍스트 소진을 막는 점진적 구현 원칙; 세션 경계를 피처 경계와 일치시킴 — standalone-extractable: **yes**

- **P5. 세션 시작 6단계 온보딩 프로토콜** — 새 에이전트가 기존 컨텍스트를 복원하는 표준 시퀀스 (pwd → git log → 피처 선택 → 서버 기동 → E2E → 구현) — standalone-extractable: **yes**

- **P6. Puppeteer MCP E2E 검증 게이트** — 코드 리뷰 대신 실제 사용자 관점 브라우저 자동화로 완료 검증; 코드만으로는 불분명한 버그 포착 — standalone-extractable: **partial** (Puppeteer MCP 의존성)

- **P7. git-as-rollback** — git을 버전 관리가 아닌 불량 변경 복구 및 안전망으로 명시적 활용 — standalone-extractable: **yes**

- **P8. 테스트 삭제 하드 금지 규칙** — 에이전트가 실패 테스트를 제거해 통과시키는 패턴을 프롬프트 레벨 명시적 금지로 차단 — standalone-extractable: **yes**

---

## 기존 하네스 노트와의 연결

**ralph-wiggum** — 가장 직접적 대응. Ralph의 "파일시스템이 유일한 지속 기억" + while-true bash 루프가 이 포스트의 세션 간 상태 외재화 + Coding Agent 반복 루프와 구조적으로 동일. 차이: Ralph는 단일 루프 + PROMPT.md, Anthropic 패턴은 2-에이전트 분리 + JSON 상태 파일 3종. Anthropic 버전이 Ralph의 프로덕션 강화판으로 읽힌다.

**ouroboros** — Ouroboros의 ambiguity ≤ 0.2 / similarity ≥ 0.95 숫자 게이트와 이 포스트의 `passes: false` 기본값 게이트는 동일 문제(조기 완료 선언 방지)를 다른 메커니즘으로 해결. Ouroboros는 정량적 임계값, Anthropic은 불리언 상태 + E2E 검증 요구.

**superpowers** — Superpowers의 `<HARD-GATE>` XML 태그 + TDD 강제가 이 포스트의 "테스트 제거 불가" 하드 금지 규칙과 같은 계열. 검증 없는 완료 마킹 방지를 하드 규칙으로 프롬프트에 명시하는 공통 패턴.

**gsd** — GSD의 Wave 단위 컨텍스트 격리(context-engineering)가 이 포스트의 원피처-원세션 제약과 동일 목적(one-shotting 방지). GSD는 Wave 파일명 프로토콜로, Anthropic은 JSON 피처 목록 + 1개 선택으로 구현.

**compound-engineering** — Compound Engineering의 progress 기록 + 다음 이터레이션 자동 회피(docs/solutions/ + CLAUDE.md)가 이 포스트의 `claude-progress.txt` 세션 간 활동 로그와 기능적으로 동일. 차이: Compound Engineering은 학습 누적(복리), Anthropic 패턴은 단순 핸드오프 로그.

---

## 후속 조사 / 빈틈

- **멀티 에이전트 확장 미해결**: 저자가 "테스트 전담 QA 에이전트, 코드 정리 에이전트" 가능성을 언급하지만 구체적 구현은 open question으로 남김 — 3+ 에이전트 아키텍처로 확장 시 세션 간 상태 동기화 방법 불명확
- **피처 리스트 200+ 생성 방법론 미공개**: Initializer Agent가 200+ 항목을 어떻게 생성하는지(단일 프롬프트? 반복 정제?) 설명 없음
- **전체 스택 웹 개발 외 일반화 검증 없음**: 과학 연구, 금융 모델링 적용 가능성을 언급하나 사례 없음
- **init.sh 내용 미공개**: 실제 init.sh 스크립트 내용이나 생성 방법 제시 없음
- **Puppeteer MCP 설정 세부사항 없음**: 어떤 MCP 서버 사용인지, 설정 방법, 비용 구조 언급 없음
- **세션 길이 최적화**: 원피처-원세션 규칙이 단일 피처가 컨텍스트 창을 초과하는 경우 대처 방법 미언급
- **진행 파일 포맷 미명시**: claude-progress.txt의 구체적 구조(자유 텍스트 vs 구조화 템플릿) 미공개
