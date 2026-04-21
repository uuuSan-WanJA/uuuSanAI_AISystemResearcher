---
title: Graph-based LLM knowledge layer survey
date: 2026-04-21
type: inbox / survey
status: captured
---

## 3줄 요약

- **지형은 두 축으로 분화**: (1) **graph construction cost** — 엔터프라이즈급 풀파이프라인(Microsoft GraphRAG, Neo4j LLM Graph Builder) vs 경량 재구현(nano-graphrag, LightRAG, HippoRAG 2) — 고비용 인덱싱이 가장 큰 진입장벽이자 분화 동인. (2) **retrieval mechanism** — community summarization(GraphRAG), dual-level entity/relation(LightRAG), Personalized PageRank(HippoRAG), path pruning(PathRAG), auto-route remember/recall API(Cognee).
- **모두 "offline graph precompute + online retrieval" 2단 구조**로 수렴. LLM은 양쪽에서 활용되지만 **builder 역할이 비용 중심**이며, 최근 프레임워크(HippoRAG 2, PathRAG)는 인덱싱 비용 절감을 공개적 벤치마크 축으로 삼음.
- **Karpathy LLM Wiki 대비**: 이들 전부 **automated graph extraction** 이라 "LLM 이 self-builder" 축에 있지만, LLM Wiki 처럼 compile-time curated human-written knowledge base 는 아님 — 전부 **induction 계열**. 수동 accumulation 모델의 LLM-Wiki 와는 패러다임이 다름.

## Framework entries

### 1. Microsoft GraphRAG
- **URL**: https://github.com/microsoft/graphrag (v3.0.9 릴리즈 2026-04-13)
- **What**: LLM 으로 비정형 텍스트에서 엔티티·관계를 추출하고 커뮤니티 계층 요약을 미리 만들어 global/local 하이브리드 질의를 지원하는 데이터 파이프라인.
- **Scale**: 엔터프라이즈. repo 가 대놓고 "indexing can be an expensive operation, start small" 이라 경고. 토큰 비용 큼.
- **Differentiator**: 단순 vector 가 아니라 **커뮤니티 단위 계층 요약(Leiden clustering + summary)** — global query 에서 whole-corpus-level 질문에 답할 수 있는 것이 핵심 주장.
- **LLM Wiki positioning**: **precompute-heavy navigation layer**. LLM 이 builder+retriever 양쪽 담당. Wiki 처럼 compile-time 이지만 **induction (LLM 자동 생성)** 이지 **curation (인간 편집)** 이 아님.
- **Deep-dive**: **yes** — 이 지형의 de-facto reference. 나머지 전부가 "GraphRAG 대비" 로 포지셔닝함.
- **Source quality**: primary

### 2. LightRAG
- **URL**: https://github.com/HKUDS/LightRAG, paper: https://arxiv.org/abs/2410.05779 (HKU-NLP, NAACL '25)
- **What**: 엔티티-관계 추출 후 **dual-level retrieval** (low-level entities + high-level relations) 로 GraphRAG 의 무거운 인덱싱을 단순화한 graph RAG.
- **Scale**: 중간급. 32B+ LLM, 32KB+ 컨텍스트 요구. 벤치마크에서 GraphRAG 보다 4–8%p 앞선 주장.
- **Differentiator**: community summarization 제거, dual-level retrieval 로 "simple and fast" 추구. Incremental update 지원 강조.
- **LLM Wiki positioning**: **induction-based, lighter precompute**. navigation 보다는 retrieval-augmentation 에 가까움.
- **Deep-dive**: **yes** — dual-level retrieval 개념은 LLM Wiki 의 "index + full text" 이중 구조와 구조적으로 유사해 비교 가치 있음.
- **Source quality**: primary

### 3. HippoRAG 2
- **URL**: https://github.com/OSU-NLP-Group/HippoRAG, v2 paper: https://arxiv.org/abs/2502.14802 (ICML '25), v1: https://arxiv.org/abs/2405.14831 (NeurIPS '24)
- **What**: 해마(hippocampal indexing theory) 에서 영감받은 long-term memory framework — KG + **Personalized PageRank** 로 multi-hop 연상 검색 구현.
- **Scale**: offline indexing 비용이 GraphRAG/RAPTOR/LightRAG 대비 "significantly less" 라고 명시적 주장. 개인 ~ 중간.
- **Differentiator**: **associativity (multi-hop) + sense-making** 이 두 축. PPR 로 query entity 에서 그래프 확산 검색 — 전통 graph traversal 이 아닌 random-walk 기반.
- **LLM Wiki positioning**: **navigation layer with biomimetic retrieval**. LLM Wiki 는 human navigation, HippoRAG 는 PPR 자동 navigation — 설계 철학은 다르지만 "retrieval 이 graph traversal 이다" 를 공유.
- **Deep-dive**: **yes** — PPR 기반 retrieval 은 이 지형에서 가장 이색적. v1→v2 진화 궤적도 분석 가치.
- **Source quality**: primary

### 4. PathRAG
- **URL**: https://github.com/BUPT-GAMMA/PathRAG, paper: https://arxiv.org/abs/2502.14902 (BUPT, AAAI '25 — date unclear on version이지만 2025-02 submitted)
- **What**: 그래프에서 **key relational paths** 를 flow-based pruning 으로 추출해 노이즈를 줄이고 LLM prompt 에 신뢰도 순으로 배치하는 graph RAG.
- **Scale**: 중간. repo 은 UI 포함 fullstack 지향.
- **Differentiator**: 3단계 파이프라인 — node retrieval → **flow-based path pruning** → reliability-ordered prompting. "노드/커뮤니티 단위가 아닌 path 단위 retrieval" 이 핵심 주장.
- **LLM Wiki positioning**: **retrieval-time navigation**. precompute 는 일반 KG 수준, 혁신은 query-time path selection 에 집중.
- **Deep-dive**: **maybe** — path pruning 아이디어는 흥미롭지만 구현체가 상대적으로 신규라 adoption·성숙도 불명.
- **Source quality**: primary (paper+repo 모두 확인)

### 5. Cognee
- **URL**: https://github.com/topoteretes/cognee (+ cognee.ai 매니지드 서비스)
- **What**: AI 에이전트의 메모리 레이어 — `remember/recall/forget/improve` 4-op API 로 vector + graph + cognitive-science 접근을 결합한 knowledge engine.
- **Scale**: 라이브러리(pip) + 매니지드 클라우드 둘 다. 개인 dev 부터 mid-tier 조직까지.
- **Differentiator**: GraphRAG 계열이 "document → graph → query" 파이프라인인 반면, Cognee 는 **agent memory abstraction** — 멀티테넌시·세션 인식·persistent learning 을 전면에 내세움. 경쟁 프레임워크와 직접 비교 안 함.
- **LLM Wiki positioning**: **accumulation-oriented**. `remember` 가 incremental 하게 쌓이고 `improve` 로 refine — Wiki 의 accumulation 모델과 구조적 유사성 가장 큼. 다만 자동 추출 기반.
- **Deep-dive**: **yes** — "agent memory" 를 **프레임워크 수준 abstraction** 으로 끌어올린 드문 시도. 하네스 관점에서 참고 가치 높음.
- **Source quality**: primary

### 6. Neo4j LLM Knowledge Graph Builder
- **URL**: https://github.com/neo4j-labs/llm-graph-builder, hosted: https://llm-graph-builder.neo4jlabs.com (Apache-2.0)
- **What**: PDF·DOC·YouTube·Wikipedia·S3·GCS 등 비정형 입력을 LLM 으로 파싱해 Neo4j KG 로 적재하는 **graph construction UI + chat**.
- **Scale**: 엔터프라이즈 (Neo4j 자산) + 오픈 (무료 hosted). Neo4j 라이선스·운영 비용이 동반됨.
- **Differentiator**: RAG 프레임워크라기보다 **KG-construction platform** 에 가까움. 다중 입력 소스 지원이 광범위. "Chat with Data" 는 애드온 수준.
- **LLM Wiki positioning**: **builder-first, navigation 은 2차**. LLM 은 extraction 전담, retrieval 은 Cypher/graph query. Wiki 의 "indexing 정리" 부분과 대응되나 human curation 은 없음.
- **Deep-dive**: **maybe** — 프레임워크 자체의 아이디어 혁신성보다는 **Neo4j 생태계와의 integration** 이 가치. 다른 프레임워크 backend 로 쓰이는 패턴 조사할 때 재방문.
- **Source quality**: primary

### 7. nano-graphrag
- **URL**: https://github.com/gusye1234/nano-graphrag (v0.0.8, 2024-10-01 — 이후 릴리즈 없음, 날짜 대비 6개월 정체)
- **What**: Microsoft GraphRAG 의 ~1100 LOC 경량 재구현 (fork 아님, clean rewrite). "hackable" 추구.
- **Scale**: 개인/프로토타입. full GraphRAG 의 covariates 등 일부 기능 생략.
- **Differentiator**: global search 를 top-K important communities 로 단순화(map-reduce 대신). 연구용·해커용.
- **LLM Wiki positioning**: **GraphRAG 의 minimal reproducible core**. 자체 아이디어보다는 타 프레임워크의 기반.
- **Deep-dive**: **maybe** — 흥미로운 것은 **파생물**: LightRAG, fast-graphrag, HiRAG, Medical Graph RAG 가 nano-graphrag 위에 구축됨 (repo 자체 주장). 이 지형의 **upstream dependency** 역할을 실제로 했는지가 핵심 질문.
- **Source quality**: primary

## Cross-cutting 관찰

**수렴하는 설계 결정**:
- 모두 offline graph precompute + online retrieval 2단 구조.
- 모두 entity + relation 추출을 LLM 으로 수행 (spaCy 등 전통 NLP 위주 프로젝트는 없음).
- 모두 hybrid retrieval (vector + graph) — 순수 graph-only 는 부재.

**공개적으로 분화된 지점**:
- **인덱싱 비용**: GraphRAG/Neo4j = 무겁게, HippoRAG 2/PathRAG = 명시적 비용 축소 주장, nano-graphrag = 단순화로 경량화.
- **retrieval primitive**: community summary (GraphRAG) / dual-level (LightRAG) / PPR (HippoRAG) / path pruning (PathRAG) / auto-route API (Cognee) / Cypher (Neo4j).
- **abstraction 수준**: 파이프라인 (GraphRAG, PathRAG) vs 메모리 API (Cognee) vs 구성 도구 (Neo4j). Cognee 만 **agent-centric** 언어를 씀.

**LLM Wiki 대비 포지셔닝**:
- **전원 induction 계열** — LLM 이 자동으로 graph 를 채움. LLM Wiki 의 **curation (human-written, compile-time)** 축에 있는 프레임워크는 이 조사에서 발견 안 됨.
- Cognee 의 `improve` 연산이 LLM Wiki 의 iterative refinement 와 가장 유사.
- "navigation layer vs accumulation" 축에서는 GraphRAG/LightRAG/PathRAG = navigation-heavy, Cognee = accumulation-heavy, HippoRAG/Neo4j = 중간.

## Deep-dive 우선순위 top 3

1. **Microsoft GraphRAG** — 지형 전체의 reference point. community summarization + global/local search 의 구체 구현 메커니즘을 파악해야 나머지 프레임워크의 "we're lighter than GraphRAG" 주장이 의미를 가짐.
2. **Cognee** — agent memory 를 프레임워크 수준 abstraction 으로 끌어올린 유일한 사례. 하네스 엔지니어링 관점 및 LLM Wiki 의 accumulation 모델과의 직접 비교 가치.
3. **HippoRAG 2** — Personalized PageRank 기반 retrieval 이라는 구조적으로 이색적인 설계. "retrieval = associative recall" 이라는 철학이 agent memory 설계에 주는 함의가 큼.

## 미답 / 열린 질문

- nano-graphrag 가 실제로 LightRAG·HiRAG·fast-graphrag 의 upstream 인지 각 프로젝트 관점에서 cross-check 필요 (nano-graphrag repo 자체 주장만 확인됨).
- PathRAG 의 flow-based pruning 이 수학적으로 어떻게 정의되는지 (paper 본문 확인 필요).
- Cognee 의 `improve` 연산이 재작성(rewrite) 인지 merge 인지 delta-update 인지 — 실제 구현 메커니즘 불명.
- Neo4j LLM Graph Builder 가 GraphRAG/LightRAG 의 **backend storage** 로 쓰이는 레퍼런스 사례가 있는지.
- LLM Wiki 스타일의 **curation 계열 (human compile-time)** graph framework 가 존재하는지 — 이번 조사에서는 발견 못함, 열린 질문.
- HippoRAG 2 의 "cost efficient indexing" 주장의 수치 근거 (token/compute 벤치마크 본문 확인 필요).
- 한·중·일어권 특화 graph RAG (LightRAG 가 HKU, PathRAG 가 BUPT — 중화권 강세) 의 다국어 성능 데이터.
