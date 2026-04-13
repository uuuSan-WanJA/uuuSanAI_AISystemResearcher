---
title: Superpowers — 한 번 이해하고 가기
based_on: notes/harness/superpowers.md
date: 2026-04-13
audience: user (Korean)
reading_time: ~8분
---

# Superpowers — 에이전트에게 방법론을 강제하는 플러그인

## 한 줄로

> "Skills are what give your agents Superpowers." — Jesse Vincent, 2025-10-09

Superpowers 는 Jesse Vincent (github: `obra`) 가 2025년 10월 9일 공개한 Claude Code 플러그인이다. 본질은 단순하다. `SKILL.md` 파일 묶음 + 부트스트랩 시스템 프롬프트로, **brainstorm → spec → plan → TDD → subagent dev → review → finalize** 라는 7단계 파이프라인을 에이전트에게 강제로 태우는 것. 제목이 과장 같지만, 내부는 "더 똑똑한 모델이 아니라 방법론 레이어를 얹자" 는 수수한 주장이다.

## 왜 태어났는가

Vincent 의 진단은 Ralph 와 다르다. Ralph 가 "컨텍스트 관리" 문제를 친다면, Superpowers 는 **디시플린 부재** 문제를 친다. 바닐라 Claude Code 는 빠르지만 전문가 관행을 전부 스킵한다는 것. 테스트 먼저 쓰지도 않고, 디자인 승인 없이 코드를 뽑고, 리뷰 없이 커밋한다.

> "I've spent the past couple of weeks working on a set of tools to better extract and systematize my processes and to help better steer my agentic buddy." — Vincent, 2025-10-09

3자 관찰자 Ewan Mak (Medium, 2026-04) 는 이를 더 날카롭게 요약한다: **"Impose a strict development methodology and output quality stabilizes."** Superpowers 는 프로세스 디시플린을 **제약**으로 부과하는 하네스이지, Ralph 처럼 컨텍스트를 리셋하는 하네스가 아니다.

## 실제로 어떻게 돌아가는가

한 프로젝트를 돌릴 때 일어나는 일을 번호로 보면:

1. 세션 시작 시 `SessionStart` hook 이 `using-superpowers` meta-skill 을 `<EXTREMELY_IMPORTANT>` 블록으로 컨텍스트에 직접 주입한다 (DeepWiki). on-demand 가 아니다.
2. **Brainstorming** 스킬이 질문으로 디자인을 뽑고 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` 로 저장. 사용자 승인이 떨어질 때까지 구현 금지.
3. **Writing-plans** 스킬이 플랜을 **2–5분 단위 bite-sized 태스크**로 쪼갠다.
4. **Subagent-driven-development** — 구현은 상위 히스토리를 상속하지 않는 독립 컨텍스트 서브에이전트가 "exactly what they need" 만 받아서 수행.
5. **TDD** 스킬이 RED → GREEN → REFACTOR 를 강제. 테스트보다 먼저 쓴 코드는 **지우라**고 명시.
6. **Code review** 단계에서 severity 기반 블로킹. v5.0.4 부터 리뷰 루프 상한 5 → 3.
7. **Finishing-a-development-branch** 스킬이 merge/PR 결정.

각 페이즈 사이에는 `<HARD-GATE>` 라는 XML 스타일 태그가 박혀 있다. `brainstorming/SKILL.md` 에 실제로 이렇게 쓰여 있다:

> ```
> <HARD-GATE>
> Do NOT invoke any implementation skill, write any code, scaffold any project,
> or take any implementation action until you have presented a design and the
> user has approved it.
> </HARD-GATE>
> ```

그리고 또 하나의 기이한 선택: **프로세스의 권위적 표현을 GraphViz DOT 플로우차트로 쓴다**. 프로즈는 DOT 를 부연하는 보조다. Vincent 는 v4 포스트(2025-12-18)에서 명시적으로 선언한다.

> "Claude is particularly good at following processes written in dot." — Vincent, 2025-12-18

## 왜 작동한다고 (Vincent 는) 주장하는가

Superpowers 의 증거는 Ralph 와 비슷하게 대부분 일화지만, 질적으로 더 단단한 실물 아티팩트가 하나 있다: Vincent 본인이 유지보수하는 **chardet 7.0.0** 릴리스 (2026-03-04). byteiota 기사 인용 기준 **41배 성능 개선, 정확도 94.5% → 96.8%**. Superpowers 루프로 만든 것. 이게 가장 많이 인용되는 사례다.

나머지는 Ralph 의 증거 패턴과 비슷하다:

- Vincent: "Claude went _hard_... it would strengthen the instructions... after each failure" — 프레임워크 자체가 실패로부터 자기 프롬프트를 강화한다는 주장 (2025-10-09)
- byteiota: 테스트 커버리지가 85~95% 로 점프한다. 프레임워크가 테스트 스킵을 차단하니까
- byteiota: "4명 × 6개월 프로젝트를 1인 2개월" — 출처 불명확한 주장이라 주의

통제된 벤치마크는 없다. Ewan Mak 은 정성적으로 "autonomous multi-hour sessions viable" 이라고 평가한다.

## 진짜 핵심 아이디어 하나

Superpowers 를 "TDD 를 강제하는 프레임워크" 로 이해하면 표면만 본 것이다. 노트를 관통하는 진짜 주장은 이것이다:

**스킬(SKILL.md) 을 발견 가능·설명 가능·테스트 가능한 자기완결 유닛으로 표준화했다는 것.**

각 스킬은 `name + description + when-to-use + DOT flowchart + HARD-GATE + prose` 라는 고정 구조를 가진다. v4 에서 Vincent 는 **description 에는 "언제 쓰는지" 만 넣는다** 는 규칙을 못 박는다 — "본문의 how 를 description 에 노출하면 모델이 읽지 않고 짐작한다." discovery 와 body 를 분리한 정보 아키텍처 결정이다.

그리고 `writing-skills` 라는 meta-skill 이 존재한다. 즉 **스킬을 쓰는 것도 하나의 스킬**이고, 사용자가 실패를 관찰하면 새 스킬을 TDD 방식으로 추가할 수 있다. Vincent 표현으로 "Writing skills IS Test-Driven Development applied to process documentation."

Ralph 가 "작은 컨텍스트 창으로 쪼개라" 는 멘탈 모델을 남겼다면, Superpowers 는 **"프로세스를 재사용 가능한 유닛으로 결정화하라"** 는 멘탈 모델을 남긴다.

## 가져갈 만한 것들

딥다이브 노트 §11 에 13개의 이식 가능한 primitive 가 정리돼 있다. 그중 가장 쓸만한 것들:

1. **HARD-GATE 태그** — `<HARD-GATE>` 한 문장으로 진전 차단. 모델 의존적이지만(Claude 에서만 검증) 태그 이름은 컨벤션일 뿐이라 교체 자유.
2. **When-only skill descriptions** — 스킬 description 은 "언제 쓰는지" 만. 본문의 how 를 description 에 노출하면 에이전트가 본문을 읽지 않고 짐작한다. 매우 이식성 높은 정보 아키텍처 원칙.
3. **Design approval gate before any implementation** — 가장 이식성 높은 primitive. 플러그인 없이도 시스템 프롬프트 한 줄로 재현 가능.
4. **2–5분 bite-sized tasks** — Ralph 의 "carve off small independent context windows" 와 **수렴한다**. 두 하네스가 독립적으로 같은 결론에 도달했다는 증거.
5. **Subagent 로 구현 분리, 코디네이터 컨텍스트는 오케스트레이션 전용** — 단 비용/지연 trade-off 큼 (뒤에 실패 모드 참고).
6. **Status-coded subagent outcomes** (`DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED`) — 서브에이전트 리턴을 enum 화해 코디네이터 분기 로직을 결정론화.

DOT 플로우차트 자체는 이식 가능하지만 "Claude 에서만 검증됨" 이라는 단서가 붙는다. 다른 모델에는 A/B 필요.

## 조심할 것

Superpowers 의 실패 모드는 **Vincent 자신의 로드맵 reversal** 에 가장 잘 드러난다. 릴리스 노트를 읽으면 긴장 지점이 보인다:

- **v5.0.6 (2026-03-24) 인라인 리뷰 회귀**: "Inline Self-Review Replaces Subagent Review Loops — removed expensive review delegation in favor of integrated checklists." 즉 서브에이전트 리뷰가 **비용 때문에 감당 불가**였다는 자인. 가장 자랑하던 설계 중 하나가 롤백된 셈.
- **v5.0.4 리뷰 루프 상한 하향**: max iterations 5 → 3. 리뷰어 서브에이전트가 지나치게 블로킹하는 경향을 보정.
- **v5.0.5 user choice 복원**: 서브에이전트 강제가 비용 이슈를 일으켜 인라인/서브에이전트 **둘 다 선택지로 유지**로 후퇴.

3자 관찰 중 눈여겨 볼 것:

- Ewan Mak: "Superpowers' interactive prompts blocking Claude Code's input stream" — 다른 프레임워크와 합성 시 발생하는 실패 모드.
- byteiota 기사는 **부정적 사례를 의도적으로 누락**한다. 강제 TDD 가 실제로 속도를 저하시키는지에 대한 1차 사례는 현재 공개된 자료에 거의 없다. 긍정 bias 경고.
- **Brainstorm server** (WebSocket 기반 visual companion, v5.0.0 도입) 가 Windows/MSYS2 에서 불안정 → v5.0.5 에서 Owner-PID 모니터링 Windows 비활성화. 크로스 플랫폼 성숙도 이슈.
- DOT 플로우차트의 **Claude-specificity**: Vincent 본인이 "Claude is particularly good at" 이라고 표현했다. Gemini/GPT 에서의 준수도는 미검증.

그리고 가장 큰 설계 긴장: **스킬 수 폭발**. v4 에서 이미 Vincent 가 "consolidate skills" 결정을 내렸다 (`test-driven-development` 가 `testing-anti-patterns` 를 흡수, 등). 스킬 시스템은 자라면 자체 거버넌스가 필요해진다.

## 어디에 쓰고 어디에 쓰지 말까

**쓸만한 영역**
- 품질·규율이 속도보다 중요한 그린필드 또는 중형 라이브러리
- TDD 가 실제로 말이 되는 프로젝트 (테스트 가능한 단위가 명확)
- 장시간 자율 세션을 돌리되 디자인/리뷰 게이트에 사람이 관여할 여유가 있는 환경
- Claude Code (+ 확장적으로 Cursor/Codex/OpenCode) 런타임

**쓰면 안 되는 영역 / 주의**
- 저사양·저예산 환경 — 서브에이전트 리뷰가 비용을 넘는다 (v5.0.6 회귀가 증거)
- 대규모 legacy 코드베이스 — Vincent 사례는 그린필드/중형 라이브러리 위주, HARD-GATE 가 병목 될 가능성
- Non-Claude 모델 — DOT 플로우차트와 anti-rationalization 프로즈의 효과가 미검증
- 탐색적·실험적 작업 — 디자인 승인 게이트 자체가 과한 오버헤드

## 한국어 독자를 위한 참고

한국어 자료는 현재 제한적이다. 영어권에서는 heyuan110 블로그의 "bilingual" 프레이밍 — Superpowers 는 execution quality, OpenSpec 은 decision traceability, 둘을 병용하라는 — 이 가장 실용적인 합성 가이드다. Superpowers 를 단독으로 쓰기보다 **디자인 거버넌스 도구와 짝짓는** 패턴을 염두에 둘 것.

## 더 읽을거리

- **Vincent 본인** — [공개 원글](https://blog.fsck.com/2025/10/09/superpowers/), [v4 (DOT 도입)](https://blog.fsck.com/2025/12/18/superpowers-4/), [조상 포스트](https://blog.fsck.com/2025/10/05/how-im-using-coding-agents-in-september-2025/)
- **레포·1차** — [obra/superpowers](https://github.com/obra/superpowers), [RELEASE-NOTES.md](https://github.com/obra/superpowers/blob/main/RELEASE-NOTES.md), [brainstorming SKILL.md (HARD-GATE verbatim)](https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md), [marketplace PR #148](https://github.com/anthropics/claude-plugins-official/pull/148)
- **실전 재현 / 사례** — [byteiota: chardet 41x](https://byteiota.com/superpowers-82k-stars-transform-claude-code-senior-dev/), [heyuan110 deep dive](https://www.heyuan110.com/posts/ai/2026-02-01-superpowers-deep-dive/)
- **비판 / 비교** — [Ewan Mak: Superpowers vs GSD vs gstack](https://medium.com/@tentenco/superpowers-gsd-and-gstack-what-each-claude-code-framework-actually-constrains-12a1560960ad), [OpenSpec × Superpowers 병용](https://www.heyuan110.com/posts/ai/2026-04-09-claude-code-openspec-superpowers/), [Rick Hightower 4-프레임워크 비교](https://medium.com/@richardhightower/the-great-framework-showdown-superpowers-vs-bmad-vs-speckit-vs-gsd-360983101c10)
- **기판** — [Anthropic Agent Skills (2025-10-16)](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## 한 문장으로 덮기

Superpowers 는 TDD 프레임워크가 아니라 **"프로세스 디시플린을 SKILL.md 라는 재사용 가능한 유닛으로 결정화한다"** 는 베팅이고, 그 베팅의 비용은 v5.0.6 롤백이 솔직하게 보여준다.
