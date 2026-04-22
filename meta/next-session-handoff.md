---
date_recorded: 2026-04-22 (Claude Design / gpt-image-2 design-layer twin launches)
author_session: 디자인-레이어 양대 랩 쌍둥이 런칭 — Claude Design (04-17) + gpt-image-2/"Duct Tape" (04-21) 딥다이브 각 1건 + 비교 digest 1건 + `primitive-format-native-curation` carve-out. Knowledge-layer 플로우 일시 중단, 제품-레이어 최신 동향 흡수. Phase 2 graft 대기 상태 유지.
phase: Phase 1 확장기 — 제품-레이어 coverage 확장. Knowledge-layer 후속 (Mem0/Zep/Graphiti) 은 다음 세션으로 이월.
---

# 다음 세션 이어서 하기 — 핸드오프 메모

## 2026-04-22 세션 — 디자인 레이어 쌍둥이 런칭

**작성물 (4건, 총 1,740+줄)**:
1. `notes/harness/claude-design.md` (429줄 → SKILL.md probe 추가로 +~30줄) — Anthropic Labs Claude Design 딥다이브. Opus 4.7 substrate, tar+README handoff bundle, `frontend-design` 스킬 productization, Krieger 사임(04-14)→런칭(04-17) 타이밍.
2. `notes/harness/gpt-image-2.md` (480줄) — OpenAI gpt-image-2 / "Duct Tape" 딥다이브. Instant/Thinking 2-mode split, Arena +242 대 Nano Banana 2, fal.ai + Azure Foundry day-0 GA, architecture 비공개.
3. `digests/2026-04-22-design-layer-twin-launches.md` (262줄) — 양 런칭 구조적 비교. 레이어 다름 (product-vertical vs foundation-horizontal), 텍스트 렌더링 moat collapse, "thinking before drawing" 새 contract, handoff surface 가 실질 경쟁축.
4. `insights/primitive-format-native-curation.md` (신규 카드) — 커뮤니티 큐레이션이 "프롬프트 문자열 → 포맷-네이티브 primitive 번들" 로 시프트. confidence: medium (독립 사례 1.5건). Primitive surface 풍부한 제품에서만 발생하는 조건부 패턴.

**핵심 발견**:
- **Claude Design handoff bundle = prompt-handoff glue** (tar + README + chat transcript). Figma 의 JSON-manifest 와 철학적 정반대 — Claude Code 가 "재현".
- **`frontend-design` SKILL.md 구조적 역설**: 스킬이 homogenization 을 *명시적으로* 금지하지만 (anti-pattern 블록 + "NEVER converge on Space Grotesk"), 실제 Claude Design 출력은 여전히 "container soup" 수렴. **Prompt-level 지시 < training-data 기본값**. Anthropic 이 model-level 로 해결해야 할 문제일 가능성.
- **텍스트 렌더링 moat 18개월 collapse**: Ideogram (전문) → Recraft #1 (AR 아키텍처) → gpt-image-2 99%+CJK. 단일 축 전문 벤더 moat 이 foundation capability 점프 1회에 흡수된 드문 사례.
- **한국어 early-signal 채널 등재**: choi.openai / @aisocity / qjc.ai (Threads). 영어권 tech press 대비 평균 12~48h 빠름. sources.md Candidates 섹션에 3건 등록.

**스키마 진전**:
- 신규 축 후보 **"curation-primitive-surface-richness"** (`primitive-format-native-curation.md`) — 2 사례 (Claude Code vs gpt-image-2). 3번째 promotion 시 검증.
- Δ1 subtype 후보 **"skill-productization"** (`frontend-design` → Claude Design). 2번째 사례 대기.
- **"user-visible vs vendor-hidden mode split"** 신규 축 후보 — OpenAI Instant/Thinking + Anthropic extended thinking. 2 사례 확보, 3번째 (Google Gemini toggle?) 대기.
- **"Arena-as-prelaunch-stealth-QA"** 신규 축 후보 — gpt-image-2 "Duct Tape" + Anthropic Opus anonymous 시기 + Google Nano Banana prelaunch. 3 사례 *추정* (primary evidence 각각 확인 필요).

**sources.md 갱신**:
- Active 4건 추가: Claude Design (announcement + Help Center), gpt-image-2 (API docs + blog), Anthropic News 계열, 각 deep-dive 레퍼런스.
- Candidates 9건 추가: Simon Willison (promote 후보), fal.ai, Victor Dibia newsletter, Sam Henri Gold blog, Neuron Daily, choi.openai / @aisocity / qjc.ai (Threads), rohitg00/awesome-claude-design + ZeroLu/awesome-gpt-image.

**미처리 / 다음 세션 후보**:
- **Mem0 deep-dive** (2026-04-21 recommend 이월) — knowledge-layer 4분지 매트릭스 안정화의 잔존 분기 2개 동시 후보. 여전히 최상위.
- **`frontend-design` cookbook 깊이 파기** — `anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb` 미확보. longer-form 가이드의 실제 내용이 SKILL.md 의 역설 (homogenization 금지 vs 관찰된 수렴) 을 해결하는 구체 recipe 를 제공하는지 확인 필요. 0.5 round probe 로 가능.
- **Arena-as-prelaunch-stealth-QA 3번째 사례 검증** — 각 사례의 primary evidence 1개씩 확보 후 carve-out. 0.5~1 round probe.
- **Figma 의 Claude Design 대응 제품 공개** 시기 모니터링 — "design tool 카테고리가 LLM 의 thin UI 로 붕괴" 가설의 falsifier.

---

## 이전 세션 기록 (2026-04-21 오후 — 아래는 아카이브)



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

## 현재 corpus 상태 (2026-04-21 오후 기준)
- **Deep-dive notes**: 14 harness + 1 agent-framework + 1 infra + **12 techniques** = **28 건** (Letta 추가)
- **Digests**: 1건 (2026-04-17 Anthropic sweep)
- **Insight cards**: **6건** (primitive-*.md 5건 + `knowledge-lifecycle-operations.md` 신규 carve-out)
- **Schema candidate axes**: Δ1~Δ5 + T, U, V, W + gateway-event-surface + side-channel + audit-trail-vs-epistemic-confidence sub-axis 후보 = 11개 (+ META-tier confirmed)
- **Folder tiers**: 4종 (harness / agents / infra / techniques) + 1 유휴 (llm)
- **Knowledge-layer 매트릭스 안정도**: 4분지 중 2분지 (structural lint, consolidation+feedback) 임계 충족, 1분지 약한 2 (incremental update), 1분지 1 (semantic lint). primitive 카드 confidence: medium-high → **high**.

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

### 2026-04-21 추가 세션 ②(오후) — Letta deep-dive + 카드 carve-out

- **Letta deep-dive 완료** (`notes/techniques/letta.md`, 690줄): 4번째 knowledge-layer deep-dive. harness-analyzer Mode B 직접 fallback 으로 진행 (6 fetch round 모두 성공). **5개 검증 질문 결론**:
  - **Q1 markdown 수렴 2번째 사례 → 확정**: MemFS = 진짜 git 레포 (`~/.letta/agents/<id>/memory`) + `.md` + frontmatter (description 필수, Anthropic SKILL.md 패턴). server `memory(...)` 도구를 **대체** (Letta Code 한정).
  - **Q2 consolidation+feedback 2번째 사례 → 부분 확정**: 11+ self-editing 도구 (`core_memory_*`, `memory_*`, `archival_memory_*`, `memory_apply_patch` codex-style diff, `conversation_search`, `open/grep/semantic_search_files`). 두 종류 sleep-time 명확 구분 — server-side `enable_sleeptime` (multi-agent group) vs client-side `reflection` subagent (Letta Code, git worktree 비동기). Cognee `improve` 와 다른 위상 (단일 시스템 4-stage vs actor 분리 + git commit).
  - **Q3 축 4 (감사 가능성) → 반증**: confidence/honesty rule 부재. git commit 은 약한 audit trail 이지만 Graphify edge confidence 와 다른 layer. 축 4 = **여전히 Graphify 단일 사례** + sub-axis 분리 후보 등장 (audit-trail vs epistemic confidence).
  - **Q4 structural lint 2번째 사례 → 확정 (보너스)**: `/doctor` = `context_doctor` skill (changelog 0.19.8), *"Identify and repair degradation in system prompt, external memory, and skills"* — Basic Memory `doctor` 와 어휘 1:1 일치. 4-step 절차 (identify → plan → commit → recompile).
  - **Q5 세션→영속 bridging 2번째 사례 → 부분 확정**: Cognee 2-tier (cache→graph) vs Letta 4-tier (live→summary→archival→blocks/MemFS). 추상 패턴 공유, 위상 다름. 축 3 timing 의 *"hybrid bridging"* sub-value 정당화.
  - **두 가지 Letta 좌표 동시 점유**: server `(self-editing, hybrid 4-tier blocks/files/archival/RAG, runtime + 4-tier descending)` + Letta Code MemFS `(self-editing, markdown primary + git secondary, runtime + git commit)`.
  - **메인 세션 codex 위임 후보 3건** (비-차단): alembic migration 자동 vs 명시 정책 / MemFS git push 실패 fallback (`memoryGit.ts`) / reflection git worktree 격리 메커니즘.
- **신규 카드 carve-out** (`insights/knowledge-lifecycle-operations.md`, 325줄): 두 분지 (structural lint + consolidation+feedback) 동시 임계 도달이 carve-out 트리거. **4분지 매트릭스 안정화**:
  - structural lint: Basic Memory `doctor` + Letta `/doctor` (2 사례 → 임계 충족)
  - semantic lint: LLM Wiki `Lint Workflow` (1 사례, Cognee `improve` 는 src 동사 분석으로 반증)
  - incremental update: Graphify `--update` (1 강한 + Basic Memory `sync --watch` 약한 2)
  - consolidation+feedback: Cognee `improve` + Letta `reflection` (2 사례, 다른 위상)
  - **분지 판정 결정 트리**: src 의 동사 (apply/consolidate/create/persist vs detect/validate/flag vs verify/repair vs update/rebuild) 가 결정적 신호. docs 의 마케팅 어휘는 신뢰 불가 (Cognee `improve` 가 결정적 사례).
  - **Forgetting** 은 carve-out 카드 외부 별도 차원 (소멸 vs 유지).
  - **직교성 주장** = 중간 confidence (5 데이터포인트, (storage, lint 분지) 약한 상관 관찰).
- **primitive-knowledge-layer-design-space.md 갱신** (293 → 301줄): confidence medium-high → **high**. 데이터포인트 17 → 18. 핵심 변경:
  - **(builder, storage) 평면의 첫 수렴 cluster 등재**: Basic Memory + Letta MemFS + LLM Wiki = (builder 다른) markdown primary 좌표 3 데이터포인트. SKILL.md 패턴 차용으로 frontmatter 어휘까지 정렬되는 2차 수렴 (Anthropic Agent Skills 가 attractor).
  - **운영 프리미티브 분리 섹션 carve-out**: 본문은 짧은 reference 로 축소, detail 은 신규 카드 참조.
  - **축 4 후보 4-layer 구분 갱신**: epistemic / provenance / schema validation / **change history (Letta git commit 이 등재시킨 신규 layer)**. sub-axis 분리 후보 (audit-trail vs epistemic confidence) 등재.
  - **잠재 신규 카드 후보 3건 등재**: `forget-strategies` / `oss-dual-product-economics` (Letta+Letta Cloud 가 3사례 도달) / `audit-trail-vs-epistemic-confidence`.
- **sources.md 갱신**: Letta 항목 신규 등록 (Apache-2.0, server v0.16.7 + Letta Code v0.22.4, MemFS 0.15.0 도입, carve-out 트리거 도달 마커).

- **서베이 2건 저장**: `inbox/2026-04-21-graph-rag-survey.md` (7종 graph RAG), `inbox/2026-04-21-memory-pkm-survey.md` (7종 memory/PKM). 14 프레임워크 primary docs 스캔 수준.
- **Graphify upstream 식별 완료**: `inbox/2026-04-21-graphify-upstream.md`. upstream = `github.com/safishamsi/graphify` (MIT, PyPI `graphifyy` v0.4.23, 2026-04-04 첫 릴리스). 사용자 로컬 `-windows` 는 upstream 의 `--platform windows` 설치 표식, fork 아님. Phase 1 external research 대상 확정.
- **신규 insight 카드**: `insights/primitive-knowledge-layer-design-space.md` — builder/storage/timing 3축 프레임. **2026-04-21 deep-dive 2건 반영 후 갱신**: confidence medium→medium-high, 축 4 후보(감사 가능성) 등재, Lint 3분지 확정, 축 2 재해석(primary+secondary 벡터), cross-harness skill tier 후보.
- **Deep-dive 완료 2건**:
  - `notes/techniques/basic-memory.md` (~260줄) — 3축: `co-authored + markdown+hybrid(SQLite FTS5 + FastEmbed) + runtime`. LLM Wiki 와 storage 1축만 일치 → "가장 가까운 형제" 가설 재정의. Lint = structural only (`schema_infer/validate/diff` + `doctor`). 미답: 충돌 해소 정책.
  - `notes/techniques/graphify.md` (~?줄) — 3축: `induction + KG+6표면 fan-out + compile-time`. **curation+KG 공백 안 메움** → 공백 재확증. 축 4 후보 확보: `EXTRACTED(1.0)/INFERRED(0.4–0.9)/AMBIGUOUS(0.1–0.3)` 의무 confidence + *"Never invent an edge"* honesty rule. 10+ 하네스 동시 지원 → cross-harness skill tier 후보 1사례. PyPI v0.1.1 2026-04-04 (Karpathy 트윗 2026-04-02 → 48h 정합), 17일 만에 31.4k stars (재검증됨, 일자별 곡선은 미답).
- **재수집 필요** (상태 유지): Anthropic Claude Memory 공식 페이지 (404 리다이렉트), ChatGPT Memory FAQ (403), Cognition Devin's Wiki 세부. 상업 메모리 3종 source thin 상태.
- **Deep-dive 다음 후보 우선순위 (업데이트)**:
  1. ~~Basic Memory~~ → **완료**
  2. ~~Graphify~~ → **완료**
  3. ~~Cognee~~ → **완료 (2026-04-21)**. 두 가설 반증: semantic lint 2번째 사례 **미성립** (`memify_pipelines/` 5파일 전부 additive 동사), 축 4 2번째 사례 **미성립** (provenance ≠ confidence). 대신 **새 4번째 분지 "Consolidation + feedback refinement"** 등장.
  4. **Letta (MemFS 중심)** — "git-tracked memory" + self-editing 피드백이 (a) 축 2 markdown 수렴 2번째 사례, (b) consolidation+feedback 4번째 분지 2번째 사례 후보. **이중 트리거** 가능성으로 다음 우선순위 최상.
  5. **Zep/Graphiti** — temporal invalidation 이 본 지형 단독 축. semantic lint 2번째 사례 후보이나 "시간축 invalidation ≠ orphan 탐지" 라 조건부.
  6. **Mem0 또는 Hermes** — 축 4 후보 정찰 (Hermes self-improving loop 에 confidence 가 있는지).
- **공백 영역 실험 후보 (상태 유지)**: curation+KG 조합은 Graphify deep-dive 로 **메우지 못함을 확증**.
- **후속 카드 후보 상태**: `knowledge-lifecycle-operations` 카드 **carve-out 여전히 보류**. Cognee deep-dive 로 semantic lint 2번째 사례 트리거가 **무산**됐기 때문. 현재 매트릭스 4분지 × 각 1 사례:
  - structural lint: Basic Memory (1)
  - semantic lint: LLM Wiki (1, 2번째 대기)
  - incremental update: Graphify (1, Basic Memory sync 약한 2번째)
  - consolidation+feedback: Cognee (1, 새 분지)
  - 카드 작성 트리거: 어느 한 cell 이 2+ 도달. Letta deep-dive 가 다음 유력 트리거.
- **Tier 체계 변경 후보**: `skills/` 또는 `cross-cutting/` 신규 tier. Graphify 1사례. `meta/harness_schema.md` META-tier 축에 기록. 2번째 사례 대기.
- **새로 관찰된 패턴 (후속 카드 후보 2)**: **OSS + 상용 튜너/클라우드 dual-product** — Graphify + Penpax, Cognee + Dreamify. 2사례 확보. 추가 사례(예: Zep OSS + Zep Cloud 등) 확인되면 별도 primitive 카드 후보. 현재는 primitive 카드에 흡수.

### 분기 3: 횡단 분석 (digest / insight)
- **"Personal assistant gateways" 축 digest**: OpenClaw (single-user) vs openwork (team) vs Claude Cowork (상업 team) 비교
- **"Self-improving agents" 축 digest**: Hermes (skill-generation) vs Ouroboros (spec-edit) vs Compound Engineering vs AutoAgent
- **META-tier 축 공식화** — 각 tier 의 애플리커블 축 행렬 작성
- **Phase 2 진입 — graft-evaluator** — 2026-04-17 handoff 의 원래 계획이 여전히 유효. gamemaker 프로젝트 × 기존 5 primitive insight 카드 평가 가능.

### 분기 4: 시스템 개선 후속
- `.claude/agents/harness-analyzer.md` 에 Mode B 추가된 후 실전 검증 1회 완료 (이번 OpenClaw main-session 경로) — 추후 sub-agent 호출 시 Mode B 실제 발동 모니터링 필요
- analyzer 의 `axes_added_local` vs 글로벌 `candidate_axis_promotion` 동기화 프로세스 미정립 — 스키마가 커질수록 필요해짐

## 재진입 시 빠른 오리엔테이션 순서 (2026-04-21 오후 갱신)
1. 이 파일 읽기 — 특히 "2026-04-21 추가 세션 ②(오후)" 블록 (위)
2. `insights/primitive-knowledge-layer-design-space.md` TL;DR + "Letta deep-dive" 단락 + "축 4 후보" 섹션 (3축 + 수렴 cluster + sub-axis 분리 후보)
3. `insights/knowledge-lifecycle-operations.md` 전체 — **신규 carve-out 카드, 4분지 매트릭스 + 분지 판정 결정 트리 + actor 위상 spectrum**
4. `notes/techniques/letta.md` 의 "5개 검증 질문 결론 표" 섹션 — 두 좌표 점유 + carve-out 트리거 발화 핵심
5. 아래 다음 세션 추천 읽고 방향 선택

## 권고 — 다음 세션 첫 추천 (2026-04-21 오후 갱신)

**최상위: Mem0 deep-dive** (`notes/techniques/mem0.md` 신규). 4분지 매트릭스의 잔존 1사례 분지 두 개(semantic lint, incremental update) 동시 후보. Mem0 가 가장 가능성 높은 이유:
- *semantic lint 2번째 사례 후보*: Mem0 의 `arbitration` 로직 (last-write-wins) 이 detection 단계를 거치는지 확인 — 거친다면 detect/validate/flag 동사 발견으로 semantic lint 분지 임계 충족.
- *forget 차원 강한 사례*: TTL 기반 자동 감쇠가 Cognee/Letta 와 다른 메커니즘이라 forget-strategies 카드 carve-out 후보 데이터.
- *induction + 벡터 + runtime 좌표의 가장 직접적 사례*: 서베이만 한 마지막 큰 미커버 좌표. 본 카드의 "induction+벡터+runtime 으로 뭉친 관성" 주장의 결정적 증거 또는 반례.
- 이중 트리거 가능성: semantic lint 임계 도달 시 4분지 중 3분지가 임계 충족 → matrix 안정도 medium-high → high 로 강화.

**대안 A**: Zep/Graphiti deep-dive — temporal invalidation 이 semantic lint 2번째 사례로 성립하는지 판정. Mem0 보다 조건부 ("시간축 invalidation ≠ orphan 탐지" 갈림길) 이지만 temporal KG 단일 사례라 카드 다양성 측면에서 가치. incremental update 강한 사례 가능성도 있음 (bi-temporal 인덱스 갱신 비용 통제).

**대안 B**: Hermes deep-dive 보강 — `self-improving loop` 의 confidence 스코어링 (축 4 epistemic 2번째 사례 후보) + skill-generation 이 consolidation+feedback 3번째 사례인지. 축 4 promotion 의 가장 가까운 후보. 단 Hermes 노트가 이미 일부 작성됐으므로 follow-up probe 형태가 적절.

**대안 C**: Phase 2 graft-evaluator 진입 — primitive 카드가 high confidence + 신규 카드 carve-out 완료 + 데이터포인트 18. 사용자 다른 프로젝트(gamemaker)에 graft 평가 시작 가능. 단 semantic lint 잔존 1 사례 + 축 4 단일 사례 문제가 해소 안 됐으므로 카드가 완전 안정화 상태는 아님. Mem0 한 번 더 돌리고 Phase 2 가는 게 자연스러움 — 그러나 *"카드 완결 perfectionism"* 함정 경계 (Phase 2 에서 graft 평가가 카드의 한계를 더 잘 드러낼 수도).

**대안 D**: 다른 후보 카드 carve-out — `forget-strategies` (5 메커니즘 × 5 시스템 매트릭스 채우기, 데이터 부분 확보) 또는 `oss-dual-product-economics` (Graphify+Penpax, Cognee+Dreamify, Letta+Letta Cloud 3사례 도달, carve-out 가능). 현재 carve-out 모멘텀 활용 의의는 있지만, primitive 카드 안정화 우선이라 우선순위 낮음.

**대안 E**: 기존 "infra tier 2번째 entry" (AgentMail 또는 Claude Cowork) 재개 — 2026-04-20 원래 handoff 의 1순위 권고. knowledge-layer 흐름을 잠시 끊고 gateway-event-surface 축 promotion 으로 환승. corpus 의 폭 확보 관점에선 여전히 유효, knowledge-layer 모멘텀 활용 가치 vs corpus 다양성 trade-off.

---

## 이전 미처리 사항 (2026-04-17 handoff 에서 승계)
- Anthropic Engineering 블로그 **미커버 포스트 5편** (Claude Code auto mode / infrastructure noise eval / the think tool / Beyond permission prompts / Advanced tool use on Developer Platform) — 제품·보안 맥락. 필요 시 증분 스윕.
- Insight 카드 5개 상호 cross-link 보강 (반쪽 상태)
- Anthropic 블로그 신규 포스트 증분 모니터링 (자동화 미설정)
