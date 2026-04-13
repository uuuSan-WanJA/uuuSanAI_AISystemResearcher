---
title: Compound Engineering
slug: compound-engineering
date: 2026-04-13
author: Kieran Klaassen (GM of Cora) + Dan Shipper (CEO, Every)
primary_sources:
  - https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents
  - https://every.to/guides/compound-engineering
  - https://github.com/EveryInc/compound-engineering-plugin
status: deep-dive
confidence: high
rounds: 3
axes_used: [1,2,3,4,5,6,7,8,9,10,11,12]
axes_added: [L-variant]
axes_dropped: []
candidate_axis_proposals: []
candidate_axis_reuse: [A, C, F, K, L]
---

## TL;DR (3줄)
Compound Engineering은 Every.to가 사내에서 사용하는 Plan→Work→Review→Compound 루프 기반 AI 네이티브 개발 하네스다. 핵심은 네 번째 단계 "Compound"로, 매 이터레이션이 해결한 문제·학습한 패턴을 `docs/solutions/` + `CLAUDE.md`에 기록해 **다음 이터레이션이 같은 실수를 자동 회피**하는 자기강화 루프를 만든다. 14개 병렬 리뷰 서브에이전트, 50+ 에이전트 `/lfg` 엔드투엔드 커맨드, 14.2k GitHub 스타(14.2k ⭐, 1.1k forks, 620+ commits, v2.65.0 릴리즈)가 실질적 채택 신호다.

---

## Proposed schema deltas
- **축 L 재사용(강)**: Compound 단계의 `/ce:compound` → `docs/solutions/` → 베스트프랙티스 에이전트의 "genetic search" → 다음 `/ce:plan` 컨텍스트 주입 루프는 ECC의 `/learn`→`/evolve` 사이클과 독립된 2번째 강한 사용 사례. **축 L("instinct learning as harness layer") 승격 권고 충족.**
- **축 C 재사용(7번째)**: Brainstorm/Plan/Work/Review/Compound 5-모드 분할 + `/lfg` 통합 모드. 축 C 승격 확정 근거 추가.
- **축 F 재사용(4번째)**: 26개 전문화 에이전트 + 13개 스킬 + 23개 workflow 커맨드 → SKILL.md 컨벤션 레이어. 축 F 승격 근거 추가.
- **축 A 재사용(4번째)**: Compound 이터레이션 경계 = `docs/solutions/` 파일 커밋 + `CLAUDE.md` 갱신 + 다음 루프에서 자동 재로드. 축 A("iteration-boundary semantics") 4번째 독립 사용.
- **축 K 재사용(3번째)**: 14개 리뷰 에이전트는 각각 역할/페르소나에 결박(security-sentinel, dhh-rails-reviewer, performance-oracle). 축 K("role perspective as constraint surface") 3번째 사용 → 승격 확정 권고.

---

## 1. Identity & provenance
- **저자**: Kieran Klaassen (GM of Cora, Every.to) — 메소돌로지 설계자. Dan Shipper (CEO, Every.to) — 공동 저자, 사내 채택 책임.
- **첫 공개**: 2025-12-11 (Chain of Thought 블로그 포스트). 가이드 페이지는 2026-02-09 초판 → 2026-03-13 갱신 → 2026-04-06 재갱신.
- **배포 방식**: Every.to 블로그 + GitHub 오픈소스 플러그인 (`EveryInc/compound-engineering-plugin`, MIT)
- **GitHub 채택 신호**: ⭐14.2k, 1.1k forks, 620+ commits, v2.65.0 (94 릴리즈), issues 38, PRs 23 (2026-04 기준)
- **다중 플랫폼 지원**: Claude Code, Cursor, OpenCode, Codex, Droid, Pi, Gemini, Copilot, Kiro, Windsurf, OpenClaw, Qwen Code (TypeScript CLI로 변환)
- **팟캐스트**: "Compound Engineering: Manage Teams of AI Agents with Kieran Klaassen of Cora" (This New Way, 2025-10-09)
- **사내 적용**: Every.to가 5개 내부 프로덕션 제품을 이 하네스로 운영 중 (각 제품당 주로 1인 엔지니어 담당)

## 2. Problem framing
저자의 핵심 문제의식은 **전통적 코드베이스의 엔트로피 역전**이다:

> "Each unit of engineering work should make subsequent units easier—not harder."

기존 개발에서는 피처가 쌓일수록 복잡도가 높아지고, 새 팀원은 기존 코드를 이해하는 데 오랜 시간이 걸린다. Compound Engineering은 이 방향을 뒤집어 매 이터레이션이 축적한 학습이 다음 이터레이션을 더 빠르게 만드는 "복리" 구조를 제안한다.

부수적으로 "완벽한 첫 구현" 문화를 비판한다:

> "95% garbage rate typical; iterate faster than hand-coding"

그리고 코드 중심 역할에서 시스템 중심 역할로의 전환을 선언한다:

> "Code is just one input in that job—planning, reviewing, and teaching the system all count too."

"8가지 버려야 할 믿음" 중 핵심: "코드가 1차 아티팩트"가 아니라 코드를 생성하는 **시스템**이 1차 아티팩트다.

## 3. Control architecture
**루프 구조**: Plan → Work → Review → Compound → (반복). 선택적으로 앞에 Brainstorm/Ideate 단계 추가.

```
Brainstorm → Plan → Work → Review → Compound → Repeat
               ↑
            Ideate (optional)
```

**Anthropic 분류 매핑**:
- `/ce:plan`: 3개 병렬 연구 에이전트 스폰 → 결과 통합 → 계획 문서 생성 (LLM-directed workflow)
- `/ce:work`: 계획 단계적 실행 + git worktree 격리 (agent 자율)
- `/ce:review`: 14+ 전문 에이전트 병렬 심사 (LLM-directed workflow, 결과 P1/P2/P3 우선순위화)
- `/ce:compound`: 학습 추출 → `docs/solutions/` YAML 태깅 → `CLAUDE.md` 갱신 (agent-human hybrid)
- `/lfg`: plan → build → review → fix → merge의 50+ 에이전트 엔드투엔드 (고자율)

**종료 조건**: 명시적 PR 승인. `/lfg`는 "until PR is up with screenshots and videos and tested in a browser."

**시간 할당**: 80% Plan + Review, 20% Work + Compound. "Most thinking occurs before and after code writing."

**자기강화 루프**: Compound 단계 산출물(`docs/solutions/`, `CLAUDE.md`)이 다음 루프의 Plan 단계 컨텍스트로 자동 재주입 — 하네스 자체가 이터레이션마다 재구성된다.

## 4. State & context model
**지속 상태 파일 구조**:
```
your-project/
├── CLAUDE.md              # 에이전트 지시, 선호도, 재사용 패턴 (매 세션 자동 로드)
├── docs/
│   ├── brainstorms/       # /ce:brainstorm 출력
│   ├── solutions/         # /ce:compound 출력 (YAML frontmatter 태깅)
│   └── plans/             # /ce:plan 출력
└── todos/                 # P1/P2/P3 찾기(finding) 트래킹
    ├── 001-ready-p1-fix-auth.md
    └── 002-pending-p2-add-tests.md
```

**이터레이션 경계 (축 A)**:
- 리셋: 각 `/ce:*` 커맨드의 에이전트 컨텍스트 창
- 커밋: `docs/solutions/` 파일 (새 학습), `CLAUDE.md` 업데이트, `todos/` 상태 갱신
- 다음 루프 전파: `CLAUDE.md`는 모든 에이전트 세션에서 자동 로드됨. `docs/solutions/`는 베스트프랙티스 에이전트가 "genetic search"로 관련 패턴만 추출해 주입 (컨텍스트 오염 방지)
- 외부 액션: git worktree 생성/병합, GitHub PR 생성

**모델이 매 세션에서 보는 것**: `CLAUDE.md` (누적 학습) + 관련 `docs/solutions/` 스니펫 + 현재 작업 계획 + 코드베이스

**핵심 설계 원칙**: `CLAUDE.md`는 Compound 단계에서만 갱신됨. "CLAUDE.md failures trigger additions for auto-correction next time."

## 5. Prompt strategy
**모드 분할 (축 C)**: 5개 명시적 모드. Brainstorm(발산 탐색) / Plan(수렴 설계) / Work(실행) / Review(평가) / Compound(학습 추출). 각 모드는 별도 커맨드로 호출, 자동 전환 없음 — 사람이 단계 진행을 결정.

**베스트프랙티스 에이전트의 "genetic search"**: 리뷰·플래닝 단계에서 `docs/solutions/` 전체를 검색, 문맥적으로 관련된 패턴만 선별 주입. "Creating a custom knowledge base without bloating context windows." (Kieran 설명)

**전략적 질문 3개** (리뷰 승인 전):
> "What was the hardest decision you made here?" / "What alternatives did you reject, and why?" / "What are you least confident about?"

**선호도 코딩**: CLAUDE.md + 스킬 파일에 "taste"(색상·간격·타이포그래피·컴포넌트 패턴) 추출 → 재사용 가능한 단위로 고정.

**"/lfg" 프롬프트 패턴**: 단일 자연어 아이디어 → 50+ 에이전트가 나머지 처리. 출력: PR + 스크린샷 + 영상 + 브라우저 테스트.

**DHH 페르소나 리뷰어**: 강한 의견을 가진 리뷰어 페르소나("controversial suggestions force reconsideration of architectural choices").

**계획 중심 지향**: Kieran — "when we started AI coding, we just kind of forgot to plan. It was like one shot everything." 현재는 계획 문서가 "코드의 소스 오브 트루스"로 기능.

## 6. Tool surface & permission model
**실행 환경**: Claude Code 주력 (Cursor, OpenCode, Codex 등 멀티 지원)

**도구**:
- MCP: Playwright (브라우저 자동화), XcodeBuildMCP (iOS/Mac 빌드)
- `/ce-setup` 부트스트랩: agent-browser, gh, jq, vhs, silicon, ffmpeg 설치 확인
- git worktrees: 격리된 실험 브랜치
- GitHub CLI (PR 생성, 브랜치 관리)

**퍼미션 모델**: `--dangerously-skip-permissions` 권장 (속도를 위해). 단, 가이드가 명시적으로 조건 제시:
- 사용할 때: 프로세스 신뢰, 안전한 샌드박스, 속도 우선
- 피할 때: 학습 중, 프로덕션 코드, 롤백 불가

**안전 메커니즘**: git reset, 테스트, PR 리뷰, git worktrees ("safety nets replace review gates")

**26개 전문 에이전트 카테고리**: review(14), research, design, workflow automation, documentation

**멀티 플랫폼 동기화**: `bunx @every-env/compound-plugin sync` — Claude Code 로컬 설정을 10+ 다른 IDE에 동기화.

## 7. Human-in-the-loop points
**주요 게이트**:
1. Plan 승인 — "Plan approval is explicit (not silence)" (팀 협업 표준)
2. PR 리뷰 — PR owner가 인간 리뷰어. 단, 초점은 "intent, not syntax/security/style (에이전트 처리)."
3. Compound 단계 — 인간이 중요한 학습을 선별하고 `CLAUDE.md`에 추가할지 결정

**자율 최대화**: `/lfg`는 "plan→build→review→fix→merge"를 인간 없이 처리. 인간은 최종 PR을 보고 승인.

**어댑테이션 사다리**: Stage 0(수동) → Stage 5(병렬 클라우드, 랩탑 불필요). Stage 3부터 Compound Engineering 적용 시작.

**새 팀 역할 다이나믹**: "Person A creates plan → AI implements → AI agents review → Person B reviews AI review → Merge." PR 소유권은 사람 엔지니어에게 있다.

## 8. Composability
**다중 플랫폼 이식성**: TypeScript CLI(`bunx @every-env/compound-plugin install compound-engineering --to [target]`)로 OpenCode/Codex/Droid/Pi/Gemini/Copilot/Kiro/Windsurf/OpenClaw/Qwen Code 에 설치 가능.

**스킬 컨벤션 레이어 (축 F)**:
- 26개 전문화 에이전트 파일
- 13개 스킬 파일 (agent-native architecture, style guides, 도메인 전문성)
- 23개 workflow 커맨드
- Cursor는 `.cursor-plugin/`, Claude Code는 `.claude-plugin/`에 별도 형식으로 변환

**외부 하네스 결합**: Angelo Lima의 비교 분석이 제안하는 SDD + Compound Engineering 결합: "Use OpenSpec for structuring complex changes, execute through the compound loop, then archive learnings alongside specs." 이론적 결합이지 실제 검증된 패턴은 아님.

**설정 동기화**: `bunx @every-env/compound-plugin sync` — `~/.claude/` 스킬·커맨드·MCP 서버를 다른 IDE에 심링크/복사.

**개인 커스터마이징**: `/skill-create`로 사용자 정의 스킬 추가 가능.

## 9. Empirical claims & evidence
**저자 주장 (Every.to 사내, 일화 + 사용 통계)**:
- "A single developer can do the work of five developers a few years ago"
- Every.to는 5개 프로덕션 제품을 각각 주로 1인으로 운영, 수천 명 일일 사용자
- Kieran이 Cora(AI 이메일 어시스턴트)를 이 방법으로 단독 구축

**플러그인 채택 지표**:
- GitHub: ⭐14.2k, 1.1k forks (2026-04 기준, 공개 후 ~4개월)
- v2.65.0까지 94 릴리즈 — 활발한 유지보수 신호

**효율 비율 주장**:
- 80/20 시간 배분 (Plan+Review / Work+Compound)
- "50/50 rule": 50% 피처 구축 vs. 50% 시스템 개선 (전통 90/10 대비)

**증거 유형**: 내부 사례 + 채택 지표. 통제된 벤치마크 없음. 14.2k 스타는 인식론적 관심의 지표이지 효과 측정치가 아님.

## 10. Failure modes & limits
### 저자 인정 한계
- `--dangerously-skip-permissions` 사용의 위험성 — 명시적으로 조건 부여: "Avoid when: learning, production code, no rollback capability"
- **Compound 단계 규율 의존**: "Depends on developer discipline during the Compound phase." — 스킵하면 일반 AI 보조 개발과 차이 없음
- **첫 시도 품질 낮음**: "95% garbage rate typical" — 반복이 전제임

### 3자 관찰 (Angelo Lima, 2026)
- **업스트림 스펙 부재**: "Lacks formal upstream specification" — 복잡한 프로젝트에서 계약적 엄밀성 부족
- **규제 환경 부적합**: "Less suitable for regulated environments requiring audit trails"
- **모델 품질 의존**: "Quality depends heavily on the underlying model (some LLMs struggle to correctly parse structured Markdown files)"

### 구조적 한계 (하네스 분석)
- **CLAUDE.md 비대화 위험**: 매 이터레이션 학습이 누적되면서 CLAUDE.md 크기가 컨텍스트 창을 침식할 수 있음. "genetic search"가 완화책이나 장기 운영 시 검증 필요.
- **병렬 에이전트 비용**: 50+ 에이전트 `/lfg`는 고비용. 가이드가 비용 추정치를 미제공.
- **인간 taste 의존**: "Extract taste into the system" 명제는 결국 인간이 명확한 취향·기준을 가지고 있어야 함. 취향이 없으면 시스템화도 없음.
- **AI 코드 복잡성 과잉**: Dev|Journal(2026-04-10) — "AI tends to generate solutions with excessive complexity; locally reasonable decisions that compound into poor system architecture."

## 11. Transferable primitives ★ (load-bearing)

### P1. Compound step — 학습의 아티팩트화
- **설명**: 매 이터레이션 후 "무엇이 작동했고 무엇이 안 됐는가"를 YAML frontmatter 태깅된 마크다운으로 `docs/solutions/`에 저장. 단순 기록이 아니라 **검색 가능한 지식 베이스**로 승격.
- **전제**: 파일시스템 R/W, 에이전트가 YAML frontmatter를 파싱·검색 가능.
- **standalone-extractable**: YES. CLAUDE.md 갱신과 분리해서도 적용 가능. "Learn from past bugs" 원시요소로 독립 이식 가능.
- > "each bug, failed test, or a-ha problem-solving insight gets documented and used by future agents"

### P2. Genetic search over accumulated solutions
- **설명**: 플래닝·리뷰 단계에서 누적된 `docs/solutions/`를 전부 컨텍스트에 넣지 않고, 베스트프랙티스 에이전트가 관련된 것만 추출해 주입 ("genetic search"). 컨텍스트 폭발 없이 기관 기억 활용.
- **전제**: 전용 검색 에이전트, 문서에 일관된 메타데이터.
- **standalone-extractable**: PARTIAL. 별도 에이전트 역할 필요. 원리(full-load 대신 selective retrieval)는 이식 가능.
- (Kieran — "creating a custom knowledge base without bloating context windows")

### P3. 80/20 phase inversion (plan+review heavy)
- **설명**: 기존 90% 구현 + 10% 리뷰를 뒤집어 80% Plan+Review, 20% Work+Compound로 투자. "Plans are the new code."
- **전제**: 에이전트가 구현을 담당할 수 있어야 함. 인간의 역할을 설계·판단으로 한정.
- **standalone-extractable**: YES. 조직 프로세스 원칙으로 독립 적용 가능.

### P4. 14 parallel specialized review agents (P1/P2/P3 priority output)
- **설명**: 코드 리뷰를 한 에이전트가 일반 리뷰하는 대신, 14개 도메인 전문 에이전트(security-sentinel, performance-oracle, dhh-rails-reviewer...)가 병렬 심사 후 P1/P2/P3로 우선순위화.
- **전제**: 충분한 에이전트 스폰 비용, 전문 리뷰어 페르소나 파일.
- **standalone-extractable**: PARTIAL. P1/P2/P3 우선순위화 패턴은 독립 이식. 14개 에이전트 풀은 플러그인 의존.
- (축 K 직접 구현체: 역할 페르소나를 리뷰 품질 제어 장치로 사용)

### P5. CLAUDE.md as living system spec
- **설명**: CLAUDE.md는 단순 지시 파일이 아니라 매 Compound 단계에서 갱신되는 **시스템의 누적 지성**. 새 팀원이 읽으면 기존 팀원의 경험이 전달됨. "A new hire as well-armed to avoid common mistakes as someone on the team for a long time."
- **전제**: 모든 에이전트 세션이 CLAUDE.md를 자동 로드, 편집 규율.
- **standalone-extractable**: YES. 다른 하네스(Ralph의 AGENTS.md + IMPLEMENTATION_PLAN.md 분리 원칙)에서도 같은 방향이 관찰됨.

### P6. /lfg (Let's F'ing Go) — 엔드투엔드 자율 파이프라인
- **설명**: 단일 아이디어 입력 → 50+ 에이전트가 plan→build→review→fix→merge까지 처리 → 인간이 PR을 확인. 최고 자율성 모드.
- **전제**: 안전한 샌드박스, 테스트 커버리지, git rollback 능력.
- **standalone-extractable**: PARTIAL. 원리(end-to-end 파이프라인 단일 커맨드화)는 이식 가능. 실현은 플러그인 생태계 의존.

### P7. Adoption ladder (Stage 0→5)
- **설명**: 5단계 사다리로 조직/팀이 어디에 있는지 진단하고 다음 한 단계만 개선. Stage 3(Plan-first, PR-only review)에서 Compound Engineering 본격 적용.
- **전제**: 팀이 단계를 인식하고 의도적으로 이동할 의지.
- **standalone-extractable**: YES. 다른 하네스 온보딩 프레임워크로 독립 이식.

### P8. Git worktrees for risky work isolation
- **설명**: 위험하거나 탐색적인 작업은 git worktree로 격리. 실험과 메인 코드베이스 사이 오염 방지.
- **전제**: git, worktree 지원.
- **standalone-extractable**: YES. 일반 개발 원칙.

### Rejected as primitive
- "50+ 에이전트를 항상 쓸 것" — 비용 추정 없이 규모 복사는 부채. `/lfg`의 자율성 원칙은 이식하되, 에이전트 수는 실제 필요에 따라 결정할 것.
- "모든 것을 CLAUDE.md에 넣을 것" — CLAUDE.md 비대화는 Ralph의 "bloated AGENTS.md" 실패 패턴과 동일. Genetic search가 완화책이나 크기 제한 정책 필요.

## 12. Open questions
- **Compound 단계 사람 개입 정도**: 가이드는 에이전트가 `/ce:compound`를 실행하지만 사람이 검토한다고 암시. 실제로 에이전트 자율 실행 비율 vs. 사람 편집 비율 불명확.
- **CLAUDE.md 크기 한계**: 장기 운영 시 크기 관리 정책이 명시되지 않음. "Genetic search" 에이전트의 구체 구현(임계값, 유사도 기준) 불명확.
- **비용 데이터**: `/lfg` 50+ 에이전트 실행의 실제 Claude API 비용 사례가 없음.
- **브라우저 자동화 안정성**: Playwright MCP 통합의 플레이크니스(flakiness) 보고 없음.
- **Stage 5 실증 사례**: "병렬 클라우드 실행, 랩탑 불필요" 단계의 실제 사례 불명확.
- **한국어 커뮤니티 재현**: 영어 검색으로 한국어 적용 사례 미노출.

---

## Sources

### Primary (Every.to / Klaassen)
- https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents — 원글, 2025-12-11 (갱신 2026-04-06)
- https://every.to/guides/compound-engineering — 가이드, 2026-02-09 (갱신 2026-04-06)
- https://github.com/EveryInc/compound-engineering-plugin — 플러그인 레포 (MIT, ⭐14.2k)
- https://every.to/source-code/compound-engineering-the-definitive-guide — 2026-02-09
- https://davidguttman.github.io/every-vibe-code-camp-distilled/13_kevin_kieran.html — Kevin Rose + Kieran Klaassen 대담

### Third-party analysis
- https://angelo-lima.fr/en/sdd-compound-engineering-bmad-philosophies-en/ — SDD vs CE vs BMAD 비교
- https://rywalker.com/research/compound-engineering-plugin — 플러그인 기술 분석
- https://earezki.com/ai-news/2026-04-10-reviewing-ai-generated-work/ — AI 코드 리뷰 실패 모드

### Podcast
- https://podcasts.apple.com/us/podcast/compound-engineering-manage-teams-of-ai-agents/id1509072609?i=1000730933805 — This New Way, 2025-10-09
