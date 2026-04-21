---
title: LLM agent memory & PKM frameworks survey
date: 2026-04-21
type: inbox / survey
status: captured
---

## 3줄 요약

메모리 프레임워크는 세 축으로 분화한다 — (a) **스토리지 프리미티브**: 벡터 DB / 시계열 지식 그래프 / 평문 markdown / 혼합, (b) **LLM 의 역할**: memory builder(대화에서 자동 추출·갱신) vs retriever(사용자가 쌓은 것을 검색만) vs self-editor(에이전트가 자신의 메모리 블록을 도구 호출로 편집), (c) **에피소딕 vs 누적**: 대화/사용자당 짧은 사실 조각을 휘발적으로 관리하느냐, 사용자 자산으로 영속 축적하느냐. Karpathy LLM Wiki 는 이 스펙트럼의 극단(compile-time 정적·builder = 저자 본인·스토리지 = markdown+index.md) 에 위치하며, 아래 7개는 대부분 런타임·동적·LLM-as-builder 쪽에 몰려 있다.

## Framework entries

### 1. Mem0
- **URL**: https://docs.mem0.ai/overview, https://docs.mem0.ai/core-concepts/memory-operations, https://github.com/mem0ai/mem0
- **What**: 에이전트가 대화에서 사용자 선호·사실을 자동 추출해 영속 저장하고, 이후 호출 시 맥락으로 재주입해 주는 매니지드 메모리 레이어.
- **Storage**: hybrid — 벡터 스토어 + 선택적 그래프 스토어 + 리랭커를 호스팅 스택으로 묶음(셀프호스트 OSS 버전도 있음).
- **Memory lifecycle**: `add()` 호출 시 LLM 이 "Information extraction" 단계에서 핵심 사실/결정/선호를 뽑아냄(`infer=True` 기본). "Conflict resolution" 단계에서 기존 메모리와 중복/모순을 체크해 **last-write-wins** 로 덮어씀. 검색은 의미 검색 기반. `infer=False` 로 넣으면 원문 저장되지만 충돌 해소·중복 제거 우회. forgetting/TTL 은 공식 overview 에선 미기재(별도 API 필요 추정).
- **LLM Wiki positioning**: 순수 **builder** 계열. LLM 이 대화 스트림 → 사실 조각 변환을 자동 수행. 축적형이지만 단위가 짧은 "선호/사실 조각" 이라 LLM Wiki 처럼 긴 연결된 지식 문서가 아니라 **episodic facts 더미**에 가까움. 스케일은 SaaS 매니지드(SOC2/GDPR 명시) — 개인 지식 관리보단 제품 내 사용자별 메모리 레이어.
- **Deep-dive**: **yes** — "LLM 이 덮어쓴다" 는 consolidation 정책이 LLM Wiki 의 저자 edit-in-place 와 가장 대비되는 지점. 충돌 해소 프롬프트 내부가 궁금.
- **Source quality**: primary (공식 docs 2페이지 + 레포 확인)

### 2. Letta (구 MemGPT)
- **URL**: https://github.com/letta-ai/letta, https://docs.letta.com/concepts/memgpt, MemGPT 논문 (Packer et al., 2023, arxiv 2310.08560)
- **What**: 에이전트가 자기 자신의 메모리 블록을 도구 호출로 편집하며 장기 상태를 유지하는 stateful agent 프레임워크(OS-like memory hierarchy 에서 출발).
- **Storage**: 릴레이셔널 DB 기반(레포에 `alembic/`, `init.sql` 존재 — Postgres/SQLite). 조직 단위는 **memory_blocks** (예: `human`, `persona` 라벨). MemGPT 의 core / archival / recall 3단 계층은 원 논문의 구조이며, 최신 Letta 는 "MemFS" 라는 git-tracked 메모리 시스템도 도입(공식 docs 언급, 세부는 내부 링크 필요).
- **Memory lifecycle**: 에이전트가 LLM 도구 호출로 직접 memory_block 을 편집(append/replace) — "self-editing memory". insert/update 는 함수 호출 한 번으로 일어남. retrieve 는 컨텍스트 윈도우에 core memory 가 상주하고 archival 은 필요 시 검색 도구 호출. forget 은 명시 문서 미확인.
- **LLM Wiki positioning**: **self-editing builder** — LLM Wiki 와 가장 닮은 철학(LLM이 자기 지식을 직접 써 내려감)이나, 단위가 사용자 가시 markdown 이 아니라 에이전트 내부 메모리 블록이라 **사용자 PKM 으로 꺼내 쓰기엔 벽이 있음**. MemFS 가 git-tracked 라는 점은 Wiki 쪽에 가까워진 움직임으로 주목할 만함.
- **Deep-dive**: **yes** — MemFS (git-tracked memory) 가 Wiki 와 Letta 의 교차점일 가능성. MemGPT 논문의 3단 계층이 현재 Letta 에서 어떻게 진화했는지 확인 가치 높음.
- **Source quality**: primary (README + 개념 페이지; 세부 API 는 추가 문서 필요)

### 3. Zep
- **URL**: https://help.getzep.com/concepts, https://github.com/getzep/zep, Graphiti 관련 https://github.com/getzep/graphiti
- **What**: 에이전트용 context engineering 플랫폼으로, 대화/이벤트를 **temporal knowledge graph** 에 ingest 해 시점별로 유효한 사실만 프롬프트에 주입한다.
- **Storage**: graph-primary **hybrid**. 노드=엔티티, 엣지=관계/사실, 엣지에 `valid_from / invalid_at` 타임스탬프를 붙이는 bi-temporal 모델. 벡터 검색도 함께.
- **Memory lifecycle**: **insert** = `graph.add` / `thread.add_messages` (JSON·텍스트·메시지). **retrieve** = `graph.search` / `thread.get_user_context`. **update/forget** = "Fact Invalidation" — 구 사실을 지우지 않고 엣지에 invalid 타임스탬프를 기록(temporal invalidation, append-only 성격). LLM 이 엔티티/엣지 추출 파이프라인에 관여(세부는 Graphiti 레포 참조 필요).
- **LLM Wiki positioning**: **builder + temporal**. LLM Wiki 가 "지금 저자가 믿는 것의 스냅샷" 이라면 Zep 은 "시간축을 가진 믿음의 이력". 누적·기록형이지만 단위가 에이전트가 쓸 구조화된 fact edge 라서 **사용자 읽기 경험은 좋지 않음** (내부 상태). 스케일은 agent-per-user 관점으로 설계.
- **Deep-dive**: **yes** — temporal invalidation 은 Mem0 의 last-write-wins 와 대척점. "시간 가진 지식" 이라는 설계가 개인 PKM 에 쓸 수 있는지 추적할 가치 높음. Graphiti OSS 레포가 구현 진입점.
- **Source quality**: primary

### 4. Basic Memory
- **URL**: https://basicmemory.com/, (Obsidian + MCP 통합; GitHub 레포는 basicmachines-co 추정, 홈페이지 기준)
- **What**: 대화 중 얻은 지식을 Claude/Codex/Cursor 등 MCP 클라이언트를 통해 **로컬 markdown 파일**로 영속 저장·편집·연결하는 사용자 소유 PKM.
- **Storage**: plain markdown on filesystem, Obsidian vault 호환. 별도 벡터/그래프 인덱스 홈페이지 단계에선 불명(쿼리 시 내부에 SQLite/fts 가능성은 있으나 primary source 미확인 — **(storage detail unclear)**).
- **Memory lifecycle**: MCP 도구로 노트를 생성·읽기·수정. 사용자와 LLM 이 공동 저자. 연결("월요일에 언급한 사람을 금요일에 물어보면 이미 연결돼 있다")이 핵심 UX 로 홍보됨 — 링크 기반 그래프 탐색 시사. 삭제는 파일 삭제.
- **LLM Wiki positioning**: **LLM Wiki 와 가장 가까운 형제**. 파일시스템 + markdown + 사용자 가시성·편집 가능성. 차이: LLM Wiki 는 compile-time 저자 빌드·index.md 직독 navigation / Basic Memory 는 runtime 대화 빌드·MCP query. **accumulation, co-builder**.
- **Deep-dive**: **yes — 최우선** — LLM Wiki 대비 가장 직접 비교 가능한 사례. MCP 노출 면(어떤 도구·어떤 prompt 로 LLM 이 쓰게 하는지), 링크/그래프 구축 방식, 인덱스 유무가 핵심.
- **Source quality**: primary (홈페이지) / 세부는 thin — 레포·docs 2차 확인 필요.

### 5. Khoj
- **URL**: https://docs.khoj.dev/, https://github.com/khoj-ai/khoj
- **What**: 사용자가 소유한 파일(pdf/markdown/org-mode/Notion 등)과 웹을 대상으로 자연어 채팅·검색을 제공하는 self-host/cloud 개인 AI.
- **Storage**: primary docs overview 에 기술 상세 미기재 — 레포 README 기준으로는 벡터 임베딩 인덱스(내부 SQLite + 임베딩) 사용. **(storage detail from README, not overview page)**
- **Memory lifecycle**: 사용자가 연결한 소스(파일/Notion) 를 주기적으로 재인덱싱(insert/update). 검색은 의미 검색 + 웹. forget 은 소스 연결 해제 기반. 대화 자체의 장기 메모리(Mem0 류)는 부수적.
- **LLM Wiki positioning**: **retriever 우세**, builder 약함. "사용자가 이미 쓴 것" 을 임베딩해 꺼내 쓰는 RAG-over-PKM. LLM Wiki 와 유사한 면: 사용자 소유 파일이 source-of-truth. 차이: Khoj 는 LLM 이 쓰지 않음, 읽기만. 스케일은 consumer-hardware self-host 가능.
- **Deep-dive**: **maybe** — RAG-over-vault UX 의 reference 포인트로는 유용하지만, "LLM 이 지식을 만들고 관리" 축에서 새 정보는 적음.
- **Source quality**: primary (홈) / 세부는 thin — 아키텍처 상세는 레포 확인 필요.

### 6. AnythingLLM
- **URL**: https://docs.anythingllm.com/, https://github.com/Mintplex-Labs/anything-llm
- **What**: 문서 RAG + 에이전트 워크플로를 워크스페이스 단위로 묶어 제공하는 올인원 데스크톱/서버 앱.
- **Storage**: 다수 벡터 DB 지원(LanceDB/Chroma/Milvus 로컬, Pinecone/Qdrant/Weaviate/Zilliz/AstraDB 클라우드). 조직 단위 = **Workspaces**. 별도 "agent memory" 기능은 홈 docs 단계에선 명시되지 않음 — 문서 RAG 와 동일 스택으로 보임.
- **Memory lifecycle**: 워크스페이스에 문서 업로드(insert) → 벡터화 → RAG 검색(retrieve). 업데이트/삭제는 워크스페이스 단위 파일 관리. 장기 에이전트 메모리 개념은 약함.
- **LLM Wiki positioning**: **retriever 중심, 제품 형태의 RAG box**. LLM 이 빌더가 아니며 Wiki 의 "LLM 이 만든다" 축과 거리가 멀다. 스케일: 데스크톱(1인) / 셀프호스트 / 클라우드 멀티유저 3트랙.
- **Deep-dive**: **no** — 이미 잘 알려진 RAG 제품. 메모리/지식 프레임워크 관점에선 새 아이디어 적음. 단 "벡터 DB 선택 매트릭스" 참조용으로만 유용.
- **Source quality**: primary

### 7. 상업 에이전트 메모리 (Claude / ChatGPT / Cognition Devin)
- **URL**:
  - Claude Memory: Anthropic 공식 발표 페이지 (news/memory) — 현재 blog/memory 로 리다이렉트 후 404 발생 (2026-04-21 시점) → **공식 소스 접근 불안정, (source availability unclear)**
  - ChatGPT Memory FAQ: https://help.openai.com/en/articles/8590148-memory-faq — 자동 요청 차단(403), 브라우저로는 접근 가능.
  - Cognition Devin: https://cognition.ai/ — 공식 블로그에서 "Devin's Wiki" 등 지식 자산 언급(이 프로젝트 노트에서 이미 일부 커버됐을 가능성).
- **What**: 각 상업 에이전트가 "사용자·프로젝트·세션" 스코프의 메모리를 내장해 재대화 시 맥락을 자동 이어주는 제품 기능.
- **Storage**: 모두 **opaque managed**. 사용자 시점에선 편집 가능한 텍스트 목록(ChatGPT·Claude) 또는 프로젝트별 컨텍스트(Devin) 로 노출. 내부 구현(벡터/그래프/DB) 공개 안 됨.
- **Memory lifecycle**:
  - ChatGPT: 모델이 대화 중 자동 저장 + 사용자 "Remember this" 로 강제 저장. 설정 → Manage memories 에서 개별 삭제. 옵트아웃 가능. (공식 FAQ 기준, 본 서베이에선 직접 fetch 실패 — **second-hand knowledge**)
  - Claude: 프로젝트 스코프의 영속 컨텍스트 + (엔터프라이즈) 팀 레벨 컨트롤로 출시됨(발표 페이지 접근 실패로 상세 미검증).
  - Devin: 세션 종료 시 "session knowledge" 를 Devin's Wiki 등 내부 자산에 승격(공식 블로그). builder 성격 강함.
- **LLM Wiki positioning**: 블랙박스 builder. 사용자에겐 편집 가능한 짧은 bullet 목록으로만 보여 **가독·편집·포팅 모두 LLM Wiki 대비 약함**. 상업 제품은 UX 단순화가 핵심이라 파일시스템·markdown 형태의 지식 자산으로는 내주지 않는 경향.
- **Deep-dive**: **maybe** — Devin 의 Wiki 승격 메커니즘은 LLM Wiki 와 컨셉이 겹쳐 follow 가치 있음. Claude/ChatGPT 는 UX 참조. **primary source 재수집 필요**.
- **Source quality**: thin / secondary (직접 fetch 실패 다수, date unclear)

## Cross-cutting 관찰

### LLM 역할 스펙트럼 (builder ↔ retriever)
- **순수 builder (LLM이 쓴다)**: Mem0 (자동 추출·덮어쓰기), Zep (자동 엔티티/엣지 추출·시간축 기록), ChatGPT/Claude/Devin 메모리.
- **self-editing builder (에이전트가 자기 손으로 쓴다)**: Letta — 도구 호출로 memory block 직접 편집.
- **사용자·LLM 공동 builder**: Basic Memory (markdown 을 양쪽이 편집), Karpathy LLM Wiki (저자 주도, LLM 은 보조).
- **순수 retriever**: Khoj, AnythingLLM — 사용자가 이미 쓴 것을 읽기만.

### 스토리지 선택 → UX 결과
- **Markdown 파일 (Basic Memory, LLM Wiki)**: 사용자가 **볼 수 있고, 복사·버전관리·포팅 가능**. 대신 시맨틱 검색/시간 축은 약함.
- **벡터 DB (Mem0, Khoj, AnythingLLM)**: 의미 검색 강함. 대신 사용자가 "내 지식" 을 직접 읽기 불가능(오paque chunks).
- **Temporal graph (Zep)**: "언제 유효했던 사실인가" 를 재현 가능. 대신 내부 상태 성격이 강해 사용자 UX 로는 거의 노출 안 됨.
- **릴레이셔널 + memory blocks (Letta / MemFS)**: 구조화된 에이전트 상태. MemFS 의 git-tracked 선택은 markdown 쪽으로 움직이는 신호.
- **매니지드 블랙박스 (ChatGPT/Claude/Devin)**: 편집 가능한 bullet 목록 정도만 사용자에게 노출. 포팅 사실상 불가.

### LLM Wiki 와 겹치는 지점 / 다른 지점
- **겹침**: Basic Memory(거의 직접 비교 가능), Letta MemFS(git-tracked 지향), Devin's Wiki(개념 수준).
- **다름**: 대부분의 프레임워크는 **런타임·자동·에피소딕 사실 조각** 에 최적화 — LLM Wiki 의 **compile-time·저자 주도·연결된 문서** 철학과 축이 다름. 즉 LLM Wiki 는 "지식 문서", 여타는 "상태 메모리" 에 가까움.

## Deep-dive 우선순위 top 3

1. **Basic Memory** — LLM Wiki 와 가장 가까운 형제(파일시스템 + markdown). MCP 도구면·인덱싱 방식·링크 그래프 세부만 확인하면 LLM Wiki 의 직접 비교군 확보.
2. **Letta (특히 MemFS)** — "LLM 이 자기 지식을 직접 쓴다" 는 철학을 가장 멀리 밀고 간 사례. MemFS 의 git-tracked 선택이 Wiki 쪽으로의 수렴인지 확인.
3. **Zep (+ Graphiti OSS)** — temporal invalidation 은 다른 어디에도 없는 축. "지식이 시간을 가진다" 가 개인 PKM 에 쓸 수 있는 아이디어인지 OSS 레포에서 구현 단계까지 내려가 볼 가치.

(Mem0 은 4위 — consolidation 프롬프트 내부가 궁금하지만 철학적으로 LLM Wiki 와 결이 덜 겹침.)

## 미답 / 열린 질문

- Basic Memory 의 내부 인덱스(SQLite/fts/임베딩 여부) — 홈페이지만으로 미확인, 레포 확인 필요.
- Letta MemFS 의 현재 위상 — "latest memory system" 이라는 표현인데 기존 core/archival/recall 과 공존인지 대체인지 공식 문서 명확화 필요.
- Zep 의 LLM 추출 파이프라인 프롬프트/모델 — Graphiti 레포에서만 확인 가능할 가능성.
- Mem0 의 conflict resolution 이 LLM arbitration 인지 deterministic rule 인지 — docs 에서 명시 안 됨.
- ChatGPT Memory FAQ, Anthropic Claude Memory 공식 페이지 — 이번 서베이 시점(2026-04-21)에 직접 fetch 실패(403 / 404 리다이렉트). **재수집 필요**.
- Cognition Devin 의 "session → wiki" 승격 루프 — 이 프로젝트 `notes/` 에 별도 딥다이브가 있는지 교차 확인 필요(중복 방지).
- 이번 서베이는 primary docs 중심이라 실제 **프로덕션 사용 후기/한계(e.g., Mem0 의 메모리 폭증, Zep graph 의 noise)** 는 미수집 — 필요 시 별도 세션.
