---
title: Ouroboros — 한 번 이해하고 가기
based_on: notes/harness/ouroboros.md
date: 2026-04-13
audience: user (Korean)
reading_time: ~8분
---

# Ouroboros — 스펙을 숫자로 재단하는 진화 루프

## 한 줄로

> "Stop prompting. Start specifying."

Ouroboros 는 이 한 문장으로 자기를 소개한다. 슬로건만 보면 흔한 "스펙 주도 개발" 류 하나로 보이지만, 실제로 열어보면 독특한 지점이 여럿 있다. 2026년 1월 14일 Q00 (Seoul 거주, ZEP Tech Lead) 이 공개했고, 사용자와 Claude Code / Codex CLI / OpenCode 같은 AI 런타임 사이에 **MCP 서버**로 끼어들어 `interview → seed → execute → evaluate → evolve` 5단계 사이클을 강제한다. 이름은 "자기 꼬리를 먹는 뱀" — 평가 결과가 다음 generation 의 스펙으로 다시 들어간다는 은유다.

## 왜 태어났는가

Q00 의 진단은 Ralph(Huntley)나 GSD(TÂCHES)와 또 다른 각도를 찍는다. Huntley 는 "완벽한 프롬프트 집착" 을, Vincent 는 "프로세스 디시플린 부재" 를, TÂCHES 는 "context rot" 을 적으로 지목했다. Q00 가 지목한 적은 **인풋의 모호성**이다.

> "Most AI coding fails at the **input**, not the output. The bottleneck is not AI capability -- it is human clarity." — README

즉 코드가 실패하는 건 모델이 멍청해서가 아니라 사람이 무엇을 만들고 싶은지 스스로 모르기 때문이라는 주장. 해법도 자연스럽다. 모델에게 "뭘 만들어 줘" 라고 말하는 대신, **모델이 먼저 Socratic 질문으로 사용자를 심문**해서 숨은 가정을 전부 꺼내게 하고, 그 결과를 불변 스펙으로 굳힌 뒤에야 코드 생성으로 넘어간다. 슬로건인 "specifying" 은 그냥 "문서 쓰자" 가 아니라 **"모호성을 숫자로 잴 수 있는 무언가로 변환하자"** 에 가깝다.

## 실제로 어떻게 돌아가는가

하나의 generation 이 무슨 일을 하는지가 핵심이다. `ooo evolve "build a task CLI"` 한 줄로 트리거하면:

1. **Interview** — Socratic 면접이 시작된다. 매 질문은 4-path 라우팅 중 하나로 답한다 — 코드 확인 / 사용자 판단 / 둘 다 / 리서치 (WebFetch). "3 연속 코드·리서치 답변이면 다음 질문은 **반드시** 사용자에게" 라는 dialectic rhythm guard 가 박혀 있다. 코드 탐험에 매몰되어 사람을 잊지 말라는 뜻
2. 면접은 **ambiguity score ≤ 0.2** 가 될 때까지 반복된다. 그 숫자를 어떻게 재는지는 MCP 서버 내부에 있고 스킬 레이어에서는 불투명
3. **Seed** — 면접 결과가 YAML 스펙으로 crystallize 된다. 7개 필드: GOAL / CONSTRAINTS / ACCEPTANCE_CRITERIA / ONTOLOGY_SCHEMA / EVALUATION_PRINCIPLES / EXIT_CONDITIONS / METADATA. 한 번 굳어진 seed 는 **불변**
4. **Execute** — Double Diamond 분해로 실행. 첫 diamond 는 Socratic (Wonder → Ontology), 둘째 diamond 는 Pragmatic (Design → Evaluation). UX 유산의 직접 수입
5. **Evaluate** — 3-stage 검증이 순차로: Mechanical (lint/build/test, $0) → Semantic (AC 준수, 드리프트 측정) → Multi-Model Consensus (Frontier tier, 불확실할 때만)
6. **Evolve** — Wonder ("아직 모르는 건?") 와 Reflect ("ontology 를 어떻게 변이시킬까?") 사이클이 다음 generation 의 seed 를 만든다. 여기서 우로보로스가 자기 꼬리를 먹는다

루프의 종료 조건은 셋 중 하나 — ontology similarity 가 **≥ 0.95** 가 되면 `converged`, 30 세대에 도달하면 `exhausted`, 3 세대 연속 불변이면 `stagnated`. 마지막 경우 사용자는 `ooo unstuck` 으로 탈출한다.

`ooo unstuck` 은 작지만 예쁜 primitive 다. 5개의 lateral thinking 페르소나 중 하나를 주입한다: **Hacker**("작동하게 먼저, 우아함은 나중"), **Researcher**("뭘 모르고 있지?"), **Simplifier**("범위 자르고 MVP 로"), **Architect**("접근 자체를 다시 짜자"), **Contrarian**("잘못된 문제를 풀고 있는 건 아닐까?"). 트리거 키워드는 "I'm stuck" 또는 "think sideways".

상태는 어디에 있는가. Ralph 는 파일, GSD 는 `.planning/*.md`, Superpowers 는 `docs/superpowers/specs/` — 다들 파일시스템이 권위적 매체다. Ouroboros 는 다르다. **MCP 서버 + EventStore** 가 권위적이고, `evolve_step` 호출은 stateless 다 (상태는 이벤트 리플레이로 재구성). 이 설계 덕에 매 generation 마다 컨텍스트를 이론상 카브오프 할 수 있고, 그것이 왜 메뉴얼에 **"Designed for Ralph integration"** 이라고 쓰여 있는지의 이유다.

## 왜 작동한다고 (Q00 는) 주장하는가

증거는 얇다. 이게 정직한 평가다.

README 에는 "12 hidden assumptions exposed, ambiguity scored to 0.19" 같은 한 줄 예시가 있고, "rework rate Low vs vanilla AI coding" 이라는 정성 비교 테이블이 있다. 숫자 수사(0.2 / 0.95 / 0.3) 가 풍성해서 정량 지향으로 보이지만, 정작 그 숫자들의 **측정 함수는 블랙박스**고 벤치마크는 없다.

3자 재현·리뷰도 Ralph (Tessmann, Wang, Devon, beuke) 나 Superpowers (Willison, Mak) 대비 **가장 얇다**. Lobehub 에 스킬 등재된 정도가 외부 가시성의 전부. 그 빈자리를 대신 메우는 건 **활발한 릴리즈 페이스** — 2026-03-30 v0.26.6 에서 2026-04-12 v0.28.4 까지 약 2주 동안 마이너 10개 릴리즈가 쏟아졌다. 지금 성장 중인 하네스라는 얘기고, 역으로 지금 막 써보기에는 이르다는 얘기이기도 하다.

## 진짜 핵심 아이디어 하나

Ouroboros 가 자기를 판매하는 방식("스펙 우선") 과, 실제로 갖고 있는 가장 독창적인 primitive 는 다르다.

진짜 핵심은 **"모호성을 숫자로 재단해 게이트 구문으로 쓴다"** 는 점이다. Superpowers 의 `<HARD-GATE>` XML 태그나 Ralph 의 CAPS 호통과 달리, Ouroboros 의 게이트는 ambiguity ≤ 0.2, similarity ≥ 0.95, drift ≤ 0.3 같은 **정량 임계값**이다. 모델 출력을 "통과 / 차단" 두 상태로 가르는 기준이 숫자라는 것 — 이 아이디어 하나가 계보 상 새롭다. 다른 하네스는 정성 게이트(HARD-GATE 태그, phase enum, CAPS yelling, 파일 sentinel) 를 쓴다.

이 정량 게이트 발상은 이식 가능하지만, 측정 함수의 품질은 이식 불가능하다. "ambiguity 를 뭐라고 정의하고 어떻게 재는가" 라는 핵심 질문에 Ouroboros 는 코드로만 답하고 스펙 레이어에서는 답하지 않는다. 사용자가 이 숫자를 신뢰하려면 결국 구현부를 읽어야 한다.

## 가져갈 만한 것들

딥다이브 노트 §11 에 12개의 이식 가능한 원시요소를 정리해뒀다. 가장 주목할 5개:

1. **Ambiguity-as-gate** — 인풋 모호성을 숫자 임계값으로 차단. 측정 함수는 프로젝트에 맞게 커스텀 — LLM-as-judge, 구조 검증, 체크리스트 매칭 중 고르면 된다. 원시요소 자체는 런타임 중립
2. **Seed = immutable 7-field YAML 계약** — GOAL / CONSTRAINTS / ACCEPTANCE_CRITERIA / ONTOLOGY_SCHEMA / EVALUATION_PRINCIPLES / EXIT_CONDITIONS / METADATA. GSD 의 `.planning/*.md` 셋, Superpowers 의 design.md 와 같은 계열인데 여기는 **스키마가 명시적**이고 불변
3. **Socratic interview + dialectic rhythm guard** — 3 연속 코드/리서치 확인이면 다음 질문은 강제로 사람에게. 면접이 코드 탐험에 매몰되지 않도록 하는 backpressure 정책. 순수 프롬프트 레이어로 이식 가능
4. **5 lateral thinking personas as escape hatch** — stagnation 감지 시 Hacker/Researcher/Simplifier/Architect/Contrarian 중 하나를 주입. Persona 프롬프팅의 실용적 적용 예. 구조화된 "막혔을 때 이렇게 생각해봐" 메뉴
5. **Path A / Path B skill duality** — 모든 SKILL.md 가 "MCP 툴 있으면 Path A, 없으면 agent 채택해서 Path B" 로 이중화. 플러그인 의존과 self-contained 폴백을 같은 스킬 안에 넣는 컨벤션. 생태계 레이어 의존에 대한 우아한 해답

더 있다(PAL Router 3-tier 비용 에스컬레이션, 30-generation state machine, Double Diamond 수입, MCP 이벤트 기반 상태) — 노트에서 확인.

## 조심할 것

실패 모드는 Q00/ouroboros 의 GitHub 이슈 트래커가 잘 드러낸다. 전부 저자 본인이 인지하고 open 으로 추적 중이다:

- **Issue #371 — parallel session 의 429 cascade**: 병렬 세션을 스폰하면 rate-limit 토큰 버킷이 공유되지 않아 연쇄 폭탄
- **Issue #369 — AC 트리 무한 분해**: Acceptance Criteria 가 재귀적으로 쪼개지다가 3분 만에 `ac_3000002` 같은 300만 노드에 도달. "runaway fractal nesting"
- **Issue #341 — 서브프로세스 누수**: 취소된 job 이 Claude CLI 서브프로세스를 살려둔다. #269 의 리그레션
- **Issue #310 — MCP 서버 startup 블로킹**: 동기 orphan session 스캔이 서버 시작을 막아 연결 타임아웃
- **Issue #305 — 중첩 세션 실패**: Claude Agent SDK 가 중첩 호출에서 에러. Ouroboros + 다른 MCP 하네스 병용 시 위험 신호
- **Issue #364 — interview 피로도**: "Harden interview flow UX, auto-confirm, batch questions" — 3+ 라운드 면접이 과한 경우 있음

그리고 구조적 한계:

- **Ambiguity score 가 블랙박스**: 0.2 임계값이 게이트지만 "왜 0.19 인가" 를 사용자가 검증할 수 없다. 신뢰는 결국 구현부 리딩 문제
- **3자 검증 부재**: Ralph/Superpowers/GSD 대비 외부 재현 보고가 사실상 없음. 지금 프로덕션 의존 대상으로 쓰기엔 이르다
- **30-generation 상한은 cost cap 이지 safety control 이 아니다**: Devon 의 Ralph 비판("숫자 제한은 두 번째 이터레이션에서 DB 를 지우는 걸 막지 못한다") 이 여기도 그대로 적용
- **Ralph 이름 재사용의 의미론 충돌**: `ooo ralph` 는 Huntley 의 file-mediated bash loop 과 의미론적으로 무관하고 모토가 "The boulder never stops" (시지프스 은유) 다. 브랜드 혼란 소스

그리고 팔지 않을 게 하나 있다. **seed crystallize 직후 GitHub star 를 요구하는 gate**. `ooo setup` 을 "Full Mode 잠금해제" 로 포장하고 star 를 선조건처럼 제시한다 — 이건 하네스 primitive 가 아니라 **distribution tactic** 이다. 이식할 때 버릴 것.

## 어디에 쓰고 어디에 쓰지 말까

**쓸 만한 영역**
- 요구사항이 애매한 상태로 Claude 에게 던져지는 패턴을 개선하고 싶은 팀
- 스펙을 구조화된 불변 YAML 로 관리하고 싶은 프로젝트 (ACCEPTANCE_CRITERIA 와 ONTOLOGY_SCHEMA 를 분리하고 싶은 경우)
- Socratic 면접 단계 하나만 떼서 쓰고 싶을 때 — unstuck 의 5 페르소나 같은 것도 독립 primitive 로 추출 가능
- MCP 스택을 이미 운영 중이고 서버 관리 복잡도를 감당할 수 있는 팀

**쓰면 안 되는 영역**
- 그린필드 부트스트랩 속도가 최우선일 때 (Ralph 가 훨씬 가볍다)
- Brownfield 마이그레이션 주 작업 (v0.28.0 의 `ooo brownfield` 로 보완 중이지만 설계 원류가 greenfield)
- 3자 검증이 부족한 상태가 신경 쓰이는 프로덕션 파이프라인
- MCP 서버 관리 + deferred tool 디버깅을 감당하기 어려운 개인 개발자
- 파일 기반 감사 추적이 필요한 환경 (Ouroboros 의 권위적 상태는 EventStore — `git log` 로 못 본다)

## 한국어 독자를 위한 참고

Q00 는 Seoul 에 있는 ZEP Tech Lead 다(GitHub 프로필 기준). 그러나 한국어 블로그·YouTube 에서 Ouroboros 를 소개한 2차 자료는 검색에서 거의 안 보인다 — 저자가 한국인인 것과 별개로 **아직 한국 커뮤니티 확산 전**이라는 뜻이다. 우리가 "우로보로스" 라고 읽을 때 주의할 점 하나 — razzant/ouroboros (텔레그램 기반 자기개조 agent, 2026-02-16) 와 이름이 완전히 겹친다. 본 노트가 가리키는 것은 **Q00/ouroboros** 이며, 스타 기준으로 4.7배 크고 계보상 하네스 계열에 속한다.

## 더 읽을거리

- **Q00 본인** — [레포](https://github.com/Q00/ouroboros), [CLAUDE.md](https://github.com/Q00/ouroboros/blob/main/CLAUDE.md), [PyPI 패키지](https://pypi.org/project/ouroboros-ai/), [릴리즈 노트](https://github.com/Q00/ouroboros/releases), [프로필](https://github.com/Q00)
- **스킬 내부** — [seed/SKILL.md](https://github.com/Q00/ouroboros/blob/main/skills/seed/SKILL.md), [evolve/SKILL.md](https://github.com/Q00/ouroboros/blob/main/skills/evolve/SKILL.md), [unstuck/SKILL.md](https://github.com/Q00/ouroboros/blob/main/skills/unstuck/SKILL.md), [evaluate/SKILL.md](https://github.com/Q00/ouroboros/blob/main/skills/evaluate/SKILL.md), [ralph/SKILL.md](https://github.com/Q00/ouroboros/blob/main/skills/ralph/SKILL.md)
- **실패 모드 추적** — [open issues](https://github.com/Q00/ouroboros/issues) (#371 rate-limit cascade, #369 AC fractal nesting, #341 subprocess leak, #310 MCP startup block)
- **외부 마켓플레이스** — [Lobehub 스킬](https://lobehub.com/skills/q00-ouroboros-welcome)
- **계보 비교** — Ralph (`notes/harness/ralph-wiggum.md`) / Superpowers (`notes/harness/superpowers.md`) / GSD (`notes/harness/gsd.md`) — 같은 리포지토리의 앞선 3개 딥다이브 노트

## 한 문장으로 덮기

Ouroboros 는 "스펙 주도 개발" 을 다시 포장한 것이 아니라, **모호성을 숫자로 재단해 코드 생성 게이트로 쓴다** 는 한 아이디어를 중심으로 돌아가는 진화 루프이며, 그 발상이 맞는 영역인지 아닌지는 당신이 측정 함수를 신뢰할 수 있는가에 달려 있다.
