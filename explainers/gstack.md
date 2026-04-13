---
title: gstack — 한 번 이해하고 가기
based_on: notes/harness/gstack.md
date: 2026-04-13
audience: user (Korean)
reading_time: ~8분
---

# gstack — Claude 를 한 명 말고 스물 명처럼 부리기

## 한 줄로

gstack 은 Y Combinator 대표 **Garry Tan** 이 공개한 Claude Code 용 skill-pack 으로, 23개의 슬래시 커맨드를 각각 **하나의 엔지니어링 역할**에 결박시켜 "Claude 를 한 사람이 아니라 한 팀으로 부리는" 기법을 체계화했다. CEO, Engineering Manager, Staff Engineer, Designer, QA Lead, CSO, Release Engineer — 이렇게 페르소나 단위로 명령이 나뉘어 있다. tentenco (Ewan Mak) 가 Medium 2026 년 4월에 가장 정확히 요약했다. Superpowers 가 **프로세스**를 제약하고 GSD 가 **실행 환경**을 제약한다면, gstack 은 **"누구의 시선으로 생각할 것인가"**를 제약한다. 이것이 gstack 의 진짜 한 줄이다.

## 왜 태어났는가

Garry Tan 의 문제의식은 레포 README 와 ETHOS.md 에서 직접 읽힌다. 그의 프레임은 "생산성"이 아니라 **완전성의 마진 비용이 거의 0 이 되었다는 인식**이다:

> "AI-assisted coding makes the marginal cost of completeness near-zero. When the complete implementation costs minutes more than the shortcut — do the complete thing. Every time." — gstack ETHOS.md, "Boil the Lake"

"보일 수 있는 호수는 끓여라, 대양은 범위 밖으로 표시하라." 한 모듈의 100% 테스트 커버리지, 모든 엣지 케이스, 완전한 에러 경로 — 이런 것들은 AI 로 달성 가능한 "호수"이므로 쇼트컷을 치지 말라는 주장. 그는 이를 **"human engineering time 이 병목이었던 시절의 레거시 사고"** 에 대한 반박으로 포지션한다.

그리고 그 주장의 증거로 README 에 올려둔 숫자: "지난 60일간 600,000 줄 이상의 production code, 35% 테스트, 하루 10,000~20,000 줄, YC 를 풀타임으로 운영하면서 파트타임으로." 이 수치는 gstack 바이럴의 동력이자 격렬한 반발의 진원지다 (뒤에 비판 섹션).

## 실제로 어떻게 돌아가는가

gstack 의 워크플로는 **7 단계 스프린트**로 구조화된다: Think → Plan → Build → Review → Test → Ship → Reflect. 한 태스크의 전형적 동선:

1. **Think** — `/office-hours` 를 호출하면 Claude 가 YC 식 오피스 아워로 변신해 6가지 forcing question 을 던진다: Demand Reality, Status Quo, Desperate Specificity, Narrowest Wedge, Observation, Future-Fit. 사람이 답한다.
2. **Plan** — `/plan-ceo-review` (전략적 범위 챌린지) → `/plan-eng-review` (아키텍처, 엣지 케이스, 테스트 계획 락) → `/plan-design-review` (디자인 감사). 각 단계 출력이 다음 단계 입력으로 명시적으로 흘러간다.
3. **Build** — **여기가 비어 있다** (후술). Claude 가 기본 모드로 돌아가 코드를 쓴다.
4. **Review** — `/review` 로 Staff Engineer 페르소나가 코드를 감사하고 auto-fix 제안. `/cso` 는 OWASP + STRIDE 기반 보안 검토.
5. **Test** — `/qa` 가 앱을 실제로 실행하고 버그 찾고 atomic commit 으로 수정. `/qa-only` 는 리포트만.
6. **Ship** — `/ship` 이 main 과 sync, 테스트 실행, 커버리지 감사, PR push. `/land-and-deploy` 가 merge + deploy + production health 확인.
7. **Reflect** — `/retro` 가 주간 회고.

핵심은 **한 커맨드가 하나의 의사결정 클래스에만 대응**한다는 것. Agent Native 의 표현을 빌리면 "Claude 가 engineering manager 로 동작할 때는 UI 색상 피드백을 무시하고 framework 선택과 유지보수성에만 집중한다." 한 대화에 product judgment, implementation, verification 을 뒤섞지 않는 것이 규율이다.

파괴적 명령에 대한 방어선도 명시적이다. `/careful` 은 `rm -rf`, `DROP TABLE`, force push 같은 것들을 경고 후에만 실행, `/freeze` 는 편집 범위를 한 디렉토리로 가둔다, `/guard` 는 둘 다. Ralph 의 `--dangerously-skip-permissions` 를 정확히 반전시킨 지점.

## 왜 작동한다고 (저자는) 주장하는가

Garry Tan 의 증거는 두 가지다. 하나는 위의 수치 (600K LOC / 60일 / 1,237 contributions in 2026). 다른 하나는 그가 X 에 올린 CTO 친구의 인용:

> "Your gstack is crazy. This is like god mode. Your eng review discovered a subtle cross site scripting attack that I don't even think my team is aware of." — Garry Tan, X (트윗 2032196172)

통제된 벤치마크는 없다. Ralph 에 대한 Braintrust/Wang 의 $1.38 측정 같은 독립 재현도 없다. 모든 수치는 저자 자기 보고 + 스크린샷 + 일화다. gstack 바이럴의 큰 부분은 **Garry Tan 이 YC 대표라는 플랫폼 효과**로 설명된다 — 이 점은 비판자들이 가장 먼저 지적하는 부분이기도 하다.

## 진짜 핵심 아이디어 하나

tentenco 가 가장 정확하게 짚어냈다:

> "gstack's design assumption sits on a different axis from Superpowers and GSD. It doesn't care about your development process or context window health. It governs who makes what decision." — Ewan Mak, Medium 2026-04

gstack 의 진짜 가치는 23개의 커맨드도 아니고, Boil the Lake 원칙도 아니고, 병렬 Conductor 도 아니다. 그것은 **LLM 을 "만능 조수" 가 아니라 "역할을 부여받은 전문가" 로 호출한다**는 설계 철학 자체다. 같은 코드라도 engineering manager 가 보느냐 designer 가 보느냐 QA lead 가 보느냐에 따라 review vector 가 달라지게 강제하는 것. 하나의 대화에서 역할을 뒤섞지 않는 것.

이 멘탈 모델은 23개 커맨드 없이도 이식 가능하다. 당신의 프로젝트에 단 두 개의 role-scoped prompt — "엔지니어링 매니저로서 이 코드를 검토하라" vs "디자이너로서 이 UI 를 검토하라" — 만 도입해도 gstack 의 핵심을 맛본다.

## 가져갈 만한 것들

딥다이브 노트 §11 에 10개의 이식 primitive 가 있다. 가장 가치 있는 다섯:

1. **Role-scoped slash command** — 한 커맨드 = 한 페르소나. gstack 의 가장 순수한 기여이고 Superpowers/GSD 가 가지지 않은 원시요소.
2. **`/office-hours` 6-forcing-question gate** — 코드 쓰기 전 사람에게 Demand Reality, Narrowest Wedge 등 6가지 질문을 강제로 답하게 한다. 어떤 하네스에도 이식 가능한 "문제 먼저" 게이트.
3. **User Sovereignty 원칙** — "AI models recommend. Users decide." 한 줄로 선언 가능한 generation-verification loop. 모든 하네스의 시스템 프롬프트에 바로 추가할 수 있다.
4. **`/careful` + `/freeze` + `/guard` firewall** — 파괴적 명령 경고, 파일 편집 범위 락, 둘의 조합. YOLO 의 정확한 대척점이고 Ralph 사용자들이 가장 아쉬워하는 primitive 의 구체적 구현.
5. **`allowed-tools:` frontmatter declarative permission** — 각 skill 이 YAML 에 필요한 툴만 선언. GSD 의 동일 패턴과 함께 나타난 **같은 방향으로 수렴하는 두 번째 증거**라는 점이 중요하다.

## 조심할 것

gstack 의 실패 모드는 이례적으로 잘 문서화되어 있다. Hacker News (#47418576) 쓰레드가 가장 조직화된 비판원이다.

- **Build 단계 skill 공백** — tentenco 의 결정적 관찰. "Build 단계에 대응하는 skill 이 없다. Claude Code 는 사람이 수동으로 `/review` 를 돌릴 때까지 기본 모드로 돌아간다." 즉 gstack 의 제약이 **가장 위험한 단계에서 풀린다**.
- **LOC 메트릭의 자기모순** — 여러 HN 사용자가 지적. `the_af` 는 "600K LOC 를 production code 로 썼다는 게 자랑할 일이 아니다", `tabs_or_spaces` 는 "LOC 는 소프트웨어 엔지니어링 메트릭이 될 수 없다, 왜 우리는 이걸 계속 받아들이나", `coldtea` 는 "역사적으로 이 수치는 거대한 liability 이자 수치로 여겨졌다". 그리고 Tan 자신의 ETHOS.md "Completeness is cheap" 과 "600K LOC 자랑" 사이의 긴장은 비판자들 눈에 자기모순이다.
- **토큰 블로트** — dev.to imaginex 의 관찰: "모든 skill 을 켜면 실행 코드 한 줄 쓰기 전부터 단일 skill 이 10K+ 토큰을 소모한다." `preamble-tier` 필드 존재 자체가 저자도 이 문제를 인지한 증거.
- **Sherveen 의 종합 비판** — HN 쓰레드에서 가장 많이 인용된 회의론: gstack 은 "overengineered" 이고 "에이전트를 더 낫게 만들지 못하며 오히려 나쁘게 만들 가능성이 높다". 대안으로 Every Inc 의 compound engineering plugin 과 Simon Willison 의 agentic patterns 를 권한다.
- **`arnvald` 의 관찰** — "모든 skill 에 광고를 다는 게 불필요하게 컨텍스트를 어지럽힌다" — 모든 skill 이 gstack 자기 프로모션 블록을 포함하는 디자인에 대한 비판.
- **augmentcode 의 한 줄 요약** — 저자가 솔직하다: "600K LOC 주장을 액면가로 받아들이지 않는다. gstack 을 채택한다는 건 새 인프라를 채택하는 게 아니라 **프로세스**를 채택하는 것이다." 기술적 혁신 부재에 대한 정직한 요약.
- **Retrofitting 어려움** — MindStudio 분석: "기존 프로젝트가 깨끗한 스택 정의에 맞지 않으면 gstack 에 온보딩하는 데 진짜 노력이 든다. 처음부터 함께 짓는 프레임워크이지 기존 작업에 덮어씌우는 것이 아니다."
- **지속 가능성 이슈** — TechCrunch 기사에 따르면 Tan 은 "하루 4시간만 잠", "cyber psychosis" (후에 농담이라고 해명) 같은 발언을 했고, 이는 **저자 페르소나와 제품 규범 사이의 긴장**을 담론화시켰다. gstack 을 따라한다는 것이 무엇을 따라하는 것인지 묻게 하는 지점.

그리고 가장 중요한 함정. **"10K LOC per day" 메트릭은 이식하지 말 것.** 저자 자신의 ETHOS.md ("Search Before Building" — reinventing something worse) 와도 정면 충돌하고, HN 이 체계적으로 논박했다. gstack 의 역할 멘탈 모델은 가져가되 숫자 자랑은 두고 올 것.

## 어디에 쓰고 어디에 쓰지 말까

**쓸만한 영역**
- 그린필드 프로젝트, 특히 **스펙이 아직 흐릿한** 단계. `/office-hours` 와 `/plan-*-review` 체인이 결정을 명확히 한다.
- 창업자 / 솔로 빌더처럼 여러 역할을 혼자 다 쓰는 맥락 — gstack 의 role injection 이 실제 업무 구조와 맞물림.
- 파괴적 명령에 노출된 환경 — `/careful` / `/freeze` / `/guard` 가 Ralph 식 YOLO 의 안전 대안.
- 토큰 비용을 감수할 수 있는 개인 / 소규모 팀 (풀 스택 활성화 시 한 skill 당 10K+ 토큰).
- 다른 하네스와의 cherry-pick 스태킹 — decision layer 만 가져와서 GSD / Superpowers 의 execution layer 와 결합하는 **"gstack thinks, GSD stabilizes, Superpowers executes"** 패턴.

**쓰면 안 되는 영역**
- 이미 형태가 잡힌 기존 코드베이스의 retrofit — 명시적으로 "build with, not retrofit onto" 프레임워크.
- Build 단계가 핵심 리스크인 작업 — gstack 은 거기서 가장 약하다. Superpowers 의 TDD 나 GSD 의 context isolation 이 더 맞다.
- 토큰 예산이 빡빡한 프로덕션 운영 — 23 skill 풀 로딩은 가볍지 않다.
- LOC 메트릭을 진짜 KPI 로 쓰려는 조직 — 원칙적으로 ETHOS.md 와 모순.
- 1인 창업자 페르소나 전시가 아니라 **팀 프로세스**가 실제로 필요한 현장 — gstack 은 솔로 빌더의 "팀 시뮬레이터"이지 팀을 위한 도구가 아니다.

## 한국어 독자를 위한 참고

한국 커뮤니티에서는 2026년 3월 중순 Garry Tan 의 공개 직후 "지스택" 으로 종종 언급되었다. 다만 FastCampus 의 하네스 엔지니어링 강의나 Toss Tech 의 하네스 관련 글들이 gstack 을 직접 다룬 사례는 아직 확인되지 않았다. **tentenco (Ewan Mak) 의 Medium 비교글**이 3-framework 축 프레이밍의 원본이고, 그 위로 dev.to imaginex 의 스태킹 패턴이 파생됐다. 한국어 번역/재해석보다 원본을 직접 읽는 걸 권한다.

## 더 읽을거리

- **저자 본인** — [garrytan/gstack 레포](https://github.com/garrytan/gstack), [ETHOS.md](https://github.com/garrytan/gstack/blob/main/ETHOS.md), [CLAUDE.md](https://github.com/garrytan/gstack/blob/main/CLAUDE.md), [공식 랜딩 gstacks.org](https://gstacks.org/)
- **축 프레이밍** — [tentenco: Superpowers, GSD, gstack — What Each Claude Code Framework Actually Constrains](https://medium.com/@tentenco/superpowers-gsd-and-gstack-what-each-claude-code-framework-actually-constrains-12a1560960ad)
- **소개 & 아키텍처** — [Agent Native: Garry Tan's gstack — Running Claude Like an Engineering Team](https://agentnativedev.medium.com/garry-tans-gstack-running-claude-like-an-engineering-team-392f1bd38085), [awesomeagents.ai 가이드](https://awesomeagents.ai/guides/gstack-garry-tan-claude-code-guide/)
- **스태킹 패턴** — [dev.to imaginex: A Claude Code Skills Stack](https://dev.to/imaginex/a-claude-code-skills-stack-how-to-combine-superpowers-gstack-and-gsd-without-the-chaos-44b3), [UpayanGhosh/claude-jarvis intent router](https://github.com/UpayanGhosh/claude-jarvis)
- **비판** — [Hacker News 쓰레드 #47418576](https://news.ycombinator.com/item?id=47418576), [augmentcode: "I don't take that claim at face value"](https://www.augmentcode.com/learn/garry-tan-gstack-claude-code), [TechCrunch 2026-03-17](https://techcrunch.com/2026/03/17/why-garry-tans-claude-code-setup-has-gotten-so-much-love-and-hate/)

## 한 문장으로 덮기

gstack 은 "23개 슬래시 커맨드 skill-pack" 이 아니라 **"LLM 에게 어떤 역할의 시선으로 판단할지 명시적으로 부여한다"** 는 멘탈 모델이고, 그 모델은 600K LOC 주장이나 YC 대표 플랫폼 효과 없이도 오늘 당신의 프로젝트에 두 줄 프롬프트로 이식된다.
