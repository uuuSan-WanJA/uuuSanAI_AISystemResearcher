---
title: LLM 지식 레이어 설계 공간 — 3축 (builder / storage / timing) primitive
date: 2026-04-21
last_updated: 2026-04-21 (deep-dive 2건 반영 — Basic Memory / Graphify)
based_on:
  - notes/techniques/karpathy-llm-wiki.md
  - notes/techniques/basic-memory.md
  - notes/techniques/graphify.md
  - inbox/2026-04-21-graph-rag-survey.md
  - inbox/2026-04-21-memory-pkm-survey.md
  - inbox/2026-04-21-graphify-upstream.md
confidence: medium-high (16 데이터포인트 중 2건 deep-dive 완료, 나머지 14건 primary docs 스캔)
tags: [knowledge-layer, memory, rag, wiki, pkm, graph-rag, design-space, primitive, auditability-candidate]
---

## 한 줄 요약

LLM 지식 레이어 설계 공간은 **builder · storage · timing** 3축으로 분해되며, 서베이 14종 + deep-dive 2건(Basic Memory, Graphify)을 통해 **curation + markdown + compile-time** 상한점은 **Karpathy LLM Wiki 단일 표본**으로 축소됐다 — Basic Memory 는 `co-authored + markdown + runtime` 으로 storage 1축만 일치하는 친족일 뿐이고, Graphify 는 `induction + KG + compile-time` 으로 서베이 7종 그래프 RAG 와 동일 좌표에 합류해 **"curation + KG" 조합은 여전히 공백**. Deep-dive 는 추가로 (a) 축 2(storage)가 배타적 값이 아니라 **primary + secondary surfaces 벡터**라는 재해석, (b) Graphify `EXTRACTED/INFERRED/AMBIGUOUS` 3-tier 로 촉발된 **축 4 후보 '감사 가능성(auditability)'**, (c) Lint 연산의 3분지(structural / semantic / incremental-update) 를 드러냈다.

---

## 패턴 / 주장

지식을 LLM에 "DB로 붙이는" 프레임워크들은 표면적으로는 다 다르지만, 실제로 결정이 일어나는 축은 세 개로 압축된다.

**축 1 — Builder (누가 지식을 쓰는가)**

- *induction*: LLM이 입력(문서/대화)에서 엔티티·관계·사실을 자동 추출. Microsoft GraphRAG, LightRAG, HippoRAG, PathRAG, Cognee, Neo4j LLM-GB, nano-graphrag (그래프 7종 전부) / Mem0, Zep, 상업 메모리 3사.
- *self-editing*: 에이전트가 자기 메모리 블록을 도구 호출로 편집. Letta (MemGPT 계보).
- *co-authored*: 사용자와 LLM이 같은 파일을 편집. Basic Memory.
- *curation*: 사람이 `raw/`를 선별하고 LLM은 `wiki/`를 빌드하되 사용자 승인·검토를 전제. **Karpathy LLM Wiki**.

**축 2 — Storage primitive (무엇에 쓰는가)**

- *벡터 DB*: Mem0, Khoj, AnythingLLM — 의미 검색 강함, 사용자 가독성 0 (opaque chunks).
- *지식 그래프 (induction)*: GraphRAG / LightRAG / HippoRAG / PathRAG / Cognee / Neo4j / nano-graphrag — 엔티티·관계 추출 후 인덱싱.
- *temporal KG*: Zep + Graphiti — 엣지에 `valid_from/invalid_at` 타임스탬프 (bi-temporal).
- *릴레이셔널 + memory blocks*: Letta — Postgres/SQLite 에 labeled block 단위, MemFS 는 git-tracked 방향으로 분기.
- *markdown 파일시스템*: **LLM Wiki, Basic Memory** — 사용자 가독·버전관리·포팅 가능.
- *opaque managed*: ChatGPT/Claude/Devin memory — 편집 가능한 짧은 bullet 목록만 노출.

**축 3 — Timing (언제 지식이 형성되는가)**

- *compile-time, 정적 스냅샷*: **LLM Wiki** (ingest 시점에 요약·상호연결·index 업데이트 후 고정).
- *runtime, 증분*: Mem0 / Zep / Letta / Basic Memory (대화·이벤트가 오는 대로 갱신).
- *offline precompute + online retrieval 2단*: GraphRAG 계열 7종 (무거운 인덱싱 후 질의 시 가벼운 검색).

**핵심 주장**: 이 세 축이 서로 직교인 것처럼 보이지만, 실제 구현체들은 **induction + graph/vector + runtime** 조합으로 수렴한다. 단순히 "자동화가 편해서"이지 로지컬 필연 때문이 아니다. *curation + markdown + compile-time* 에 **LLM Wiki 단 하나**(+ 파생 오픈소스 3종)만 있고, Graphify 가 "curation+KG 공백" 후보로 기대됐으나 deep-dive 결과 `induction + KG + compile-time` 으로 판정돼 서베이 7종 그래프 RAG 와 같은 좌표에 합류했다 — **공백은 재확증**. Basic Memory 는 `co-authored + markdown + runtime` 으로 LLM Wiki 와 3축 중 1축(storage)만 일치하는 **부분 친족** 이었다.

**축 2 재해석 (deep-dive 강제)**: 최초 카드는 storage 를 markdown / 벡터 / KG / temporal KG / ... 의 **배타적 단일값** 으로 다뤘으나, deep-dive 는 이것이 틀렸음을 보여줬다 — Basic Memory 는 markdown(primary) + SQLite FTS5 + FastEmbed vector(v0.19.0, 2026-03-07 도입) **3중 레이어**, Graphify 는 추출 결과를 HTML + JSON + markdown + Obsidian vault + Neo4j + MCP server + `--wiki` agent-crawlable 등 **6+ 표면에 동시 fan-out**. 축 2 는 *primary storage(사용자 소유 형식)* + *secondary surfaces(파생 소비자 표면)* 2-component 벡터로 재정의되어야 한다. "markdown vs 벡터" 는 primary 선택일 뿐, secondary 에선 대부분 공존.

---

## 근거가 되는 관찰

**그래프 RAG 7종 모두 induction 계열**

Graph-based 지식 레이어 서베이(`inbox/2026-04-21-graph-rag-survey.md`)의 공식 결론: "모두 entity + relation 추출을 LLM으로 수행 (spaCy 등 전통 NLP 위주 프로젝트는 없음)", "모두 offline graph precompute + online retrieval 2단 구조", "curation (human-written, compile-time) 축에 있는 프레임워크는 이 조사에서 발견 안 됨". 차이는 retrieval primitive(community summary / dual-level / PPR / path pruning / auto-route API) 뿐이고, builder 축은 전부 자동 induction.

**메모리/PKM 7종의 builder 분포**

Memory & PKM 서베이(`inbox/2026-04-21-memory-pkm-survey.md`)에선 builder 축이 갈라진다 — Mem0/Zep/상업 3사는 induction, Letta 는 self-editing, Basic Memory 는 co-authored, Khoj/AnythingLLM 은 retriever-only(builder 아님). **curation 축에 도달한 사례 없음**. Basic Memory 가 가장 근접하지만 "대화 중에 LLM이 같이 쓴다"는 점에서 LLM Wiki의 compile-time curation 과 정확히 같지는 않다.

**LLM Wiki 노트 내부 증언 — 16M 뷰 + 1주일 7+ 오픈소스**

`notes/techniques/karpathy-llm-wiki.md` 기록: X에서 16M+ 뷰, gist 5,000+ 스타, 1주일 내 Agent Skills·MCP·세션로그 인제스트형 오픈소스 구현체 7+ 개 등장. 이 반응은 curation+markdown+compile-time 조합이 **수요가 있으나 공급이 없던 공백**이었다는 시장 신호. 기존 프레임워크들이 이 조합을 의식적으로 기피한 게 아니라 **자동화 내러티브에 매몰돼 탐색 자체를 안 한 것**으로 읽힌다.

**Storage → UX 인과 체인 (memory 서베이 cross-cutting 관찰 인용)**

- 벡터 DB → 의미 검색 강함, 사용자 "내 지식" 직접 읽기 불가능.
- markdown → 사용자가 볼 수 있고 복사·버전관리·포팅 가능, 대신 의미 검색·시간 축 약함.
- Temporal graph → "언제 유효했던 사실인가" 재현, 대신 내부 상태 성격이라 UX 노출 거의 없음.
- Opaque managed → UX 단순화 극대, 포팅 사실상 불가.

이 인과는 축 2(storage) 선택이 축 1(builder)·축 3(timing)을 강제하는 상관을 낳는다. 벡터 DB 고르면 induction·runtime 이 거의 강제되고, markdown 고르면 curation·compile-time 이 합리적 선택이 된다. **축들이 독립 차원처럼 보이나 실전에선 강하게 상관**.

**Letta MemFS 의 수렴 신호 (1개 사례, 트렌드 확정 어려움)**

Letta의 원래 구조(core/archival/recall 3단 릴레이셔널)에 최근 "MemFS" 가 추가된 움직임 — 공식 docs 의 "git-tracked memory" 표현. 자동 induction/self-editing 쪽에 있던 프레임워크가 markdown·버전관리 쪽으로 한 걸음 당겨지는 **단일 수렴 신호**. 다만 1개 사례라 일반화는 불가. LLM Wiki 반향의 **영향일 수도**, **독립 수렴일 수도** — 서베이로는 판정 불가.

**Cognee `improve` 연산 — LLM Wiki `Lint` 와 개념 중첩**

Cognee 는 `remember/recall/forget/improve` 4-op API 를 agent memory 프레임워크 수준 추상화로 노출한 드문 사례. 이 중 `improve` 는 LLM Wiki 의 Lint Workflow (orphan/contradiction/stale claim/missing concept 점검) 와 개념적으로 동일. 축 1(induction)·축 2(hybrid storage) 에서 멀리 떨어진 두 프레임워크가 **동일한 운영 문제**(지식 노후화)에 대해 유사 대응을 독립 발명함. 이는 축과 무관한 **운영 프리미티브**(refinement/lint)가 별도 축일 가능성을 시사 — 본 카드에선 가설로만 기록.

**Basic Memory deep-dive — "가장 가까운 형제" 가설 재정의**

`notes/techniques/basic-memory.md` 판정: **co-authored + markdown + runtime** (LLM Wiki = curation + markdown + compile-time). **3축 중 1축(storage)만 일치**. 구체적으로:

- *Builder 불일치*: LLM Wiki 는 사용자가 `raw/` 를 선별하고 LLM 이 `wiki/` 를 빌드하는 비대칭 구조(사용자 승인 전제). Basic Memory 는 대화 중 LLM이 `write_note`·`edit_note` 로 직접 쓰고 사용자가 Obsidian/VS Code 로 동시 편집 — 진정한 co-authored.
- *Timing 불일치*: LLM Wiki 는 ingest 시점에 상호연결까지 해둔 정적 스냅샷. Basic Memory 는 `basic-memory sync --watch` 로 실시간 증분 + MCP 도구 호출 시 재인덱싱.
- *Storage 2-component*: primary = markdown 파일(진실), secondary = SQLite(FTS5) + FastEmbed vector(v0.19.0+) **하이브리드 인덱스**. markdown 단일 축에 있지 않음.
- *`memory://` URL + recursive CTE 그래프 탐색*: wikilink 기반 graph traversal 을 MCP 도구(`build_context(depth, timeframe)`) 로 노출 — 사용자 명시 엣지(자동 induction 아님) 기반 그래프라 **curation + graph 조합의 인접 사례**. 다만 "엣지를 사람이 쓴다" vs "그래프 추출이 자동" 경계가 불분명.

LLM Wiki 의 "가장 가까운 형제" 는 **단일 점이 아니라 3축 공간 내 1-hop 이웃들의 집합**으로 재정의. Basic Memory 는 storage-축 1-hop 이웃이지, 전체적 형제는 아님.

**Graphify deep-dive — 공백 메움 실패 + 축 4 후보 등장**

`notes/techniques/graphify.md` 판정: **induction + KG + compile-time 지배** (LLM 호출은 빌드 시점 서브에이전트 청크 dispatch 3곳에만 집중). 서베이 7종 그래프 RAG 와 동일 좌표 — primitive 카드가 기대했던 "curation+KG 공백 메움" 가설은 **반증**. Graphify 는 `/graphify add <url>` 로 raw 수집·markdown 변환까지 자동화하므로 curation 마찰을 오히려 낮추는 induction 극대화 방향.

그러나 deep-dive 는 2개의 독립 발견을 추가했다:

- *Storage 축 다중점유 (축 2 재해석 증거 2)*: HTML + JSON + markdown + Obsidian vault + Neo4j Cypher + MCP stdio + `--wiki` agent-crawlable 까지 **6+ 표면 fan-out**. 단일 추출 결과가 다수 소비자에게 동시 노출되는 아키텍처. primary 는 `graph.json`, secondary 는 사용처에 따라 선택.
- *Confidence 3-tier = 축 4 후보*: 모든 엣지에 `EXTRACTED(1.0) / INFERRED(0.4–0.9) / AMBIGUOUS(0.1–0.3)` 의무 태깅. skill *Honesty Rules* 섹션: *"Never invent an edge. If unsure, use AMBIGUOUS."* — 추출 결과의 **감사 가능성(auditability)** 을 프레임워크 1등 시민으로 승격한 단일 사례. 서베이 14종 + Basic Memory 중 이런 축을 명시한 경우 없음. **새 축 4 후보 등재, 2번째 사례 대기**.
- *Lint 3분지*: Graphify 의 `--update`·`--watch` 는 **incremental update** (파일 해시 캐시로 LLM 재호출 없이 AST 만 재실행). Basic Memory `doctor` + `schema_infer/validate/diff` 는 **structural lint** (파일↔인덱스 정합성·스키마 드리프트). Cognee `improve` + LLM Wiki `Lint` 는 **semantic lint** (의미적 노후화·모순·orphan). 이 3분지는 `knowledge-lifecycle-operations` 후보 카드가 **3개 하위 차원** 을 필요로 함을 확정.

---

## 구성 요소 (이식 가능한 단위)

**1. 포지셔닝 매트릭스 — 도입 전 3축 결정 의무화**

새 지식 레이어를 설계·도입할 때 builder·storage·timing 각 축의 목표 위치를 문서로 먼저 박아라. "LLM이 쓴다" 를 기본값으로 두지 말고 네 가지(induction/self-editing/co-authored/curation) 중 하나를 **의도적으로 선택**. 스토리지도 마찬가지 — "벡터 DB" 가 기본이라고 가정하면 UX 결과(사용자 가독성 0)가 자동으로 따라온다. 타이밍은 compile-time 과 runtime 의 비용·반응성 트레이드오프가 다르므로 명시.

**2. Storage → UX 의존성 표 (primary storage 기준, 사용자 소유권 관점)**

| Primary storage | 사용자 읽기 | 버전관리 | 포팅 | 의미검색 | 시간축 |
|---|---|---|---|---|---|
| markdown | ○ | ○ (git) | ○ | △ (secondary 로 벡터 얹으면 ○ — Basic Memory 가 이 방향) | × |
| 벡터 DB | × | × | × | ◎ | × |
| KG (induction) | △ (시각화 가능) | × (실시간 그래프) | △ | ○ (graph traversal) | × |
| Temporal KG | × | × (append-only 로그는 ○) | × | ○ | ◎ |
| 릴레이셔널 blocks | △ | △ (MemFS = git-tracked 시) | △ | △ | × |
| opaque managed | △ (bullet 목록만) | × | × | ? | ? |

**중요**: 이 표는 *primary storage* (진실의 저장소) 기준. Secondary surfaces (HTML/JSON/벡터 인덱스/Neo4j/MCP 서버 등)는 거의 모든 프레임워크가 다수 제공하므로 축 2 는 2-component 벡터로 읽어야 함.

- Basic Memory: primary = markdown, secondary = SQLite FTS5 + FastEmbed vector.
- Graphify: primary = `graph.json` (파이프라인 진실), secondary = HTML/Obsidian/Neo4j/MCP/wiki.
- LLM Wiki: primary = markdown, secondary = index.md(자체 markdown, 별도 인덱스 없음).
- Mem0: primary = 벡터 DB, secondary = (선택) 그래프 스토어.

"사용자가 자기 지식을 **소유·포팅·버전관리** 해야 한다" 가 요구사항이면 **primary storage** 가 markdown(또는 git-tracked blocks)여야 함. Secondary 에 벡터/그래프가 얹히는 것은 요구사항과 모순되지 않음.

**3. 축들의 상관 끊기 — 의도적 직교화**

대부분의 프레임워크가 induction+벡터+runtime 또는 induction+KG+offline-precompute 로 뭉친 이유는 구현 편의. **의도적으로 축을 끊으면** 새로운 설계 공간이 열린다:
- *curation + KG*: 사람이 raw 를 선별하고 LLM은 그래프를 자동 추출 (현재 공백).
- *curation + temporal + markdown*: Wiki 에 `valid_from/invalid_at` 프론트매터를 추가 (LLM Wiki 의 "Superseded claims" 플래그를 시계열화).
- *induction + markdown + compile-time*: LightRAG 의 추출 파이프라인을 LLM Wiki 의 markdown 출력 포맷으로 (Astro-Han 의 Agent Skills 포장이 이 방향 근접).

이 세 조합은 모두 서베이에 부재. 설계 공백이 곧 기회 영역.

**4. 운영 프리미티브 분리 — 축 3종 밖의 공통 프리미티브**

Lint/Refinement, Consolidation, Forgetting 은 축 1·2·3과 무관한 별개 운영 차원. Deep-dive 2건 이후 **Lint 는 3개 하위 차원** 으로 분화됨이 확정:

- **Structural lint** — 스키마 정합성, 파일↔인덱스 동기화 드리프트 탐지. 예: Basic Memory `schema_infer/validate/diff` (v0.19.0, 2026-03-07), `basic-memory doctor` (v0.17.4, 2026-01-05). 기계적·결정적 판정 가능.
- **Semantic lint** — 의미적 노후화, 모순, orphan, stale claim 탐지. 예: Cognee `improve`, LLM Wiki `Lint Workflow`. LLM 기반 판정 필요, 자동화에 Grader 신뢰성 이슈 동반(cf. `primitive-evaluator-optimizer-diffusion.md`).
- **Incremental update** — 재추출 비용 통제, "바뀐 부분만" 재빌드. 예: Graphify `--update`·`--watch` (파일 해시 캐시 → LLM 호출 0회로 AST 만 재실행), Basic Memory `sync --watch`. Lint 라기보다 운영 최적화.

Consolidation(Mem0 last-write-wins ↔ Zep temporal invalidation ↔ Basic Memory `move_note`·`edit_note`), Forgetting(TTL / graph invalidation / 파일 삭제) 도 별도 차원. 새 카드 후보: **knowledge-lifecycle-operations** — 3개 하위 차원(structural/semantic/incremental) × 3개 운영(lint/consolidation/forgetting) = 9-cell 매트릭스로 carve out 대기. 현재 Basic Memory(structural lint O, semantic X), Graphify(incremental update O, semantic X), LLM Wiki·Cognee(semantic O) 로 3분지 확정.

**5. Builder 축의 경제적 해석**

- induction = "시간 × 토큰 비용" 선결제. 대량 데이터를 빠르게 indexable 하게 만듦.
- curation = "저자 주의력" 선결제. 작은 corpus 를 밀도 있게.
- self-editing = "에이전트 컨텍스트 토큰" 실시간 결제.
- co-authored = 저자-에이전트 공동 결제, 동기화 비용 발생.

스케일(소스 수 × 질문 빈도) 이 작으면 curation 이 경제적, 커질수록 induction 이 유일 옵션이 됨. LLM Wiki 노트의 ~100 소스 붕괴점이 이 경제 논리의 수치 버전.

**6. 축 4 후보 — 감사 가능성 (auditability) — 2026-04-21 등재, 1사례**

Graphify 의 `EXTRACTED(1.0) / INFERRED(0.4–0.9) / AMBIGUOUS(0.1–0.3)` 의무 confidence 태깅 + *"Never invent an edge. If unsure, use AMBIGUOUS."* honesty rule 은 조사한 16개 데이터포인트 중 **단일 사례**. 다른 프레임워크는:

- GraphRAG/LightRAG/HippoRAG/PathRAG/Cognee/Neo4j/nano-graphrag: 엣지 confidence 를 선택 필드로 두거나 없음.
- Mem0/Zep: 메모리/엣지에 reliability 스코어 명시 안 함.
- LLM Wiki/Basic Memory: contradiction 플래그는 있으나 엣지 단위 confidence 없음.

**축 4 promotion 조건**: 2번째 사례 발견 시 공식 축으로 승격. 현재는 후보. 이 축이 의미 있다면 "감사 없는 induction" 이 지형의 기본값이고 Graphify 가 그 반례인 셈 — 대부분의 프레임워크는 추출 결과를 **bit-level 정확성** 기준이 아닌 **유용성** 기준으로만 평가.

**7. Tier 분류 — Cross-cutting skill 후보 (meta/harness_schema.md 영역)**

Graphify 는 단일 PyPI 패키지 + 하네스별 skill adapter 로 Claude Code / Codex / Cursor / Aider / Gemini CLI / Copilot CLI / OpenClaw / Factory Droid / Trae / Hermes / Kiro / Google Antigravity 등 10+ 하네스에 **동시 배포**된다. 이는 현재 프로젝트의 4-tier(`harness/` / `agents/` / `infra/` / `techniques/`)에 깔끔히 맞지 않는 **cross-harness 수평 skill**. 일단 `techniques/` 유지하되 2번째 사례 발견 시 **`skills/` 또는 `cross-cutting/` 신규 tier** 제안 — `meta/harness_schema.md` 의 META-tier 축에 기록 후보.

---

## 반례 또는 한계

**서베이 깊이 — primary docs 스캔 수준**

14개 프레임워크는 각각 1–2개 primary source(README·공식 docs·논문 초록) 수준으로만 확인됨. 각 프레임워크의 내부 프롬프트·실제 토큰 비용·production 후기는 미수집. 축 구분이 "공식 self-description 기준"이라 실제 행동이 다를 수 있음. 특히 Letta MemFS, Cognee `improve`, Zep fact invalidation 의 구현 세부는 재확인 필요.

**상업 제품 3종(ChatGPT/Claude/Devin memory) source thin**

`inbox/2026-04-21-memory-pkm-survey.md` 에 명시됐듯 Anthropic Claude Memory 공식 페이지 404 리다이렉트, ChatGPT Memory FAQ 403. 상업 메모리의 구체 동작은 이 카드에서 "opaque managed" 로만 묶였는데, 재수집 후 이 묶음이 유의미한지 재검증 필요.

**"지식 vs 상태 메모리" 경계 모호**

이 카드가 같은 축에 놓은 것들 — Mem0(사용자별 에피소딕 사실), Zep(대화 이력 KG), LLM Wiki(저자가 선별한 문서 corpus), Basic Memory(공동 저작 노트) — 는 "지식" 의 정의가 다를 수 있다. Mem0 의 "사용자가 커피를 안 마신다" 같은 사실 조각과 LLM Wiki 의 "Karpathy 의 LLM Wiki 패턴은 ~" 같은 개념 페이지를 같은 스펙트럼에 놓는 것의 타당성은 **열린 질문**. 이 prime 카드는 일단 모두 묶어서 공간을 그렸지만, 후속 카드에서 **에피소드-vs-자산 축** 을 별도로 분리할 가능성 있음.

**축 상관 현상을 "관성" 으로 단정한 주장**

"축들이 induction+벡터/graph+runtime 으로 뭉친 건 설계자 관성" 이라는 이 카드의 주장은 해석이지 증거가 아님. 실제로는 (a) 벤치마크 리더보드가 induction 기반 평가 중심이라 induction 편향이 훈련된 것, (b) runtime 이 SaaS 수익모델에 유리한 것, (c) curation 은 사용자 노동 비용이 높아 frictiom 큰 것 등 구조적 이유도 있음. "공백을 기회로 읽을 수 있다" 는 주장은 유지하되, 공백의 **원인** 에 대해선 보수적으로 기록.

---

## 전제 / 선행 조건

- **지식 레이어가 필요한지 선검증**: 에이전트가 in-context 만으로 해결되는 태스크에 지식 레이어를 얹으면 복잡도만 늘어남. Anthropic `building-effective-agents` 의 "augmented LLM 우선, 필요할 때만 프레임워크" 원칙.
- **정의 합의**: "지식", "메모리", "상태" 를 같이 논의할 때 각 프로젝트에서 경계가 다름. 팀·개인 레벨에서 이 3개를 어떻게 나누는지 사전 정렬.
- **스케일 추정**: 소스 수 × 질문 빈도 × 기대 수명 을 미리 추정해야 축 선택이 타당. 100 소스/일 50 질문/6개월 vs 10만 문서/일 10k 질문/5년 은 완전히 다른 설계.

---

## 내 프로젝트에 적용한다면 (Phase 2 후보)

Phase 2 진입 시 사용자의 다른 프로젝트(예: 게임메이커, 다른 리서치 저장소)에 지식 레이어를 얹을 필요가 생기면 이 카드를 먼저 꺼내 포지션을 결정:

1. **축 1 결정**: 사용자가 원하는 "LLM 이 얼마나 자율적으로 쓰길 바라는가" — 전적으로 자동(induction) ↔ 완전 사용자 소유(curation) 스펙트럼에서 위치 고르기. 이 프로젝트의 현재 구조(사용자가 `notes/` 를 큐레이트, LLM 이 probe 로 보조)는 이미 **curation+markdown+compile-time** 에 있으므로, 새 프로젝트에도 같은 축으로 시작하는 것이 일관성 유리.
2. **축 2 결정**: 사용자 소유·포팅·버전관리 요구사항이 있는가. 있으면 markdown (Basic Memory / LLM Wiki 형) 선택. 의미 검색이 필수면 Graphify 같은 그래프 레이어를 markdown 위에 얹는 혼합.
3. **축 3 결정**: 지식이 빠르게 갱신되는가(runtime) 대부분 안정적인가(compile-time). 전자면 Basic Memory+MCP, 후자면 LLM Wiki 패턴+주기적 재컴파일.
4. **공백 영역 탐색**: 이 프로젝트 자체가 "하네스 리서치 corpus" 인데, 현재는 파일+index 구조 (compile-time curation)만 가졌음. **curation + KG 조합** (즉 `notes/` 위에 Graphify 로 그래프 레이어 추가)은 서베이에서 부재한 공백이라 직접 실험 가치 있음. 다만 graphify upstream 식별이 선행 조건(handoff 의 기존 대기 항목).

**주의**: 이 카드는 Phase 1 synthesis 결과이므로, Phase 2 graft-evaluator 로 사용자 프로젝트와 합류 시 "축 1·2·3 현재 위치" 를 먼저 매핑한 뒤 차이를 논할 것. 사용자 프로젝트에 대한 가정 없이 카드 자체는 일반 프레임으로 유지.

---

## 관련 primitive 카드 / 노트

- `notes/techniques/karpathy-llm-wiki.md` — 이 카드의 단일 표본 중심점. Wiki 의 축 1·2·3 위치는 (curation, markdown, compile-time). "커뮤니티 수용 — 한국어권" 섹션의 Graphify 포지셔닝 (2026-04-21 추가) 역시 이 설계 공간 해석에 기여.
- `notes/techniques/basic-memory.md` — 2026-04-21 deep-dive. 3축 판정 = (co-authored, markdown+hybrid index, runtime). "가장 가까운 형제" 가설 재정의의 증거.
- `notes/techniques/graphify.md` — 2026-04-21 deep-dive. 3축 판정 = (induction, KG+6표면 fan-out, compile-time). curation+KG 공백 재확증 + 축 4 후보(감사 가능성) 발견의 증거. cross-harness skill tier 후보의 1사례.
- `inbox/2026-04-21-graph-rag-survey.md` — 7종 primary source. 축 1 의 induction 편재 증거.
- `inbox/2026-04-21-memory-pkm-survey.md` — 7종 primary source. 축 2 의 storage→UX 인과 체인 원 출처.
- `inbox/2026-04-21-graphify-upstream.md` — Graphify upstream 식별 probe 결과. 사용자 로컬 스킬이 third-party 오픈소스의 설치본임을 확정.
- `primitive-evaluator-optimizer-diffusion.md` — 약한 연결: Evaluator-Optimizer 루프 내부에 "지식 축적" 이 발생하면 이 카드의 축들이 루프 안에 중첩 적용됨. 예: ECC instinct accumulation 은 축 1=curation+induction 혼합, 축 2=markdown+JSON, 축 3=runtime 이라고 해석 가능. 또한 semantic lint(Cognee `improve`, LLM Wiki `Lint`) 는 Evaluator-Optimizer 의 특수형(evaluator가 지식 노후화 판정자) 이라 두 카드는 **Lint 하위 차원에서 만남**.
- **후보 신규 카드 (본 카드에서 분기)**: `knowledge-lifecycle-operations` — 3 하위 차원(structural / semantic / incremental-update) × 3 운영(lint / consolidation / forgetting) = 9-cell 매트릭스. 현재 각 cell 별 사례:
  - *structural lint*: Basic Memory `schema_infer/validate/diff` + `doctor` (확정)
  - *semantic lint*: Cognee `improve` ≈ LLM Wiki `Lint Workflow` (확정)
  - *incremental update*: Graphify `--update` + `--watch` + 파일 해시 캐시 (확정)
  - *consolidation*: Mem0 last-write-wins ↔ Zep temporal invalidation ↔ Basic Memory `edit_note` (3분지 관찰됨, 정리 대기)
  - *forgetting*: TTL vs graph invalidation vs 파일 삭제 (미정리)
  Carve-out 시점: 각 cell 에 2+ 사례 확보되는 시점.

---

## 미답 / 열린 질문 (카드 갱신 트리거)

### 2026-04-21 deep-dive 로 해소된 항목
- ~~Basic Memory 내부 인덱스~~ → **해소**: SQLite FTS5 + FastEmbed vector hybrid (v0.19.0 / 2026-03-07 도입). primary markdown + secondary 인덱스 이중 구조로 판정.
- ~~curation+KG 조합의 현실 구현체 (Graphify 후보)~~ → **해소 (반증)**: Graphify 는 induction + KG + compile-time 이라 서베이 7종 그래프 RAG 와 동일 좌표. curation+KG 공백 재확증.
- ~~Cognee `improve` 구현~~ → **부분 해소**: Basic Memory `schema_infer/validate/diff` + `doctor` 와 Graphify `--update`·`--watch` 도입으로 Lint 3분지(structural / semantic / incremental) 확정. Cognee 자체 구현 세부는 여전히 미답 (Cognee deep-dive 대기).

### 남은/새로 생긴 열린 질문
- **축 4 promotion** — Graphify confidence 3-tier 의 2번째 사례. Hermes `self-improving loop` 에 confidence 가 있는지, OpenClaw gateway 의 에이전트 응답 로깅에 confidence 가 있는지 재확인 가치.
- **Basic Memory 충돌 해소 정책** — `write_note` / `edit_note` 의 last-write-wins 인지 merge 인지 공식 문서 범위 외 (Basic Memory deep-dive 보고에서 미답 플래그).
- **Letta MemFS 세부** — 축 2 가 관계형→markdown 으로 수렴 중인지 단일 사례로 판정 불가, 2번째 수렴 사례 발견 시 트렌드 확정. Letta deep-dive 필요.
- **"에피소딕 사실 vs 문서 자산"** 을 같은 축에 놓은 것의 타당성 — Mem0/Zep deep-dive 시 재평가. 현재까지 Basic Memory 는 **양쪽 단위가 markdown 파일 하나로 수렴**된 사례(사실 조각 = 짧은 observation 라인, 문서 자산 = 전체 파일) → "단위" 가 아닌 "밀도" 축일 가능성.
- **Cross-harness skill tier 판정** — Graphify 1사례. 2번째 사례 (예: 다른 PKM/analysis skill 이 유사 분포를 갖는지) 발견 시 신규 tier 확정.
- **Graphify 31.4k stars 의 일자별 곡선** — star-history 주간 +1.1k 만 확보. 실제 피크 이벤트(Karpathy 트윗 2026-04-02 → PyPI v0.1.1 2026-04-04 → 어느 시점부터 급상승) 미답.
