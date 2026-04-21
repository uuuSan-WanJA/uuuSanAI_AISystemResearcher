---
title: 지식 레이어의 운영 프리미티브 — 4분지 lifecycle operations 매트릭스
date: 2026-04-21
based_on:
  - notes/techniques/karpathy-llm-wiki.md
  - notes/techniques/basic-memory.md
  - notes/techniques/graphify.md
  - notes/techniques/cognee.md
  - notes/techniques/letta.md
  - insights/primitive-knowledge-layer-design-space.md
confidence: medium-high (5 deep-dive 데이터포인트 → 4분지 중 2분지 2 사례 충족)
tags: [knowledge-layer, lifecycle, lint, consolidation, refinement, doctor, reflection, primitive, carve-out]
carve_out_from: insights/primitive-knowledge-layer-design-space.md
carve_out_trigger: 2026-04-21 Letta deep-dive (structural + consolidation+feedback 동시에 2 사례 임계 충족)
---

## 한 줄 요약

지식 레이어가 살아있는 시스템인 한 builder·storage·timing 3축 *외부* 의 **운영 차원**(이미 쌓인 지식을 어떻게 유지·개선·축적하는가)이 따로 존재하며, 5개 deep-dive 사례(LLM Wiki / Basic Memory / Graphify / Cognee / Letta) 의 src 동사 분석으로 이 차원이 **4분지**로 분화됨이 드러났다 — **structural lint**(스키마/인덱스 정합성, 기계적 판정), **semantic lint**(의미적 노후화·모순·orphan 탐지, LLM grader 필요), **incremental update**(재추출 비용 통제), **consolidation + feedback refinement**(피드백 루프 통한 additive 재조정). 4분지 중 **2분지가 carve-out 임계(2 사례)를 충족** — structural lint = Basic Memory `doctor` + Letta `/doctor` (어휘 1:1 일치), consolidation+feedback = Cognee `improve` + Letta `reflection` (다른 메커니즘, 같은 추상). semantic lint(LLM Wiki 단일) 와 incremental update(Graphify 단일 + Basic Memory `sync --watch` 약한 2) 는 1 사례 잔존. **분지를 가르는 결정적 신호는 src 의 동사** — `apply/consolidate/create/persist`(additive enrichment) vs `detect/validate/flag`(orphan/contradiction 탐지) vs `update/rebuild`(efficiency) vs `verify/repair`(structural). Forgetting(TTL / graph invalidation / 파일 삭제) 은 "소멸" 성격이라 본 매트릭스 외부의 별도 차원으로 유지.

---

## 패턴 / 주장

LLM 지식 레이어를 도입할 때 대부분의 주의가 *"무엇을 어떻게 쓸 것인가"*(builder/storage/timing 3축, `primitive-knowledge-layer-design-space.md`) 에 쏠리지만, 실전에서 시스템이 무너지는 지점은 *"이미 쓴 것을 시간이 지나면서 어떻게 다룰 것인가"* 다. 5개 프레임워크의 src 분석은 이 운영 차원이 4개 분지로 분화돼 있고, 분지마다 동사 시그니처·자동성 수준·LLM 호출 빈도·사용자 인터랙션이 다름을 보여준다.

**핵심 주장**: 운영 차원은 builder/storage/timing 3축과 **직교** 다. 같은 (builder, storage, timing) 좌표의 두 시스템이 서로 다른 운영 분지를 채택할 수 있고(예: Basic Memory + Letta MemFS 둘 다 markdown 좌표인데 structural lint 분지를 공유), 다른 좌표의 두 시스템이 같은 운영 분지를 공유할 수도 있다(예: Cognee induction-graph + Letta self-editing-blocks/markdown 이 consolidation+feedback 분지를 공유). 따라서 **운영 차원은 도입 의사결정에서 별도 슬롯으로 다뤄야 한다**.

**부수 주장**: 분지가 "lint" 라는 단일 단어로 묶이지만 *내용은 4가지로 다르다*. 한 분지의 도구를 다른 분지의 사례로 잘못 등재하면(2026-04-21 Cognee deep-dive 이전 카드의 *"`improve` ≈ semantic lint"* 가 src 동사 분석으로 반증된 케이스) primitive 카드의 사례 카운트가 오염되고 carve-out 의사결정이 왜곡된다. **분지 판정은 docs 의 마케팅 어휘가 아니라 src 의 함수 이름·동사로 한다**.

---

## 4분지 매트릭스 (현재 상태, 2026-04-21)

| 분지 | 정의 | 1사례 | 2사례 | 3+ | 동사 시그니처 |
|---|---|---|---|---|---|
| **Structural lint** | 스키마·인덱스·파일↔DB 정합성, 기계적 판정 | Basic Memory `doctor` + `schema_infer/validate/diff` | Letta `/doctor` (`context_doctor` skill) | (대기) | `verify`, `validate`, `repair`, `infer`, `diff` |
| **Semantic lint** | 의미적 노후화·모순·orphan·stale claim 탐지, LLM grader 필요 | LLM Wiki `Lint Workflow` (4 categories: orphan/superseded/missing concept/research gap) | (대기 — Cognee `improve` 는 반증됨) | (대기) | `detect`, `flag`, `find_contradictions`, `find_orphans` |
| **Incremental update** | 재추출 비용 통제, "바뀐 부분만" 재빌드 | Graphify `--update`/`--watch` (파일 해시 캐시 → LLM 호출 0회) | Basic Memory `sync --watch` (약한 사례 — 단순 파일 watcher) | (대기) | `update`, `rebuild`, `watch`, `sync` |
| **Consolidation + feedback refinement** | 피드백 루프 통한 additive 재조정, 삭제 없이 덧붙임 | Cognee `improve` (feedback weight + session→permanent + entity description 재합성) | Letta `reflection` subagent (mistake-driven LLM 분석 + git commit) | (대기) | `apply`, `consolidate`, `create`, `persist`, `enrich`, `reflect` |

**Carve-out 충족 분지** (2 사례 임계 도달): structural lint, consolidation+feedback.
**잔존 1 사례 분지**: semantic lint, incremental update — 다음 deep-dive 가 이쪽을 트리거할 가능성.

---

## 분지별 상세

### 1. Structural lint — 자기진단 명령의 원형

**정의**: 스키마 정합성, 파일↔인덱스 동기화, 마이그레이션 무결성을 기계적으로 점검·복구. LLM 호출 없이도 결정적 판정 가능. 사용자가 명시적으로 호출하는 self-diagnose 명령으로 노출되는 것이 패턴.

**1사례 — Basic Memory** (`notes/techniques/basic-memory.md`):
- `basic-memory doctor` (v0.17.4, 2026-01-05) — DB 무결성 점검 + 파일↔인덱스 드리프트 탐지.
- `schema_infer` / `schema_validate` / `schema_diff` (v0.19.0, 2026-03-07) — knowledge graph 스키마 추론·검증·diff.
- 동작: 결정적, LLM 호출 없음, 수정 가능 항목은 자동 패치, 수정 불가 항목은 사용자에게 보고.

**2사례 — Letta `/doctor`** (`notes/techniques/letta.md` Q4):
- `context_doctor` skill (`src/skills/builtin/context_doctor/SKILL.md`, changelog 0.19.8): *"Identify and repair degradation in system prompt, external memory, and skills preventing you from following instructions or remembering information as well as you should"*.
- 4-step 절차 — (Step 1) issue 식별 (system prompt bloat / redundancy / invalid format / poor progressive disclosure), (Step 2) plan + implement, (Step 3) git commit/push, (Step 4) `/recompile` 권유.
- 차이: Basic Memory `doctor` 는 결정적, Letta `/doctor` 는 LLM이 자기 컨텍스트를 self-grade — *"context bloat"* 같은 평가에 LLM 호출이 들어감. 그러나 절차가 동일하고 어휘 1:1 일치(*"Identify and repair degradation"* / *"파일↔DB 드리프트 탐지"*).

**핵심 관찰**: 두 사례 모두 명령 이름이 *"doctor"*. 어휘가 우연히 일치한 것이 아니라 *"진단 → 처방 → 후속 조치"* 메타포가 두 팀에 독립적으로 떠올랐다는 시장 신호. **사용자 호출 가능한 자기진단 명령** 은 지식 레이어 도입 시 1등급 시민으로 노출해야 할 패턴.

**잠재 3+ 사례 후보**: Cognee 의 `alembic/` 마이그레이션 + 자체 `eval_framework/` (Cognee deep-dive 의 미답), Mem0/Zep 의 헬스체크 도구 (deep-dive 미수행).

---

### 2. Semantic lint — LLM grader 필요한 노후화 탐지

**정의**: 의미적 노후화, 모순, orphan(연결 끊긴 개념), stale claim, missing concept 탐지. 결정적 판정 불가능, **LLM grader 필수**. 동사 시그니처가 detect/validate/flag.

**1사례 — LLM Wiki `Lint Workflow`** (`notes/techniques/karpathy-llm-wiki.md`):
- 4 categories: orphan / superseded / missing concept / research gap.
- 작동: LLM 이 wiki corpus 를 읽고 각 페이지에 위 4 flag 중 해당하는 것을 표시. 사용자는 flag 된 페이지를 review 하고 결정.
- Compile-time + curation 컨텍스트라 lint 결과가 곧바로 사용자 의사결정 입력이 됨.

**(반증) Cognee `improve`**: 이전 카드 판은 `improve` 를 semantic lint 2번째 사례로 잠정 등재했으나 src 분석으로 반증 (`notes/techniques/cognee.md`). `memify_pipelines/` 5파일 — `apply_feedback_weights`, `consolidate_entity_descriptions`, `create_triplet_embeddings`, `memify_default_tasks`, `persist_sessions_in_knowledge_graph` — 모두 apply/consolidate/create/persist 동사. **detect/validate/flag 동사 0건**. orphan/contradiction/superseded claim 탐지 부재. → consolidation+feedback 분지로 이동.

**잠재 2사례 후보** (조건부):
- **Zep fact invalidation**: 시간축 invalidation 이지 orphan/contradiction 탐지가 아니라 약한 후보. Zep deep-dive 시 정밀 판정 필요.
- **Letta 내부 memory block 정리 루틴**: docs 에 명시된 detect 동사 없음 (Letta deep-dive 검색 결과). Cognee 와 같은 패턴으로 반증될 가능성.
- **상업 에이전트 메모리 dedup**: 재수집 필요 (ChatGPT/Claude/Devin memory 페이지 source thin).

**잠재 3+ 사례 후보**: Mem0 의 `arbitration` 로직 (last-write-wins 자체는 consolidation 이지만 그 전에 detect 단계가 있는지 확인 필요).

**핵심 관찰**: semantic lint 는 *"detect → flag"* 패턴이 핵심. additive 도구(consolidate/enrich) 와 동사가 다르다. 분지 판정 시 docs 의 추상 어휘(*"improve"*, *"refine"*) 가 아니라 src 의 함수 이름을 봐야 함.

---

### 3. Incremental update — 재추출 비용 통제

**정의**: 전체 재빌드 비용을 줄이기 위해 *"바뀐 부분만"* 재처리. 파일 해시·timestamp·git diff 기반. Lint 라기보다 운영 최적화이지만 *"오래된 산출물 감축"* 기능을 공유하므로 같은 매트릭스에 포함.

**1사례 — Graphify `--update` / `--watch`** (`notes/techniques/graphify.md`):
- 파일 해시 캐시 → 변경된 청크만 재처리. 변경 없으면 LLM 호출 0회.
- AST 만 재실행, embedding 재생성 skip.
- `--watch` 는 inotify/FSEvents 기반 실시간 incremental.

**약한 2사례 — Basic Memory `sync --watch`**:
- 단순 파일 watcher. Graphify 처럼 정교한 해시 캐시 + LLM 호출 skip 메커니즘 부재.
- markdown 파일 변경 시 SQLite FTS5 인덱스 + FastEmbed 벡터 재생성. *"바뀐 파일만"* 처리하나 캐시 정밀도가 낮음.
- *"약한 2사례"* 라고 표시하는 이유: 분지 정의의 핵심(LLM 호출 비용 회피)이 약함. 임베딩 재생성 비용은 여전히 발생.

**잠재 2사례 강화 후보**: Cognee `add → cognify` 의 incremental mode (deep-dive 미답), Letta MemFS 의 partial recompile (changelog 0.19.7 *"Differential memory load"* 언급, 정밀 동작 미답).

**핵심 관찰**: 이 분지는 *"비용을 줄이는가"* 가 판정 기준. 단순 watcher 는 자동성은 있어도 비용 회피가 약하면 약한 사례. Graphify 의 *"LLM 호출 0회"* 는 강한 신호.

---

### 4. Consolidation + feedback refinement — 피드백 루프 additive 재조정

**정의** (2026-04-21 Cognee deep-dive 로 새로 분기): 피드백 루프를 통해 기존 지식에 *덧붙이는* 방식의 재조정. 삭제·탐지 동사 없이 apply/consolidate/create/persist/enrich/reflect 동사로 작동. 기본형 consolidation(Mem0 last-write-wins, Zep temporal invalidation, Basic Memory `move_note`/`edit_note`)보다 **피드백 루프 + LLM 재합성** 이 핵심.

**1사례 — Cognee `improve`** (`notes/techniques/cognee.md`):
- `memify_pipelines/` 5단 — feedback weight 스트리밍(positive 가중·negative 감쇠), 세션 QA → permanent graph 승격, entity description LLM 재합성, triplet embedding, 세션 cache 역방향 sync.
- 단일 시스템 내 4단 파이프라인. Actor 분리 없음.
- `remember(self_improvement=True)` 기본값 — 자동 트리거 가능.

**2사례 — Letta `reflection` subagent** (`notes/techniques/letta.md` Q2):
- 별도 subagent (`src/agent/subagents/builtin/reflection.md`): *"You are a reflection subagent — a background agent that asynchronously processes conversations after they occur, similar to a 'sleep-time' memory consolidation process"*.
- 4-step 루프: identify mistakes → analyze user feedback → propose memory updates → git commit & push.
- Letta Code 한정, MemFS git worktree 비동기 격리.
- Trigger 옵션: `Off` / `Step count` / `Compaction event` (recommended).

**같은 분지 내 차이**: Cognee = 단일 시스템 + feedback weight 정량값(α). Letta = actor 분리 + git commit 영속 + mistake-driven 정성 LLM 분석. **같은 추상 (피드백 → 재조정 → 영속), 다른 구현 (단일 vs actor 분리, 정량 vs 정성)**.

**잠재 3+ 사례 후보**:
- **Hermes `self-improving loop`** (`notes/agents/hermes.md`): skill-generation + 자체 평가 루프. 본 분지의 변형으로 등재 가능, deep-dive 미수행이라 잠정.
- **Anthropic `compound engineering`**: Evaluator-Optimizer 의 다회 반복 + 결과를 spec 으로 환류 (`primitive-evaluator-optimizer-diffusion.md` 참조). 본 분지와 Evaluator-Optimizer 의 교집합.
- **Ouroboros**: spec-edit 루프. 마찬가지로 교집합.

**핵심 관찰**: 이 분지는 *"피드백 신호 → 지식 변형"* 이 핵심. 단순 consolidation(Mem0 dedup, Zep 시간축 invalidation) 과 다른 점은 **피드백 루프** 의 명시성. 피드백이 없으면 그냥 consolidation 분지(별도). 피드백이 있으면 본 분지.

**Evaluator-Optimizer 와의 관계**: `primitive-evaluator-optimizer-diffusion.md` 의 Evaluator-Optimizer 루프와 본 분지는 **교집합** — Evaluator 가 *"지식 노후화 판정자"* 인 특수형이 본 분지 + semantic lint 분지. 즉 두 카드는 lint/refinement 차원에서 직접 교차한다.

---

## Forgetting — 매트릭스 외부 별도 차원

위 4분지 모두 *"유지·개선"* 성격. **Forgetting 은 "소멸"** 이라 다른 차원으로 유지. 사례 분류:

| 메커니즘 | 사례 | 트리거 |
|---|---|---|
| TTL 자동 감쇠 | Mem0 (관찰), Zep (관찰) | 시간 기반 |
| Graph invalidation | Zep `invalid_at` (temporal KG) | 신규 사실로 모순 발생 시 |
| 명시적 dataset 삭제 | Cognee `forget(everything=True/dataset/data_id)` | 사용자 호출 |
| 파일 삭제 | Basic Memory (rm note), Letta MemFS (git rm) | 사용자 호출 |
| 자동 압축 (loss-y) | Letta `compaction` 4 modes (~30% 요약) | 컨텍스트 초과 |

**Cognee 는 TTL 자동 forget 부재** (deep-dive 결과 — 사용자 주도 3단 scope 만). Letta 의 `compaction` 은 자동이지만 conversation history 만 대상이고 memory blocks/MemFS 는 영속. 즉 자동 forget 의 정의 자체가 시스템마다 다름. **forget 매트릭스 자체가 별도 카드 후보** 일 수 있으나 현재는 사례 5개로 묶여있는 짧은 관찰 수준.

---

## 횡단 관찰

### 분지 판정 결정 트리

분지가 모호한 도구를 만났을 때 다음 순서로 판정:

1. **src 의 함수 이름이 detect/validate/flag/find_orphans 류인가?** → semantic lint.
2. **src 의 함수 이름이 verify/repair/schema_validate/diff 류이고 LLM 호출 없이 결정 가능한가?** → structural lint.
3. **src 의 함수 이름이 apply/consolidate/create/persist/enrich/reflect 류이고 피드백 신호가 입력으로 들어가는가?** → consolidation + feedback.
4. **src 의 함수 이름이 update/rebuild/watch/sync 류이고 비용 회피(LLM 호출 skip 포함) 가 핵심 motivation 인가?** → incremental update.
5. **위 어디에도 안 맞으나 *"기존 지식을 다룬다"* 면** → forgetting 또는 신규 분지 후보.

이 결정 트리가 Cognee `improve` 를 semantic lint 에서 consolidation+feedback 로 옮긴 결정적 기준이었다.

### Actor 구조의 두 위상

Consolidation+feedback 분지 내에서 actor 위상이 두 가지로 갈린다:
- **단일 시스템 내 파이프라인** (Cognee `improve` = `memify_pipelines/` 5단 in-process).
- **별도 actor 분리** (Letta `reflection` = subagent + git worktree 격리).

후자는 *"메인 agent 의 컨텍스트 오염 방지 + 비동기 처리 + git 단위 audit trail"* 이 부수 이득. 전자는 *"트랜잭션 단순함 + 즉시 활용"* 이 강점. 두 위상이 **trade-off** 이라 어느 쪽이 우월하다고 단정 불가. 이식 시 대상 시스템의 컨텍스트 예산이 빡빡하면 후자, 풍부하면 전자가 자연스러운 선택.

### LLM 호출 빈도 스펙트럼

| 분지 | 호출 빈도 | LLM 신뢰도 의존 |
|---|---|---|
| Structural lint | 매우 낮음 (Basic Memory: 0회, Letta: 자기 컨텍스트 평가에만) | 낮음 |
| Semantic lint | 중간 (corpus 단위 grader 호출) | **매우 높음** (grader 신뢰도 = `primitive-evaluator-optimizer-diffusion.md` 의 핵심 위험) |
| Incremental update | 매우 낮음 (Graphify: 변경 청크만, 0회 가능) | 낮음 |
| Consolidation + feedback | 높음 (entity description 재합성, reflection 분석 등 매 사이클) | 중간 (생성자가 evaluator 가 아니라 개선자 역할) |

이 스펙트럼이 분지 선택의 비용 모델을 결정. semantic lint 가 가장 위험한 분지 — grader 가 잘못 판정하면 *"멀쩡한 지식이 stale 로 표시*" 되는 false positive 가 반복적으로 누적된다.

---

## 구성 요소 (이식 가능한 단위)

### 1. 동사 시그니처 분류기

새 시스템의 메모리/지식 도구를 분류할 때 **함수 이름·docstring 의 동사** 를 결정 트리(위 횡단 관찰)에 입력. docs 의 마케팅 단어(*"improve"*, *"refine"*, *"smart"*) 는 무시. 이 분류기 하나만으로 운영 분지가 정확히 잡힌다.

### 2. 자기진단 명령 (`/doctor`) 노출

Structural lint 의 핵심 패턴은 **사용자 호출 가능한 self-diagnose 명령** — Basic Memory `doctor` + Letta `/doctor` 둘 다 이 형태. 새 지식 레이어 도입 시 *"진단 → 처방 → 후속 조치"* 의 사용자 인터페이스를 1등급 시민으로 노출. 자동 백그라운드 점검만 두면 사용자가 시스템 상태를 알 수 없고, 자동 수정만 두면 신뢰가 안 쌓임.

### 3. Reflection actor 분리 (격리 + 영속)

Consolidation+feedback 분지에서 위상 선택 — Letta `reflection` 형태(별도 subagent + git worktree + 자동 commit) 가 컨텍스트 격리 + audit trail 두 마리 토끼를 잡음. 이식 시: (a) 메인 agent 의 컨텍스트 예산이 빡빡한가, (b) 변경 이력이 사용자에게 가시화돼야 하는가. 둘 중 하나라도 *"예"* 면 actor 분리 형태가 자연스러움.

### 4. Lint 분지 선택 결정 트리 (시스템 설계자 관점)

새 시스템 설계 시 4분지 중 *어느 것을 채택할지* 결정:

```
지식 레이어 운영 분지 선택
├─ 사용자가 자기 지식을 직접 본다 (markdown / git-tracked)
│  → structural lint 필수 (사용자가 *"내 지식이 깨졌나"* 묻는다)
│  → semantic lint 권장 (curation 컨텍스트면 lint 결과 = 사용자 입력)
│  → consolidation+feedback 선택적
├─ 사용자가 자기 지식을 직접 안 본다 (벡터 DB / 그래프 induction)
│  → consolidation+feedback 필수 (사용자가 못 본다면 시스템이 스스로 정리해야)
│  → incremental update 강력 권장 (재추출 비용 폭발 방지)
│  → semantic lint 선택적 (LLM grader 비용·신뢰도 trade-off)
│  → structural lint 백그라운드만 (사용자 직접 호출 불필요)
└─ 둘 다 (markdown primary + 벡터/그래프 secondary, e.g. Basic Memory)
   → 4분지 모두 권장 — 운영 비용은 자동성으로 흡수
```

### 5. 분지 confidence 등재 규칙 (carve-out 의사결정)

본 카드의 매트릭스 자체가 이식 가능한 단위. 신규 분지 후보가 등장할 때 다음 기준:
- **1 사례**: 분지 후보로 매트릭스에 등재. 카드 carve-out 보류.
- **2 사례 (서로 다른 시스템)**: 분지 확정. carve-out 가능.
- **2 사례 (같은 시스템 내 변종)**: 약한 사례, 1.5 로 카운트.
- **3+ 사례**: primitive 카드의 1등급 축으로 승격 검토.

이 규칙이 본 카드의 lint 분지를 *"각 cell 2 사례 도달 시 carve-out"* 으로 운영해 온 근거. 동일 규칙을 다른 매트릭스(forget 매트릭스, audit 매트릭스 등) 에 재적용 가능.

---

## 반례 / 한계

### 5 데이터포인트 — 일반화 risk

본 카드의 4분지는 5개 deep-dive(LLM Wiki / Basic Memory / Graphify / Cognee / Letta) 의 src 동사 분석에서 추출됐다. Mem0 / Zep / Letta server 의 sleep-time multi-agent / Hermes self-improving / 상업 메모리 3사 미수집. 이 8개를 추가하면 4분지 외 신규 분지 등장 가능. 특히 **Mem0 arbitration** 과 **Zep temporal invalidation** 은 본 매트릭스의 어느 분지에도 깨끗이 안 맞을 가능성.

### 분지 판정의 동사-only 기준 — 부분 정합성

src 동사로 분지를 판정한다는 결정 트리는 docs 의 마케팅 어휘 오염을 막는 강한 도구이지만, **동사 자체가 다중 의미** 일 수 있다. 예: Cognee `consolidate_entity_descriptions` 의 *"consolidate"* 가 본 카드에서는 additive enrichment(consolidation+feedback 분지) 신호로 해석됐지만, 다른 시스템에서 *"consolidate"* 가 dedup(forgetting 차원) 으로 쓰이는 경우 분지가 다르다. 결정 트리는 **동사 + docstring + 실제 호출 시 입력/출력** 3 신호 통합으로 운영해야 함.

### 본 카드와 `primitive-knowledge-layer-design-space.md` 의 직교성 주장 — 중간 confidence

운영 차원이 builder/storage/timing 3축과 직교라고 주장했으나, 5개 사례에서 (storage, lint 분지) 상관이 약하게 관찰됨 — markdown primary 시스템(Basic Memory, Letta MemFS) 둘 다 structural lint 채택, 그래프 induction 시스템(Cognee, Graphify) 은 incremental update + consolidation+feedback 채택. 직교가 아닌 **약한 상관** 일 가능성. 더 많은 데이터포인트로 검증 필요.

### Letta `/doctor` 의 LLM 의존성 — 분지 정의 모호성

Structural lint 정의는 *"LLM 호출 없이 결정적 판정"*. Basic Memory `doctor` 는 이 정의에 부합하나 Letta `/doctor` 는 *"context bloat"* 같은 평가에 LLM 호출이 들어감. 두 사례를 같은 분지에 묶는 것이 적절한지 의문. **분지 내 sub-spectrum** 으로 다루는 것이 정확할 수 있음 — *"순수 결정적"*(Basic Memory) vs *"LLM-assisted self-grade"*(Letta).

---

## 미답 / 다음 deep-dive 후보

### 매트릭스 빈 cell 채우기 우선순위

1. **semantic lint 2번째 사례** — 가장 시급. 후보:
   - Zep fact invalidation (temporal invalidation ≠ orphan 탐지라 조건부) — Zep deep-dive 시 정밀 판정.
   - Mem0 arbitration 전 detect 단계 (있다면).
   - Letta server-side multi-agent 의 sleep-time agent 가 conversation 분석 시 detect 동사 사용하는지 (deep-dive Q2 미답).
   - 상업 에이전트 메모리 dedup (재수집 필요).

2. **incremental update 강한 2번째 사례** — Basic Memory `sync --watch` 가 약한 2사례라 강한 사례 필요. 후보:
   - Cognee `add → cognify` incremental mode (deep-dive 미답).
   - Letta MemFS `Differential memory load` (changelog 0.19.7 언급, 정밀 동작 미답).
   - GraphRAG 계열 7종 중 incremental update 가 강한 사례 — 서베이에 *"7종 모두 offline graph precompute + online retrieval 2단"* 만 기록, incremental 정밀도 미수집.

3. **structural lint 3+ 사례** — 매트릭스 강화. 후보:
   - Cognee `eval_framework/` + `alembic/` 자기진단 도구.
   - Mem0/Zep CLI 헬스체크.

4. **consolidation+feedback 3+ 사례** — 분지 내 actor 위상 spectrum 정밀화.
   - Hermes self-improving loop (skill-generation).
   - Anthropic compound engineering 의 spec 환류.

### 직교성 검증

5 데이터포인트로는 *"운영 차원이 3축과 직교"* 주장 약함. 후속 deep-dive 5+ 건이 추가될 때 (storage, lint 분지) 상관표를 다시 그려서 직교 vs 약한 상관 vs 강한 상관 판정.

### Forget 차원 별도 카드 carve-out 후보

Forget 매트릭스가 5 메커니즘 × 5 시스템 으로 채워지면 별도 카드 carve-out. 현재는 본 카드 외부 단일 섹션으로 유지.

### Letta deep-dive 미답 항목 (해소 시 본 카드 보강)

Letta deep-dive 의 3개 미답 (alembic 자동성, MemFS git push 실패 fallback, reflection git worktree 격리) 가 해소되면:
- alembic 정책 → structural lint 분지의 *"자동 vs 명시"* 스펙트럼 정밀화.
- reflection 격리 → consolidation+feedback 분지의 *"actor 분리 위상"* 정밀화.

---

## 관련 카드 / 노트

### 모(母) 카드
- **`insights/primitive-knowledge-layer-design-space.md`** — 본 카드의 carve-out 출처. builder/storage/timing 3축과 본 카드의 운영 차원이 **직교 주장** (중간 confidence). 모 카드의 *"구성 요소 4 — 운영 프리미티브 분리"* 섹션이 본 카드로 이동, 모 카드는 짧은 reference 로 축소됨.

### 데이터 출처 (deep-dive 노트)
- **`notes/techniques/karpathy-llm-wiki.md`** — semantic lint 분지 1사례 (`Lint Workflow` 4 categories).
- **`notes/techniques/basic-memory.md`** — structural lint 분지 1사례 (`doctor` + `schema_infer/validate/diff`), incremental update 약한 2사례 (`sync --watch`).
- **`notes/techniques/graphify.md`** — incremental update 분지 1사례 강한 사례 (`--update`/`--watch` + 파일 해시 캐시).
- **`notes/techniques/cognee.md`** — consolidation+feedback 분지 1사례 (`improve` = `memify_pipelines/` 5단). semantic lint 가설 src 동사 분석으로 반증된 결정적 케이스.
- **`notes/techniques/letta.md`** — structural lint 2사례 (`/doctor` = `context_doctor`) + consolidation+feedback 2사례 (`reflection` subagent). 본 카드 carve-out 트리거.

### 횡단 연결
- **`insights/primitive-evaluator-optimizer-diffusion.md`** — 본 카드의 semantic lint + consolidation+feedback 분지가 Evaluator-Optimizer 의 특수형 (Evaluator 가 지식 노후화 판정자). 두 카드는 **lint/refinement 차원에서 교차**. Grader 신뢰도 위험은 두 카드 공통 우려사항.

### 잠재 연결 (사례 추가 시)
- **신규 카드 후보 `forget-strategies`** — 본 카드 외부 별도 차원. Mem0/Zep/Cognee/Letta/Basic Memory 의 forget 메커니즘 5종이 매트릭스 채우면 carve-out.
- **신규 sub-axis 후보 `audit-trail-vs-epistemic-confidence`** — Letta deep-dive 가 제기한 *"audit = 변경 이력(git/log) vs 추출 신뢰도(Graphify confidence 3-tier)"* 두 차원 분리. 모 카드의 축 4 후보 보강 시 본 카드와 연결.

---

## 카드 수명 / 갱신 트리거

### 다음 갱신 트리거 (우선순위 순)
1. **Mem0 또는 Zep deep-dive** — semantic lint 2사례 또는 incremental update 강한 2사례 등재 가능.
2. **Hermes deep-dive 보강** — consolidation+feedback 3사례 + actor 위상 spectrum 정밀화.
3. **Letta deep-dive 미답 3건 해소** — 두 분지 정밀화 (구체 사항은 *"미답"* 섹션).
4. **상업 메모리 3사 재수집** — opaque managed 시스템의 운영 분지 가시화.

### 카드 수명 종료 트리거
- 4분지 모두 5+ 사례 도달 시 본 카드는 *"확정 primitive"* 로 안정화, 모 카드의 5번째 축으로 승격 검토.
- 본 카드 매트릭스로 분류 불가능한 신규 운영 패턴 3+ 사례 등장 시 본 카드 deprecate 검토 (예상 가능성 낮음).
