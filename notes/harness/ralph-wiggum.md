---
title: Ralph Wiggum
date: 2026-04-13
author: Geoffrey Huntley (@ghuntley)
first_public: 2025-07-14
primary_source: https://ghuntley.com/ralph/
topic: harness
tags: [harness, claude-code, bash-loop, greenfield, huntley, ralph]
status: deep-dive
confidence: high
rounds: 1
axes_used: [1,2,3,4,5,6,7,8,9,10,11,12]
axes_added: []
axes_dropped: []
candidate_axis_proposals: [iteration_boundary_semantics, backpressure_mechanism, mode_splitting]
---

## TL;DR (3줄)
Ralph은 `while true; cat PROMPT.md | claude -p --dangerously-skip-permissions` 형태의 최소주의 bash 루프로 그린필드 SW를 자동 생성하는 하네스. 매 이터레이션마다 컨텍스트 창을 초기화하되 **파일시스템 (`specs/*`, `IMPLEMENTATION_PLAN.md`, `AGENTS.md`)을 유일한 지속 기억**으로 쓰는 것이 본질. "완벽한 프롬프트는 없다, 매 루프가 스택을 결정적으로 할당한다"가 철학이며 그린필드 90% 달성 주장과 ripgrep 비결정성·싸이코판시 루프라는 뚜렷한 한계가 공존.

## 1. Identity & provenance
- **Author**: Geoffrey Huntley (독립, @ghuntley, ghuntley.com)
- **First public**: 2025-07-14 — `ghuntley.com/ralph/`
- **Distribution**: 블로그 포스트 → 2025년 12월 바이럴 → 서드파티 playbook 포크 → Anthropic 퍼스트파티 플러그인 반영
- **Huntley 후속 포스트**:
  - 2025-09-28 `/cursed/` — Ralph로 3개월간 CURSED 프로그래밍 언어 생성 실험
  - 2026-01-17 `/loop/` — Ralph를 "스크립트"에서 "마인드셋"으로 재프레임
  - 2026-02-27 `/real/` — 1년 회고, $10.42/hr 주장
- **현 주력 스캐폴드**: `ClaytonFarr/ralph-playbook` (ghuntley가 `how-to-ralph-wiggum`로 포크, ⭐1577)
- **유지 상태**: 블로그와 생태계 변종을 통해 활발히 진화. Anthropic `ralph-wiggum` 플러그인 공식 탑재.

## 2. Problem framing
Huntley는 Ralph를 **그린필드 아웃소싱 대체재**로 포지션. 핵심 수사는 "비결정론적 세계에서 결정론적으로 나쁜" 기법 — 의도적으로 단순해서 결함이 식별가능하고 프롬프트 튜닝으로 해결 가능하다는 것.

> "Ralph can replace the majority of outsourcing at most companies for greenfield projects. It has defects, but these are identifiable and resolvable through various styles of prompts. That's the beauty of Ralph — the technique is deterministically bad in an undeterministic world." — ghuntley.com/ralph

## 3. Control architecture
**Unconditional `while true` bash 루프.** 한 이터레이션 = `cat PROMPT.md | claude -p --dangerously-skip-permissions --model opus --output-format=stream-json --verbose` 1회 호출 → `git push`. 내부 수렴 판정 없음. `max_iterations=N` 인자는 선택적 소프트캡.

**핵심 규칙**: 한 루프에 한 작업만(one thing per loop).

**Anthropic 분류 매핑**: 이터레이션 **내부**는 LLM 자율(agent). **외곽 하네스**는 단순 workflow. 하이브리드.

**현재 canonical form** (how-to-ralph-wiggum): `./loop.sh [plan|N]` — `PROMPT_plan.md` vs `PROMPT_build.md` 모드 선택 + 반복 상한.

> "In its purest form, Ralph is a Bash loop. `while :; do cat PROMPT.md | claude-code ; done` ... To get good outcomes with Ralph, you need to ask Ralph to do one thing per loop. Only one thing."

## 4. State & context model
**Ralph의 진짜 핵심.** 이터레이션 사이에 컨텍스트는 완전 초기화(`claude -p` 재실행). 지속은 전적으로 디스크:

| 파일 | 역할 | 변경자 |
|---|---|---|
| `PROMPT.md` / `PROMPT_build.md` / `PROMPT_plan.md` | 매 루프 진입 프롬프트 | **operator only** ("tune like a guitar") |
| `specs/*` | 소스 오브 트루스 사양 | operator + Opus subagent (모순 발견 시) |
| `IMPLEMENTATION_PLAN.md` / `fix_plan.md` | 우선순위화된 living TODO | agent (subagent로) |
| `AGENTS.md` | 운영 명령(build/test/lint) | agent (새로운 운영 학습 시만) |
| `src/*` + git | 실제 코드 | agent |

**턴 N+1에 모델이 보는 것**: 빈 컨텍스트 → PROMPT 재독 → IMPLEMENTATION_PLAN.md 재독 → AGENTS.md 재독 → specs/* 재독 → src/* 재연구. **크로스 이터레이션 기억은 100% 파일 매개**.

> "every loop, with each loop with its new context window ... future loops will not have the reasoning in their context window"

명시적 설계 원칙: `AGENTS.md` 는 **운영만**, 진행 상황은 `IMPLEMENTATION_PLAN.md` 로. 혼합 금지. "A bloated AGENTS.md pollutes every future loop's context."

## 5. Prompt strategy
- **"No perfect prompt"** — 지속 튜닝. 운영자가 실패를 관찰하고 PROMPT.md 수정.
- **"Stack allocation" 은유**: 매 루프에 plan + specs 를 결정론적으로 주입.
- **숫자 상승 가드레일**: `9`, `99`, `999`, ..., `99999999999999` — 높을수록 중요. 해킹스럽지만 작동 보고.
- **2모드 분할**: `PROMPT_plan.md` (갭 분석 only, 구현 금지) ↔ `PROMPT_build.md` (우선순위 1건 선택 후 구현).
- **서브에이전트 지시**:
  - 읽기/검색: up to **500 parallel Sonnet**
  - 빌드/테스트: **exactly 1 Sonnet** (백프레셔)
  - 복잡 추론: Opus
- **플레이스홀더 방지 대문자 호통**:
  > "9999999999999999999999999999. DO NOT IMPLEMENT PLACEHOLDER OR SIMPLE IMPLEMENTATIONS. WE WANT FULL IMPLEMENTATIONS. DO IT OR I WILL YELL AT YOU"
- **자기개선**: agent가 AGENTS.md(운영 학습)와 IMPLEMENTATION_PLAN.md(작업 진행)를 subagent로 갱신.

> "There seems to be an obsession in the programming community with the perfect prompt. There is no such thing as a perfect prompt. ... deterministically allocate the stack the same way every loop."

## 6. Tool surface & permission model
**YOLO**: `--dangerously-skip-permissions`. 모든 Claude Code 툴 오픈, 샌드박스는 운영자 책임.

- 모델: 기본 **Opus**. 빌드 모드에서 속도 위해 Sonnet 허용.
- 출력: `stream-json` 로 로깅 가능.
- 자동화: 매 이터레이션 후 `git push origin <current>`.
- Anthropic 공식 Ralph 플러그인은 이 플래그 강제가 일관되지 않아 **제 기능을 못 함** (뒤의 실패 모드 참조).

## 7. Human-in-the-loop points
**실행 중 내부 HITL 없음.** 인간은 **외곽 제어 루프** — 로그 감시, 프로세스 kill, PROMPT.md / fix_plan.md / specs/* 편집 후 재시작. Huntley가 인정한 "you'll wake up to a broken codebase" 실패 모드가 이를 확증. HITL은 Ralph **세션 사이**에 일어나지, 세션 **안**에 있지 않음.

## 8. Composability
Ralph는 프레임워크가 아닌 **패턴**이라 잘 합성됨:

| 변종 | 저자 | 변경점 |
|---|---|---|
| Agent Teams + Ralph | Meag Tessmann | 플래너가 shared-contract 파일을 먼저 생성 → N개 worker Ralph를 병렬 worktree에서 구동 |
| `vercel-labs/ralph-loop-agent` | Vercel | AI SDK로 포팅, `verifyCompletion` 오라클이 외곽 게이트 |
| `snarktank/ralph` | snarktank | PRD 기반 stop condition (완료 표기가 종료 조건) |
| `frankbria/ralph-claude-code` | Frank Bria | 이중 종료 게이트 + `EXIT_SIGNAL:true` 토큰 + 24h 타임아웃 + tmux 실시간 스트림 |
| Sondera "Principal Skinner" | Josh Devon | 툴콜 인터셉션 + 행동 서킷브레이커 + 적대적 시뮬레이션 |
| d4b Codex 스왑 | d4b | 드라이버를 Claude Code → OpenAI Codex CLI |
| Anthropic 공식 플러그인 | Anthropic | Stop hook 기반 퍼스트파티 구현 |

**런타임 이식성 실증**: 동일 원시요소가 Claude Code / Codex / Vercel AI SDK / 커스텀 CLI 모두에서 재현됨. 언어-애그노스틱한 bash이기 때문.

## 9. Empirical claims & evidence

### Huntley 자신 주장 (일화 + 스크린샷 + 임베디드 트윗, **벤치마크 없음**)
- **CURSED 프로그래밍 언어**: compiler + stdlib + LSP + Treesitter + IDE 확장. 3개월 Ralph 루프 결과. (ghuntley.com/cursed)
- **$50k 계약 MVP를 $297에 납품** (한 엔지니어 사례, 임베디드 트윗)
- **YC 해커톤 필드 리포트**: "Shipped 6 Repos Overnight"
- **$10.42/hr SW 개발 비용 주장** (2026-02 회고)
- **PE 펌이 Atlassian 숏 포지션 진입** (Ralph 보고)
- **개인 예제**: Cloudflare D1 → PlanetScale Postgres 마이그레이션 "just worked"

### 3자 측정
- **Tessmann** (himeag/medium): worktree 3개에 걸쳐 10 tasks in <1hr, $15~25, 빌드+테스트 100% 통과
- **Braintrust/Wang**: 2 user story 에 274 LLM 호출, 95,256 토큰, **$1.38**

**증거 유형**: 압도적으로 일화 + 스크린샷. 통제된 벤치마크 없음.

## 10. Failure modes & limits

### 저자 자인
- **Ripgrep 비결정성 (Achilles' heel)** — 검색 실패 시 "구현되지 않음"으로 잘못 결론 → 중복 구현
- **Claude 플레이스홀더 편향** — 대문자 호통으로 대응
- **Wake-up broken codebase** — 아침에 일어나면 컴파일 안 되는 레포
- **그린필드 전용** — "There's no way in heck would I use Ralph in an existing code base"
- **90% ceiling** — 마지막 10%는 사람이 마감
- **Context overflow** — compile error 출력이 147k/170k 창 초과
- **세 가지 산출 상태**: under baked / baked / baked with unspecified latent behaviours
- **쓰레기 누적**: temp files, binaries

### 3자 관찰
- **"Agents Don't Commit" (Tessmann)**: 9번 중 1번만 `git commit` 수행. 3차례 프롬프트 튜닝 실패. **4줄 bash safety net 만 효과**.
- **Skipped tests mask failures (Tessmann)**: Ralph가 "15 passed, 3 skipped"를 그린으로 간주, 정작 스킵된 테스트가 진짜 버그를 잡는 것. `"All tests pass" is not the same as "all tests ran."`
- **Sycophancy / overbaking (Devon)**: Ralph가 완료를 주장하려고 작동하는 코드를 리팩터하거나 설정을 삭제하거나 존재하지 않는 문법을 발명
- **max-iterations is not a safety control (Devon)**: "A numerical limit does not prevent an agent from deleting a database in the second iteration."
- **Hook-brick (Dex/HumanLayer)**: Anthropic 공식 Ralph 플러그인이 state 파일을 삭제하면 **레포 내 Claude 를 영구 브릭**
- **Permission-syntax 버그 (GH #16398)**: 공식 `/ralph-wiggum:ralph-loop` 명령이 자신의 퍼미션 체크에 실패 (`! code-fence` 문법 파서 문제)
- **beuke.org 6가지 내재 모드**: no stop condition, oscillation, context overload, hallucination amplification, metric gaming, cost escalation

### 자기비판
Huntley 자신 (via The Register 2026-01-27): "It's cursed in its lexical structure, it's cursed in how it was built, it's cursed that this is possible." — Ralph가 SaaS 기능 커머디티화를 가능하게 했다는 공개 우려.

## 11. Transferable primitives ★ (load-bearing)

각 항목: 이름 / 설명 / 전제 컨텍스트 / standalone-extractable?

### P1. Fresh context per iteration + file-mediated memory
- 매 턴 빈 창, 지속은 디스크상 작은 파일 세트.
- 전제: 파일시스템 있는 런타임, 파일 r/w 툴 접근.
- **YES**. 어떤 에이전트 런타임에도 이식 가능. Ralph의 진짜 핵심.

### P2. "Tune like a guitar" — static prompt, operator-mutated
- 프롬프트는 "완벽"하지 않다. 실패 관찰하고 외곽에서 수정.
- 전제: 운영자 모니터링, 외곽 편집 루프.
- **YES**.

### P3. Stack-allocated context (deterministic preload)
- 매 루프 시작에 동일한 파일 세트(plan + specs + ops)를 결정론적으로 주입.
- 전제: `study @FILE` 류 지시 존중 모델, 작고 안정적인 파일 세트.
- **YES**. 광의의 context engineering 전략으로 일반화.

### P4. 2-mode prompt split (plan vs build)
- 기획과 구현에 서로 다른 프롬프트 파일. plan 모드는 코드 수정 금지.
- 전제: 모드 유지할 수 있는 모델, 파일 기반 plan 핸드오프.
- **YES**. 루프 자체와 직교, 즉시 이식 가능.

### P5. Asymmetric subagent backpressure (N readers : 1 writer)
- 읽기/검색은 N병렬, 빌드/테스트는 정확히 1. 탐색 속도 유지하면서 상태 경쟁 차단.
- 전제: 서브에이전트 + 역할별 throttle 지원 런타임.
- **PARTIAL**. 원시요소(비대칭 비율)는 이식 가능. 실장은 런타임 의존.

### P6. Numbered priority guardrails (ascending absurdity)
- 규칙에 9, 99, 999… 숫자를 붙여 중요도 신호. 해킹.
- 전제: long-context 모델, sentinel 길이 반응성.
- **YES**, 단 low confidence — 효과에 대한 벤치마크 없음.

### P7. Living task file as the one-task-per-loop oracle
- IMPLEMENTATION_PLAN.md 1개가 우선순위 목록. "제일 중요한 것 하나 선택"이 선택 primitive.
- 전제: agent가 우선순위 존중, 파일 크기 관리.
- **YES**.

### P8. Operational-learning file (AGENTS.md) separate from task state
- 운영 명령/런북 전용 파일. 진행상황은 **금지**. 컨텍스트 오염 방지 명시적 분리.
- 전제: agent + 운영자 양쪽이 경계 존중.
- **YES**. P7와 자연스러운 쌍.

### P9. Anti-placeholder CAPS yelling
- 대문자 anti-stub 명령. Claude 편향 대응.
- 전제: Claude 계열 편향; 다른 모델엔 미검증.
- **PARTIAL** (모델 의존).

### P10. "Carve off small independent context windows" (Dex 재프레임)
- Ralph의 진짜 가치는 "영원히 돌림"이 아니라 **"작업을 작은 독립 컨텍스트 창으로 쪼갠다"**. 작게 분해 가능하고 명확한 done-test 있는 작업에만 적용.
- 전제: 작업이 실제로 분해 가능, done-test 존재.
- **YES** — 이것이 이식해야 할 **멘탈 모델**. bash 스크립트보다 중요.
- > "it misses the key point of ralph which is not 'run forever' but in 'carve off small bits of work into independent context windows'" — Dex, HumanLayer

### P11. Per-iteration commit+push as audit trail
- 매 이터레이션 끝 `git commit` + `git push`. 롤백 granularity + 외부 관측성을 커스텀 로거 없이 획득.
- 전제: git 레포, Ralph 전용 브랜치 감수.
- **YES**.

### P12. Three-phase greenfield workflow (plan-out-loud → plan loop → build loop)
- 1단계: LLM 대화로 specs 도출 (루프 밖). 2단계: plan mode Ralph로 IMPLEMENTATION_PLAN.md 굳히기. 3단계: build mode Ralph로 구현. 단계 전환은 `loop.sh` 인자로 수동.
- 전제: 그린필드, plan-loop 지연 감수.
- **YES** — 다른 원시요소 없이도 독립 적용 가능한 워크플로 템플릿.

### Rejected as primitive (중요)
**`--dangerously-skip-permissions` 를 안전 모델로 포팅하지 말 것.** Sondera의 비판은 옳다 — 이것은 이식 가능한 원시요소가 아니라 **부채**. "bounded fresh context" 멘탈 모델과 P5 백프레셔는 포팅하되, "YOLO 모든 툴"은 지속 상태를 잃을 수 있는 프로젝트에는 **넣지 말 것**.

## 12. Open questions
- Dex/HumanLayer "Brief History of Ralph" 전문 독해 — P10 인용구만 확보됨, 전체 논증은 follow-up probe 대상
- Dev Interrupted 팟캐스트 Huntley 발언 전사 — 공개 인덱싱 안 됨
- Braintrust/Wang 퍼미션 우회 구체 — 실패 anecdote로 가치
- Ralph × Superpowers / Ralph × GSD 합성 사례 — 발견된 재현 없음
- 한국어 커뮤니티 재현 — 영어 검색으로는 미노출, 한국어 probe 대상
- 정량적 비용 폭발 postmortem — 아직 공개된 것 없음

## Sources

### Primary (Huntley)
- https://ghuntley.com/ralph/ — 원글, 2025-07-14
- https://ghuntley.com/cursed/ — 2025-09-28
- https://ghuntley.com/loop/ — 2026-01-17
- https://ghuntley.com/real/ — 2026-02-27
- https://github.com/ghuntley/how-to-ralph-wiggum — fork of ClaytonFarr/ralph-playbook

### Primary (third-party reproductions & critiques)
- https://www.humanlayer.dev/blog/brief-history-of-ralph — Dex, P10 재프레임
- https://medium.com/@himeag/when-agent-teams-meet-the-ralph-wiggum-loop-4bbcc783db23 — Tessmann, Agent Teams + Ralph, "Agents Don't Commit"
- https://www.braintrust.dev/blog/ralph-wiggum-debugging — Wang, 274 calls $1.38
- https://blog.sondera.ai/p/ralph-wiggum-principal-skinner-agent-reliability — Devon, Sycophancy 비판
- https://beuke.org/ralph-wiggum-loop/ — 6가지 내재 모드
- https://github.com/anthropics/claude-code/issues/16398 — 공식 플러그인 퍼미션 버그

### Variants (코드)
- https://github.com/frankbria/ralph-claude-code
- https://github.com/vercel-labs/ralph-loop-agent
- https://github.com/snarktank/ralph

### Secondary
- https://www.theregister.com/2026/01/27/ralph_wiggum_claude_loops/ — Huntley 자기비판 인용원
- https://linearb.io/dev-interrupted/podcast/inventing-the-ralph-wiggum-loop — 팟캐스트 (transcript 없음)
