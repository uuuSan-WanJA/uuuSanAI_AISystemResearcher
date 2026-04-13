# Harness Analysis Schema (evolving)

The set of axes used when analyzing a harness / preset / agentic workflow. **This is a seed, not a mandate.** Individual analyses are expected to add, drop, or reframe axes based on what the subject actually is. Global schema updates below get version-bumped when a pattern across multiple subjects justifies it.

## Rules of evolution
- **Per-analysis deviation**: Every harness note declares in its frontmatter which axes it actually uses, and notes any axes added or dropped with a one-line reason.
- **Promotion to global**: If an added axis turns out to be broadly useful (used in ≥2 subsequent analyses) → promote to the global seed schema in the next version bump. Record the bump below.
- **Retirement**: If a global axis proves empty or redundant in ≥3 analyses → retire it with a note.
- **Who edits this file**: The `harness-analyzer` coordinator proposes changes at the end of each analysis cycle. The user (or orchestrator) approves before the bump lands.

## Current version: v1 (seed, 2026-04-13)

Axes below are the STARTING checklist. Order is roughly "outside-in": provenance → architecture → internals → edges → synthesis.

### 1. Identity & provenance
Who, when, where published, maintenance posture, adoption signal.

### 2. Problem framing
What pain does the author name? Verbatim framing.

### 3. Control architecture
Loop vs linear vs graph. Workflow (code-path) vs agent (LLM-directed) per Anthropic taxonomy. Termination conditions.

### 4. State & context model
What persists across turns/iterations? Where (filesystem, messages, spec file, DB)? What does the model see each turn?

### 5. Prompt strategy
System prompt shape, slash commands, skills, templates, meta-prompting moves.

### 6. Tool surface & permission model
Tools granted, permission posture (YOLO / gated / approval), fs/shell/MCP access.

### 7. Human-in-the-loop points
Checkpoints, escalation, approval gates.

### 8. Composability
Stacks with other harnesses? Plugin/skill/subagent interface? Runtime portability.

### 9. Empirical claims & evidence
Author's stated effects + evidence type (anecdote / benchmark / demo).

### 10. Failure modes & limits
Observed vs inferred, with source.

### 11. Transferable primitives ★
**Load-bearing axis.** Atomic extractable ideas. For each: name, 2-line description, assumed context, standalone-extractable? (yes/partial/no + why).

### 12. Open questions
Things still unknown after the analysis cycle finishes.

## Version log
- **v1** (2026-04-13) — Initial seed with 12 axes. Derived from the mental model used when drafting `harness-analyzer` v1.

## Candidate additions (not yet promoted)

### A. Iteration-boundary semantics ★ PROMOTION THRESHOLD REACHED (2026-04-13)
- **Proposed by**: Ralph Wiggum deep-dive (2026-04-13)
- **Independently used by**: GSD deep-dive (2026-04-13) — phase boundary = subagent spawn + artifact commit + summary-only propagation + verify-triggered rollback option
- **Rationale**: Ralph의 본질이 "한 이터레이션이 끝날 때 무슨 일이 일어나는가"에 집중됨 — 컨텍스트 와이프, git commit+push, 파일 상태 전파. 현재 축 4(State & context)의 일부로 묻혀 있지만, 별도 축으로 분리하면 다른 하네스(GSD의 phase spawn, Superpowers의 subagent 경계)와 일관되게 비교 가능.
- **Proposed form**: "매 이터레이션 경계에서 (a) 무엇이 리셋되는가 (b) 무엇이 커밋되는가 (c) 무엇이 다음 턴으로 전파되는가 (d) 어떤 외부 액션(push, tag, alert)이 트리거되는가"
- **Status**: 2개 독립 사용 확인 → 다음 schema bump에서 승격 권고

### B. Backpressure mechanism
- **Proposed by**: Ralph Wiggum deep-dive (2026-04-13)
- **Rationale**: Ralph의 "500 parallel read : 1 sequential write" 규칙은 하네스 특유의 정책 primitive. 다른 하네스에도 유사한 비대칭 리소스/권한 규칙이 있을 가능성 높음 (e.g., Superpowers의 subagent-driven review). 현재 어느 seed 축에도 잘 안 맞음.
- **Proposed form**: "리소스 또는 권한의 비대칭 배분 규칙이 존재하는가. 있다면 무엇이 병렬화되고 무엇이 직렬화되는가, 무엇이 관문화(gated)되어 있는가."
- **Promotion threshold**: 동일

### C. Mode splitting ★ PROMOTION THRESHOLD EXCEEDED (2026-04-13)
- **Proposed by**: Ralph Wiggum deep-dive (2026-04-13)
- **Independently used by**: Superpowers deep-dive (7-phase DAG), GSD deep-dive (discuss/plan/execute/verify/ship 5-way)
- **Rationale**: Ralph의 `PROMPT_plan.md` vs `PROMPT_build.md` 분할은 GSD의 discuss/plan/execute/verify 4페이즈, Spec Kit의 `/speckit.*` 체인과 같은 계열 primitive. "한 프롬프트로 모든 것"을 피하고 명시적 모드 분리. 축 5(Prompt strategy) 안에 있지만 독립 축으로 승격할 가치.
- **Proposed form**: "명시적으로 분리된 모드/페이즈가 있는가. 있다면 전환은 수동인가 자동인가. 모드 간 상태는 어떻게 넘어가는가."
- **Status**: 3개 독립 사용 확인 → 다음 schema bump에서 승격 강력 권고

### D. Gate mechanism syntax ★ PROMOTION THRESHOLD REACHED (2026-04-13)
- **Proposed by**: Superpowers deep-dive (2026-04-13)
- **Independently used by**: GSD deep-dive (schema drift / security / scope reduction gates + `allowed-tools:` 프론트매터 + verify-gate)
- **Rationale**: Superpowers의 `<HARD-GATE>` XML-스타일 태그는 Ralph의 CAPS-yelling, GSD의 phase gate, OpenSpec의 approval과 같은 계열 — "진전을 차단하는 구문 장치"가 독립 축 가치. 현재 축 5(Prompt strategy) 안에 묻혀 있지만 syntax가 에이전트 행동에 직접 영향을 준다는 점에서 분리가 유용.
- **Proposed form**: "진전/실행을 차단하는 구문 장치가 있는가. 그 형태는 무엇인가(XML 태그 / 대문자 호통 / phase enum / 파일 sentinel). 어떤 조건이 충족되어야 해제되는가."
- **Status**: 2개 독립 사용 확인 → 다음 schema bump에서 승격 권고

### G. Execution environment as constraint surface
- **Proposed by**: GSD deep-dive (2026-04-13)
- **Rationale**: tentenco(Ewan Mak, 2026-04)가 명시적으로 뽑아낸 비교 축 — "Superpowers constrains the development process / GSD constrains the execution environment / gstack constrains the decision-making perspective." GSD의 프레시 컨텍스트 카브오프, Pi SDK 레벨 세션 제어, 명시적 allow-list, 웨이브 스케줄링은 모두 **LLM이 무엇을 생각하는가가 아니라 LLM이 어떤 환경에서 동작하는가**를 제약. 현재 seed 축 중 어느 것도 이 구분을 정확히 포착하지 못함.
- **Proposed form**: "하네스가 제약하는 주 대상이 (a) 모델의 프로세스/사고(Process) (b) 의사결정 관점/롤(Perspective) (c) 실행 환경(Environment) 중 무엇인가. 컨텍스트 윈도·세션 수명·권한·스케줄링·비용 추적처럼 LLM 바깥 조건을 지배하는 장치들을 묶는다."
- **Promotion threshold**: 2개 이상 독립 사용. 비교 포지션 프레임으로 이미 기능 중이라 빠른 승격 가능성 높음.

### H. Artifact naming schema as protocol
- **Proposed by**: GSD deep-dive (2026-04-13)
- **Rationale**: GSD의 `{PHASE}-{WAVE}-{TYPE}.md` (`1-0.2-PLAN.md`, `1-VERIFICATION.md`)는 파일명 자체가 프로세스 이벤트 로그 + 에이전트 간 RPC 프로토콜. 사람·오케스트레이터·서브에이전트·`gsd-tools.cjs`가 모두 같은 regex로 파싱. Ralph의 평평한 네이밍, Superpowers의 date-topic 네이밍과 다른 차원으로 명명 규약을 계약 매체로 승격.
- **Proposed form**: "하네스의 상태 파일들이 명명 규약을 갖는가. 명명 규약이 {프로세스 페이즈, 역할, 이벤트 종류}를 인코딩하여 에이전트·툴·사람 간 공통 파싱 계약으로 기능하는가. 규약 위반 시 어떻게 실패하는가."
- **Promotion threshold**: 동일

### E. Authoritative process medium
- **Proposed by**: Superpowers deep-dive (2026-04-13)
- **Rationale**: Superpowers가 v4부터 GraphViz DOT을 **프로세스의 권위적 표현**으로 쓰고 prose를 부연으로 강등한 결정은 "프로세스를 무엇으로 쓰는가"라는 차원을 드러냄. Ralph는 프로즈, Spec Kit은 JSON 유사 스펙, BMAD는 페르소나 정의 — 각각 매체가 다름. 축으로 분리하면 하네스 간 비교가 명료해짐.
- **Proposed form**: "프로세스/워크플로의 권위적 표현 매체는 무엇인가(prose / DOT / Mermaid / JSON schema / code). 매체 선택이 모델 준수도에 미치는 영향은 어떻게 주장되는가."
- **Promotion threshold**: 동일

### F. Skill as unit of discipline (컨벤션 레이어)
- **Proposed by**: Superpowers deep-dive (2026-04-13)
- **Rationale**: Anthropic Agent Skills(2025-10-16)는 기판이지만, 그 위에 Superpowers가 얹은 **SKILL.md 컨벤션**(when-only description, HARD-GATE, DOT flowchart, anti-rationalization table)은 별개 primitive. 축 1(Identity/provenance)이나 축 5(Prompt strategy) 어느 쪽에도 안 맞음. 기판과 컨벤션 레이어를 분리해서 보는 축이 필요.
- **Proposed form**: "기판(SDK/플러그인/프롬프트)과 별도로, 하네스가 제안하는 컨벤션 레이어(스킬 포맷, 네이밍 규칙, 본문 구조 템플릿)가 존재하는가. 이 레이어가 기판과 어떻게 분리되는가."
- **Promotion threshold**: 동일

### I. Ambiguity-as-numeric-gate (subtype of D)
- **Proposed by**: Ouroboros deep-dive (2026-04-13)
- **Rationale**: Ouroboros는 진전 차단 게이트를 **단일 숫자 임계값**으로 표현한다 — ambiguity ≤ 0.2, ontology similarity ≥ 0.95, drift ≤ 0.3. Superpowers의 `<HARD-GATE>` XML, GSD의 페이즈 enum, Ralph의 CAPS 호통과 **형태가 다른** gate 구문: 정량 측정 기반. 축 D의 자연스러운 서브타입으로 볼 수도, 별개 축으로 볼 수도 있음.
- **Proposed form**: "진전 차단 게이트가 (a) 정성 (HARD-GATE 태그, enum, 호통) vs (b) 정량 (수치 임계값 + 측정 함수) 중 어느 쪽인가. 정량이면 측정 함수는 결정론적인가 모델 호출인가."
- **Promotion threshold**: 독립 사용 1회 — 축 D와의 관계 결정 필요. Ouroboros 외에 동일 패턴 사용하는 하네스가 나타나면 승격.

### J. Deferred-tool loading protocol in skill body
- **Proposed by**: Ouroboros deep-dive (2026-04-13)
- **Rationale**: Ouroboros의 모든 SKILL.md는 agent에게 "ToolSearch로 MCP 툴을 먼저 로드한 뒤 Path A/B 를 결정하라" 명시 지시. Claude Code의 deferred-tool 시스템(late-binding)을 컨벤션 레이어로 끌어올린 특이 패턴. Superpowers의 `using-superpowers` meta-skill 부트스트랩, GSD의 `gsd-tools.cjs` 결정론 레이어와 닮았으나, **툴 가용성 자체를 skill 본문이 책임**진다는 점에서 구별.
- **Proposed form**: "스킬 본문이 런타임 툴 가용성(late-binding, MCP, plugin fallback)을 직접 조회/로드하는 프로토콜을 명시하는가. 불가 시 agent adoption 폴백이 있는가 (Path A/B duality)."
- **Promotion threshold**: 독립 사용 1회. 플러그인 생태계가 deferred-tool 패턴으로 수렴하면 빠르게 2회 확보 가능.

### 축 G 재사용 확인 (Ouroboros, 2026-04-13)
- Ouroboros는 축 G("execution environment as constraint surface")를 **입력 측 변종**으로 재사용. PAL Router 3-tier + MCP 서버 세션 격리 + stateless evolve_step이 execution environment 제약. **2번째 독립 사용 카운트** — 축 G 승격 권고 유지.

### 축 D 재사용 확인 (Ouroboros, 2026-04-13)
- Ouroboros의 숫자 임계값 게이트(0.2/0.95/0.3)는 축 D("gate mechanism syntax")의 **3번째 독립 사용**. 승격 권고 강화.

### 축 C 재사용 확인 (Ouroboros, 2026-04-13)
- Ouroboros의 7+ 명령 모드(interview/seed/execute/evaluate/evolve/ralph/unstuck)는 축 C("mode splitting")의 **4번째 독립 사용**. 승격 권고 최상위.

### 축 A 재사용 확인 (Ouroboros, 2026-04-13)
- Ouroboros의 generation boundary (evolve_step = stateless one-generation call, EventStore로 상태 재구성)는 축 A("iteration-boundary semantics")의 **3번째 독립 사용** — Ralph(파일), GSD(페이즈 스폰), Ouroboros(이벤트)로 매체 스펙트럼 형성. 승격 권고 강화.

### 축 C 재사용 확인 (gstack, 2026-04-13)
- gstack의 23+ 슬래시 커맨드 × 7-phase 스프린트(Think/Plan/Build/Review/Test/Ship/Reflect)는 축 C("mode splitting")의 **5번째 독립 사용** (Superpowers/GSD/Ouroboros/Ralph에 이어). **승격 확정적**.

### 축 F 재사용 확인 (gstack, 2026-04-13)
- gstack의 SKILL.md + YAML frontmatter(`allowed-tools:`, `preamble-tier:`, `version:`, `description:` with auto-invoke)는 축 F("skill as unit of discipline")의 **2번째 독립 사용** (Superpowers 다음). 기판(Anthropic Agent Skills)과 **컨벤션 레이어**의 분리 가설이 gstack에서도 명확히 관찰됨 — gstack은 plugin 경로가 아닌 `git clone + ./setup` 단순 파일 복사이며, 그 위에 얹힌 SKILL.md 구조가 곧 gstack의 "제품". 승격 권고 강화.

### 축 H 재사용 확인 (gstack, 2026-04-13, 약)
- gstack의 `.tmpl`(human) vs 생성된 `.md`(never edited directly) + `browse/dist` never-committed 규칙은 파일명에 "편집 권리자"를 인코딩. GSD의 `{PHASE}-{WAVE}-{TYPE}.md` regex 계약보다 약하지만 같은 방향. **2번째 독립 사용(약)**. 승격 권고는 다른 하네스에서 강한 증거 더 필요.

### 축 G 대립 사용 (gstack, 2026-04-13)
- gstack은 축 G("execution environment as constraint surface")를 **직접 재사용하지 않고 쌍대 축으로 호출**. tentenco의 3-축 프레임("Superpowers=process / GSD=environment / gstack=perspective")이 G의 쌍대 축(아래 K)을 자연스럽게 요구. G 자체의 독립 사용 카운트는 증가 안 함, 그러나 **G의 승격 근거로서 비교축 기능을 재확인**.

### K. Role perspective as constraint surface (새 후보)
- **Proposed by**: gstack deep-dive (2026-04-13)
- **Rationale**: gstack의 23+ 슬래시 커맨드는 각각 한 엔지니어링 역할(CEO/Eng Manager/Staff Engineer/Designer/QA Lead/CSO/Release Engineer…)에 결박되어, "LLM이 어떤 시선으로 판단할 것인가"를 1차 제약 대상으로 삼는다. tentenco(Medium 2026-04)가 명시적으로 축 G와 쌍대 프레임으로 호출: "Superpowers constrains the development process / GSD constrains the execution environment / **gstack constrains the decision-making perspective**". 현재 seed 축 1(Identity), 5(Prompt strategy), 6(Tool surface) 어느 것도 이 구분을 정확히 포착하지 못함.
- **Proposed form**: "하네스가 제약하는 주 대상이 LLM의 **역할/페르소나/의사결정 클래스**인가. 역할 정의 위치(SKILL.md frontmatter / CLAUDE.md / persona file), 전환 방식(명시적 slash command vs 암묵적 mention), 한 대화 내 다중 역할 허용 여부, 역할별 permission/tool 차등 존재 여부."
- **Expected 2번째 사용 후보**: BMAD-METHOD의 ~21 persona 시스템, Anthropic Claude Projects, Agent OS의 standards injection. 빠른 2회 확보 전망.
- **Promotion threshold**: 2개 이상 독립 사용. 축 G의 자연스러운 쌍대로 위상이 분명해 선호 승격 후보.

### 축 K 재사용 확인 (ECC, 2026-04-13)
- ECC의 47개 전문화 에이전트(code-reviewer, security-reviewer, planner, language-specific builder 등)는 역할/페르소나를 1차 제약 대상으로 삼는 구조. gstack의 slash command별 역할 결박과 같은 방향 — "LLM이 어떤 역할로 판단할 것인가"를 사전 정의. **2번째 독립 사용 → 축 K 승격 권고 충족**.

### 축 C 재사용 확인 (ECC, 2026-04-13)
- ECC의 `/plan` vs `/tdd` vs `/code-review` vs `/multi-plan` 등 역할별 스킬 분리는 축 C("mode splitting")의 **6번째 독립 사용** (Superpowers/GSD/Ouroboros/Ralph/gstack에 이어). **승격 확정 최강**.

### 축 F 재사용 확인 (ECC, 2026-04-13)
- ECC의 181개 스킬 파일 + 스킬 인덱스 + `/skill-create` 사용자 정의 스킬은 축 F("skill as unit of discipline")의 **3번째 독립 사용** (Superpowers, gstack에 이어). 승격 권고 강화.

### L. Instinct learning as harness layer (새 후보)
- **Proposed by**: ECC deep-dive (2026-04-13)
- **Rationale**: ECC의 `/learn` → `/evolve` → confidence pruning 사이클은 "하네스가 에이전트 행동을 관찰해 재사용 가능 패턴으로 자동 추출하는 메타학습 루프"라는 독립 차원. 현재 seed 축 4(State & context)와 축 5(Prompt strategy)에 분산 가능하나, 하네스 자체가 학습 주체라는 점에서 별도 축 가치. Ralph의 "tune like a guitar"(운영자 수동 튜닝), GSD의 STATE.md(정적 축적)와 구별되는 동적·자동 학습 루프.
- **Proposed form**: "하네스가 에이전트 행동에서 패턴을 자동 추출해 재사용 가능 단위(instinct/skill/rule)로 승격하는 메타학습 루프를 갖는가. 있다면 (a) 추출 트리거는 무엇인가 (b) 신뢰도 평가 방식은 결정론적인가 LLM 호출인가 (c) 사람의 개입은 어느 지점인가 (d) 저신뢰도 단위의 폐기 기준은 무엇인가."
- **Status**: 1회 (ECC). BMAD-METHOD의 persona evolution, Ouroboros의 ontology drift repair가 2번째 후보.
- **Promotion threshold**: 2개 이상 독립 사용.

### 축 L 재사용 확인 (Compound Engineering, 2026-04-13) ★ PROMOTION THRESHOLD REACHED
- Compound Engineering의 `/ce:compound` → `docs/solutions/` (YAML frontmatter 태깅) → 베스트프랙티스 에이전트의 "genetic search" → 다음 `/ce:plan` 컨텍스트 주입 루프는 축 L("instinct learning as harness layer")의 **2번째 독립 사용**. ECC의 `/learn`→`/evolve`→confidence pruning과 구현 매체가 다름(ECC: 신뢰도 수치 + 자동 pruning / CE: YAML 마크다운 + 에이전트 검색). 두 사례가 "하네스가 이터레이션 간 학습을 자동 추출·재주입하는 메타루프"라는 동일 패턴을 독립적으로 구현. **축 L 승격 권고 충족.**

### 축 C 재사용 확인 (Compound Engineering, 2026-04-13)
- CE의 Brainstorm/Plan/Work/Review/Compound 5-모드 분할 + `/lfg` 통합 모드는 축 C("mode splitting")의 **7번째 독립 사용**. 승격 확정 근거 추가.

### 축 F 재사용 확인 (Compound Engineering, 2026-04-13)
- CE의 26개 전문 에이전트 파일 + 13개 스킬 파일 + 23개 workflow 커맨드 + 멀티 IDE 변환 레이어는 축 F("skill as unit of discipline")의 **4번째 독립 사용** (Superpowers, gstack, ECC에 이어). 승격 권고 최강.

### 축 A 재사용 확인 (Compound Engineering, 2026-04-13)
- CE의 이터레이션 경계 = `docs/solutions/` 파일 커밋 + `CLAUDE.md` 갱신 + 다음 루프 자동 재로드 + GitHub PR 트리거는 축 A("iteration-boundary semantics")의 **4번째 독립 사용** (Ralph/GSD/Ouroboros에 이어). 승격 권고 강화.

### 축 K 재사용 확인 (Compound Engineering, 2026-04-13)
- CE의 14개 병렬 리뷰 에이전트(security-sentinel, performance-oracle, dhh-rails-reviewer, julik-frontend-races-reviewer 등)는 역할/페르소나를 1차 제약 대상으로 삼는 구조. gstack/ECC와 같은 방향. **3번째 독립 사용 → 축 K 승격 확정 권고.**

### 축 C 재사용 확인 (revfactory-harness, 2026-04-13)
- revfactory/harness의 Phase-0 3-way 분기(신규/확장/유지보수) + Phase-2.1 실행 모드(팀/서브에이전트/하이브리드) + Phase 7 진화 워크플로는 축 C("mode splitting")의 **8번째 독립 사용**. **승격 확정 최강 유지** (CE가 이미 7번째로 카운트, 이 항목은 8번째로 수정).

### 축 F 재사용 확인 (revfactory-harness, 2026-04-13)
- SKILL.md YAML frontmatter, "Pushy" description(트리거 상황 + near-miss 구별 명시), Progressive Disclosure 레이어(메타데이터→본문→references→scripts), 500줄 상한, should-trigger/should-NOT-trigger 8–10개 검증 — 축 F("skill as unit of discipline")의 **5번째 독립 사용** (Superpowers/gstack/ECC/CE에 이어). **승격 확정 추가 근거**.

### 축 K 재사용 확인 (revfactory-harness, 2026-04-13)
- Phase 3에서 모든 에이전트에 domain-specific 역할 + 입출력 프로토콜 + 협업 규약 정의. harness-100의 978개 에이전트 정의는 역할 페르소나를 1차 제약 대상으로 삼는 규모 있는 증거. 축 K("role perspective as constraint surface")의 **4번째 독립 사용** (gstack/ECC/CE에 이어). **승격 확정 추가 근거**.

### M. Meta-skill bootstrapping (새 후보)
- **Proposed by**: revfactory-harness deep-dive (2026-04-13)
- **Rationale**: Harness는 단일 SKILL.md 실행이 `.claude/agents/*.md` + `.claude/skills/*/SKILL.md` 전체를 사이드이펙트로 산출하는 **생성기(generator)** 패턴. ECC의 `/skill-create`(단일 스킬 생성)와 비교하면 scope가 다름 — ECC는 스킬 단위, Harness는 전체 팀 아키텍처 단위. 현재 seed 축 1–12 중 어느 것도 "하네스가 실행 결과로 다른 하네스를 낳는가"를 포착하지 못함. 재귀적 생성 여부 + 생성 범위 + 생성물 품질 검증 방식이 독립 비교 축 가치.
- **Proposed form**: "하네스가 1회 실행의 사이드이펙트로 다른 하네스(에이전트 정의 + 스킬 파일 + 오케스트레이션 구성)를 생성하는가. 있다면 (a) 생성 범위(단일 스킬 vs 전체 팀 vs 프레임워크) (b) 생성물 품질 검증 방식(검증 Phase 내장 여부) (c) 재귀 깊이(생성된 하네스가 다시 하네스를 낳는가) (d) ECC /skill-create, harness-100처럼 라이브러리로 발전하는가."
- **Status**: 1회 (revfactory-harness). ECC의 `/skill-create`가 약한 사례. 2번째 강한 사례 필요.
- **Promotion threshold**: 2개 이상 독립 사용.

## Retired axes
(Empty.)
