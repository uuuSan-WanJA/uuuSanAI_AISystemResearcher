---
title: OpenSpec — 한 번 이해하고 가기
based_on: notes/harness/openspec.md
date: 2026-04-13
audience: user (Korean)
reading_time: ~8분
---

# OpenSpec — "왜 이 변경을 했는가"를 코드와 함께 보존하는 프레임워크

## 한 줄로

> `/opsx:propose` → 스펙 리뷰 → `/opsx:apply` → 리뷰 → `/opsx:archive`

OpenSpec은 이 세 단계 루프가 전부다. 각 단계 사이에 사람이 리뷰한다. 루프가 한 번 돌면 하나의 기능 변경이 끝나고, 스펙이 코드와 함께 히스토리에 남는다. 2026년 1월 v1.0.0으로 정식 출시된 이후 GitHub에서 39.6k 스타를 받은 Fission-AI의 Spec-Driven Development 프레임워크다.

## 왜 태어났는가

OpenSpec 저자들의 진단은 두 가지다.

첫째, **컨텍스트 소멸**. LLM 세션이 닫히면 "왜 이 결정을 내렸는가"가 사라진다. 다음 세션의 에이전트는 이전 세션의 의도를 알 수 없어 이미 완료된 기능을 재구현한다. heyuan110.com 비교 포스트에서 저자 본인이 직접 경험한 실패로 등장한다: "Finished a feature, skipped `/opsx:archive`. Next session, AI read the old spec and reimplemented existing functionality."

둘째, **브라운필드 외면**. 대부분의 AI 코딩 도구는 처음부터 시작하는 그린필드를 가정한다. OpenSpec은 반대 방향을 택한다.

> "Most tools assume you're starting fresh. We focus on mature codebases where the real struggle is figuring out how the current system works." — openspec.dev

이 포지션이 Ralph Wiggum("그린필드 외주 대체재")이나 Spec Kit("그린필드 0→1")과 OpenSpec을 가르는 핵심 선택이다.

## 실제로 어떻게 돌아가는가

한 번의 기능 변경 사이클이 어떻게 흘러가는지 추적해본다.

1. `openspec init`으로 프로젝트를 초기화하면 `openspec/specs/`(소스 오브 트루스)와 `openspec/changes/`(변경 격리 폴더)가 생긴다
2. `/opsx:propose add-2fa`를 실행하면 에이전트가 `openspec/changes/add-2fa/` 폴더를 만들고 네 개의 아티팩트를 생성한다: `proposal.md`(왜 하는가, 스코프), `design.md`(어떻게 하는가), `tasks.md`(구현 체크리스트), `specs/`(delta 스펙)
3. delta 스펙은 이런 구조다:
   ```
   ## ADDED Requirements
   ### Requirement: 2FA 인증
   GIVEN 사용자가 2FA를 활성화한 상태에서
   WHEN 올바른 아이디/비밀번호를 입력하면
   THEN 시스템은 토큰 직접 발급 대신 OTP 챌린지를 반환해야 한다
   ```
4. 사람이 아티팩트를 리뷰하고 OK 하면 `/opsx:apply`로 구현에 들어간다
5. 구현이 끝나면 `/opsx:verify`로 코드가 아티팩트와 일치하는지 검증한다
6. `/opsx:archive`로 변경을 완료한다 — delta 스펙이 `openspec/specs/`의 main spec에 병합되고, change 폴더 전체가 타임스탬프 디렉토리에 보존된다

다음 기능 변경은 1번부터 다시 시작한다. 이전 세션의 추론은 없지만, 파일에 기록된 **의도와 결정 이력**은 영구히 남는다.

## 왜 작동한다고 저자는 주장하는가

공식 문서와 서드파티 분석에서 반복 등장하는 주장들이다.

**변경 격리가 팀 충돌을 막는다**: 각 기능이 독립된 `changes/<name>/` 폴더에서 진행되므로 여러 사람이 동시에 작업해도 main spec이 깨지지 않는다. "OpenSpec's biggest advantage is its change isolation mechanism. SpecKit tends to directly modify main spec files, easily causing conflicts." — redreamality.com

**감사 추적(audit trail)**: archive된 폴더가 "왜 이 변경을 했는가"를 코드 수준이 아닌 의도 수준에서 보존한다. git blame이 줄 단위 추적이라면 OpenSpec archive는 결정 맥락 수준의 추적이다.

**도구 독립성**: Claude Code, Cursor, Windsurf, Gemini CLI, Copilot 등 21개 도구에서 동일한 워크플로가 작동한다. npm으로 설치하고 파일시스템만 있으면 되므로 외부 SaaS 의존이 없다.

수치 데이터는 거의 없다. "컨텍스트 40% 초과 시 AI 성능이 현저히 저하된다"는 주장이 redreamality.com 분석에 등장하지만 1차 출처가 명시되지 않아 검증이 안 된다. 통제된 벤치마크는 없다.

## 진짜 핵심 아이디어 하나

bswen.com 비교 분석이 가장 간결하게 OpenSpec의 본질을 짚는다:

> "OpenSpec excels at decision traceability, while Superpowers excels at execution quality."
> "Does your team care more about documenting why changes were made, or enforcing how changes are implemented?"

OpenSpec이 실제로 해결하는 문제는 "에이전트가 코드를 더 잘 쓰게 한다"가 아니다. **"변경의 이유가 코드와 함께 살아남는다"**가 핵심이다. 이 관점에서 보면 OpenSpec은 AI 코딩 도구가 아니라 **AI 시대의 의사결정 기록 시스템**에 가깝다.

heyuan110 포스트의 포지션도 같은 방향이다:

> "OpenSpec handles planning, Superpowers handles coding discipline, Claude Code executes. They don't conflict — each owns its stage."

서로 경쟁하는 게 아니라 레이어를 나눠 갖는다.

## 가져갈 만한 것들

§11에 8개의 이식 가능한 primitive를 정리했다. 가장 즉각 쓸 수 있는 것들을 고르면:

1. **델타 마커 스펙 포맷** — `## ADDED / MODIFIED / REMOVED Requirements` 섹션으로 변경 전후를 명시. 전체 스펙을 다시 쓰지 않고 diff만 기술한다. 어느 Markdown 스펙 파일에도 즉시 적용 가능한 컨벤션.

2. **change 폴더 격리 단위** — 하나의 기능 변경 = 하나의 폴더. proposal + design + tasks + delta specs가 한 묶음. 완료 전까지 main spec과 독립. PR 브랜치와 자연스럽게 매핑된다.

3. **스펙을 행동 계약으로 쓰기 (RFC 2119 + Gherkin)** — MUST/SHALL/SHOULD + GIVEN/WHEN/THEN으로 구현 방법이 아닌 관찰 가능한 외부 동작만 기술. 에이전트가 스펙을 acceptance test 기준으로 읽도록 유도한다.

4. **archive = 의도 수준 커밋** — 코드 커밋이 코드 변경을 기록하듯, archive가 의사결정 맥락을 보존. "왜 이 변경을 했는가"를 나중에 다른 에이전트(또는 사람)가 읽을 수 있는 형태로 남긴다.

5. **explore-before-commit 탐색 모드** — `/opsx:explore`는 아티팩트 없이 아이디어를 탐색하는 모드. 커밋 없는 탐색과 아티팩트 생성을 분리하는 원칙은 Ralph의 plan/build 분할, Superpowers의 phase gate와 같은 계열.

## 조심할 것

### 저자 인정 (간접, 문서에서)
- **Archive 스킵 시 재구현 루프**: archive를 빠뜨리면 다음 세션이 이미 완료된 기능을 재구현한다. 저자가 경고로 명시.
- **스펙이 pseudocode가 되는 함정**: 구현 단계를 스펙에 쓰면 AI가 대안적 해법을 못 고른다. 스펙은 행동 기술, 구현 지시가 아님.

### 3자 관찰
- **TDD 미강제** (bswen.com): "The framework assumes I'm disciplined enough to write tests." 테스트 작성은 사람 자기절제에 전적으로 의존. Superpowers와의 최대 차이점이 여기다.
- **단일 에이전트 모델** (bswen.com): "No built-in code review mechanism." 멀티에이전트 리뷰 루프 없음. `tasks.md` 체크리스트를 사람이 활용해야 의미가 있다.
- **수동 Git 워크플로**: 브랜치 격리나 자동 git 커밋 규율 강제 없음. Ralph의 "per-iteration commit+push"와 대비되는 수동 운영.
- **Plan Mode 제약**: Claude Code의 Plan Mode에서 직접 파일 조작 불가 — archive를 CLI로 수동 실행해야 한다 (redreamality.com 지적).

### 규모에 따른 오버헤드
- 30분짜리 작업에 proposal/design/tasks 풀 파이프라인을 적용하면 오버헤드가 이득보다 크다. heyuan110의 권고 기준: 2시간 이하 작업엔 Claude Code only.

## 어디에 쓰고 어디에 쓰지 말까

**쓸만한 영역**
- 기존 프로덕션 코드베이스의 점진적 기능 추가 (브라운필드 1→n)
- 여러 사람이 동시에 다른 기능에 손대는 팀 환경
- 변경 이유를 감사 추적해야 하는 컴플라이언스 요구사항이 있는 프로젝트
- 장기간 유지보수해야 하는 시스템 (의사결정 맥락 보존이 중요)
- 4시간 이상 걸리는 복잡한 기능 변경

**쓰면 안 되는 영역**
- 2시간 이하 단발 작업 — 오버헤드가 이득보다 큼
- TDD 강제가 필요한 팀 — OpenSpec 혼자로는 테스트 규율 없음 (Superpowers 병행 필요)
- 진짜 그린필드 부트스트랩 — Spec Kit 또는 Ralph가 더 적합
- 빠른 실험/프로토타입 — 스펙 정의가 탐색을 늦춤

## 더 읽을거리

- **공식** — [GitHub 레포](https://github.com/Fission-AI/OpenSpec), [openspec.dev](https://openspec.dev), [개념 문서](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md), [v1.0.0 릴리즈](https://github.com/Fission-AI/OpenSpec/releases/tag/v1.0.0)
- **비교 분석** — [heyuan110: Claude Code + OpenSpec + Superpowers 3-way](https://www.heyuan110.com/posts/ai/2026-04-09-claude-code-openspec-superpowers/), [bswen: OpenSpec vs Superpowers](https://docs.bswen.com/blog/2026-03-27-openspec-vs-superpowers/)
- **딥다이브** — [redreamality: OpenSpec 아키텍처 심층 분석](https://redreamality.com/garden/notes/openspec-guide/)

## 한 문장으로 덮기

OpenSpec은 "에이전트가 코드를 더 잘 쓰게 하는" 도구가 아니라 **"왜 이 코드가 이렇게 됐는지를 코드와 함께 살아남게 하는"** 의사결정 보존 시스템이다.
