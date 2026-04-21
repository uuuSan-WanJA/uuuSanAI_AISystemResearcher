---
title: Graphify — 하네스-교차 knowledge-graph skill
date: 2026-04-21
source_url: https://github.com/safishamsi/graphify
source_type: repo / pypi / skill
topic: techniques (tier 재평가 후보 — cross-harness-skill 또는 infra-tier)
tags: [graphify, knowledge-graph, skill, multi-harness, obsidian, mcp, neo4j, leiden, confidence-tiering, penpax]
status: processed
---

## 요약 (3줄)

Graphify 는 `pip install graphifyy` 하나로 설치되고 Claude Code·Codex·Cursor·Gemini CLI·Copilot CLI·OpenClaw 등 **10+ 개의 AI 코딩 하네스에 동일 `/graphify` skill 로 주입**되는, 폴더 → 지식 그래프 파이프라인. 내부는 **Tree-sitter AST(결정적) + LLM 서브에이전트(의미) 듀얼 패스 추출 → Leiden 커뮤니티 탐지 → 6가지 출력 표면(HTML/JSON/Obsidian/Neo4j/MCP/wiki)**으로 구성되며, 모든 엣지를 `EXTRACTED / INFERRED / AMBIGUOUS` 3-tier confidence 로 태깅해 "invent 금지" 규율을 skill 레벨 honesty rule 로 박아둔 점이 지형 내 이례. 2026-04-04 첫 릴리스(PyPI v0.1.1) 후 17일 만에 31.4k stars 로 폭발 — Karpathy 가 2026-04-02 게시한 *LLM Knowledge Bases* 트윗의 48시간 직후 등장했다는 서사가 1차 바이럴 드라이버.

---

## 핵심 포인트

1. **단일 upstream, 다중 하네스**: `safishamsi/graphify` 하나가 Claude Code, Codex, OpenCode, Cursor, Gemini CLI, GitHub Copilot CLI, VS Code Copilot Chat, Aider, OpenClaw, Factory Droid, Trae, Hermes, Kiro, Google Antigravity 를 공식 지원 (README 타이틀 verbatim). "하네스별 포팅" 이 아니라 "동일 `/graphify` trigger + 동일 PyPI 엔진 + 하네스별 skill 파일" 구조.
2. **skill 자체가 1245줄 파이프라인 스크립트**: `SKILL.md` (51 KB) 가 Step 1–9 + 4개 서브커맨드(`query / path / explain / add`) + `--update / --cluster-only / --watch` 분기까지 전부 **PowerShell + Python inline** 로 하드코딩. 하네스는 이 skill 을 "읽고 실행" 만 하면 됨 — 즉 skill 이 곧 orchestration 코드.
3. **듀얼 패스 추출**: Part A (Tree-sitter AST, 결정적, 무료) + Part B (LLM 서브에이전트, 청크당 20–25 파일씩 병렬 dispatch). 두 패스는 **같은 메시지에서 동시 시작** (Step 3 verbatim: *"Run Part A (AST) and Part B (semantic) in parallel. Dispatch all semantic subagents AND start AST extraction in the same message"*). 5–15초 절감을 명시적으로 회수.
4. **confidence 3-tier 가 의무 필드**: 모든 엣지에 `confidence_score` REQUIRED, 기본값 0.5 사용 금지. EXTRACTED=1.0, INFERRED=0.4–0.9(상세 구간 지정), AMBIGUOUS=0.1–0.3. skill 의 *Honesty Rules* 섹션 첫 줄: *"Never invent an edge. If unsure, use AMBIGUOUS."* — 추론 품질의 **감사 가능성**을 설계 1등 시민으로 선언.
5. **추출 캐시**: Step B0 에서 `graphify.cache.check_semantic_cache()` 로 파일 해시 기반 캐시 히트 판정, uncached 만 서브에이전트 dispatch. `--update` 는 여기에 `detect_incremental()` 을 더해 "코드만 바뀐 커밋" 은 LLM 호출 0회로 재빌드 (Step: *"Code-only changes detected — skipping semantic extraction (no LLM needed)"*).
6. **Leiden 커뮤니티 + 고유 분석 산출**: `graphify.cluster.cluster()` 가 Leiden 으로 묶고, `analyze.god_nodes()` (높은 degree 중심성 노드), `surprising_connections()` (서로 다른 커뮤니티를 잇는 이례 엣지), `suggest_questions()` 를 자동 계산. 사용자에게 "이 그래프가 가장 흥미롭게 답할 수 있는 질문" 을 **파이프라인 종료 직후 1개 추천** 하는 것이 Step 9 의 마지막 지시 — skill 이 "report 출력" 에 그치지 않고 **탐색 세션으로 전환 유도**.
7. **6가지 출력 표면 동시 생성**: HTML (항상, 5000노드 이하), GRAPH_REPORT.md (항상), graph.json (항상), Obsidian vault (`--obsidian`), Neo4j Cypher / bolt push (`--neo4j / --neo4j-push`), SVG/GraphML (선택), MCP stdio 서버 (`--mcp`), agent-crawlable wiki (`--wiki`). 하나의 추출 결과를 다수 소비자 표면에 얹는 "fan-out 아키텍처".
8. **watch + git hook 이중 auto-incremental**: `python -m graphify.watch` 로 debounce 3초 파일 워처, `graphify hook install` 로 post-commit 훅. 둘 다 "코드만 바뀌면 LLM 안 부르고 AST 만 재실행" 규칙 공유. **agentic workflow 용 설계** 명시 (*"Code changes from agent waves are picked up automatically between waves"*).
9. **ingest 자동화**: `/graphify add <url>` 로 Twitter/X (oEmbed), arXiv, PDF, 이미지, 웹페이지를 자동 분기 수집·markdown 변환해 `./raw/` 에 넣고 `--update` 까지 연쇄. **저자/기여자 프론트매터** (`--author`, `--contributor`) 를 노드 메타로 승격.
10. **query feedback loop**: `query / path / explain` 답변을 `python -m graphify save-result` 로 그래프에 역피드 (*"This closes the feedback loop: the next `--update` will extract this Q&A as a node in the graph"*). 그래프가 자기 사용 기록을 흡수하는 **self-enlarging** 설계.

---

## 파이프라인 아키텍처 — Step 1–9 enumeration

| Step | 역할 | LLM 개입 | 출력 |
|---|---|---|---|
| 1 | graphifyy 설치 확인 · Python interpreter 경로 고정 | ✗ | `.graphify_python` |
| 2 | `detect()` — 파일 분류(code/docs/papers/images/video), 단어 수, 민감 파일 skip, 200+ 파일/2M+ 단어 시 subfolder 질의 | ✗ | `.graphify_detect.json` |
| 2.5 | (video 감지 시만) Whisper 전사 — **LLM 이 스스로 도메인 힌트 한 문장 작성** 해 initial prompt 주입 | 간접 (Whisper, LLM prompt 자작) | `.graphify_transcripts.json` |
| 3A | Tree-sitter AST — `graphify.extract.extract()`, 25 언어 | ✗ | `.graphify_ast.json` |
| 3B | 서브에이전트 병렬 dispatch (청크 20–25 파일, 단일 메시지 내 N개 Agent 호출 의무) | ◎ | `graphify-out/.graphify_chunk_NN.json` |
| 3C | AST + semantic 병합, node id 기반 dedup | ✗ | `.graphify_extract.json` |
| 4 | `build_from_json → cluster(Leiden) → score_all(cohesion) → god_nodes / surprising_connections / suggest_questions` | ✗ | `graph.json`, `GRAPH_REPORT.md`, `.graphify_analysis.json` |
| 5 | **LLM (메인 세션)** 이 각 커뮤니티 id 에 2–5단어 라벨 직접 작성 → report 재생성 | ◎ (메인 세션이 직접) | `.graphify_labels.json`, 갱신된 REPORT |
| 6 | HTML (default, ≤5000 노드), Obsidian vault + Canvas (`--obsidian` 시) | ✗ | `graph.html`, `obsidian/*.md`, `graph.canvas` |
| 7a–c | Neo4j Cypher 파일 또는 bolt push, SVG, GraphML 조건부 | ✗ | `cypher.txt`, `graph.svg`, `graph.graphml` |
| 7d | MCP stdio 서버 (`--mcp`) — `query_graph / get_node / get_neighbors / get_community / god_nodes / graph_stats / shortest_path` 노출 | 런타임 LLM (Claude Desktop 등) | stdio 바인드 |
| 8 | `>5000 단어` 시 토큰 절감 벤치마크 (예: 71.5× 절감 수치 공식 주장의 출처) | ✗ | stdout |
| 9 | manifest 저장, 누적 cost tracker 갱신, 정리, **"가장 흥미로운 질문" 1개로 탐색 제안** | ✗ (출력은 LLM) | `graphify-out/cost.json` |

**LLM 호출이 실제로 발생하는 지점은 3곳**: (1) 3B 서브에이전트 (가장 비쌈), (2) 2.5 Whisper prompt 자작, (3) 5 커뮤니티 라벨링. 나머지는 deterministic Python — "compile-time 인덱스 + runtime 질의 2단" 중 compile-time 에만 LLM 비용 집중.

---

## Confidence tiering (EXTRACTED / INFERRED / AMBIGUOUS) — 지형 내 이례

skill 에 박힌 규칙 verbatim (Step 3B 프롬프트):

- `EXTRACTED`: *"relationship explicit in source (import, call, citation, 'see §3.2')"* → `confidence_score = 1.0 always`
- `INFERRED`: *"reasonable inference (shared data structure, implied dependency)"* → 0.4–0.9, 구간별 상세 지침 (*"Direct structural evidence: 0.8–0.9. Reasonable inference with some uncertainty: 0.6–0.7. Weak or speculative: 0.4–0.5. Most edges should be 0.6–0.9, not 0.5"*)
- `AMBIGUOUS`: *"uncertain — flag for review, do not omit"* → 0.1–0.3

**지형 내 이례성**: `insights/primitive-knowledge-layer-design-space.md` 의 서베이 14종 중 confidence 를 엣지 필수 필드로 강제하는 KG 프레임워크는 확인되지 않음 (GraphRAG / LightRAG / HippoRAG / PathRAG / Cognee / Neo4j LLM-GB / nano-graphrag 전부 엣지 품질 태깅 없음). Zep 의 `valid_from/invalid_at` 은 **시간적 유효성**이지 **추출 신뢰도**가 아님. Graphify 의 3-tier 는 **"LLM 이 만들어낸 엣지" 와 "원본에서 발견한 엣지"를 혼동하지 않는다** 는 인식론적 규율을 skill-level honesty rule 로 직접 박은 드문 사례.

이 축은 **promotion 가치 있음** — `insights/` 에 `edge-epistemic-tagging` (후보) 카드로 분기할 만함. 단일 사례이므로 2번째 관찰(예: Cognee `improve` 가 엣지 confidence 를 들고 있는지, Neo4j LLM-GB 의 provenance 필드) 대기.

---

## 출력 표면 매트릭스

| 표면 | 트리거 | 주 소비자 | 특성 |
|---|---|---|---|
| `graph.html` | default (≤5000 노드) | 사람 (브라우저) | 서버 불필요, 단일 파일 |
| `GRAPH_REPORT.md` | default | 사람 + LLM | god nodes / surprising / suggested Q 섹션이 chat paste 대상 |
| `graph.json` | default | LLM / MCP / 외부 도구 | node_link format, 재로드 가능 |
| Obsidian vault (`--obsidian`) | opt-in | 사람 (Obsidian) | 노드당 파일 1개, 커뮤니티별 `_COMMUNITY_*` overview, `graph.canvas` 구조화 레이아웃, dataview 쿼리 |
| Neo4j (`--neo4j` / `--neo4j-push`) | opt-in | DBA / GraphQL 앱 | MERGE 기반 idempotent, bolt 직접 push |
| SVG / GraphML | opt-in | 블로그/Notion/GitHub / Gephi / yEd | 임베드·외부 툴 호환 |
| MCP stdio 서버 (`--mcp`) | opt-in | 다른 agent (Claude Desktop 등) | 7개 tool: query/get_node/get_neighbors/get_community/god_nodes/graph_stats/shortest_path |
| Wiki (`--wiki`) | opt-in | 에이전트 크롤러 | `index.md + 커뮤니티당 article 1개` — 명시적으로 LLM Wiki 호환 포맷 (skill usage verbatim: *"build agent-crawlable wiki (index.md + one article per community)"*) |

**`--wiki` 모드가 중요**: Graphify 를 "그래프 전용 도구" 가 아니라 **Karpathy 의 `/raw → /wiki` 구조에 직접 플러그인**하도록 설계했다는 증거. What-graphify-is-for 섹션 verbatim: *"graphify is built around Andrej Karpathy's /raw folder workflow: drop anything into a folder — papers, tweets, screenshots, code, notes — and get a structured knowledge graph"*. 즉 한국 커뮤니티의 "보완재" 포지셔닝은 upstream 의 공식 self-positioning 과 **정합**.

---

## 하네스 통합 — 커버리지와 adapter 구조

**공식 지원 하네스 목록** (GitHub README 타이틀 verbatim): Claude Code, Codex, OpenCode, Cursor, Gemini CLI, GitHub Copilot CLI, VS Code Copilot Chat, Aider, OpenClaw, Factory Droid, Trae (+ Trae CN), Hermes, Kiro, Google Antigravity.

**adapter 구조 (inbox probe + SKILL.md 증거)**:

- **엔진 일원화**: `graphifyy` PyPI 패키지 하나가 모든 로직 (`graphify.detect / extract / cluster / build / analyze / export / serve / transcribe / cache / benchmark / ingest / watch`). 하네스는 이 패키지를 **import + CLI 호출** 만 함.
- **설치 커맨드**: `pip install graphifyy && graphify install` — `graphify install` 서브커맨드가 플랫폼 감지 후 하네스별 디렉터리에 skill 파일 배치 (사용자 로컬 skill frontmatter 가 `graphify-windows` 인 것이 증거).
- **트리거 통일**: 모든 하네스에서 `/graphify <path>` 동일 슬래시 커맨드. 하네스별 skill 파일은 **같은 SKILL.md 를 plat-specific 쉘 문법**(PowerShell vs bash)으로 바꾼 변형.
- **별도 바이너리 없음**: skill 파일 + PyPI 엔진 조합. Hermes/OpenClaw 처럼 자체 런타임을 두지 않음.

**tier 판정**:

기존 리서치 프로젝트의 4-tier (`harness/` agent-loop-shapers / `agents/` agent-framework / `infra/` gateway-control-plane / `techniques/` pattern-level) 중 Graphify 는 **어느 쪽에도 깔끔히 들어가지 않음**:

- `harness/` 가 아님: 자체 agent loop 이 없음. 호스팅되는 쪽.
- `agents/` 가 아님: LLM 호출은 하지만 자율 에이전트가 아니라 고정 파이프라인.
- `infra/` 에 인접하지만 다름: OpenClaw 같은 gateway control plane 이 아니라 **skill 레벨 툴**.
- `techniques/` 로 두긴 했지만 단일 패턴이 아니라 **구현체 + 다중 하네스 확장 포맷**.

→ **권고: 신규 tier 후보 `cross-cutting-skill` (또는 `skill-engine`)** 을 `meta/harness_schema.md` 에 제안. 2번째 사례가 나올 때 정식 승격(현재 1번째). 후보 2번째는: 어떤 하네스든 `/graphify` 유사하게 공통 트리거로 불리는 PyPI/npm 엔진 — 예컨대 추후 식별될 "skill-as-PyPI-package" 패턴 (현재는 graphify 단 하나). 임시 보관 위치는 `techniques/` 유지.

---

## 3축 프레임 판정 (primitive 카드 직접 적용)

**축 1 — Builder (누가 그래프를 쓰는가)**

- Tree-sitter AST (structural induction, 비-LLM) + LLM 서브에이전트 (semantic induction). 둘 다 **induction**.
- 사용자 curation 개입 지점: 지엽적 — `/graphify add <url>` 시 author/contributor 태그 부여, `query / path / explain` 답변 승인 여부. 그러나 **어떤 엣지가 그래프에 들어갈지** 는 사용자가 선택하지 않음. AMBIGUOUS 엣지도 "flag for review, do not omit" — 즉 들어가되 태깅됨.
- 판정: **induction (primary) + 매우 얕은 co-authored 요소**. primitive 카드의 `curation` 축에서 먼 지점.

**축 2 — Storage (무엇에 쓰는가)**

- 1차 저장소: `graph.json` (node_link format, NetworkX 호환) + `GRAPH_REPORT.md` + HTML.
- 2차 표면: Obsidian markdown (사용자 소유), Neo4j (관계형 그래프 DB), MCP (API surface).
- 판정: **KG (induction) + markdown fan-out**. primitive 카드의 "지식 그래프 (induction)" 셀에 해당하되, **Obsidian 표면과 `--wiki` 모드로 markdown 쪽을 동시 점유**. 혼합 포지션.

**축 3 — Timing (언제 지식이 형성되는가)**

- compile-time: `/graphify <path>` 이산 실행 시점 추출 (비용 집중).
- + runtime 증분: `--watch` + `--update` + git hook 이 "code-only 재추출 LLM=0", "docs 변경 시만 서브에이전트 재dispatch" 분기로 **선택적 runtime**.
- query 시점: 그래프 읽기만, 새 지식 생성 없음 (query 답은 save-result 로 역피드될 수 있으나 선택).
- 판정: **offline precompute + online retrieval 2단** (primitive 카드의 "GraphRAG 계열 7종" 과 동일) **+ incremental runtime 보정**. LLM Wiki 의 순수 compile-time 과도 다름.

**공백 메움 여부 — 결정적 판정**:

primitive 카드가 지목한 공백은 **"curation + KG 조합"** (사람이 raw 선별, LLM 이 그래프 자동 추출). Graphify 는 이 공백에 **들어가지 않음**:

- 사용자 curation 은 `raw/` 폴더에 뭘 넣을지 수준에 머물고, 그래프 추출 과정 전체가 induction.
- 즉 Graphify 는 **"induction + KG + offline-precompute"** 로 기존 GraphRAG 7종과 **같은 자리**.
- 차이점은 **(a) 하네스 통합 표면 다양성, (b) confidence tiering 강제, (c) markdown fan-out (`--wiki`, Obsidian), (d) 하네스-교차 skill 패키징** 이지 축 좌표가 아님.

**그럼 한국 커뮤니티 "보완재" 포지셔닝은 뭔가**: LLM Wiki(`curation + markdown + compile-time`) 위에 **Graphify 를 얹는 것**은 두 시스템이 **다른 축에 있기 때문에 레이어링 가능**. Wiki 는 사용자 선별 markdown, Graphify 는 그 markdown(+raw) 에 induction 으로 그래프 레이어. 즉 "공백 메움" 이 아니라 **"축 2를 markdown 과 KG 로 동시 점유하는 하이브리드 사용 패턴"** 이 LLM Wiki + Graphify 스택의 실체. 검증: upstream README 의 *"built around Karpathy's /raw folder workflow"* 가 이 하이브리드 의도를 공식 self-description 으로 확인.

**결론**: curation+KG 공백은 여전히 열려 있음 (Graphify 가 채우지 않음). 그러나 **markdown ↔ KG 사이의 사용자 포팅 브릿지** 로서 Graphify 는 primitive 카드가 예측하지 못한 "축 2 다중 점유" 패턴의 1번째 실제 사례. primitive 카드 업데이트 트리거 — `구성 요소 3. 축들의 상관 끊기` 섹션의 *"induction + markdown + compile-time"* 예측을 Graphify 가 `--wiki`/Obsidian 으로 **직접 실증**.

---

## Lint / Refinement 연산 유무 — `knowledge-lifecycle-operations` 2번째 사례 판정

primitive 카드는 `Cognee improve ≈ LLM Wiki Lint` 를 1번째 관찰로 확보하고 **2번째 사례 대기 중**. Graphify 확인:

**있음 — 단 형태가 다름**:

- `--update` 의 `graph_diff(G_old, G_new)` 분석 — 추가된 노드/엣지를 리포트 (skill Step 4 verbatim: *"diff['summary']... New nodes: ..."*).
- `save-result` 역피드로 Q&A 가 노드화 → 다음 `--update` 에서 추출되어 그래프에 병합.
- `--cluster-only` 는 엣지 변경 없이 커뮤니티만 재계산.
- god_nodes / surprising_connections 자동 재계산.

**없음**:

- Cognee `improve` 나 LLM Wiki Lint 와 달리 **stale claim / contradiction / orphan 탐지 연산이 명시적으로 없음**. SKILL.md 어디에도 "drift" , "stale", "contradiction detection" 문자열 없음 (Grep 결과 — 확인됨).
- confidence 가 `EXTRACTED → AMBIGUOUS` 로 **강등**되는 연산도 없음. 한 번 EXTRACTED 된 엣지는 재추출 전까지 신뢰도 유지.

**판정**: **부분 사례**. Graphify 는 **재계산/병합** (`update`, `cluster-only`, `save-result`) 은 1급 시민이지만, **품질 감사** (lint, contradiction, staleness) 는 미구현. `knowledge-lifecycle-operations` 카드의 2번째 사례로 **약하게 카운트** — Cognee/LLM Wiki 의 "lint" 와 Graphify 의 "diff + re-merge" 는 같은 운영 차원의 다른 primitive.

카드 업데이트 제안: `knowledge-lifecycle-operations` 의 1개 개념 "Lint/Refinement" 를 2개로 분리 — **(1) 품질 감사 (Cognee improve / LLM Wiki Lint)**, **(2) 증분 병합/diff (Graphify update)**. 둘 다 "축 밖 운영 프리미티브" 지만 서로 다른 연산.

---

## LLM Wiki 와의 비교 — 한국 커뮤니티 "보완재" 포지셔닝 검증

`notes/techniques/karpathy-llm-wiki.md` "커뮤니티 수용 — 한국어권" 섹션의 주장: *"Graphify 가 Obsidian 파일·링크 구조를 지식 그래프로 변환해 키워드 검색이 아닌 '관계/맥락 탐색'을 추가"*, 둘은 **"경쟁 관계가 아니라 레이어드 스택"**.

**실제 설계 증거**:

| 비교 축 | LLM Wiki | Graphify | 판정 |
|---|---|---|---|
| 빌더 | 사용자 curation + LLM builder (raw 선별은 사람) | Tree-sitter + LLM 서브에이전트 induction | 다름 — 레이어링 가능 |
| 스토리지 | markdown only | graph.json (주) + markdown fan-out (부, `--wiki`/Obsidian) | **공통분모가 markdown** — 레이어링 가능 |
| 타이밍 | compile-time 순수 | compile-time + incremental runtime | Graphify 가 runtime 보정 추가 |
| 엔티티/관계 | `[[wiki-link]]` 수동, 개념 페이지 수동 작성 | `extract()` 자동 엣지, 25 언어 AST | 보완적 — 수동 링크를 자동 그래프로 증강 |
| 검색 primitive | `index.md` 직독 | BFS/DFS 그래프 traversal + community | 한국 커뮤니티 주장 정확 — 텍스트→관계 탐색 보완 |
| staleness 대응 | Lint workflow (명시) | 없음 (Graphify 약점) | Wiki 가 메워주는 방향 |

**검증 결과**: 한국 커뮤니티의 "보완재" 포지셔닝은 **설계 근거상 맞음**. 특히 **Graphify 의 `--wiki` 모드가 community 당 article 1개 + index.md 를 생성** 해 LLM Wiki 포맷과 **구조적으로 호환** 되도록 설계된 것이 결정적 증거. upstream 의 Karpathy /raw 워크플로 명시적 참조와 일치.

단 **역방향 보완**도 관찰: Graphify 가 없는 것 = staleness/lint. LLM Wiki 가 이 약점을 메움 (Lint Workflow). 즉 **양방향 보완** — stack 의 각 레이어가 상대의 약점을 덮는 구조.

---

## 에코시스템 — 31.4k stars 검증 + Karpathy 타임라인 + Penpax

**31.4k stars 재검증**:

- GitHub 레포 페이지 직접 스냅샷 (2026-04-21 fetch): **31.4k stars / 3.5k forks** — inbox probe 수치와 동일, 확인됨.
- star-history.com snapshot 은 weekly 누적 리더보드만 보여주고 (2026-04-13~19 주간 +1.1k 성장, 주간 리더보드 11위) 일자별 누적 곡선은 이 단일 fetch 로 얻지 못함. 일자별 검증은 **(공식 범위 외 — 미답)**.
- 해석: 17일 만의 31.4k 는 **GitHub 일간 trending 장기 노출 × Karpathy 맥락 바이럴** 조합. 리더보드에 여전히 weekly +1.1k 로 성장 중.

**Karpathy 트윗 타임라인**:

- **Karpathy 원 트윗**: `x.com/karpathy/status/2039805659525644595` — *"LLM Knowledge Bases"*. 검색 결과 **2026-04-02** 게시 (WebSearch 확인, 본문 일부 verbatim: *"Something I'm finding very useful recently: using LLMs to build personal knowledge bases for various topics of research interest"*). 트윗 직접 접근은 status 402 로 차단, 날짜는 2차 검색 경유.
- **Graphify 첫 릴리스**: PyPI v0.1.1, **2026-04-04** (inbox probe 확인, PyPI 스냅샷 재확인).
- **시간차**: 트윗 후 **~48시간**. 바이럴 트윗들(socialwithaayan, itsoliviasco)이 *"48 hours after Karpathy posted his LLM Knowledge Bases workflow, this showed up on GitHub"* 라는 문구로 서사화 — **날짜 산술상 정합**. "이미 작업 중이었는데 타이밍이 맞은 것" 인지 "트윗 보고 급조한 것" 인지는 **(공식 범위 외 — 미답)**.

**Penpax 엔터프라이즈 레이어**:

- README verbatim: *"Penpax is the enterprise layer on top of graphify"* — 브라우저 히스토리, 미팅, 이메일, 파일, 코드를 **단일 on-device knowledge graph 로 continuously 동기화**, free trial 예정.
- 구조: Graphify(MIT, 오픈) + Penpax(상용, enterprise) **이원 구조**.
- OpenClaw 와의 대조: OpenClaw 는 "OpenAI/GitHub/NVIDIA/Vercel 등 industry-sponsor 모델 + MIT 단일 codebase" 로 상용화 없이 펀딩. Graphify 는 **dual-license/dual-product 전략** — 오픈소스 skill 은 커뮤니티 획득(31.4k stars), 엔터프라이즈는 on-device PKM 풀스택. 둘 다 2026-04 시점 정립 중인 **infra-tier 상용화 모델의 2가지 분기**로 기록 가치.

---

## 실용 체크리스트 — 도입 시 결정 포인트

- [ ] 코퍼스 규모 확인: `total_files > 200` 또는 `total_words > 2M` 이면 subfolder 선택 필수 (skill 이 자동 경고)
- [ ] 코드-only vs 혼합 판단: 코드만이면 `--update` 시 LLM 비용 0, 혼합이면 서브에이전트 청크 dispatch 비용 발생 → cost.json 모니터링
- [ ] 하네스별 skill 동기화: 버전 업그레이드는 `pip install --upgrade graphifyy && graphify install --platform <name>` — 하네스마다 SKILL.md 재배치 확인
- [ ] 출력 표면 선택: 사람 탐색=HTML/Obsidian, LLM 소비=json/MCP, 공유=SVG/Neo4j. 동시 활성화 가능하나 storage 중복 유의
- [ ] `--watch` 가 agentic loop 과 충돌하지 않는지: agent wave 중간 debounce 3s 로 충분한지, 아니면 git-hook 만 쓸지
- [ ] confidence_score 기본값 0.5 사용 금지 규칙을 팀/에이전트가 준수하는지 — Honesty Rules 감사 필요
- [ ] LLM Wiki 와 병행 운영 시: `--wiki` 모드를 Wiki 의 `wiki/` 디렉터리와 분리된 `graphify-out/wiki/` 에 둘지, Wiki 에 직접 merge 할지 결정 (후자는 index.md 충돌 위험)
- [ ] Penpax 전환 필요성: 개인 dev corpus 면 Graphify 로 충분, 브라우저/이메일/미팅 통합 PKM 필요 시 Penpax 검토

---

## 연결

- `insights/primitive-knowledge-layer-design-space.md` — 3축 프레임 적용. Graphify 는 **induction + KG + offline-precompute** 로 서베이 7종과 동일 좌표. "curation+KG 공백" 은 **여전히 열림**. 단 축 2 (storage) 를 graph+markdown 으로 **동시 점유**하는 하이브리드 첫 실증 사례 — 카드의 "축 상관 끊기" 예측을 `--wiki` 모드가 직접 실현. **카드 업데이트 트리거**.
- `notes/techniques/karpathy-llm-wiki.md` — "커뮤니티 수용 — 한국어권" 섹션의 Graphify=보완재 포지셔닝 **검증됨** (upstream 이 Karpathy /raw 워크플로 명시적 참조 + `--wiki` 모드 포맷 호환). 단 LLM Wiki 의 Lint workflow 가 Graphify 에 없다는 **역방향 보완** 도 추가 기록 필요.
- `notes/harness/kilo-code.md` — 대조군: Kilo Code 는 자체 VS Code extension + CLI + JetBrains 3-surface, 각 surface 가 shared engine. Graphify 는 **하네스 11종 위에 단일 skill 얹기**. "substrate 을 만드는가 vs 기존 substrate 위에 붙는가" 축에서 정반대.
- `notes/agents/hermes.md` — 대조군: Hermes 는 자체 agent loop + 자체 skill 카탈로그 (agentskills.io 표준 호환). Graphify 는 agent loop 없음, **Hermes 에도 "손님" 으로 들어감** (Hermes README 지원 목록에 포함). **skill 소비자와 skill 제공자의 비대칭**.
- `notes/infra/openclaw.md` — 대조군: OpenClaw 는 "gateway — 세션/채널/툴/이벤트의 단일 control plane" 으로 harness 들을 호스팅. Graphify 는 harness 들 안에 **스킬로 삽입**. 상용화 모델 대조: OpenClaw=industry-sponsor MIT 단독, Graphify=MIT 오픈 + Penpax 엔터프라이즈 **dual-product**.
- `knowledge-lifecycle-operations` (후보 카드) — 2번째 사례로 **부분 카운트**. Graphify 의 `update/graph_diff/save-result` 는 "증분 병합" primitive 로 Cognee `improve` / LLM Wiki Lint 의 "품질 감사" 와 **다른 차원**. 카드 내부에서 2개 하위 primitive 로 분기 제안.
- 후보 신규 primitive 카드: **`edge-epistemic-tagging`** (3-tier confidence 를 엣지 level 에서 강제하는 설계) — 현재 Graphify 1번째 사례. 2번째 관찰 대기.
- 후보 신규 tier: **`cross-cutting-skill`** / **`skill-engine`** — 현재 Graphify 1번째 사례. 2번째 관찰 대기 시 `meta/harness_schema.md` 정식 승격.

---

## Sources

- [safishamsi/graphify (GitHub repo)](https://github.com/safishamsi/graphify) — 2026-04-21 fetch, 31.4k stars / 3.5k forks 확인
- [graphifyy (PyPI)](https://pypi.org/project/graphifyy/) — 2026-04-21 fetch, v0.1.1 (2026-04-04) → v0.4.23 (2026-04-18), maintainer `captainturbo`
- `~/.claude/skills/graphify/SKILL.md` — v0.4.23, 1245줄 primary source (로컬 설치본)
- [Karpathy — LLM Knowledge Bases tweet](https://x.com/karpathy/status/2039805659525644595) — 2026-04-02, 직접 접근 402, 날짜/텍스트는 WebSearch 경유 확인
- [Muhammad Ayan on X — "48 hours after Karpathy" viral tweet](https://x.com/socialwithaayan/status/2041192946369007924) — 48시간 서사 진원
- [Mehul Gupta — Andrej Karparthy's LLM Wiki Codes: Graphify (Medium)](https://medium.com/data-science-in-your-pocket/andrej-karparthys-llm-wiki-codes-graphify-b73bec5d87ea) — dual-pass (AST + AI) 및 confidence 3-tier 외부 재확인
- [Analytics Vidhya — From Karpathy's LLM Wiki to Graphify](https://www.analyticsvidhya.com/blog/2026/04/graphify-guide/) — 릴리스 내러티브
- [Connected Data on X — Graphify 3-layer framing](https://x.com/Connected_Data/status/2041827996806340736) — Karpathy raw→wiki 확장 포지셔닝
- [star-history.com — safishamsi/graphify snapshot](https://star-history.com/#safishamsi/graphify&Date) — 2026-04-13–19 weekly +1.1k 확인, 일자별 곡선 미조회
- `inbox/2026-04-21-graphify-upstream.md` — 2026-04-21 upstream 식별 probe (로컬 레퍼런스)
- `insights/primitive-knowledge-layer-design-space.md` — 3축 프레임 원 카드 (로컬 레퍼런스)
- `notes/techniques/karpathy-llm-wiki.md` — LLM Wiki deep-dive (로컬 레퍼런스)
