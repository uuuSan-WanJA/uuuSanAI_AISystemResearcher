---
title: Claude Design — deep dive
status: deep-dive
confidence: medium-high
rounds: 1 (web — no public repo)
subject: Claude Design (Anthropic Labs)
primary_source: https://www.anthropic.com/news/claude-design-anthropic-labs
license: proprietary (research preview)
version: research preview, launched 2026-04-17
tier_note: "notes/harness/ 배치는 사용자 지정. 엄밀히는 coding-harness 범주(Claude Code 등)가 아닌 Anthropic Labs의 design-layer product. handoff 메커니즘으로 Claude Code와 직접 결합되기 때문에 harness 생태계의 일부로 취급. 추후 tier 재편 시 `notes/products/` 또는 `notes/apps/` 후보."
runtime_notes: "외부 웹 리서치만 수행. Anthropic 공식 announcement + Help Center + Opus 4.7 post + 2nd-party 리뷰 15+건으로 교차검증. VentureBeat/Inc/MacStories 는 403/429 로 직접 인용 불가 → 검색 스니펫 경유 claim 은 confidence 한 단계 낮춤."
---

## TL;DR (5줄)

1. **Claude Design** = Anthropic Labs 가 2026-04-17 출시한 대화형 디자인 제품. Opus 4.7 기반, `claude.ai/design` 접속. Pro/Max/Team/Enterprise 플랜에 포함 (Enterprise 는 **기본 OFF** — 관리자 opt-in).
2. **핵심 차별화는 디자인 생성이 아니라 Claude Code handoff**: 산출물을 tar archive + README + 컴포넌트 파일 + 채팅 로그 형태로 묶어 "Claude Code 야, 내 코드베이스 맞춰 다시 구현해" 지시. 구조화된 design DSL 이 아님 — **prompt-handoff glue**.
3. **내부 표상은 HTML/JS**: Sam Henri Gold 의 관찰 *"HTML and JS all the way down"* — vector graph/component DB 저장소가 없어서 editing fragility + multi-user 실시간 협업 불가능의 구조적 이유가 됨. Figma 의 아키텍처와 정반대.
4. **Opus 4.7 (2026-04-16 출시, 1일 선행) 이 substrate**. 이미지 입력 최대 2576px(3.75MP, 이전 대비 3×) 지원. 스크린샷·코드베이스·디자인 파일 동시 ingestion 을 가능하게 하는 vision 전제조건이지만 Anthropic 공식 문구는 직접 연결 주장을 안 함 (추론).
5. **실전 평가는 양극단**: X 파워유저는 "10× better than Lovable" (Ran Segall), 반면 r/ClaudeAI 는 "resounding meh", HN 은 "single session 이 weekly Pro 한도 95% 소진", 그리고 모든 출력이 "container soup" (serif/accent bar/blinking dot) 동일 스타일로 수렴 — `frontend-design` 스킬의 기본 프리셋이 aesthetic attractor 로 작동.

---

## 1. Identity & provenance

- **Official announcement**: https://www.anthropic.com/news/claude-design-anthropic-labs
- **Product URL**: https://claude.ai/design — 웹 전용, 데스크톱/API 없음
- **Launch date**: 2026-04-17 (Friday)
- **Status**: research preview
- **Model substrate**: Claude Opus 4.7 (공식 confirmed — 동일 announcement 에 명시)
- **Opus 4.7 announcement**: https://www.anthropic.com/news/claude-opus-4-7 (2026-04-16, **1일 먼저** 출시)
- **Anthropic Labs 브랜드**: 이번 런칭으로 "Anthropic Labs" 가 제품 실험 sub-brand 로 확립. Claude Code 본체와는 별도의 experimental surface.
- **Pricing**: 기존 플랜에 번들 — *"Access is included with your plan and uses your subscription limits."* ([announcement](https://www.anthropic.com/news/claude-design-anthropic-labs)). 별도 티어 없음. 초과 사용 시 usage-based 추가 구매 가능.
- **Availability matrix** (Help Center [admin guide](https://support.claude.com/en/articles/14604406-claude-design-admin-guide-for-team-and-enterprise-plans)):
  - Pro / Max / Team: **기본 ON**, research preview 로 즉시 접근
  - Enterprise: **기본 OFF**, admin 이 opt-in 필요 (*"This capability is default off for Enterprise plans"*). 엔터프라이즈 데이터 거버넌스 우려 반영.

> Confidence: high. 모든 identity 사실은 1차 소스(공식 announcement + Help Center) 또는 1차 인용 확보.

## 2. Market context — collision timing

Claude Design 런칭은 **의도적 충돌**로 프레이밍된다:

- **Mike Krieger Figma 이사회 사임**: Anthropic CPO Mike Krieger 가 **2026-04-14** Figma 이사회에서 사임. 3일 후 Claude Design 런칭.
- **The Information 리포트**: 같은 날(04-14) Anthropic 의 디자인 도구 계획 첫 보도.
- **Figma 주가 반응**: 2026-04-17 당일 NYSE: FIG **−7.04%** (시가 ~$21 → 종가 $18.92, 장중 최저 $18.61). 다수 거래지 "failed breakout" 프레이밍.
- **2차 파장**: Adobe / Wix 주가도 동반 하락. 실제로 Gizmodo 헤드라인 그대로 *"Figma Stock Immediately Nosedives"*.
- Anthropic 자체 announcement 문구는 **Figma 를 직접 명명하지 않음** — 대신 우회 프레이밍 사용: *"Claude Design gives designers room to explore widely and everyone else a way to produce visual work"*. Canva 만 언급하면서 *"intended to complement rather than replace"* — Canva 는 보완재, Figma 는 대체재라는 암시적 positioning.

> Confidence: high (타이밍·주가). medium (Krieger 사임-런칭 linkage 의 인과성 — Krieger 측 해명 없음).

## 3. Product surface — UI shape & artifacts

### 3.1 UI layout

Help Center 공식 문구:
> *"Claude Design has two main areas: a chat interface on the left and a canvas on the right. You describe what you want in the chat, and Claude generates a working design on the canvas."*

- **좌측**: 채팅 인터페이스 (Claude Code / claude.ai 와 동일 패턴)
- **우측**: 캔버스 — 실시간 렌더링된 HTML/JS 아티팩트

### 3.2 산출물 유형 (announcement 에서 열거)

공식 문구:
> *"Interactive prototypes… Product wireframes and mockups… Design explorations… Pitch decks and presentations… Marketing collateral (landing pages, social media assets, campaign visuals)… Code-powered prototypes with 'voice, video, shaders, 3D and built-in AI'"*

구체적 예시 (Help Center 기준):
- dashboards
- mobile app onboarding flows
- landing pages
- forms
- internal tools
- pitch decks / one-pagers

### 3.3 입력 받는 것

- 텍스트 프롬프트
- 이미지 (스크린샷 포함)
- 오피스 파일: DOCX / PPTX / XLSX
- 코드베이스 참조 (GitHub 연동 또는 로컬 directory attach)
- 웹 캡처

### 3.4 수정 채널 (4가지)

announcement 원문:
> *"Comment inline on specific elements, edit text directly, or use adjustment knobs to tweak spacing, color, and layout live"*

4개 채널:
1. **인라인 코멘트** — 요소별 comment
2. **다이렉트 텍스트 편집** — 직접 typing
3. **Adjustment knobs/sliders** — 컨텍스트별 자동 생성 (spacing, color, layout)
4. **대화형 리파인** — 좌측 chat 경유

**중요 관찰**: Adjustment sliders 는 **고정 툴바가 아니라 model-generated per context**. 즉 각 element/컴포넌트마다 Claude 가 "이 요소에 뭐를 조정 가능한지" 실시간 판단해 슬라이더를 제공. 이 구조는 slider drag 1회가 Opus 4.7 호출 1회를 유발할 가능성을 시사 (→ 토큰 burn 문제의 유력 원인, §7 참조).

> Confidence: high (확정된 UX 구성요소는 Help Center 에 명시). medium (slider = model call 인지는 추론 — 공식 기술 명세 없음, 사용자 reproduction 미수행).

### 3.5 Export (확인된 경로)

- **HTML bundles** (기본 — internal 구조의 그대로)
- **PPTX** (사실상의 Gamma/Beautiful.ai 진입)
- **PDF**
- **Canva export** (공식 Canva 호환 경로)
- **Internal-org URL** (org 내부 공유 전용 링크)
- **"Save as folder"** (파일 번들 로컬 저장)

---

## 4. Code handoff — the load-bearing primitive

이 부분이 Claude Design 의 진짜 아키텍처적 차별점이다.

### 4.1 공식 문구

announcement:
> *"When a design is ready to build, Claude packages everything into a handoff bundle that you can pass to Claude Code with a single instruction."*

공식 tutorial ([claude.com/resources/tutorials/using-claude-design-for-prototypes-and-ux](https://claude.com/resources/tutorials/using-claude-design-for-prototypes-and-ux)):
> *"Click 'Export' and 'Hand off to Claude Code' to get started. By default, we bundle the project's design files, chat, and a README"*

### 4.2 handoff bundle 의 실제 형태

**Victor Dibia 의 newsletter 리뷰**가 1차 관찰로 가장 상세:
> *"a tar archive with a README instructing the coding agent to read the files directly and match the visual output in whatever technology fit the existing codebase."*

HN 에서는 "ZIP file" 로 언급 — tar vs zip 의 일관성은 미확정. 공식 Help Center 는 일반화된 "bundle" 용어만 사용.

구성 요소:
- 프로젝트의 HTML/CSS/JS 아티팩트 파일
- **README** — Claude Code 용 instruction ("이 파일들 읽고 기존 코드베이스의 기술 스택에 맞게 시각적으로 재현해")
- 채팅 transcript — 설계 의도 맥락
- 필요 시 이미지/asset

### 4.3 핵심 구조 관찰

Dibia 의 분석:
> *"[the README instructs the coding agent to] match the visual output rather than transpile"*

즉 이것은 **prompt + artifacts 묶음**이지, **declarative design-to-code manifest** 가 아니다. Figma 가 제공하는 JSON + design tokens + 컴포넌트 그래프 방식과 **구조적으로 다름**:
- Figma handoff: structured source-of-truth → 결정론적 export
- Claude Design handoff: semi-structured prompt → 확률론적 재현 (Claude Code 가 알아서 맞춤)

Sam Henri Gold 의 관련 관찰:
> *"Claude Design, for all its roughness, is at least honest about what it is: HTML and JS all the way down."*

### 4.4 handoff 목적지 (2가지)

Help Center 기준:
- **Send to local coding agent** — 사용자의 로컬 Claude Code / Codex 등으로 다운로드
- **Send to Claude Code Web** — 클라우드 Claude Code 워크스페이스로 직접 전송

### 4.5 코드베이스 링킹 효과

announcement:
> *"handoff is especially valuable when your codebase is linked, because Claude Code already understands the components and patterns the prototype was built with."*

→ 단방향 forward 흐름 (Design → Code) 은 공식 지원. **역방향 (Code → Design) 지원 여부 미확인** (Jack Anglesea 가 Medium 에서 "dumping things directly into Claude Code and vice versa" 로 암시하지만 공식 문서는 침묵).

> Confidence: high (forward handoff 확정). medium (파일 포맷 — tar vs zip). low (역방향 지원 여부).

---

## 5. Design system ingestion — onboarding 메커니즘

announcement 의 핵심 주장:
> *"During onboarding, Claude builds a design system for your team by reading your codebase and design files. Every project after that uses your colors, typography, and components automatically."*

### 5.1 링킹 방법 (tutorial 기준)

- **GitHub import** — repository URL 입력
- **로컬 디렉토리 attachment** — Import 버튼 경유

### 5.2 Claude 가 분석하는 대상

tutorial 문구:
> *"Component structure — Your UI building blocks and how they compose together; Styling and theming — Your color system, spacing scale, typography, and CSS approach."*

지원 스타일링:
- CSS modules
- Tailwind
- styled-components
- (기타 명시적 언급 없음 — SCSS/SASS, CSS-in-JS 변형 등은 불분명)

### 5.3 제약

**알려진 한계** (tutorial):
> *"Linking very large repositories can cause lag or browser stability issues… we recommend linking the specific package or directory… Chrome doesn't handle attaching huge file trees well."*

**제외 경로**:
- `.git/`
- `node_modules/`

### 5.4 조직 레벨 운영

admin guide:
- **"Organizations can have multiple design systems"** — multi-brand / multi-product 시나리오 대응
- **Design-system editing permissions** 이 custom role 로 분리 가능 — 모든 member 가 시스템 편집 가능한 건 아님
- **Upload brand assets**: 코드베이스 외에도 슬라이드 덱 / 기타 디자인 reference 파일 업로드 가능

### 5.5 저장 형태 (open question)

Claude 가 ingest 한 후 "design system" 이 실제로 어떻게 persist 되는가:
- (A) 생성된 tokens 파일 (colors.json, typography.json 등)?
- (B) 코드베이스 위의 embedding/RAG store?
- (C) system prompt prefix 형태의 compressed summary?

→ **공식 문서 미명시**. §10 의 follow-up Q3.

> Confidence: high (UX 인풋 측). low (저장 형태).

---

## 6. Model substrate — Opus 4.7

### 6.1 비전 해상도

Opus 4.7 announcement 에서 Claude Design 과 직결되는 수치:
> *"Opus 4.7 can accept images up to 2,576 pixels on the long edge (~3.75 megapixels), more than three times as many as prior Claude models."*

### 6.2 "디자인 취향" 주장

announcement:
> *"It's more tasteful and creative when completing professional tasks, producing higher-quality interfaces, slides, and docs."*

embedded user testimonial:
> *"Claude Opus 4.7 is the best model in the world for building dashboards and data-rich interfaces. The design taste is genuinely surprising — it makes choices I'd actually ship."*

### 6.3 가격

Opus 4.7 은 **Opus 4.6 과 동일 가격** ($5/$25 per M tokens input/output). 3× 해상도 + 디자인 성능 업그레이드를 무상 제공.

### 6.4 디자인 워크플로에 대한 의미 (추론)

- 2576px 한도가 있으면 **high-DPI 스크린샷 / dense mockup / multi-screen prototype 동시 ingest** 가능 — 이전 모델에서는 downsampling 이 필요했음
- 코드베이스 파일 + 디자인 reference 이미지 + 기존 스크린샷을 **한 컨텍스트**에 주입 가능 → 디자인 시스템 추출 품질의 원천

**캐비엇**: Anthropic 은 2576px 수치를 Claude Design 과 **직접 연결하여 주장하지 않음**. 인과성은 추론 기반. Claude Design 이 사실 더 낮은 해상도로만 처리하거나, 더 복잡한 tiling 전략을 쓸 수도 있음.

> Confidence: high (수치). medium (Claude Design 과의 인과 linkage).

---

## 7. Limitations & early critique

### 7.1 토큰 경제성 (지배적 불만)

HN 리뷰:
> *"I used it today… finally got something satisfactory. Then I looked at the usage and it said I had used 95% of my Claude design usage for the week!"* ([HN #47818700](https://news.ycombinator.com/item?id=47818700))

Neuron Daily: **2~3개의 full prompts 로 Pro weekly 한도 소진**.

Quasa 리뷰: **단일 세션(design system + news-site prototype + tweaks + explainer video)에서 Pro 한도 >50% 소진**.

**구조적 원인 가설**: adjustment slider drag 가 매번 Opus 4.7 호출을 트리거하는 경우 — §3.4 참조. 확정되면 product architecture 자체의 비용 구조 문제.

### 7.2 Homogenization — "container soup" 문제

Reddit reaction (Neuron Daily 요약):
> *"Every generated app looks identical, right down to the serif font, the blinking status dot, colored accent bars"*

Ocasio (aggregated):
> *"essentially cookie cutter templates you can find anywhere"*

**구조적 원인**: `frontend-design` 스킬이 Claude Code 플러그인 마켓 (`anthropics/claude-code`) 에 2025-10 부터 존재했고, **Claude Design 은 이 스킬의 productization** 이다. 스킬 정체성은 [`plugins/frontend-design/skills/frontend-design/SKILL.md`](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md) 에서 직접 확인 가능:

- **Authors**: Prithvi Rajasekaran + Alexander Bricken (Anthropic)
- **Install 수**: 299,900+ (플러그인 마켓 기준)
- **Cookbook reference**: `anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb` (longer-form Jupyter 노트북)

SKILL.md 의 **anti-pattern 블록이 특히 주목할 만하다** — 스킬 자체가 homogenization 을 *명시적으로 금지*한다:

> *"NEVER use: Generic AI-generated aesthetics / Overused font families (Inter, Roboto, Arial, system fonts) / Clichéd color schemes (particularly purple gradients on white backgrounds) / Predictable layouts and component patterns / Cookie-cutter design that lacks context-specific character"*

> *"No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations."*

SKILL.md 는 **11가지 tone palette** 로 분산을 유도:
- brutally minimal / maximalist chaos / retro-futuristic / organic/natural / luxury/refined / playful/toy-like / editorial/magazine / brutalist/raw / art deco/geometric / soft/pastel / industrial/utilitarian

**구조적 역설**: 스킬이 homogenization 을 명시적으로 금지하지만, 커뮤니티가 관찰하는 출력은 여전히 수렴 (serif + blinking dot + accent bar + container). **Prompt-level 지시가 training-data 기본값을 완전히 제압하지 못한다**는 증거. 이는 Anthropic 이 model-level fine-tuning 으로 해결해야 할 문제이지 skill-level 지침으로 해결 불가능한 문제일 가능성.

Korean-language 수용에서 choi.openai 가 2025-10 에 이미 같은 스킬을 다룸 (*"Claude Code 사용한다면 꼭 사용해보세요"*, [Threads](https://www.threads.com/@choi.openai/post/DRCQa-qisNd)) — Claude Design 의 underlying 이 이 스킬임을 간접 확인.

### 7.3 편집 취약성

Gizmodo:
> *"when a user starts trying to edit individual elements, things can quickly fall apart."*

Help Center 가 공식적으로 인정한 버그:
- Comment persistence issues
- Save errors in compact view mode
- Large codebase lag
- Chat upstream errors

**구조적 원인** (Sam Henri Gold 의 관찰에서 추론): 내부 표상이 HTML/JS 파일 집합이고 vector/component graph 가 없어서 "이 요소 하나만 수정" 이 "전체 재생성" 으로 쉽게 번짐.

### 7.4 Figma 대비 미비한 것들

(복수 리뷰 공통 — absence of evidence 이지만 모든 출처에서 일관):
- Multi-user real-time cursors — 없음
- Native versioning graph — 없음
- Component library source-of-truth — 없음
- Plugin ecosystem — 없음
- Vector-level editing surface — 명시적으로 없음

### 7.5 엔터프라이즈 거버넌스 공백

admin guide 가 자체 인정:
- **"doesn't support audit logs or usage tracking yet"**
- **"doesn't currently support data residency requirements"**

→ 엔터프라이즈 가 **기본 OFF** 인 구조적 이유.

### 7.6 Opus 4.7 자체의 동시기 issue

Neuron Daily 의 r/ClaudeCode 관찰 (Claude Design 과 무관한 Opus 4.7 전반):
- *"inventing files, defending hallucinated test results across 10 turns"*
- *"obsessively checking benign PowerPoint templates for malware"*

→ Claude Design 은 Opus 4.7 의 behavior issue 를 상속.

> Confidence: high (문제의 존재). medium (구조적 원인 가설 — 공식 확인은 아님).

---

## 8. Competitive positioning (요약 — §3 digest 에서 깊이 다룸)

**직접 경쟁군** (AI-native design 계열):
- v0 (Vercel) — component-scoped, React+Tailwind, Figma import
- Bolt.new (StackBlitz) — full-stack app, WebContainer
- Lovable — MVP-in-a-prompt, DB+auth 포함, Figma link import ($20M ARR 2개월 — 유럽 스타트업 최고 기록)
- Magic Patterns — custom component import, design-system-aware
- Galileo AI → Google Stitch — Gemini 기반, 구글 제품군 편입 (big-lab 최초 design-tool 흡수)
- Figma Make — Figma 자체 AI 응답 (Config 2025 발표). design-system awareness + Supabase 연동
- Canva Magic Studio — Magic Design/Media/Edit/Write/Switch/Morph + 5B+ 사용 (OpenAI 기반)

**Claude Design 만의 포지션**:
- 경쟁 제품들이 component / app / full-stack 각각에 수직 베팅하는 반면, Claude Design 은 **design system + 다종 artifact (prototype/slide/one-pager/marketing) + Code handoff** 의 수평 어그리게이션.
- 약점: 각 수직에서 전문 경쟁자에 밀림 (v0 의 React 퀄리티, Lovable 의 full-stack 완결성, Canva 의 template 라이브러리).
- 강점: handoff bundle 이 타 제품에 없는 유일 primitive.

---

## 9. 실제 사용 사례 (landscape sweep 에서)

**X / Threads 파워유저 데모**:
- **Ran Segall (@ransegall)**: Claude Design 으로 homeschooling app 구축 → *"10× better than Lovable or Replit"*
- **Jerrod Lew**: "personal dashboard OS" 2 prompts
- **rohitg00/awesome-claude-design** — DESIGN.md 프롬프트 패턴 큐레이션 repo. 런칭 직후 등장 (prompt-pattern market 의 1차 사례 — gpt-image-2 도 유사한 `awesome-gpt-image` 가 등장)

**공개된 워크플로**:
- *"Design System → PPTX / Canva export → Claude Code implementation"* 풀 루프
- *"Conversational UI → PPTX and Canva Export"* — PPTX export 가 Gamma / Beautiful.ai 대체 가능성
- Muzli walkthrough, claudefa.st handoff guide — 런칭 후 1주 내 2nd-party 튜토리얼 다수

**한국어권 수용**:
- [GPTERS](https://www.gpters.org/news/post/claude-design-sayongbeob-wanbyeog-jeongri----dijaineo-eobsi-pm-cangeobjaga-FT0hAJo0eifVMAj) — *"디자이너 없이 PM·창업자가 프로토타입 만드는 법"*
- [Digital Insight](https://ditoday.com/%ED%94%BC%EA%B7%B8%EB%A7%88-%EB%8C%80%EC%B2%B4%ED%95%A0%EA%B9%8C-%EC%95%A4%ED%8A%B8%EB%A1%9C%ED%94%BD-%ED%81%B4%EB%A1%9C%EB%93%9C-%EB%94%94%EC%9E%90%EC%9D%B8-%EC%B6%9C%EC%8B%9C/) — *"피그마 대체할까?"*
- RiseMoment AI 의 종합 가이드가 한국어권에서 가장 상세

**사용자/채널 관찰**: X 파워유저 = 열광, r/ClaudeAI = resounding meh. 타 개발자 커뮤니티 분기가 평소보다 커진 사례.

---

## 10. Follow-up questions (sharpest 5)

1. **Handoff bundle 의 실제 스키마**: tar vs zip 의 일관성. 디렉토리 구조 (flat HTML/CSS/JS + assets + README + chat transcript) 인지, 혹은 구조화된 manifest (components.json, tokens.json) 를 포함하는지. **이것이 Figma-killer 아키텍처(구조적 source-of-truth) vs prompt-handoff glue(재도출 가능 artifact)의 경계를 결정**.

2. **내부 저장 객체**: Sam Henri Gold 의 "HTML/JS all the way down" 관찰이 정확한가, 혹은 vector/component graph 레이어가 있는가? 사실이라면:
   - Multi-user 실시간 협업 로드맵은 구조적으로 불가
   - Editing fragility 가 바로 이 구조에서 기원
   - "Design system" 은 실제로는 재참조되는 코드 snippet 덩어리

3. **"design system" 의 persist 형태**: 코드베이스 ingest 후 실제로 어떻게 저장되는가 — tokens 파일 / embedding store / prompt prefix?  Admin 이 "multiple design systems per org" 스위칭하면 실제로 뭐가 바뀌나 (model context / system prompt / first-class config)?

4. **Adjustment slider 의 model-call 경제학**: 각 slider drag 이 Opus 4.7 호출 1회인가, 혹은 결정론적 CSS edit 인가? 토큰 burn 문제 (weekly 한도 50~95% 소진) 와 "live tweaking" UX 의 교차점.

5. **역방향 handoff (Code → Design)**: forward 는 공식, 역방향은 미확인. "기존 컴포넌트를 Claude Design 에서 재디자인" 시나리오가 지원되는가?

---

## 11. 본 프로젝트 corpus 와의 연결

### 11.1 관련 노트

- [`notes/harness/gpt-image-2.md`](./gpt-image-2.md) — 같은 주 OpenAI 의 대칭 launch. 레이어는 다름 (product vs model).
- [`digests/2026-04-22-design-layer-twin-launches.md`](../../digests/2026-04-22-design-layer-twin-launches.md) — Claude Design ↔ gpt-image-2 구조적 비교 digest.
- `notes/techniques/anthropic-*.md` 10건 — Anthropic 엔지니어링 패턴 스윕. Claude Design 은 Anthropic 의 "harness-design-long-running-apps" 패턴을 design-layer 로 확장한 첫 공식 사례.

### 11.2 스키마 축 영향

- **Δ1 provenance subtype**: Claude Design 은 Claude Code 의 `frontend-design` 스킬을 **productization** 했으므로 새 subtype 후보 — "skill-productization" (internal skill → standalone product). 2번째 사례 필요.
- **축 T out-of-loop productization**: openwork + Kilo 이미 2사례 (promotion 충족). Claude Design 이 3번째 사례 — pattern 의 stability 강화.
- **handoff-bundle-as-interchange-format**: 신규 축 후보. Figma export 와 구조적으로 다른 primitive (declarative → probabilistic). 2번째 사례 (다른 시스템의 유사 handoff) 필요 — Lovable / v0 / Magic Patterns 의 handoff 메커니즘 조사 후 promotion 판정.

### 11.3 Insight card 후보

- **prompt-pattern market** — `awesome-claude-design` + `awesome-gpt-image` 이 런칭 후 수일 내 등장한 curated prompt repo 패턴. MCP server / Agent Skill / knowledge-layer 에 이어 새 primitive 후보. 2 사례 확보. carve-out 검토 가능.

### 11.4 sources.md 등록

Claude Design announcement + Help Center + Claude Opus 4.7 announcement 를 active 소스로 등록 후 모니터링 대상 추가.

---

## 12. Source list

**Primary** (1차):
- [Anthropic: Introducing Claude Design by Anthropic Labs](https://www.anthropic.com/news/claude-design-anthropic-labs)
- [Help Center: Get started with Claude Design](https://support.claude.com/en/articles/14604416-get-started-with-claude-design)
- [Help Center: Admin guide for Team and Enterprise](https://support.claude.com/en/articles/14604406-claude-design-admin-guide-for-team-and-enterprise-plans)
- [Anthropic: Claude Opus 4.7 announcement](https://www.anthropic.com/news/claude-opus-4-7)
- [Official tutorial: Using Claude Design for prototypes and UX](https://claude.com/resources/tutorials/using-claude-design-for-prototypes-and-ux)

**2nd-party (technical commentary)**:
- [Victor Dibia — How good is Anthropic's Claude Design?](https://newsletter.victordibia.com/p/how-good-is-anthropics-claude-design) — handoff bundle 의 tar+README 형태 관찰
- [Sam Henri Gold — Thoughts and Feelings around Claude Design](https://samhenri.gold/blog/20260418-claude-design/) — "HTML and JS all the way down" 관찰
- [Jack Anglesea — Medium](https://medium.com/@jackanglesea/claude-design-is-here-and-its-narrowing-the-gap-between-design-and-engineering-36fb8c681293) — 디자인-엔지니어링 갭 내러티브

**Press**:
- [VentureBeat — 프롬프트-to-prototype challenges Figma](https://venturebeat.com/technology/anthropic-just-launched-claude-design-an-ai-tool-that-turns-prompts-into-prototypes-and-challenges-figma)
- [Gizmodo — Figma Stock Immediately Nosedives](https://gizmodo.com/anthropic-launches-claude-design-figma-stock-immediately-nosedives-2000748071)
- [TheNewStack — Figma and Canva rival](https://thenewstack.io/anthropic-claude-design-launch/)
- [CMSWire — Visual Prototyping](https://www.cmswire.com/digital-marketing/anthropic-labs-launches-claude-design-tool-for-visual-prototyping/)
- [ALM Corp — Features / Pricing / Use Cases](https://almcorp.com/blog/claude-design-anthropic-labs/)

**Community signal**:
- [HN thread #47818700](https://news.ycombinator.com/item?id=47818700) — 토큰 burn 관찰
- [Neuron Daily](https://www.theneurondaily.com/p/anthropic-s-claude-design-launched-and-reddit-has-thoughts) — r/ClaudeAI "resounding meh" 요약
- [choi.openai Threads (2025-10)](https://www.threads.com/@choi.openai/post/DRCQa-qisNd) — `frontend-design` 스킬 수용 (Claude Design 의 substrate)
- [awesome-claude-design (rohitg00)](https://github.com/rohitg00/awesome-claude-design) — prompt-pattern curation
- [Stockstotrade — FIG 주가 분석](https://stockstotrade.com/news/figma-inc-fig-news-2026_04_17-2/)
- [MarketingEdge — Figma 시가 7% 손실](https://marketingedge.com.ng/claude-design-launches-and-figma-loses-7-market-value-within-hours/)

**Korean**:
- [GPTERS — 디자이너 없이 PM·창업자가 프로토타입](https://www.gpters.org/news/post/claude-design-sayongbeob-wanbyeog-jeongri----dijaineo-eobsi-pm-cangeobjaga-FT0hAJo0eifVMAj)
- [Digital Insight — 피그마 대체할까?](https://ditoday.com/%ED%94%BC%EA%B7%B8%EB%A7%88-%EB%8C%80%EC%B2%B4%ED%95%A0%EA%B9%8C-%EC%95%A4%ED%8A%B8%EB%A1%9C%ED%94%BD-%ED%81%B4%EB%A1%9C%EB%93%9C-%EB%94%94%EC%9E%90%EC%9D%B8-%EC%B6%9C%EC%8B%9C/)
- [RiseMoment AI — Claude Design 종합 가이드](https://blog.risemoment.ai/claude-design-complete-guide/)
- [Quasa — 토큰 한도 burn 분석](https://quasa.io/media/claude-design-looks-great-but-it-devours-your-token-limits-here-s-how-to-use-it-smartly)

**Failed fetches** (명시):
- VentureBeat article body — 429 Too Many Requests
- Inc.com "Saved 10 hours" — 403 Forbidden
- MacStories hands-on preview — 403 Forbidden
- Tom's Guide pizza-startup review — navigation chrome only
