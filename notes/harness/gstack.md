---
title: gstack
date: 2026-04-13
author: Garry Tan (President & CEO, Y Combinator — github:garrytan, x:@garrytan)
first_public: ~2026-02 (viral Mar 2026; TechCrunch coverage 2026-03-17; bswen docs 2026-03-31)
primary_source: https://github.com/garrytan/gstack
topic: harness
tags: [harness, claude-code, skill-pack, role-personas, plan-heavy, decision-layer, garrytan, gstack, y-combinator]
status: deep-dive
confidence: medium-high
rounds: 4
axes_used: [1,2,3,4,5,6,7,8,9,10,11,12]
axes_added: [role_perspective_as_constraint_surface]
axes_dropped: []
candidate_axis_reuse:
  - C (mode splitting) — 7-phase sprint (Think → Plan → Build → Review → Test → Ship → Reflect) with 23+ slash commands, each scoped to one role and one decision class. **5번째 독립 사용.**
  - G (execution environment as constraint surface) — tentenco의 3-축 대비("Superpowers=process, GSD=environment, gstack=perspective")가 축 G를 **보색(complement) 축**으로 소환. gstack은 G 축을 직접 재사용하지 않고 **대립 축**으로 쓰지만, 비교 프레임으로 1회 기능. 약한 재사용.
  - H (artifact naming schema as protocol) — `.tmpl` (human-edited) vs generated `.md` (never edited directly) + `browse/dist` never-committed 규칙이 파일명에 역할 인코딩. **2번째 독립 사용 후보**(GSD의 `{PHASE}-{WAVE}-{TYPE}.md` 대비 약함).
  - F (skill as unit of discipline) — `SKILL.md` + YAML frontmatter(`allowed-tools:`, `preamble-tier:`, `version:`) + auto-invoke 조건 기술은 Superpowers의 SKILL.md 컨벤션과 동일 계열. **2번째 독립 사용.**
candidate_axis_proposals:
  - role_perspective_as_constraint_surface — 새 축 제안. 축 G(execution environment)의 쌍대(dual): 하네스가 LLM을 **어떤 역할 관점**에서 생각하게 강제하는가. 본문 §13 참조.
notes: |
  Dispatched via WebFetch + WebSearch in 4 rounds (Agent-dispatch tool
  unavailable — Ralph/Superpowers/GSD/Ouroboros 와 동일 precedent).
  Primary sources: garrytan/gstack README·CLAUDE.md·ETHOS.md·SKILL.md
  (office-hours). Secondaries: tentenco Medium 2026-04, Agent Native
  Medium 2026-03-14, dev.to imaginex 스태킹 글, awesomeagents.ai 가이드,
  sitepoint 리뷰, mindstudio 분석 2종, bswen docs 2026-03-31, bskiller
  deep-dive, Hacker News 토론, augmentcode 분석. Garry Tan 자신의 트윗
  (2032196172, "god mode" CTO 인용)은 검색 스니펫으로만 확보 — 트윗
  본문 직접 fetch는 402(paywall). 첫 공개 정확 일자는 미확보 —
  레포는 2026-02 직전 존재했고 2026-03 중순 바이럴 확산. TechCrunch
  2026-03-17 커버리지가 가장 이른 주류 보도로 확인.
---

## TL;DR (3줄)
gstack은 Y Combinator 대표 **Garry Tan**이 2026년 초 공개한 Claude Code용 **skill-pack 하네스**로, 23+개 슬래시 커맨드(`/office-hours`, `/plan-ceo-review`, `/plan-eng-review`, `/review`, `/ship` 등)를 **각각 하나의 엔지니어링 역할(CEO / Engineering Manager / Staff Engineer / Designer / QA Lead / CSO / Release Engineer …)에 결박**시켜 "Claude를 한 명의 팀원이 아니라 조직으로 부리는" 기법을 체계화했다. 본질은 tentenco가 요약하듯 "**gstack은 의사결정 관점(decision-making perspective)을 제약한다**" — Superpowers가 프로세스를, GSD가 실행 환경을 제약한다면 gstack은 **"LLM이 어떤 역할의 시선으로 판단할 것인가"**를 강제한다. 단 구조적 결함이 뚜렷하다: Think→Plan→Build→Review→Test→Ship→Reflect 7단계 중 **Build 단계에 대응하는 skill이 없다**(tentenco 관찰). 저자의 "60일간 60만 LOC, 주간 10~20K LOC" 주장은 1차로는 프론트페이지 README 그대로이나 3자 검증 불가(Hacker News/bskiller 강한 반론).

## Disambiguation (중요)
검색 시 혼동되는 프로젝트들:
- `Chachamaru127/claude-code-harness` — 별개의 "Plan→Work→Review" 하네스. 같은 키워드만 공유.
- `affaan-m/everything-claude-code` — 또 다른 skill-pack, 이름 유사.
- **canonical gstack = `github.com/garrytan/gstack`** (Garry Tan, YC). 2026-04 기준 71.3k stars / 10k forks / MIT (레포 페이지 확인).
- 공식 랜딩: `gstacks.org` ("Turn Claude Code into a Virtual Software Development Team")

> "gstack — Garry Tan's opinionated Claude Code setup featuring 23 specialized tools functioning as a virtual engineering team (CEO, Designer, Eng Manager, Release Manager, Doc Engineer, QA)." — GitHub 레포 설명

## 1. Identity & provenance
- **Author**: Garry Tan (President & CEO, Y Combinator) — @garrytan / github:garrytan
- **레포**: `github.com/garrytan/gstack`, 라이선스 **MIT**, 2026-04-13 기준 ~71.3k stars / ~10k forks
- **First public**: 정확 일자 미확보. 가장 이른 주류 보도 **TechCrunch 2026-03-17** ("Why Garry Tan's Claude Code setup has gotten so much love, and hate"). bswen 2026-03-31 문서에 이미 상세 분석 존재. Agent Native Medium 글은 **2026-03-14**. 2026-03 초순 전후 공개로 추정.
- **바이럴 궤적**: 공개 48시간 내 10k stars 돌파(augmentcode 보도), 몇 주 내 66k stars, 4월 초 71.3k. Garry Tan의 YC 대표 플랫폼 효과 명시적 동반.
- **유지 상태**: 매우 활발. bswen 기준 "v0.15.14.0 / 204 commits / 33 contributors" (2026-04-06), 이후 계속 증가.
- **비공식 주장 (저자 자신, README)**: "2026 — 1,237 contributions and counting"

## 2. Problem framing
Garry Tan이 명시적으로 말한 문제의식은 레포 서문 + ETHOS.md에서 추출된다. 핵심은 **"한 명의 창업자가 엔지니어링 팀 20명처럼 출하(ship)하기"** — 그는 README에서 다음을 수치로 주장한다:

> "In the last 60 days: 600,000+ lines of production code (35% tests), 10,000-20,000 lines per day, part-time, while running YC full-time." — garrytan/gstack README

그의 프레임은 "생산성" 그 자체가 아니라, **효율 압축으로 완전성(completeness)이 값싸졌다는 인식**이다. ETHOS.md의 "Boil the Lake" 원칙이 이 프레임의 심장이다:

> "AI-assisted coding makes the marginal cost of completeness near-zero. When the complete implementation costs minutes more than the shortcut — do the complete thing. Every time. Boil lakes. Flag oceans as out of scope." — gstack ETHOS.md

대립 축은 **"legacy thinking from when human engineering time was the bottleneck"**(README)으로, "시간이 비싸니 쇼트컷을 쳐라"는 전통적 소프트웨어 공학 지혜에 대한 명시적 반박이다. 이 지점이 Hacker News 커뮤니티의 격렬한 반발(후술 §10)을 촉발한다.

## 3. Control architecture
**Workflow(코드 경로) 타입**. 내부 자율 루프 없음. `./setup` 스크립트 + Claude Code의 기본 skill-loading 메커니즘이 전부.

**7-phase sprint**: Think → Plan → Build → Review → Test → Ship → Reflect. 각 단계는 사람이 슬래시 커맨드로 수동 전환하거나 `/autoplan` 같은 메타-커맨드로 연쇄 호출한다. 종료 조건은 human-decided — 자율 종료 없음.

> "28 slash commands across seven development phases: Think, Plan, Build, Review, Test, Ship, and Reflect" — awesomeagents.ai (sitepoint 보강)

**구조적 특이점**: 핵심 관찰은 tentenco의 것이다.

> "Its workflow runs: Think (/office-hours) → Plan (/plan-*-review) → Build → Review (/review) → Ship (/ship). But the Build phase has no corresponding skill. Claude Code reverts to default mode until you manually run /review." — Ewan Mak (tentenco), Medium 2026-04

즉 **Build 단계에 대응하는 skill이 구조적으로 비어 있다**. 이는 "Claude Code가 Build 중에는 어떤 역할에도 묶이지 않고 자기 기본 모드로 돌아가 버린다"는 뜻이며, Superpowers의 TDD/subtask dispatch나 GSD의 context isolation + atomic commits가 강점을 가지는 바로 그 지점에 대한 공백이다.

Anthropic 분류 매핑: **workflow 우위**. agent-side autonomy는 skill 내부에만 국한되며 skill은 LLM-directed 프로세스가 아니라 "역할 페르소나 + 할 일 체크리스트"에 가깝다.

## 4. State & context model
gstack의 상태 모델은 **파일 기반이되 Ralph/GSD만큼 엄격하지 않다**. 핵심 아티팩트:

| 파일/디렉토리 | 역할 | 변경자 |
|---|---|---|
| `CLAUDE.md` (repo 루트에 gstack이 심는 것) | "persistent context that Claude Code reads at the start of every session" (mindstudio) | operator + `/gstack-upgrade` |
| `SKILL.md` (각 skill 폴더) | skill 본문. prompt template "instructions about methodology, not executable scripts" | gstack maintainer |
| `.tmpl` 파일 | 사람이 편집하는 템플릿 | human |
| 생성된 `.md` 파일 | skill output — "never edited directly" | agent |
| `ETHOS.md` | 철학/원칙 레이어 | human |
| `AGENTS.md` | agent methodology 문서 | human |
| `browse/dist/`, `design/dist/` | 컴파일 바이너리 — "never committed" | build system |

**런타임에 모델이 보는 것**: 매 세션 시작 시 `CLAUDE.md`가 최상위 컨텍스트로 주입되고, 호출된 slash command의 `SKILL.md`가 당해 턴의 프롬프트 레이어가 된다. skill 간 상태 전파는 **"Output from /office-hours feeds into /plan-ceo-review, which feeds into /plan-eng-review. Each step's output becomes the next step's input."** (Agent Native Medium)

즉 gstack의 상태 전파는 **연쇄 슬래시 커맨드 파이프라인** — 각 단계가 다음 단계에 읽히는 artifact(주로 plan doc)를 남기는 Unix-pipe 방식이다. 이는 Ralph의 `IMPLEMENTATION_PLAN.md` single-living-file과도, GSD의 `{PHASE}-{WAVE}-{TYPE}.md` protocol naming과도 다른 중간 지점.

## 5. Prompt strategy
gstack 본질의 **7할**이 이 축에 있다. 핵심 무브는 세 가지:

### (a) Role-scoped SKILL.md convention
각 skill은 YAML frontmatter + 자연어 본문 구조. `/office-hours` skill의 frontmatter가 대표 예:

> ```yaml
> name: office-hours
> preamble-tier: 3
> version: 2.0.0
> description: YC Office Hours — two modes. Startup mode: six forcing questions that expose
>   demand reality, status quo, desperate specificity, narrowest wedge, observation,
>   and future-fit. Builder mode: design thinking brainstorming for side projects...
> allowed-tools: Bash, Read, Grep, Glob, Write, Edit, AskUserQuestion, WebSearch
> ```
> — gstack/office-hours/SKILL.md

`allowed-tools:` 필드는 **tool permission을 skill frontmatter에서 선언**하는 GSD와 동일 계열의 장치. `preamble-tier: 3`은 컨텍스트 프리앰블 주입 수준을 숫자로 표현 — 미니멀 gate 문법.

### (b) One command = one decision class
Agent Native의 요약:

> "When Claude operates as an engineering manager reviewing code, it ignores feedback about UI colors and focuses on framework choices and maintainability." — Agent Native, Medium 2026-03-14

즉 `/plan-eng-review`와 `/plan-design-review`는 **서로 겹치지 않는 관심사**로 엄격히 분리되어, "한 대화에서 product judgment + implementation + verification이 뒤섞이는" 통상 Claude Code 용법을 차단한다.

### (c) Role injection via natural language
CLAUDE.md의 설계 원칙은 "Express conditionals as English. Instead of nested if/elif/else in bash, write numbered decision steps." — gstack/CLAUDE.md. 즉 **분기/게이트를 코드가 아닌 자연어 steps로** 쓴다. Superpowers의 DOT/HARD-GATE와 정반대 매체 선택.

### 보조 메커니즘들
- **"Boil the Lake" 인라인 원칙** — 모든 skill이 shortcut 대신 complete implementation을 선호하도록 유도
- **User Sovereignty 규칙** — "AI models recommend. Users decide. This is the one rule that overrides all others." (ETHOS.md). 명시적 HITL primacy 선언.
- **Search Before Building** — "Three Layers of Knowledge" (standard patterns → current best practices → first-principles). skill이 build 전 web search/grep를 의무화.

> "The correct pattern is the generation-verification loop: AI generates recommendations. Users verify and decide. The AI never skips verification because it's confident." — gstack ETHOS.md

### Sub-agent / parallel 장치
`/pair-agent` ("Multi-agent coordinator with shared browser") + "Conductor" 언급(mindstudio: "Conductor that runs multiple Claude Code sessions in parallel — each in its own isolated workspace"). Ralph의 worktree 패턴과 유사한 parallel execution layer가 skill-pack 외부에 동거.

## 6. Tool surface & permission model
- **Permission posture**: 각 skill이 `allowed-tools:` frontmatter로 **자신이 필요로 하는 툴만** 선언. Ralph의 YOLO와 대조되는 **fine-grained declarative permission**.
- **Destructive-command guards**: gstack의 서명 primitive는 **`/careful` / `/freeze` / `/guard` 3종 세트**:
  > "/careful warns before any destructive command — rm -rf, DROP TABLE, force-push, git reset --hard" — mindstudio
  > "/freeze locks edits to one directory while debugging" — mindstudio
  > "/guard: Full safety combining /careful + /freeze" — README
- **Browser daemon**: "persistent Chromium process via Playwright with 100-200ms latency per command — claimed to be '20x faster than Chrome MCP tools'" (awesomeagents.ai). `/open-gstack-browser`, `/setup-browser-cookies`, `/connect-chrome` 등.
- **Localhost-only + bearer token** 인증, "without mandatory telemetry" (awesomeagents.ai)
- **크로스호스트 지원**: `./setup --host <name>` — Claude Code (default), Codex CLI, OpenCode, Cursor, Factory Droid, Slate, Kiro
- **/codex**: "Second opinion from OpenAI Codex CLI" — gstack 내부에서 **다른 에이전트에게 cross-check 질의** 가능. 설계상 주목할 포인트.

## 7. Human-in-the-loop points
gstack은 **HITL을 명시적 설계 원칙**으로 내세운 최초 하네스 중 하나:

> "User Sovereignty: AI models recommend. Users decide. This is the one rule that overrides all others." — gstack ETHOS.md

- `/office-hours` 인터뷰 단계 — 사람이 Q1~Q6 답변 필수
- `/plan-*-review` 체인 각 단계 — 사람이 다음 단계 호출 수동
- `/careful` — 파괴적 명령 실행 전 인간 승인 강제
- `/qa-only` — "Bug report without code changes" (QA 관찰 모드)
- `/land-and-deploy` — PR merge + deploy는 사람이 명시적으로 호출
- **"Review Readiness Dashboard"** — Agent Native: "shows which reviews ran, what's missing, and whether you're clear to ship." (tentenco 재인용)

전체적으로 **HITL이 외부 아니라 내부에 편재** — Ralph와 정반대 스펙트럼.

## 8. Composability
- **플러그인이 아닌 skill-pack**: 설치는 `git clone → ./setup` 단순 파일 복사. Superpowers의 plugin-marketplace 경유와 다른 경로.
- **멀티호스트 1차 지원**: 7개 이상 agent runtime에서 동일 skill 재사용. GSD의 CLI 다중지원, Ouroboros의 installer와 같은 계열.
- **다른 하네스와의 스태킹이 명시적 담론화됨**: dev.to imaginex 글이 "gstack + Superpowers + GSD"를 실제 실무 조합으로 제시:
  > "gstack thinks, GSD stabilizes, Superpowers executes." — dev.to imaginex 2026
- **단, 토큰 비용이 스태킹 걸림돌**:
  > "Bloated and token-hungry when fully enabled. A single execution-layer skill can consume 10K+ tokens before code is written." — dev.to imaginex
  > "gstack for the decision layer (cherry-picked)... prioritize high-value flows like /office-hours and /plan-ceo-review, avoid over-investing in every role." — dev.to imaginex

## 9. Empirical claims & evidence

### Garry Tan 자신 주장 (README + X 포스트)
- **600,000+ LOC / 60일 / 35% tests** (README, 위 §2 인용)
- **10,000~20,000 LOC / day part-time** (README)
- **140,751 LOC / 362 commits / 1주** (README, `/retro` 통계)
- **1,237 contributions in 2026** (README)
- **"Your gstack is crazy. This is like god mode. Your eng review discovered a subtle cross site scripting attack that I don't even think my team is aware of. I will make a bet that over 90% of new repos from today forward will use gstack."** — Garry Tan, X 2032196172430131498 (CTO 친구 인용, 그의 트윗)

### 3자 관찰 / 간접 증언
- **tentenco(Medium 2026-04)**: gstack의 decision-layer 강점 공인, Build 공백 비판
- **Agent Native(Medium 2026-03-14)**: "mapping to how real engineering organizations actually work" 디자인 의도 확인
- **Andrej Karpathy 인용(gstack README)**: "I don't think I've typed like a line of code probably since December" — gstack 맥락의 인증 인용(Karpathy가 gstack을 쓴다는 언급이 아니라, AI-assisted workflow의 일반 정당화로 README가 차용)

### 벤치마크? 없음
**통제된 벤치마크는 공개된 것 없음.** 모든 수치는 저자 자기보고 + 스크린샷 + 일화. Braintrust/Ralph 류의 독립 토큰 측정도 부재.

## 10. Failure modes & limits

### 저자 자인 (or 레포 상의 경고)
- **token bloat** — 모든 skill 동시 활성화시 컨텍스트 과포화. `preamble-tier` 필드 존재 자체가 이 문제 의식의 증거.
- **제한된 build-phase 지원** — README는 "Build" 단계 skill 공백을 암시적으로만 인정(`/investigate`, `/review` 등 인접 단계는 있음).
- **Lines-of-code 메트릭의 자기모순**: 저자 자신 ETHOS.md의 "Completeness is cheap"과 "600K LOC" 자랑 사이의 긴장은 비판자들이 명시적으로 지적(후술).

### 3자 관찰 — **Hacker News (#47418576)**
HN 쓰레드는 gstack에 대한 **가장 조직화된 반대 목소리** (사용자명 verbatim):
- **the_af**: "writing over 600,000 lines of production code is not _something to be proud of_" — LOC를 liability로 보는 전통 소프트웨어 공학 원리 위반
- **tabs_or_spaces**: "LOC will never be a good metric of software engineering. Why do we keep accepting this?"
- **coldtea**: 그 수치는 "would be considered a huge liability and shameful historically"
- **Sherveen** (가장 많이 인용된 회의론자): "overengineered" 셋업이며 "will not make your agents better, and is likely to make it worse". 대안으로 Every Inc의 compound engineering plugin과 Simon Willison의 agentic patterns 제시.
- **arnvald**: "adding an ad to every single skill... unnecessarily clutters the context" — 모든 skill이 gstack 자기-프로모션 블럭을 포함하는 것을 비판
- **madrox** (실사용자): "/ceo role feels ... not terribly effective", 단 design/plan skills는 인정
- **input_sh**: astroturfing 의혹, "five digits" 월별 API 비용 우려, YC 창업자 편향 가능성

### 3자 관찰 — tentenco
- **Build 단계 skill 공백** (위 §3 인용) — gstack의 가장 중요한 구조적 결함으로 tentenco가 명시.
- 결과: "Claude Code reverts to default mode until you manually run /review" — 즉 **가장 위험한 단계에서 gstack의 제약이 풀림**.

### 3자 관찰 — dev.to imaginex
- **token-hungry**: 모든 skill 켜면 실행 전부터 10K+ 토큰 소모
- **"Execution feels rougher vs Superpowers"** — 실행 레이어 품질에서 Superpowers에 밀림

### 3자 관찰 — bswen / bskiller / awesomeagents
- **novelty challenge**: "just prompts in text files — that many developers had built similar setups privately" (awesomeagents.ai 요약)
- **credibility amplification**: "Tan's prominence as Y Combinator's CEO gave the project 'outsized attention' relative to technical merit" (awesomeagents.ai)
- **지속가능성 문제**: TechCrunch/주류 보도 재인용 "sleeping only four hours a night" + "cyber psychosis"(농담이라고 후속 해명) — **저자 페르소나와 제품 규범 사이의 긴장**이 담론화됨
- **retrofitting 어려움**: "If your project already exists and doesn't conform to a clean stack definition, onboarding it to GStack takes real effort. It's a framework you build with from the start more than something you retrofit onto existing work." — mindstudio gstack vs hermes 분석

### 3자 관찰 — augmentcode
- **600K LOC 주장 신뢰성**: "I don't take that claim at face value" — augmentcode 저자
- **"you're not adopting new infrastructure, you're adopting a process"** — 기술적 혁신 부재에 대한 정직한 요약

## 11. Transferable primitives ★ (load-bearing)

각 항목: 이름 / 설명 / 전제 컨텍스트 / standalone-extractable?

### P1. Role-scoped slash command as perspective constraint
- 한 slash command = 한 페르소나(CEO / Eng Manager / Designer / Staff Engineer / QA / CSO / Release Engineer …). 같은 코드라도 **누가 보느냐**에 따라 review vector가 달라지게 강제.
- 전제: slash command 지원 하네스, skill-level prompt injection.
- **YES**. 그리고 **gstack의 가장 순수한 기여**. Superpowers/GSD에 없는 primitive.

### P2. `/office-hours` 6-forcing-question interview gate
- 코드 쓰기 전에 Demand Reality / Status Quo / Desperate Specificity / Narrowest Wedge / Observation / Future-Fit 6개 질문을 사람이 답변. Y Combinator의 실제 office hours 방법론 이식.
- 전제: 사람이 답할 시간/의지.
- **YES**. 하네스 독립적 primitive로 뽑아도 즉시 쓸 수 있는 "Problem-first gate".

### P3. "Boil the Lake" completeness bias
- Shortcut보다 complete implementation 선호. "lake is boilable, ocean is not" — 완전성이 달성 가능할 때는 항상 완전성 선택.
- 전제: AI-assisted coding의 마진 비용 압축이 실재함. 완전성 평가 척도 필요.
- **PARTIAL**. 원칙은 이식 가능하나, "lake vs ocean" 판정 자체가 어려워 운영자 판단 의존.

### P4. User Sovereignty as hard principle
- "AI models recommend. Users decide." — generation-verification loop 명시적 선언. skill이 "자신감이 있어도 verification을 건너뛰지 말라"고 agent에게 금지.
- 전제: agent가 자연어 원칙 존중.
- **YES**. 가장 이식 쉬운 원칙 — 한 줄 프롬프트 규칙으로 어느 하네스에도 추가.

### P5. `/careful` + `/freeze` + `/guard` destructive-command firewall
- 파괴적 명령 warn / 파일 편집 범위 lock / 둘의 조합. YOLO의 대척점.
- 전제: bash 샌드박스 제어 가능, skill이 shell 검사 가능.
- **YES**. Ralph의 `--dangerously-skip-permissions`를 정확히 반전하는 원시요소.

### P6. `allowed-tools:` frontmatter declarative permission
- 각 skill이 자신이 호출할 수 있는 툴만 YAML에 선언. 원칙적 least-privilege.
- 전제: 하네스가 frontmatter를 파싱해 permission 적용.
- **YES**. GSD의 동일 패턴과 **같은 방향으로 수렴하는 2차 증거**.

### P7. Pipeline chaining: skill output as next skill input
- `/office-hours` → `/plan-ceo-review` → `/plan-eng-review` 순으로 각 단계의 산출물이 다음 단계의 명시적 입력. Unix pipe 멘탈 모델.
- 전제: skill이 파일 기반 handoff 지원.
- **YES**. 그러나 구현은 "파일을 한 방향으로 흘린다"는 명시적 컨벤션 필요 — 자동 enforcement 없음.

### P8. `/codex` cross-model second opinion primitive
- gstack 내부에서 OpenAI Codex CLI에게 재검토 요청. 모델 간 cross-check를 slash command 하나로.
- 전제: 로컬에 다른 CLI 설치.
- **PARTIAL**. 개념은 일반화, 구현은 런타임 의존.

### P9. "Three Layers of Knowledge" search-first discipline
- 구현 전 search 순서: standard patterns → current best practices → first-principles. 모든 skill에 주입.
- 전제: agent가 web search/grep 툴 보유.
- **YES**. "reinvention detection" primitive.

### P10. Role-perspective as first-class constraint surface
- LLM을 "일반 조수"가 아니라 "역할을 부여받은 전문가"로 호출한다는 **설계 철학 자체**. 하나의 대화에 role을 뒤섞지 않는 것.
- 전제: 호출자가 사전에 역할을 선택할 수 있는 이해도.
- **YES** — 이것이 이식해야 할 **멘탈 모델**. 23개 command는 그 모델의 특정 표현일 뿐.

### Rejected as primitive
**"10k LOC per day" metric은 이식하지 말 것.** 저자 자신의 ETHOS.md ("Completeness is cheap" — 즉 양이 아니라 완전성이 덕목)와도 모순되고, Hacker News 커뮤니티가 체계적으로 논박한 지점이다. gstack을 따라하면서 LOC 메트릭을 목표로 삼는 것은 ETHOS.md의 "Search Before Building" 원칙("reinventing something worse")을 정면 위반한다. **멘탈 모델 P1~P10은 가져가되 수치 자랑은 두고 올 것.**

## 12. Open questions
- **정확한 first-public 날짜** — TechCrunch 2026-03-17이 확실한 상한. 그 전 어느 시점에 Git 히스토리가 시작되었는지 첫 커밋 타임스탬프 미확보(레포 루트 fetch로는 확인 불가).
- **Build-phase skill 공백의 저자 해명** — Tan 본인이 이 관찰에 응답한 기록 미발견. 의도적 설계인지 로드맵 공백인지 불분명.
- **Conductor / `/pair-agent` 내부 구현** — Ralph의 worktree 대비 관계, 실제 동시성 상한, 비용 추적 — 모든 정보가 secondary 코멘터리에 의존. 1차 파일(`agents/` 폴더의 SKILL.md들) 직접 읽기 필요.
- **"Review Readiness Dashboard" 실물** — tentenco가 언급한 대시보드의 실제 artifact 형식(JSON? Markdown? TUI?) 미확인.
- **v2 / TypeScript rewrite 계획?** — GSD가 밟은 경로를 gstack이 따라갈지 여부. 1차 정보 없음.
- **Dex/HumanLayer 또는 Josh Devon 급의 체계적 postmortem** — HN 쓰레드 외 전문가급 비판 글이 아직 없음.
- **한국어 커뮤니티 채택** — 영어 기반 자료만 확보. tentenco 저자 Ewan Mak이 대만/홍콩권으로 추정되며, 한국 커뮤니티의 독립 재현 사례는 미확인.

## 13. 축 제안: Role perspective as constraint surface (새 후보축)

gstack을 seed schema로 분석하면서 가장 뚜렷하게 드러난 것은 **기존 축들이 gstack의 본질을 정확히 포착하지 못한다**는 사실이다. tentenco의 3-축 구분 — "Superpowers=process, GSD=environment, gstack=**perspective**" — 는 축 G("execution environment as constraint surface")가 커버하지 못하는 **쌍대 축(dual axis)**을 요구한다.

**제안 축 K (role_perspective_as_constraint_surface)**:
- 하네스가 제약하는 주 대상이 **LLM의 "누구의 시선으로 사고하는가"(role / persona / decision class)**인가.
- G축(execution environment = 컨텍스트·세션·권한·스케줄링)의 쌍대.
- 현재 gstack만 단일 사용이나, Anthropic의 Claude Projects, BMAD-METHOD의 ~21 persona 시스템, Agent OS의 standards injection 모두 이 축의 변종으로 볼 수 있어 **2~3개 빠른 독립 사용 확보 전망**.

**측정 가능한 하위 질문**:
1. 역할 정의가 어디에 있는가 (SKILL.md frontmatter / CLAUDE.md / dedicated persona file)
2. 역할 간 전환이 명시적인가 (slash command 교체) 아니면 암묵적인가 (persona mention)
3. 한 대화 안에서 다중 역할 허용 여부, 허용 시 역할 충돌 조정 규칙
4. 역할별 permission / tool 접근 차등이 있는가 (gstack의 `allowed-tools:` + role mapping)

이 축이 승격되면 BMAD-METHOD / Agent OS / Ouroboros의 PAL Router는 G축, gstack / Party Mode / Claude Projects는 K축으로 정렬 가능해져 비교 도식이 훨씬 명료해진다.

## Sources

### Primary (레포 내부)
- https://github.com/garrytan/gstack — 레포 루트 (71.3k stars / MIT / 2026-04-13 fetch)
- https://github.com/garrytan/gstack/blob/main/README.md — 600K LOC 주장 원문
- https://github.com/garrytan/gstack/blob/main/CLAUDE.md — instruction template 철학
- https://github.com/garrytan/gstack/blob/main/ETHOS.md — Boil the Lake / User Sovereignty / Search Before Building
- https://github.com/garrytan/gstack/blob/main/office-hours/SKILL.md — 대표 SKILL.md frontmatter
- https://github.com/garrytan/gstack/blob/main/ARCHITECTURE.md — (참조만, 본 라운드에서 full fetch 안 함)

### Primary (저자 public posts)
- https://x.com/garrytan/status/2032196172430131498 — "god mode" CTO 인용 트윗 (검색 스니펫)
- https://x.com/garrytan/status/2037051410857283967 — "GStack beats Superpowers head to head" (검색 스니펫, 본문 paywall)
- https://gstacks.org/ — 공식 랜딩

### 주류 / 3자 보도
- https://techcrunch.com/2026/03/17/why-garry-tans-claude-code-setup-has-gotten-so-much-love-and-hate/ — 이른 주류 커버리지
- https://news.ycombinator.com/item?id=47418576 — HN 쓰레드 (the_af, Sherveen, arnvald, madrox, coldtea, tabs_or_spaces, input_sh)
- https://medium.com/@tentenco/superpowers-gsd-and-gstack-what-each-claude-code-framework-actually-constrains-12a1560960ad — tentenco 3-framework 비교
- https://agentnativedev.medium.com/garry-tans-gstack-running-claude-like-an-engineering-team-392f1bd38085 — Agent Native 2026-03-14
- https://dev.to/imaginex/a-claude-code-skills-stack-how-to-combine-superpowers-gstack-and-gsd-without-the-chaos-44b3 — 3-way stacking 논의
- https://awesomeagents.ai/guides/gstack-garry-tan-claude-code-guide/ — 아키텍처 상세, 비판 요약
- https://docs.bswen.com/blog/2026-03-31-what-is-gstack-claude-code/ — 2026-03-31 시점 상태(v0.15.14.0)
- https://www.mindstudio.ai/blog/what-is-gstack-gary-tan-claude-code-framework — 기본 소개
- https://www.mindstudio.ai/blog/gstack-vs-superpowers-vs-hermes-claude-code-frameworks — retrofitting 비판
- https://www.augmentcode.com/learn/garry-tan-gstack-claude-code — "I don't take that claim at face value" 비판
- https://bskiller.com/blog/deep-dive-19-garry-tan-gstack-god-mode — (403) 제목만 확보
- https://www.sitepoint.com/gstack-garry-tan-claude-code/ — (403) 제목만 확보

### 변종 / 스태킹 구현
- https://github.com/UpayanGhosh/claude-jarvis — gstack + GSD + Superpowers intent router
- https://github.com/affaan-m/everything-claude-code — 유사 카테고리 skill-pack (disambiguation용)
