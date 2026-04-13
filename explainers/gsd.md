---
title: GSD (Get Shit Done) — 한 번 이해하고 가기
based_on: notes/harness/gsd.md
date: 2026-04-13
audience: user (Korean)
reading_time: ~8분
---

# GSD — 컨텍스트 로트를 파일과 서브에이전트로 분해하는 하네스

## 한 줄로

> `/gsd:discuss-phase 1` → `/gsd:plan-phase 1` → `/gsd:execute-phase 1` → `/gsd:verify-work 1` → `/gsd:ship`

GSD(Get Shit Done)는 이 5단계 슬래시 명령 체인이 전부다. 각 단계는 `.planning/` 디렉토리 아래 구조화된 Markdown 파일 세트를 읽고 쓰면서, 매 실행 태스크를 **프레시 200K 토큰 서브에이전트**로 카브오프(carve-off)해 넘긴다. 저자는 Lex Christopherson(TÂCHES / @official_taches). 사용자 힌트에는 "jasonkneen"으로 나와있었지만, 1라운드 확인 결과 사실이 아니다 — 원본 레포는 `glittercowboy/get-shit-done`이었고 현재는 `gsd-build/get-shit-done`으로 옮겨졌다.

## 왜 태어났는가

GSD가 적으로 지목한 것은 단 하나, **context rot** — 컨텍스트 창이 차면서 Claude의 품질이 무너지는 현상이다. README는 이렇게 말한다.

> "Solves context rot — the quality degradation that happens as Claude fills its context window."

TÂCHES 본인의 포지셔닝은 더 직설적이다. "I'm a solo developer. I don't write code — Claude Code does." 그리고 "Other spec-driven development tools exist...but they all seem to make things way more complicated than they need to be (sprint ceremonies, story points, stakeholder syncs, retrospectives, Jira workflows)" — BMAD-METHOD의 "에이전트 팀"이나 Spec Kit의 체계 같은 엔터프라이즈 리추얼을 명시적으로 거부한다.

Ewan Mak(tentenco, 2026-04 Medium)은 세 프레임워크를 이렇게 요약했다: **"Superpowers는 개발 프로세스를, GSD는 실행 환경을, gstack은 의사결정 관점을 제약한다."** GSD가 관심 있는 것은 모델이 *어떻게 생각하는가*가 아니라 모델이 *어떤 환경에서 동작하는가*다.

## 실제로 어떻게 돌아가는가

한 번의 "페이즈" 진행이 어떻게 흘러가는지가 핵심이다. 예를 들어 Phase 1을 돌린다고 하면:

1. `/gsd:new-project` 로 `.planning/PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md`, `config.json`을 생성한다. 인터뷰 → 리서치 → 요구사항 → 로드맵 순
2. `/gsd:discuss-phase 1` 이 **사용자에게 구조화 질문**(`AskUserQuestion` 툴)을 던져 회색 영역을 수면 위로 올리고 결정을 `1-CONTEXT.md`에 고정한다
3. `/gsd:plan-phase 1` 이 `gsd-planner` 서브에이전트를 스폰해 리서치를 돌리고, 웨이브 단위로 `1-0.1-PLAN.md`, `1-0.2-PLAN.md` 원자 태스크 파일들을 만든다
4. `/gsd:execute-phase 1` 은 각 플랜을 받아 `gsd-executor` 서브에이전트를 **`Task()` 툴로 신선한 200K 컨텍스트에** 스폰한다. 의존성이 없는 플랜은 같은 웨이브에서 병렬, 의존 플랜은 다음 웨이브로 밀린다. 각 executor는 결과를 `1-0.1-SUMMARY.md`에 쓴다. 오케스트레이터 세션은 구현 디테일을 **절대 보지 않는다** — 서머리만 읽는다
5. `/gsd:verify-work 1` 이 `gsd-verifier`를 스폰해 REQUIREMENTS.md와 SUMMARY를 비교하는 goal-backward 체크리스트를 돌리고 `1-VERIFICATION.md`에 ✓/✗/? 를 기록한다. 실패 시 rework / accept-with-caveats / rollback 세 옵션을 제안
6. `/gsd:ship` 으로 PR 생성, `/gsd:complete-milestone`으로 태그

핵심 파일 명명 규약은 `{PHASE}-{WAVE}-{TYPE}.md` — `1-0.2-PLAN.md`는 Phase 1, Wave 0.2, PLAN 아티팩트다. 이 이름 자체가 사람·오케스트레이터·서브에이전트·`gsd-tools.cjs` Node 유틸 모두가 같은 regex로 파싱하는 일종의 RPC 프로토콜이다. Felix Abele(codecentric, 2026-03)가 인용한 설계 원칙이 이 구조의 이유를 압축한다:

> "Deterministic logic belongs in code, not in prompts."

번호 파싱, git 커밋, 페이즈 전이 같은 결정론적 연산은 LLM에서 빼내 Node 유틸로 밀어내고, LLM에는 판단만 시킨다.

## 왜 작동한다고 (TÂCHES는) 주장하는가

증거의 결은 Ralph와 비슷하다. 통제된 벤치마크는 없고, 자기주장 + 소셜 증거 + 일화가 섞여 있다.

- README: "trusted by engineers at Amazon, Google, Shopify, and Webflow" (1차 출처 불명)
- Lex 본인 X 트윗: "A month ago, I launched GSD. 8.5k+ GitHub stars later, it's become the #1 Claude Code framework for vibe coding successfully" (2026 초, search snippet 기반 — 본문은 로그인 월)
- `gsd-build/get-shit-done` 레포: 2026-04 기준 **51.7k stars / 4.3k forks**. Superpowers(94k) 다음 2위 규모
- codecentric: "currently among the most well-known Spec-Driven Development tools" — 정성 평가
- dev.to 알리카즈미: "4:1 token overhead ratio" — 플래닝 오버헤드 추정, 방법론 불명

GSD가 주장하는 작동 메커니즘 자체는 관찰 가능하다. 커뮤니티 안에서 "오케스트레이터 세션이 30-40% 컨텍스트 사용률로 유지된다"는 보고가 반복된다. 반대 주장, 즉 "프레시 카브오프가 무의미하다"는 반박은 Phase 1 탐색에서는 발견하지 못했다.

## 진짜 핵심 아이디어 하나

표면적으로 GSD는 "슬래시 명령 한 뭉치"지만 진짜로 이식해야 할 것은 아키텍처다. Ralph의 Dex가 "Ralph의 요점은 무한 루프가 아니라 독립 컨텍스트 창으로 쪼개는 것"이라고 했던 것과 정확히 같은 원리가 GSD에서는 **시간이 아니라 공간 축**으로 구현된다.

Ralph는 `while true`로 **다음 루프**에서 프레시 컨텍스트를 얻는다. GSD는 **지금 이 순간 Task()로 서브에이전트를 분기**해서 프레시 컨텍스트를 얻는다. 같은 멘탈 모델의 두 가지 구현. 오케스트레이터 세션은 구현 디테일에 오염되지 않기 위해 서머리만 읽고, executor 서브에이전트는 플랜 하나와 관련 요구사항 슬라이스만 본다. 이 비대칭이 GSD 전체를 설명한다.

tentenco의 요약이 같은 것을 다른 각도에서 찍는다:

> "gstack handles thinking, Superpowers handles doing, GSD keeps long context honest."

## 가져갈 만한 것들

GSD 딥다이브 노트 §11에 12개 원시요소가 정리돼 있다. 가장 쓸만한 6개를 간추리면:

1. **`.planning/` 역할별 분해** — `PROJECT.md`(비전), `REQUIREMENTS.md`(ID 기반 추적), `ROADMAP.md`(순서), `STATE.md`(지금 여기), `config.json`(워크플로 토글). 각 파일은 단일 책임. Ralph의 "플랜 1개 + 운영 1개" 모델의 일반화 버전
2. **`{PHASE}-{WAVE}-{TYPE}.md` 네이밍 프로토콜** — 파일명이 프로세스 이벤트 로그. 에이전트 간 RPC 계약 역할. 규약만 지키면 어떤 런타임에서도 이식 가능
3. **Task() 기반 프레시 200K 카브오프** — 오케스트레이터는 서머리만, executor는 플랜 하나만. 서브에이전트 스폰 API가 있는 런타임에서는 즉시 재현 가능
4. **웨이브 병렬 + 의존성 그래프** — `parallelization: true/false` 토글 + 플랜의 `dependencies` 필드. 탐색은 빠르되 상태 변경은 직렬화하는 Ralph의 N:1 백프레셔와 다른 형태의 같은 원리
5. **Deterministic logic는 code, not prompts** — 번호 파싱·git·페이즈 전이는 `gsd-tools.cjs` Node 유틸로. LLM에는 판단만. 가장 일반화하기 쉬운 원칙이자 가장 자주 무시되는 원칙
6. **페이즈별 명시적 allow-list** — 각 워크플로 파일 프론트매터에 `allowed-tools: [Read, Bash, Write, Task, AskUserQuestion]`. Ralph의 `--dangerously-skip-permissions`와 정반대 포지션이다

비주류지만 눈에 띄는 둘: `/gsd:quick`("Add dark mode" 수준 태스크의 escape hatch)과 `/gsd:map-codebase`(brownfield 위에 얹을 때의 전처리). Ralph가 "그린필드 전용"인 것과 대비되는 설계 결정들이다.

## 조심할 것

GSD는 자기 아키텍처의 약속을 실제로 위반하는 실패 모드들을 기록해뒀다. 이슈 트래커가 가장 좋은 소스다.

- **`--auto` 구현 오류** (이슈 #780) — 서브에이전트들이 페이즈 핸드오프를 따르지 않고 자기 자신이 모든 페이즈를 수행. "fresh context와 compaction 보호라는 에이전트 아키텍처의 목적을 무력화"시킨다. 이건 **치명적** — GSD의 핵심 약속이 깨지는 실패
- **HITL 자동응답 회귀** (이슈 #803) — v1.21→1.22 업데이트에서 `/gsd:discuss-phase`의 모든 질문이 자동으로 응답됨. 구조화 질문 툴이 HITL 채널 역할을 하는 설계에서 채널이 고장나면 워크플로 전체가 쓰레기를 자동 승인한다
- **Claude Code 2.1.88+ 호환 붕괴** (이슈 #218, #1504, #1528) — Claude Code가 스킬 디스커버리를 `~/.claude/commands/`에서 `~/.claude/skills/*/SKILL.md`로 옮기면서 모든 `/gsd:*` 명령이 "Unknown skill"로 실종. 런타임 버전 커플링이 취약하다는 증거
- **기존 CLAUDE.md 미주입** (이슈 #50) — brownfield 프로젝트에 GSD를 얹을 때 방법론 룰이 기존 CLAUDE.md에 자동 통합되지 않는다
- **Standalone shipping 약함** — tentenco 비판: "GSD excels at keeping specs, goals, and state anchored across long sessions. But if you use it alone, it does not directly produce code, run tests, or open a PR." GSD는 context anchor로는 강하지만 단독 shipping 가치는 제한적
- **비용 구조** — Claude Pro($20/mo) 부족, Max($100–200/mo) 권장. 4:1 토큰 오버헤드 추정
- **v1 자기부정** — TÂCHES 본인이 v1의 "Markdown 프롬프트 주입" 방식을 "fighting the tool"이라고 부르며 v2(Pi SDK TypeScript CLI)로 갈아엎는 중. 커뮤니티는 v1에 표준화돼 있고 v2(5.6k stars)는 아직 과도기. 지금 시점에 어느 버전을 쓸지 결정하는 게 필요

그리고 강조할 것 하나: **auto-answer 기반 완전 자율화는 포팅하지 말 것**. 이슈 #803/#780이 보여주듯 HITL 채널을 꺼버리면 GSD의 핵심 안전장치가 사라진다. 프레시 카브오프 모델은 가져오되, "사용자 없이 돌아가게 만드는 것"은 GSD가 스스로 경고하는 실패 모드다.

## 어디에 쓰고 어디에 쓰지 말까

**쓸만한 영역**
- 장시간 세션에서 컨텍스트 로트가 실제로 문제가 되는 중대형 프로젝트
- 스펙/요구사항/진행 상황을 파일로 anchor해야 하는 브라운필드 연속 작업
- HITL 체크포인트를 받아들일 수 있는 솔로 개발자 워크플로 (Max 플랜)
- Superpowers(doing)나 gstack(thinking)과 스택해서 context 레이어로 쓸 때
- 멀티 런타임에 이식하려는 프로젝트 (Claude Code / Codex / Gemini / Cursor 등 14개 런타임 지원)

**쓰면 안 되는 영역**
- 수 분짜리 애드혹 태스크 (오버킬 — 대신 `/gsd:quick`)
- 토큰 예산 $20/mo 미만 Claude Pro 환경
- HITL이 불가능한 완전 자율 파이프라인 (auto-answer 회귀 선례)
- 기존 CLAUDE.md 설정이 민감한 프로젝트 (이슈 #50)
- Claude Code 런타임 버전 변경에 민감한 프로덕션 환경 (컴패티 버그 선례)

## 한국어 독자를 위한 참고

한국 커뮤니티 노출은 Ralph/Superpowers만큼은 아니지만 "GSD 프레임워크" "Get Shit Done 클로드" 검색어로 국내 블로그 글이 점차 늘고 있다. 대부분은 tentenco / codecentric / dev.to 자료의 2차 요약이므로, 원문(README, codecentric Felix Abele, ccforeveryone Carl Vellotti)을 직접 읽는 걸 권한다. 용어상 "페이즈"는 그대로 쓰고, "wave"는 번역하지 말고 그대로 쓰는 게 낫다 — 플랜 파일 명명에 직접 들어가 있기 때문이다.

## 더 읽을거리

- **저자/공식** — [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done), [gsd-build/gsd-2 (v2 TypeScript rewrite)](https://github.com/gsd-build/gsd-2), [gsd.build 랜딩](https://gsd.build/), [Mintlify 문서](https://gsd-build-get-shit-done.mintlify.app/)
- **해설** — [Ewan Mak (tentenco): Superpowers, GSD, gstack 비교](https://medium.com/@tentenco/superpowers-gsd-and-gstack-what-each-claude-code-framework-actually-constrains-12a1560960ad), [Felix Abele (codecentric): Claude Code 워크플로 아나토미](https://www.codecentric.de/en/knowledge-hub/blog/the-anatomy-of-claude-code-workflows-turning-slash-commands-into-an-ai-development-system), [Agent Native: Meta-prompting and Spec-driven Development](https://agentnativedev.medium.com/get-sh-t-done-meta-prompting-and-spec-driven-development-for-claude-code-and-codex-d1cde082e103)
- **실전 가이드** — [알리카즈미: Complete Beginner's Guide](https://dev.to/alikazmidev/the-complete-beginners-guide-to-gsd-get-shit-done-framework-for-claude-code-24h0), [imaginex: Skills Stack (Superpowers+gstack+GSD)](https://dev.to/imaginex/a-claude-code-skills-stack-how-to-combine-superpowers-gstack-and-gsd-without-the-chaos-44b3), [ccforeveryone 강의](https://ccforeveryone.com/gsd)
- **실패 모드** — [이슈 #780 (`--auto` 오류)](https://github.com/gsd-build/get-shit-done/issues/780), [이슈 #803 (HITL 회귀)](https://github.com/gsd-build/get-shit-done/issues/803), [이슈 #218/#1504/#1528 (Claude Code 호환)](https://github.com/gsd-build/get-shit-done/issues/218)
- **구조 인덱스** — [DeepWiki: gsd-build/get-shit-done](https://deepwiki.com/gsd-build/get-shit-done)

## 한 문장으로 덮기

GSD는 "슬래시 명령 뭉치"가 아니라 **"매 태스크를 프레시 200K 서브에이전트로 카브오프하고, 오케스트레이터는 서머리만 읽게 만드는" 공간 축 컨텍스트 엔지니어링**이며 — 이 원리는 `.planning/` 디렉토리와 파일명 프로토콜만 따라하면 어떤 런타임에서도 재현된다.
