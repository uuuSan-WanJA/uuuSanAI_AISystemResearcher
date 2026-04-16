---
title: Bundle_GameMaker 개선 리포트 (post-rebuttal 재판정)
date: 2026-04-15
version: post_rebuttal
supersedes: report_gamemaker_improvements.md (2026-04-13)
note: v2 슬롯은 차후 개정용으로 예약
based_on:
  - insights/project_map_gamemaker_post_rebuttal.md
  - insights/graft_tier1_to_gamemaker.md
  - insights/synthesis_tier1.md
  - Bundle_GameMaker/uuuSanAI_GameMakerCollabMonitor_Codex/state/report_gamemaker_improvements_rebuttal.md
---

# Bundle_GameMaker 개선 리포트 (post-rebuttal)

## 0. 이 재판정이 존재하는 이유

원본 리포트(2026-04-13)는 `uuuSanAI_GameMaker/docs/00_system_overview.md`의 낡은 상태표를 ground truth로 취급했고, Monitor가 반박문서로 정정했다. 이 재판정은 live repo(`src/`) 코드를 ground truth로 놓고 9개 Tier1 하네스 synthesis와 재대조한다. 모든 권고는 반박문이 명시한 owner routing 원칙(**GameMaker 코드 수정 = Engine-owned bounded task**)을 따른다.

---

## 1. 원본에서 철회하는 주장

### 1-A. 3-F "GameMaker Provider Router 미완성" — **완전 철회**

맵 §1.1 [observed: `uuuSanAI_GameMaker/src/router/index.ts:1-10`]: GameMaker router는 8개 파일(`routed-llm-client`, `provider-intelligence`, `provider-router`, `quality-signals`, `review-prompts`, `routing-log`, `usage-tracker`, `index`)이 모두 존재하며 Engine router(9개, + `codex-advisor`)와 동일 API surface를 export한다. v1의 "10단계 이식 작업" 권고는 live 코드 기준 무효.

### 1-B. 블로커 4 "GameMaker 핵심 컴포넌트 4개 미착수" — **완전 철회**

맵 §1.1 [observed: `src/director/{director,workflow,scheduler,task-manifest}.ts`]: Director 클래스 633줄, `runPhase`/`handleGate`/`executeTask` 완전 구현. CreativeDirector 3모드(auto/human/interactive) 연결됨, `TaskManifestStore` 증분 실행, Executor materialization hook 포함, 30% failure-rate gate [director.ts:412] 구현. Shared Infrastructure(`knowledge-base`, `glossary`, `consistency-checker`, `artifact-store`), Agent Runtime(`createAgentRuntime`)도 모두 존재.

### 1-C. Quick win #1 "Typed gate enum" — **ALREADY-PRESENT로 격하**

맵 §1.3 [observed: `CollabMonitor_Codex/CLAUDE.md:26-28`]: Monitor는 이미 `NON-BLOCKING` / `DELEGATED-OR-CONSENT` / `HARD-GATE` 3분류를 CLAUDE.md에 typed enum으로 명시하고 있다. v1이 "프로즈로만 서술된다"고 한 것은 사실 오인. 이 primitive는 ALREADY-PRESENT — 재작성 불필요. 단, 19개 action family(`trigger_collab_action.ps1:2`)를 이 3분류에 전부 매핑한 **완성 표**는 아직 없음 → 매핑 보강만 남음.

### 1-D. Quick win #2 "Phase-0 3-way 감사" — **ALREADY-PRESENT로 격하**

맵 §3 workflow step 2 [observed: `CollabMonitor_Codex/CLAUDE.md:18`]: Monitor는 이미 first-run / active-extend / steady-state 3분류를 세션 시작 시 강제하고, steady-state 기본값은 pause. v1이 "분류되지 않는다"고 한 것도 사실 오인. primitive #10은 ALREADY-PRESENT.

### 1-E. 블로커 5 "스냅샷 staleness가 Phase-0 미적용 때문" — **원인 재해석**

맵 §2 [observed: `state/monitor_brief.md:3-4`]: Engine 스냅샷 2117분(~35h), Helper 2211분(~37h). v1(604/699분)보다 훨씬 악화됨. Phase-0 분류는 이미 있는데 staleness가 심해진 것은 분류 부재가 아니라 **운영 단절**(Engine 빌드 깨짐 + zero-task no-op)이 원인이다. 이 블로커는 harness 차원이 아니라 operational 차원.

---

## 2. 원본에서 유지하되 재프레이밍하는 주장

### 2-A. SKILL.md 위임 프로토콜 (Primitive #1/#4/#9) — **유효, 최우선**

맵 §6 Axis F [observed: 전 sub-project에 `.claude/skills/` 없음]: Axis F는 여전히 real empty-axis. 반복되는 behavioral trap(vitest 직접 실행, memory-only promise, 모호한 consent, path-cleanup을 runtime 경유로 시도)은 정확히 SKILL.md anti-trigger가 잡는 실패 모드다. v1 3-A의 판단은 그대로 유효.

**재프레이밍**: 삽입 작업은 `uuuSanAI_GameMakerEngine/.claude/skills/delegate-implementation.md` 및 `uuuSanAI_GameMaker/.claude/skills/delegate-implementation.md` 파일 생성 — 이를 **Engine-owned bounded task**로 만들어 Monitor가 engine owner에게 위임. GameMaker 쪽 파일도 Engine이 수정 (Helper 협업 프로토콜 167-174에 따름).

**Open question (v1 개방 질문 4 재게시)**: Claude Code 런타임이 두 sub-project의 `.claude/skills/`를 각각 자동 탐지하는가, 아니면 CLAUDE.md에서 명시 참조해야 하는가? 이 답에 따라 rollout 형태가 달라짐.

### 2-B. 상태 파일 명명 규칙 (Primitive #3) — **유효하되 범위 축소**

맵 §1.3: `CollabMonitor_Codex/state/`에 18개 파일, 그중 8개가 `*_handoff.md` 형태로 이미 task 단위 lifecycle을 암시적으로 표기 중이다. Axis H는 PARTIAL — GSD의 `{PHASE}-{WAVE}-{TYPE}` 수준은 아니지만 이미 단초가 있다.

**재프레이밍**: "새 컨벤션 도입"이 아니라 "이미 있는 `*_handoff.md` 패턴을 state_digest.md header에 명문화"로 축소. 기존 파일 이름 변경 없음, forward-only.

### 2-C. Compound step / 세션 학습 artifact (Primitive #2) — **유효**

맵 §6 Axis L: Arena+Evolver는 cross-cycle 구조 진화로 완전 구현이지만 session-level instinct capture는 부재. v1 3-E 판단은 유지. 단, 위치를 재조정한다.

**재프레이밍**: v1은 `EngineHelper_Codex/docs/solutions/`를 제안했으나, Helper는 "Monitor/supervisor" 역할이고 Engine이 Primary executor다 [`collaboration_protocol.md:167-174`]. 따라서 `docs/solutions/`는 `uuuSanAI_GameMakerEngine/docs/solutions/`로 이동하고, Helper cycle 종료 시 Engine에 추가 요청(bounded task)을 emit하는 구조가 프로토콜과 일관된다.

**구체적 첫 엔트리 2개 (실 블로커에서 바로 태깅 가능)**:
- `category: build-health, trigger: Engine typecheck broken 2117min, resolved: false`
- `category: pipeline-gap, trigger: followup-once Success:true but 0 tasks / Playable:NO / Genre 29%, missing WBP_CardWidget/WBP_HandDisplay/WBP_CombatScreen/EnemyTable/BalanceTable, resolved: false`

---

## 3. 재판정에서 새로 추가하는 개선점

### 3-α. 문서-코드 일관성 체크 규칙 (NEW)

맵 §5 Pain point 7 [observed: `uuuSanAI_GameMaker/docs/00_system_overview.md:86-89`]: 이 상태표가 Director/Shared Infra/Human Interface/Engine Adapter를 "⬜ 미착수"로 표기 유지 중이고, 이 drift가 v1 리포트의 직접 원인이다. 같은 drift가 재발하지 않게 하려면:

1. `00_system_overview.md`의 상태표를 live `src/` 기준으로 즉시 갱신(1회성).
2. `uuuSanAI_GameMaker/CLAUDE.md`에 rule 추가: "`docs/00_*.md` 상태표를 편집하기 전에 해당 디렉터리가 `src/`에 실재하는지 먼저 검증한다. 불일치가 있으면 같은 turn에 수정한다." — Monitor CLAUDE.md `P10 rule-persistence discipline`의 서브규칙으로 프레이밍.
3. Engine-owned bounded task로 실행.

**난이도**: 매우 낮음. 핵심은 이번 drift가 v1 사고의 **upstream cause**였다는 점이다 — 이 primitive 없이는 같은 사고가 재발한다.

### 3-β. Action family 전수 매핑표 (Primitive #6 확장)

맵 §1.3 [observed: `trigger_collab_action.ps1:2`]: Monitor가 선언하는 action family는 19개(`assess`, `preflight`, `launch-status`, `observe-engine`, `engine-self-progress`, `engine-helper-followup`, `helper-review`, `helper-self-progress`, `run-engine`, `run-helper`, `run-session`, `launch-*`, `ask-engine-*` 5종). CLAUDE.md:26-28의 3분류(NON-BLOCKING/DELEGATED-OR-CONSENT/HARD-GATE)에는 5개 액션만 예시되어 있고, 19개 전부에 대한 매핑은 없음.

**적용**: CLAUDE.md에 19×3 매핑 표를 한 번에 추가. 모든 action이 자신이 어느 blocking class에 속하는지 명시적 소속을 가지게 됨. `assess`/`preflight`/`launch-status` 등 unclassified action이 "암묵적으로 non-blocking이라 가정"되는 현재 상태를 제거.

**난이도**: 매우 낮음. 코드 변경 없음, CLAUDE.md 표 1개.

### 3-γ. `CANONICAL_ACTION_FAMILIES` 어휘를 구조화 매체로 승격 (Axis E 보강)

맵 §6 Axis E [observed: `engine_ask_contract.py`, `monitor_cycle.py:11`]: 현재 Bundle_GameMaker에서 유일한 structured-vocabulary layer는 Python의 `CANONICAL_ACTION_FAMILIES`. CLAUDE.md는 prose, `docs/`는 Markdown. 이 어휘가 Monitor(Python)와 Engine Ask 경로에만 묶여 있어 GameMaker/Helper는 참조 불가.

**적용**: `CANONICAL_ACTION_FAMILIES`를 `uuuSanAI_bridge-types/src/index.ts`로 이동(또는 미러)하여 TypeScript enum으로 재export. 이후 Engine/GameMaker/Helper가 모두 동일 어휘를 참조. GSD의 `{PHASE}-{WAVE}-{TYPE}` 수준은 아니지만 Axis E가 "Markdown + JSON only"에서 "Markdown + JSON + shared typed vocab"로 개선된다.

**난이도**: 중간(Engine-owned bounded task). 파일 1개 이동/미러, enum export 정렬.

---

## 4. 새 적용 순서

### Tier 0 — 반드시 선행

**T0-1. Engine build/typecheck health 복구 + followup-once zero-task 버그 원인 규명**
이것은 harness primitive가 아니라 operational 블로커다. 맵 §2에서 Monitor의 `next_work_brief`가 최우선 태스크로 지목하고 있음. 이게 풀리기 전까지는 어떤 harness graft도 **측정 불가**(Engine이 안 돌면 효과 관측할 cycle이 없음).

### Tier 1 — Quick wins (코드 변경 없음, 모두 Engine-owned bounded task)

1. **3-α 문서 drift fix + 가드레일 rule** — `docs/00_system_overview.md:86-89` 상태표 갱신 + `uuuSanAI_GameMaker/CLAUDE.md`에 검증 rule 추가. 이 사고의 upstream cause 제거.
2. **3-β Action family 19개 전수 매핑표** — `CollabMonitor_Codex/CLAUDE.md`에 매핑 표 1개 추가. `HARD-GATE` unclassified 회색지대 제거.
3. **2-B `state/*_handoff.md` 컨벤션 명문화** — `state_digest.md` header에 1회 문서화. 기존 파일 rename 없음.

### Tier 2 — SKILL.md 파일럿

4. **2-A SKILL.md 위임 프로토콜 (vitest anti-trigger 범위 축소판)** — 먼저 `uuuSanAI_GameMakerEngine/.claude/skills/delegate-implementation.md` 1개만 생성. `allowed-tools: [Task, Read]` + anti-trigger. Open question(자동 탐지 여부) 해소 후에만 GameMaker 쪽에 복제.

### Tier 3 — 구조적 추가

5. **2-C Compound step `docs/solutions/`** — `uuuSanAI_GameMakerEngine/docs/solutions/` 신설. 첫 엔트리 2개는 맵 §3에서 제공(build-health + pipeline-gap). Tier 2 SKILL.md가 안정된 후 착수.
6. **3-γ `CANONICAL_ACTION_FAMILIES` TS 미러** — `uuuSanAI_bridge-types`로 이동. Axis E 보강. Tier 1-2가 정착된 후.

### 장기 (현재 operational 블로커 해소 후)

- **v1 #5 Role-specialized review subagent** — v1은 "Director 미착수"를 이유로 DEFER 판정했으나 Director는 이미 존재. 다만 각 부서(`src/departments/{design,narrative,programming,art,sound,level_assembly,qa,deploy}/`)가 Claude Code `.claude/agents/` 경로로 노출돼 있지 않다. 이것이 실제 잔여 gap. 부서 8개 각각에 대해 agents 파일을 생성하면 현재 generalist LLM이 부서 평가에 쓰이는 것을 스코프로 제한할 수 있음. **재판정: DEFER → Tier 4 후보**.
- **v1 #8 Wave-parallel execution** — v1이 "Director 미착수"를 이유로 DEFER했으나 `TaskScheduler`의 topological batching은 이미 존재하고 concurrency는 CLI=1, API=3으로 하드코딩되어 있다 [director.ts:278]. 실제 잔여 gap은 "부서 간 병렬 실행 가능성을 명시적 gate로 노출"하는 것. 단, CLI MAX 구독 제약이 있어 concurrency=1은 의도적일 수 있음 — **재판정 전 사용자 확인 필요** (구독 제약이 근거인가, 안전성이 근거인가).

---

## 5. 살아 있는 블로커 (재판정 업데이트)

원본 블로커 리스트는 "path migration이 단일 루트"로 서술했으나 맵 §2는 이를 정정한다.

1. **Engine build/typecheck 깨짐** — `next_work_brief.md`의 최우선. path migration보다 위. 이게 풀리지 않으면 Engine cycle 자체가 돌지 않음.
2. **`followup-once` zero-task materialization** — `Success:true / 0 tasks / 0 artifacts / 31 skipped`, `Playable: NO`, `Overall 69%`, `Genre 29%`, missing `WBP_CardWidget`·`WBP_HandDisplay`·`WBP_CombatScreen`·`EnemyTable`·`BalanceTable`. 증분 실행 캐시 또는 task 선택 규칙에 문제 가능성.
3. **Path migration 미해결** — 여전히 open이지만 더는 lead가 아님. 유지보수 전용 태스크로 격하.
4. **Helper efficacy low** — 동일 gap 반복 발견. 3-α와 2-C가 간접적으로 완화하지만 직접 해결책은 아님.
5. **Delegation-guardrail rollout 미완** — open engine task로 존재. 2-A(SKILL.md)가 직접 대응.
6. **DALL-E 3 deprecated warning 소음** — non-terminal로 격하됐으나 매 run에 노이즈.
7. **`docs/00_system_overview.md` drift** — 3-α가 직접 대응. 이 문서 drift가 v1 사고의 원인이었음.

---

## 6. 원본 대비 요약

| 항목 | 원본 | 재판정 |
|---|---|---|
| 3-F GameMaker Router | GRAFT, 10단계 이식 | **철회** (완비) |
| 블로커 4 핵심 컴포넌트 미착수 | 4개 미착수 | **철회** (모두 존재) |
| Primitive #6 typed gate | GRAFT (Quick win) | **ALREADY-PRESENT** (매핑 보강만 남음 = 3-β) |
| Primitive #10 Phase-0 audit | GRAFT (Quick win) | **ALREADY-PRESENT** |
| Primitive #1 SKILL.md | GRAFT (Quick win) | **유지, Engine-owned로 프레이밍** |
| Primitive #2 docs/solutions | GRAFT | **유지, Engine으로 소유자 이동** |
| Primitive #3 상태 파일 명명 | GRAFT | **유지, forward-only 범위 축소** |
| Doc drift 가드레일 | — | **NEW (3-α, 최우선)** |
| Action family 전수 매핑 | — | **NEW (3-β)** |
| Bridge-types 어휘 승격 | — | **NEW (3-γ)** |
| 블로커 1 (path migration) | 최우선 | 운영 유지보수로 격하 |
| 블로커 (Engine build health) | — | **NEW, 최우선** |

---

## 7. Owner routing 제약 (모든 권고에 적용)

맵 §7 [observed: `monitor_cycle.py:226-241`, `CollabMonitor_Codex/CLAUDE.md:20,37`, `collaboration_protocol.md:167-174`]:

```
target_agent_role ∈ {engine, helper}   — gamemaker 없음
uuuSanAI_GameMaker 코드 변경 → Engine-owned bounded task, GameMaker 파일명 지명
Monitor는 직접 편집 금지 (사용자 명시 허가 없을 때)
```

**이 재판정의 모든 권고는 이 규칙을 따른다.** 3-A/3-B/3-C/3-α/3-β/3-γ 전부 Engine이 수행하는 bounded task로 프레이밍되며, GameMaker 쪽 파일(CLAUDE.md, .claude/skills/, docs/)을 건드려야 할 때도 Engine-owned task가 그 파일을 수정한다.

---

*이 재판정은 원본을 supersedes 관계로 기록한다. 모든 정정은 `project_map_gamemaker_post_rebuttal.md`의 [observed: path:line] 근거로 추적 가능하다. `v2` 슬롯은 차후 주요 개정을 위해 비워둔다.*
