---
title: Cognee — agent memory engine (4-op API + knowledge graph)
date: 2026-04-21
source_url: https://github.com/topoteretes/cognee
source_type: repo / docs / pypi
topic: techniques
tags: [cognee, agent-memory, knowledge-graph, vector, relational, remember-recall-forget-improve, knowledge-lifecycle]
status: processed
---

## 요약 (3줄)

Cognee(Topoteretes, Apache-2.0, 2024-03 첫 릴리스 → 2026-04-18 v1.0.1)는 `remember/recall/forget/improve` 4-op API 를 **agent memory engine** 추상화로 노출한 파이썬 라이브러리 + 매니지드 클라우드. 내부는 **vector store + graph store + relational store 3중 스토리지**(로컬 기본, ChromaDB/Neo4j/Neptune/Postgres/Redis 스왑 가능) + **session cache (Redis/filesystem diskcache) → permanent graph bridging** 구조로, `improve` 는 **"additive enrichment"** 로만 작동(feedback weights 적용 + 세션 QA 를 graph 로 승격 + 엔티티 description LLM 재합성 + triplet embedding) 하며 **orphan/contradiction/stale claim 탐지는 미구현** — 따라서 **`improve` 는 LLM Wiki `Lint Workflow` 의 semantic lint 2번째 확정 사례로 성립하지 않고, "knowledge lifecycle operations" 카드의 별도 primitive (세션 consolidation + feedback weighting) 로 분기**해야 함. 엣지 confidence/provenance 는 relational store 의 "documents ↔ chunks ↔ provenance" 추적 수준에만 존재, 엣지 단위 신뢰도 3-tier 나 honesty rule 은 **공식 범위 외 — 축 4 (감사 가능성) 2번째 사례도 미성립**.

---

## 핵심 포인트

1. **4-op API 는 agent memory abstraction 의 일관된 표면**: `remember / recall / forget / improve`. `remember` 가 `add → cognify → improve` 를 기본으로 돌리는 오케스트레이션 래퍼, `recall` 은 auto-routing (summary / graph-traversal / temporal / code / lexical) 라우터, `forget` 은 dataset·item·user 단위 GC, `improve` 는 "이미 쌓인 그래프 위에 derived structure 를 더하는" 후행 enrichment.
2. **Session ↔ Permanent 이중 메모리**: `(user_id, session_id)` 키로 Redis 또는 `{DATA_ROOT_DIRECTORY}/.cognee_fs_cache/sessions_db` (diskcache) 에 보관되는 단기 캐시 + Postgres/Neo4j 등에 저장되는 장기 KG. `recall` 은 세션 먼저 keyword 검색 → miss 시 permanent graph fallthrough, 결과에 `_source="session" | "graph"` 태그. 세션의 영구화는 `improve` (혹은 `persist_sessions_in_knowledge_graph` memify 파이프라인) 호출 시에만 — **자동 백그라운드 sync 가 기본은 아님** (docs 에 "can be persisted" 로 선택적 표현).
3. **3중 스토리지 설계**: vector store (semantic similarity), graph store (entities + edges), relational store (documents · chunks · provenance 추적). 로컬 기본 + 프로덕션 스왑. 지원 DB: ChromaDB · Neo4j · Neptune · Postgres · Redis (PyPI 의존성으로 확인).
4. **`improve` 는 rewriting 이 아닌 additive enrichment 4단 파이프라인**: (1) 이전 retrieval 에서 사용된 노드/엣지의 `feedback_weight` 업데이트 — positive 는 랭킹 가중, negative 는 감쇠, (2) session Q&A 를 permanent graph 에 **`user_sessions_from_cache` 태그로 영구화**, (3) enrichment pass (triplet embedding · entity description 재합성), (4) 새 그래프 관계를 session cache 에 역방향 sync. Docs 원문: *"enriches an existing Cognee graph after data has already been ingested"*, *"derived retrieval structures"*.
5. **`improve` 는 `memify` 를 내부적으로 호출**: docs verbatim — *"default memify behavior is what Improve uses under the hood for its enrichment stage"*. `memify` 는 2-stage (extraction → enrichment) 컨피그러블 파이프라인. 기본 enrichment = `Task(index_data_points, batch_size=100)`. `memify_pipelines/` 디렉터리에 5개 구현 파일 — `apply_feedback_weights.py`, `consolidate_entity_descriptions.py`, `create_triplet_embeddings.py`, `memify_default_tasks.py`, `persist_sessions_in_knowledge_graph.py`.
6. **`remember(self_improvement=True)` 기본값 — 자동 `improve` 체인**: Docs 원문 *"remember(..., self_improvement=True) already calls improve() for you"*. 즉 "ingest 직후 enrichment" 가 암묵적 기본. 별도 `improve()` 명시 호출은 세션 종료 시점 + 여러 세션 합류 시 권장 (*"at the end of a chat or agent session"*).
7. **Multi-tenancy 는 v0.5.0 (2025-12) 부터 기본 활성**: `ENABLE_BACKEND_ACCESS_CONTROL` 환경변수 + `(User, Tenant, Role, Principal, ACL)` 5-개념 permission model. Dataset 단위 read/write 격리, `recall` 이 "사용자가 read 권한 가진 dataset 만" 자동 필터. 이는 "agent memory 가 SaaS 백엔드가 될 때 필수" 인 멀티테넌시를 abstraction 1등급 시민으로 올린 설계.
8. **Ontology 통합 — RDF/OWL 참조 어휘 선택적 주입**: 추출된 엔티티가 ontology 와 매칭되면 `ontology_valid=True` 플래그 + parent class / object-property 엣지 자동 추가. **confidence score 는 아니고 boolean 검증 플래그** — 축 4 (감사 가능성) 의 약한 형태.
9. **"Cognitive science approaches" 문구는 README 마케팅 수준에 그침**: 실제 docs overview · architecture · sessions-and-caching · ontologies 4개 핵심 페이지에서 episodic/semantic memory, consolidation, hippocampus-neocortex 등 구체 신경과학 용어 **전부 부재**. PyPI 설명 *"Combines vector search and graph databases with cognitive science"* 가 가장 구체적 — 즉 마케팅 수사이지 알고리즘에 반영된 메커니즘 아님. "single statement"(PyPI) vs "zero details"(docs) 일관성 격차가 명확한 증거.
10. **경쟁 비교는 자체 블로그에서만**: 공식 docs/README 에는 GraphRAG/Mem0/Letta/Zep 언급 없음. `cognee.ai/blog/deep-dives/ai-memory-tools-evaluation` 에 Mem0/Zep/Graphiti 대비 벤치마크 ("Dreamify" 프로프라이어터리 튜너 포함) 를 게시, 단 정량 수치는 텍스트 내 미포함 (차트 이미지 참조). Cognee 공식 self-positioning: *"local-first, privacy-critical deployments with graph reasoning"* (vectorize.io 2026 서베이 요약).
11. **`forget` 은 사용자 주도 3단 scope**: `data_id+dataset` (단일 아이템) / `dataset` (데이터셋 전체) / `everything=True` (사용자 소유 전부 + 세션 캐시). relational + graph + vector 3스토어 동시 삭제. **TTL 자동 forget 없음** — Mem0/Zep 류 자동 감쇠와 구별.
12. **라이선스 Apache-2.0, Python 86% + TypeScript 13%**: 매니지드 "Cognee Cloud" 병행. 고객 사례 (Splunk · Redis · AutoDesk · AWS · Atlassian · Infosys · Knowunity 40k 학생) 노출 — 엔터프라이즈 스케일 레퍼런스는 홈페이지에 있으나 **노드/쿼리 수 기준 공식 브레이크포인트는 (공식 범위 외 — 미답)**.

---

## 아키텍처 / 스토리지

### 3중 스토리지 (docs 원문 기준)

| 스토어 | 역할 (docs verbatim) | 기본 | 스왑 옵션 |
|---|---|---|---|
| **Vector store** | *"Holds embeddings for semantic similarity"* — 의미 유사도 | local (FastEmbed 추정) | ChromaDB, Postgres(pgvector), Redis |
| **Graph store** | *"Captures entities and relationships in a knowledge graph"* — 노드·엣지 구조 탐색 | local | Neo4j, Neptune, (Spanner Graph 이슈 제기됨) |
| **Relational store** | *"Tracks your documents, their chunks, and provenance"* — 원본 ↔ 청크 ↔ provenance 링크 | local | Postgres |

**Session cache** (별도 레이어): Redis 또는 filesystem diskcache (`{DATA_ROOT_DIRECTORY}/.cognee_fs_cache/sessions_db`). 키 `agent_sessions:{user_id}:{session_id}`, TTL/자동만료 없음.

### 파이프라인 단계 (docs verbatim)

- **Cognification phase** (`remember` 내부): *"The relational store matters most during cognification, keeping track of documents, chunks, and where each piece of information comes from"* → relational 이 provenance 중심축.
- **Search & retrieval phase** (`recall` 내부): *"vector stores for semantic searches and graph stores for structural searches"* + **hybrid mode** (*"combine both perspectives to surface results that are contextually rich and structurally precise"*).

### src 디렉터리 구조 (2026-04-21 확인)

```
cognee/
├── api/                  # REST endpoints
├── cli/                  # CLI
├── infrastructure/       # DB config, migrations
├── modules/              # feature modules
├── pipelines/            # add → cognify 파이프라인
├── memify_pipelines/     # improve 의 내부 엔진 — 아래 확대
├── tasks/                # async task handling
├── eval_framework/       # 자체 평가 프레임
├── alembic/              # DB migration
└── shared/
```

**`memify_pipelines/` 5개 파일** (=`improve` 내부 = 축 4 판정의 결정적 증거):

- `apply_feedback_weights.py` — 세션 QA 피드백 → 노드/엣지 weight 갱신 (streaming, alpha 0<α≤1 영향력).
- `consolidate_entity_descriptions.py` — 엔티티 description LLM 재합성 (이웃 그래프 컨텍스트 주입 후 재작성). **주의: 중복 entity 머지도, 모순 탐지도 아님 — "description enhancement through LLM-based summarization"** (src 분석 verbatim).
- `create_triplet_embeddings.py` — 트리플릿 단위 임베딩 생성 (hybrid retrieval 용).
- `memify_default_tasks.py` — 기본 태스크 config.
- `persist_sessions_in_knowledge_graph.py` — 세션 QA 를 permanent graph 로 승격 (**영구화 bridging** 의 실제 구현 위치).

---

## 4-op API — 시그니처와 행동

### `remember(data, ...)` — ingest + 기본 enrichment

**내부 3단**: (1) Ingest (정규화 + dataset 부착), (2) Build the graph — *"documents are chunked, entities and relationships are extracted, and embeddings are created"*, (3) Enrich (기본값 `self_improvement=True` 로 `improve` 후행 호출).

**Session mode**: `session_id` 지정 시 cache 에만 즉시 쓰고 즉시 반환 — background bridging 이 선택적으로 permanent 화.

**파라미터 (docs 발췌)**:

```python
await cognee.remember(
    data,                          # text | file path | URL | DataItem
    dataset_name="main_dataset",   # 기본 dataset
    session_id=None,               # 주면 session mode
    self_improvement=True,         # 기본 True — improve 자동 호출
    run_in_background=False,
    chunk_size=None, chunker=None, custom_prompt=None,
    user=None, dataset_id=None, graph_model=None, node_set=None,
)
```

**코드 예 (docs verbatim)**:

```python
result = await cognee.remember(
    "Einstein was born in Ulm.",
    run_in_background=True,
)
print(result)   # status='running'
await result
print(result)   # status='completed'
```

### `recall(query_text, ...)` — auto-routing retrieval

**Auto-route 규칙 (docs verbatim)**:

- *"overview / summary / key takeaways"* → summary retrieval
- *"how are X and Y connected"* → graph context-extension retrieval
- *"when / before / after / year ranges"* → temporal retrieval
- *"coding rules / async def"* → coding-rules retrieval
- quoted exact phrases → lexical chunk search
- `query_type` 명시 시 router 우회

**Session-aware**: `session_id` + `datasets` 없음 + `query_type` 없음 → 세션 캐시 keyword 검색 → miss 시 graph fallthrough. 결과에 `_source` 태그.

```python
await cognee.recall(
    query_text="Tell me about NLP",
    only_context=True,       # LLM 답 생성 없이 context 만
    top_k=10,
    auto_route=True,
    session_id=None,
    feedback_influence=None,  # improve 에서 적용된 feedback_weight 의 retrieval 가중
)
```

### `forget(...)` — 사용자 주도 3단 GC

```python
await cognee.forget(
    data_id=None,     # dataset 과 pair 필요
    dataset=None,     # 이름 or UUID
    everything=False, # 사용자 소유 전부
    user=None,
)
```

**scope 별 동작**: single item → 3스토어 동시 삭제, dataset 전체 → relational records + graph 노드/엣지 + vector embeddings 모두 삭제, everything → 세션 캐시 포함. *"does not replace low-level destructive prune operations"* — raw 파일시스템은 안 건드림.

### `improve(...)` — enrichment (심층은 아래 별도 섹션)

```python
await cognee.improve(
    dataset="main_dataset",
    session_ids=["chat_1", "chat_2"],  # 이 세션들을 permanent 화
    run_in_background=False,
    node_name=None,
    feedback_alpha=None,  # weight update 영향력
    extraction_tasks=None, enrichment_tasks=None,  # memify override
    data=None, node_type=None, user=None,
    vector_db_config=None, graph_db_config=None,
)
```

---

## `improve` operation 심층 — semantic lint 2번째 사례 **판정 = NO**

### 실제 4-stage (docs verbatim + src 검증)

1. **Feedback weight 적용** — *"Apply feedback weights to previously-used graph nodes/edges"* → `apply_feedback_weights.py` 가 세션 QA 의 평가 피드백(alpha 0<α≤1) 을 streaming 방식으로 노드/엣지 `feedback_weight` 필드에 주입. Positive = 향후 랭킹 가중, negative = 감쇠.
2. **세션 영구화** — *"Persist session Q&A into permanent graph (tagged as `user_sessions_from_cache`)"* → `persist_sessions_in_knowledge_graph.py` 가 단기 캐시의 QA 를 graph 노드화.
3. **Enrichment pass** — triplet embedding 재계산 + `consolidate_entity_descriptions.py` 로 **엔티티 description LLM 재합성** (이웃 그래프 컨텍스트 → LLM → `NodeDescription` 응답 모델로 description 재작성).
4. **Session 역sync** — *"Sync new graph relationships back to session cache"*.

### Detection 대상 — docs 직접 확인

Docs `improve.md` 원문은 **feedback weighting + session bridging + graph enrichment** 3항목만 명시. Cross-check:

| LLM Wiki `Lint` 항목 | Cognee `improve` 존재 여부 | 근거 |
|---|---|---|
| Orphan 페이지 탐지 | **× 부재** | `improve.md` / `memify.md` / src `memify_pipelines/` 5파일 중 orphan 관련 로직 없음 |
| Superseded / stale claims | **× 부재** | docs 4개 핵심 페이지에 "stale" / "outdated" 문자열 0회 |
| Contradiction 탐지 | **× 부재** | `consolidate_entity_descriptions` 는 *"does not detect contradictions"* — WebFetch 로 src 분석 verbatim |
| Missing concept (N노드에서 언급되나 전용 노드 없음) | **× 부재** | docs 에 해당 개념 미등장 |
| Research gap (시간·토픽 유입 중단) | **× 부재** | docs 미등장 |
| Schema/frontmatter 정합성 | **△ 부분** | `ontology_valid` boolean 플래그만 존재, 스키마 drift 연산 아님 |

### 대신 존재하는 것 — "additive refinement"

- **Feedback weighting** — 사용자 피드백을 edge weight 으로 반영하는 **평가 → 랭킹 가중 루프**. Evaluator-Optimizer primitive 의 좁은 형태지만, LLM Wiki 의 "지식 정합성 감사" 와는 성격이 다름.
- **Description 재합성** — 엔티티 노드의 description 필드를 이웃 컨텍스트로 enrichment. **교체(rewrite) 지 diff/merge 는 아님** — 기존 description 을 새 LLM 합성 결과로 덮어쓰는 형태 (src 분석).
- **세션 consolidation** — 단기 ↔ 장기 메모리 승격.

### 판정 — `knowledge-lifecycle-operations` 카드 적용

**`improve` = semantic lint 2번째 확정 사례 성립 = NO (미성립)**.

근거 3가지:
1. **탐지 범주 불일치**: LLM Wiki `Lint` 는 *"orphan / superseded / missing concept / research gap"* 4 카테고리 **품질 감사** 모드 — Cognee `improve` 는 이 4개 중 **0개** 를 가짐.
2. **연산 방향 불일치**: Lint = "문제 발견 → 사용자 승인 후 수정" (LLM Wiki Workflow 원문: *"발견 시 제안만 보고하고 사용자 승인 후 수정 적용"*). Improve = "자동 enrichment + 가중치 갱신" — 감사 단계 없음.
3. **src 증거**: `memify_pipelines/` 5 파일이 모두 *"apply / consolidate / create / persist"* 동사로 명명됨 — **additive 동작 only**. "detect / validate / flag" 동사는 0개.

**재분류 제안**: Cognee `improve` 는 `knowledge-lifecycle-operations` 카드의 **별도 하위 차원**으로 분기해야 함:

- *Lint 3분지* 확정된 것: **structural** (Basic Memory), **semantic** (LLM Wiki — 여전히 단일 사례), **incremental-update** (Graphify).
- *새로 발견된 4번째 차원 후보* — **"Feedback-weighted refinement"** 또는 **"Consolidation + feedback"**: Cognee `improve` 의 feedback weight + session bridging + description rewrite. Mem0 의 last-write-wins arbitration, Zep 의 temporal invalidation 과 같은 "consolidation" 축에 Cognee 가 feedback 루프를 덧댄 가장 정교한 1번째 사례.

→ `insights/primitive-knowledge-layer-design-space.md` 의 열린 질문 *"Cognee `improve` 구현 세부"* 는 **해소 — 단 예상과 반대 방향으로**. Basic Memory 판정 당시 "Cognee improve 가 semantic lint 2번째 사례" 로 잠정 가정됐으나, deep-dive 결과 **그 가정은 반증**. 카드 업데이트 트리거.

---

## 3축 프레임 판정

### 축 1 — Builder (누가 지식을 쓰는가)

**판정: induction (primary) + 얕은 self-editing 요소 (세션 feedback)**.

근거:
- `remember` 가 호출되면 LLM 이 자동으로 청크·엔티티·관계 추출 → graph 빌드. 사용자는 **원본만 던짐**. Curation 의 "사용자 승인 게이트" 부재.
- `improve` 의 feedback weight 는 agent/사용자 피드백을 그래프에 반영 — self-editing 의 약한 형태 (에이전트가 **직접 노드 편집하지는 않고** QA 평가를 통한 간접 weight 수정).
- Ontology 제공이 사용자 개입 지점이지만 "사전 스키마 고정" 수준, Graphify 의 "모든 엣지 confidence 태깅" 같은 규율은 없음.

→ 서베이 그래프 RAG 7종 (GraphRAG / LightRAG / HippoRAG / PathRAG / nano-graphrag / Neo4j LLM-GB) 과 **builder 축에서 동일 좌표 = induction**.

### 축 2 — Storage primitive

**판정: 3중 하이브리드 (vector + graph + relational) + session cache 레이어**. Primary = graph store (의미 중심), secondary = vector + relational + session cache.

근거:
- Docs architecture 페이지의 3중 스토어 명시 + hybrid retrieval (vector + graph) 1등급 기능.
- Basic Memory (markdown primary + SQLite+FastEmbed secondary) · Graphify (graph.json primary + 6표면 fan-out) 에 이어 **"primary + secondary surfaces 벡터" 해석** 의 3번째 증거.
- 단 Cognee 는 사용자 소유 markdown 이 없음 — **포팅·버전관리 축은 약함**. Basic Memory/LLM Wiki 와 대비되는 지점. (Dataset export 기능은 `api-reference/datasets/get-dataset-graph.md` 존재, 단 markdown fan-out 아님.)

→ `primitive-knowledge-layer-design-space.md` 의 **"정보 소유권" 관점에서 Cognee 는 opaque middle-ground** — Mem0 같은 벡터-only 불투명성보다는 낫지만 (graph 구조 export 가능), Basic Memory/LLM Wiki 같은 git-tracked markdown 진실 소유권과는 명확히 다른 좌표.

### 축 3 — Timing

**판정: runtime + 2단 (session cache = instant / permanent graph = `remember` 시점 compile)**.

근거:
- `remember(session_id=...)` 는 즉시 cache 쓰기 후 반환 — runtime 증분.
- `remember` 기본 모드는 `add → cognify → improve` 동기 체인 — ingest 시점에 그래프 확정 (compile-time 적). 단 `run_in_background=True` 로 async 가능.
- `improve` 는 명시 호출 or `remember(self_improvement=True)` 트리거 — **주기적 자동 재빌드 없음**.
- 서베이 GraphRAG 계열의 "offline precompute + online retrieval 2단" 과 유사하되, **세션 레이어가 실시간** 추가돼 hybrid.

→ **Basic Memory 와 인접** (runtime 증분) 이면서도, session/permanent 2단 구조가 **GraphRAG 계열 의 compile-time 축 과도 발을 걸치는 하이브리드**. 단일 라벨 어려움.

### 3축 종합 좌표

`(induction, graph+vector+relational+session hybrid, runtime + 2단 hybrid)`.

이는 서베이 그래프 RAG 7종과 가장 가깝지만 **session cache 레이어와 agent memory abstraction 어휘가 추가된 변형**. `primitive-knowledge-layer-design-space.md` 축 매트릭스에 기존 GraphRAG 7종 점과 **같은 좌표계 1-hop 이웃** 으로 등재.

### 축 4 후보 (감사 가능성) — 판정 = **NO (미성립)**

기준: Graphify 의 `EXTRACTED(1.0) / INFERRED(0.4-0.9) / AMBIGUOUS(0.1-0.3)` 엣지 단위 의무 confidence + *"Never invent an edge. If unsure, use AMBIGUOUS"* honesty rule.

Cognee 확인 결과:

| 항목 | Cognee 존재 여부 | 근거 |
|---|---|---|
| 엣지 단위 confidence 필드 | **× 부재** (필수도 선택도 아님) | `core-concepts/architecture.md` + `ontologies.md` + `recall.md` 에 confidence 언급 0회 |
| 노드 reliability / source_trust | **× 부재** | 위 동일 |
| "invent 금지" / "uncertain 명시" 프롬프트 규칙 | **× 부재** | docs 내 honesty rule 검색 0건 |
| Provenance 추적 | **○ 존재 (단 레이어 다름)** | Relational store 가 "documents ↔ chunks ↔ provenance" 링크 유지 — **소스 정보 추적** 은 하되 **엣지 신뢰도 태깅은 아님** |
| Ontology 검증 | **△ boolean** | `ontology_valid=True` 플래그만 — 3-tier 아님 |
| Feedback weight | **○ 존재 (단 의미 다름)** | retrieval 랭킹용 가중치이지 추출 신뢰도 아님 |

**판정**: Cognee 의 provenance (source traceability) 는 Graphify 의 confidence tiering (epistemic tagging) 과 **다른 layer 의 문제**. 소스를 추적하는 것 ≠ 엣지 신뢰도를 태깅하는 것.

→ 축 4 (감사 가능성) 는 **여전히 Graphify 단일 사례**. promotion 조건 (2번째 사례) 미충족. 카드의 후보 상태 유지.

---

## Lint 3분지 위치

`primitive-knowledge-layer-design-space.md` 의 Lint 3분지 재적용:

| 분지 | Cognee 대응 | 세부 |
|---|---|---|
| **Structural lint** (스키마 drift / 인덱스 정합성) | **× 부재** | Basic Memory `schema_infer/validate/diff`, `doctor` 류 없음. Dataset schema 조회는 있으나(`get-dataset-schema.md`) drift 탐지 아님 |
| **Semantic lint** (의미 노후화 / 모순 / orphan) | **× 부재** | 위 상세 판정 |
| **Incremental update** (변경분 재빌드) | **△ 부분** | Graphify `--update` / 파일 해시 캐시 같은 LLM 비용 우회 명시적 기능 없음. `forget` + 재 `remember` 수동. 단 session → permanent bridging 자체가 "증분 통합" 의 한 형태 |

**Cognee 의 고유 위치 — 4번째 분지 제안**:

- **Consolidation / feedback refinement** (새 분지): session QA → permanent graph 승격 + feedback weight streaming + entity description 재합성. 이는 structural/semantic/incremental 3분지 **밖** 의 운영 primitive.

→ `knowledge-lifecycle-operations` 카드가 carve-out 될 때 **최소 4분지** 를 가져야 함 (기존 Basic Memory 구조 lint, LLM Wiki 의미 lint, Graphify 증분, Cognee consolidation + feedback). 또는 Cognee 를 **"운영 primitive = consolidation"** 별도 축으로 두고 lint 와 분리.

---

## 지형 내 포지셔닝

### vs GraphRAG (Microsoft)

- **공식 docs 직접 비교 없음** — README · overview · architecture 4개 페이지에 "GraphRAG" 언급 0회. 서베이 카드 기록과 일치.
- **설계 관점 차이**: GraphRAG = "document → graph → query" 파이프라인 (community summarization 중심), Cognee = "agent memory abstraction" (세션 + 멀티테넌시 1등급). Cognee 는 community detection 같은 그래프 구조 분석 기능은 1차 API 에 없음, `recall` 의 graph context-extension 이 가장 가까움.
- Survey 요약 verbatim (`inbox/2026-04-21-graph-rag-survey.md`): *"GraphRAG 계열이 '파이프라인' 관점인 반면, Cognee 는 agent memory abstraction — 멀티테넌시·세션 인식·persistent learning 을 전면에 내세움. 경쟁 프레임워크와 직접 비교 안 함."*

### vs Mem0 / Letta / Zep

- 공식 docs/README 에는 **부재**. 자체 블로그 `cognee.ai/blog/deep-dives/ai-memory-tools-evaluation` 에만 존재 — Cognee · Mem0 · Zep/Graphiti 3자 비교 벤치마크 게시, *"our approach delivers significant improvements in handling complex, multi-step questions"* 주장. 단 텍스트 내 수치 미포함 (차트 이미지만) — **정량 검증은 (공식 범위 외 — 미답)**.
- 외부 2026 서베이 (vectorize.io, atlan.com, letta forum) 요약: *"Cognee is best for local-first, privacy-critical deployments with graph reasoning"*. Mem0 = "managed drop-in personalization", Zep/Graphiti = "temporal knowledge graph", Letta = "self-editing memory runtime". Cognee 의 독특 좌표 = **멀티테넌시·권한·dataset 단위 격리 + 3중 하이브리드 스토리지**.
- Letta 포럼에 *"Agent memory: Letta vs Mem0 vs Zep vs Cognee"* 커뮤니티 토론 스레드 존재 — 4자를 **직접 경쟁 카테고리**로 인식하는 외부 합의.

### vs Basic Memory

- **Builder 축 공유** (induction 비중 — Basic Memory 가 co-authored 지만 MCP write_note 호출 시 LLM induction 와 유사) 하지만 **storage 축 상이** (Cognee = graph primary + cache, Basic Memory = markdown primary + SQLite/vector secondary).
- **Multi-tenancy**: Cognee 는 v0.5.0 부터 기본 활성, Basic Memory 는 v0.16 Postgres backend 지원 수준 — 권한 모델은 Basic Memory 문서에 명시 없음.
- `improve` ↔ Basic Memory `schema_validate`/`doctor` 는 서로 **완전히 다른 분지** (Cognee = 피드백 consolidation, Basic Memory = 구조 lint).

### vs LLM Wiki

- **3축 모두 상이**: LLM Wiki (curation + markdown + compile-time) vs Cognee (induction + hybrid graph + runtime). 유일한 공통점은 **"시간에 따라 지식이 누적된다"** 는 accumulation 서사.
- 서베이 카드의 *"`improve` 연산이 LLM Wiki 의 iterative refinement 와 가장 유사"* 주장은 **본 deep-dive 로 반증** — 두 연산의 detection 범주/연산 방향이 근본적으로 다름 (위 판정 참조).

### Dreamify 상용 레이어

Cognee 블로그의 *"proprietary tool Dreamify"* — 정확도를 높이는 프로프라이어터리 튜너. 오픈소스 Cognee 위에 상용 레이어가 얹힌 구조는 **Graphify(MIT) + Penpax(상용)** 와 유사한 dual-product 패턴. 2026-04 시점 정립 중인 "infra-tier knowledge 레이어의 상용화 모델" 의 1사례 (세부 기능 · 가격 (공식 범위 외 — 미답)).

---

## 스케일 감각

### 공식 문서 확인

- **엔터프라이즈 레퍼런스**: Splunk · Redis · AutoDesk · AWS · Atlassian · Infosys · Knowunity (40,000 students) (landing 확인).
- **Dataset 단위 분할**: 대규모 코퍼스를 여러 dataset 으로 쪼개 `recall(datasets=[...])` 로 scope 제한 — LLM Wiki "index.md 붕괴점" 같은 단일 네비게이션 레이어 없음.
- **Dataset Database Handlers** (v0.5.0+): "intelligently direct connections to appropriate databases or logical schemas based on dataset configuration" — 데이터셋별 DB 라우팅으로 수평 확장.

### 공식 범위 외 (미답)

- **노드/엣지 수 기준 성능 브레이크포인트**: (공식 범위 외 — 미답).
- **매니지드 Cognee Cloud 의 tier별 한도**: landing 페이지에 `/pricing` · `/cost-calculator` 링크만, 세부 (공식 범위 외 — 미답).
- **LLM 호출 비용 프로파일링**: `remember` 가 ingest 시 LLM 얼마나 부르는지 정량 기록 (공식 범위 외 — 미답).
- **Dreamify 튜너의 실제 성능 증가폭**: 블로그에 "significant improvements" 표현, 정량 (공식 범위 외 — 미답).

---

## 연결

- **`insights/primitive-knowledge-layer-design-space.md`** — 본 deep-dive 로 3축 좌표 `(induction, hybrid 3-store + session, runtime + 2단)` 추가. GraphRAG 7종 좌표와 1-hop 이웃. **카드의 열린 질문 "Cognee `improve` 구현" 해소** — 단 예상 반대 방향 (semantic lint 2번째 사례 **반증**). Lint 3분지 업데이트 필요: Cognee 는 3분지 중 어디에도 안 들어가고 **4번째 분지 후보 "consolidation + feedback refinement"** 로 등재 제안. 축 4 (감사 가능성) 2번째 사례 **미성립** — Graphify 단일 사례 상태 유지.
- **`notes/techniques/karpathy-llm-wiki.md`** — `improve` vs `Lint Workflow` 직접 비교. 서베이가 기록한 "개념 중첩" 은 표면적이고 **실제 구현은 근본적으로 다름** 을 본 deep-dive 가 확증. LLM Wiki 노트의 "Lint workflow" 섹션에 "Cognee `improve` 는 이 계열과 다른 별도 primitive" 주석 추가 가치 있음.
- **`notes/techniques/basic-memory.md`** — Structural lint 비교 대조. Basic Memory 는 `schema_validate/doctor` 로 structural 만, Cognee 는 consolidation + feedback weight 으로 **서로 배타적 운영 primitive**. `knowledge-lifecycle-operations` 카드가 carve-out 될 때 둘을 다른 셀에 배치.
- **`notes/techniques/graphify.md`** — Incremental update + 축 4 후보 비교. Graphify 의 confidence tiering 은 Cognee 에 부재 — **축 4 promotion 대기 상태 유지**. Graphify `--update` 증분과 Cognee session→permanent bridging 은 **모두 "증분적 병합"** 이지만 triggering condition 이 다름 (Graphify = 파일 변경, Cognee = 세션 종료/명시 호출).
- **후보 신규 카드 `knowledge-lifecycle-operations`** — 본 deep-dive 가 **4분지 구조** 를 확정: structural (Basic Memory) / semantic (LLM Wiki — 단일) / incremental (Graphify) / **consolidation + feedback (Cognee — 신규 확정)**. Cognee 가 4번째 분지에 첫 사례를 공급. Carve-out 시점 도래.
- **Mem0 / Letta / Zep deep-dive (미작성)** — Letta 포럼 스레드가 이 4자를 직접 경쟁으로 인식. Mem0 의 last-write-wins, Zep 의 temporal invalidation 이 **Cognee 의 feedback weight + consolidation** 과 어떻게 다른지 교차 매트릭스 작성 가치. 2nd-pass 축 4 증거 후보도 여기서 나올 가능성.
- **`inbox/2026-04-21-graph-rag-survey.md`** — Cognee 항목의 미답 질문 *"`improve` 가 재작성(rewrite) 인지 merge 인지 delta-update 인지 — 실제 구현 메커니즘 불명"* **해소**: **additive enrichment** (rewrite/merge/delta 그 어느 쪽도 아닌 **덧붙이기 + streaming weight + description 재합성**). 서베이 파일에 resolution 플래그 추가 가치.

---

## Sources

- [topoteretes/cognee GitHub repository](https://github.com/topoteretes/cognee) — 2026-04-21 fetch, Apache-2.0, Python 86.5% / TypeScript 13.1%, v1.0.1 (2026-04-18)
- [cognee.ai 공식 랜딩](https://www.cognee.ai) — 2026-04-21 fetch, "AI memory engine / knowledge engine that learns" 포지셔닝
- [docs.cognee.ai llms.txt 문서 인덱스](https://docs.cognee.ai/llms.txt) — 2026-04-21 fetch, 전체 URL 맵핑
- [docs.cognee.ai — improve operation](https://docs.cognee.ai/core-concepts/main-operations/improve.md) — 2026-04-21 fetch, 본 deep-dive 판정의 결정적 1차 소스
- [docs.cognee.ai — remember operation](https://docs.cognee.ai/core-concepts/main-operations/remember.md) — 2026-04-21 fetch
- [docs.cognee.ai — recall operation](https://docs.cognee.ai/core-concepts/main-operations/recall.md) — 2026-04-21 fetch
- [docs.cognee.ai — forget operation](https://docs.cognee.ai/core-concepts/main-operations/forget.md) — 2026-04-21 fetch
- [docs.cognee.ai — memify (legacy) operation](https://docs.cognee.ai/core-concepts/main-operations/legacy-operations/memify.md) — 2026-04-21 fetch, improve 의 내부 엔진 확인
- [docs.cognee.ai — architecture](https://docs.cognee.ai/core-concepts/architecture.md) — 2026-04-21 fetch, 3중 스토어 구조
- [docs.cognee.ai — sessions and caching](https://docs.cognee.ai/core-concepts/sessions-and-caching.md) — 2026-04-21 fetch, session ↔ permanent 구조
- [docs.cognee.ai — multi-user mode overview](https://docs.cognee.ai/core-concepts/multi-user-mode/multi-user-mode-overview.md) — 2026-04-21 fetch, v0.5.0 기본 활성 권한 모델
- [docs.cognee.ai — ontologies](https://docs.cognee.ai/core-concepts/further-concepts/ontologies.md) — 2026-04-21 fetch, `ontology_valid` 플래그 확인
- [docs.cognee.ai — overview](https://docs.cognee.ai/core-concepts/overview.md) — 2026-04-21 fetch, cognitive science 마케팅 수사 확인
- [PyPI cognee](https://pypi.org/project/cognee/) — 2026-04-21 fetch, 릴리스 타임라인, 의존성, maintainer (Vasilije Markovic / Boris Arzentar)
- [github.com/topoteretes/cognee/tree/main/cognee](https://github.com/topoteretes/cognee/tree/main/cognee) — 2026-04-21 fetch, src 디렉터리 구조 (`memify_pipelines/` 등)
- [github.com/topoteretes/cognee/tree/main/cognee/memify_pipelines](https://github.com/topoteretes/cognee/tree/main/cognee/memify_pipelines) — 2026-04-21 fetch, 5 파일 확인
- [cognee/memify_pipelines/apply_feedback_weights.py](https://github.com/topoteretes/cognee/blob/main/cognee/memify_pipelines/apply_feedback_weights.py) — 2026-04-21 fetch, improve 의 feedback weight 구현
- [cognee/memify_pipelines/consolidate_entity_descriptions.py](https://github.com/topoteretes/cognee/blob/main/cognee/memify_pipelines/consolidate_entity_descriptions.py) — 2026-04-21 fetch, "does not detect contradictions" 확인
- [cognee.ai/blog/deep-dives/ai-memory-tools-evaluation](https://www.cognee.ai/blog/deep-dives/ai-memory-tools-evaluation) — 2026-04-21 fetch, Mem0/Zep/Graphiti 비교 블로그 (정량 수치는 차트 이미지에만)
- [Letta forum — Agent memory: Letta vs Mem0 vs Zep vs Cognee](https://forum.letta.com/t/agent-memory-letta-vs-mem0-vs-zep-vs-cognee/88) — 2026-04-21 WebSearch 확인, 커뮤니티가 4자를 직접 경쟁으로 인식하는 증거
- `inbox/2026-04-21-graph-rag-survey.md` — 로컬 서베이, Cognee 항목 5번 (참조)
- `insights/primitive-knowledge-layer-design-space.md` — 로컬 primitive 카드 (3축 프레임 적용 대상)
