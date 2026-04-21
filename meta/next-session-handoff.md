---
date_recorded: 2026-04-20
author_session: Trend harness expansion + tier system + two infra-layer fixes
phase: Phase 1 확장기 — corpus 가 harness 한 계층에서 tier 4종 구조로 확장됨
---

# 다음 세션 이어서 하기 — 핸드오프 메모

## 이번 세션(2026-04-19~04-20) 진행 완료

### A. 코퍼스 확장 (7개 신규 딥다이브)
1. **OMX + OMC bundle** (`notes/harness/omx-omc.md`, 719줄 + correction block) — Yeachan-Heo 자매 하네스
2. **OMO** (`notes/harness/omo.md`, 777줄) — code-yeongyu, OMC/OMX 의 어휘 상당수 원류. 후속으로 OMX/OMC 노트에 5개 corrections 패치
3. **Cline v3.58** (`notes/harness/cline-v3-58.md`, 305줄) — IDE 확장 계열, ACP 어댑터
4. **openwork** (`notes/harness/openwork.md`, 306줄) — OpenCode 기반 팀 GUI, out-of-loop productization
5. **Kilo Code** (`notes/harness/kilo-code.md`, 315줄) — Cline→Roo Code→Kilo fork chain consolidator, 서버사이드 auto-model 라우팅
6. **Hermes** (`notes/agents/hermes.md`, 368줄) — **첫 agent-framework tier**. Nous Research, 101k★, self-improving loop
7. **OpenClaw** (`notes/infra/openclaw.md`, 286줄) — **첫 infra/gateway tier**. 360k★, 산업 스폰서 다수

### B. 시스템 수정 2건 (구조적 버그 수정)
1. **codex 호출 규약** (commit `7a8f1d6`) — `.claude/agents/harness-analyzer.md` + `project-analyzer.md` 에서 `codex:rescue` dispatch 경로 제거. sub-agent 컨텍스트가 `/codex:status`·`/codex:cancel` 미접근이라 hang 관찰·취소 불가였던 문제. 메인 세션 codex 는 정상 사용 유지.
2. **analyzer Mode A/B 이중화** (commit `edffb26`) — sub-agent 런타임이 Agent 도구를 주지 않는 환경에서 analyzer 가 "읽기 금지" 규정과 충돌해 deadlock 하던 문제 (OpenClaw deep-dive 1차 시도에서 52+ min hang 발생 후 진단). Mode A: Agent 가용 → harness-probe dispatch. Mode B: 불가 → coordinator 가 WebFetch + Bash(curl --max-time 30) 로 직접 읽기. **2회 실패 시 unreachable 마킹**, 재시도 루프 금지.

### C. 폴더 구조 신설
```
notes/
├── harness/      14개 (기존 9 + 신규 5)
├── agents/       1개  (Hermes)    ← 비어있던 폴더 활성화
├── infra/        1개  (OpenClaw)  ← 신규 폴더
├── techniques/   11개
└── llm/          0개  (여전히 비어있음)
```
**제안자**: 사용자 ("openclaw/hermes 조사 가치? 폴더 구분 필요할 듯"). "platforms" 명명 기각, **`infra/`** 로 합의.

### D. 스키마 진전 (`meta/harness_schema.md`)
- **META-tier 축 → confirmed** (4 tier 모두 populated)
- **신규 후보 축**:
  - Δ5 headless-mode-as-first-class-output-contract (Cline — 1st case)
  - T out-of-loop productization (openwork → Kilo, 2nd case 도달 → **promotion threshold 충족**)
  - U server-routed filesystem mutation policy (openwork)
  - V declarative mode bundles (Kilo)
  - W server-routed auto-model tiers (Kilo)
  - gateway-event-surface (OpenClaw, infra-tier 전용)
  - side-channel-for-notifications (clawhip 패턴)
- **Δ1 refined** — 5-subtype 분류 (hand-reinvention / single-home+inbound / core+adapter / product-wrapper / consolidator-fork)
- **Δ2 refined** — 6가지 게이팅 전략 스펙트럼 정리
- **Δ3 불변** — 여전히 2nd case 대기 (OMC 만 유일)
- **REFUTED** (corpus-level): DD-gossip (Hermes 주장 primary source 부재), ACP-contract (Hermes + OpenClaw 모두 README 미언급)

### E. 메모리 업데이트
- `feedback_codex_invocation_protocol.md` v1 → v2 (framing 교정: "codex 전체 비사용" → "sub-agent 내부만 구조적 금지")
- 저장 위치: `C:\Users\kys90\.claude\projects\D--ClaudeCode-Projects-Bundle-Researcher-uuuSanAI-AISystemResearcher\memory\`

## 현재 corpus 상태 (2026-04-20 기준)
- **Deep-dive notes**: 14 harness + 1 agent-framework + 1 infra + 11 techniques = **27 건**
- **Digests**: 1건 (2026-04-17 Anthropic sweep)
- **Insight cards**: 5건 (primitive-*.md)
- **Schema candidate axes**: Δ1~Δ5 + T, U, V, W + gateway-event-surface + side-channel = 10개 (+ META-tier confirmed)
- **Folder tiers**: 4종 (harness / agents / infra / techniques) + 1 유휴 (llm)

## 다음 세션 진입점 — 의사결정 분기

### 분기 1: 코퍼스 폭 확장 (tier 채우기)
- **agents tier** 두 번째 후보: Devin 2.0 / Manus / Agno Framework — Hermes 와의 대비군 형성
- **infra tier** 두 번째 후보: AgentMail / Anthropic Claude Cowork (공식 사이트) / 기타 gateway
  - gateway-event-surface 축 promotion threshold(2번째 케이스) 달성을 위한 직접 탐색
- **llm tier** 첫 entry: 후보 불명확 (Karpathy 글은 techniques 로 분류됐음)

### 분기 2: 코퍼스 깊이 (기존 항목 후속 probe)
- **OpenClaw Gateway 프로토콜 RPC spec** (`docs.openclaw.ai/reference/rpc`) — 이벤트 타입 enumeration. 최우선 open question.
- **Hermes gossip/ACP 재확인** — developer-guide/architecture 깊은 페이지 probe. 만약 primary source 에서 정말 없다면 SEO 글들이 완전 오정보였음을 확정.
- **OMO Hashline 벤치마크** (Grok Code Fast 1: 6.7% → 68.3% 주장) — 재현성 확인
- **Kilo `kilo run --auto` stdout JSON 스키마** — Δ5 promotion 판정 대기
- **Graphify upstream 식별 + `techniques/graphify.md` deep-dive** — 2026-04-21 Brain Trinity YouTube 영상(`cNlvrU-KcRg`) 경유 발견. 사용자 로컬 스킬 `graphify-windows` (`~/.claude/skills/graphify/SKILL.md`) 존재하나 primary source upstream 불명. Karpathy LLM Wiki 와 짝인 knowledge-layer tooling — 그래프 navigation vs index.md navigation 두 노선 비교 가능. upstream(레포·저자) 식별이 선행 조건이라 1–2 probe 로 먼저 사전조사 후 deep-dive 진입 판단. 영상 관찰 결과는 `notes/techniques/karpathy-llm-wiki.md` "커뮤니티 수용 — 한국어권" 섹션에 이미 anchor.

### 2026-04-21 추가 세션 (knowledge-layer synthesis + deep-dive 2건)

- **서베이 2건 저장**: `inbox/2026-04-21-graph-rag-survey.md` (7종 graph RAG), `inbox/2026-04-21-memory-pkm-survey.md` (7종 memory/PKM). 14 프레임워크 primary docs 스캔 수준.
- **Graphify upstream 식별 완료**: `inbox/2026-04-21-graphify-upstream.md`. upstream = `github.com/safishamsi/graphify` (MIT, PyPI `graphifyy` v0.4.23, 2026-04-04 첫 릴리스). 사용자 로컬 `-windows` 는 upstream 의 `--platform windows` 설치 표식, fork 아님. Phase 1 external research 대상 확정.
- **신규 insight 카드**: `insights/primitive-knowledge-layer-design-space.md` — builder/storage/timing 3축 프레임. **2026-04-21 deep-dive 2건 반영 후 갱신**: confidence medium→medium-high, 축 4 후보(감사 가능성) 등재, Lint 3분지 확정, 축 2 재해석(primary+secondary 벡터), cross-harness skill tier 후보.
- **Deep-dive 완료 2건**:
  - `notes/techniques/basic-memory.md` (~260줄) — 3축: `co-authored + markdown+hybrid(SQLite FTS5 + FastEmbed) + runtime`. LLM Wiki 와 storage 1축만 일치 → "가장 가까운 형제" 가설 재정의. Lint = structural only (`schema_infer/validate/diff` + `doctor`). 미답: 충돌 해소 정책.
  - `notes/techniques/graphify.md` (~?줄) — 3축: `induction + KG+6표면 fan-out + compile-time`. **curation+KG 공백 안 메움** → 공백 재확증. 축 4 후보 확보: `EXTRACTED(1.0)/INFERRED(0.4–0.9)/AMBIGUOUS(0.1–0.3)` 의무 confidence + *"Never invent an edge"* honesty rule. 10+ 하네스 동시 지원 → cross-harness skill tier 후보 1사례. PyPI v0.1.1 2026-04-04 (Karpathy 트윗 2026-04-02 → 48h 정합), 17일 만에 31.4k stars (재검증됨, 일자별 곡선은 미답).
- **재수집 필요** (상태 유지): Anthropic Claude Memory 공식 페이지 (404 리다이렉트), ChatGPT Memory FAQ (403), Cognition Devin's Wiki 세부. 상업 메모리 3종 source thin 상태.
- **Deep-dive 다음 후보 우선순위 (업데이트)**:
  1. ~~Basic Memory~~ → **완료**
  2. ~~Graphify~~ → **완료** (원래 handoff 에선 대기 항목이었으나 이번 세션에 실행)
  3. **Cognee** — `remember/recall/forget/improve` 4-op API. `improve` 실제 구현이 semantic lint 2번째 확정 사례가 될지 판정.
  4. **Letta (MemFS 중심)** — "git-tracked memory" 가 markdown 쪽 수렴 신호인지 확인.
  5. **Zep/Graphiti** — temporal invalidation (bi-temporal KG) 이 본 지형 단독 축.
- **공백 영역 실험 후보 (상태 유지)**: curation+KG 조합은 Graphify deep-dive 로 **메우지 못함을 확증**. 이 프로젝트 자체 `notes/` 위에 Graphify 를 실제로 돌려보는 건 여전히 유효한 self-test (Graphify 는 induction 이라 이 프로젝트 corpus 에 돌리면 자동 추출 그래프가 생성됨. curation 된 `notes/` 를 입력으로 induction 하는 경우, 출력이 curated source 에 대한 2차 induction 인 특이 케이스).
- **후속 카드 후보 (상세화)**: `knowledge-lifecycle-operations` — 3 하위 차원(structural / semantic / incremental-update) × 3 운영(lint / consolidation / forgetting) = 9-cell 매트릭스. 각 cell 별 1+ 사례 확보됨 (primitive 카드의 "관련 primitive 카드" 섹션 참조). Carve-out 시점: cell 별 2+ 사례. Cognee deep-dive 가 트리거 가능성 높음.
- **Tier 체계 변경 후보**: `skills/` 또는 `cross-cutting/` 신규 tier. Graphify 1사례. `meta/harness_schema.md` META-tier 축에 기록. 2번째 사례 대기.

### 분기 3: 횡단 분석 (digest / insight)
- **"Personal assistant gateways" 축 digest**: OpenClaw (single-user) vs openwork (team) vs Claude Cowork (상업 team) 비교
- **"Self-improving agents" 축 digest**: Hermes (skill-generation) vs Ouroboros (spec-edit) vs Compound Engineering vs AutoAgent
- **META-tier 축 공식화** — 각 tier 의 애플리커블 축 행렬 작성
- **Phase 2 진입 — graft-evaluator** — 2026-04-17 handoff 의 원래 계획이 여전히 유효. gamemaker 프로젝트 × 기존 5 primitive insight 카드 평가 가능.

### 분기 4: 시스템 개선 후속
- `.claude/agents/harness-analyzer.md` 에 Mode B 추가된 후 실전 검증 1회 완료 (이번 OpenClaw main-session 경로) — 추후 sub-agent 호출 시 Mode B 실제 발동 모니터링 필요
- analyzer 의 `axes_added_local` vs 글로벌 `candidate_axis_promotion` 동기화 프로세스 미정립 — 스키마가 커질수록 필요해짐

## 재진입 시 빠른 오리엔테이션 순서
1. 이 파일 읽기
2. `meta/harness_schema.md` 끝부분 "Candidate additions" 훑기 (현재 후보 축 10개 상태 확인)
3. `notes/infra/openclaw.md` TL;DR 읽기 — infra tier 가 왜 load-bearing 인지 한 번에 파악
4. `notes/agents/hermes.md` 의 "✅ Main-session verification" 블록 읽기 — agent-framework tier 의 첫 사례
5. 위 분기 1~4 중 어느 쪽으로 갈지 사용자에게 질의

## 권고 — 다음 세션 첫 추천
**분기 1의 infra tier 2번째 entry** (AgentMail 또는 Anthropic Claude Cowork) — gateway-event-surface 축 promotion 확보를 우선 처리. 그 후 분기 3의 "personal assistant gateways" digest 쓰면 corpus 에 tier-cross-cutting 통찰이 쌓임.

대안: 분기 4의 Phase 2 graft-evaluator 로 아예 Phase 2 개시. 단, corpus 확장이 아직 진행 중이라 디저트보다 메인을 먼저 마무리하는 게 자연스러움.

---

## 이전 미처리 사항 (2026-04-17 handoff 에서 승계)
- Anthropic Engineering 블로그 **미커버 포스트 5편** (Claude Code auto mode / infrastructure noise eval / the think tool / Beyond permission prompts / Advanced tool use on Developer Platform) — 제품·보안 맥락. 필요 시 증분 스윕.
- Insight 카드 5개 상호 cross-link 보강 (반쪽 상태)
- Anthropic 블로그 신규 포스트 증분 모니터링 (자동화 미설정)
