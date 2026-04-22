---
title: Format-native community curation primitive
date: 2026-04-22
based_on:
  - notes/harness/claude-design.md
  - notes/harness/gpt-image-2.md
  - digests/2026-04-22-design-layer-twin-launches.md
  - notes/techniques/anthropic-* (skill ecosystem 배경)
confidence: medium
tags: [curation, community, skills, primitives, awesome-list, carve-out]
---

## 한 줄 요약

AI 제품을 둘러싼 커뮤니티 큐레이션이 **"프롬프트 문자열 목록"** (awesome-chatgpt-prompts, langgptai/awesome-claude-prompts) 에서 **"포맷-네이티브 primitive 아티팩트 라이브러리"** (DESIGN.md 템플릿, Skill 파일, MCP 설정, hooks, agent-orchestrator 정의) 로 시프트하고 있으며, 이 새로운 형태는 **제품의 1차 문서보다 커뮤니티 재현성을 더 높인다**.

---

## 패턴 / 주장

"awesome-X" 자체는 2014년 sindresorhus 의 원형 이후 AI 도구에 광범위하게 적용돼온 오래된 패턴이며, **AI 제품 런칭에 따라 awesome-X repo 가 수일 내 등장하는 것 자체는 novel 하지 않다**. 실제로 awesome-chatgpt-prompts (2022), langgptai/awesome-claude-prompts, hesreallyhim/awesome-claude-code (2025), AwesomeCursorPrompt, awesome-ai-system-prompts, system-prompts-and-models-of-ai-tools 등 프롬프트 문자열 큐레이션 repo 는 이미 수백 개 존재한다.

**Novel 한 subpattern 은 큐레이션의 구조적 단위가 바뀐다는 것**이다. 2026년 봄 들어 관찰되는 시프트:

### 시프트 1 — 프롬프트 문자열 → 재현 가능한 아티팩트 파일

rohitg00/awesome-claude-design 은 단순 링크/프롬프트 나열이 아닌 **DESIGN.md 템플릿** 을 aesthetic family (9개: Linear, Warp, Claude, ClickHouse, RunwayML, Figma, Arc, The Verge, indie) 별로 정리하고, swatch + typography + reference link 를 구조화된 metadata 로 제공한다. 사용자가 `DESIGN.md` 를 Claude Design 프로젝트에 첨부하면 의도가 결정론적으로 재현된다.

구조적 슬롯 (README 기준 14 section):
- Feature Map / Launch Timeline / Official Resources
- **X Signal** — 커뮤니티 파워유저 데모 모음
- **DESIGN.md by Aesthetic Family** — 9 families × ~4-5 brands
- **Remix Recipes** — "Linear × Claude" 같은 조합 specification
- **Prompt Packs** — `/prompts/` 디렉토리의 before/after 예시
- **Anti-Slop Kit** — Claude Design 의 "container soup" 문제 대응 프래그먼트
- Skills & Plugins / Workflows & Recipes / Video Teardowns
- Comparisons / Showcase / Community Takes / FAQ / Related OSS

이것은 **링크 dump 가 아니라 제품 사용을 위한 mini-manual** 이다.

### 시프트 2 — 단일 카테고리 → 다종 primitive 번들

rohitg00/awesome-claude-code-toolkit 은 문자열/링크가 아닌 **실행 가능한 primitive 단위들의 번들**로 자신을 소개:

> *"135 agents, 35 curated skills (+400,000 via SkillKit), 42 commands, 176+ plugins, 20 hooks, 15 rules, 7 templates, 14 MCP configs, 26 companion apps, 52 ecosystem entries"* ([README](https://github.com/rohitg00/awesome-claude-code-toolkit))

각 단위는 Claude Code 생태계의 **포맷-네이티브 primitive** (skill, slash command, plugin, hook, MCP server config) 와 직접 매핑된다. 이는 전통적 awesome-list 가 URL 링크의 집합인 것과 **구조적으로 다른 카테고리**다.

### 시프트 3 — 결과: 1차 문서 대비 재현성 역전

Anthropic 공식 `claude.com/docs` 는 Claude Code 의 skill 생태계·hook·MCP 설정 · agent orchestrator 에 대해 reference document 만 제공한다. 반면 awesome-claude-code-toolkit 은 재현 가능한 구성 단위 수백 개를 실제 파일로 제공한다. 사용자 입장에서 **"Claude Code 로 X 를 하려면 무엇부터 시작해야 하는가"** 의 answer surface 가 1차 문서에서 커뮤니티 큐레이션으로 이동.

같은 역학이 gpt-image-2 에는 **아직 발생하지 않음**: ZeroLu/awesome-gpt-image 는 전통적 prompt gallery (8 카테고리 × 40+ 프롬프트 문자열 + 결과 이미지) 로 awesome-chatgpt-prompts 2022 패턴에 머묾. 이는 **gpt-image-2 의 primitive 표면이 단일 API endpoint 이기 때문** — 커뮤니티가 큐레이션할 구조화된 slot 이 없음 (Claude Code 처럼 skill / hook / plugin / MCP 같은 다종 primitive 가 없음).

---

## 근거가 되는 관찰

**Novel 구조화 curation 의 직접 사례 (2 사례, 같은 작성자 discount 포함)**:
- `rohitg00/awesome-claude-design` — DESIGN.md templates + aesthetic family + anti-slop kit. Claude Design 런칭 (2026-04-17) 후 수일 내 등장. 14 README 섹션.
- `rohitg00/awesome-claude-code-toolkit` — 135 agents / 35 skills / 42 commands / 176 plugins / 20 hooks / 15 rules / 7 templates / 14 MCP configs 구조화 번들.

**같은 작성자 이슈**: 위 두 사례가 동일 작성자(rohitg00)이므로 **독립 사례 카운트에서는 1.5 사례로 환산**해야 한다. 진짜 독립 사례 확보까지 confidence 보류.

**과도기적 (structured 요소 + 링크 dump 혼재) 사례**:
- `hesreallyhim/awesome-claude-code` (2025) — skills/hooks/slash-commands/agent-orchestrators/plugins 카테고리로 정리된 링크 리스트. **카테고리는 포맷-네이티브** 이지만 내용은 여전히 외부 링크. 시프트의 중간 단계.
- `jqueryscript/awesome-claude-code` — tool/IDE 통합/framework 카테고리. 비슷한 transitional 상태.

**전통적 패턴 대조군 (시프트 발생 *전*)**:
- `f/awesome-chatgpt-prompts` (2022) — 순수 prompt 문자열 리스트. GitHub star 기준 장르 원형.
- `langgptai/awesome-claude-prompts` — Claude 대상 prompt 문자열 모음.
- `legendyxu/AwesomeCursorPrompt` — Cursor Composer prompt 템플릿.
- `dontriskit/awesome-ai-system-prompts` — ChatGPT/Claude/Perplexity/Manus/Claude-Code/Lovable/v0/Grok/same.new/windsurf/notion/MetaAI 시스템 프롬프트 **원본 덤프**. 구조적 slot 없음 — 단지 각 제품의 leaked system prompt 모음.
- `ZeroLu/awesome-gpt-image` — 전통 pattern. gpt-image-2 용 prompt gallery.

**대조군 해석**: 공존하는 전통 패턴 repo 가 다수 존재함 → novel subpattern 은 **대체가 아닌 추가**이며, **primitive 표면이 다양한 제품에서만 발생**한다.

---

## 구성 요소 (이식 가능한 단위)

novel 큐레이션 repo 에서 반복 등장하는 구조적 slot:

1. **포맷-네이티브 템플릿 디렉토리** — 제품의 primitive 를 직접 저장하는 파일들. 예: `DESIGN.md`, `SKILL.md`, `CLAUDE.md`, `skill.json`, `.mcp/config.json`, `agent.yaml`
2. **조합 recipe** — 여러 템플릿을 조합하는 지침. 예: "Linear × Claude" aesthetic remix, multi-agent orchestration 배치
3. **Anti-pattern 프래그먼트** — 제품의 알려진 실패 모드 대응 (Claude Design 의 "container soup" 에 대한 "Anti-Slop Kit")
4. **카테고리별 inventory counts** — "X 종 skill, Y 종 plugin, Z 종 MCP config". 큐레이터가 1차 문서보다 더 comprehensive 함을 주장하는 수사적 장치
5. **Launch timeline + X signal** — 제품 런칭 직후 커뮤니티 파워유저 데모를 구조화 기록. 2차 문헌의 아카이브 역할
6. **Comparison matrix** — 경쟁 제품 대비 정리. 1차 벤더가 못 하는 역할 (conflict of interest)

이 6가지 slot 중 3~4개 이상이 동시에 존재하면 "포맷-네이티브 큐레이션" 으로 분류.

---

## 파생 효과 / 함의

### 벤더-커뮤니티 관계의 재설계

1차 벤더 (Anthropic, OpenAI) 의 공식 문서가 구조화된 primitive 의 **reference spec** 을 제공하면, 커뮤니티가 **사용 가능한 instance** 들을 생산한다. Spec ↔ Instance 분업이 발생. 벤더 입장에서:
- 장점: 문서 작성 부담 감소, 생태계 확장
- 위험: 커뮤니티 instance 가 사실상 표준이 되면 공식 방향성 통제 상실 (Claude Code 의 custom skill 로 재정의된 "Claude Code 경험" 이 Anthropic 의도와 divergence 가능)

### 제품 타입 의존성 — primitive surface 부재 시 시프트 미발생

gpt-image-2 가 시프트를 트리거하지 못한 이유 추론:
- **Primitive surface 단순함**: image/text input → image output 단일 API. 커뮤니티가 큐레이션할 구조화된 slot 없음.
- **비교**: Claude Code 는 skill / hook / slash command / MCP server / agent / plugin 6+ primitive 표면. 큐레이션 slot 이 풍부.

→ **Primitive surface 의 다양성이 novel curation 의 precondition**. 제품이 구조적으로 "API" 에 머물면 전통적 prompt-string curation 외에는 생길 수 없다.

### Rapid coalescence 의 의미

awesome-claude-design 이 런칭 수일 내에 14-section README 와 9 aesthetic family 로 정리된 것은 **파워유저 집단이 런칭 전부터 `frontend-design` skill 을 사용해왔기 때문**으로 가장 잘 설명된다. choi.openai 의 2025-10 Threads 포스트가 동일 skill 을 다룬 것과 일관 — Claude Design 은 기존 skill 의 productization 이고, awesome-claude-design 은 skill 사용자 집단의 기존 지식을 제품 브랜드로 재라벨링.

→ **Novel curation 의 등장 속도는 1차 벤더 런칭 속도보다 기존 파워유저 그룹의 집단 지식 축적도에 더 의존**.

---

## 현재 confidence 와 미결 질문

**Confidence: medium**. 이유:
- Novel 구조화 curation 의 직접 사례가 2건이지만 동일 작성자 (rohitg00) → 독립 사례로는 1.5건.
- 과도기 사례 (hesreallyhim, jqueryscript) 는 시프트를 부분적으로만 보여줌.
- 2026-04 시점 관찰 — 시간의 검증 (6개월 내 지속되는지) 필요.

**Promotion 트리거**:
- **독립 작성자의 novel-structured curation repo 추가 1건** 확보 시 medium → medium-high. 후보:
  - Figma Make / Figma Weave 용 curation 이 DESIGN.md 형식을 차용하면 강한 증거
  - Lovable / Bolt 용 curation 이 "component templates + recipe" 구조로 등장하면 중간 증거
  - Midjourney v8.1 의 3D mesh feature 용 curation 이 `.glb` 템플릿 카탈로그 형식으로 등장하면 구조적 확장
- **과도기 사례의 구조화 심화 관찰**: hesreallyhim/awesome-claude-code 가 시간이 지나면서 링크 리스트 → 파일 번들로 전환되는지 모니터링.

**미결 질문**:
1. DESIGN.md 템플릿이 Anthropic 1차 문서에 흡수되는가, 아니면 계속 커뮤니티 surface 에 머무는가? 흡수 시 벤더-커뮤니티 분업의 결과.
2. rohitg00 의 두 toolkit 이 단일 개인의 brand-building 인가, 아니면 반복 가능한 큐레이션 디자인 패턴인가? 작성자 인터뷰 / 다른 contributor 의 유사 repo 등장 여부로 판별.
3. **Primitive surface 가 풍부한 제품**에서만 novel curation 이 발생하는가? OpenAI 가 Codex / ChatGPT 에 plugin / skill / hook 계열 primitive 를 도입하면 gpt-image-2 용 novel curation 이 뒤따라 등장할지 예측 가능.

---

## 본 프로젝트 corpus 와의 연결

### 스키마 축

- **신규 축 후보**: **"curation-primitive-surface-richness"** — 제품의 primitive 표면 개수 · 타입 다양성이 novel 큐레이션 등장의 precondition. 현재 확인: Claude Code (6+ primitives → novel curation), gpt-image-2 (1 primitive → 전통 curation only). 2 사례 확보. 3번째 (Codex plugin 생태계 확장 후 관찰) 에서 promotion 가능.
- **기존 축 보강**: Δ1 provenance subtype 의 "skill-productization" 후보 (Claude Design 이 `frontend-design` skill 의 productization) 와 **같은 skill 이 community curation 의 구조적 단위로도 기능** — 하나의 skill 이 두 방향 (벤더 제품화 + 커뮤니티 큐레이션) 으로 branch 하는 패턴.

### Insight card 가족

- `primitive-knowledge-layer-design-space.md` — 지식 레이어 (builder / storage / timing 3축). 본 카드의 "포맷-네이티브 primitive" 와 **직교** — 큐레이션은 지식 레이어의 소비 surface.
- `knowledge-lifecycle-operations.md` — structural/semantic lint 등 운영 차원. 본 카드와 **상호 보완** — 큐레이션이 lint 의 데이터 소스가 될 수 있음 (awesome-* repo 의 카테고리 오탑재가 structural lint 대상).

### 후속 데이터 수집 우선순위

1. Figma Make 의 awesome-* 등장 여부 모니터링 (3~6개월)
2. rohitg00 외 독립 작성자의 novel-structured curation repo 탐색 — GitHub topics `skills`, `design-tokens`, `agent-orchestrator` 검색
3. OpenAI 가 Codex plugin 생태계 확장 시 curation repo 패턴 관찰

---

## Source list

**Primary (novel 구조화 사례)**:
- [rohitg00/awesome-claude-design](https://github.com/rohitg00/awesome-claude-design)
- [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit)

**Transitional (부분 구조화)**:
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [jqueryscript/awesome-claude-code](https://github.com/jqueryscript/awesome-claude-code)

**Traditional (대조군 — prompt string only)**:
- [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) — 2022 장르 원형
- [langgptai/awesome-claude-prompts](https://github.com/langgptai/awesome-claude-prompts)
- [legendyxu/AwesomeCursorPrompt](https://github.com/legendyxu/AwesomeCursorPrompt)
- [dontriskit/awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts)
- [ZeroLu/awesome-gpt-image](https://github.com/ZeroLu/awesome-gpt-image)
- [x1xhlol/system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)

**Related deep-dives**:
- [`notes/harness/claude-design.md`](../notes/harness/claude-design.md) — `frontend-design` skill 의 productization
- [`notes/harness/gpt-image-2.md`](../notes/harness/gpt-image-2.md) — primitive surface 단일성
- [`digests/2026-04-22-design-layer-twin-launches.md`](../digests/2026-04-22-design-layer-twin-launches.md) — 두 런칭의 구조적 비교
