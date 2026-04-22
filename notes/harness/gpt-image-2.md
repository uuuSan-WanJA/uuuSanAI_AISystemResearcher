---
title: GPT Image 2 (ChatGPT Images 2.0, codename "Duct Tape") — deep dive
status: deep-dive
confidence: medium-high
rounds: 1 (web — primary blocked 403, routed via 2nd-party)
subject: gpt-image-2 / ChatGPT Images 2.0
primary_source: https://openai.com/index/introducing-chatgpt-images-2-0/ (403 — 직접 fetch 불가)
api_docs: https://developers.openai.com/api/docs/models/gpt-image-2
license: proprietary (OpenAI hosted, partner-hosted via fal.ai + Azure Foundry)
version: gpt-image-2 snapshot `gpt-image-2-2026-04-21`, launched 2026-04-21
tier_note: "notes/harness/ 배치는 사용자 지정. 엄밀히는 image-generation model (Anthropic 이 LLM 을 만드는 것과 같은 layer). `notes/llm/` (현재 비어있음) 에 더 적합할 수도 있지만 사용자 지정을 따름. Phase 2 에서 tier 재편 시 재배치 후보."
runtime_notes: "OpenAI 공식 announcement 페이지(openai.com/index/introducing-chatgpt-images-2-0/)가 모든 직접 fetch 시도에서 403 반환. 핵심 quote 는 PetaPixel + TechCrunch + Microsoft Foundry 블로그 등 2차 전달 경유. fal.ai + developers.openai.com + Microsoft techcommunity 는 1차 fetch 성공. 여러 SEO 사이트의 고유 주장(99% 정확도 benchmark 명칭, '2× 속도' 구체 수치, '4K native' 등)은 confidence 를 한 단계 이상 낮춤."
---

## TL;DR (5줄)

1. **gpt-image-2** (ChatGPT Images 2.0) = OpenAI 가 2026-04-21 공식 발표, 04-22 롤아웃 개시. 코드명 "Duct Tape" 는 **2026-04-04** LM Arena 에 익명 3변종 (`packingtape-alpha` / `maskingtape-alpha` / `gaffertape-alpha`) 으로 등장한 prelaunch test 에서 유래.
2. **아키텍처 핵심은 Instant vs Thinking 모드 분리**. Thinking 모드가 "이 모델은 생각한다" 주장의 실체 — 웹 검색 + 멀티 캔디데이트 자체 검증 + 1 프롬프트 당 최대 8장 연속성 생성. 공식 직접 인용: *"Images 2.0 is our first image model with thinking capabilities"*.
3. **Arena 벤치마크에서 Nano Banana 2 를 +242점차로 압도** — *"largest gap between #1 and #2 ever recorded"*. 비-라틴 텍스트 서브카테고리에서 **+316점 점프** — 한/중/일/힌/벵 렌더링의 구조적 개선 시사.
4. **팩트체크 필요 항목 다수**: "99% typography accuracy" 의 benchmark 명칭 미공개, "4096×4096 native" 는 실제로는 2K 지원 + 4K experimental, "2× 속도" 는 TechCrunch 가 오히려 slower 관찰. → 마케팅 overshoot 영역.
5. **API 는 day-0 부터 간접 접근 가능**: fal.ai + Microsoft Foundry 에서 2026-04-21 동시 GA. OpenAI 직접 API 는 문서 공개됐으나 rate limit tier 로만 접근 (free tier 미지원). Simon Willison hands-on: 4K high-quality 이미지 = ~$0.40 (13,342 output tokens @ $30/M).

---

## 1. Identity & provenance

- **Official launch**: 2026-04-21 (Tuesday) — OpenAI announcement + Sam Altman 주도 라이브스트림
- **Codename**: "Duct Tape" — LM Arena 익명 테스트에서 유래, 공식 확인 post-launch
- **Model IDs**:
  - API: `gpt-image-2`
  - Snapshot: `gpt-image-2-2026-04-21`
  - fal.ai slug: `openai/gpt-image-2` (generation), `openai/gpt-image-2/edit` (editing)
- **Livestream presenters** ([OpenAI Developer Community](https://community.openai.com/t/livestream-starting-now-chatgpt-images-2-0/1379464)):
  - Sam Altman (host)
  - Gabriel Goh, Kenji Hata, Kiwhan Song, Alex Yu, Boyuan Chen, Nithanth Kudige (researchers)
  - **Mira Murati 부재** — 본 런칭에는 등장하지 않음 (이전 리포트의 Murati 인용은 부정확)
- **Altman 키노트 프레이밍** (Gizmodo 경유):
  > *"Images 2.0 is a huge step forward; this is like going from GPT-3 to GPT-5 all at once."*
  > *"Its ability to make extremely beautiful things is remarkable. The team really cooked with this one."*
- **Rollout timeline** (TechCrunch):
  > *"All ChatGPT and Codex users will be able to access Images 2.0 starting Tuesday; paid users will be able to generate more advanced outputs."*
- **접근 계층**:
  - Free tier (ChatGPT): Instant 모드 일부 사용 가능
  - Plus / Pro / Business: Thinking 모드 해제 — 웹 검색 / 8장 시퀀스 등
  - API: tier-based rate limits (see §6)

> Confidence: high (identity + 런칭 타이밍). medium (Thinking 모드 gating 의 정확한 티어 경계 — 2차 소스 편차 있음).

## 2. "Duct Tape" — Arena prelaunch history

### 2.1 3 변종

- `packingtape-alpha`
- `maskingtape-alpha`
- `gaffertape-alpha`

**첫 등장**: 2026-04-04 on LM Arena (*"with little fanfare"* — Miraflow)

**첫 공개 flagger**:
- **Pieter Levels (@levelsio)**
- **Justine Moore (@venturetwins)**

**한국어권 seed post**: **@aisocity Threads, 2026-04-04**:
> *"OpenAI's new image model GPT-Image-2 has leaked. It seems to have extremely good world knowledge and great text rendering. Possibly better than Nano Banana Pro."* (4 images: world map/radar, poster, product display, YouTube UI mock) ([Threads](https://www.threads.com/@aisocity/post/DWtLdcMjOOf/open-ais-new-image-model-gpt-image-has-leaked-it-seems-to-have-extremely-good))

### 2.2 변종 간 차이 (약하게 문서화됨)

- **packingtape-alpha**: *"correctly rendered the time on a watch in an image, something Nano Banana Pro failed to do"* (OfficeChai)
- **maskingtape-alpha**: Minecraft Manhattan 프롬프트에서 *"outperformed all three of its tape siblings — and Nano Banana Pro"*
- **gaffertape-alpha**: 구분되는 고유 특성 미보고
- Miraflow 는 *"Duct Tape 2 and 3 appeared to produce the best results"* 로 표현 — 구체 순서는 혼재

해석: 3개는 독립 제품이 아닌 **같은 모델 패밀리의 체크포인트 또는 튜닝 변종**일 가능성이 높음. 공식 확인 없음.

### 2.3 철회

Miraflow: *"pulled from the Arena within hours"* — 정확한 timestamp 없음. 2026-04-04 ~ 04-16 사이 간헐적 재등장.

### 2.4 OpenAI 공식 확인

런칭 후:
> *"Instant Mode was internally tested under the codename 'duct tape.'"* ([InterestingEngineering](https://interestingengineering.com/ai-robotics/chatgpt-images-2-0-2k-output))

→ "Duct Tape" 는 **Instant 모드 체크포인트의 코드명**. Arena 3변종이 모두 Instant 모드인지 일부는 Thinking 모드인지는 미확인.

### 2.5 커뮤니티 벤치마크 프롬프트 (Arena 테스트용)

주목받은 프롬프트:
- *"Average engineer's screen"*
- *"Young woman taking selfie with Sam Altman"*
- *"Top-down strategy game about optimizing an AI data center, high-end realistic graphics"*
- *"First-person Minecraft gameplay screenshot set in Manhattan"*
- Fake OpenAI homepage
- Shibuya Scramble 4 AM rain
- League of Legends KDA HUD
- **Rubik's cube reflection** — Duct-tape 가 여전히 **실패**하는 테스트 (거울 물리 정합성)

> Confidence: high (3변종 존재 및 타이밍). medium (변종별 차이 — 단일 소스). medium (OpenAI 의 공식 linkage).

---

## 3. Two-mode architecture: Instant vs Thinking

이 부분이 기존 image 모델과의 구조적 차이점이다.

### 3.1 공식 주장

PetaPixel 경유 OpenAI 직접 인용:
> *"To extend the model's capabilities for the most complex tasks, Images 2.0 is our first image model with thinking capabilities."*

### 3.2 모드별 특성

**Instant 모드**:
- 기본 설정 — fast, 단일 출력
- Free tier 도 접근 가능
- Duct Tape 코드명이 여기서 유래

**Thinking 모드** (paid 티어 한정):
- 웹 검색 가능 — *"search the web for real-time information"* (TechCrunch)
- 멀티 캔디데이트 자체 검증 — *"double-check its own outputs"*
- **최대 8장 시퀀스** — *"You can ask for a coherent set of up to eight outputs in one go with character and object continuity, that sequentially build on one another"* (OpenAI 직접 인용)
- *"The system no longer simply 'draws'; it researches, plans, and reasons through the structure of an image before the first pixel is rendered"* (The New Stack)

### 3.3 아키텍처 — open question

OpenAI 가 **명시적으로 architecture 공개를 거부**:
> *"OpenAI declined to specify the underlying architecture."* (TechCrunch)

후보 가설 (§11 follow-up Q4):
- (A) Latent-space CoT — diffusion step 전에 reasoning pass
- (B) Planner-LLM + diffusion backbone — LLM 이 layout spec 작성 → 별도 렌더링 모델이 실행
- (C) Unified autoregressive — Recraft v3 처럼 AR 아키텍처 + reasoning token

System card / paper 미발표. 2026-04-22 시점 공개 정보로는 판별 불가.

### 3.4 "intelligent routing layer" — 정정

일부 2차 소스가 "intelligent routing layer" 를 언급하지만 **OpenAI 공식 용어 아님**. 실제 architecture 는 **user-visible Instant/Thinking 선택**. GPT-5 의 real-time router (숨겨진) 와 달리 **user-facing mode toggle** — 이것이 OpenAI 의 설계 선택.

> Confidence: high ("thinking" claim 이 OpenAI 공식). low (실제 architecture).

---

## 4. Technical capabilities — claims vs verification

### 4.1 해상도 (disputed)

**공식 발표** (9to5Mac, InterestingEngineering):
> *"Images can now be up to 2K resolution and in multiple aspect ratios"*
> *"Aspect ratios from 3:1 to 1:3"*

**4K "native" 주장** (여러 SEO 사이트):
- fal.ai 문서: *"Maximum edge: 4000px … Maximum total pixels: 8,294,400 (roughly 4K)"* — 가능성은 있음
- **하지만**: *"resolutions above 2K should be considered experimental"* + *"recommend 'low-quality generation plus upscaling' for 4K"*
- Simon Willison hands-on: **3840×2160** 이 실제 API 최대로 관찰

→ **실전 ceiling 은 2K, 4K 는 experimental/upscale 경로**. 마케팅 "4096×4096 native" 는 overshoot.

### 4.2 타이포그래피 99% — benchmark 미공개

주장:
> *"OpenAI says GPT-Image-2 hits 99% accuracy on standard typography benchmarks"*

**문제**: *어느* benchmark 인지 명시되지 않음. TextEval? OCR-bench? MARIO-Eval? 자체 internal eval? 공개 방법론 없음.

**참고 대비 수치** (fal.ai learn page 경유):
> *"reportedly achieves 'over 99%' accuracy compared to 90–95% in previous versions"*

→ Ideogram 3 이 ~90% 주장 → gpt-image-2 가 +5~9% 개선을 99% 클레임으로 환산.

### 4.3 속도 — slower 관찰 존재

마케팅: "~2× 속도 vs gpt-image-1"

반례 (TechCrunch):
> *"a multi-paneled comic still takes just a few minutes"*

→ **text prompt 대비 느림**. "2×" 는 gpt-image-1 대비 수치이지만 1차 소스 확인 불가. SEO aggregator 들의 복제 가능성.

### 4.4 다국어 텍스트 (primary — PetaPixel 직접 인용)

OpenAI 공식:
> *"Stronger multilingual understanding and significant gains in non-Latin text rendering, particularly in Japanese, Korean, Chinese, Hindi, and Bengali."*

Arena **+316점 점프** in 비-라틴 텍스트 서브카테고리 (OfficeChai) — 수치적 확인.

### 4.5 8장 시퀀스 (Thinking 모드)

OpenAI 공식:
> *"You can ask for a coherent set of up to eight outputs in one go with character and object continuity, that sequentially build on one another."*

→ **manga/comics/storyboard** 유즈케이스의 근거.

### 4.6 입력 모달리티

- 텍스트
- 이미지 (reference)
- 이미지 편집 (edit endpoint — `openai/gpt-image-2/edit` on fal)
- `input_fidelity` 파라미터는 **disabled** for gpt-image-2 (fal 확인)

> Confidence: high (다국어 / 8장 시퀀스 — 1차 인용). medium-low (99% / 4K / 2× — 마케팅 수치, benchmark 미공개).

---

## 5. Arena benchmark results

OfficeChai 수집 데이터 (가장 상세 단일 소스):

| 카테고리 | gpt-image-2 | Nano Banana 2 | 차이 |
|---|---|---|---|
| Text-to-Image | **1,512** | 1,271 | **+242** |
| Single-Image Edit | 1,513 | ~1,388 | +125 |
| Multi-Image Edit | 1,464 | ~1,374 | +90 |
| Non-Latin Text (subcategory) | — | — | **+316** |

**키 인용** (OfficeChai):
> *"the largest gap between #1 and #2 ever recorded"*

### 해석

- **Text-to-Image 격차 +242** 는 역대 최대. Arena 에서 통상 #1 ↔ #2 차이는 30~80점 수준 → **3~8× 구조적 격차**.
- **Non-Latin Text +316** 은 단일 카테고리 최대 점프. 아시아 시장 대상 경쟁 축의 전환점 (§9 참조).
- **Edit 카테고리에서는 격차 축소** (+125, +90). 즉 generation 에서 압도적이지만 editing 에서는 Nano Banana 2 가 상대적으로 선방.

> Confidence: medium (단일 1차 소스 — Arena 공식 dashboard 재확인 필요). high (+242 클레임의 ordinality).

---

## 6. API details

### 6.1 OpenAI 직접 API

**Developers 문서**: https://developers.openai.com/api/docs/models/gpt-image-2

- **Endpoint**: `POST /v1/images/generations` + `POST /v1/images/edits`
- **Model parameter**: `model: "gpt-image-2"`
- **Snapshot pinning**: `gpt-image-2-2026-04-21`
- **Quality tiers** (fal 표기 — OpenAI 도 유사 추정): `low`, `medium`, `high`
- **Image size**: `landscape_16_9`, `square`, `portrait_9_16` 등 aspect-ratio preset
- **Input fidelity**: **disabled** for this model

### 6.2 Rate limits (by tier)

| Tier | TPM (tokens/min) | IPM (images/min) |
|---|---|---|
| Tier 1 | 100,000 | 5 |
| Tier 2 | 250,000 | 20 |
| Tier 3 | 800,000 | 50 |
| Tier 4 | 3,000,000 | 150 |
| Tier 5 | 8,000,000 | 250 |
| Free | 미지원 | 미지원 |

### 6.3 가격 (추정 / 관찰)

**OpenAI docs**: per-image USD 명시 없음 — pricing calculator 로 리다이렉트.

**Simon Willison hands-on** (결정적 datapoint):
- 3840×2160 high-quality 이미지 1장 → **13,342 output tokens** @ $30/M → **~$0.40**

**fal.ai 가격 레인지** (partner hosting):
- Low (1024×768): **$0.01 / image**
- High (4K): **$0.41 / image**

→ OpenAI 직접 + fal 가 유사한 상한. Ideogram 3 Quality ($0.09) / Nano Banana Pro ($0.134) 대비 **3~5× 비쌈**.

### 6.4 SDK 호환성

Simon Willison:
> *"OpenAI's Python client hasn't yet been updated to include gpt-image-2 but doesn't validate the model ID"*

→ 클라이언트 업데이트 없이 model 문자열만 넘기면 작동. SDK 보수 타임라인 미정.

> Confidence: high (API docs + Willison primary). medium (fal 가격이 OpenAI 와 정확히 일치하는지).

---

## 7. Distribution partners

### 7.1 fal.ai — day-0 hosting

- 출시일 2026-04-21 동시 GA
- Pay-per-image, subscription 없음
- Model slugs: `openai/gpt-image-2`, `openai/gpt-image-2/edit`
- 마케팅: *"takes a quality-first approach" — "prioritizes quality over speed"*

### 7.2 Microsoft Foundry / Azure — day-0 GA

[Microsoft techcommunity blog](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/introducing-openais-gpt-image-2-in-microsoft-foundry/4500571):
> *"now generally available and rolling out today to Microsoft Foundry."*

**Azure 가격** (per 1M tokens):
| 종류 | Input | Cached Input | Output |
|---|---|---|---|
| Images | $8 | $2 | $30 |
| Text | $5 | $1.25 | $10 |

- **Deployment type**: Standard Global 만 (Provisioned 미언급)
- **Safety**: *"OpenAI's image generation safety mitigations with Azure AI Content Safety, including filters and classifiers for sensitive content"*
- 지역 리스트 미공개

### 7.3 "API 는 5월 초" 주장 — 재해석

많은 SEO 소스가 "API access in early May" 주장. **실제로는**:
- OpenAI 직접 API: 2026-04-21 부터 developers.openai.com docs 공개, tier-gated access 즉시
- fal.ai: day-0 GA
- Azure Foundry: day-0 GA

→ "early May" 는 아마도 **무료 / Tier 1 상향 조정 또는 추가 endpoint 릴리스** 시점으로 추정. SEO 소스의 부정확한 복제 가능성 높음.

> Confidence: high (Azure + fal 실제 GA). medium ("early May" 주장의 실체).

---

## 8. Concrete demo list (keynote)

Gizmodo / PetaPixel / TechCrunch / Community 관찰 종합:

- **쌀알 한 톨 위에 쓰여진 텍스트** — precision demo
- **동일 캐릭터가 여러 panel 에 걸쳐 진화하는 만화** — character continuity
- **단일 프롬프트로 전체 magazine page** (typography + layout)
- **인포그래픽 / 슬라이드 / 지도 / 다국어 텍스트** (VentureBeat 헤드라인)
- **DALL-E 3 vs Images 2.0 레스토랑 메뉴 비교** (typography progression)
- **Starling murmuration** (realism)
- **Periodic table** (multi-cell typography stress test — fal learn page)

마케팅 프레이밍 (Gizmodo):
> 이전 버전들이 *"cave drawings"* 과 *"ancient art"* 였다면, Images 2.0 은 *"Renaissance"* — 이미지 생성의 르네상스.

---

## 9. Competitive positioning (요약 — digest 에서 깊이)

### 주요 경쟁 모델 (2026-04 기준)

| 모델 | 벤더 | 강점 | 대비 gpt-image-2 |
|---|---|---|---|
| **Nano Banana Pro** (Gemini 3 Pro Image) | Google | 구조적 thinking, conversational edit, brand/context aware, $0.134 | Arena 에서 +242 차이로 밀림, 특히 비-라틴 텍스트 |
| **Imagen 4** | Google | 가격 리더십 ($0.02~0.06), 생성 전용 | thinking 없음, 대화 편집 없음 |
| **Midjourney v8.1 Alpha** | Midjourney | 예술적 퀄리티, 3D mesh 생성(`--3d`), video extension | 텍스트 렌더링 약점 — ~15% gain 만 |
| **Ideogram 3** | Ideogram | 기존의 "text-first" 전문 모델 (~90%) | gpt-image-2 가 99% 주장으로 moat 흡수 |
| **Recraft v3** | Recraft | AR 아키텍처, **SVG/vector 출력** | niche 로 생존 (vector 는 gpt-image-2 비지원) |
| **FLUX 2 Pro** | Black Forest Labs | **open weights**, multi-image refs, 4K, $0.055 | self-hosting 에서 생존 |
| **SD 3.5** | Stability | open weights, ComfyUI 생태계 | control-first niche |
| **Firefly Image Model 4** | Adobe | 상업 안전 (Adobe Stock / 공개 domain 학습), Precision Flow slider | enterprise 라이선스 moat |
| **Krea 1** | Krea AI | aggregator (64+ models), realtime canvas | UX 레이어 — gpt-image-2 를 포함 |

### gpt-image-2 의 position

- **Text rendering moat 흡수** — Ideogram / Recraft 의 핵심 차별화를 base model 로 편입
- **"Thinking" architecture** — Nano Banana Pro 와 함께 새로운 table-stakes 가 됨. 순수 diffusion (Midjourney / Flux / SD) 압박
- **비-라틴 텍스트** — 한/중/일 3국 시장 대상 경쟁에서 선점
- **약점**: SVG/vector 비지원, open weights 아님, 4K 는 experimental, 여전히 Rubik's cube 반사같은 물리 정합성 테스트에서 실패

---

## 10. Limitations & open issues

### 10.1 OpenAI 공식 인정 (PetaPixel 경유)

> *"still has limitations, particularly in areas that require precise physical reasoning or highly detailed structural accuracy"*
> *"extremely dense textures and highly detailed diagrams may require additional review"*

### 10.2 Knowledge cutoff

- **2025년 12월** (TechCrunch, 9to5Mac). 최신 이벤트/인물 렌더링 불가 — 웹 검색 경유 우회 필요.

### 10.3 속도

- TechCrunch: text prompt 대비 **느림**. "a multi-paneled comic still takes just a few minutes"
- Thinking 모드 + 8장 시퀀스는 1회 수분

### 10.4 4K — experimental

- fal.ai learn: 4K 는 "experimental"
- 권장 경로: **low-quality 생성 + upscaling**

### 10.5 여전히 failing 케이스

- **Rubik's cube 반사** — duct-tape Arena 시대부터 fail (Miraflow)
- **픽셀 아트 / 스프라이트시트** 약함 (OpenAI Community thread)
- Simon Willison raccoon 테스트: **default 설정에서 target 미스, `high` 설정에서만 성공**

### 10.6 Watermarking / provenance — 공백

- C2PA 메타데이터: DALL·E 3 이후 기존 정책 유지 추정, **gpt-image-2 에 대한 명시적 재확인 없음**
- **SynthID 등가 invisible watermark 없음** — Google Nano Banana Pro 와의 차별
- 2026 규제 환경 (EU AI Act transparency 08-02, TAKE IT DOWN Act May 2026) 대비 정책 미흡 가능성

### 10.7 Architecture 공개 거부

- 시스템 카드 / 논문 / architecture diagram 모두 미공개 — §3.3 follow-up

> Confidence: high (OpenAI 자체 인정 + 실측 관찰). medium (정책 gap 의 규제 영향).

---

## 11. Follow-up questions (sharpest 5)

1. **"99% typography accuracy" 의 benchmark 명칭**. 모든 1차/2차 소스가 명칭 없이 수치만 반복. 어느 내부 eval 인지, 공개 benchmark 라면 TextEval / OCR-bench / MARIO-Eval 중 무엇인지. 미공개 시 independent 재현 설계 필요.

2. **Thinking 모드의 실제 아키텍처**. Latent-space CoT (diffusion 전 reasoning pass) vs planner-LLM + diffusion backbone vs unified AR 중 무엇인가? OpenAI 의 architecture 공개 거부로 현 시점 판별 불가 — 시스템 카드 / 논문 release 모니터링.

3. **Watermarking/provenance 정책**. SynthID 등가 invisible watermark 없다는 것이 2026 EU AI Act 의 transparency 의무 (08-02) 를 충족하는가? OpenAI 가 C2PA 만으로 compliance 유지할 계획인지, 추가 release 예정인지.

4. **Arena 3변종 (`packingtape` / `maskingtape` / `gaffertape`) 이 실제로 어떤 튜닝 차이인가**. 모두 Instant 모드인가, 일부는 Thinking 모드 프로토타입인가? OpenAI 가 post-launch 에 어느 변종이 최종 gpt-image-2 가 됐는지 공개할 가능성.

5. **실제 API 접근 타임라인**. "early May" 주장이 무엇을 가리키는가 — 무료 tier 상향, 추가 endpoint, 멀티모달 output (video/3D) 등. OpenAI 공식 공지 모니터링 필요.

---

## 12. 본 프로젝트 corpus 와의 연결

### 12.1 관련 노트

- [`notes/harness/claude-design.md`](./claude-design.md) — 같은 주 Anthropic 대칭 런칭. 레이어 다름 (model vs product).
- [`digests/2026-04-22-design-layer-twin-launches.md`](../../digests/2026-04-22-design-layer-twin-launches.md) — 구조적 비교 digest.

### 12.2 스키마 축 영향

- **llm tier 첫 entry**: 현재 프로젝트 `notes/llm/` 이 비어있음. gpt-image-2 가 image-gen model 이므로 엄밀히는 거기에 속함. harness/ 배치는 사용자 지정 이지만, tier 재편 시 "llm" 이 "image/video 포함 foundation model" 로 재정의되면 이 노트의 재배치 후보.
- **vendor-visible vs vendor-hidden mode split 축 후보**: GPT-5 의 hidden router 와 달리 **user-facing Instant/Thinking toggle** 이 이 모델의 선택. Anthropic 의 extended thinking (user visible) 과 설계 일관성. 2번째 사례 확보로 축 promotion 검토 가능.
- **pre-launch Arena anonymous test 축 후보**: LMSYS Arena 를 익명 prelaunch 채널로 쓰는 패턴 — Anthropic (Claude Opus 4.5 의 anonymous 시기), Google (Nano Banana prelaunch) 모두 유사 이력. "Arena-as-prelaunch-stealth-QA" 패턴. 3 사례면 primitive 카드 carve-out 가능.

### 12.3 모니터링 대상

- OpenAI 공식 page 403 해제 시 직접 fetch 및 모든 "99%" / 속도 / 해상도 주장 1차 확인
- 시스템 카드 / 논문 release
- fal.ai 의 `input_fidelity` disable 해제
- API tier 1 한도 변화

### 12.4 choi.openai Threads 한국어 signal

- 2026-04-04 @aisocity 의 prelaunch 식별이 한국어권 early-signal 채널로 검증됨. sources.md 에 등재 가치.
- choi.openai 의 gpt-image-2 공식 post-launch post 는 landscape sweep 중 landscape 에이전트가 확인 — 한국어 렌더링 99%+ 주장, Nano Banana Pro 3축 동시 압도 클레임.

---

## 13. Source list

**Primary (직접 fetch 성공)**:
- [OpenAI Developer API docs — gpt-image-2](https://developers.openai.com/api/docs/models/gpt-image-2)
- [Microsoft Foundry (Azure AI) — gpt-image-2 GA](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/introducing-openais-gpt-image-2-in-microsoft-foundry/4500571)
- [fal.ai — gpt-image-2 playground](https://fal.ai/gpt-image-2)
- [fal.ai learn — What is gpt-image-2](https://fal.ai/learn/tools/what-is-gpt-image-2)
- [OpenAI Developer Community — Livestream thread](https://community.openai.com/t/livestream-starting-now-chatgpt-images-2-0/1379464)
- [OpenAI Help — C2PA in ChatGPT Images](https://help.openai.com/en/articles/8912793-c2pa-in-chatgpt-images) (legacy policy)

**Primary (403/429 — 2차 인용 경유)**:
- [OpenAI — Introducing ChatGPT Images 2.0](https://openai.com/index/introducing-chatgpt-images-2-0/) — **403**

**Press (1차 소스 quote 전달)**:
- [TechCrunch — surprisingly good at text](https://techcrunch.com/2026/04/21/chatgpts-new-images-2-0-model-is-surprisingly-good-at-generating-text/)
- [PetaPixel — Claims ChatGPT Images 2.0 Can Think](https://petapixel.com/2026/04/21/openai-claims-chatgpt-images-2-0-can-think/)
- [Gizmodo — usher in AI slop renaissance](https://gizmodo.com/openai-unveils-new-image-generator-to-usher-in-an-ai-slop-renaissance-2000749159)
- [9to5Mac — ChatGPT Images 2 magazine design](https://9to5mac.com/2026/04/21/openai-unveiling-chatgpt-images-2-image-generation-model-watch-live-demo-here/)
- [InterestingEngineering — 2K output](https://interestingengineering.com/ai-robotics/chatgpt-images-2-0-2k-output)
- [The New Stack — OpenAI thinks before it draws](https://thenewstack.io/chatgpt-images-20-openai/)
- [Thurrott — OpenAI announces ChatGPT Images 2.0](https://www.thurrott.com/a-i/openai-a-i/335196/openai-announces-chatgpt-images-2-0)
- [TechRadar — fundamentally change how you make AI images](https://www.techradar.com/ai-platforms-assistants/chatgpt/not-just-generating-images-its-thinking-chatgpt-images-2-0-could-fundamentally-change-how-you-make-ai-images)

**Arena + Duct Tape history**:
- [OfficeChai — Three codename models on Arena](https://officechai.com/ai/three-image-generation-models-named-maskingtape-gaffertape-and-packingtape-create-buzz-on-arena-rumoured-to-be-openais-gpt-image-2/)
- [OfficeChai — Arena post-launch numbers](https://officechai.com/ai/chatgpt-images-2-0-tops-arena-with-big-jump-over-nano-banana-2/)
- [Miraflow — duct-tape explainer](https://miraflow.ai/blog/openai-duct-tape-model-explained-gpt-image-2-already-here-terrifying)
- [Miraflow — Arena testing guide](https://miraflow.ai/blog/how-to-use-duct-tape-ai-model-arena-gpt-image-2-guide)
- [@aisocity Threads (2026-04-04, leak post)](https://www.threads.com/@aisocity/post/DWtLdcMjOOf/open-ais-new-image-model-gpt-image-has-leaked-it-seems-to-have-extremely-good)

**Hands-on / independent review**:
- [Simon Willison — gpt-image-2](https://simonwillison.net/2026/Apr/21/gpt-image-2/) — raccoon test, 3840×2160 $0.40 datapoint

**Community curation**:
- [awesome-gpt-image (ZeroLu)](https://github.com/ZeroLu/awesome-gpt-image/) — prompt-pattern repo
- [Latent Space AINews](https://www.latent.space/p/ainews-openai-launches-gpt-image)

**Failed fetches** (명시):
- OpenAI announcement page — 403 전부
- VentureBeat 본문 — 429 반복
- Startup Fortune — 403
- Axios — 403
- DEV.to ji_ai duct-tape post — 404 (URL revised)
