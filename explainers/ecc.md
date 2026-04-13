---
title: Everything Claude Code (ECC) — 한 번 이해하고 가기
based_on: notes/harness/ecc.md
date: 2026-04-13
audience: user (Korean)
reading_time: ~8분
---

# Everything Claude Code — "설정 파일 번들"인가, "에이전트 레이어"인가

## 한 줄로

> 47개 에이전트 + 181개 스킬 + 72개 규칙 + 20개+ 훅 — 한 번 설치하면 에이전트가 알아서 역할을 맡는다.

ECC의 주장을 압축하면 이렇다. 에이전트에게 매번 같은 설정을 가르치는 게 지겹다면, 그 설정을 번들로 묶어 설치하면 된다. Affaan Mustafa는 이걸 "에이전트 하네스 성능 최적화 시스템"이라고 부른다. 거창한 이름 뒤에 있는 핵심은 훨씬 단순하다.

## 왜 태어났는가

Affaan은 2025년 2월 Claude Code 실험 출시 때부터 매일 써왔다. 10개월쯤 되자 반복 패턴이 쌓였다 — 새 프로젝트를 시작할 때마다 같은 코드 리뷰 기준을 설명하고, 같은 TDD 워크플로를 지시하고, 같은 보안 검토 체크리스트를 붙이는 일. 이 반복을 패키지로 만들어 설치하면 어떨까. 2025년 9월 Anthropic × Forum Ventures 해커톤(Cerebral Valley, NYC)에서 그는 8시간 만에 zenith.chat을 빌드해 $15,000 크레딧을 받았다. 그때 쓴 설정 묶음이 ECC의 씨앗이 됐다.

> "ECC is not just configs. It's a complete system: skills, instincts, memory optimization, continuous learning, security scanning, and research-first development." — README

2026년 1월 MIT 라이선스로 공개했고, 그가 X에 올린 "Shorthand Guide" 스레드가 90만 뷰, 1만 북마크를 기록하며 바이럴됐다. 이후 별점은 82K → 100K → 118K → 140K+(2026-04 기준)로 빠르게 올랐다. 다만 개발자 커뮤니티 일부는 "X 스레드 바이럴이 별점을 끌어올렸고 GitHub Discussions 활동은 미미하다"는 회의적 시각을 가지고 있다 — Ewan Mak(tentenco)의 지적이다.

## 실제로 어떻게 돌아가는가

ECC는 여러 실행 레이어가 중첩된 구조다. 간단히 정리하면:

1. **설치**: `./install.sh --profile full`(또는 Claude Code 플러그인 마켓플레이스). 단, rules는 플러그인으로 배포 불가 — `~/.claude/rules/`에 수동 설치 필수.
2. **SessionStart 훅 자동 실행**: 세션이 열리면 훅이 메모리 로드, 컨텍스트 최적화, 관련 스킬 인덱스 주입을 자동 처리.
3. **Progressive disclosure**: Claude는 181개 스킬의 이름·설명 인덱스만 먼저 로드하고, 태스크 컨텍스트와 관련된 스킬만 풀 본문으로 주입받는다. 컨텍스트 포화를 피하는 방법.
4. **역할 위임**: `/plan`을 치면 planner 에이전트가 받고, `/code-review`는 code-reviewer 에이전트가 받는다. 47개 전문화 에이전트가 태스크 유형에 따라 자동 위임된다.
5. **NanoClaw v2**: 하지 않은 모델 라우팅(태스크에 맞는 모델 자동 선택)과 스킬 핫로드를 오케스트레이션 레이어에서 처리. 내부 로직은 공개 문서 없음.
6. **Instinct 학습**: `/learn`으로 반복 패턴 추출 → confidence score 부여 → 높으면 영속 instinct로 승격, 낮으면 `/instinct-prune`으로 정리.
7. **Stop 훅**: 세션 종료 시 요약을 자동 저장해 다음 세션으로 기억을 전달.

Ralph가 "매 이터레이션마다 빈 컨텍스트에서 시작해 파일로 기억을 넘긴다"면, ECC는 "세션 사이에 SQLite + instinct store + session adapter 레이어가 상태를 유지한다"고 볼 수 있다. 더 풍부한 상태, 더 복잡한 디버깅.

## 왜 작동한다고 (저자는) 주장하는가

직접 수치는 많다. 997+ 내부 단위 테스트 통과, AgentShield 1,282 보안 테스트 98% 커버리지, 150+ GitHub App 설치, 170+ 컨트리뷰터. 그러나 이 수치들은 **내부 품질 지표이지 퍼포먼스 벤치마크가 아니다**. "997 tests passing"은 코드가 깨지지 않았다는 뜻이지 에이전트가 더 잘 코딩한다는 뜻이 아니다.

3자 평가 중 가장 구체적인 것은 Mak의 관찰이다. code-reviewer 에이전트의 **80% 신뢰도 필터링** — 이 기준 이하 이슈는 리포트하지 않는 — 이 실질적으로 리뷰 노이즈를 줄였다고 한다. TDD 스킬과 세션 요약 훅도 standalone 가치를 인정받았다. Mak의 결론은 온건하다: "전체를 설치하기보다, 에이전트·스킬 마크다운 파일을 읽고 자신의 워크플로에 맞는 패턴을 빌려라."

## 진짜 핵심 아이디어 하나

ECC를 둘러싼 논쟁의 핵심은 이것이다: **"완전한 에이전트 생태계"가 필요한 사람이 얼마나 되는가.**

비판 진영에서 가장 많이 들리는 말: "Most people just need a good CLAUDE.md, not an entire ecosystem." (Mak이 전달한 커뮤니티 목소리) YAGNI(You Ain't Gonna Need It) 원칙 관점에서 보면, 47개 에이전트와 181개 스킬은 대부분의 솔로 개발자나 소규모 팀에 과도하다. 이해하지 못한 채로 설치한 "블랙박스 슈퍼스트럭처"는 나중에 디버깅이 막막해진다.

그러나 ECC의 진짜 포지션은 다른 데 있다. Mak의 비교 프레임을 빌리면: Superpowers는 **프로세스**를 제약하고, GSD는 **실행 환경**을 제약하고, gstack은 **의사결정 관점**을 제약한다. ECC는 이 세 가지와 다른 차원이다 — **사전 구성된 역할·스킬 생태계 자체를 삽입**한다. 에이전트가 무엇을 해야 하는지(프로세스), 어떤 환경에서 실행할지, 어떤 시각으로 판단할지를 각각 다른 하네스가 담당한다면, ECC는 "누가 맡아서 할 것인가"를 사전 정의해두는 레이어다.

이식해야 할 멘탈 모델: **역할 위임의 사전 구성**. 에이전트에게 매번 "이번엔 보안 검토자처럼 생각해"라고 지시하는 대신, 보안 검토자 에이전트를 미리 정의해두고 호출하는 것.

## 가져갈 만한 것들

딥다이브 노트 §11에 8개의 이식 가능한 원시요소를 정리했다. 가장 즉시 쓸만한 것들:

1. **Progressive skill disclosure** — 스킬 인덱스만 먼저 주입하고 관련 스킬만 풀 로드. GSD의 carve-off와 같은 계열, 스킬 인벤토리에 특화. 어떤 런타임에도 적용 가능.
2. **Confidence-gated code review** — 80% 이상 신뢰도 이슈만 리포트. 노이즈 필터링 효과를 Mak이 독립적으로 확인한 유일한 컴포넌트. 단독 이식 가능.
3. **Role-specialized subagent delegation** — code-reviewer, security-reviewer, planner 세 역할만 골라도 대부분의 워크플로 커버. 47개 다 쓸 필요 없다.
4. **Hook-profile tiering** (`minimal|standard|strict`) — 환경변수 하나로 훅 수위 전환. 개발/CI/프로덕션 컨텍스트 적응에 즉시 이식 가능한 설계 패턴.
5. **Instinct learning loop (경량화 버전)** — 자동 학습보다는 수동 `/learn` → 파일 기반 instinct 목록이 더 이해 가능하고 안전하다. 개념만 이식하고 5-layer observer는 직접 구현하지 말 것.

ECC의 전체 스택을 가져올 필요는 없다. Mak의 권고처럼 스킬·에이전트 마크다운 파일을 읽고 이해한 것만 빌리는 것이 훨씬 안전하다.

## 조심할 것

### 저자/프로젝트 자인
- **플러그인 vs OSS installer 갭**: README가 직접 "OSS installer가 가장 안정적"이라고 인정. 플러그인 경로는 불안정 가능성 있음.
- **Rules 분리 설치**: 플러그인으로 rules 배포 불가, 수동 설치 필수. "Agents, skills, hooks, commands는 받지만 rules는 못 받는다"는 UX 단절.
- **Multi-model 커맨드 의존성**: `/multi-plan`, `/multi-execute`는 `ccg-workflow` 런타임 없으면 실패. 의존성 명시는 됐으나 설치 경로 복잡.

### 커뮤니티/3자 비판 (Mak, Mar 2026)
- **Over-engineering**: 997 내부 테스트와 오케스트레이션 엔진은 소규모 팀에 과도. "Most people just need a good CLAUDE.md."
- **Opacity risk**: 이해하지 못한 채 설치한 시스템은 디버깅 범위 밖으로 나간다. 블랙박스 채택의 고전적 위험.
- **Star count skepticism**: 유기적 채택 대 바이럴 별점 비율 미분리.

### 구조적 불투명 (분석 도출)
- **NanoClaw v2 내부 미공개**: 모델 라우팅 결정 로직을 알 수 없다. 의도치 않은 라우팅 결정이 어디서 오는지 추적 불가능할 수 있다.
- **Instinct confidence 평가 함수 미공개**: 자동 pruning 기준이 불명확한 상태에서 중요한 패턴이 제거될 위험.
- **ECC 2.0 (Rust) 미완성**: alpha 단계. 프로덕션 사용 권장 불가.

## 어디에 쓰고 어디에 쓰지 말까

**쓸만한 영역**
- 여러 AI 코딩 도구(Claude Code, Cursor, Codex)를 병행 사용하며 동일 기준을 유지하고 싶은 팀
- 반복적인 코드 리뷰·보안 감사·TDD 지침 설정에 시간을 쓰고 있는 팀
- ECC의 스킬/에이전트 파일을 읽고 이해한 뒤, 필요한 부분만 선택적으로 채택하는 경우
- 보안 감사(`/security-scan`, AgentShield)가 필요한 설정 파일 관리

**쓰면 안 되는 영역**
- 시스템 전체를 이해하지 못한 채 "일단 설치해보자"는 접근
- NanoClaw v2나 instinct confidence scoring의 내부를 알아야 디버깅할 수 있는 프로덕션 임계 워크플로
- ECC 2.0 alpha (Rust control-plane)를 프로덕션에 배포하는 경우
- 단일 하네스를 이미 잘 쓰고 있는 솔로 개발자 — 이미 좋은 CLAUDE.md가 있다면 ECC의 추가 복잡도가 가치를 넘어설 수 있다

## 더 읽을거리

- **저자** — [GitHub 레포](https://github.com/affaan-m/everything-claude-code), [릴리스 노트](https://github.com/affaan-m/everything-claude-code/releases)
- **균형 잡힌 분석** — [Ewan Mak (tentenco), Medium Mar 2026](https://medium.com/@tentenco/everything-claude-code-inside-the-82k-star-agent-harness-thats-dividing-the-developer-community-4fe54feccbc1)
- **기술 분해** — [bridgers.agency](https://bridgers.agency/en/blog/everything-claude-code-explained), [dev.to 치트시트](https://dev.to/shimo4228/everything-claude-code-ecc-complete-cheatsheet-24ok)
- **플러그인 메타데이터** — [ClaudePluginHub](https://www.claudepluginhub.com/plugins/affaan-m-everything-claude-code)

## 한 문장으로 덮기

ECC는 "에이전트 생태계"의 가장 야심찬 시도 중 하나이지만, 그 야심이 자산인지 부채인지는 당신이 그것을 이해하고 쓰는가 모르고 설치하는가에 달려 있다.
