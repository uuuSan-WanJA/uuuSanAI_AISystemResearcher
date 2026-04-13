---
title: Everything Claude Code (ECC)
date: 2026-04-13
author: Affaan Mustafa (@affaan-m, San Francisco)
first_public: 2026-01 (GitHub open-source release, MIT)
primary_source: https://github.com/affaan-m/everything-claude-code
topic: harness
tags: [harness, claude-code, multi-harness, skill-system, agent-delegation, security, instinct-learning, nanoclaw, agentshield]
status: deep-dive
confidence: medium
rounds: 3
axes_used: [1,2,3,4,5,6,7,8,9,10,11,12]
axes_added: [instinct_learning_as_harness_layer]
axes_dropped: []
candidate_axis_proposals: [instinct_learning_as_harness_layer]
notes: |
  Dispatched via WebFetch + WebSearch in 3 rounds (Agent dispatch tool
  unavailable; same pattern as prior analyses). Primary sources: GitHub
  README, release notes, ClaudePluginHub, bridgers.agency, augmentcode.com
  teardown, dev.to cheatsheet, Ewan Mak / tentenco Medium article (Mar 2026).
  NanoClaw v2 internals remain partially opaque — no standalone documentation
  page found; description synthesized from scattered README snippets and
  release notes. Instinct confidence scoring internals unverified.
  Star count data: sources cite 82K (tentenco Mar 2026), 100K (augmentcode
  early Apr 2026), 118K (augmentcode Apr 2026), 140K (README Apr 2026) —
  rapid growth but organic-vs-incentivized split unknown.
---

## TL;DR (3줄)
ECC는 Affaan Mustafa가 10개월 이상의 Claude Code 일상 사용 끝에 공개한 **크로스하네스 에이전트 설정 번들**로, 47개 전문화 서브에이전트·181개 스킬·72개 규칙·20개+ 훅을 하나의 설치형 레이어로 묶는다. 핵심 아이디어는 "에이전트 런타임에 사전 구성된 역할·워크플로·학습 루프를 주입하면 매번 다시 설정하는 비용을 없앨 수 있다"는 것으로, NanoClaw v2 오케스트레이터가 모델 라우팅과 스킬 핫로드를 담당한다. Ewan Mak(tentenco)의 표현대로 ECC는 **"레이어 추가형 하네스"** 로, 실행 환경 제약(GSD)이나 프로세스 제약(Superpowers)이 아닌 **사전 구성된 역할·스킬 생태계를 삽입**하는 방식으로 포지셔닝된다.

---

## 1. Identity & provenance

- **Author**: Affaan Mustafa, 샌프란시스코 기반 개발자. Claude Code 실험 출시(2025-02)부터 매일 사용.
- **Origin**: 2025-09 Anthropic × Forum Ventures 해커톤(Cerebral Valley, NYC) 우승 — 8시간 내 zenith.chat 빌드, $15,000 API 크레딧 획득. 당시 사용한 설정 번들이 ECC의 기반.
- **First public**: 2026-01, MIT 라이선스 GitHub 공개.
- **Star trajectory**: 82K (2026-03, tentenco) → 100K (2026-04초) → 118K → 140K+ (2026-04-13 README). 초기 바이럴은 Affaan이 X에 올린 "Shorthand Guide" 스레드가 90만 뷰, 1만 북마크를 기록하며 시작됨.
- **Maintenance posture**: 활발. 2026-04-05 v1.10.0 출시(ECC 2.0 alpha 포함). 170+ contributors. 150+ GitHub App 설치.
- **프로 티어**: v1.9.0(2026-03-21)부터 `$19/seat/month` Pro 티어(Stripe 빌딩, 프라이빗 레포). 오픈소스 + 상업화 혼합 모델.

> "Affaan Mustafa, a San Francisco-based developer, has been using Claude Code daily since its experimental rollout in February 2025. In September 2025, he won the Anthropic x Forum Ventures hackathon at Cerebral Valley with an agent optimization system he had been refining for months." — bridgers.agency

---

## 2. Problem framing

저자의 명시적 문제 프레임: **"AI 코딩 에이전트를 생산적으로 쓰려면 매번 바닥부터 설정하는 비용이 너무 크다."** ECC는 이를 "성능 최적화 시스템"으로 해결한다고 주장한다 — 토큰 효율, 세션 간 컨텍스트 유지, 패턴의 재사용 가능 스킬 추출, 보안 스캐닝.

> "ECC is not just configs. It's a complete system: skills, instincts, memory optimization, continuous learning, security scanning, and research-first development." — README

추가 프레임: **크로스하네스 표준화**. Claude Code만 지원하는 다른 하네스와 달리 ECC는 Cursor, OpenCode, Codex, Gemini까지 "동일한 행동"을 재현하겠다는 목표를 가진다.

---

## 3. Control architecture

**혼합형: hook-lifecycle + 선형 스킬 실행 + NanoClaw v2 그래프 오케스트레이션.**

- **Hook-based lifecycle**: `SessionStart`, `PreToolUse`, `PostToolUse`, `Stop` 훅이 세션 전 구간을 커버. 훅은 Node.js DRY 어댑터 패턴으로 작성돼 플랫폼 간 이식됨.
- **선형 스킬 실행**: 개별 스킬(`/tdd`, `/code-review` 등)은 단일 워크플로 파일을 선형 실행. LLM 지시형이지만 스크립트 형태에 가까움.
- **NanoClaw v2**: 오케스트레이터 레이어. 모델 라우팅(태스크 컨텍스트에 따른 모델 자동 선택), 스킬 핫로드(동적 스킬 주입), 세션 브랜치/검색/익스포트/컴팩트/메트릭. v1.8.0(2026-03-05)에서 공개 강화됨.
- **ECC 2.0 alpha (Rust control-plane)**: v1.10.0에서 등장. `dashboard / start / sessions / status / stop / resume / daemon` 명령 제공. 아직 알파.
- **루프**: `/loop-start`, `/loop-status` 커맨드 + PM2 통합으로 장기 자율 실행 지원. Ralph 스타일 bash 루프와는 달리 PM2 오케스트레이션 레이어를 씀.
- **Anthropic 분류 매핑**: 스킬 레벨 = workflow(코드패스), 하네스 레벨 = 에이전트(LLM 지시형 위임). 하이브리드.

**Termination conditions**: 명시적 stop condition 없음. `/quality-gate`, `/checkpoint`, `/verify` 커맨드가 게이트로 기능하나 자동 종료 조건 아님.

---

## 4. State & context model

| 저장소 | 역할 | 유형 |
|---|---|---|
| SQLite state store | 설치된 컴포넌트 추적, 증분 업데이트 | 영속 |
| Instinct store | 신뢰도 스코어 0.3–0.9를 가진 학습된 패턴 | 반영속 |
| Session adapters | 구조화된 세션 레코딩 (브랜치·검색·컴팩트) | 세션 범위 |
| Memory hooks | SessionStart 루트 폴백, Stop-phase 요약 자동 저장 | 세션 간 |
| `~/.claude/rules/` | 규칙 파일 (플러그인 배포 불가, 수동 설치 필수) | 영속 |

**핵심 차이**: Ralph가 파일시스템을 유일한 상태 매체로 쓰는 반면, ECC는 **SQLite + instinct store + session adapter**를 중첩해 더 풍부한 상태 레이어를 제공한다. 그러나 이 풍부함은 디버깅 복잡성으로도 돌아온다.

**Memory explosion 완화**: 관찰자 루프가 스로틀링과 테일 샘플링으로 메모리 폭발 위험을 관리. 그러나 이 메커니즘의 내부 임계값은 문서화 미비.

**Context strategy**: "Progressive disclosure" — Claude가 먼저 스킬 이름/설명 목록만 로드하고, 컨텍스트상 관련 스킬만 풀 본문으로 로드. GSD의 `carve-off` 전략과 철학 공유.

---

## 5. Prompt strategy

### 모드 분할
ECC는 한 모노리식 프롬프트 대신 **역할별 스킬 파일**로 분할한다. 예: `/plan`(구현 전 확인 요구), `/tdd`(테스트 우선 사이클), `/code-review`(80% 이상 신뢰도 이슈만 리포트).

### 핵심 전략: "Instinct Learning"
ECC의 가장 독특한 프롬프트 전략 — **행동 패턴을 자동 추출해 재사용 가능한 instinct으로 변환**하는 학습 루프:
- `/learn`: 패턴 추출 실행
- `/evolve`: instinct를 스킬·커맨드·에이전트로 승격
- `/instinct-status`: 신뢰도 목록 조회
- `/instinct-export`, `/instinct-import`: 이식
- `/instinct-prune`: 저신뢰도 instinct 제거
- 5-layer observer loop가 반복 패턴을 감지해 자동 instinct화

### 슬래시 커맨드 분류 (representative)
- **개발**: `/plan`, `/tdd`, `/build-fix`, `/code-review`, `/refactor-clean`, `/verify`, `/checkpoint`
- **멀티모델**: `/multi-plan`, `/multi-execute`, `/multi-workflow`, `/orchestrate`
- **보안**: `/security-scan` (AgentShield 기반)
- **하네스 관리**: `/harness-audit`, `/loop-start`, `/loop-status`, `/quality-gate`
- **세션**: `/sessions`(브랜치/검색/컴팩트), `/model-route`
- **학습**: `/learn`, `/evolve`, `/instinct-status`, `/skill-create`

79개 레거시 커맨드 심은 스킬로의 마이그레이션 중인 구 API 호환 레이어.

### AgentShield
보안 스캐닝 레이어. 1,282 테스트, 102개 규칙, 98% 커버리지 주장. `CLAUDE.md`, `.cursorrules`, `agents.json`을 감사해 취약점·프롬프트 인젝션·설정 드리프트를 검출. PR 리뷰 모드는 설정 변경을 자동 감사.

---

## 6. Tool surface & permission model

- **Tool access**: 모든 Claude Code 툴 오픈. 권한 모델 명시 없음 (YOLO 또는 표준 Claude Code 권한, 하네스 별 조정 없음).
- **Hook profiles**: `ECC_HOOK_PROFILE=minimal|standard|strict` 환경변수로 훅 수위 제어.
- **Selective disable**: `ECC_DISABLED_HOOKS="pre:bash:tmux-reminder,post:edit:typecheck"` 개별 훅 비활성화.
- **MCP servers**: 14개 포함 (상세 목록 미공개, README 언급 수준).
- **AgentShield sandboxing**: 5-layer re-entrancy guard. 보안 스캔은 `/security-scan`으로 명시적 실행.
- **플랫폼**: Windows/macOS/Linux. Claude Code plugin marketplace + shell script(`./install.sh --profile full`) + npm.
- **멀티모델 커맨드** (`/multi-plan`, `/multi-execute`): 별도 `ccg-workflow` 런타임 필요. 없으면 "will not run correctly" — 명시된 제약.

---

## 7. Human-in-the-loop points

- `/plan` 커맨드: **"waits for user confirmation before touching code"** — 명시적 승인 게이트.
- `/quality-gate`, `/checkpoint`: 게이트로 기능하나 자동 차단이 아닌 수동 실행 트리거.
- `/instinct-prune`: 저신뢰도 instinct 제거는 사람이 수동 실행.
- AgentShield PR 심사: 자동 감사 → 결과 리포트. 차단 여부는 사람 판단.
- 장기 루프(`/loop-start`) 중 내부 HITL 없음 — Ralph와 동일한 패턴. 인간은 외곽 모니터.

ECC는 Ralph보다 더 많은 명시적 게이트 포인트를 가지나, 자동화 파이프라인에서 사람 개입을 **강제**하는 구조는 약하다. 주요 게이트는 수동 호출 의존.

---

## 8. Composability

**설계 의도 자체가 "크로스하네스 표준 레이어"**:
- **지원 하네스**: Claude Code, Cursor, OpenCode, Codex(앱+CLI), Gemini
- **설치 방식**: 플러그인 마켓플레이스 / shell script / npm 엔트리포인트 — 3개 경로 중 OSS installer가 가장 안정적이라고 README가 직접 언급
- **선택적 설치**: `--profile core|developer|security|full` 4단계. 증분 채택 가능.
- **Manifest-driven**: v1.9.0+에서 manifest 기반 파이프라인으로 설치 상태를 SQLite에 추적
- **Rules 분리 설치**: 플러그인이 rules를 배포 불가 — `~/.claude/rules/` 수동 설치 필수. 이 분리는 비판의 대상이기도 함 ("Getting agents, skills, hooks, and commands but not rules through the plugin feels incomplete" — Mak)

**타 하네스와의 통합**: 명시적 통합 사례 미확인. ECC가 다른 하네스(Ralph, GSD, gstack)와 협조적으로 쓰인 공개 사례는 Round 3까지 발견 안 됨.

---

## 9. Empirical claims & evidence

### 저자/프로젝트 주장 (자가 측정)
- **140K+ GitHub stars, 21K+ forks, 170+ contributors** (README 2026-04)
- **997+ internal tests passing** (훅/런타임 리팩터 후)
- **1,282 AgentShield security tests**, 102 rules, 98% coverage
- **150+ GitHub App installations**
- X 스레드 90만 뷰, 1만 북마크 (론칭 직후)

### 크리에이터 출처 증거
- Anthropic 해커톤 우승 (2025-09) — 8시간 내 실제 제품(zenith.chat) 빌드.
- 10+ months daily Claude Code use — 경험 기반 주장.

### 3자 측정
- **tentenco (Ewan Mak, Mar 2026)**: code-reviewer 에이전트의 80% 신뢰도 필터링이 노이즈 감소에 실질적 효과. TDD 스킬과 세션 요약 훅은 standalone 가치 인정.
- **augmentcode.com**: 독립 검증 없이 주장 재인용 (프로모셔널 성격).
- **bridgers.agency**: 기술 분해 시도했으나 비판적 검증 없음.

**증거 유형**: 주로 수치(stars, test count) + 저자 경험 주장. 통제된 A/B 비교 없음. "997 tests passing"은 내부 단위 테스트이지 퍼포먼스 벤치마크가 아님.

**Star count 주의**: 개발자 커뮤니티 일부에서 초기 X 스레드 바이럴이 별점을 인위적으로 끌어올렸다는 의구심 제기됨 ("viral X thread inflated metrics; GitHub Discussions activity remains minimal" — Mak).

---

## 10. Failure modes & limits

### 명시된 (README / release notes)
- **플러그인 vs OSS installer 갭**: "plugin is convenient, but OSS installer is still the most reliable path" — 플러그인 경로의 안정성 문제 자인.
- **Rules 배포 불가**: 플러그인으로 rules 설치 불가, 수동 필수 — UX 단절.
- **Multi-model 커맨드 의존성**: `/multi-plan`, `/multi-execute`는 `ccg-workflow` 없으면 실패.
- **Memory explosion 위험**: 관찰자 루프 스로틀링으로 완화하나 임계값 미문서화.

### 커뮤니티 비판 (tentenco / Mak, Mar 2026)
- **Over-engineering**: "Most people just need a good CLAUDE.md, not an entire ecosystem." 997 내부 테스트와 오케스트레이션 엔진은 일반 팀에 과도.
- **Opacity risk**: 시스템을 "without mastering all its moving parts"로 채택하면 디버깅이 이해 범위 밖에 놓임. (bridgers.agency 분석)
- **Star count skepticism**: GitHub Discussions 활동은 daily Issues에 비해 minimal. 스타 수가 실사용 반영 여부 의문.

### 구조적 한계 (분석 도출)
- **NanoClaw v2 내부 불투명**: 독립 문서 없음. 모델 라우팅 결정 로직, 스킬 핫로드 트리거 조건 미공개.
- **Instinct confidence scoring 불투명**: 0.3–0.9 스케일과 5-layer observer loop 구조는 언급되나 평가 함수 미공개. 자동 pruning 기준 불명확.
- **ECC 2.0 alpha 미완성**: Rust control-plane은 아직 알파. 프로덕션 사용 권장 불가.
- **크로스하네스 parity 미검증**: "Claude Code, Cursor, OpenCode, Codex, Gemini 동일 행동"은 주장이나 독립 검증 없음.

---

## 11. Transferable primitives ★ (load-bearing)

각 항목: 이름 / 설명 / 전제 컨텍스트 / standalone-extractable?

### P1. Progressive skill disclosure
- 스킬 이름·설명 인덱스만 먼저 로드, 태스크 관련 스킬만 풀 본문 주입. 컨텍스트 포화 없이 넓은 스킬 라이브러리 유지.
- 전제: 스킬 인덱스 파일 + 라우팅 로직.
- **YES**. GSD의 carve-off와 같은 계열이나 스킬 인벤토리에 특화된 형태. 어떤 에이전트 런타임에도 이식 가능.

### P2. Instinct-confidence learning loop
- 반복 행동 → confidence score → high-confidence는 영속 instinct로 승격, low-confidence는 prune. 에이전트가 프로젝트별 컨벤션을 자동 학습.
- 전제: 세션 기록 스토어, 패턴 추출 로직, 사람의 prune 판단.
- **PARTIAL**. 개념은 이식 가능하나 5-layer observer loop 구현이 ECC-specific. 경량 버전으로 단순화 가능 (수동 `/learn` → 파일 기반 instinct 목록).

### P3. Cross-harness skill portability via convention
- 동일 스킬 파일을 Claude Code / Cursor / Codex 등 여러 런타임에 재사용. 런타임 특이성을 Node.js DRY 어댑터 훅으로 격리.
- 전제: 여러 런타임 환경, manifest 기반 설치.
- **PARTIAL**. 어댑터 패턴은 이식 가능하나 실장은 런타임 목록 의존.

### P4. Role-specialized subagent delegation
- 태스크 유형별로 사전 정의된 에이전트(code-reviewer, security-reviewer, planner, language-specific builder)에 자동 위임. 단일 generalist LLM 호출 대신 전문화.
- 전제: 에이전트 위임 기능이 있는 런타임 (Claude Code subagent, Cursor agent mode).
- **YES**. ECC의 47 에이전트 중 3–5개의 핵심 역할(reviewer, planner, security)만 골라 이식해도 즉시 효과.

### P5. Confidence-gated code review
- code-reviewer 에이전트가 80% 이상 신뢰도 이슈만 리포트. 저신뢰도 노이즈 필터링 → 실행 가능한 피드백만.
- 전제: LLM-based review with self-assessed confidence, human threshold setting.
- **YES**. Mak이 ECC의 독립적 가치를 인정한 단일 컴포넌트. 단독 추출 가능.

### P6. Security-scan as first-class harness layer (AgentShield)
- 에이전트 설정 파일(`CLAUDE.md`, `.cursorrules`)을 정적 분석 규칙 + 레드팀/블루팀 파이프라인으로 감사. 프롬프트 인젝션·설정 드리프트 감지.
- 전제: 감사 대상이 되는 설정 파일 세트, 보안 룰셋.
- **PARTIAL**. 1,282 테스트 규칙셋은 ECC 독점이나 "설정 파일 보안 감사" 개념 자체는 이식 가능.

### P7. Hook-profile tiering (`minimal|standard|strict`)
- 환경변수 하나로 훅 수위를 전환. 개발/CI/프로덕션 컨텍스트에 맞게 훅 레이어 전환 가능.
- 전제: 훅 시스템이 있는 런타임, env var 기반 컨트롤.
- **YES**. 매우 이식 가능한 설계 패턴.

### P8. Manifest-driven incremental install
- SQLite 상태 스토어가 설치된 컴포넌트 추적. 증분 업데이트, 선택적 프로파일, 롤백 경로 제공.
- 전제: 여러 설치 가능 컴포넌트.
- **YES**. 다른 대형 설정 번들에 즉시 적용 가능한 엔지니어링 패턴.

### Rejected as primitive (중요)
**NanoClaw v2를 블랙박스로 채택하지 말 것.** 모델 라우팅·스킬 핫로드 내부 로직이 미공개 상태에서 NanoClaw를 신뢰 기반 의존성으로 쓰면, 예기치 않은 라우팅 결정에 디버깅이 막막해질 수 있다. P1(progressive disclosure)과 P4(role delegation)처럼 이해 가능한 구성 요소만 이식 권장.

---

## 12. Open questions

- **NanoClaw v2 내부 로직**: 모델 라우팅 결정 함수, 스킬 핫로드 트리거 조건 — 독립 문서 없음. ECC 레포 내 코드 직접 추적 필요 (codex:rescue 적합).
- **Instinct confidence scoring 함수**: 0.3–0.9 스케일 평가 로직, 5-layer observer loop 구체 구현 미공개.
- **ECC 2.0 (Rust) 로드맵**: alpha에서 stable로 전환 예정 시기, Rust control-plane이 현 Node.js 훅을 대체하는지 보완하는지 불명확.
- **크로스하네스 parity 독립 검증**: "Cursor / OpenCode / Gemini에서 동일 행동" 주장에 대한 3자 재현 미확인.
- **Star inflation 정도**: 초기 X 바이럴과 유기적 채택 비율 미분리. GitHub Discussions 활동 저조가 실채택률 하방 신호인지 판단 유보.
- **ECC + Ralph/GSD 합성 사례**: ECC를 Ralph 루프나 GSD 파이프라인과 함께 쓰는 재현 사례 미발견.
- **Pro tier 가치**: `$19/seat/month` 유료 플랜의 기능 차이 상세 미확인.

---

## Proposed schema deltas

### 후보 축: Instinct learning as harness layer (신규 후보)
- **Proposed by**: ECC deep-dive (2026-04-13)
- **Rationale**: ECC의 `/learn` → `/evolve` → confidence pruning 사이클은 "하네스가 에이전트 행동을 관찰하고 재사용 가능 패턴으로 자동 추출하는 메타학습 루프"라는 독립 차원. 현재 seed 축 중 축 4(State & context)와 축 5(Prompt strategy)에 분산 가능하나, **하네스 자체가 학습 주체**라는 점에서 별도 축 가치가 있음. Ralph의 "tune like a guitar"(수동)나 GSD의 STATE.md(정적 축적)와 구별되는 동적·자동 학습 루프.
- **Proposed form**: "하네스가 에이전트 행동에서 패턴을 자동 추출해 재사용 가능 단위(instinct/skill/rule)로 승격하는 메타학습 루프를 갖는가. 있다면 (a) 추출 트리거는 무엇인가 (b) 신뢰도 평가 방식은 결정론적인가 LLM 호출인가 (c) 사람의 개입은 어느 지점인가."
- **Promotion threshold**: 동일 (2개 이상 독립 사용 확인 시 승격).
- **Status**: 1회 (ECC). BMAD-METHOD의 agent persona 진화, Ouroboros의 ontology evolution과 유사 방향이나 독립 확인 필요.

### 기존 후보 축 재사용 확인

**축 C (Mode splitting) — ECC 6번째 독립 사용**
- ECC의 `/plan` vs `/tdd` vs `/code-review` vs `/multi-plan` 등 역할별 스킬 분리는 축 C의 재사용. 단, 전환이 명시적 slash command로 이루어지며 모드 간 상태 전달이 session adapter를 통함. **6번째 독립 사용 — 승격 확정 강화**.

**축 F (Skill as unit of discipline) — ECC 3번째 독립 사용**
- ECC의 181개 스킬 파일 + 스킬 인덱스 + `/skill-create`로 사용자가 새 스킬 정의 가능한 구조는 축 F의 재사용. Superpowers(SKILL.md 컨벤션), gstack(YAML frontmatter 스킬)에 이어 3번째. **승격 권고 강화**.

**축 K (Role perspective as constraint surface) — ECC 1번째 독립 사용**
- ECC의 47 전문화 에이전트(code-reviewer, security-reviewer, planner, language-specific 등)는 역할/페르소나를 1차 제약 대상으로 삼는 구조. gstack이 slash command별 역할 결박으로 K를 제안했을 때와 같은 방향. **2번째 독립 사용(ECC) → 축 K 승격 권고 충족**.

**축 G (Execution environment as constraint surface) — ECC 간접 재사용**
- ECC의 `ECC_HOOK_PROFILE=minimal|standard|strict`과 `ECC_DISABLED_HOOKS` env var는 실행 환경을 직접 제어하는 축 G 계열. 직접 독립 사용으로 카운트하기엔 약하나 G의 승격 근거 재확인.

---

## Sources

### Primary
- https://github.com/affaan-m/everything-claude-code — 메인 레포 (README)
- https://github.com/affaan-m/everything-claude-code/releases — 릴리스 노트 v1.2.0~v1.10.0
- https://github.com/affaan-m/everything-claude-code/releases/tag/v1.8.0 — NanoClaw v2 언급

### Secondary (third-party analysis)
- https://medium.com/@tentenco/everything-claude-code-inside-the-82k-star-agent-harness-thats-dividing-the-developer-community-4fe54feccbc1 — Ewan Mak (tentenco), Mar 2026 — **가장 균형 잡힌 분석**
- https://bridgers.agency/en/blog/everything-claude-code-explained — 기술 분해 (프로모셔널)
- https://www.augmentcode.com/learn/everything-claude-code-118k-stars — 수치 집계 (프로모셔널)
- https://dev.to/shimo4228/everything-claude-code-ecc-complete-cheatsheet-24ok — 커맨드 레퍼런스
- https://www.claudepluginhub.com/plugins/affaan-m-everything-claude-code — 플러그인 허브 메타데이터
