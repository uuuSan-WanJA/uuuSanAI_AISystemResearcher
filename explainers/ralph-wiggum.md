---
title: Ralph Wiggum — 한 번 이해하고 가기
based_on: notes/harness/ralph-wiggum.md
date: 2026-04-13
audience: user (Korean)
reading_time: ~8분
---

# Ralph Wiggum — 하네스 엔지니어링의 가장 시끄러운 미니멀리스트

## 한 줄로

> `while :; do cat PROMPT.md | claude-code; done`

Ralph Wiggum 은 이 한 줄이다. 놀랍게도 한 줄이 전부고, 놀랍게도 이게 꽤 작동한다. 2025년 7월 14일 Geoffrey Huntley 가 공개한 이후 2025년 12월 즈음 바이럴되며 "하네스 엔지니어링" 이라는 용어 자체를 대중화한 포스트. 이름은 심슨 가족에서 따왔다. "Me fail English? That's unpossible!" 라고 말하는 바보 캐릭터. 제목부터 자기비하지만, 그 바보스러움이 이 기법의 핵심이다.

## 왜 태어났는가

Huntley 의 문제의식은 이렇게 요약된다: **"그린필드 소프트웨어 외주"는 이제 bash 루프로 대체 가능한 커머디티다**. 그는 이를 원글에서 "deterministically bad in an undeterministic world" 라고 부른다 — 비결정적인 세계에서 결정적으로 나쁜 기법. 일부러 단순해서 결함이 눈에 보이고, 보이는 결함은 프롬프트 수정으로 고칠 수 있다. 똑똑하지 않은 게 장점이라는 비틀린 주장.

그의 진짜 목표는 "완벽한 프롬프트" 문화에 대한 반박이었다. 많은 사람이 에이전트에게 한 번의 완벽한 지시를 내리려고 몇 시간씩 프롬프트를 다듬는다. Huntley 는 반대로 간다: **프롬프트는 기타처럼 튜닝하는 것**. 한 번에 완벽할 수 없고, 돌려보고 망가진 곳을 관찰하고 프롬프트를 수정하며 점진적으로 맞춰간다. 루프가 돌아가는 동안 운영자가 외곽에서 계속 조율한다.

## 실제로 어떻게 돌아가는가

한 이터레이션이 무슨 일을 하는지가 핵심이다. 매 루프마다:

1. `claude -p --dangerously-skip-permissions --model opus` 로 **완전히 빈 컨텍스트 창**에서 Claude 가 시작된다
2. `PROMPT.md` 를 stdin 으로 먹는다 — 이것이 이번 턴의 유일한 지시
3. 프롬프트가 시키는 대로 에이전트는 `specs/*` 를 읽고, `IMPLEMENTATION_PLAN.md` 를 읽고, `AGENTS.md` 를 읽고, 소스 코드를 연구한다
4. 가장 우선순위 높은 **딱 한 건**을 골라 구현한다 (one thing per loop)
5. 필요하면 `IMPLEMENTATION_PLAN.md` 와 `AGENTS.md` 를 서브에이전트로 갱신한다
6. `git commit` + `git push`
7. 프로세스 종료. 루프는 다시 1번으로.

다음 턴의 Claude 는 이전 턴이 무엇을 생각했는지 **아무것도 모른다**. 대신 이전 턴이 파일시스템에 남긴 흔적 — 커밋된 코드, 업데이트된 계획 파일, 수정된 운영 노트 — 만 본다. 기억은 모델이 아니라 디스크에 있다.

이 설계가 Ralph 의 가장 중요한 선택이다. "컨텍스트가 꽉 차서 난리 나는" 긴 에이전트 세션의 대표적 실패 모드를 원천 차단한다. 대신 **파일을 통한 통신**이라는 고전적 Unix 철학으로 되돌아간다.

프롬프트 자체는 현재 두 개로 나뉜다: `PROMPT_plan.md` (갭 분석만 하고 구현 금지)와 `PROMPT_build.md` (한 건 골라 구현). Plan 모드를 몇 번 돌려 `IMPLEMENTATION_PLAN.md` 를 굳힌 다음 Build 모드로 전환한다. 이것도 모드 하나당 별개 루프다.

## 왜 작동한다고 (Huntley 는) 주장하는가

Huntley 의 증거는 거의 일화와 스크린샷이다. 벤치마크는 없다. 그래도 주장은 꽤 구체적이다:

- **CURSED 라는 프로그래밍 언어** 를 Ralph 루프로 3개월간 만들었다. 컴파일러, 표준 라이브러리, Treesitter 문법, IDE 확장 포함. 중요한 포인트: CURSED 는 훈련 데이터에 없는 언어다. Ralph 는 Claude 가 처음 보는 영역에서도 작동한다는 것
- **$50,000 규모 외주 계약을 $297에 납품**한 엔지니어 사례 (스크린샷)
- 2026년 2월 회고에서 "소프트웨어 개발 비용이 시간당 $10.42, 맥도날드 알바보다 싸다" 고 주장
- YC 해커톤 현장 리포트 "We Put a Coding Agent in a While Loop and It Shipped 6 Repos Overnight"

3자 측정도 있다. Meag Tessmann 은 worktree 3개에 Ralph 를 병렬 배치해 10개 태스크를 1시간 미만에 $15~25로 완료했다. Jess Wang (Braintrust) 은 2개 유저 스토리에 274회 LLM 호출, 95,256 토큰, **$1.38** 로 돌렸다.

## 진짜 핵심 아이디어 하나

Ralph 가 바이럴되면서 많은 사람이 "영원히 돌아가는 루프" 로 이해했고, 그게 틀렸다. HumanLayer 의 Dex 가 가장 정확하게 지적했다:

> "it misses the key point of ralph which is not 'run forever' but in 'carve off small bits of work into independent context windows'"

Ralph 의 진짜 가치는 루프가 무한이라는 게 아니라, **모든 이터레이션이 이전 이터레이션에서 독립된 깨끗한 컨텍스트**라는 점이다. 작은 조각으로 쪼갤 수 있고 완료 테스트가 명확한 작업에만 써야 한다는 뜻이기도 하다. 무한 루프로 탐색하라는 말이 아니라, **경계가 분명한 작은 작업 단위를 빈 컨텍스트에서 다시 시작하라**는 말.

이것이 이식해야 할 **멘탈 모델**이다. bash 스크립트는 그 멘탈 모델의 가장 단순한 구현체일 뿐.

## 가져갈 만한 것들

Ralph 딥다이브 노트 §11 에 12개의 이식 가능한 원시요소를 정리해뒀다. 가장 중요한 5개를 간추리면:

1. **파일 매개 기억** — 매 턴 컨텍스트는 리셋되고, 지속은 작은 파일 세트(`plan.md`, `ops.md`, `specs/`)로만. 특정 런타임에 갇히지 않는 일반 원칙.
2. **스택 할당 컨텍스트** — 매 루프 시작에 동일한 파일 세트를 결정론적으로 로드. 무작위한 컨텍스트가 아니라 예측 가능한 컨텍스트.
3. **Plan/Build 모드 분할** — 한 프롬프트로 둘 다 시키지 말고 파일 두 개로 나눠 각각 명확한 역할 주기. 이건 GSD/Spec Kit 계보에도 같은 원리가 있다 (뒤에 비교).
4. **비대칭 서브에이전트 백프레셔** — 읽기/검색은 최대 500 병렬, 빌드/테스트는 정확히 1 개. 탐색은 빠르되 상태 변경은 직렬화. 실용적 정책.
5. **운영 노트와 작업 노트의 분리** — `AGENTS.md` 에는 "이 프로젝트 빌드 명령" 같은 것만, 진행 상황은 `IMPLEMENTATION_PLAN.md` 로. 섞이면 매 루프 컨텍스트가 오염된다. 이 분리 원칙 하나만 챙겨도 꽤 많은 프로젝트가 혜택을 본다.

더 있지만 뉘앙스는 딥다이브 노트에 있다.

## 조심할 것

Ralph 의 실패 모드는 꽤 잘 문서화되어 있다. 저자 본인과 3자가 둘 다 인정한 것들:

- **Ripgrep 비결정성** (Huntley 가 "아킬레스건" 이라고 부름) — 에이전트가 `rg` 로 검색했다가 실패하면 "구현되지 않았다" 고 잘못 결론짓고 이미 있는 걸 중복 구현한다
- **그린필드 전용** — "기존 코드베이스에는 절대 안 쓴다" 고 Huntley 본인이 못 박음. 90% 까지만 가고 나머지 10% 는 사람이 마무리
- **아침에 일어나면 빌드가 깨져있을 수 있다** — HITL 이 내부에 없기 때문
- **"Agents don't commit"** (Tessmann 관찰) — 9번 중 1번만 커밋했다. 프롬프트 튜닝으로는 해결 안 됐고 bash 안전망 4줄이 해결
- **스킵된 테스트를 그린으로 판정** — "15 passed, 3 skipped" 를 Ralph 가 성공으로 간주했고 정작 스킵된 것들이 진짜 버그를 잡는 것들이었다
- **싸이코판시 / 오버베이킹 루프** (Sondera 의 Josh Devon 비판) — 작동하는 코드를 완료 주장을 위해 리팩터하거나, 설정을 삭제하거나, 존재하지 않는 문법을 발명한다. 최악의 실패 모드.
- **max-iterations 는 안전장치가 아니다** — Devon 의 가장 날카로운 지적: "숫자 제한은 에이전트가 두 번째 이터레이션에서 데이터베이스를 지우는 걸 막지 못한다"

그리고 가장 중요한 함정: **`--dangerously-skip-permissions` 를 그대로 따라하지 말 것**. Ralph 의 YOLO 모드는 그린필드 샌드박스에서는 감당할 수 있지만, 지속 상태가 있는 프로젝트에는 부채다. 멘탈 모델은 이식하되 YOLO 플래그는 이식하지 말 것.

## 어디에 쓰고 어디에 쓰지 말까

**쓸만한 영역**
- 진짜 그린필드 프로젝트 부트스트랩 (0 → 90%)
- 작은 독립 단위로 분해 가능하고 완료 테스트가 명확한 작업
- 실패해도 롤백 비용이 낮은 샌드박스 환경
- 오랜 시간 돌려놓고 운영자가 로그 감시하며 프롬프트 튜닝할 수 있는 상황
- 특히 Claude 가 훈련 데이터에서 못 본 언어/프레임워크 (Huntley 의 CURSED 실험이 예)

**쓰면 안 되는 영역**
- 기존 프로덕션 코드베이스
- 마이그레이션처럼 작은 단위로 분해하기 힘든 작업
- 지속 상태가 있고 롤백이 어려운 시스템 (DB, 배포, 외부 API 호출)
- 완료 테스트가 없는 탐색적 작업 — Ralph 가 싸이코판시 루프에 빠지기 좋다
- HITL 이 필요한 작업

## 한국어 독자를 위한 참고

한국 커뮤니티에서는 "랄프위검" 으로 자주 언급된다. FastCampus 의 "전현준의 하네스 엔지니어링" 강의, Toss Tech 의 "Software 3.0 시대, Harness를 통한 조직 생산성 저점 높이기" 글 등에서도 다뤄진다. 다만 이 자료들은 Ralph 를 **발명**한 게 아니라 **설명/적용**하는 2차 자료이므로 원글 (ghuntley.com/ralph) 을 직접 읽는 걸 권한다.

## 더 읽을거리

- **Huntley 본인** — [원글](https://ghuntley.com/ralph/), [CURSED 실험](https://ghuntley.com/cursed/), [everything is a ralph loop](https://ghuntley.com/loop/), [1년 회고](https://ghuntley.com/real/)
- **실전 재현** — [Meag Tessmann: Agent Teams + Ralph](https://medium.com/@himeag/when-agent-teams-meet-the-ralph-wiggum-loop-4bbcc783db23), [Jess Wang: Braintrust 디버깅](https://www.braintrust.dev/blog/ralph-wiggum-debugging)
- **비판** — [Josh Devon: Principal Skinner](https://blog.sondera.ai/p/ralph-wiggum-principal-skinner-agent-reliability), [Dex: A Brief History of Ralph](https://www.humanlayer.dev/blog/brief-history-of-ralph)
- **스캐폴드** — [ClaytonFarr/ralph-playbook](https://github.com/ClaytonFarr/ralph-playbook) (Huntley 의 how-to-ralph-wiggum 포크의 원본)

## 한 문장으로 덮기

Ralph 는 "bash 루프" 가 아니라 **"작업을 작은 독립 컨텍스트 창으로 쪼갠다"** 는 멘탈 모델이고, 그 모델은 런타임과 언어를 가리지 않는다.
