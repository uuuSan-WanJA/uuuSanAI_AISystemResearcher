---
title: revfactory/harness — 한 번 이해하고 가기
based_on: notes/harness/revfactory-harness.md
date: 2026-04-13
audience: user (Korean)
reading_time: ~8분
---

# revfactory/harness — 하네스를 만드는 하네스

## 한 줄로

> "Build a harness for this project"

한 문장이 전부다. 이 한 마디를 Claude Code에서 치면 Harness가 도메인을 분석하고, 에이전트 팀을 설계하고, 스킬 파일 전체를 `.claude/` 디렉토리에 생성한다. **하네스를 만드는 하네스** — 메타-스킬이다.

만든 사람은 황민호(@revfactory). 제주에서 일하는 카카오 AI Native Strategy 팀 리더다. 2013년부터 Daum 검색, Moment 광고 플랫폼, OLIVE 오픈소스 플랫폼을 거쳐 지금은 AI 에이전트 전략을 연구한다. Claude Code 생태계에서 한국인 기여자가 2.4k 스타(2026-04 기준)를 받은 프로젝트는 극히 드물다. README_KO.md, README_JA.md까지 다국어 문서를 동시에 제공한다.

## 왜 태어났는가

황민호가 진단한 문제는 이렇다:

> "The bottleneck is structure, not capability. LLMs have sufficient knowledge — they lack project-specific structural guidance." — README (claude-code-harness)

LLM은 이미 충분히 똑똑하다. 문제는 구조다. 복잡한 도메인 작업을 단일 에이전트에 맡기면 품질이 낮고 편차가 크다. 멀티에이전트 팀을 직접 설계하려면 역할 분리, 스킬 파일 작성, 오케스트레이션 프로토콜 정의 같은 반복 보일러플레이트가 진입 장벽이 된다.

해결책이 Harness다. "사전 구조화(structured pre-configuration)"를 자동화한다. 경험 많은 엔지니어가 프로젝트를 시작할 때 가져오는 아키텍처 감각 — 그것을 에이전트 팀 형태로 자동 조립해 준다.

## 실제로 어떻게 돌아가는가

한 실행이 무슨 일을 하는지가 핵심이다. 트리거 순간부터:

1. **Phase 0 (상태 감사)**: 기존 `.claude/agents/`, `.claude/skills/`, `CLAUDE.md`를 읽는다. 신규 빌드인지, 기존 팀 확장인지, 유지보수인지 — 3가지 경로 중 하나로 분기.
2. **Phase 1 (도메인 분석)**: 프로젝트 코드베이스와 기술 스택 분석. 생성/검증/편집/분석 등 핵심 작업 유형 분류. 사용자의 기술 숙련도도 대화 단서에서 감지.
3. **Phase 2 (팀 아키텍처 설계)**: 실행 모드 선택(에이전트 팀 / 서브에이전트 / 하이브리드). 6개 아키텍처 패턴 중 선택 — Pipeline(순차), Fan-out/Fan-in(병렬), Expert Pool(선택), Producer-Reviewer(생성+검증), Supervisor(중앙조율), Hierarchical Delegation(재귀위임).
4. **Phase 3 (에이전트 정의 생성)**: `.claude/agents/{name}.md` 파일 생성. 역할, 원칙, 입출력 프로토콜, 에러 처리, 협업 규약 포함. 모든 Agent 툴 호출에는 `model: "opus"` 지정.
5. **Phase 4 (스킬 생성)**: `.claude/skills/{name}/SKILL.md` 파일 생성. YAML frontmatter + Markdown body 구조. "Pushy" description — 트리거 상황과 near-miss 구별을 명시.
6. **Phase 5 (통합 & 오케스트레이션)**: 팀 모드면 `TeamCreate → TaskCreate → SendMessage` 협업 체계. `CLAUDE.md`에는 트리거 규칙 + changelog만 — 에이전트 목록·디렉토리 구조·상세 규칙 금지.
7. **Phase 6 (검증 & 테스트)**: 2–3개 현실적 프롬프트로 스킬 테스트. with-skill vs. without-skill 비교. should-trigger / should-NOT-trigger 8–10개씩 트리거 검증.
8. **Phase 7 (하네스 진화)**: 실행 후 피드백 요청. 결과 품질→스킬, 역할 공백→에이전트 정의, 워크플로→오케스트레이터로 라우팅.

실행 결과물은 파일이다. `.claude/agents/`, `.claude/skills/`, `CLAUDE.md` 변경. 이 파일들이 다음 실행의 상태 기반이 된다.

Ralph의 `while true` 무한 루프와 달리, Harness는 **단일 실행 파이프라인**이다. 루프가 아니라 생성기.

## 왜 작동한다고 (황민호는) 주장하는가

통제 실험을 직접 수행해 논문으로 냈다. `revfactory/claude-code-harness` 저장소에 한국어·영어 PDF가 있다. 실험 구조도 공개되어 있다: 15개 태스크의 YAML 정의, baseline vs. harness 결과물 각각, 10차원 평가 JSON.

수치는 이렇다:
- 평균 품질: 49.5 → 79.3 (+60%)
- 승률: 15/15 (100%)
- 출력 분산: -32%

가장 주목할 발견은 **복잡도 스케일링**이다. Basic 태스크에서 +23.8점, Advanced에서 +29.6점, Expert에서 +36.2점. 어려울수록 구조 사전 설정의 효과가 커진다. 10차원 중 가장 큰 개선은 Test Coverage(+4.9)와 Architecture(+4.4) — 가이드 없는 에이전트가 테스트를 거의 생성하지 않고 단일 파일 구현으로 수렴하는 경향을 Harness가 깬다.

단, 황민호 본인이 수행한 실험이다. 제3자 독립 재현은 2026-04 기준 없다. "100% 승률"은 외부 검증 전까지 유보적으로 읽는 것이 맞다.

## 진짜 핵심 아이디어 하나

Harness의 본질은 "멀티에이전트 팀 자동 생성"이 아니다. 진짜 핵심은 **Progressive Disclosure** — 컨텍스트 관리 철학이다.

SKILL.md의 스킬 body는 트리거될 때만 로드된다. `references/`는 필요할 때만 조건부 로드. `scripts/`는 자체 포함해 독립 실행. 메타데이터만 항상 로드.

이것은 Ralph의 "매 루프 결정론적 preload"와 정반대 방향이다. Ralph는 항상 모든 것을 주입하고, Harness는 필요한 것만 점진적으로 열어준다. 두 전략 모두 컨텍스트 오염을 막는 방어 설계지만 방향이 다르다.

그리고 `CLAUDE.md` 원칙: 에이전트 목록, 디렉토리 구조, 상세 규칙 — 전부 금지. 트리거 규칙 + changelog만. "과도한 문서화가 컨텍스트를 오염한다"는 직접 언급. 이 미니멀리즘이 Harness가 생성한 팀 전체에도 전파되는 설계 원칙이다.

## 가져갈 만한 것들

딥다이브 노트 §11에 10개의 이식 가능한 원시요소를 정리했다. 핵심 5개:

1. **Phase-0 상태 감사**: 실행 전 기존 아티팩트 감사 → 3-way 분기(신규/확장/유지보수). Ralph의 IMPLEMENTATION_PLAN.md 재독과 같은 계열이지만 drift 탐지가 추가됨. 어느 에이전트 시스템에도 이식 가능.
2. **Progressive Disclosure**: 메타데이터 항상 → 본문 트리거 시 → 참조 조건부 → 스크립트 자체포함. 스킬 파일을 레이어로 구조화하면 컨텍스트 비용을 크게 줄일 수 있다.
3. **"Pushy" description**: 스킬 description에 트리거 상황 + near-miss 구별 명시. 자동 호출 정확도를 위한 precision engineering. should-trigger/should-NOT-trigger 8–10개 테스트와 함께.
4. **CLAUDE.md 최소화 원칙**: 트리거 규칙 + changelog만. 목록·구조·규칙 금지. Ralph의 AGENTS.md 분리 원칙과 같은 방향의 더 강한 제약.
5. **6 아키텍처 패턴 어휘**: Pipeline / Fan-out/Fan-in / Expert Pool / Producer-Reviewer / Supervisor / Hierarchical Delegation. 멀티에이전트 팀 설계할 때마다 재참조할 수 있는 도메인 독립적 어휘집.

## 조심할 것

저자 설계상 드러난 제약들:

- **실험적 기능 의존**: Agent Team 모드는 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 환경변수 필요. 실험 플래그 — 안정성 보장 없음.
- **메타-스킬의 오류 증폭**: Harness가 잘못된 도메인 분석을 하면 생성된 팀 전체가 오염된다. "garbage in, garbage in × 팀 규모"의 위험.
- **CLAUDE.md drift**: Phase 0 감사가 파일시스템 상태에 의존하므로, 외부 수동 편집 후 재실행 시 충돌 가능.
- **100% 승률의 외부 미검증**: 황민호 본인 실험만 있다. 15개 태스크 선택 기준과 편향성 통제 방법론 상세가 공개되지 않았다.
- **Agent Team 비용 미정량화**: 팀 실행의 토큰 비용 대비 품질 트레이드오프가 수치화되어 있지 않다.

## 어디에 쓰고 어디에 쓰지 말까

**쓸만한 영역**
- 반복되는 도메인(소프트웨어 개발, 콘텐츠, 데이터 분석)에서 팀 구성을 빠르게 부트스트랩하고 싶을 때
- 멀티에이전트 설계 경험이 없는 상태에서 시작점이 필요할 때
- harness-100 중 자신의 도메인과 가까운 것을 템플릿으로 골라 수정할 때
- Expert 수준 복잡도가 높은 태스크 (황민호의 실험에서 가장 효과가 큰 구간)

**쓰면 안 되는 영역**
- Agent Team 실험 기능이 불안정한 환경
- Harness가 한 번만 돌아가는 단순 태스크 (1회성 스크립트, 작은 수정)
- 도메인 분석이 거의 불가능한 극단적 신규 영역 (Harness도 코드베이스 없이는 판단 근거가 없다)
- 팀 비용(토큰)에 민감한 환경

## 한국어 독자를 위한 참고

이것은 한국인이 만든 Claude Code 생태계의 가장 많이 스타 받은 플러그인 중 하나다. 황민호는 카카오 AI 전략팀 리더라는 직함을 가진 상태에서 공개 연구로 기여했다 — 개인 프로젝트인지 회사 지원인지는 공개 불명이지만, 저자의 배경이 하네스 설계의 현장 실용성을 뒷받침한다.

한국어 커뮤니티에서 "하네스 엔지니어링"은 2026년 초부터 개념어로 자리잡고 있다. haandol, madplay 등 한국 개발자 블로그가 하네스 엔지니어링 개념을 다루지만, 직접 revfactory/harness를 언급하지는 않는다. 한국어 README_KO.md가 있어 한국어로 먼저 읽는 것도 가능하다 — 번역이 아니라 동시 제공이라 원문과 동일한 품질.

"하네스 구성해줘" 라는 한국어 트리거가 공식 README에 예시로 실려 있다는 것 자체가, 이 도구가 한국어 사용자를 1등 시민으로 설계한 증거다.

## 더 읽을거리

- **저장소** — [revfactory/harness](https://github.com/revfactory/harness), [README_KO.md](https://github.com/revfactory/harness/blob/main/README_KO.md)
- **실험 & 논문** — [revfactory/claude-code-harness](https://github.com/revfactory/claude-code-harness) (experiments/, paper/ PDF)
- **100-harness 라이브러리** — [revfactory/harness-100](https://github.com/revfactory/harness-100) (200 패키지, 한국어/영어)
- **공식 랜딩** — [revfactory.github.io/harness](https://revfactory.github.io/harness/)
- **저자 프로필** — [github.com/revfactory](https://github.com/revfactory)

## 한 문장으로 덮기

Harness는 "멀티에이전트 팀 생성기"가 아니라 **"구조 사전 설정이 복잡도에 비례해 효과를 낸다"**는 실험 기반 주장이고, 그 주장을 한 번에 검증하고 적용하는 메타-스킬이다.
