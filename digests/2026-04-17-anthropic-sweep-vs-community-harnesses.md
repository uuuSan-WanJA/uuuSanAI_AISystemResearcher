---
title: Anthropic 공식 글 10편 vs 커뮤니티 하네스 9종 비교 다이제스트
date: 2026-04-17
type: digest
sources_anthropic:
  - anthropic-building-effective-agents
  - anthropic-harness-design-long-running-apps
  - anthropic-effective-harnesses-long-running-agents
  - anthropic-effective-context-engineering
  - anthropic-writing-tools-for-agents
  - anthropic-multi-agent-research-system
  - anthropic-demystifying-evals
  - anthropic-code-execution-with-mcp
  - anthropic-managed-agents
  - anthropic-building-c-compiler
sources_community:
  - ralph-wiggum
  - superpowers
  - gsd
  - gstack
  - openspec
  - ouroboros
  - ecc
  - compound-engineering
  - revfactory-harness
status: draft
---

## TL;DR (3줄)

Anthropic 10편이 제시한 **패턴 언어**(Augmented LLM → 7 workflow/agent 패턴 + Brain/Hands/Session 분리 + Context engineering + Eval 로드맵)와 커뮤니티 9종 하네스가 **상당 부분 수렴**하지만, 측정 가능한 수치 주장(Anthropic의 65% 토큰 절감, 90.2% 성능 향상, 42→95% CORE-Bench, P95 TTFT 90% 감소)은 커뮤니티 측에서 거의 재현되지 않는다(revfactory +60% 품질 주장 제외, gap: 3자 검증 부재). 가장 심각한 공백은 **(a) Regression eval 수명주기, (b) Vault+Proxy 크리덴셜 격리, (c) Brain/Hands/Session 구조적 분리**로, 커뮤니티 하네스 중 어느 것도 이 세 가지를 제대로 구현하지 않는다.

---

## A. Coverage Matrix — Anthropic 7패턴 × 커뮤니티 9하네스

Anthropic이 `building-effective-agents`에서 정리한 **7가지 canonical 패턴**(Augmented LLM 기반 + 5 workflow + 1 autonomous agent)이 각 커뮤니티 하네스에서 어떻게 구현되어 있는지 매핑한다. 표기: Y=명시적 구현, P=부분 구현, N=없음, —=해당 범주가 무의미.

| 패턴 | Ralph | Superpowers | GSD | gstack | OpenSpec | Ouroboros | ECC | Compound | revfactory |
|---|---|---|---|---|---|---|---|---|---|
| **Augmented LLM** (retrieval+tools+memory) | P (파일시스템만) | Y (SKILL.md+MCP) | Y (.planning/+MCP) | P (역할 컨텍스트) | Y (spec+Markdown) | Y (EventStore+MCP) | Y (181 skills+hooks) | Y (docs/solutions+MCP) | Y (메타스킬이 생성) |
| **Prompt Chaining** (순차+gate) | N (단일 루프) | Y (brainstorm→spec→plan→TDD→dev→review→finalize) | Y (discuss→plan→execute→verify→ship) | Y (Think→Plan→Build→Review→Test→Ship→Reflect, Build gap) | Y (propose→apply→archive) | Y (interview→seed→execute→evaluate→evolve) | P (훅 라이프사이클) | Y (Plan→Work→Review→Compound) | Y (6-phase 파이프라인) |
| **Routing** (분류→전문 라우팅) | N | P (서브에이전트 분기) | P (carve-off 라우팅) | Y (23+ 슬래시→역할) | N | Y (PAL Router 3-tier) | Y (NanoClaw v2) | Y (14 리뷰어 라우팅) | Y (팀 자동 생성) |
| **Parallelization** (Sectioning/Voting) | N (1 writer) | P (독립 서브에이전트) | Y (웨이브 병렬) | P (동시 역할 리뷰) | N | P (비동기 목표, Issue #371) | Y (14+ 도메인 병렬) | Y (14 병렬 리뷰, /lfg 50+) | Y (15 태스크 A/B) |
| **Orchestrator-Workers** (동적 분해) | N | Y (서브에이전트 dev/review) | Y (.planning/+Task() 200K) | P (Staff Engineer 역할) | N | Y (evolve_step 오케스트레이션) | Y (NanoClaw v2 핫로드) | Y (/ce:plan 3-parallel 연구) | Y (메타 수준 워커 생성) |
| **Evaluator-Optimizer** (생성자↔평가자) | N (독립 평가자 부재) | Y (HARD-GATE+DOT, v5.0.6 inline 롤백) | P (/gsd:verify-work) | P (plan-*-review 계열) | P (델타 마커 비교) | Y (ambiguity≤0.2/similarity≥0.95/drift≤0.3) | Y (/learn→/evolve) | Y (베스트프랙티스 에이전트 genetic search) | Y (Phase 7 Harness Evolution) |
| **Autonomous Agent** (도구 피드백 루프) | Y (`while true` 극단) | P (HARD-GATE로 제약) | P (체크포인트로 제약) | N (plan-heavy) | N | Y (`ooo ralph` 모드) | P (NanoClaw 라우팅 내) | P (/lfg 50+) | N (일회성 메타스킬) |

**관찰**: 커뮤니티 하네스는 **Prompt Chaining(9/9)** 과 **Orchestrator-Workers(7/9)** 에는 강하게 수렴하지만, **Evaluator-Optimizer**는 명시적으로 구현한 경우가 4개뿐이며 그중 Superpowers는 v5.0.6에서 비용 문제로 inline self-review로 **롤백**했다(ref: `superpowers`). 이는 Anthropic `multi-agent-research-system`의 "~15× 토큰 비용" 경제성 경고와 정확히 일치하는 실패 증거다.

**핵심 "축" 포착**: Anthropic `managed-agents`의 **Brain/Hands/Session 3-layer 분리**는 위 7패턴과 직교하는 **인프라 레이어** 개념이므로 별도로 취급한다. 커뮤니티 하네스 중 이 3-layer 분리를 구조적으로 구현한 경우는 없으며, Ouroboros의 EventStore+MCP 구조가 가장 근접하지만 Brain은 여전히 하네스와 묶여 있다(ref: `ouroboros`, `anthropic-managed-agents`).

---

## B. Anthropic 경험적 수치 vs 커뮤니티 채택 현황

Anthropic 포스트가 제시한 **측정 가능한 수치 주장**과 그에 대응되는 커뮤니티 하네스의 **구현/검증 상태**를 대조한다. 커뮤니티에 해당 수치 또는 원리 구현이 없으면 **gap: 미구현** 또는 **gap: 미명시**로 표시한다.

| # | Anthropic 수치/원리 | 출처 | 커뮤니티 대응 | 평가 |
|---|---|---|---|---|
| B1 | **ResponseFormat enum: 206 tok → 72 tok (65% 절감)** — Slack tool | `anthropic-writing-tools-for-agents` | 어느 커뮤니티 하네스도 툴셋 토큰 밀도를 측정하지 않음 | **gap: 미측정**. Compound의 14 리뷰 에이전트·ECC의 181 skills 모두 총 토큰 사용량의 툴별 분해가 공개되지 않음. |
| B2 | **멀티에이전트 90.2% 성능 향상 + ~15× 토큰 비용** (BrowseComp) | `anthropic-multi-agent-research-system` | Compound `/lfg` 50+ 에이전트, ECC 47 서브에이전트, Ouroboros 500 parallel Sonnet — 수치 벤치마크 미공개 | **부분 수렴**. Superpowers v5.0.6 inline 롤백(ref: `superpowers`)과 Ouroboros Issue #371(공유 토큰 버킷)(ref: `ouroboros`)이 Anthropic의 "~15×" 비용 경고를 **사후 확증**한다. Anthropic 원 수치는 3자 재현 없음(gap). |
| B3 | **CORE-Bench: 42% → 95%** (grader 수정 후) + Capability/Regression 이분법 | `anthropic-demystifying-evals` | 커뮤니티 하네스 중 **어느 것도 자체 grader 품질을 eval하지 않음** | **gap: 전면 미구현**. ECC `/learn`→`/evolve`(ref: `ecc`)와 Compound `docs/solutions/`(ref: `compound-engineering`)는 학습 축적은 있지만 Regression suite 승격 메커니즘이 없다. Anthropic 포스트의 "teams without evals get bogged down in reactive loops" 경고가 9/9 커뮤니티 하네스에 직접 적용. |
| B4 | **MCP code execution: 150K tok → 2K tok (98.7% 절감)** — Google Drive→Salesforce | `anthropic-code-execution-with-mcp` | 어느 커뮤니티 하네스도 progressive tool loading을 구조적으로 채택하지 않음 | **gap: 미구현**. ECC(181 skills 핫로드)(ref: `ecc`)와 Ouroboros(`ToolSearch` 지연 로딩)(ref: `ouroboros`)가 원리적으로 근접하지만 토큰 절감 측정값 미공개. |
| B5 | **Managed Agents: P50 TTFT 60% 감소 / P95 TTFT 90%+ 감소** + Vault+Proxy | `anthropic-managed-agents` | **커뮤니티 하네스 중 Vault+Proxy에 상응하는 크리덴셜 격리 구현 0건** | **gap: 전면 미구현**. Ralph `--dangerously-skip-permissions`(ref: `ralph-wiggum`), Superpowers 동일 플래그 전제(ref: `superpowers`), gstack·GSD 모두 크리덴셜 보안에 대해 명시적 경계 없음. Anthropic이 제시한 "프롬프트 인젝션 한 번이면 크리덴셜 탈취" 위협 모델이 커뮤니티에 미반영. |
| B6 | **Retro Game Maker: Solo $9 / 20분 vs Full $200 / 6시간 (≈20× 비용)** + Sprint Contract 27 기준 | `anthropic-harness-design-long-running-apps` | revfactory: "+60% 품질"(15 태스크 A/B, ref: `revfactory-harness`) / Compound: 구체적 비용 비교 없음 / 나머지: 비용 벤치마크 미공개 | **부분 수렴**. revfactory는 태스크 A/B 구조(ref: Anthropic의 Capability eval Step 3 balanced set)(ref: `anthropic-demystifying-evals`)를 명시적으로 따른 유일한 사례. 다만 3자 검증 부재(gap). |
| B7 | **200+ feature JSON + Puppeteer MCP E2E gate** (premature victory 차단) | `anthropic-effective-harnesses-long-running-agents` | Superpowers: `<HARD-GATE>` XML + DOT(ref: `superpowers`) / GSD: `/gsd:verify-work`(ref: `gsd`) / OpenSpec: 델타 마커(ref: `openspec`) | **수렴 강함**. 셋 다 "자기 선언 완료" 차단 패턴 공유. 다만 Anthropic의 "passes: false 기본값 + JSON(markdown 아님)" 선택 근거("모델이 JSON 파일을 부적절하게 변경할 가능성이 낮음")는 커뮤니티 중 OpenSpec의 RFC 2119 + Gherkin 조합만이 구조적으로 근접. |
| B8 | **C compiler: 16 parallel Claudes × 2주 / 2B 입력 tok / $20K / GCC torture 99%** | `anthropic-building-c-compiler` | Ralph(1-writer greenfield 90% 주장, ref: `ralph-wiggum`) / revfactory(한국어 연구 논문 동반, ref: `revfactory-harness`) | **상호 보완**. Anthropic 케이스는 "중앙 오케스트레이터 없이 파일 락(`current_tasks/`)"을, Ralph는 "단일 루프 + 파일시스템 = 유일한 기억"을 택한다. 둘 다 오케스트레이터 없음 + 파일시스템 상태 원리 공유. $20K 비용은 커뮤니티 측에 대응 수치 없음(gap). |
| B9 | **서브에이전트 반환: 수만 tok 소비 → 1,000–2,000 tok 압축 요약만 상위로** | `anthropic-effective-context-engineering` | GSD `.planning/`+`Task()` 200K carve-off(ref: `gsd`) / Compound 3-parallel 연구 에이전트 통합(ref: `compound-engineering`) / ECC 47 서브에이전트 | **원리적 수렴**. 다만 "1,000–2,000 tok 압축 요약" 정량 기준을 실제 적용/측정한 커뮤니티 하네스 없음(gap: 임계값 미명시). |
| B10 | **Agent eval 8단계 로드맵**: 20–50 태스크 시작 + step-sequence grader 금지 + positive/negative 균형 | `anthropic-demystifying-evals` | revfactory: 15 태스크 A/B(ref: `revfactory-harness`) — 유일한 명시적 eval set | **부분 수렴**. revfactory가 태스크 수(15 ≈ 20–50 하단)·A/B 구조 면에서 Anthropic 권고에 가장 가깝지만, "step-sequence grader 금지"·"positive/negative 균형" 원칙은 공개 정보로 확인 불가(gap). |

**항목 수**: 10개(요구 ≥6 충족).

---

## C. 커뮤니티가 놓친 공백(Gaps)

Anthropic 포스트가 제시했지만 9/9 커뮤니티 하네스에서 구조적으로 구현되지 않은 항목을 **심각도 순**으로 정리한다.

### C1. Regression eval 수명주기 관리 — 전면 미구현

Anthropic `anthropic-demystifying-evals`는 **Capability eval**(낮은 통과율에서 개선 신호 추출)과 **Regression eval**(~100% 유지)을 명확히 분리하고, SWE-Bench Verified가 1년 만에 40%→80%+로 포화된 사례를 제시한다. 9/9 커뮤니티 하네스 중 어느 것도 이 이분법을 구조적으로 구현하지 않는다. ECC `/learn`→`/evolve`(ref: `ecc`)와 Compound `docs/solutions/`(ref: `compound-engineering`)가 학습 축적은 하지만, **"어느 태스크가 포화되어 regression으로 강등되었는가"를 자동 판별하는 메커니즘이 전무**하다. 결과: 커뮤니티 하네스의 반복 이터레이션은 "노이즈 대 실제 회귀"를 구별하지 못한 채 무한히 돌 위험을 안고 있다(Anthropic 원 경고 그대로 적용).

### C2. Vault+Proxy 크리덴셜 격리 — 전면 미구현

Anthropic `anthropic-managed-agents`의 핵심 보안 주장은 "프롬프트 인젝션 하나면 Claude가 환경 변수를 읽어 크리덴셜을 탈취할 수 있다"는 결합 아키텍처의 구조적 취약성이다. 이를 **Bundled Authentication** 또는 **Vault+Proxy** 두 패턴으로 해결한다. 커뮤니티 9/9 하네스 중 어느 것도 이에 상응하는 크리덴셜 격리 레이어를 갖고 있지 않다. Ralph(ref: `ralph-wiggum`)와 Superpowers(ref: `superpowers`)는 `--dangerously-skip-permissions`를 전제로 하며, gstack(ref: `gstack`)·GSD(ref: `gsd`)는 보안 경계를 명시적으로 다루지 않는다. revfactory(ref: `revfactory-harness`)·OpenSpec(ref: `openspec`)은 스펙 생성에 집중하고 실행 보안은 에이전트 런타임에 위임. ECC(ref: `ecc`)는 "보안 스캐닝"을 언급하지만 실행 경계에서의 크리덴셜 격리와는 다른 레이어.

### C3. Brain/Hands/Session 3-layer 구조적 분리 — 전면 미구현

Anthropic `anthropic-managed-agents`가 제시한 "Brain(무상태 하네스) / Hands(`execute(name, input)→string` 단일 인터페이스) / Session(외부화 append-only 이벤트 로그)" 분리는 **모델 업그레이드 시 하네스 기술 부채를 0으로 만드는** 구조적 답이다. Ouroboros EventStore(ref: `ouroboros`)가 Session 개념에 가장 근접하지만, Brain은 여전히 MCP 서버와 묶여 있다. GSD 체크포인트(ref: `gsd`), Ralph `PROMPT.md`+git(ref: `ralph-wiggum`)는 "파일시스템이 상태"지만 컨테이너 수명과 분리되지 않는다. 결과: 커뮤니티 하네스는 **Claude Sonnet 4.5 → Opus 4.6 업그레이드 시 "context anxiety 회피 스캐폴딩이 죽은 코드가 되는"**(Anthropic `anthropic-harness-design-long-running-apps` 명시 사례) 위험을 직접적으로 안고 있다.

### C4. 툴셋 토큰 밀도 측정 원칙 — 전면 미측정

Anthropic `anthropic-writing-tools-for-agents`의 5대 설계 원칙 중 핵심은 "Optimize for Token Efficiency"(ResponseFormat enum, pagination, 25K response cap). Slack tool의 206→72 tok(65% 절감) 수치가 대표 증거. Anthropic은 **"툴 설명 개선만으로 태스크 완료 시간 40% 단축"**(`anthropic-multi-agent-research-system`)까지 주장한다. 커뮤니티 9/9 하네스 중 어느 것도 자사 툴/스킬의 토큰 밀도를 측정·공개하지 않는다. Compound 14 리뷰 에이전트·ECC 181 skills·Superpowers SKILL.md 묶음·gstack 23+ 슬래시 커맨드 — 모두 토큰 회계의 1급 대상이지만 수치 미공개(gap: 측정 원칙 자체가 채택되지 않음).

### C5. pass@k vs pass^k 이중 지표 사용 — 전면 미구현

Anthropic `anthropic-demystifying-evals`는 **pass@k**(k회 중 ≥1회 성공, 상향, 단일 솔루션 시나리오)와 **pass^k**(k회 모두 성공, 하향, customer-facing 신뢰성)를 상호보완 지표로 제안한다(예: 75% per-trial × 3회 = pass^3 ≈ 42%). 커뮤니티 하네스 중 이 공식으로 자사 하네스를 측정한 경우 0건. Ralph "그린필드 90% 성공"(ref: `ralph-wiggum`)·gstack "60일 60만 LOC"(ref: `gstack`)·revfactory "+60% 품질"(ref: `revfactory-harness`) 모두 **단일 시도 통과율** 기반 주장이며, 비결정성 하에서의 신뢰성(pass^k)은 미공개(gap).

---

## D. Cross-Reinforcement — 커뮤니티가 Anthropic을 보완·확장하는 지점

### D1. Compound 14 parallel 리뷰어 = Anthropic의 "단일 LLM judge가 앙상블보다 낫다" 주장에 대한 직접 반증 후보

Anthropic `anthropic-demystifying-evals`는 "단일 LLM 판단이 앙상블보다 인간 판단과 더 일치"한다고 명시하지만, Compound Engineering `notes/harness/compound-engineering.md`는 security-sentinel / dhh-rails-reviewer / performance-oracle 등 **14개 역할별 독립 판단 + 종합** 구조를 대규모 채택(14.2k ⭐)했다. 두 주장이 **동일 태스크에서 어느 쪽이 우세한지 비교 실험되지 않았다**. 커뮤니티 채택 수치(14.2k 스타)는 Anthropic의 single-LLM judge 권고에 대한 실전 반례 후보로 가치가 있다(ref: `compound-engineering`, `anthropic-demystifying-evals`).

### D2. Ouroboros의 숫자 임계값 게이트 = Anthropic Prompt Chaining "gate" 개념의 수치 구현

Anthropic `anthropic-building-effective-agents`의 Prompt Chaining 패턴은 "gate = 프로그래밍 방식 체크"라는 개념만 제시하고 구체적 수치 임계값은 주지 않는다. Ouroboros `notes/harness/ouroboros.md`는 **ambiguity ≤ 0.2**, **ontology similarity ≥ 0.95**, **drift ≤ 0.3**이라는 3개 숫자 임계값으로 이를 구현한 유일한 사례. Ouroboros의 수치는 Anthropic이 `anthropic-harness-design-long-running-apps`에서 언급한 "Sprint Contract 27 기준"과 원리적으로 같은 계열(구현 전 테스트 가능한 성공 기준 협상)이지만, 숫자 임계값 수준까지 구체화한 것은 Ouroboros가 선도. **Anthropic 측에 수치 임계값 사례로 역수입할 가치 있음**(ref: `ouroboros`, `anthropic-building-effective-agents`, `anthropic-harness-design-long-running-apps`).

### D3. GSD `.planning/` carve-off = Anthropic "just-in-time context loading" 원리의 파일 시스템 구현

Anthropic `anthropic-effective-context-engineering`은 "경량 식별자만 유지 + 런타임에 도구로 필요 데이터 동적 로드"를 추상적으로 제시한다. GSD `notes/harness/gsd.md`의 `.planning/PROJECT.md`·`REQUIREMENTS.md`·`ROADMAP.md`·`STATE.md` 구조 + `Task()` 200K 서브에이전트 carve-off는 이 원리의 **파일 시스템 레벨 완전 구현**이다. tentenco가 "GSD=실행 환경 제약"이라 요약한 것은 Anthropic의 just-in-time 원리가 "실행 환경을 제약 표면으로 사용"하는 형태로 구현될 수 있음을 보여준다. Anthropic의 서브에이전트 1,000–2,000 tok 요약 반환 원칙(`anthropic-effective-context-engineering`)을 GSD carve-off에 결합하면 **측정 가능한 현실적 구현 청사진**이 된다(ref: `gsd`, `anthropic-effective-context-engineering`).

### D4. Anthropic C compiler 파일 락 + Ralph 무한 루프 = "오케스트레이터 없는 코디네이션" 축의 공동 증거

Anthropic `anthropic-building-c-compiler`의 "16 parallel Claudes + `current_tasks/` 텍스트 락 + 중앙 오케스트레이터 없음" 패턴과 Ralph `notes/harness/ralph-wiggum.md`의 "`while true` + 파일시스템 = 유일한 지속 기억" 패턴은 **독립적으로 도달한 같은 결론**이다: 오케스트레이터 레이어는 파일 시스템 컨벤션으로 대체 가능. 두 케이스 모두 동일 원리를 공유하지만 스케일(1 vs 16)과 상태 표현(단일 git vs `current_tasks/` 락)이 다르다. 이는 "lock-file as coordination primitive"가 현재 12축 분류에 없는 **새 축 후보**임을 시사(ref: `anthropic-building-c-compiler`, `ralph-wiggum`).

---

## E. Next Steps — 우선순위화된 후속 조치

### E1. Regression eval 수명주기 패턴(P2 from `anthropic-demystifying-evals`)을 ECC/Compound에 이식하는 프로토타입

**이유**: C1 gap이 가장 심각하고, ECC `/learn`→`/evolve`(ref: `ecc`)·Compound `docs/solutions/`(ref: `compound-engineering`)는 이미 학습 축적 인프라가 있어 "포화 자동 판별 → regression suite 승격" 레이어만 추가하면 즉시 적용 가능. **insights/ 승격 최우선 후보**.

### E2. Vault+Proxy 크리덴셜 격리(C2 gap)를 커뮤니티 하네스에 역수입하는 참조 구현

**이유**: C2 gap은 보안 관점에서 치명적이고, Anthropic `anthropic-managed-agents`의 두 패턴(Bundled Authentication / Vault+Proxy)은 구현 난이도가 중간 수준. Ralph 계열(ref: `ralph-wiggum`)·Superpowers 계열(ref: `superpowers`)이 전제로 깐 `--dangerously-skip-permissions`의 구조적 대안으로 제시 가능. **insights/ 2순위**.

### E3. Ouroboros 숫자 임계값 게이트(D2)를 일반 Prompt Chaining 설계 지침으로 추상화

**이유**: Anthropic 원 포스트에 숫자 임계값 gate 사례가 부재하므로, Ouroboros(ref: `ouroboros`)의 ambiguity ≤ 0.2 / similarity ≥ 0.95 / drift ≤ 0.3을 "gate = 수치 임계값"이라는 재사용 가능한 설계 원시요소로 추출. 이식 가능성 **높음**(모든 Prompt Chaining 하네스에 적용 가능).

### E4. 툴셋 토큰 밀도 측정 프로토콜(C4 gap) 정의

**이유**: Anthropic Slack tool 206→72 tok(65% 절감, ref: `anthropic-writing-tools-for-agents`)과 MCP code execution 150K→2K tok(98.7% 절감, ref: `anthropic-code-execution-with-mcp`) 수치는 커뮤니티 하네스가 **자사 스킬/툴 묶음의 토큰 회계**를 공개하지 않는 한 비교 불가. Compound 14 리뷰어·ECC 181 skills·gstack 23+ 커맨드를 대상으로 **ResponseFormat enum 도입 + 응답 25K cap + concise/detailed 분기 벤치마크**를 제안. 경제성 가시화 측면에서 가치 높음.

### E5. C compiler + Ralph 공통 원리 기반 "lock-file as coordination primitive" 신축 제안

**이유**: D4의 공동 증거가 기존 12축에 없는 새 축 후보를 시사. `anthropic-building-c-compiler`의 `current_tasks/` 텍스트 락과 Ralph(`notes/harness/ralph-wiggum.md`)의 git+file 상태를 통합해 **"오케스트레이터 없는 N-에이전트 코디네이션의 최소 primitive"** 축으로 승격 제안. insights/로는 최하 우선순위지만 **장기 분류 체계 강화**에 기여.

---

## 본문 외: 코퍼스 한계

- **Anthropic 포스트 수치의 3자 검증 부재**: 90.2%·65%·98.7%·P95 TTFT 90%·$20K 등 수치는 Anthropic 자체 보고. 독립 재현 실험은 코퍼스 내 없음.
- **커뮤니티 하네스 스타 수치의 organic-vs-incentivized 분해 불가**: ECC 82K→140K(ref: `ecc`)·gstack 71.3k(ref: `gstack`)·Compound 14.2k(ref: `compound-engineering`)·Ouroboros 2.3k(ref: `ouroboros`) 급증 곡선이 실제 채택인지 바이럴 효과인지 구별 어렵다.
- **한국어 사용자 저자 하네스 2종 편중**: Ouroboros(Q00, Seoul, ZEP)·revfactory(황민호, Jeju, Kakao) — 한국 AI 생태계 샘플링 편향 가능성. 다른 지역 하네스 조사 시 대조군 필요.
- **Anthropic `anthropic-managed-agents`의 공개 범위**: Managed Agents API 외부 공개 여부 불명(ref: `anthropic-managed-agents` §후속 조사 1). 본 digest는 내부 인프라 가정 하에 비교했다.

---

*Cited source slugs (19/19 corpus)*: `anthropic-building-effective-agents`, `anthropic-harness-design-long-running-apps`, `anthropic-effective-harnesses-long-running-agents`, `anthropic-effective-context-engineering`, `anthropic-writing-tools-for-agents`, `anthropic-multi-agent-research-system`, `anthropic-demystifying-evals`, `anthropic-code-execution-with-mcp`, `anthropic-managed-agents`, `anthropic-building-c-compiler`, `ralph-wiggum`, `superpowers`, `gsd`, `gstack`, `openspec`, `ouroboros`, `ecc`, `compound-engineering`, `revfactory-harness`.
