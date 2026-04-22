---
title: Claude Design ↔ gpt-image-2 — 같은 주 양대 랩 디자인-레이어 쌍둥이 런칭 비교
date: 2026-04-22
type: digest
sources_deep_dive:
  - claude-design
  - gpt-image-2
sources_supporting:
  - inbox landscape sweep (2026-04-22)
  - anthropic-harness-design-long-running-apps (기존 corpus)
status: draft
---

## TL;DR (5줄)

1. **같은 주 (2026-04-17 / 04-21) 양대 랩의 디자인-레이어 동시 베팅**이지만 **레이어가 다르다**: Anthropic = **product layer 수직 통합** (Claude Design + Opus 4.7 + Claude Code handoff), OpenAI = **model layer 수평 파운데이션** (gpt-image-2 + API + partners fal/Azure). 같은 주에 의도적으로 부딪혔지만 **같은 축에서 경쟁하지 않는다**.
2. **텍스트 렌더링 moat 가 18개월 만에 붕괴**: Ideogram (전문 벤더) → Recraft v3 (AR 아키텍처로 #1) → **gpt-image-2 (99% + CJK)**. 단일 축 전문 벤더의 moat 이 foundation model 에 흡수된 드문 사례. 디자인 도구의 "typography" 품질은 이제 base model capability 에 종속.
3. **"Thinking before drawing" 이 새 architecture contract** — gpt-image-2 (Instant/Thinking 모드) + Nano Banana Pro (Gemini 3 Pro Thinking) 공통 구조. 순수 diffusion (Midjourney/Flux/SD) 에 reasoning front-end 없으면 category 에서 밀려남.
4. **"Prompt-to-production-code" 가 새 contested seam**: Claude Design 의 handoff bundle (tar + README — prompt-glue 타입) vs Figma Make (Figma 노드 기반) vs Lovable/Bolt (app 전체 빌드) vs v0 (component-scoped). **"design tool" 카테고리는 code-generating LLM 의 thin UI 로 붕괴 중** — 경쟁은 "AI 가 디자인 할 수 있는가" 가 아니라 **"handoff surface 는 누가 장악하는가"**.
5. **두 런칭 모두 정확한 architecture 공개 거부**: Anthropic 은 Claude Design 의 internal representation / `frontend-design` 스킬 스키마 / 토큰 소비 모델 비공개, OpenAI 는 Thinking 모드의 reasoning architecture 비공개. 벤더 side 가 구조를 숨기면서 UX 만 공개 — Phase 1 외부 리서치로 가능한 범위의 한계.

---

## A. 타임라인 & 런칭 정황

| 날짜 | 이벤트 | 의미 |
|---|---|---|
| 2026-04-04 | LM Arena 에 익명 `packingtape` / `maskingtape` / `gaffertape` 등장 | gpt-image-2 prelaunch stealth QA |
| 2026-04-04 | @aisocity Threads — 한국어권 최초 "gpt-image-2 leaked" 식별 | Arena 익명 → 한국 early-signal 채널 활성화 |
| 2026-04-14 | Mike Krieger (Anthropic CPO) Figma 이사회 사임 | Claude Design 런칭 3일 전 |
| 2026-04-14 | The Information — Anthropic 디자인 도구 계획 첫 보도 | leak 주도인지 coordinated 인지 미확인 |
| 2026-04-16 | **Claude Opus 4.7 출시** | Claude Design 의 substrate — 이미지 해상도 2576px / 3.75MP 지원 |
| 2026-04-17 | **Claude Design 런칭** | Pro/Max/Team 즉시, Enterprise 기본 OFF. FIG 주가 당일 −7.04% |
| 2026-04-21 | **gpt-image-2 공식 발표** (Altman livestream) | fal.ai + Azure Foundry 동일 day GA |
| 2026-04-22 | gpt-image-2 단계적 롤아웃 개시 | 본 digest 작성 시점 |

### 관찰

- **런칭 간격 4일**. 의도된 타이밍일 가능성 높음 — 각 랩은 상대 로드맵을 리크로 인지했을 것으로 추정.
- **Krieger 사임 타이밍**: Figma 보드에서 AI-관련 IP 방어 의무를 해제하고 바로 공격. **구조적 이해관계 충돌** 제거가 런칭 3일 전. Anthropic 측 공식 해명 없음.
- **양측 모두 livestream 으로 발표**하되 형식 차이: Anthropic = blog + demo 비디오, OpenAI = 6-researcher 라이브 데모 (Altman 호스트). OpenAI 가 **모델 수치 / 시연 중심**, Anthropic 이 **제품 워크플로 중심**이라는 평소 패턴 유지.

---

## B. 구조적 비교 매트릭스

| 축 | Claude Design | gpt-image-2 |
|---|---|---|
| **레이어** | Application (대화형 디자인 도구) | Foundation model (image-gen) |
| **진입점** | `claude.ai/design` (web 전용) | ChatGPT UI / Codex / API / fal / Azure |
| **기반 모델** | Claude Opus 4.7 (vision: 2576px/3.75MP) | gpt-image-2 자체 (architecture 비공개) |
| **주 산출물** | Prototypes, slides, one-pagers, marketing, dashboards | 이미지 (텍스트 렌더링 강점, 최대 2K + experimental 4K) |
| **상위 루프** | Claude Code handoff — tar + README + chat transcript | API → 외부 시스템이 소비 |
| **Architecture 공개도** | UI/인풋은 공개, 내부 표상 비공개 (HTML/JS 라는 관찰만 존재) | Thinking 메커니즘 **명시적 비공개** |
| **Architecture contract** | Skill productization (`frontend-design` → Claude Design) | User-visible mode split (Instant / Thinking) |
| **비용 모델** | 기존 플랜에 번들 — weekly usage burn 이슈 | per-image ($0.01~$0.41 레인지) |
| **접근 tier** | Pro / Max / Team (Enterprise opt-in) | Free (Instant) + Plus/Pro/Business (Thinking) + API tier 1~5 |
| **도발 대상** | Figma / Canva / Adobe Creative Suite | Midjourney / Ideogram / Nano Banana Pro / Imagen |
| **주가 반응 (런칭일)** | FIG −7.04% | 주가 영향 분산 — 직접 경쟁 상장사 적음 |
| **Watermarking/provenance** | 산출물이 HTML/JS — native C2PA 부재 | C2PA 상속 추정, SynthID 등가 invisible watermark 없음 |
| **한국어권 early signal** | choi.openai (Threads, 2025-10 skill 시기 이미 인지) | @aisocity (Threads, 2026-04-04 prelaunch) |

---

## C. 5가지 load-bearing 관찰

### C1. 같은 "디자인-레이어" 런칭이지만 **경쟁 안 함**

- Claude Design 은 산출물이 prototype/slide/dashboard — 이미지도 포함하지만 **구성 요소**로만.
- gpt-image-2 는 raw image generation — Claude Design 이 이 같은 카테고리 도달은 Opus 4.7 vision capability + `frontend-design` 스킬 한계 내.
- **상호 보완 가능성**: Claude Design 이 gpt-image-2 API 를 상위 레이어에서 호출하는 시나리오는 기술적으로 막는 장벽 없음. 실제로 Anthropic 이 OpenAI API 를 호출할지는 정치적 질문.
- 반대도 가능: OpenAI 가 Codex / ChatGPT 에 "Claude Design 같은 design-product" 레이어를 얹을 것으로 예상됨 — sam Altman 의 "full-stack image + app" 비전 관련 언급들이 힌트.

**→ 이 주의 런칭은 "정면 충돌" 이 아니라 "평행 레이어 점유". 진짜 충돌은 OpenAI 가 design-layer product 를 낼 때 시작.**

### C2. 텍스트 렌더링의 moat collapse — 시스템 컨텐트

- 18개월 전: Ideogram 이 "text-in-image" 전문 벤더로 $80M+ 자본 조달. 단일 축 기업.
- 12개월 전: Recraft v3 가 AR 아키텍처로 Artificial Analysis Arena #1 (2024-10) — **AR 아키텍처 자체가 text 에 유리하다**는 구조적 관찰 성립.
- 현재: gpt-image-2 가 99% + CJK 로 Arena +242 (=Non-Latin +316). Ideogram / Recraft 가 존속은 하지만 **차별화 축이 무력화**.

**함의**:
- 전문 벤더의 moat 은 foundation model capability 점프 1회에 흡수될 수 있음 — **vertical specialists 의 구조적 취약성**.
- 생존 경로: (a) vector 출력 (Recraft 계속), (b) open weights (Flux/SD), (c) aggregator UX (Krea).
- 새 차별화 축: (i) **typographic intent** (단순 정확도 너머의 font 선택/kerning/hierarchy), (ii) **instruction following on text semantics** (텍스트 뜻을 이해하는가), (iii) **adversarial conditions** (곡면 / 작은 글씨 / dense layout).

### C3. "Thinking before drawing" = 새로운 table-stakes

- OpenAI: **Instant vs Thinking** (user-visible toggle)
- Google: **Nano Banana Pro on Gemini 3 Pro Thinking**
- 공통 구조: 이미지 생성 이전에 reasoning + 웹 검색 + self-check 단계

**순수 diffusion 의 압박**:
- Midjourney v8.1 Alpha (2026-04-14 런칭) — reasoning front-end 없음. 예술적 퀄리티로 방어.
- FLUX 2 Pro — 없음. Open weights + production package 로 방어.
- Stable Diffusion — 없음. ComfyUI 생태계로 방어.

**Anthropic 의 위치**:
- Claude Design 은 **reasoning + rendering 을 외부화** (design 을 Opus 4.7 CoT 로 + artifact 를 HTML/JS 로). 이미지 생성이 아닌 design-product 이므로 이 축에서는 다른 게임.
- 하지만 Claude 가 이미지 생성을 직접 하게 되면 같은 Thinking architecture contract 로 들어와야 함.

### C4. "Handoff surface" 가 실질 경쟁축

**관찰**: AI 네이티브 디자인 도구들이 모두 **다른 handoff surface** 를 선택:

| 제품 | Handoff 형태 |
|---|---|
| Claude Design | tar + README + chat transcript → Claude Code |
| Figma Make | Figma 노드 그래프 + Supabase 연동 |
| Lovable | 배포된 웹 앱 (DB/auth 포함) |
| Bolt.new | WebContainer 샌드박스 전체 |
| v0 | React + Tailwind 컴포넌트 파일 |
| Magic Patterns | custom design-system-aware React |
| Framer AI | 네이티브 게시된 웹사이트 |

이것들은 모두 **같은 source (design intent)** 을 **다른 target (코드/앱/노드/배포물)** 으로 투사. 서로 배타적이지 않음 — 팀은 여러 개 동시 사용 가능.

**핵심 질문**: 어느 handoff surface 가 **실제로 production 에 merge 되는가**? 이것이 승자 예측의 결정 변수.

**Claude Design handoff 의 특이성**: *"match the visual output rather than transpile"* (Victor Dibia 관찰). 즉 **결정론적 export 가 아니라 확률론적 재현** — Claude Code 가 알아서 맞춤. 이는:
- 유연성: 어떤 기술 스택이든 대응
- 취약성: reproducibility 없음, design-system drift 누적 가능
- **Figma 의 JSON-manifest 기반 export 와 정반대 설계 철학**

### C5. Anthropic 이 product-vertical, OpenAI 가 foundation-horizontal — 로드맵 시그널

| 전략 | Anthropic 의 패턴 | OpenAI 의 패턴 |
|---|---|---|
| 제품 릴리스 | Claude Code → Claude Cowork → **Claude Design** — design-to-code 수직 확장 | Base model (GPT-4o → GPT-5 → gpt-image-2) — foundation 수평 확장 |
| Go-to-market | 기존 Pro/Max/Team 플랜 번들 | Free 티어 + API partners + paid 확장 |
| 개발자 접근 | Claude Code plugin 마켓 (`frontend-design` skill) | Direct API + fal / Azure Foundry |
| 엔터프라이즈 | Claude Design 기본 OFF, admin opt-in | Azure Foundry Standard Global 즉시 |
| 외부 노출 surface | **Product (Claude Code, Claude Cowork, Claude Design)** | **Model (gpt-image-2, GPT-5, o-series)** |

**함의**:
- Anthropic 은 **application layer 수직 통합**을 베팅 — design/code/office/meeting 각각에 Claude-labeled 제품.
- OpenAI 는 **foundation 수평 확장** + thin product (ChatGPT) — 제3자 벤더 생태계에 application layer 위임.
- 이 구조는 **Apple vs Microsoft 1990s** 또는 **Google vs Facebook 2010s** 의 반복으로 보임. 어느 쪽이 이기는지는 **user preference 의 진화** 에 달림 — 통합된 스위트 vs 개방형 생태계.

---

## D. 랜드스케이프 스윕의 추가 관찰

### D1. 한국어권 early-signal 채널 재확인

- **choi.openai** (Threads) — `frontend-design` 스킬을 2025-10 이미 다룸 + gpt-image-2 post-launch 에서 한국어 렌더링 99%+ / Nano Banana Pro 3축 압도 주장. **한국어권의 OpenAI 코리아 대표급 시그널 소스**로 확정.
- **@aisocity** (Threads) — 2026-04-04 prelaunch 식별. gpt-image-2 leak 의 한국어권 first mover.
- **qjc.ai** (Threads) — 8-point Nano Banana Pro displacement 분석. 구체 테스트 프롬프트 제공.

이 세 계정은 영어권 기술 언론 (VentureBeat/TechCrunch) 보다 **평균 12~48시간 빠름**. sources.md 등재 가치 있음.

### D2. `awesome-*` 가 prompt-pattern market 의 primitive

- [awesome-claude-design (rohitg00)](https://github.com/rohitg00/awesome-claude-design) — 런칭 후 1주 내
- [awesome-gpt-image (ZeroLu)](https://github.com/ZeroLu/awesome-gpt-image/) — 런칭 후 1주 내

두 사례 모두 **출시 직후 등장**, **DESIGN.md / prompt templates / style recipes** 구조. MCP server / Agent Skill / knowledge-layer 와 어깨를 나란히 하는 primitive 후보. **2 사례 확보로 insight card carve-out 가능** — `insights/primitive-prompt-pattern-market.md` 후보.

### D3. Big-lab 디자인 tool 흡수 패턴

- Google Stitch (구 Galileo AI) — **디자인 툴 레이어에서 big-lab 최초 흡수**. Google 이 Gemini 통합. 2026-04-22 기준 가장 명시적 사례.
- Canva Magic Studio — OpenAI 기반, **5B+ Magic Studio 사용**. OpenAI 가 이 레이어에 "OEM 벤더" 로 참여.
- Figma Make / Figma Weave — Figma 자체 AI 응답.

**유추**: Anthropic 은 Claude Design 으로 **자체 빌드** 경로 선택, OpenAI 는 **파트너십** 경로 선택. Google 은 **인수** 경로.

### D4. 동일 주 시장 반응

- **FIG (Figma)**: −7.04% (2026-04-17). "failed breakout" 프레이밍.
- **Adobe (ADBE)**: 동반 하락 (정확 수치 미수집).
- **Wix (WIX)**: 동반 하락.
- **gpt-image-2 런칭 2거래일 후 (04-22)**: 주가 영향 분산 — 직접 상장 경쟁사 없음 (Midjourney 비상장, Stability 재정 이슈).

→ 디자인 툴 시장이 **상장사 영향 구조** 임에 비해 이미지 모델 시장이 **비상장 중심 구조**. 투자자에게 보이는 "disruption" 신호가 다름.

---

## E. Phase 1 외부 리서치의 한계 — 명시적 공백

### E1. Architecture 비공개

- Claude Design 의 내부 표상 / `frontend-design` 스킬 스키마 / 토큰 소비 모델 — 비공개
- gpt-image-2 의 Thinking 아키텍처 / Arena 3변종 차이 / 99% benchmark 명칭 — 비공개

**Phase 1 외부 리서치로는 접근 불가**. 시스템 카드 / 논문 / source code 공개 모니터링이 해결책.

### E2. 실전 가격 경제성

- Claude Design: 단일 세션 weekly 50~95% burn 관찰 — 구조적 원인 (slider = model call 인가) 확정 못 함
- gpt-image-2: Simon Willison 4K high-quality $0.40 datapoint 1건 — 반복 재현 필요

### E3. handoff bundle 의 실제 format

- tar vs ZIP 일관성 미확인
- 컴포넌트 manifest / design tokens 포함 여부 미확인

**해결 경로**: 실제 Claude Design 사용 후 handoff bundle 추출 및 구조 분석. Phase 2 에서 가능.

---

## F. 주목할 한 가지

**"Design tool 카테고리가 code-generating LLM 의 thin UI 로 붕괴 중"**.

- Claude Design 의 handoff bundle 이 가장 날카로운 증거: **디자인은 사실상 prompt 묶음**이고, 실제 "design" 은 Claude Code 가 재구성할 때 발생.
- Figma Make, Lovable, v0, Bolt, Magic Patterns 모두 같은 방향으로 수렴 — **"design tool = LLM + canvas"**.
- 전통 Figma 의 구조화된 design object (nodes, constraints, auto-layout) 는 **human collaboration 의 artifact** 로 남고, production 으로 가는 경로는 별도.

**이것이 맞다면**:
- 2026 H2~2027: **디자인 도구 스타트업의 재편** — 모델 접근권을 가진 스타트업만 생존
- Figma 의 반응: **자체 모델 파트너십 vs. 인수 vs. in-house 모델** 중 선택 강제
- Anthropic 의 다음 수: **Claude Cowork 이 design 팀 collaboration layer 로 확장** (Figma 의 real-time cursor 대응)
- OpenAI 의 다음 수: **Codex + ChatGPT 에 design-product 레이어 추가** (Anthropic 의 Claude Design 대응)

이 예측의 falsifier:
- Figma 가 Claude Design 대응 제품을 6개월 내 공개했는데 사용자 이탈을 막는 데 성공 → 구조화된 design object 가 여전히 가치 있음
- Claude Design 의 "weekly 토큰 한도 burn" 이 사용자 성장을 제약 → price model 이 벽
- Claude Code 로의 handoff 가 실제로 production-grade 결과를 못 냄 → handoff-glue 가 production 에 부적합

Phase 2 에서 **graft-evaluator** 로 사용자 자신의 gamemaker / uuu 프로젝트에 Claude Design / gpt-image-2 적용 가능성 평가 시 이 가설들을 테스트 가능.

---

## G. 다음 세션 / 다음 기간에 볼 것

### 즉시 (1~2주)

- [ ] OpenAI 공식 announcement (openai.com/index/introducing-chatgpt-images-2-0) 403 해제 시 직접 fetch → "99%" / 속도 / 해상도 주장 1차 확인
- [ ] gpt-image-2 시스템 카드 / 논문 release 모니터링
- [ ] Claude Design handoff bundle 실제 추출 (사용자가 직접 사용 시)
- [ ] Figma 의 Claude Design 대응 제품 공개 시기

### 중기 (2026 Q2~Q3)

- [ ] **Insight card carve-out 후보**: `primitive-prompt-pattern-market.md` — `awesome-*` repo 패턴이 2 사례 확보. MCP / Skill / knowledge-layer 와 병렬 primitive
- [ ] **Arena-as-prelaunch-stealth-QA 패턴**: Anthropic (Opus 시절), Google (Nano Banana), OpenAI (gpt-image-2 "Duct Tape") 3 사례면 carve-out 가능
- [ ] **User-visible mode split 축 promotion**: Anthropic extended thinking (user visible) + OpenAI Instant/Thinking — 2사례 확보. 3번째 케이스 (Google Gemini mode toggle?) 확인 시 promotion
- [ ] **Skill-productization subtype** (Δ1): Claude Code `frontend-design` skill → Claude Design product. 2번째 사례 (다른 스킬이 standalone product 화) 확인 시 Δ1 subtype 확정

### Phase 2 진입 시

- [ ] uuu 프로젝트에 Claude Design graft 평가 — design 산출물이 필요한 module 있다면
- [ ] gpt-image-2 API 를 직접 사용하는 workflow — CJK 렌더링 실제 test

---

## H. 관련 노트 / cross-link

- [`notes/harness/claude-design.md`](../notes/harness/claude-design.md) — Claude Design deep-dive
- [`notes/harness/gpt-image-2.md`](../notes/harness/gpt-image-2.md) — gpt-image-2 deep-dive
- [`digests/2026-04-17-anthropic-sweep-vs-community-harnesses.md`](./2026-04-17-anthropic-sweep-vs-community-harnesses.md) — 기존 Anthropic sweep — Claude Design 은 이 sweep 의 "production" end-product
- `insights/primitive-knowledge-layer-design-space.md` — 지식 레이어 primitive card. handoff-bundle 을 knowledge-layer artifact 의 새 형태로 연결 가능성

## I. Source 요약

Claude Design + gpt-image-2 각각의 deep-dive 노트에 full source list. 본 digest 의 기반이 된 추가 소스:

- [Figma Config 2025 recap](https://www.figma.com/blog/config-2025-recap/) — Figma 자체 AI 응답 (Figma Make / Weave)
- [Google DeepMind — Nano Banana Pro](https://deepmind.google/models/gemini-image/pro/) — Thinking architecture 비교 대상
- [TechCrunch on Config](https://techcrunch.com/2025/05/07/figma-releases-new-ai-powered-tools-for-creating-sites-app-prototypes-and-marketing-assets/)
- [NxCode v0/Bolt/Lovable 비교](https://www.nxcode.io/resources/news/v0-vs-bolt-vs-lovable-ai-app-builder-comparison-2025)
- [The Neuron Daily](https://www.theneurondaily.com/p/anthropic-s-claude-design-launched-and-reddit-has-thoughts) — 파워유저 reaction 집약
