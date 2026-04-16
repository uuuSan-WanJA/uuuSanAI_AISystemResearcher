---
title: Building a C compiler with a team of parallel Claudes
date: 2026-04-17
source_url: https://www.anthropic.com/engineering/building-c-compiler
source_type: blog
topic: agents
tags: [anthropic, multi-agent, parallel, case-study, compiler, claude-opus, docker, git-coordination, no-orchestrator, infinite-loop-harness]
status: processed
---

## 요약 (3줄 이내)

16개의 Claude Opus 4.6 에이전트가 약 2주간 병렬로 동작하며 Rust로 C 컴파일러를 구축한 실전 케이스 스터디. 중앙 오케스트레이터 없이 각 에이전트가 파일 락 + git을 통신 레이어로 삼아 자율적으로 태스크를 선택·완료한다. 비용 $20,000, 200억 입력 토큰, GCC torture test suite 99% 통과라는 구체적 수치가 검증 가능한 성과로 제시된다.

---

## 핵심 포인트

1. **오케스트레이터 없는 병렬 팀**: 중앙 디스패처 없이 에이전트 각자가 `current_tasks/` 디렉토리의 텍스트 락 파일로 작업을 예약·해제하며 중복 작업을 방지한다.
2. **역할 전문화**: 코어 컴파일러 개발, QA, 성능 최적화, 코드 효율화, 문서 관리, 중복 제거 등 6~7가지 역할로 분리된 에이전트가 각자 도메인에 집중한다.
3. **하네스 설계가 80%**: 프롬프트보다 테스트 파이프라인·락 메커니즘·컨텍스트 오염 차단 설계에 훨씬 많은 노력이 투입됐다.
4. **모델 능력 임계점 관찰**: Opus 4.0 → 4.5 → 4.6 순으로 실제 컴파일 가능 프로젝트의 규모가 급격히 확대되었으며, 4.6에서 Linux 커널 컴파일에 성공했다.
5. **자율 진행 유효성 확인**: 에이전트는 인간 개입 없이 다음 우선순위를 스스로 판단하고, 공유 진행 문서를 유지하며 지속적으로 진행한다.

---

## 시스템 아키텍처

| 항목 | 내용 |
|---|---|
| 병렬 에이전트 수 | **16개** (Claude Opus 4.6) |
| 실행 환경 | 개별 Docker 컨테이너, 공유 git upstream 레포에 마운트 |
| 태스크 조율 방식 | `current_tasks/` 폴더의 텍스트 파일 락 — 에이전트가 락 취득 → 작업 → 락 해제 |
| 통신 패턴 | git pull/merge/push; 공유 진행 문서(PROGRESS.md류) |
| 오케스트레이션 레이어 | **없음** — 각 에이전트가 "다음으로 명백한 문제"를 자율 선택 |
| 에이전트 생명주기 | `while true; do claude ...; done` 무한루프 — 컨테이너 완료 후 즉시 재생성 |
| 감독 구조 | 인간 감독자는 존재하지 않음; 테스트 suite가 사실상 심판자 역할 |

**역할 분할 (6~7종):**
- Core compiler developers (parser, codegen, optimization)
- Quality assurance agent
- Performance specialist
- Code efficiency agent
- Documentation maintainer
- Deduplication agent

**핵심 하네스 루프 (pseudo-code):**
```bash
while true; do
    claude --dangerously-skip-permissions \
           -p "$(cat AGENT_PROMPT.md)" \
           --model claude-opus-X-Y
done
```

---

## 저자의 프레임워크 / 명시적 주장

- **"Write extremely high-quality tests"**: 테스트 품질이 에이전트 방향을 결정한다. 부실한 테스트 = 에이전트가 잘못된 문제를 해결.
- **환경 설계 80%**: 하네스·테스트 설계가 프롬프트 작성보다 압도적으로 중요하다.
- **자율 태스크 선택 유효**: "다음으로 명백한 문제" 지시만으로 에이전트가 실질적 진전을 만들어냄.
- **컨텍스트 오염 방지 패턴**: 테스트 출력은 바이트 단위로 제한, 상세 로그는 별도 파일에 저장.
- **`--fast` 샘플링 옵션**: 전체 테스트의 1~10%만 무작위 샘플링해 에이전트가 시간 맹목성(time blindness) 속에서 빠른 피드백을 받도록 설계.
- **Oracle-based 이진 탐색**: Linux 커널 단일 병목 구간 디버깅 시 GCC를 "온라인 정답 컴파일러"로 활용, 이진 탐색 + delta debugging으로 문제 파일 조합을 격리.
- **검증 문제 경고**: "직접 검증하지 않은 소프트웨어를 배포하는 개발자에 대한 우려"를 저자 자신이 명시적으로 표명.

---

## 구체적 패턴·체크리스트·숫자

| 지표 | 수치 |
|---|---|
| 운영 기간 | 약 2주 연속 |
| Claude Code 세션 수 | 2,000+ |
| 입력 토큰 | **20억 (2B)** |
| 출력 토큰 | **1억 4천만 (140M)** |
| 총 비용 | **~$20,000** |
| 생성 코드량 | **100,000줄 (Rust)** |
| GCC torture test 통과율 | **99%** |
| 병렬 에이전트 수 | **16개** |
| 컴파일 성공 프로젝트 | Linux 커널 6.9 (x86/ARM/RISC-V), QEMU, FFmpeg, SQLite, PostgreSQL, Redis, Doom |

**모델별 능력 임계점:**
- Opus 4.0 — 기능적 컴파일러 간신히 가능
- Opus 4.5 — 대규모 테스트 suite 최초 통과; 실제 프로젝트 컴파일 실패
- Opus 4.6 — Linux 커널 등 실질적 실세계 프로젝트 컴파일 성공

**한계:**
- 16비트 x86 효율 코드 생성 불가 (GCC 위임)
- 독립 어셈블러/링커 없음 (최종 링킹은 GCC 의존)
- GCC 최적화 비활성 시 생성 코드 효율 열세
- 모든 프로젝트가 컴파일되지는 않음

---

## 인용 가치 있는 구절

> "Write extremely high-quality tests — poor tests cause agents to solve the wrong problem."

> "80% of effort went into harness and test design rather than agent prompting."

> "Each agent autonomously selects the 'next most obvious problem' without an orchestration layer."

> "The thought of programmers deploying software they've never personally verified is a real concern."

> "Opus 4.6 achieved substantial real-world compilation capability" — 모델 능력 임계점의 갑작스러운 도약을 묘사하는 문장.

---

## 이식 가능한 원시요소

- **P1. 파일 락 기반 태스크 큐** (`current_tasks/` 텍스트 파일): 오케스트레이터 없이 N개 에이전트가 작업 중복을 피하는 최소 코디네이션 패턴. — standalone-extractable: **yes**

- **P2. 무한루프 컨테이너 재생성 패턴** (`while true; do claude ...; done`): 에이전트 세션이 끝나면 즉시 새 컨텍스트로 재시작하여 컨텍스트 오염을 초기화. — standalone-extractable: **yes**

- **P3. `--fast` 샘플링 테스트 모드**: 전체 테스트의 1~10%를 결정론적 랜덤으로 샘플링 → 에이전트 세션 내 빠른 피드백 루프. 에이전트별 시드 고정으로 회귀 추적 가능. — standalone-extractable: **yes**

- **P4. Oracle 이진 탐색 + delta debugging**: 알려진 정답 컴파일러(GCC)를 oracle로 두고 문제 파일 조합을 이진 탐색으로 격리하는 디버깅 패턴. — standalone-extractable: **partial** (oracle 역할의 대응물이 존재해야 함)

- **P5. 역할 전문화 에이전트 분리**: QA, 성능, 문서, 중복제거 등 역할을 독립 에이전트로 분리해 메인 개발 흐름과 병행 실행. — standalone-extractable: **yes**

- **P6. 공유 진행 문서 (PROGRESS.md 류)**: 에이전트가 시도한 접근법·남은 태스크를 공유 파일에 기록 → 컨텍스트 교환 채널 역할. — standalone-extractable: **yes**

---

## 기존 하네스 노트와의 연결

**compound-engineering** (`notes/harness/compound-engineering.md`):
- 공통점: 역할 전문화 에이전트 분리 (compound의 14개 리뷰 서브에이전트 vs 이 케이스의 6~7개 역할 에이전트). 둘 다 "다음 이터레이션이 더 빠르게" 지향.
- 차이점: compound는 인간이 Plan→Work→Review→Compound 루프를 능동적으로 주도하고 CLAUDE.md에 학습을 축적. 이 케이스는 인간 개입 없이 에이전트가 자율 진행하며 진행 문서가 학습 축적 역할을 대신.

**gstack** (`notes/harness/gstack.md`):
- 공통점: 역할 결박 (role perspective as constraint surface). gstack의 CEO/EM/Staff Engineer 역할 결박 vs 이 케이스의 QA/성능/문서 에이전트 분리는 같은 원리.
- 차이점: gstack은 인간이 슬래시 커맨드로 역할 전환을 명시적으로 호출; 이 케이스는 에이전트가 역할을 스스로 유지하며 자율 동작.

**ouroboros** (`notes/harness/ouroboros.md`):
- 공통점: 무한루프 실행 생명주기 + 상태는 외부 파일(EventStore vs `current_tasks/` + git)로 관리.
- 차이점: ouroboros는 Socratic 인터뷰·모호성 게이트·PAL Router 등 진입 구조가 정교함; 이 케이스는 진입 구조 없이 단순 무한루프.

**revfactory-harness** (`notes/harness/revfactory-harness.md`):
- 공통점: 에이전트 팀 아키텍처, 병렬 실행, 품질 에이전트 분리 패턴.
- 차이점: revfactory는 "하네스를 생성하는 하네스"라는 메타-스킬 접근. 이 케이스는 단일 목적(컴파일러 구축) 전용 하드코딩 아키텍처.

**축(axis) 수준 연결:**
- 축 F (skill as unit of discipline): 역할 에이전트 분리 패턴 — 5번째 독립 사용 후보
- 축 G (execution environment as constraint surface): Docker 컨테이너 격리 + git upstream 공유 — 강한 재사용
- 축 A (iteration-boundary semantics): 무한루프 내 세션 경계 = 컨텍스트 초기화 경계 — 재사용
- 새 축 후보: **"lock-file as coordination primitive"** — 오케스트레이터 없이 파일 시스템 락으로 N-에이전트를 조율하는 패턴은 기존 12축에 없음

---

## 후속 조사 / 빈틈

1. **프롬프트 전문 (AGENT_PROMPT.md)**: 공개 여부 불명. 역할별 프롬프트 구조가 어떻게 설계되었는지 확인 필요.
2. **락 충돌 처리**: 에이전트가 동일 락을 동시에 취득 시도할 때 백오프 전략이 있는지, 아니면 단순 선착순인지 불명.
3. **컨텍스트 오염 차단 구체 구현**: 테스트 출력 바이트 제한의 구체적 임계값 미공개.
4. **비용 대비 기여**: 16개 에이전트 중 실질 기여 비중 분포가 균등한지, 특정 에이전트에 집중되는지 불명.
5. **생성 Rust 코드 품질**: "전문가 수준은 아니지만 허용 가능(acceptable)"이라는 저자 평가 — 코드 리뷰 구체 기준 미공개.
6. **재현 가능성**: 하네스 코드가 오픈소스로 공개되었는지 확인 필요. 현재 블로그 포스트만 확인.
7. **$20,000 비용 정당화 기준**: 동일 결과를 인간 엔지니어 팀으로 달성하는 비용과의 비교 프레임이 포스트에 제시되었는지 추가 확인 필요.
