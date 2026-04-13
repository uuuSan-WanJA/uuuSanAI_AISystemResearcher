---
title: Ouroboros (우로보로스)
date: 2026-04-13
author: Q00 (Tech Lead @ ZEP, Seoul) — github:Q00, x:@JqOnly, email:jqyu.lee@gmail.com
first_public: 2026-01-14 (레포 생성) / v0.26.6 2026-03-30 첫 릴리즈 tracked
primary_source: https://github.com/Q00/ouroboros
topic: harness
tags: [harness, claude-code, codex-cli, opencode, mcp, spec-driven, evolutionary-loop, socratic, double-diamond, ambiguity-gate, pal-router, korean-author, q00, ouroboros]
status: deep-dive
confidence: high
rounds: 4
axes_used: [1,2,3,4,5,6,7,8,9,10,11,12]
axes_added: [ambiguity_as_numeric_gate, deferred_tool_loading_protocol]
axes_dropped: []
candidate_axis_reuse:
  - A (iteration-boundary semantics) — 각 generation = evolve_step 1회, 상태는 EventStore로 재구성 (Ralph/GSD와 다른 매체)
  - C (mode splitting) — interview/seed/execute/evaluate/evolve/ralph/unstuck 7+모드, 각자 SKILL.md
  - D (gate mechanism syntax) — ambiguity ≤ 0.2 / similarity ≥ 0.95 / drift ≤ 0.3 — **숫자 임계값을 게이트 구문으로 사용**
  - G (execution environment as constraint surface) — PAL Router 3-tier 비용 제약 + MCP 서버 세션 격리
candidate_axis_proposals:
  - ambiguity_as_numeric_gate — 축 D의 자연스러운 서브타입: 진전 차단을 **숫자 임계값**(0.2/0.95/0.3)으로 표현
  - deferred_tool_loading_protocol — 스킬이 agent에게 "ToolSearch로 MCP 툴을 먼저 로드하라"고 명시 지시하는 패턴
notes: |
  Dispatched via WebFetch + WebSearch in 4 rounds (Agent-dispatch tool
  unavailable — Superpowers/GSD와 동일 precedent). All load-bearing claims
  cite primary README, CLAUDE.md, SKILL.md files (seed/evolve/evaluate/
  unstuck/ralph/interview/openclaw), PyPI ouroboros-ai metadata, releases page,
  GitHub issues tracker, and Q00 profile. Author disambiguated to Korean
  (Seoul, ZEP Tech Lead) in round 4. Ralph skill 안에 Huntley 레퍼런스는
  명시적으로 없음 — 이름만 따오고 의미론을 재정의함 (하네스 계보 표식).
---

## TL;DR (3줄)
Ouroboros는 Q00(한국, Seoul, ZEP Tech Lead)이 2026-01-14 공개한 **스펙 우선 진화 루프 엔진**으로, 사용자와 AI 코딩 런타임(Claude Code / Codex CLI / OpenCode) 사이에 MCP 서버로 끼어들어 `interview → seed → execute → evaluate → evolve` 5단계 사이클을 강제한다. 본질은 "코딩 실패는 아웃풋이 아니라 **인풋**에서 난다"는 진단 — 해법은 Socratic 면접으로 모호성을 **숫자(ambiguity ≤ 0.2, ontology similarity ≥ 0.95)** 까지 떨어뜨린 뒤에야 코드 생성을 허용하는 것. Ralph/GSD와 달리 상태를 파일이 아닌 **EventStore + MCP 서버**에 두고, Ralph의 이름을 `ooo ralph` 서브모드로 흡수해 "boulder never stops" 식 영속 루프로 재정의한 점이 계보적으로 가장 독특하다.

## 1. Identity & provenance
- **저자**: Q00 (GitHub: Q00, 본명/이메일: jqyu.lee@gmail.com, X: @JqOnly, LinkedIn: in/Q00)
  - **위치**: Seoul
  - **소속**: Tech Lead @ **@zep-us** (ZEP, 한국 메타버스 플랫폼)
  - **관심 리포**: `Glitch-Jar/LLM-EYES`, `Glitch-Jar/BabelGopher`, `agent-project`, `zep-us/zeude` (Claude Code 엔터프라이즈 모니터링), BMAD-METHOD 스타
  - **개인 웹사이트**: wpti.dev
- **레포 생성**: 2026-01-14 (`github.com/Q00/ouroboros`)
- **첫 tracked 릴리즈**: v0.26.6 (2026-03-30, TUI completion events + subprocess safety)
- **최신 버전**: v0.28.4 (2026-04-12 — PyPI `ouroboros-ai`)
- **인기**: ⭐ 2.3k / 🍴 220 (2026-04-13 기준)
- **라이선스**: MIT
- **Python >= 3.12**
- **설치**:
  ```
  curl -fsSL https://raw.githubusercontent.com/Q00/ouroboros/main/scripts/install.sh | bash
  ```
  또는 `pip install ouroboros-ai[claude|litellm|mcp|tui|all]`
- **지원 런타임**: Claude Code, Codex CLI, OpenCode (인스톨러 자동 감지 → MCP 서버 등록)
- **유지 상태**: 매우 활발. 18+ open issue, v0.27→v0.28 사이 MCP 브릿지·AC 트리·OpenClaw 등 대규모 아키텍처 진화.
- **마켓플레이스 존재감**: Lobehub에 "q00-ouroboros-welcome" 스킬 등재 확인.

### 동명 프로젝트 재확인 (canonical = Q00/ouroboros)
- `razzant/ouroboros` (2026-02-16, ⭐489) — 텔레그램 기반 self-modifying agent. **별개 계열, 이 노트의 대상 아님**.
- `joi-lab/ouroboros` — self-creating AI agent, 2026-02-16.
- `ShuoShenDe/OuroDev` — "loops endlessly through tasks" 유사 카피캣.
- `eLafo/ouroboros` — 무관.
- **본 노트의 대상**: Q00/ouroboros 2.3k stars (collected_facts 2026-04-13에서 확정).

## 2. Problem framing
Q00의 진단은 Huntley(프롬프트 완벽주의), Vincent(프로세스 디시플린 부재), TÂCHES(context rot) 와 **또 다른 각도**다 — **인풋의 모호성**.

> "Most AI coding fails at the **input**, not the output. The bottleneck is not AI capability -- it is human clarity." — README (primary source, WebFetch 2026-04-13, high confidence)

> "Stop prompting. Start specifying." — 슬로건 (README 헤더 + PyPI summary verbatim)

> "Before telling AI what to build, define what should be built. As Socrates asked 2,500 years ago — 'What do you truly know?' Ouroboros turns that question into an evolutionary AI workflow engine." — README (search snippet, high confidence)

> "Wonder → 'How should I live?' → 'What IS live?' → Ontology — Socrates" — README 철학 섹션 (verbatim, WebFetch)

**핵심 이동**: "프롬프트 엔지니어링" → "**스펙 엔지니어링**". 프롬프트를 잘 쓰는 것이 아니라, 프롬프트로 들어갈 명세 자체를 형식화·측정(ambiguity score) 해서 임계값 이하로 내린 다음에야 코드 생성을 허용.

**포지션 비교 (축 G 재사용)**:
- Ralph: 프로세스(작은 컨텍스트 카브오프 + 무한 루프)
- Superpowers: 프로세스 디시플린(SKILL.md + HARD-GATE)
- GSD: 실행 환경(프레시 컨텍스트 서브에이전트 + 웨이브 스케줄링)
- **Ouroboros**: **입력 공간**(모호성을 숫자로 재단 후에야 실행 진입) — 축 G에 추가 가능한 새 포지션 or 축 G의 "입력 측 변종".

## 3. Control architecture
**MCP 서버로 호스팅되는 페이즈 체인 + 진화 루프 하이브리드.** Anthropic 분류 기준으로 바깥층은 workflow(코드 경로로 고정된 5단계), 각 단계 내부는 agent(LLM 자율). GSD의 slash-command 체인과 Superpowers의 7-phase DAG 사이에 위치.

**5단계 evolutionary cycle** (README + skills/evolve/SKILL.md verbatim):
```
Gen 1: Interview → Seed(O₁) → Execute → Evaluate
Gen 2: Wonder → Reflect → Seed(O₂) → Execute → Evaluate
Gen 3: Wonder → Reflect → Seed(O₃) → Execute → Evaluate
...until ontology converges (similarity ≥ 0.95) or max 30 generations
```

> "Each cycle does not repeat -- it **evolves**." — README (search snippet)

**`ooo` 명령 표면** (CLAUDE.md + README verbatim):
| 명령 | 용도 | 비고 |
|---|---|---|
| `ooo setup` | 런타임 등록 + 프로젝트 설정 | MCP 서버 등록 |
| `ooo interview` | Socratic 질문으로 모호성 해소 | 3+ 라운드, ambiguity ≤ 0.2 |
| `ooo seed` | Interview 결과를 불변 스펙으로 crystallize | YAML, 저장 |
| `ooo run` | Double Diamond 분해 실행 | `ouroboros run seed.yaml` |
| `ooo evaluate` / `eval` | 3-stage 검증 | Mechanical → Semantic → Consensus |
| `ooo evolve` | 진화 루프 (최대 30 gen) | Wonder/Reflect 반복 |
| `ooo ralph` | Persistent 루프 until QA PASS | "The boulder never stops" |
| `ooo unstuck` / `stuck` / `lateral` | 5 lateral thinking persona | Hacker/Researcher/Simplifier/Architect/Contrarian |
| `ooo status` / `drift` | 세션 추적 + drift 감지 | drift ≤ 0.3 |
| `ooo qa` | QA 판정 | qa-judge agent |
| `ooo cancel` | 멈춘 실행 취소 | Issue #341 규제 |
| `ooo pm` | PM interview 모드 | DECIDE_LATER 지원 |
| `ooo publish` | 스펙 → GitHub Issues 변환 | v0.27.0 도입 |
| `ooo brownfield` | 기존 코드베이스 온보딩 | Issue #57 이후 추가 |
| `ooo openclaw` | Slack/Discord 릴레이 | ooo 접두 메시지 감지 |
| `ooo welcome` / `tutorial` / `help` / `update` | 부트스트랩/유지보수 | |

(소스: `skills/` 폴더 19개 디렉토리 직접 나열 — brownfield/cancel/evaluate/evolve/help/interview/openclaw/pm/publish/qa/ralph/run/seed/setup/status/tutorial/unstuck/update/welcome)

**evolve 상태 머신 (skills/evolve/SKILL.md verbatim, high confidence)**:
- `continue` → `ouroboros_evolve_step` 재호출
- `converged` → ontology similarity ≥ 0.95 → `ooo evaluate` 권유
- `stagnated` → 3+ gen 동안 ontology 불변 → `ooo unstuck` 권유
- `exhausted` → 30 gen 최대 → best result 표시
- `failed` → 오류 → `ooo status` 권유

**Termination**: 세 축 동시 가능 — 숫자 수렴 / 정체 감지 / 세대 예산.

## 4. State & context model
**가장 독특한 축.** Ralph(파일만), GSD(`.planning/*.md` 파일 + git + Pi SDK 세션), Superpowers(`docs/superpowers/specs/plans/*` + 서브에이전트 worktree)와 달리 Ouroboros의 권위적 상태 매체는 **EventStore + MCP 세션**이다.

| 매체 | 저장 내용 | 인용/근거 |
|---|---|---|
| **MCP 서버 세션** | interview Q&A 히스토리, ambiguity score, session_id | `skills/seed/SKILL.md`: "Check conversation for a recent `ouroboros_interview` session ID" |
| **EventStore** | 실행 이벤트, QA verdict, lineage 진화 | `skills/ralph/SKILL.md`: "Stores execution data in EventStore (not file I/O)" |
| **`ouroboros_query_events()`** | 이터레이션 히스토리 재구성 API | 동상 |
| **Seed YAML** | 불변 스펙 (GOAL / CONSTRAINTS / ACCEPTANCE_CRITERIA / ONTOLOGY_SCHEMA / EVALUATION_PRINCIPLES / EXIT_CONDITIONS / METADATA) | `skills/seed/SKILL.md` 전문 |
| **Lineage snapshot** | 각 generation이 rewind 가능한 스냅샷 | `skills/evolve/SKILL.md`: "Each generation is a snapshot. You can rewind to any generation and branch evolution from there" |
| **`~/.ouroboros/prefs.json`** | 운영자 preference (star_asked 등) | `skills/seed/SKILL.md` verbatim |
| **SKILL.md** | 명령 정의 + agent 로 지시 | `CLAUDE.md`: "Read the corresponding SKILL.md file ... Do NOT use the Skill tool — instead read with the Read tool and execute directly" |

**evolve_step의 스테이트리스성 (핵심 설계)**:
> "evolve_step: Runs exactly ONE generation per call. Designed for Ralph integration — state is fully reconstructed from events between calls" — `skills/evolve/SKILL.md` (verbatim)

이것이 Ralph 루프 친화적 설계의 원천이다. 매 gen 사이 컨텍스트가 (이론상) 카브오프 가능하고, MCP 서버가 상태를 보존한다. Ralph(Huntley)의 file-mediated memory 를 **event-mediated memory** 로 치환한 것.

**Seed 불변성 (축 D 재사용 — gate syntax)**:
> "Seed YAML specification ... GOAL / CONSTRAINTS / ACCEPTANCE_CRITERIA / ONTOLOGY_SCHEMA ... ambiguity_score: 0.15" — `skills/seed/SKILL.md`

Seed는 crystallize 이후 **immutable**. 재협상 필요 시 evolve의 Wonder/Reflect가 새 generation을 낳고, 각 gen이 자기 seed 를 생성 (이것이 "우로보로스가 자기 꼬리를 먹는다"의 기술적 의미).

## 5. Prompt strategy
Ouroboros의 프롬프트 전략은 **"스킬 = MCP 툴 바인딩 + 폴백 agent + 구조화 게이트"** 3각.

### SKILL.md 포맷 (verbatim from skills/seed/SKILL.md)
```yaml
---
name: seed
description: Generate validated Seed specifications from interview results
mcp_tool: ouroboros_generate_seed
mcp_args:
  session_id: $1
---
```

frontmatter 자체가 **MCP 툴 콜 시그니처**를 선언. Superpowers의 `allowed-tools:` 프리앰블과 비교되지만, Ouroboros는 한 걸음 더 나아가 "이 스킬은 이 MCP 툴의 래퍼"라고 명시.

### Deferred-tool loading protocol (신규 후보 축 제안)
모든 SKILL.md가 agent에게 **동일한 부트스트랩을 지시**한다:

> "The Ouroboros MCP tools are often registered as **deferred tools** that must be explicitly loaded before use. **You MUST perform this step before deciding between Path A and Path B.**
> 1. Use the `ToolSearch` tool to find and load the seed generation MCP tool: `ToolSearch query: \"+ouroboros seed\"`
> 2. The tool will typically be named `mcp__plugin_ouroboros_ouroboros__ouroboros_generate_seed` (with a plugin prefix). After ToolSearch returns, the tool becomes callable.
> 3. If ToolSearch finds the tool → proceed to **Path A**. If not → proceed to **Path B**.
> **IMPORTANT**: Do NOT skip this step. Do NOT assume MCP tools are unavailable just because they don't appear in your immediate tool list." — `skills/seed/SKILL.md` verbatim

**Path A (MCP) / Path B (plugin fallback)** 이중화가 모든 스킬에 대칭적으로 존재. 이는 Claude Code의 deferred-tool 시스템(런타임이 제공하는 툴을 필요 시 late-binding) 을 명시적으로 프롬프트 컨벤션으로 끌어올린 것. **신규 후보 축** 후보.

### 5 personas for lateral thinking (`skills/unstuck/SKILL.md` verbatim)
| 페르소나 | 모토 | 사용 시점 |
|---|---|---|
| **Hacker** | "Make it work first, elegance later" | Use when overthinking blocks progress |
| **Researcher** | "What information are we missing?" | Use when the problem is unclear |
| **Simplifier** | "Cut scope, return to MVP" | Use when complexity is overwhelming |
| **Architect** | "Restructure the approach entirely" | Use when the current design is wrong |
| **Contrarian** | "What if we're solving the wrong problem?" | Use when assumptions need challenging |

**트리거 키워드**: "I'm stuck" / "think sideways"
**폴백**: MCP 없으면 `ouroboros:contrarian` 등 agent 로 직접 위임.

### Dialectic Rhythm Guard (`skills/interview/SKILL.md` verbatim)
> "Track consecutive PATH 1/PATH 4 (code/research confirmation) answers. If 3 consecutive questions were answered via PATH 1 or PATH 4, the next question MUST be routed to PATH 2 (directly to user)"

**4-path routing for interview answers**:
- PATH 1: Code confirmation (Read/Glob/Grep)
- PATH 2: Direct user judgment
- PATH 3: Code + judgment
- PATH 4: Research interlude (WebFetch/WebSearch, v0.27.1 추가)

이 규칙은 **interview가 코드베이스 연구에 매몰되어 사람을 빼먹는 걸 방지**하는 backpressure. Ralph의 "1 writer vs 500 readers" 비대칭과 같은 계열의 rhythm control.

### Double Diamond (README verbatim, execute 단계의 내부 구조)
```
* Wonder              * Design
 \ (diverge)           \ (diverge)
  \ explore             \ create
   \                     \
    * ------------ *----- *
   /                     /
  / define              / deliver
 / (converge)          / (converge)
* Ontology            * Evaluation
```

**첫 diamond = Socratic (Wonder → Ontology)**, **둘째 diamond = Pragmatic (Design → Evaluation)**. 표준 UX Double Diamond 를 AI 개발 사이클에 이식한 것.

### 9 specialized agents (PyPI + CLAUDE.md)
`src/ouroboros/agents/`에 번들: **socratic-interviewer, ontologist, seed-architect, evaluator, qa-judge, contrarian, hacker, simplifier, researcher, architect**. (5 lateral personas + 4 core + evaluator 역할 중복 존재).

## 6. Tool surface & permission model
- **런타임**: Claude Code (기본) / Codex CLI / OpenCode / Gemini adapter (v0.27.1)
- **MCP 서버 등록**: 인스톨러 자동 감지, `~/.claude/mcp.json` 편집
- **MCP 전송**: stdio + HTTP/SSE (v0.28.3)
- **MCP 브릿지**: 서버-투-서버 통신 (v0.27.0) — Ouroboros MCP가 다른 MCP 서버를 호출 가능
- **PAL Router (cost gate, 축 G 강하게 재사용)**:
  - Frugal (1x) → Standard (10x) → Frontier (30x)
  - Auto-escalation on failure, auto-downgrade on success
  - Stage 3 Multi-Model Consensus는 Frontier tier 전용, "only triggered by uncertainty or manual request" (`skills/evaluate/SKILL.md` verbatim)
- **권한 모델**: YOLO 명시 없음. Claude Code 표준 툴 묶음 그대로 사용.
- **Subprocess lifecycle**: Claude CLI subprocess 관리 (Issue #269, #341 리그레션 기록) — v0.28.2 MCP crash prevention 보강

## 7. Human-in-the-loop points
**명시적 HITL이 Ouroboros의 설계 원칙이다** — Ralph의 "HITL은 세션 밖" 과 정반대.

- **Interview 단계**: 매 3 질문 중 최소 1개는 반드시 사람에게 직접 감 (Dialectic Rhythm Guard)
- **Star gate (seed 단계, 독특)**: `skills/seed/SKILL.md` verbatim —
  > "Your seed has been crystallized!"
  > → `AskUserQuestion` 툴로 "If Ouroboros helped clarify your thinking, a GitHub star supports continued development. Ready to unlock Full Mode?"
  > → 옵션: "⭐ Star & Setup" (`gh api -X PUT /user/starred/Q00/ouroboros`) or "Just Setup"
  > → `~/.ouroboros/prefs.json`에 `{"star_asked": true}` 저장

  **이것은 하네스 안에 내장된 growth-hacking 게이트**. Full Mode (run/evaluate/status) 잠금해제 조건으로 star를 요구. 하네스 노트 수집 중 처음 본 패턴 — 축으로 세우기엔 특수하지만 기록 가치.

- **unstuck 단계**: 사람이 "I'm stuck" / "think sideways" 트리거로 명시 호출
- **status / drift**: 사람이 세션 건강도 조회
- **pause-work / resume-work** (`skills/`에 미확인이지만 CLAUDE.md 매핑에 존재 암시)

## 8. Composability
- **런타임 이식성**: Claude Code + Codex CLI + OpenCode + Gemini adapter. 인스톨러 자동 감지 → MCP 등록.
- **플러그인 배포**: Claude 플러그인 마켓플레이스 대응 (`CLAUDE.md`: "End users install via the Claude plugin marketplace. Once installed as a plugin, skills and agents work natively without this file.")
- **MCP 브릿지**: 서버-투-서버 (v0.27.0) → 다른 MCP 툴 체인에 끼워넣기 가능
- **OpenClaw 통합**: Slack/Discord/기타 채널 릴레이. 스킬은 "Your only job is to be a relay" — 에이전트의 나머지 컨텍스트 격리.
- **Lobehub 배포**: "q00-ouroboros-welcome" 스킬로 외부 마켓플레이스 등재
- **Ralph 이름 흡수**: `ooo ralph` 서브모드가 Huntley 루프와 **이름만 공유**하고 의미는 MCP 이벤트 기반으로 재정의 — 호환이 아니라 **브랜드 흡수**. "Designed for Ralph integration" 주석이 호환성의 유일한 흔적.
- **v0.26.5 PM interview DECIDE_LATER**: PM 스킬은 의사결정 미결을 인지함 → 나중 라운드에서 재방문 (Ralph의 fix_plan.md와 평행선)

## 9. Empirical claims & evidence
**일화 + 메트릭 주장, 벤치마크 없음**.

### Q00 자신 주장 (README + PyPI verbatim)
- **"12 hidden assumptions exposed, ambiguity scored to 0.19"** — 한 번의 interview 사이클 예시 (WebFetch README 2026-04-13)
- **Rework rate "Low" vs vanilla AI coding** — 정성 비교 테이블 (README)
- **Socratic 효율 주장**: "What IS a task?" 같은 ontological 재질문이 "eliminates rework classes before code begins" (README)

### 3자 측정
- **없음 확인됨**. 검색 결과 재현/비평 블로그 포스트 없음. Ralph(Tessmann/Wang/Devon/beuke), Superpowers(Simon Willison, byteiota, heyuan110, Mak), GSD(codecentric, tentenco, DeepWiki) 대비 **3자 커버리지가 가장 얇음**.
- **Lobehub 등재**는 존재 확인되나 리뷰 아님.

### 구조적 주장 vs 실측
- Ambiguity 0.2 / similarity 0.95 / drift 0.3 같은 숫자는 **주장**이지 **측정**이 아니다. 이 스코어들이 어떤 알고리즘(embedding? LLM-as-judge?)으로 계산되는지는 MCP 서버 구현부에 있고 스킬 레이어에서는 불투명.
- "3-stage verification"의 Stage 1 Mechanical은 lint/build/test → 결정론적, 재현 가능. Stage 2/3는 모델 호출 → 재현성 낮음.

**평가**: 3개 먼저 분석한 하네스 중 Q00가 **가장 정량화 친화적 수사**를 쓰지만, **증거 부피는 가장 적다**. 활발한 개발 릴리즈 페이스가 증거를 대신함.

## 10. Failure modes & limits

### Open issues에서 확인된 저자 인지 한계 (primary source: github.com/Q00/ouroboros/issues 2026-04-13)
- **Issue #371** — "parallel session spawning causes 429 rate-limit cascade without a shared token bucket" (needs-design) → 병렬 세션 스폰 시 토큰 버킷 공유 안 됨
- **Issue #369** — "unbounded AC decomposition leads to runaway fractal nesting (e.g. ac_3000002 after 3 minutes)" (bug + needs-design) → Acceptance Criteria 트리가 무한 분해되어 3분 만에 300만 노드
- **Issue #341** — "Cancelled job leaves Claude CLI subprocess alive (regression of #269)" → 서브프로세스 누수
- **Issue #310** — "MCP server startup blocked by synchronous orphan session scan" → MCP 서버 시작 차단
- **Issue #305** — Claude Agent SDK failures in nested sessions → 중첩 세션 실패
- **Issue #351** — Phantom tool entries from inherited bridge tools → 툴 누출
- **Issue #346** — Non-blocking event emissions needed → EventStore 동기성 문제

### 내재적 한계 (구조 분석)
- **Ambiguity 점수의 블랙박스**: 임계값 0.2가 게이트 구문이지만 측정 방법은 코드 레이어. 스킬 사용자는 "왜 0.19인가"를 설명받지 못함.
- **Interview 피로도**: 3+ 라운드 강제 → 간단한 작업에 과한 obligation. v0.26.5의 DECIDE_LATER와 "Harden interview flow UX, auto-confirm, batch questions" (Issue #364) 가 이 압력의 증거.
- **Brownfield 약점**: Issue #57 "Interview should read codebase context before asking open questions" 가 v0.28.0의 `ooo brownfield` 스킬로 대응되었으나, 설계 원류는 greenfield.
- **3자 재현/리뷰 부재**: 생태계 검증이 얇음 — 주장 대 관찰 비율이 하네스 4개 중 가장 높음.
- **Ralph 흡수의 의미론 불일치**: "The boulder never stops" 는 Sisyphus 은유지 Ralph Wiggum 은유가 아님. 이름 재사용이 계보상 혼선 유발 가능.

### 저자 자기비판
- **직접 자기비판 텍스트 미수집**. Huntley("deterministically bad")나 Vincent(v5.0.6 inline rollback)처럼 명시적 회고 아직 공개되지 않음. 활발한 릴리즈 페이스가 암묵적 자기수정 메커니즘 역할.

## 11. Transferable primitives ★ (load-bearing)

각 항목: 이름 / 설명 / 전제 / standalone-extractable?

### P1. Ambiguity-as-gate (숫자 임계값으로 코드 생성 차단)
- 인풋 모호성을 숫자(≤ 0.2)로 스코어링해 임계값 미달이면 코드 생성 **차단**.
- 전제: 모호성 측정 함수가 존재(LLM-as-judge + 구조 분석), 운영자가 임계값 수용.
- **PARTIAL**. 원시요소(게이트 + 숫자)는 이식 가능. 측정 함수 품질은 이식 불가.

### P2. Immutable seed after crystallize
- Interview 결과는 YAML로 freeze. 변경은 새 generation 이라는 **다른 우주**에서.
- 전제: YAML 직렬화 가능한 요구사항 구조, evolve 경로 존재.
- **YES**. 계약 중심 설계.

### P3. Socratic interview with dialectic rhythm guard
- Socratic 질문, but 3연속 코드/리서치 확인이면 강제로 사람에게 질문 반환.
- 전제: 4-path routing 가능, interview session persistence.
- **YES**. 순수 프롬프트 레이어로 이식 가능.

### P4. Double Diamond twice (ontology + pragmatic)
- 첫 diamond는 Socratic(Wonder→Ontology), 둘째는 Pragmatic(Design→Evaluation).
- 전제: 모델이 2-phase discovery 유지, 전이 명시.
- **YES**. UX 유산의 직접 수입, 다른 하네스에서 미본 구조.

### P5. Evolutionary loop with 4-action state machine
- `continue / converged / stagnated / exhausted / failed` + 각각 다른 권장 다음 명령.
- 전제: similarity metric, stagnation 감지 로직, 세대 카운터.
- **PARTIAL**. 상태 머신은 이식 가능, 감지 로직은 런타임 의존.

### P6. Deferred-tool loading protocol in skill body
- 모든 SKILL.md가 agent에게 "ToolSearch로 MCP 툴을 먼저 로드하라" 명시 지시.
- 전제: Claude Code deferred tools 시스템 또는 유사 late-binding.
- **PARTIAL** (런타임 특이적). 하지만 **컨벤션 아이디어**(툴 부트스트랩을 스킬 본문에 박기)는 일반화 가능.

### P7. 5 lateral thinking personas as escape hatch
- Hacker / Researcher / Simplifier / Architect / Contrarian — stagnation 탈출용 persona injection.
- 전제: agent가 persona 채택 가능, 호출 트리거("I'm stuck").
- **YES**. 순수 프롬프트 primitive.

### P8. PAL Router 3-tier cost escalation
- Frugal (1x) → Standard (10x) → Frontier (30x), 실패 시 escalate / 성공 시 downgrade.
- 전제: 멀티 모델 backend, 실패/성공 판별 가능.
- **PARTIAL**. 다이얼 자체는 이식 가능, 구현은 LiteLLM 등 라우팅 레이어 의존.

### P9. MCP server as authoritative state medium
- 파일시스템 대신 MCP 서버 + EventStore가 권위적 상태. evolve_step은 stateless 호출, 상태는 이벤트 리플레이로 재구성.
- 전제: MCP 지원 런타임, 서버 프로세스 lifetime 관리.
- **PARTIAL**. 아키텍처 선택으로서 강력하지만 Ralph/GSD의 파일 기반 대안 대비 운영 복잡도 증가.

### P10. Path A/Path B skill duality (MCP preferred, agent fallback)
- 모든 스킬이 MCP 가용 시 Path A, 불가 시 에이전트 adoption Path B 를 명시.
- 전제: 대응 agent.md 파일이 `src/ouroboros/agents/`에 존재.
- **YES**. 컨벤션 primitive — "외부 툴 없을 때 self-contained fallback" 패턴.

### P11. Seed components as contract ontology
- GOAL / CONSTRAINTS / ACCEPTANCE_CRITERIA / ONTOLOGY_SCHEMA / EVALUATION_PRINCIPLES / EXIT_CONDITIONS / METADATA — 7-필드 YAML이 스펙 protocol.
- 전제: 운영자/agent/평가자가 같은 ontology 공유.
- **YES**. GSD의 `.planning/*.md` 세트, Superpowers의 `docs/superpowers/specs/design.md` 와 평행선.

### P12. Drift measurement as runtime check
- drift ≤ 0.3 (Goal 50% + Constraint 30% + Ontology 20%) — 세션 진행 중 원래 의도와의 거리를 수치 모니터링.
- 전제: 원본 seed 접근 + embedding 기반 거리 함수.
- **PARTIAL**. 개념은 강력, 계산 함수는 불투명.

### Rejected as primitive (중요)
- **Star gate ("star this repo to unlock Full Mode")**: growth-hacking 장치로서 사용자의 리서치 흐름에 끼워넣기 적절하지 않음. 하네스 설계 원리가 아니라 **distribution tactic**. 포팅 금지.
- **Ralph 이름 재사용**: `ooo ralph` 가 Huntley 의 file-mediated bash loop과 의미론적으로 무관 — 브랜드 혼선 소스. 이름을 그대로 가져오지 말 것.
- **30-generation hard cap**: 상한은 **safety control 이 아니라 cost cap**. Devon 의 Ralph 비판("max-iterations is not a safety control") 이 여기서도 적용.

## 12. Open questions
- **Ambiguity score 계산 함수 구체**: 스킬 레이어에서 불투명. `src/ouroboros/agents/` 및 MCP 서버 구현부 probing 필요 (follow-up probe).
- **Ontology similarity 0.95** 알고리즘: embedding cosine? LLM-as-judge? 확인 필요.
- **Drift 0.3 가중치**(Goal 50 + Constraint 30 + Ontology 20) 출처 검증.
- **한국어 커뮤니티 반응**: Q00 가 Seoul ZEP Tech Lead 임에도 한국어 블로그/YouTube 리뷰 검색에서 미노출. 한국어 직접 probe 대상.
- **razzant/ouroboros vs Q00/ouroboros 혼동 사례**: Dev 커뮤니티에서 어느 쪽을 "우로보로스"로 가리키는지 샘플링 필요 (razzant가 스타는 적지만 네이밍 혼란 원인).
- **CURSED/Ralph 스타일 long-run 기록**: Ouroboros로 그린필드 프로젝트 완성 사례 수집 안 됨.
- **"The boulder never stops" 출처**: Sisyphus 레퍼런스인지 Q00 독자 구절인지 미확인.
- **Claude Agent SDK 중첩 세션 실패 (Issue #305)** 영향 범위: Ouroboros + Superpowers 병용 시 MCP 중첩 문제 예상.

## Sources

### Primary (Q00 / Ouroboros)
- https://github.com/Q00/ouroboros — README, 2026-04-13 WebFetch
- https://github.com/Q00/ouroboros/blob/main/CLAUDE.md — 2026-04-13 WebFetch
- https://github.com/Q00/ouroboros/blob/main/skills/seed/SKILL.md — 2026-04-13 WebFetch (full verbatim)
- https://github.com/Q00/ouroboros/blob/main/skills/evolve/SKILL.md — 2026-04-13 WebFetch (full verbatim)
- https://github.com/Q00/ouroboros/blob/main/skills/evaluate/SKILL.md — 2026-04-13 WebFetch
- https://github.com/Q00/ouroboros/blob/main/skills/unstuck/SKILL.md — 2026-04-13 WebFetch (5 personas verbatim)
- https://github.com/Q00/ouroboros/blob/main/skills/ralph/SKILL.md — 2026-04-13 WebFetch ("The boulder never stops")
- https://github.com/Q00/ouroboros/blob/main/skills/interview/SKILL.md — 2026-04-13 WebFetch (4-path routing)
- https://github.com/Q00/ouroboros/blob/main/skills/openclaw/SKILL.md — 2026-04-13 WebFetch
- https://github.com/Q00/ouroboros/releases — v0.26.6 (2026-03-30) ~ v0.28.4 (2026-04-12)
- https://github.com/Q00/ouroboros/issues — #57, #269, #305, #310, #341, #346, #351, #364, #369, #371
- https://pypi.org/project/ouroboros-ai/ — v0.28.4, author email jqyu.lee@gmail.com
- https://github.com/Q00 — 프로필 (Seoul, ZEP Tech Lead, X: @JqOnly, in/Q00)
- https://lobehub.com/skills/q00-ouroboros-welcome — 외부 마켓플레이스 등재 증거

### Context (prior notes / schema)
- `meta/harness_schema.md` — v1 + candidate axes A–H
- `notes/harness/ralph-wiggum.md` — Huntley 계보 비교
- `notes/harness/superpowers.md` — SKILL.md 컨벤션 비교, HARD-GATE 대비
- `notes/harness/gsd.md` — context rot / 축 G 출처, artifact naming 축 H 대비
- `notes/harness/_collected_facts_2026-04-13.md` — Q00/ouroboros 판별 근거

### Disambiguation (not target, recorded for record)
- https://github.com/razzant/ouroboros — 별개 프로젝트
- https://github.com/joi-lab/ouroboros — 별개 프로젝트
- https://github.com/ShuoShenDe/OuroDev — 카피캣
