---
title: Basic Memory — Obsidian + MCP 통합 PKM
date: 2026-04-21
source_url: https://github.com/basicmachines-co/basic-memory
source_type: product / github / docs
topic: techniques
tags: [basic-memory, pkm, obsidian, mcp, markdown, memory, co-authored]
status: processed
---

## 요약 (3줄)

Basic Memory(Basic Machines, AGPL-3.0, 2.9k★)는 **local-first markdown 파일**을 single source of truth 로 두고 그 위에 **SQLite FTS5 + FastEmbed 하이브리드 인덱스**를 얹어 MCP 로 LLM에게 읽기·쓰기·그래프 탐색을 노출하는 사용자·LLM 공동 저작 PKM 이다. Karpathy LLM Wiki 와 **storage 축은 일치**(markdown + 파일시스템)하지만 **builder 축은 co-authored, timing 축은 runtime** 으로 명확히 갈린다 — 즉 "LLM Wiki 의 가장 가까운 형제" 가설은 **storage 1축 일치에 한정된 친족**으로 재정의된다. Lint 계열 연산은 존재(`schema_infer/validate/diff`, `basic-memory doctor`)하되 Cognee `improve`·LLM Wiki `Lint` 의 "의미적 노후화 탐지"보다 **구조 정합성 점검에 가까워** `knowledge-lifecycle-operations` 후보 카드의 2번째 사례로는 **부분 해당**.

---

## 핵심 포인트

1. **지식 단위는 "파일 = 엔티티" 삼층 모델**: `Entity` (frontmatter 가진 markdown 파일 1개) ← `Observations` (`- [category] content #tag (context)` 패턴 라인) ← `Relations` (`- relation_type [[WikiLink]] (context)` 패턴 라인). 이 세 요소가 markdown 문법 안에 임베드되어 파서가 SQLite 에 인덱싱.
2. **저장소 이중 레이어 — 파일 = 진실 / DB = 인덱스**: `.md` 파일이 source-of-truth, `~/.basic-memory/` SQLite(또는 Postgres) 는 파생 인덱스. `basic-memory sync --watch` 로 파일 → DB 실시간 반영, 사용자가 Obsidian/VS Code 로 직접 편집해도 재인덱싱됨.
3. **v0.19.0 (2026-03-07) FastEmbed 도입 — 하이브리드 검색**: 이전엔 SQLite FTS5 만. 이후 "FastEmbed-based embeddings with automatic backfill"(변경로그 원문) + "Hybrid search combining full-text and vector similarity, Score-based fusion replacing RRF for better ranking". 즉 **2026-03 시점에서 "순수 markdown + grep" 포지션을 이탈해 의미 검색 레이어를 가진 혼종**으로 이동.
4. **MCP 도구 15+ 종 — write/read/navigate/schema 4 계열**: `write_note`, `edit_note` (append/prepend/find_replace/insert_before_section/insert_after_section), `read_note`, `view_note`, `read_content`, `move_note`, `delete_note`, `search_notes`, `recent_activity`, `list_directory`, `build_context` (memory:// URL 다중 홉 탐색), `canvas` (그래프 시각화), `schema_infer/validate/diff`, `list/create_memory_project`, `sync_status`.
5. **`memory://` URL 프로토콜 = 그래프 탐색 API**: `build_context(url, depth, timeframe)` 가 relations 를 따라 depth-N 까지 재귀 CTE 로 그래프 확장. LLM 이 "관련 컨텍스트 모아줘" 를 한 번의 도구 호출로 처리.
6. **Obsidian 네이티브 호환 — `[[WikiLink]]`**: 링크 포맷은 Obsidian 표준. 사용자 vault 를 그대로 쓸 수 있고, 링크 그래프는 Obsidian 의 Graph View 나 Basic Memory 자체 `canvas` 도구로 시각화.
7. **스키마 연산 존재 — 단 "구조" 레벨**: v0.19.0 (2026-03-07) 에 `schema_infer` (기존 노트에서 스키마 추론), `schema_validate` (노트가 스키마에 맞는지 검증), `schema_diff` (프로젝트 간 스키마 비교). **의미적 모순/노후화 탐지는 아님** — frontmatter·관측 패턴의 형식 정합성 점검.
8. **Doctor 연산 — 파일 ↔ DB 일관성 진단**: `basic-memory doctor` (v0.17.4, 2026-01-05). 파일시스템과 SQLite 인덱스 간 불일치를 탐지·복구하는 운영 도구. **consolidation/dedup 은 아님**.
9. **Local-first = 철학 선언**: 홈페이지/README/블로그에서 반복 — "Everything your AI knows lives in plain text files you can open, read, and edit", "If you can't read it, edit it, or take it with you — it's not yours"(2026-03-15 블로그).
10. **상업 경쟁자를 의식한 포지셔닝**: 2026-03 블로그 "Basic Memory vs Mem0 vs Letta vs Everyone Else", "Everyone's Building Memory. Nobody's Building Yours." — opaque managed 메모리(ChatGPT/Claude memory)와의 차별점을 **사용자 소유권** 으로 직접 프레이밍.

---

## 아키텍처 / 스토리지

### 레이어 분해 (deepwiki 기준)

```
┌─────────────────────────────────────────────┐
│ MCP Tools Layer                             │  ← LLM 이 보는 표면
│   write_note / read_note / build_context …  │
├─────────────────────────────────────────────┤
│ Service Layer                               │
│   ContextService / EntityService /          │
│   FileService                               │
├─────────────────────────────────────────────┤
│ Repository Pattern                          │
│   EntityRepo / ObservationRepo /            │
│   RelationRepo / SearchRepo                 │
├─────────────────────────────────────────────┤
│ Data Layer                                  │
│   SQLite (default) / Postgres (v0.16+)     │
│   + FastEmbed vectors (v0.19+)             │
│   ↔ Markdown files on disk (.md)           │
└─────────────────────────────────────────────┘
```

### 핵심 설계 결정

- **파일 = 소스 오브 트루스, DB = 파생 인덱스**: 재구축 가능. 사용자가 파일만 백업하면 전체 복원 가능(포팅/버전관리 보장).
- **Multi-hop 그래프 탐색은 recursive CTE**: `ContextService` 가 재귀 CTE 로 depth-N 확장 후 N+1 방지 배칭. 벡터 유사도가 아닌 **명시적 관계 엣지** 를 따라가는 그래프 탐색.
- **Dual backend (SQLite / Postgres)**: v0.16.0 (2025-11-10) 부터 Postgres 지원. 테스트에 testcontainers. 즉 1인 로컬부터 팀/클라우드까지 같은 스택.
- **FastEmbed 는 로컬 임베딩**: 외부 OpenAI embeddings API 호출 불필요 — local-first 철학과 정합.

### "storage detail unclear" 플래그 해소 (inbox 서베이 대비)

서베이 시점엔 "별도 벡터/그래프 인덱스 홈페이지 단계에선 불명(쿼리 시 내부에 SQLite/fts 가능성은 있으나 primary source 미확인)" 이라고만 기록됐으나, 본 deep-dive 에서 확인 — **SQLite FTS5 (기본) + FastEmbed hybrid (v0.19+)**. 즉 축 2(storage)는 **"markdown + hidden SQLite+vector index"** 의 혼종.

---

## MCP 도구 표면

### Content management (write-path + read-path)

| 도구 | 파라미터 | 역할 |
|---|---|---|
| `write_note` | title, content, folder, tags, output_format | 생성/업서트 |
| `edit_note` | identifier, operation (append/prepend/find_replace/insert_before_section/insert_after_section), content | 인크리멘탈 편집 |
| `read_note` | identifier, page, page_size | 제목/permalink 로 읽기 |
| `view_note` | identifier | 포맷된 artifact 표시 |
| `read_content` | path | 원본 바이너리·텍스트·이미지 접근 |
| `move_note` | identifier, destination_path | 재배치 + DB 동기화 |
| `delete_note` | identifier | 파일 삭제 + 인덱스 갱신 |

### Graph navigation

| 도구 | 파라미터 | 역할 |
|---|---|---|
| `build_context` | url (memory://), depth, timeframe | 관계 엣지 따라 재귀 CTE 확장 |
| `recent_activity` | type, depth, timeframe | 최근 갱신 탐색 |
| `list_directory` | dir_name, depth | 파일시스템 브라우즈 |
| `canvas` | nodes, edges, title, folder | 그래프 시각화 산출 |

### Search

| 도구 | 파라미터 | 역할 |
|---|---|---|
| `search_notes` | query, search_type, types, entity_types, after_date, metadata_filters, tags, status, project | 하이브리드 필터링 검색 (FTS5 + vector) |

### Schema / maintenance (v0.19.0+)

| 도구 | 역할 |
|---|---|
| `schema_infer` | 기존 노트에서 스키마 추론 |
| `schema_validate` | 노트를 스키마에 검증 |
| `schema_diff` | 프로젝트 간 스키마 비교 |

### Project / operational

| 도구 | 역할 |
|---|---|
| `list_memory_projects` / `create_memory_project` / `get_current_project` | 멀티 프로젝트 관리 |
| `sync_status` | 동기화 상태 조회 |
| `basic-memory doctor` (CLI) | 파일↔DB 일관성 진단·복구 |

### Write-path vs Read-path 분리 판정

**분리 안 됨 — 의도적 통합**. LLM 이 같은 MCP 표면으로 읽고 쓴다. write 도구(`write_note`/`edit_note`/`move_note`/`delete_note`)와 read 도구(`read_note`/`search_notes`/`build_context`)는 별 함수로 나뉘어 있으나, **같은 MCP 세션 안에서 LLM 이 자유롭게 둘을 섞어 호출**. LLM Wiki 의 "사용자 승인 후 쓰기" 게이트는 Basic Memory 에 **없음** — co-authored 철학상 LLM 이 직접 쓴다.

---

## 지식 라이프사이클

### insert (생성)

- 사용자가 대화 중 "이거 기억해둬" → LLM 이 `write_note` 호출 → markdown 파일 생성 → sync watcher 가 SQLite 인덱싱.
- 사용자가 Obsidian 에서 직접 `.md` 파일 추가 → `basic-memory sync --watch` 가 감지 → 파싱 후 인덱싱.
- **트리거**: 대화 맥락 기반 LLM 판단 **또는** 사용자 파일 생성 — 양방향.

### retrieve (읽기)

- LLM 이 `search_notes` (하이브리드 FTS+vector) → 후보 페이지 → `read_note` 또는 `build_context(memory://..., depth=N)` 로 그래프 확장.
- **트리거**: 사용자 질문에 답할 때 LLM 자동 판단 — retriever-agnostic. (LLM Wiki 는 `index.md` 를 먼저 읽어야 하는 고정 순서였음.)

### update (갱신)

- `edit_note(operation=append|find_replace|insert_before_section|…)` — 블록 단위 인크리멘탈 편집. 전체 재작성 아님.
- 사용자가 Obsidian 에서 파일 직접 수정해도 동일. DB 는 watcher 로 재인덱싱.
- **충돌 해소 정책**: 공식 문서 범위 외 — 미답. Mem0 의 "last-write-wins LLM arbitration" 같은 정책이 있는지 명시 안 됨 — **(공식 문서 범위 외 — 미답)**.

### forget (삭제)

- `delete_note` 또는 파일시스템에서 직접 삭제. TTL·자동 망각 없음.
- 사용자 주도 삭제만. Zep 의 "temporal invalidation"(엣지에 invalid 타임스탬프) 없음.

### 라이프사이클 판정 — 축 3(timing) 정확 좌표

**Runtime, 증분, 연속 동기화**. LLM Wiki 의 "compile-time 정적 스냅샷" 과 정면 대비. 서베이 가설 대로 Basic Memory 는 runtime 축에 위치.

---

## LLM Wiki 와의 3축 비교 매트릭스

| 축 | LLM Wiki | Basic Memory | 일치 여부 |
|---|---|---|---|
| **축 1 — Builder** | curation (사용자 raw/ 선별 → LLM wiki/ 빌드, 사용자 승인 게이트) | **co-authored** (사용자·LLM 둘 다 `.md` 직접 편집, 승인 게이트 없음) | **불일치** |
| **축 2 — Storage** | markdown 파일시스템 + `index.md` 직독 | markdown 파일시스템 + **SQLite FTS5 + FastEmbed vector 하이브리드 인덱스** | **부분 일치** (markdown 일치 / 인덱스 존재 유무 불일치) |
| **축 3 — Timing** | compile-time (ingest 시 요약·상호연결·index 확정) | **runtime 증분** (대화/파일 변경 → 실시간 재인덱싱) | **불일치** |

### 상사점 (3건)

1. **사용자 소유 markdown 파일**: 둘 다 `.md` 가 source-of-truth. 사용자가 볼 수 있고 git 버전관리·포팅 가능.
2. **Obsidian/wikilink 계열 링크 문법**: 둘 다 `[[WikiLink]]` 를 내부 링크 포맷으로 사용. LLM Wiki 는 "Obsidian 호환", Basic Memory 는 "Obsidian 네이티브".
3. **그래프 탐색 지향**: LLM Wiki 는 `index.md` 의 카테고리 테이블로, Basic Memory 는 `build_context(memory://)` recursive CTE 로 — 구현은 다르나 "관련 페이지 집합을 모아 답한다" 는 의도는 일치.

### 상이점 (4건)

1. **빌더 권한 구조**: LLM Wiki 는 **사용자가 큐레이터, LLM 이 저자, 그 사이에 승인 게이트**. Basic Memory 는 **양쪽이 동등하게 저자** — 게이트 없음. Karpathy 원문 "You don't write the wiki. The LLM does." 와 Basic Memory 홈페이지 "Everything your AI knows lives in plain text files you can open, read, and edit" 의 미묘하지만 결정적 차이.
2. **지식 형성 시점**: LLM Wiki 는 ingest 시 "summarize + cross-reference + contradiction flag" 를 **일괄 배치**로 수행. Basic Memory 는 파일이 들어오는 대로 **라인별 observation/relation 패턴** 을 파싱해 증분 인덱싱 — synthesis 단계 없음.
3. **인덱스 vs 임베딩**: LLM Wiki 는 **임베딩 없음** (`index.md` 직독). Basic Memory 는 v0.19 부터 **FastEmbed vector 포함 하이브리드**. 결과 — Basic Memory 는 LLM Wiki 가 명시적으로 거부한 "검색 레이어" 를 내장.
4. **"지식 문서" vs "상태 메모리"의 경계**: LLM Wiki 는 연결된 긴 개념 페이지 중심(synthesis/overview 레이어 존재). Basic Memory 는 observation 한 줄 단위 삽입이 자연스러운 구조 — **양쪽을 다 커버하려 하나, 실제 사용 패턴은 상태 메모리 쪽에 가까워 보임**(블로그 "Mem0/Letta 와의 비교" 프레이밍이 이를 뒷받침).

### "가장 가까운 형제" 가설 재평가

서베이가 제시한 가설 — "LLM Wiki 의 가장 가까운 형제" — 은 **축 2(storage)의 markdown 선택 1건에만 해당**. 축 1(builder)·축 3(timing)은 다른 위치.

**재정의**: Basic Memory 는 "markdown + 사용자소유" 2번째 표본이지만, **LLM Wiki 의 형제라기보다 Mem0/Letta 를 markdown 으로 이식한 하이브리드**. `primitive-knowledge-layer-design-space.md` 3축 매트릭스에서 이는 **"curation+markdown+compile-time" (LLM Wiki) vs "co-authored+markdown+runtime" (Basic Memory)** 두 점으로 분리 기록해야 정확.

---

## Lint / Refinement 연산 존재 여부

### 확인된 maintenance 연산

| 연산 | 대상 | 수준 |
|---|---|---|
| `schema_infer` | 기존 노트 → 스키마 추출 | 구조 레벨 |
| `schema_validate` | 노트가 스키마에 맞는가 | 구조 레벨 |
| `schema_diff` | 프로젝트 간 스키마 비교 | 구조 레벨 |
| `basic-memory doctor` | 파일↔DB 일관성 | 인프라 레벨 |

### 판정 — Cognee `improve` · LLM Wiki `Lint` 와의 비교

| 검사 항목 | LLM Wiki Lint | Cognee `improve` | Basic Memory |
|---|---|---|---|
| Orphan 페이지 | ○ | ?* | **× 미답** |
| Superseded/stale claims | ○ | ○ | **× 명시 없음** |
| Missing concept (N페이지 언급·전용페이지 없음) | ○ | ?* | **× 명시 없음** |
| Research gap (특정 토픽 유입 중단) | ○ | ?* | **× 명시 없음** |
| Schema/frontmatter 정합성 | △ (convention 수준) | ?* | **○ schema_validate** |
| 파일↔인덱스 일관성 | — | — | **○ doctor** |

*Cognee 세부는 `primitive-knowledge-layer-design-space.md` 시점 확인 범위 외.

### 카드 후보 판정

`knowledge-lifecycle-operations` primitive 카드의 **2번째 사례로는 부분 해당**.

- **해당하는 축**: "구조 정합성 점검" 이라는 하위 카테고리에서 `schema_validate` 는 LLM Wiki 의 convention 점검과 동류. 
- **해당하지 않는 축**: "의미적 노후화 / 모순 / 고아" 같은 **semantic lint** 는 Basic Memory 에 **부재** — 공식 도구로는 미확인.

즉 Lint 는 **"structural lint" vs "semantic lint" 하위 축으로 더 쪼개질 필요**가 있음. Basic Memory 는 structural 만, LLM Wiki 는 둘 다, Cognee `improve` 는 semantic 중심으로 추정. 이 발견은 후속 `knowledge-lifecycle-operations` 카드 작성 시 **하위 분류 프레임**으로 편입 가치 있음.

---

## 저자 설계 철학

### 인용 1 — 경쟁 포지셔닝 (README)

> "Chat histories capture conversations but aren't structured knowledge. RAG systems can query documents but don't let LLMs write back. Vector databases require complex setups and often live in the cloud. Knowledge graphs typically need specialized tools to maintain."
>
> (번역) "채팅 기록은 대화를 담지만 구조화된 지식이 아니다. RAG 는 문서를 질의할 수 있지만 LLM 이 역방향으로 쓸 수 없다. 벡터 DB 는 복잡한 세팅이 필요하고 대개 클라우드에 산다. 지식 그래프는 보통 유지보수에 전문 도구가 필요하다."

→ 4가지 대안(chat / RAG / vector DB / graph) 을 **각각 한 줄로 반박**해 자신의 포지션을 네거티브 정의로 세움.

### 인용 2 — 소유권 원칙 (2026-03-15 블로그 "Everyone's Building Memory. Nobody's Building Yours.")

> "If you can't read it, edit it, or take it with you — it's not yours."
>
> (번역) "읽을 수도, 편집할 수도, 들고 떠날 수도 없다면 — 그건 네 것이 아니다."

→ ChatGPT/Claude memory 같은 opaque managed 메모리에 대한 직접적 대비. "사용자 소유권" 을 **read + edit + port** 3조건으로 정의한 선언문.

### 인용 3 — 미션 (README 첫 문단)

> "Basic Memory lets you build persistent knowledge through natural conversations with Large Language Models (LLMs) like Claude, while keeping everything in simple Markdown files on your computer."
>
> (번역) "Basic Memory 는 Claude 같은 LLM 과 자연스러운 대화를 통해 지속 가능한 지식을 쌓되, 모든 것을 당신 컴퓨터의 간단한 markdown 파일로 유지한다."

→ 두 가지 의도의 결합 — **"대화 기반 runtime builder"**(Mem0/Letta 쪽 가치) **+ "로컬 markdown 소유"**(LLM Wiki 쪽 가치). 이 결합이 Basic Memory 의 설계 좌표를 설명하는 짧은 문장.

---

## 스케일 감각

### 공식 문서에서 확인된 스케일 단서

- **Dual backend (SQLite / Postgres)**: v0.16.0 부터. 개인 로컬(SQLite) → 팀·클라우드(Postgres) 연속 스펙트럼을 같은 코드 경로로 지원.
- **디렉토리 연산 v0.15.1 최적화**: "10-100x performance improvement in listing speed" — 노트 수가 늘어날 때의 리스팅/네비게이션 비용을 의식한 최적화.
- **Recursive CTE 그래프 탐색 + N+1 방지 배칭**: deepwiki 의 설명은 "대규모에서도 쿼리 수 제어" 를 염두에 둔 구현이라는 신호.
- **FastEmbed 로컬 임베딩**: 노트 수가 커져도 외부 API 호출 비용 없이 의미 검색 가능.

### 공식 언급 없음 (미답)

- **"몇 천 노트부터 성능 저하" 같은 수치적 브레이크포인트**: 공식 docs/README/블로그 범위 외 — **(공식 문서 범위 외 — 미답)**.
- **LLM Wiki 의 "~100 소스·수백 페이지 index 붕괴점" 같은 문서화된 상한**: Basic Memory 는 **index.md 없이 DB 검색으로 탐색**하므로 **같은 종류의 붕괴점이 구조적으로 존재하지 않음** — 그러나 다른 종류의 한계(DB 크기·임베딩 메모리·watcher 처리량)는 미기재.

### 평가

LLM Wiki 가 "~100 소스" 에서 무너지는 지점을 Basic Memory 는 **SQLite+vector 인덱스 도입으로 회피**한 것으로 보임. 대신 LLM Wiki 의 장점(전체 wiki 가 컨텍스트에 들어가 95% 토큰 절감) 도 함께 상실 — **스케일 가능성 ↔ 컨텍스트 밀도** 트레이드오프를 명시적으로 선택.

---

## 연결

- **`insights/primitive-knowledge-layer-design-space.md`** — 본 노트는 3축 매트릭스에서 **두 번째 표본점(co-authored + markdown + runtime)** 을 추가. 기존 카드가 LLM Wiki 를 "curation+markdown+compile-time" 단일 점으로 찍었다면, Basic Memory 는 **"markdown 축 공유 · 나머지 두 축 상이" 의 독립 좌표**로 등재되어야 함. 카드 내부의 "축 상관 끊기" 구성요소 3번 섹션에 "co-authored+markdown+runtime 은 Basic Memory 로 점유됨" 으로 업데이트 필요.
- **`notes/techniques/karpathy-llm-wiki.md`** — 직접 비교군. LLM Wiki 노트의 "RAG 와의 비교 표" 와 대응되는 "Basic Memory 와의 비교 표" 를 본 노트 상단에 배치. LLM Wiki 측 노트의 "후속 조사" 항목 중 "Basic Memory 의 MCP 도구 5종 스키마" 는 본 노트에서 15+ 종으로 확장 확인됨 — 해당 항목 close 가능.
- **후보 `knowledge-lifecycle-operations` 카드** — 본 deep-dive 가 "structural lint vs semantic lint" 하위 분류 필요성을 드러냄. Cognee `improve` 와 LLM Wiki `Lint` 2건 + Basic Memory 의 `schema_validate` / `doctor` 1건 = 총 3 사례 확보됐으므로 카드 분기 **가능 시점 도달**.
- **`inbox/2026-04-21-memory-pkm-survey.md`** — "Basic Memory storage detail unclear" 미답 플래그 해소. "SQLite FTS5 + FastEmbed hybrid (v0.19+)" 로 갱신 필요.
- **Mem0 / Letta deep-dive (미작성)** — Basic Memory 블로그 2026-03 "vs Mem0 vs Letta" 가 이 세 프레임워크를 직접 경쟁 관계로 놓음. Basic Memory 가 "co-authored+markdown+runtime" 좌표에서 Mem0(induction+vector+runtime) · Letta(self-editing+relational+runtime) 와 어떻게 다른지, 각 deep-dive 후 교차 매트릭스 작성 가치 있음.

---

## Sources

- [basicmachines-co/basic-memory GitHub repository](https://github.com/basicmachines-co/basic-memory) — 2.9k★ / AGPL-3.0, 2026-04-21 fetch
- [basicmemory.com 공식 홈페이지](https://basicmemory.com/) — 2026-04-21 fetch
- [docs.basicmemory.com 공식 docs 인덱스](https://docs.basicmemory.com) — 2026-04-21 fetch (내부 하위 페이지 일부 404)
- [basic-memory CHANGELOG.md](https://github.com/basicmachines-co/basic-memory/blob/main/CHANGELOG.md) — 버전 이력. v0.13 (2025-06 FTS5), v0.16 (2025-11 Postgres), v0.17.4 (2026-01 doctor), v0.19.0 (2026-03-07 FastEmbed/schema), v0.19.1, v0.20.0 (2026-03-10 auto-update)
- [basic-memory README.md](https://github.com/basicmachines-co/basic-memory/blob/main/README.md) — 미션 선언·엔티티/관측/관계 3 요소 설명, 2026-04-21 fetch
- [DeepWiki — MCP Server Setup (Context Service Architecture)](https://deepwiki.com/basicmachines-co/basic-memory/10.1-mcp-server-setup) — Repository/Service/MCP 3 계층 구조, recursive CTE 그래프 탐색 세부, 2026-04-21 fetch
- [Basic Memory 블로그 인덱스](https://basicmemory.com/blog) — 2026-03 시점 "Mem0/Letta 와의 비교" · "local-first 선언" 게시물 확인, 2026-04-21 fetch
