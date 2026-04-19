---
title: Karpathy's LLM Wiki — compile-time knowledge base pattern
date: 2026-04-19
source_url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
source_type: gist
topic: techniques
tags: [karpathy, knowledge-base, rag-alternative, memory, markdown, wiki, obsidian, agent-skills, mcp]
status: processed
---

## 요약 (3줄 이내)

Andrej Karpathy가 2026-04 공개한 "LLM Wiki" 패턴은 raw 문서를 질의 시점마다 재검색하는 RAG와 달리, LLM을 **빌더**로 써서 원본을 미리 상호연결된 markdown 엔티티/개념 페이지로 **컴파일**해두는 방식이다. X 16M+ 뷰·gist 5,000+ 스타를 받아 1주일 내 Agent Skills·MCP·세션로그 인제스트형 오픈소스 구현체 7+ 개가 등장했다. 한계는 분명히 **개인/팀 스케일 (~100 소스, ~수백 페이지)**에 묶여 있으며, 그 이상에서는 index.md 네비게이션이 붕괴해 RAG 하이브리드가 필요하다.

---

## 핵심 포인트

1. **패러다임 전환**: *query-time retrieval → compile-time integration*. RAG는 매 질문마다 raw 청크를 끌어오는 stateless 리트리버지만, LLM Wiki는 LLM이 ingest 시점에 "summarize + cross-reference + contradiction flag"를 수행하는 stateful builder다.
2. **3-레이어 구조**: `raw/` (불변 원본), `wiki/` (LLM이 쓰는 엔티티/개념/소스/쿼리 페이지), `CLAUDE.md` 또는 `AGENTS.md` 스키마 파일. 스키마는 "새 세션마다 LLM이 처음 읽어 연속성을 재확립하는 장치"로 설계됨.
3. **3대 연산**: **Ingest** (원본 → 요약 + 관련 엔티티/개념 페이지 갱신 + index/log 업데이트), **Query** (index 읽고 → 관련 페이지 읽고 → 인용과 함께 합성 → 원하면 `wiki/queries/`에 보존), **Lint** (orphan/contradiction/stale claim/missing concept 점검).
4. **한 건 Ingest = 페이지 8–15개 터치**: 원본 하나가 엔티티 여러 개, 개념 여러 개, synthesis, index를 동시에 갱신하는 "multi-page write" 연산. 이게 "compounding artifact"를 만드는 메커니즘.
5. **Index-first 네비게이션**: `index.md`에 모든 페이지가 카테고리별 테이블로 정리되어, 임베딩 검색 없이도 LLM이 "어떤 페이지를 읽을지"를 index 하나로 판단. ~100 소스·수백 페이지까지는 embedding-free로 작동.
6. **Append-only 로그**: `log.md`에 `## [YYYY-MM-DD] operation | title` 포맷으로 모든 ingest/query/lint를 기록. Unix 도구로 파싱 가능. 감사·롤백·stale 추적에 사용.
7. **스케일 브레이크포인트 ~50k–100k 토큰**: 작은 코퍼스(개인 연구 ~100편)에서는 전체 wiki가 컨텍스트에 들어가 95% 토큰 절감 가능하나, 그 이상에서는 index 자체가 컨텍스트를 초과해 실패.
8. **Staleness는 수동 + 주기적 health-check**: RAG의 자동 재인덱스와 달리 Lint 프롬프트로만 노후화 탐지. "automatic propagation 없음"이 핵심 운영 부채.
9. **오픈소스 에코시스템 3갈래**: ① Agent Skills 포장형 (Astro-Han), ② 웹 UI + MCP 서버형 (lucasastorian), ③ Claude Code/Codex/Cursor **세션 로그 자체를 소스로 먹는** 형태 (Pratiyush). 1주일 만에 등장.
10. **하이브리드가 실전 답**: production RAG 경험자들은 "session-level wiki (on-demand 생성·폐기) + persistent user wiki (세션 병합 후 누적)" 2단 구조로 벡터 검색을 네비게이션 레이어로 돌리는 방식을 제안.

---

## Karpathy의 원본 구조 (gist 기반)

### 디렉토리 레이아웃

```
your-wiki/
├── CLAUDE.md          # 스키마 — LLM이 매 세션 처음 읽음
├── raw/               # 불변 원본 (LLM은 읽기만, 쓰지 않음)
│   ├── articles/
│   ├── papers/
│   └── assets/
└── wiki/              # LLM이 유지보수하는 컴파일 산출물
    ├── index.md       # 카탈로그 (엔티티/개념/소스/쿼리 테이블)
    ├── log.md         # append-only 연산 기록
    ├── overview/      # synthesis — 전체 thesis
    ├── entities/      # 사람·모델·조직
    ├── concepts/      # 아이디어·기법
    ├── sources/       # 원본별 요약 (1 원본 = 1 페이지)
    └── queries/       # 보존된 질의 답변
```

### 페이지 프론트매터 스키마

```yaml
---
title: Page Title
type: entity | concept | source | query | overview
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [list of raw source filenames]
tags: [relevant tags]
---
```

### 필수 컨벤션

- **최소 2개 이상의 내부 링크**: 모든 페이지는 최소 2개의 다른 wiki 페이지를 `[[wiki-link]]` 문법으로 참조 (Obsidian 호환).
- **모든 주장에 인용**: `(Source Name, YYYY)` 포맷으로 원본을 명시.
- **모순 플래그**: `> **CONTRADICTION**` 콜아웃 블록으로 표시 — 덮어쓰지 않고 양 소스를 모두 인용.
- **열린 질문 플래그**: `> **OPEN QUESTION**` 콜아웃.

### CLAUDE.md 스키마 섹션 (최소 구성)

1. Purpose — 한 문단 미션 문장
2. Directory Layout — 각 디렉토리 역할
3. Conventions — 네이밍, 링크 문법, 프론트매터, 모순 처리
4. Ingest Workflow — 단계별 처리 절차
5. Query Workflow — 답변 생성·보존 방식
6. Lint Workflow — 문제 탐지·복구 절차

> "The schema is what creates continuity. Every session starts with the LLM reading it, which means every session the LLM knows exactly what directories exist, what format to use, what workflows to follow, and what conventions to maintain."

### Ingest Workflow (표준 8단계)

1. Raw 소스 파일 읽기
2. 사용자에게 강조점·프레이밍 확인 질문
3. `wiki/sources/<name>-summary.md` 생성
4. 관련 엔티티·개념 페이지 전부 갱신
5. 변화가 thesis를 바꿀 경우 `wiki/overview/synthesis.md` 갱신
6. `wiki/index.md` 갱신 (새 페이지 추가, 소스 카운트 조정)
7. `wiki/log.md`에 엔트리 append
8. 사용자에게 "생성/갱신된 페이지 몇 개, 총 터치 N개" 보고

**관측 스케일**: 원본 1건당 평균 **wiki 페이지 10–15개 터치**.

### Query Workflow

1. `index.md` 읽어 관련 페이지 식별
2. 해당 페이지들 읽기
3. wiki 페이지 인용과 함께 합성 답변 생성
4. "답변을 `wiki/queries/`에 보존할지" 사용자에게 확인

> "Good answers should not disappear into chat history. They should get filed as new wiki pages."

### Lint Workflow

- **Orphan pages**: 인바운드 링크 없음 → 삭제 또는 링크 추가
- **Superseded claims**: 이후 소스가 정정한 내용 → 출처 표기와 함께 수정
- **Missing concept pages**: N개 페이지에서 언급되나 전용 페이지 없음
- **Research gaps**: 특정 주제에 대해 특정 날짜 이후 소스 없음

발견 시 **제안만 보고하고 사용자 승인 후 수정 적용**.

### Log 포맷

```
## [YYYY-MM-DD] operation | title
- action details
- pages touched: N
```

---

## 저자의 프레임워크 / 명시적 주장

### 핵심 철학

- **Immutability separation**: raw는 불변 — "The LLM reads from it but never writes to it."
- **User as curator**: "You don't write the wiki. The LLM does. Your job is to curate sources, ask good questions, and think about what it all means."
- **Persistence over retrieval**: RAG는 "nothing accumulates"지만 wiki는 "compounds with every source you add."
- **Intentionally abstract**: 이 패턴은 도메인 의존적이므로 스키마는 일부러 추상적으로 설계됨.

### 사용 예시 (gist에서 열거)

개인 지식 관리(goals/health/psychology), 연구 딥다이브, 책 챕터 정리, 팀 wiki(Slack/트랜스크립트 피드), 경쟁 분석, 여행 계획, 강의 노트.

---

## RAG와의 정량·정성 비교

| 축 | LLM Wiki | RAG |
|---|---|---|
| 지식 조립 시점 | compile-time (ingest 시) | query-time (매 질의) |
| LLM 역할 | builder + maintainer | retriever |
| 상태 | stateful (누적) | stateless |
| 인프라 | 파일시스템 + markdown | 벡터스토어 + 임베딩 파이프라인 |
| 네비게이션 | `index.md` 직독 | 임베딩 유사도 |
| 최적 스케일 | ~50k–100k 토큰 / ~100 소스 / 수백 페이지 | 대규모 다중도메인 |
| 작은 스케일 토큰 효율 | **naive loading 대비 최대 95% 절감** | 상대적으로 비쌈 |
| 스케일 확장성 | index 붕괴로 실패 | 더 효율적으로 확장 |
| Staleness 대응 | 수동 + 주기적 Lint | 파이프라인 재인덱스 (near-real-time 가능) |
| 접근 제어 | 없음 | 기본 제공 |
| 실패 모드 | context overflow, stale, orphan, access 없음 | poor chunking, embedding drift, ungoverned data |

### Nasternak의 Heidegger 워크스루 수치 (실측)

- **Wiki 방식**: 4 턴 걸쳐 합성 토큰 ~2,600, 청크 19개 처리(3개 중복제거)
- **동등한 stateless RAG**: 합성 토큰 ~16,000, 청크 ~32개 필요
- **Follow-up 질의**: wiki가 이미 커버한 범위 내에서는 retrieval·construction 비용 0 — 합성 토큰만 소모

### 스케일 브레이크 — Nasternak의 증언

> "The pattern breaks before the wiki gets large enough to be useful at enterprise scale."

붕괴 지점: **~100 소스, ~수백 페이지**에서 index.md가 관리 불능 상태. Ingest 결정 자체가 index 탐색 비용에 질식됨.

### 하이브리드 제안 (Nasternak)

1. **Session-level wiki** — 검색 결과로 on-demand 빌드, 세션 간 리셋
2. **Persistent user wiki** — 세션 후 병합, 사용자 간 유지
3. 벡터 검색을 index.md가 아닌 **네비게이션 레이어**로 사용

> "RAG is not dead. And we know more and more how to keep it alive."

### 비용 아키텍처 레슨

> "A smaller, cheaper model handles [wiki construction] reliably...drop a model tier, or run the same model faster and cheaper."

Wiki 빌드는 Opus 급 필요 없음 — Haiku / 소형 모델로 충분. 합성·질의만 고성능.

### 평가가능성 (evaluability)

> "The session wiki is structured markdown. A domain expert can read the wiki...immediately assess whether the right concepts were retrieved."

→ RAG 디버깅이 임베딩 스페이스 블랙박스인 반면, Wiki는 markdown 인간 가독 — 도메인 전문가가 직접 품질 판정 가능.

---

## 오픈소스 구현체 스냅샷 (2026-04-19 기준)

### ① Astro-Han/karpathy-llm-wiki — Agent Skills 포장

- **포지션**: Claude Code / Cursor / Codex / OpenCode용 재사용 가능 Skill
- **구조**: `raw/`, `wiki/` (topic 하위 포함), `assets/`, `examples/`, `references/`
- **설치**: `npx add-skill Astro-Han/karpathy-llm-wiki` (Claude Code/Cursor), Codex는 `.agents/skills/`에 복사
- **특징**: 프롬프트 템플릿 + 형식화된 `SKILL.md` 사양 포함. 실제 13개 토픽 · 94개 wiki 아티클 운영 중인 레포 기반 "production-ready" 패키징
- **성숙도**: 494 ★ / 61 forks / MIT

### ② lucasastorian/llmwiki — 웹 UI + MCP 서버

- **포지션**: 문서 업로드 → Claude.ai가 MCP로 접속해 wiki 편집
- **스택**: Next.js + FastAPI + Supabase(Postgres) + MCP 서버 + LibreOffice 변환 컨테이너
- **MCP 도구 5종**: `guide`, `search`, `read`, `write`, `delete`
- **특징**: TUS 프로토콜 업로드, office→PDF 변환, OCR, S3 호환 저장, Supabase OAuth로 Claude.ai 커스텀 커넥터 연동
- **차별점**: Karpathy의 개념 레이어를 **웹 프로덕트 인프라**로 물성화 — PDF 뷰어, 멀티문서 랭킹 검색, 실시간 MCP 통합

### ③ Pratiyush/llm-wiki — 세션 로그 인제스트

- **포지션**: Claude Code / Codex CLI / Copilot / Cursor / Gemini CLI / Obsidian 세션 트랜스크립트를 wiki로
- **레이어**: `raw/sessions/<project>/` (.jsonl → markdown 불변), `wiki/` (sources/entities/concepts/syntheses/comparisons/index/MEMORY), `site/` (정적 HTML + `.txt`/`.json`/JSON-LD AI 사이블링 익스포트)
- **자동화**: SessionStart 훅으로 Claude Code 실행 시 자동 동기화, 파일 워처(debounce), OS 스케줄러(launchd/systemd/Task Scheduler), `/wiki-sync` → `/wiki-build` 자동 연결
- **MCP 도구 12종** — 에이전트 질의용
- **사용**: `./setup.sh` → `./build.sh && ./serve.sh`

### 공통 분화 축

- **입력 소스**: 파일 업로드형 (lucasastorian) vs 세션 트랜스크립트형 (Pratiyush) vs raw 디렉토리 직접 편집형 (Astro-Han, 원본)
- **통합 지점**: Skill (Astro-Han) vs MCP 서버 (lucasastorian, Pratiyush) vs CLI 프롬프트 (원본)
- **출력 표면**: markdown 파일만 (원본/Astro-Han) vs 정적 HTML 사이트 (Pratiyush) vs 전용 웹 UI (lucasastorian)

---

## 실용 체크리스트 (gist 기반)

**Ingest 품질 체크**
- [ ] 생성된 소스 요약이 원본 핵심 주장을 왜곡 없이 담는가
- [ ] 기존 엔티티 페이지에서 해당 소스를 언급하게 링크가 추가됐는가
- [ ] 신규 엔티티/개념이 최소 2개 페이지에서 참조되는가 (orphan 방지)
- [ ] 기존 주장과 충돌 시 `> **CONTRADICTION**` 콜아웃이 걸렸는가
- [ ] index.md와 log.md가 동시 갱신됐는가

**Lint 체크포인트**
- [ ] Orphan 페이지 목록
- [ ] 충돌 상태로 남은 쌍
- [ ] N개 이상 페이지에서 언급되지만 전용 페이지 없는 개념
- [ ] 특정 토픽의 최신 소스 유입 중단 기간 (research gap)

**스케일 경고 사인**
- index.md가 컨텍스트 윈도우의 상당 비율을 차지하기 시작 → 서브 index 분할 or RAG 하이브리드 검토
- Ingest 1회가 20+ 페이지 터치 → 개념 분해가 과도, consolidation 필요
- Lint가 매번 같은 orphan을 반복 보고 → 스키마의 링크 최소치 규칙 재정비

---

## 원문에서 인용할 가치가 있는 구절

> "With LLMs, knowledge is created and maintained continuously and consistently rather than being able to use individual queries to create knowledge."
> — Karpathy (Analytics Vidhya가 gist에서 인용)

> "The schema is what creates continuity. Every session starts with the LLM reading it."
> — Karpathy gist (스키마 파일의 존재 이유)

> "You don't write the wiki. The LLM does. Your job is to curate sources, ask good questions, and think about what it all means."
> — Karpathy gist (인간 역할 분업)

> "Good answers should not disappear into chat history. They should get filed as new wiki pages."
> — Karpathy gist (Query의 보존 원칙)

> "The synthesis on Thursday reflects everything you read on Tuesday, plus everything since."
> — Aaron Fulkerson 재정리 (compounding artifact의 핵심 문장)

> "The pattern breaks before the wiki gets large enough to be useful at enterprise scale."
> — Michał Nasternak (실전 스케일 한계)

> "RAG is not dead. And we know more and more how to keep it alive."
> — Michał Nasternak (하이브리드 결론)

---

## 왜 중요한가 / 어디에 써먹을 수 있나

- **개인 리서치 체계화**: ~100편 규모 논문·블로그·트랜스크립트 코퍼스를 embedding 인프라 없이 markdown만으로 운영 가능. 이 리포지토리 본인이 이미 `notes/`, `digests/`, `insights/` 구조로 유사 패턴을 부분 실천.
- **에이전트 세션 기록의 자산화**: Pratiyush형 접근은 Claude Code 세션 JSONL을 "구조화된 개념 그래프"로 변환 — 개발 활동 자체를 wiki로 축적하는 새 축.
- **RAG 대안이 아닌 RAG 전처리**: Nasternak 하이브리드는 "wiki는 session-scope synthesis 레이어, RAG는 coverage 레이어"로 역할 분담. 대규모 엔터프라이즈라도 wiki 요소를 도입 가능.
- **평가가능성**: wiki는 인간이 읽을 수 있는 markdown이므로 도메인 전문가가 품질 직접 판정 가능 — RAG 블랙박스 대비 결정적 장점.
- **저비용 모델로 충분**: wiki 빌드 자체는 Haiku/소형 모델급이면 됨. 고성능은 Query 단계만.

---

## 연결

- **관련 노트**:
  - `notes/techniques/anthropic-effective-context-engineering.md` — "structured note-taking" (NOTES.md) 패턴은 wiki의 축약판
  - `notes/techniques/anthropic-effective-harnesses-long-running-agents.md` — compaction/sub-agent와 wiki는 "컨텍스트 한계 대응 3각"
  - `notes/harness/superpowers.md`, `notes/harness/openspec.md` 등 — SKILL 기반 하네스 계열과 Astro-Han 구현의 연결점
- **후속 조사 필요**:
  - Karpathy gist 원문 직접 획득 (현재는 2차 인용 기반 재구성) — 최종 본문/업데이트 이력 확인
  - Astro-Han 레포의 실제 `SKILL.md` / 프롬프트 템플릿 덤프 — harness-analyzer 수준 딥다이브 가치 있음
  - lucasastorian MCP 도구 5종의 스키마 — `write` 도구가 어떤 구조화를 강제하는지
  - "index.md가 몇 페이지에서 붕괴하는가"의 재현 실험 — Nasternak "~100 소스 / 수백 페이지" 수치 검증
  - Obsidian + Claude 로컬 조합의 구체 워크플로 (anthemcreation 게시물 등)

## Sources

- [Karpathy's original gist — gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Nandigam Harikrishna — Full Breakdown (substack)](https://nandigamharikrishna.substack.com/p/andrej-karpathys-llm-wiki-full-breakdown)
- [Aaron Fulkerson — Karpathy's Pattern in Production](https://aaronfulkerson.com/2026/04/12/karpathys-pattern-for-an-llm-wiki-in-production/)
- [Atlan — LLM Wiki vs RAG](https://atlan.com/know/llm-wiki-vs-rag-knowledge-base/)
- [Michał Nasternak — LLM Wiki at Scale (Medium)](https://michalnasternak.medium.com/the-llm-wiki-at-scale-from-personal-research-tool-to-production-rag-247710a1284c)
- [Analytics Vidhya — LLM Wiki Revolution](https://www.analyticsvidhya.com/blog/2026/04/llm-wiki-by-andrej-karpathy/)
- [Astro-Han/karpathy-llm-wiki (GitHub)](https://github.com/Astro-Han/karpathy-llm-wiki)
- [lucasastorian/llmwiki (GitHub)](https://github.com/lucasastorian/llmwiki)
- [Pratiyush/llm-wiki (GitHub)](https://github.com/Pratiyush/llm-wiki)
- [SimpleNews — Open-source wave summary](https://www.simplenews.ai/news/karpathys-llm-wiki-pattern-sparks-wave-of-open-source-knowledge-base-tools-3hel)
- [rohitg00/...v2 gist — extended with agentmemory lessons](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2)
