---
title: GSD (Get Shit Done)
date: 2026-04-13
author: Lex Christopherson (TÂCHES / @official_taches / glittercowboy)
first_public: 2026-02 (v1 Markdown-prompt era) → v2 TypeScript rewrite ~2026-03
primary_source: https://github.com/gsd-build/get-shit-done
topic: harness
tags: [harness, claude-code, multi-runtime, meta-prompting, spec-driven, context-engineering, taches, gsd, subagent, waves]
status: deep-dive
confidence: high
rounds: 4
axes_used: [1,2,3,4,5,6,7,8,9,10,11,12]
axes_added: [mode_splitting, iteration_boundary_semantics, gate_mechanism_syntax]
axes_dropped: []
candidate_axis_proposals: [execution_environment_as_constraint_surface, artifact_naming_schema_as_protocol]
notes: |
  Dispatched via WebFetch + WebSearch in 4 rounds (Agent dispatch tool
  was not reintroduced; same pattern as Superpowers analysis). All
  load-bearing claims cite primary README, official docs, creator's
  X/Twitter posts, and tentenco/codecentric/dev.to secondaries. The
  user's hint "by jasonkneen" was wrong and disambiguated on Round 1:
  canonical GSD is by Lex Christopherson (TÂCHES), originally hosted
  at glittercowboy/get-shit-done, later moved to gsd-build org, with
  a v2 TypeScript rewrite at gsd-build/gsd-2.
---

## TL;DR (3줄)
GSD는 Lex Christopherson(TÂCHES)이 만든 Claude Code용 **메타프롬프팅 + 스펙 주도 + 컨텍스트 엔지니어링** 하네스로, `/gsd:discuss-phase → /gsd:plan-phase → /gsd:execute-phase → /gsd:verify-work → /gsd:ship` 슬래시 명령 체인과 `.planning/` 디렉토리의 파일 기반 상태(`PROJECT.md` · `REQUIREMENTS.md` · `ROADMAP.md` · `STATE.md`)로 **context rot**(컨텍스트 포화시 품질 붕괴)를 해결한다. 본질은 "매 태스크를 프레시 200K 서브에이전트 컨텍스트로 카브오프(carve-off)하는 것"이며, 이 때문에 tentenco는 "GSD는 **실행 환경**을 제약한다"라고 요약한다(Superpowers=프로세스, gstack=시점). 현재 v1(Markdown prompts, 35k+ stars)에서 **v2 TypeScript/Pi SDK CLI rewrite**(gsd-build/gsd-2, 5.6k stars)로 아키텍처 전환 중인 것이 가장 큰 설계 긴장 지점.

## Disambiguation (중요)
사용자 힌트 "by jasonkneen"은 **오류**. 1라운드 WebSearch로 확인:
- 정식 저자: **Lex Christopherson** (aka glittercowboy, aka TÂCHES / @official_taches)
- 최초 레포: `github.com/glittercowboy/get-shit-done` — dev.to ccforeveryone 강의 및 이슈 #50이 이 경로를 원본으로 지목
- 현 주력 레포: `github.com/gsd-build/get-shit-done` — README 끝에 "— **TÂCHES**" 저자 서명
- v2 CLI rewrite: `github.com/gsd-build/gsd-2`
- 공식 랜딩: `gsd.build` (by @official_taches)

> "GSD (Get Shit Done) was built by Lex Christopherson, who goes by TÂCHES." — Ewan Mak (tentenco), Medium 2026-04

> "A month ago, I launched GSD. 8.5k+ GitHub stars later, it's become the #1 Claude Code framework for vibe coding successfully. The problem was simple: Claude is brilliant, but without structure it drifts. Context rots. Sessions become ping-pong hell." — Lex Christopherson (@official_taches), X 2026 (tweet 2016562506819342639, fetched via search snippet — full text behind login, **medium confidence on exact wording**)

jasonkneen은 별개 인물(다른 Claude Code 생태계 기여자) — 이 하네스와 연관 증거 없음.

## 1. Identity & provenance
- **저자**: Lex Christopherson (TÂCHES, @official_taches, glittercowboy) — "I'm a solo developer. I don't write code — Claude Code does." (README 철학 섹션, fetched 2026-04)
- **조직**: `gsd-build` GitHub org (원본 `glittercowboy/get-shit-done` → `gsd-build/get-shit-done`로 이전)
- **첫 공개**: 2026-02 경 (tentenco X 트윗 "A month ago, I launched GSD"에서 역산, v1.28 릴리즈 2026-03-22 확인)
- **현재 버전**: v1.34.0 (README 기준, 2026-04 fetch)
- **라이선스**: MIT
- **인기**:
  - **51.7k stars / 4.3k forks** (gsd-build/get-shit-done README, 2026-04 fetch)
  - codecentric 2026-03-03 기준 23k → 한 달 만에 2배 이상 성장
  - tentenco 2026-04 기준 "roughly 35,000 GitHub stars" (구버전 스냅샷일 가능성)
  - `gsd-build/gsd-2` (v2 rewrite): 5.6k stars / 589 forks
- **지원 런타임**: "Claude Code, OpenCode, Gemini CLI, Kilo, Codex, Copilot, Cursor, Windsurf, Antigravity, Augment, Trae, Qwen Code, Cline, and CodeBuddy" (README opening 문자 그대로)
- **배포 방식**: `npx get-shit-done-cc@latest` (README)
- **유지 상태**: 매우 활발 — 3주 만에 v1.28→v1.34, 대량 이슈/PR, v2 병행 개발, Claude Code 버전 업데이트마다 호환성 픽스 추적 (이슈 #218, #1504, #1528)

> "A light-weight and powerful meta-prompting, context engineering and spec-driven development system for Claude Code, OpenCode, Gemini CLI, Kilo, Codex, Copilot, Cursor, Windsurf, Antigravity, Augment, Trae, Qwen Code, Cline, and CodeBuddy." — README

## 2. Problem framing
TÂCHES의 진단은 **컨텍스트 로트(context rot)** 단일 주제에 집중:

> "Solves context rot — the quality degradation that happens as Claude fills its context window." — README

> "0-30% context: Peak quality / 50%+: Starts rushing. 'I'll be more concise.' Cuts corners / 70%+: Hallucinations. Forgotten requirements. Drift." — ccforeveryone 2026 강의 (CC BY-NC-ND, "GSD by Lex Christopherson" 명시)

Vincent(Superpowers)는 "프로세스 디시플린 부재"를, Huntley(Ralph)는 "완벽한 프롬프트 집착"을 적으로 지목한 반면, TÂCHES는 오로지 **토큰 윈도 포화**를 적으로 지목한다. 해법은 같지 않다 — "프레시 컨텍스트로 쪼개라." Ewan Mak(tentenco, 2026-04)이 **"GSD constrains the execution environment"** / **"GSD ensures environmental quality"** 로 요약한 축이 이것.

철학적 카운터-포지션:

> "Other spec-driven development tools exist...but they all seem to make things way more complicated than they need to be (sprint ceremonies, story points, stakeholder syncs, retrospectives, Jira workflows)." — README

> "The complexity is in the system, not in your workflow. Behind the scenes: context engineering, XML prompt formatting, subagent orchestration, state management. What you see: a few commands that just work." — README

> "Vibecoding has a bad reputation...GSD fixes that. It's the context engineering layer that makes Claude Code reliable." — README

## 3. Control architecture
**페이즈 체인 워크플로 + 페이즈-내부 에이전트 + 웨이브 병렬화.** Anthropic 분류(workflows vs agents)로 하이브리드지만 무게중심은 **workflow** 쪽 — 페이즈 순서는 하드코딩된 code path, 페이즈 내부에서만 LLM 자율.

**5단계 (+ 보조 단계) 체인** (README, DeepWiki 교차 확인):
1. `/gsd:new-project` — Interview → Research → Requirements → Roadmap
2. `/gsd:discuss-phase N` — "Surface gray areas, capture decisions in N-CONTEXT.md"
3. `/gsd:plan-phase N` — "Research and create N-0.X-PLAN.md files"
4. `/gsd:execute-phase N` — "Run plans in waves with atomic commits"
5. `/gsd:verify-work N` — "Goal-backward verification and UAT"
6. `/gsd:ship [N]` — "Create rich PR from phase artifacts"
7. `/gsd:complete-milestone` — "Archive milestone and tag release"

**보조 명령** (README + DeepWiki):
- `/gsd:help`, `/gsd:map-codebase` (brownfield 대응), `/gsd:new-milestone`, `/gsd:quick` (fast path, no full plan), `/gsd:next` (auto-detect next step), `/gsd:settings`, `/gsd:manager` (interactive dashboard), `/gsd:update`, `/gsd:reapply-patches`, `/gsd:health`, `/gsd:autonomous` (headless SDK execution), `/gsd:debug`, `/gsd:pause-work`, `/gsd:resume-work`, `/gsd:set-profile budget`

**Thin orchestrator 패턴** (DeepWiki):
```
Slash Command → Workflow .md → Specialized Agent (gsd-planner / gsd-executor / gsd-verifier / gsd-phase-researcher / gsd-plan-checker) → gsd-tools.cjs (deterministic ops) → .planning/*.md + git
```

> "GSD solves this pragmatically by recording everything in files within the `.planning/` directory ... This follows an important design principle: **Deterministic logic belongs in code, not in prompts.**" — Felix Abele, codecentric.de 2026-03-03

> "The GSD workflow is divided into a chain of slash commands. Each command handles a phase—and ideally, each phase runs in a fresh context window." — codecentric.de

**종료 조건**: 한 페이즈는 verify 게이트 통과 또는 사용자 accept-with-caveats/rollback 결정 시 종료. 전체는 `/gsd:complete-milestone`로 마감.

**웨이브 병렬** (DeepWiki, ccforeveryone, 알리카즈미 dev.to 삼중 확인):

> "Plans are grouped into 'waves' based on dependencies. Within each wave, plans run in parallel. Waves run sequentially." — README
> "Wave 1 might run three plans simultaneously. Wave 2 waits for Wave 1, then runs." — ccforeveryone

토글: `.planning/config.json`의 `parallelization: true/false` (DeepWiki).

## 4. State & context model ★
**GSD의 심장.** Ralph는 파일 기반이지만 프롬프트 1개에 의존, Superpowers는 스킬 기반이지만 한 세션에서 페이즈 전환, GSD는 **스펙/플랜/서머리/검증을 `.planning/` 아래 structured artifact로 분해**하고 각 페이즈가 **Task() 툴로 독립 서브에이전트를 스폰**해서 **200K 프레시 컨텍스트**를 새로 받는다.

`.planning/` 레이아웃 (codecentric 1차 + DeepWiki 상세):

```
.planning/
├── PROJECT.md                    # Vision, tech stack, constraints
├── REQUIREMENTS.md               # Feature traceability matrix (IDs)
├── ROADMAP.md                    # Phase definitions + success criteria
├── STATE.md                      # Current session, decisions, progress
├── config.json                   # Workflow toggles, model profiles, git strategy
│
├── 1-CONTEXT.md                  # Phase 1: discuss 산출 사용자 결정
├── 1-RESEARCH.md                 # Phase 1: 도메인 조사
├── 1-0.1-PLAN.md / 1-0.1-SUMMARY.md   # Wave 1: plan/exec 페어
├── 1-0.2-PLAN.md / 1-0.2-SUMMARY.md   # Wave 2: ...
├── 1-VERIFICATION.md             # Phase 1: UAT / gaps
│
├── 2-CONTEXT.md / 2-RESEARCH.md / ...
│
└── gsd-local-patches/            # 업데이트 시 사용자 수정 백업
```

**아티팩트 네이밍 규약**: `{PHASE}-{WAVE}-{TYPE}.md` — 예: `1-0.2-PLAN.md`는 Phase 1 / Wave 0.2 / PLAN 아티팩트. 모든 파일은 YAML frontmatter(`status`, `phase`, `author`, `timestamp`) 보유. 이 **명명 스키마 자체가 에이전트-툴-사람 간 프로토콜**로 기능한다 (아래 schema candidate G 참조).

> "`PROJECT.md`: What are we building and why. `config.json`: Workflow settings. `REQUIREMENTS.md`: Exactly what, with IDs. `ROADMAP.md`: In what order. `STATE.md`: Where we are right now." — codecentric.de (verbatim)

**서브에이전트 스폰 메커닉** (DeepWiki):
- 각 페이즈 워크플로는 `Task(subagent_type: gsd-executor)` 등으로 새 에이전트 프로세스를 띄움
- 각 스폰이 **신선한 200k+ 토큰 컨텍스트**를 받음
- 스폰된 에이전트는 `N-M-PLAN.md`만 읽고 `N-M-SUMMARY.md`만 씀
- 오케스트레이터 세션은 서머리만 읽음 → "30-40% context usage" 유지

> "each executed in a fresh 200K-token context window ... Sessions remain lean at 30-40% context usage" — dev.to 알리카즈미 (v1 동작 묘사)

> "It breaks work into atomic tasks. Each task gets a fresh Claude instance with a clean 200K token context window." — tentenco, Medium 2026-04

**다음 턴에 모델이 보는 것**: 오케스트레이터 세션은 `STATE.md` + 직전 페이즈 `N-VERIFICATION.md` + 해당 페이즈 `N-CONTEXT.md`. 스폰된 executor는 `N-M-PLAN.md` + REQUIREMENTS.md 슬라이스 + git worktree 상태. **오케스트레이터는 구현 디테일을 절대 보지 않음.**

**반사실(counterfactual) 감수성**: `ccforeveryone.com`의 "0-30% peak / 50% rushing / 70% hallucination" 주장은 **커뮤니티 관찰**이지 통제된 벤치마크가 아님 — medium confidence.

**Ralph 대비**: Ralph는 `while true` 외곽 루프로 프레시를 얻음. GSD는 루프 없이 `Task()` 스폰으로 프레시를 얻음. 둘 다 "파일 매개 기억 + 프레시 컨텍스트"지만 **프레시를 만드는 축이 시간(Ralph)이냐 공간(GSD, 서브에이전트 분기)이냐**가 갈린다.

## 5. Prompt strategy
- **메타프롬프팅 레이어**: 슬래시 명령 각각이 독립 워크플로 .md 파일. 프롬프트가 아니라 **에이전트에게 읽힐 절차**로 설계.
- **모드 스플리팅** (Ralph의 plan/build와 유사, 그러나 5-way로 분화): discuss / plan / execute / verify / ship. 각 모드는 다른 툴셋 + 다른 에이전트 타입 + 다른 산출 아티팩트.
- **XML 프롬프트 포맷**: README 스스로 명시 — "Behind the scenes: ... XML prompt formatting, subagent orchestration, state management."
- **Fast path**: `/gsd:quick "Add dark mode"` — 전체 파이프라인 우회, 리서치 옵션(`--discuss --research --full`) 단계적 추가 가능 (dev.to 알리카즈미).
- **Budget profile**: `/gsd:set-profile budget` — 모델/토큰 정책 프로파일 전환 (DeepWiki).
- **Deterministic logic split**: "Deterministic logic belongs in code, not in prompts" 원칙에 따라 번호 파싱·git 커밋·phase 전이 등은 `gsd-tools.cjs` Node 유틸로 밀어냄 (codecentric).

## 6. Tool surface & permission model
- **명시적 allow-list**: README 설치 시 `~/.claude/settings.json`에 `permissions.allow` 배열을 기입. codecentric에서 포착한 워크플로 프론트매터:
  ```
  allowed-tools: [Read, Bash, Write, Task, AskUserQuestion]
  ```
- **Ralph의 YOLO 안티패턴**: GSD는 `--dangerously-skip-permissions`를 **강제하지 않음**. 대신 명시적 allow-list로 도구를 좁힘. 이는 "execution environment 제약" 포지션과 일관.
- **핵심 툴**: `Task` (서브에이전트 스폰), `AskUserQuestion` (HITL), `Bash`(git·npm·test), `Read/Write` (.planning/*).
- **hooks**: Claude Code 런타임 hooks 사용 — `gsd-statusline.js` (UI 상태바 표시), `gsd-executor-hook.js` (실행 감시). `~/.claude/settings.json` 의 `"hooks"` 배열에 등록. (DeepWiki)
- **v2 노선**: gsd-build/gsd-2는 Anthropic **Pi SDK**로 TypeScript 레벨 에이전트 하네스 직접 제어 — "clear context between tasks, inject exactly the right files at dispatch time, manage git branches, track cost and tokens, detect stuck loops, recover from crashes, and auto-advance through an entire milestone" (gsd-2 README).

## 7. Human-in-the-loop points
**GSD는 HITL을 1급 시민으로 다룬다.** Ralph(세션 밖 HITL) / Superpowers(HARD-GATE 차단) 양 극단의 중간.

- **`AskUserQuestion` 툴**: 페이즈 내 결정 지점에서 Claude Code의 구조화 질문 툴을 호출. codecentric 인용:
  > "GSD frequently uses a mix of automation and targeted decision points, utilizing the `AskUserQuestion` tool."
  > "Roadmap Approval — 'Does the roadmap look right?' (approve/adjust/view file)"
- **Discuss phase 자체가 HITL**: `/gsd:discuss-phase`의 목적은 "gray area 수면 위로 올려서 사용자 결정 캡처"→ `N-CONTEXT.md`. 사실상 **구조화된 인터뷰 루프**.
- **Verify phase UAT**: `/gsd:verify-work`는 "goal-backward QA walkthrough"로 사용자가 각 요구사항을 함께 걸으며 pass/fail 표시 (DeepWiki / ccforeveryone).
- **Manual ship decision**: `/gsd:ship`은 사용자 명시적 호출 — 자동 머지 아님.
- **실패 모드**: v1.21→1.22 업데이트에서 "**All questions are auto-answered**" 회귀 버그(GH 이슈 #803). HITL 의존성의 취약 지점 — 질문 다이얼로그가 고장나면 전체 워크플로가 쓰레기를 자동 승인.

## 8. Composability
- **멀티 런타임 이식성**: 단일 코드베이스 → 14개 런타임 (README). tentenco의 다른 인용: "Build for Claude Code and simply update all the files at install for the other platforms." (Lex X, 2028458980968652884).
- **기존 CLAUDE.md와 충돌**: 이슈 #50 — "GSD doesn't add its methodology rules to existing project CLAUDE.md files" → 기존 프로젝트에 얹을 때 방법론 주입이 자동화되지 않음.
- **Superpowers/gstack와 스택 가능** (tentenco 2026-04):
  > "_gstack handles thinking, Superpowers handles doing, GSD keeps long context honest._"
  > "Once the decision is made, use GSD (v2) to anchor the plan: `PROJECT.md` for what the project is, `DECISIONS.md` for architectural choices, `KNOWLEDGE.md` for cross-session rules and patterns, and milestone roadmaps (`M001-ROADMAP.md`) for sliced execution."
- **Universal router 등장**: `claude-jarvis` (UpayanGhosh/claude-jarvis) — "Universal intent router — picks the best skill from GSD, Superpowers, and gstack automatically." GSD가 스택의 **context/spec 레이어**로 자리 잡았다는 독립 증거.
- **단독 사용의 약점**: "**GSD — little standalone 'shipping' value.** ... if you use it **alone**, it does not directly produce code, run tests, or open a PR." (tentenco 2026-04) — 실제로는 본 분석의 실행 페이즈가 코드를 쓰긴 하지만, 저자 평가는 **context anchor로서의 가치가 shipping보다 크다**는 것.

## 9. Empirical claims & evidence
- **저자 주장** (X, README, 1차):
  - "#1 Claude Code framework for vibe coding successfully" (Lex X 2016562506819342639, medium confidence on exact wording)
  - "trusted by engineers at Amazon, Google, Shopify, and Webflow" (tentenco 인용)
  - 11,900 ratings / 4.9 average rating (gsd.build 랜딩 메타데이터, 플랫폼 불특정)
  - 51.7k stars / 4.3k forks (2026-04 README fetch) — Superpowers 94k 다음 2위 규모
- **3자 측정/일화**:
  - chardet/Superpowers 급의 대표 벤치마크는 없음. 주로 "vibe check" 일화.
  - codecentric(Felix Abele, 2026-03-03): "currently among the most well-known Spec-Driven Development tools" — 정성 평가.
  - dev.to 알리카즈미: "4:1 token overhead ratio" — 플랜+리서치+검증 오버헤드 추정. 방법론 불명.
- **증거 유형**: 주로 **README 자기주장 + 소셜 증거(stars) + 블로그 일화**. 통제된 벤치마크 부재.

## 10. Failure modes & limits

### 저자/설계 자인
- **"Not for tiny tasks"** — `/gsd:quick` 우회로를 제공하지만, 풀 파이프라인은 오버킬 (dev.to 알리카즈미).
- **토큰 비용**: Claude Pro ($20/mo) 부족, **Max ($100–200/mo) 권장** (dev.to) — 4:1 플래닝 오버헤드.
- **Brownfield 한계**: `/gsd:map-codebase`로 대응하지만 기존 CLAUDE.md 자동 통합 실패 (이슈 #50).

### 관찰/보고된 버그
- **Claude Code 2.1.88+ 호환 붕괴** (이슈 #218, #1504, #1528): 2026-03~04 Claude Code가 스킬 디스커버리를 `~/.claude/commands/` → `~/.claude/skills/*/SKILL.md`로 이동하면서 **모든 `/gsd:*` 명령이 "Unknown skill"로 실종**. GSD는 commands/ 서브디렉토리 배치이기 때문. 런타임 버전 커플링이 취약함.
- **auto-answer 회귀 (v1.22)** (이슈 #803): `/gsd:discuss-phase` 및 `/gsd:settings`의 질문들이 모두 자동응답 — HITL 채널이 고장나자 워크플로가 쓰레기를 승인.
- **`--auto` 잘못 구현** (이슈 #780): 서브에이전트들이 페이즈 핸드오프를 따르지 않고 **모든 페이즈를 자기 자신이 수행** → "fresh context와 compaction 보호라는 에이전트 아키텍처의 목적을 무력화." 이것은 **치명적** — GSD의 핵심 약속(프레시 컨텍스트)이 깨짐.

### 구조적 제약
- **Standalone shipping 약함** (tentenco): "does not directly produce code, run tests, or open a PR" — 단독으로는 context anchor 역할만.
- **Ask-cost oscillation**: discuss phase가 사용자에게 너무 많이 물어보면 피로, 너무 적으면 gray area 누락. 문서화된 해결책 없음.
- **v1→v2 아키텍처 균열**: 프롬프트 레이어(v1, Markdown)는 "LLM이 읽고 협조"에 의존, v2는 Pi SDK로 TypeScript 직접 제어. 커뮤니티는 v1에 표준화돼 있고, v2는 5.6k stars로 아직 과도기. 두 흐름 모두 활발.

> "v2 controls the agent session at the TypeScript level — clearing context, injecting files, managing git branches, tracking costs and tokens, detecting stuck loops, and recovering from crashes." — tentenco 2026-04 (v2 설계 요지)

- **`--dangerously-skip-permissions` 재도입 리스크**: GSD는 거부하지만, 사용자가 자동화를 극대화하려 할 때 복귀 유혹 상존 (일반 패턴).

## 11. Transferable primitives ★ (load-bearing)

각 항목: 이름 / 설명 / 전제 컨텍스트 / standalone-extractable?

### G1. `.planning/` 구조화 스펙 디렉토리 (PROJECT / REQUIREMENTS / ROADMAP / STATE / CONTEXT / RESEARCH / PLAN / SUMMARY / VERIFICATION)
- 스펙·진행·결정을 7+ 종류 파일로 **역할별 분해**. 각 파일은 단일 책임. `STATE.md`는 "지금 우리가 어디에 있는가"만.
- 전제: 파일 r/w + 에이전트가 파일명 규약 존중.
- **YES**. Ralph의 "플랜 파일 1개 + AGENTS.md 1개" 모델을 일반화한 형태.

### G2. `{PHASE}-{WAVE}-{TYPE}.md` 아티팩트 네이밍 프로토콜
- 파일명 자체가 페이즈/웨이브/단계(PLAN vs SUMMARY vs VERIFICATION)를 인코딩. 사람·에이전트·툴 모두 같은 스키마 해석.
- 전제: 번호 기반 계획, 안정적 파일 시스템.
- **YES**. 컴팩트한 프로토콜. 이식 시 "프로세스의 이벤트 로그를 파일명에 직접 쓴다"로 일반화.

### G3. 페이즈 분리 = 모드 분리 (5-way: discuss / plan / execute / verify / ship)
- Ralph의 2-way(plan/build), Superpowers의 7-phase DAG와 같은 계열 프리미티브지만 discuss(HITL) + verify(UAT)를 1급으로 승격한 점이 차별화.
- 전제: 각 모드가 다른 에이전트/툴셋/아티팩트 가질 수 있는 런타임.
- **YES**. 슬래시 명령이 없더라도 프롬프트 템플릿 세트로 이식 가능.

### G4. Task() 기반 프레시 200K 컨텍스트 카브오프 (오케스트레이터 lean 30-40%)
- 오케스트레이터는 서머리만 보고, 서브에이전트는 PLAN 하나만 본다. "Carve off small independent context windows" 멘탈 모델(Dex가 Ralph 리프레이밍했던 바로 그것)의 **서브에이전트 버전 구현**.
- 전제: 서브에이전트 스폰 API + 각 스폰에 독립 컨텍스트 할당.
- **YES** — Ralph의 P10 카브오프와 독립적인 두 번째 사례. 프리미티브로 확고.

### G5. 웨이브 병렬 + 의존성 그래프 (parallelization toggle)
- 한 페이즈 안에서 독립 태스크 N개를 동시 실행, 의존 태스크는 뒤 웨이브로 미룸. `parallelization: true/false` 플래그로 끌 수 있음.
- 전제: 병렬 서브에이전트 런타임, 플랜이 의존성 필드 가짐.
- **YES**.

### G6. Deterministic logic는 code, not prompts (`gsd-tools.cjs`)
- 번호 파싱·git 커밋·phase 전이 같은 **결정론적 연산을 LLM에서 빼내 Node 유틸로 밀어냄**. LLM은 판단만.
- 전제: 호스트 런타임에서 도구 실행 가능.
- **YES** — 강력한 일반 원칙. Ralph의 "bash safety net for git commit"(Tessmann)과 같은 계열.

### G7. HITL as 1급: `AskUserQuestion` + discuss-phase 구조화 인터뷰
- 사용자 결정을 "프리텍스트에 끼어넣기" 대신 **구조화 질문 툴**로 수거 → `N-CONTEXT.md`에 고정.
- 전제: Claude Code류 구조화 질문 툴.
- **PARTIAL** — 툴 의존, 다른 런타임은 어댑터 필요.

### G8. 페이즈별 명시적 allow-list (`allowed-tools:` frontmatter)
- 각 워크플로 파일이 프론트매터로 `allowed-tools: [Read, Bash, Write, Task, AskUserQuestion]` 선언. Ralph의 YOLO 정반대.
- 전제: 프론트매터 지원 슬래시 명령 런타임.
- **YES**. 페이즈별 권한 축소는 범용 원칙.

### G9. Fast path + Full path 이중 제공 (`/gsd:quick` vs 풀 파이프라인)
- 작은 태스크에는 escape hatch, 큰 태스크에는 풀 파이프라인. 프레임워크 오버킬 비판에 대한 **구조화된 답변**.
- 전제: 동일 상태 파일을 둘 다 존중.
- **YES**.

### G10. Brownfield mapper + 로드맵 생성 전처리 (`/gsd:map-codebase`)
- 기존 코드베이스 위에 GSD를 얹을 때 먼저 전용 스캔 단계를 거쳐 코드베이스 지도를 만든다. Ralph가 "그린필드 전용"인 것과 대비.
- 전제: 코드베이스 스캔 도구.
- **YES**.

### G11. 게이트 택소노미 (schema drift / security / scope reduction)
- README v1.34 하이라이트: "schema drift detection flags ORM changes missing migrations, security enforcement anchors verification to threat models, and scope reduction detection prevents the planner from silently dropping your requirements."
- 전제: 각 게이트를 실행할 도메인 검증 로직.
- **PARTIAL** — 구체 게이트는 도메인 의존이지만, "카테고리화된 게이트 테이블" 메타 원칙은 이식 가능.

### G12. Verify-then-Ship 분리 (goal-backward UAT → 별도 PR 커맨드)
- "구현 끝 ≠ 출하 가능." `verify-work`가 요구사항 기준 역방향 체크리스트를 돌린 뒤에만 `ship`이 PR을 연다. 실패 → rework / accept-with-caveats / rollback 3지 선택지.
- 전제: 요구사항 트레이서빌리티 매트릭스, git branch 전략.
- **YES**.

### Rejected as primitive
- **v1 Markdown 프롬프트 주입 방식**: 저자 자신이 "fighting the tool — injecting prompts through slash commands, hoping the LLM would follow instructions" (tentenco 인용한 v1 자기비판)라며 v2로 갈아엎는 중. 프레시 컨텍스트와 분해 모델은 이식하되, "Markdown-as-prompt-injection" 자체는 v2에서 저자가 부정한 패턴이므로 프리미티브 후보에서 제외.
- **auto-answer 기반 자동화**: 이슈 #803/#780이 보여주듯, HITL 채널을 꺼서 완전 자율화하면 GSD의 핵심 안전장치가 사라진다. 포팅 금지.

## 12. Open questions
- `gsd-build/gsd-2` Pi SDK 구체 동작 — README 레벨 이상 읽기 못 함 (파일 트리 probe 필요)
- v1 → v2 마이그레이션 경로 공식 가이드 유무
- Lex X 트윗 2016562506819342639 원문(로그인 월 뒤) — 날짜·스타 수 정확 수치는 search snippet에 의존
- "trusted by engineers at Amazon/Google/Shopify/Webflow" 주장의 1차 출처
- `gsd.build` 랜딩 "11,900 ratings / 4.9" 의 플랫폼 정체 (App Store? G2? 자체?)
- GSD × Superpowers 실제 스택 사례의 정량 결과
- 4:1 토큰 오버헤드 주장의 측정 방법론
- 한국어 커뮤니티 재현 사례 (현재 probe로는 발견 못 함)

## Sources

### Primary
- https://github.com/gsd-build/get-shit-done — 본 레포 (README v1.34 fetch 2026-04-13)
- https://github.com/gsd-build/gsd-2 — v2 TypeScript/Pi SDK CLI rewrite
- https://github.com/glittercowboy/get-shit-done — 원본 레포(이전됨, 강의/이슈에서 참조)
- https://gsd.build/ — 공식 랜딩
- https://gsd-build-get-shit-done.mintlify.app/ — 공식 Mintlify 문서
- https://deepwiki.com/gsd-build/get-shit-done — DeepWiki 구조 인덱스
- https://x.com/official_taches/status/2016562506819342639 — "A month ago, I launched GSD" (snippet)
- https://x.com/official_taches/status/2028458980968652884 — 멀티 런타임 빌드 방식
- https://x.com/official_taches/status/2019906311991787646 — v2 IDE/CLI/TUI 전환 언급
- https://x.com/official_taches/status/2020143037339316517 — TypeScript 툴로 토큰 절감

### Secondary (분석/해설)
- https://medium.com/@tentenco/superpowers-gsd-and-gstack-what-each-claude-code-framework-actually-constrains-12a1560960ad — Ewan Mak, 2026-04, "GSD constrains the execution environment"
- https://agentnativedev.medium.com/get-sh-t-done-meta-prompting-and-spec-driven-development-for-claude-code-and-codex-d1cde082e103 — Agent Native, 2026-02-23 (paywall, 미리보기만 수집)
- https://www.codecentric.de/en/knowledge-hub/blog/the-anatomy-of-claude-code-workflows-turning-slash-commands-into-an-ai-development-system — Felix Abele, 2026-03-03, `.planning/` 구조와 deterministic-logic 원칙
- https://dev.to/alikazmidev/the-complete-beginners-guide-to-gsd-get-shit-done-framework-for-claude-code-24h0 — 알리카즈미, 상세 워크플로 가이드
- https://dev.to/imaginex/a-claude-code-skills-stack-how-to-combine-superpowers-gstack-and-gsd-without-the-chaos-44b3 — GSD+Superpowers+gstack 스택 가이드
- https://ccforeveryone.com/gsd — Carl Vellotti 강의, "GSD by Lex Christopherson" 서지
- https://medium.com/@richardhightower/the-great-framework-showdown-superpowers-vs-bmad-vs-speckit-vs-gsd-360983101c10 — Rick Hightower, 2026-03 (fetch 시 402 paywall)

### Issue tracker (failure mode 출처)
- https://github.com/gsd-build/get-shit-done/issues/218 — Claude Code 2.1.88+ 호환 조사
- https://github.com/gsd-build/get-shit-done/issues/1504 — commands/ → skills/ 디스커버리 붕괴
- https://github.com/gsd-build/get-shit-done/issues/1528 — 2.1.89에서 추가 회귀
- https://github.com/gsd-build/get-shit-done/issues/803 — "All questions are auto-answered" HITL 회귀
- https://github.com/gsd-build/get-shit-done/issues/780 — `--auto` 구현 오류, 서브에이전트 핸드오프 실패
- https://github.com/glittercowboy/get-shit-done/issues/50 — 기존 CLAUDE.md 미주입

## Proposed schema deltas (이 분석이 끝나며 제안)

### 기존 후보 축 중 GSD가 독립적으로 사용한 것 (★ 프로모션 임계 도달)
- **C. Mode splitting** — Ralph(plan/build 2-way)와 Superpowers(7-phase DAG)에 이어 GSD가 독립적으로 5-way(discuss/plan/execute/verify/ship) 사용. **3번째 독립 사용 → 승격 권고.**
- **A. Iteration-boundary semantics** — GSD의 페이즈 경계에서 (a) 오케스트레이터 컨텍스트는 유지하되 서브에이전트가 새로 스폰(리셋), (b) 아티팩트 파일이 커밋, (c) 서머리만 다음 페이즈로 전파, (d) verify 실패 시 rollback 옵션 트리거. Ralph에 이어 2번째 독립 사용 → **승격 임계 도달.**
- **D. Gate mechanism syntax** — GSD의 "schema drift / security / scope reduction" 게이트 택소노미 + `allowed-tools:` 프론트매터 + verify-gate가 Superpowers의 `<HARD-GATE>`와 같은 계열. 2번째 독립 사용 → **승격 임계 도달.**

### GSD가 쓰지 않거나 변형한 것
- **B. Backpressure mechanism** — Ralph의 N readers : 1 writer 비대칭은 GSD에 직접 대응물 없음. 대신 `parallelization: true/false` + 웨이브 의존성 그래프로 다른 형태의 backpressure 제공. B의 일반 형태 "리소스/권한 비대칭 배분"에는 여전히 부합하지만 Ralph-style 스킴 아님.
- **E. Authoritative process medium** — GSD의 권위 매체는 **`.planning/` 하위의 Markdown 아티팩트 세트 + `config.json`**. Superpowers의 DOT, Ralph의 PROMPT.md와 또 다른 매체. 축 자체는 여전히 유용.
- **F. Skill as unit of discipline** — GSD는 "skill"이 아니라 "slash command + workflow .md + specialized agent type" 트리오를 디시플린 유닛으로 씀. 축 F의 일반 형태 "기판과 별개인 컨벤션 레이어"에는 부합.

### 새로 제안하는 후보 축 (`meta/harness_schema.md` 의 Candidate additions에 추가)

### G. Execution environment as constraint surface
- **Proposed by**: GSD deep-dive (2026-04-13)
- **Rationale**: tentenco(2026-04)가 명시적으로 뽑아낸 축 — "Superpowers constrains the development process / GSD constrains the execution environment / gstack constrains the decision-making perspective." GSD의 프레시 컨텍스트 카브오프, Pi SDK 레벨 세션 제어, 명시적 allow-list, 웨이브 스케줄링은 모두 **LLM이 무엇을 생각하는가가 아니라 LLM이 어떤 환경에서 동작하는가**를 제약하는 결정. 현재 seed 축 중 어느 것(아키텍처·프롬프트 전략·툴 서피스)도 이 축을 정확히 포착하지 못함. 3개 축의 파편으로 쪼개져 있음.
- **Proposed form**: "하네스가 제약하는 주 대상이 (a) 모델의 프로세스/사고(Process) (b) 의사결정 관점/롤(Perspective) (c) 실행 환경(Environment) 중 무엇인가. 컨텍스트 윈도·세션 수명·권한·스케줄링·비용 추적처럼 LLM 바깥 조건을 지배하는 장치들을 묶는다."
- **Promotion threshold**: 2개 이상 독립 사용. (GSD 1개 확정, Superpowers는 Process로 반례적 근거, gstack은 Perspective로 반례적 근거 — 사실상 **축 자체가 이미 비교적 포지션 프레임으로 작동**하므로 빠른 승격 권고.)

### H. Artifact naming schema as protocol
- **Proposed by**: GSD deep-dive (2026-04-13)
- **Rationale**: GSD의 `{PHASE}-{WAVE}-{TYPE}.md` (`1-0.2-PLAN.md`, `1-VERIFICATION.md` 등)는 **파일명 자체가 프로세스 이벤트 로그**. 사람·오케스트레이터·서브에이전트·`gsd-tools.cjs` Node 유틸 모두가 같은 regex로 파싱 가능. Ralph의 평평한 `PROMPT.md / IMPLEMENTATION_PLAN.md / AGENTS.md`, Superpowers의 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`와 또 다른 차원 — GSD는 **명명 규약을 에이전트 간 RPC 프로토콜처럼** 쓴다. 축 4(State & context) 하위에 묻힐 수도 있지만, 명명 규약이 에이전트-툴 계약의 캐리어가 된다는 점은 분리할 가치.
- **Proposed form**: "하네스의 상태 파일들이 명명 규약을 갖는가. 명명 규약이 {프로세스 페이즈, 역할, 이벤트 종류}를 인코딩하여 에이전트·툴·사람 간 공통 파싱 계약으로 기능하는가. 규약 위반 시 어떻게 실패하는가."
- **Promotion threshold**: 동일.
