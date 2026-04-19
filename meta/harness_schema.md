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

### N. Substrate feature-gap exploitation (새 후보)
- **Proposed by**: OMX/OMC deep-dive (2026-04-19)
- **Rationale**: OMX와 OMC는 동일한 canonical skill vocabulary(`$deep-interview`, `$ralplan`, `$team`, `$ralph`)를 두 개의 서로 다른 substrate에 이식한 자연실험. OMC는 Claude Code의 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` native team 기능을 탑승; OMX는 Codex CLI에 해당 기능이 없어 Rust 런타임(`omx-runtime-core/src/{mailbox,dispatch,authority}.rs`)으로 직접 재구현. 이 "substrate가 제공하지 않는 것을 하네스가 재발명한 부분"이 어느 기존 축에도 깔끔히 담기지 않음. 축 3(Control architecture)과 축 8(Composability) 어디에도 정확히 안 맞음.
- **Proposed form**: "하네스가 multi-substrate variant으로 존재한다면, 어떤 primitive가 (a) host CLI의 native 기능을 탑승, (b) host가 제공하지 않아 하네스 코드로 재구현, (c) host-exclusive라 한쪽 port에서만 존재하는가. 이 fork 패턴은 시간에 따라 수렴하는가 발산하는가."
- **Status**: 1회 (OMX/OMC). Ouroboros의 multi-runtime(Claude/Codex/OpenCode) 주장이 2번째 후보. Compound Engineering의 Claude Code → 다른 IDE 변환 레이어도 약한 후보.
- **Promotion threshold**: 2개 이상 독립 사용.
- **포인터**: `notes/harness/omx-omc.md` §2, §4 (core evidence), §13 (delta table).

### O. Consensus planning as execution gate (축 D 하위타입)
- **Proposed by**: OMX/OMC deep-dive (2026-04-19)
- **Rationale**: OMX/OMC의 `$ralplan`은 축 D("gate mechanism syntax")의 특수한 변형 — Superpowers `<HARD-GATE>`, Ouroboros 수치 임계값, Ralph CAPS 호통은 모두 **실행 *중*의 진전**을 차단하는 게이트. Ralplan의 Pre-Execution Gate는 **실행 *진입*을 차단**하고 consensus planning으로 돌려보내는 게이트 — "ralph fix this" 같은 under-specified 프롬프트를 어휘 휴리스틱(file path, camelCase symbol, issue #, test runner, 코드블록, numbered steps ≥ 1 → pass; else redirect)으로 감지해 강제 우회. `force:` / `!` escape hatch까지 명시. 축 D의 자연스러운 서브타입.
- **Proposed form**: "하네스가 under-specified 실행 요청을 거부하고 specification-first subflow로 redirect하는가. 감지 신호는 무엇인가(어휘 휴리스틱 / LLM classifier / embedding similarity). escape hatch는 무엇인가(`force:`, `!`, explicit skill 호출)."
- **Status**: OMX/OMC에서 1번째 강한 사례. GSD의 `/gsd-discuss`, Ouroboros interview, Compound Engineering plan 도 잠재적 후보 — 재사용 표시 확보 가능성 높음.
- **Promotion threshold**: 2개 이상 독립 사용.
- **포인터**: `notes/harness/omx-omc.md` §3f (ralplan mechanics), §11 (comparative position).

### P. Stage handoff as RPC protocol (축 A refinement)
- **Proposed by**: OMX/OMC deep-dive (2026-04-19)
- **Rationale**: OMC의 `.omc/handoffs/<stage-name>.md` 패턴은 stage 간 명시적 RPC 계약 — `Decided / Rejected / Risks / Files / Remaining` 5-필드 10-20줄 마크다운을 **stage 전환 전에** 쓰고, 다음 stage의 에이전트 spawn prompt에 포함. handoff 파일들이 누적되고, 취소 시에도 보존. GSD의 `{PHASE}-{WAVE}-{TYPE}.md` regex 계약보다 더 lightweight하지만 같은 방향 — 파일이 sub-agent 간 RPC 매체. 축 A(iteration-boundary semantics)의 homogeneous loop 버전과 구별되는 heterogeneous-stage 버전.
- **Proposed form**: "stage 간 handoff가 고정 스키마(필드 / 네이밍 / 저장 경로) 아티팩트로 매개되는가. 다음 stage가 자신의 에이전트를 spawn하기 전에 해당 handoff를 읽는가. handoff 체인은 누적되는가 회전되는가. cancellation 시 보존/삭제 정책은?"
- **Status**: OMC에서 1번째 강한 사례. GSD phase artifacts가 2번째 후보 — 빠른 2+ 승격 가능성.
- **Promotion threshold**: 2개 이상 독립 사용.
- **포인터**: `notes/harness/omx-omc.md` §4c (handoff contract).

### 축 C 재사용 확인 (OMX/OMC, 2026-04-19)
- OMC의 team-plan/team-prd/team-exec/team-verify/team-fix 5-stage + ralph의 starting/executing/verifying/fixing/complete/failed/cancelled 7-phase + autopilot의 Phase 0–5 (expansion/planning/execution/QA/validation/cleanup)는 축 C("mode splitting")의 **9번째 독립 사용** (Superpowers/GSD/Ouroboros/Ralph/gstack/ECC/CE/revfactory-harness에 이어). **승격 확정 최강 유지**.

### 축 D 재사용 확인 (OMX/OMC, 2026-04-19)
- OMC/OMX의 `$ralplan` Pre-Execution Gate(위 축 O 참조) + Ralph의 verification floor (STANDARD tier minimum) + deslop pass 강제 + post-deslop regression re-verification 게이트는 축 D("gate mechanism syntax")의 **4번째 독립 사용** (Superpowers/GSD/Ouroboros에 이어). 승격 권고 강화.

### 축 F 재사용 확인 (OMX/OMC, 2026-04-19)
- OMC의 40개 스킬 + 19개 에이전트 + YAML frontmatter + argument-hint + level + aliases + `<Use_When>` / `<Do_Not_Use_When>` / `<Why_This_Exists>` / `<Execution_Policy>` / `<Steps>` / `<Final_Checklist>` XML-tag 본문 구조는 축 F("skill as unit of discipline")의 **6번째 독립 사용** (Superpowers/gstack/ECC/CE/revfactory-harness에 이어). 승격 권고 최강.

### 축 G 재사용 확인 (OMX/OMC, 2026-04-19)
- OMX의 `.omx/state/` 경로 계층 + frozen schema 계약(`docs/contracts/ralph-state-contract.md` 등) + session-scope vs root-scope authoritative 규칙 + tmux pane 구분 + Rust runtime authority separation(`authority.rs`)은 축 G("execution environment as constraint surface")의 **3번째 독립 사용** (GSD/Ouroboros에 이어). 승격 권고 강화.

### 축 I 재사용 확인 (OMX/OMC, 2026-04-19)
- OMX `$deep-interview`의 weighted ambiguity score(intent 0.30 + outcome 0.25 + scope 0.20 + constraints 0.15 + success 0.10) + depth-specific threshold(`--quick` 0.30 / `--standard` 0.20 / `--deep` 0.15) + 정량 게이트 + 정성 readiness gate(Non-goals 명시 + Decision Boundaries 명시 + pressure pass 완료)는 축 I("ambiguity-as-numeric-gate")의 **2번째 독립 사용** (Ouroboros에 이어). Superpowers verification score는 약한 3번째. **축 I 승격 권고 충족**.

### 축 L 재사용 확인 (OMX/OMC, 2026-04-19)
- OMC의 `/learner` skill(패턴 자동 추출 → `.omc/skills/` YAML frontmatter + triggers) + OMX의 `$autoresearch`(mission-driven validator-gated 루프)는 축 L("instinct learning as harness layer")의 **3번째 독립 사용** (ECC, Compound Engineering에 이어). **축 L 승격 확정 권고**.

### 축 K 재사용 확인 (OMX/OMC, 2026-04-19)
- OMC의 19개 specialized agents(analyst/architect/code-reviewer/executor/...) + stage-aware routing(team-plan에서는 explore+planner, team-verify에서는 verifier+security-reviewer+code-reviewer, 조건부로 architect/critic)은 축 K("role perspective as constraint surface")의 **5번째 독립 사용** (gstack/ECC/CE/revfactory-harness에 이어). 승격 권고 최강 유지.

### Q. Category × Skill × Persona orthogonality in subagent delegation (새 후보)
- **Proposed by**: OMO deep-dive (2026-04-19)
- **Rationale**: OMO의 `task(subagent_type, category, load_skills[], run_in_background)` 호출은 3개 독립 차원을 직교적으로 결합 — **category** (model + temperature + prompt_append 결정), **skill** (tool/MCP 그랜트 + domain knowledge 주입), **persona** (agent identity + tool restriction 정책). 8 categories × 11 agents × N skills 제품 공간을 실제로 88+ 고정 에이전트 정의로 폭발시키지 않고 orthogonal factoring으로 관리. OMC/OMX의 staged pipeline 라우팅(team-plan/prd/exec/verify/fix 각 stage마다 미리 정해진 에이전트 세트)과 구별 — OMO는 delegate 시점 동적 조합. 현재 축 3(control architecture), 축 5(prompt strategy), 축 6(tool surface) 어느 것도 "delegation의 직교 차원 수"를 명시적으로 포착하지 못함.
- **Proposed form**: "하네스가 subagent 호출을 몇 차원으로 factoring하는가? (a) 1차원 — 단일 agent 선택 (b) 2차원 — agent × skill, agent × category 등 (c) 3차원 — model × skill × persona 직교 조합. 차원 간 독립성이 런타임에서 강제되는가(합법 조합만 허용)? default 정책은 N×M×P 조합 폭발을 어떻게 억제하는가?"
- **Status**: OMO 1회 강한 사례. ECC, Compound Engineering이 약한 2번째 후보 (agent + skill 2차원). 2+ 확인 후보 빠르게 가능.
- **Promotion threshold**: 2개 이상 독립 사용.
- **포인터**: `notes/harness/omo.md` §4c (category system), §4d (built-in skills), Δ4 제안.

### R. Wisdom-accumulation notepad system (새 후보)
- **Proposed by**: OMO deep-dive (2026-04-19)
- **Rationale**: OMO Atlas orchestrator의 `.sisyphus/notepads/{plan-name}/{learnings.md, decisions.md, issues.md, verification.md, problems.md}` 5-type 노트패드 — 각 sub-delegation 직후 결과에서 Conventions/Successes/Failures/Gotchas/Commands 추출해 카테고리별 추가. 다음 sub-delegation prompt에 전체 notepad 주입. **orchestrator가 "실행 중 학습한 것"을 type-structured memory로 누적** + 같은 plan 내 subsequent workers에 forward. 축 A(iteration boundary: per-loop reset)도 축 L(instinct learning: cross-session 자동 추출)도 정확히 아닌 **intra-plan cumulative memory during orchestration**. Ralph의 파일-매개 메모리나 GSD의 STATE.md(monolithic), OMC의 `.omc/handoffs/*`(stage-level)와 구별되는 **task-level + field-typed + always-injected**.
- **Proposed form**: "orchestrator가 한 plan 실행 중 typed notepad 시스템(복수 파일, 고정 카테고리)을 유지하며 모든 subsequent sub-delegation prompt에 자동 주입하는가? (a) field 수와 의미 (b) write-trigger(deterministic post-delegate vs 모델 판단) (c) 범위(per-plan / per-session / cross-plan) (d) deduplication 정책."
- **Status**: OMO 1회 강한 사례. GSD의 STATE.md가 약한 2번째 (monolithic이지만 같은 지향). Compound Engineering의 `docs/solutions/`는 cross-plan이라 다른 층. 2+ 후보.
- **Promotion threshold**: 2개 이상 독립 사용.
- **포인터**: `notes/harness/omo.md` §4m (Atlas + notepads), Δ5 제안.

### S. Authorship-cluster porting patterns (새 후보 — 메타축)
- **Proposed by**: OMO deep-dive (2026-04-19)
- **Rationale**: OMO/OMC/OMX 트리오는 **single-ecosystem같지만 실제로는 two-author two-product + bidirectional porting**이 drive하는 진화 패턴. 기존 축 어느 것도 "who ported what from whom and when"을 기록하지 못함. 이 차원은 primitive 추적에 결정적이 됨 — OMC의 `$deep-interview`는 Ouroboros-inspired (cross-ecosystem), OMC의 ralphloop/ultrawork는 OMO-port (intra-cluster), OMC의 OpenClaw는 OMC-origin이 OMO/OMX로 정방향 port — 세 가지 direction이 공존.
- **Proposed form**: "harness가 다른 harness와의 관계에서 어떤 포지션인가? (a) origin only — 자체 primitive만 생산 (b) port target only — 다른 데서 가져옴만 (c) bidirectional — primitive 양방향 교환 (d) lineage — 명시적 fork/port 선언. 교환되는 primitives는 무엇이고 attribution은 어떻게 유지되는가? git commit message, CHANGELOG, README credits 중 어디서 추적 가능한가?"
- **Status**: OMO/OMC/OMX 트리오가 1st 강한 case. 다른 multi-harness author 클러스터(만약 존재) 발굴 시 2+ 확인 가능. 현 시점에선 메타-typological axis로 제안.
- **Promotion threshold**: 2개 이상 독립 클러스터 관찰.
- **포인터**: `notes/harness/omo.md` §11 (comparative position), §13 (provenance delta table).

### OMO's partial support/refutation summary for earlier candidates
- **축 Δ1 (Substrate feature-gap exploitation)** — OMO는 single-substrate (OpenCode plugin-only) + Claude Code 인바운드 어댑터. OMX↔OMC의 "same vocab, two substrates" pattern과 다름. **OMO refutes the broader generalization**; Δ1은 OMC↔OMX 특유 case로 유지.
- **축 Δ2 (Consensus planning as execution gate)** — OMO의 Prometheus는 opt-in formal planner (`@plan` / Tab). ultrawork keyword는 prompt-shape discipline gate (CAPS + "UNACCEPTABLE" violation table), auto-redirect 없음. **Δ2 refined**: gate 형태가 (a) lexical heuristic + redirect (OMC), (b) numeric threshold + qualitative readiness (Ouroboros, OMC deep-interview), (c) prompt-shape discipline + opt-in formal planner (OMO) 세 갈래로 분화. 축 D의 하위타입으로 계속 유지.
- **축 Δ3 (Stage handoff as RPC protocol)** — OMO의 `/handoff`는 **single-session context compaction**이지 stage-to-stage RPC 아님. 사용자가 output을 copy-paste해서 새 세션 시작하는 수동 artifact. **OMO does NOT count as 2nd use**. Δ3 promotion threshold 미달 유지 (OMC 단독 + GSD near-match). 다른 harness에서 2+ 확인 필요.

### Cline v3.58 partial support/refutation summary for earlier candidates (2026-04-19)
- **축 Δ1 (Substrate feature-gap exploitation)** — Cline이 **3번째 패턴**을 도입하여 축 refine 권고. OMC↔OMX의 "per-host hand-reinvention"과 OMO의 "single-substrate + inbound loaders"에 이어, Cline은 **"core + adapter protocol (ACP)"** 패턴을 사용. 하나의 TypeScript core + Agent Client Protocol 공개 표준으로 VS Code / JetBrains / Zed / Neovim / CLI / Cursor 6개 substrate에 배포. **Δ1 축을 3-branch 서브타이폴로지로 재구성 권고**: (a) hand-reinvention, (b) single-home + inbound, (c) core + adapter.
- **축 Δ2 (Consensus planning as execution gate)** — Cline의 Plan Mode + `/deep-planning`은 **user-triggered opt-in**이지 detector-triggered redirect 아님. OMC/OMX `$ralplan`과 달리 underspecified 감지 로직 없음. **Δ2 refuted for Cline** — OMC/OMX 단독 강사례 유지.
- **축 Δ3 (Stage handoff as RPC protocol)** — Cline 서브에이전트는 stage-to-stage handoff 아님 (main → parallel read-only workers → report strings → main, 단일 fan-out). **N/A**. Δ3 카운트 무변화.
- **축 Δ4 (Category × Skill × Persona orthogonality)** — Cline 서브에이전트는 single-role (read-only researcher) with optional per-subagent `modelId` + skills. OMO의 3차원 직교 matrix와 **다른 shape**. Plan mode model ≠ Act mode model이 2차원 assignment의 최대치. **Δ4 refuted for Cline** — OMO 단독 강사례 유지.

### 축 C 재사용 확인 (Cline v3.58, 2026-04-19, 약)
- Cline의 Plan/Act mode + `/deep-planning` 4-step (Silent Investigation → Discussion → Plan Creation → Task Creation)은 축 C("mode splitting")의 **11번째 사용 (약)**. "약"인 이유: Cline은 대부분의 workflow를 slash-command bundle로 ship하지 않음 (Superpowers/GSD/gstack/ECC/CE와 달리). Plan/Act 토글 + `/deep-planning` 하나가 주요 모드 분할. 승격 확정 최강 유지, 카운트만 증가.

### 축 F (Cline은 재사용 NO)
- Cline은 Skills를 **메커니즘**으로 탑재 (SKILL.md 포맷, progressive disclosure, YAML frontmatter, `.cline/skills/` 디스커버리)하지만 **오피니어네이티드 스킬 라이브러리를 함께 ship하지 않음**. Superpowers/OMO/OMC/gstack/ECC/CE가 "플러그인 + 큐레이티드 스킬 번들"인 것과 달리 Cline은 "플랫폼 only". 축 F의 카운트에 포함하지 **않음** — 축 F는 "discipline-layer convention을 **제공**하는가"가 아니라 "**제안/ship**하는가"에 대한 것이었음. 이 구분을 명시적으로 기록.

### 축 G 재사용 확인 (Cline v3.58, 2026-04-19)
- Cline의 8-event hook lifecycle (TaskStart/Resume/Cancel/Complete/PreToolUse/PostToolUse/UserPromptSubmit/PreCompact) + global-before-workspace 실행 순서 + `cancel: true` 반환으로 차단 + `CLINE_COMMAND_PERMISSIONS` 환경변수 deterministic allowlist 레이어 + `requires_approval` 모델-태그 메커니즘은 축 G("execution environment as constraint surface")의 **5번째 독립 사용** (GSD/Ouroboros/OMX-OMC/OMO에 이어). 승격 권고 강화. Cline 특유 기여: policy를 agent-prompt가 아닌 **executable script + JSON stdin/stdout contract**로 외부화.

### Δ5 (신규 후보) — Headless-mode-as-first-class output contract
- **Proposed by**: Cline v3.58 deep-dive (2026-04-19)
- **Rationale**: Cline CLI 2.0은 non-interactive execution을 **typed output contract**로 취급 — auto mode-detection (TTY/pipe/flag), `--json` 출력이 `ui_messages.json`과 동일 schema(`{type: "ask"|"say", text, ts, reasoning?, partial?}`), shell pipe composition (`git diff | cline -y "x" | cline -y "y"`)을 1급 패턴으로 문서화. Ralph의 bash-loop-over-prompt(입력 계약만, 출력 계약 없음)와 GSD의 file-based state(pipe 불가)와 구별.
- **Proposed form**: "하네스가 headless/non-interactive 실행을 1급 output contract로 취급하는가? (a) 모드 스위치 트리거(flag / TTY / pipe / all) (b) 출력 포맷 보장(plain text / JSON schema / both) (c) chain composition 문서화 여부 (d) exit 계약(complete 시 자동 종료 vs long-running)."
- **Status**: Cline 단독 강사례. GSD batch commands가 약한 near-match. Compound Engineering의 `/lfg`는 pipeable 아님. 2번째 independent case 대기.
- **Promotion threshold**: 2개 이상 독립 사용.
- **포인터**: `notes/harness/cline-v3-58.md` §5 (prompt strategy), §11 P2 (primitive).

### 축 C 재사용 확인 (OMO, 2026-04-19)
- OMO의 3-layer orchestration (Planning/Execution/Worker) × 8 categories × 11 agents × N skills 제품 공간 + 3 modes (simple/ultrawork/prometheus) + `/ralph-loop` vs `/ulw-loop` vs `/start-work` vs `/handoff` vs `/init-deep` slash-command 분할은 축 C("mode splitting")의 **10번째 독립 사용** (Superpowers/GSD/Ouroboros/Ralph/gstack/ECC/CE/revfactory-harness/OMX-OMC에 이어). **승격 확정 최강 유지**.

### 축 F 재사용 확인 (OMO, 2026-04-19)
- OMO의 SKILL.md format 채택 (Claude Code 호환 via `claude-code-*-loader`) + built-in skills `src/features/builtin-skills/skills/*.ts` + user-space `.opencode/skills/*/SKILL.md` + skill-embedded MCP + per-skill tool restriction은 축 F("skill as unit of discipline")의 **7번째 독립 사용** (Superpowers/gstack/ECC/CE/revfactory-harness/OMX-OMC에 이어). 승격 권고 최강.

### 축 K 재사용 확인 (OMO, 2026-04-19)
- OMO의 11 named agents (Sisyphus/Hephaestus/Prometheus/Atlas/Metis/Momus/Oracle/Librarian/Explore/Multimodal-Looker/Sisyphus-Junior) + 각 agent의 명시적 tool restriction (Oracle/Librarian/Explore: read-only, Momus: cannot write/edit/delegate, Atlas: cannot delegate, Sisyphus-Junior: cannot re-delegate) + Greek-mythology persona naming은 축 K("role perspective as constraint surface")의 **6번째 독립 사용** (gstack/ECC/CE/revfactory-harness/OMX-OMC에 이어). 승격 권고 최강 유지.

### 축 G 재사용 확인 (OMO, 2026-04-19)
- OMO의 Bun-only runtime + per-agent tool restriction allowlist/blocklist + preemptive-compaction 10-hook suite + `/tmp/oh-my-opencode.log` 단일 글로벌 로그 + `.sisyphus/` 디렉터리 계층 + 5 concurrent background agents per model/provider (circuit breaker) + `OMO_DISABLE_POSTHOG` 등 env var 제어는 축 G("execution environment as constraint surface")의 **4번째 독립 사용** (GSD/Ouroboros/OMX-OMC에 이어). 승격 권고 강화.

### 축 L (OMO는 재사용 NO)
- OMO는 Atlas wisdom notepad(intra-plan)는 있지만 OMC `/learner`, ECC `/skill-create`, CE `/ce:compound`같은 **cross-session 자동 skill 추출** 메커니즘은 **없음**. OMO가 지원하는 건 intra-plan cumulative memory (새 candidate R). 축 L 카운트 증가 안 함. OMC가 OMO에 비해 축 L 측면에서 진화된 후속 — port-then-innovate 패턴.

### T. Out-of-loop productization surface (새 후보)
- **Proposed by**: openwork deep-dive (2026-04-19)
- **Rationale**: 대다수 코퍼스 하네스(Superpowers, GSD, Ralph, Ouroboros, gstack, ECC, CE, OMC, OMX, OMO, Cline)는 **에이전트 루프 *안*에서** 사고와 행동을 조형하는 것이 주 관심사. openwork는 체계적으로 **에이전트 루프 *밖*에서** 무엇이 일어나는가를 제품화한다 — 배포, 서피스 레이어, 팀 채팅 브리지, 감사·승인 중재자, 스코프된 원격 공유, 포터블 워크플로 번들. 기존 축 3/4/5/6(control/state/prompt/tool-surface)은 루프 내부를 다루고, 축 8(composability)은 약한 근사치. "what the harness adds outside the loop" 차원을 포착하지 못함.
- **Proposed form**: "하네스가 에이전트 루프 바깥에 아티팩트를 추가하는가? (배포 서피스, 채팅 플랫폼 어댑터, 감사·승인 중재자, 스코프된 원격 공유, 내보낼 수 있는 워크플로 번들). 각각에 대해 (a) 외부 서피스 (b) 인증 모델 (c) portability를 가능하게 하는 아티팩트 계약."
- **Status**: openwork 1st strong case. Open Interpreter desktop + LibreChat + Continue(추측) 2nd 후보. 대부분의 기존 corpus는 해당하지 **않음** — 순수 루프-사이드.
- **Promotion threshold**: 2개 이상 독립 사용.
- **포인터**: `notes/harness/openwork.md` §11 P1, §13 table.

### U. Server-routed filesystem mutation policy (새 후보 — 좁은 축)
- **Proposed by**: openwork deep-dive (2026-04-19)
- **Rationale**: openwork의 `ARCHITECTURE.md`는 **"쓰기는 서버 경로로, 셸 경로는 fallback"** 단일 규칙으로 permission/approval/audit/reload/remote parity를 한꺼번에 일관화함. Tauri 로컬 FS 호출은 명시적으로 fallback으로 demoted. 축 G("execution environment as constraint surface")와 축 6(tool surface)이 다루지 못하는 **write-path vs read-path 비대칭**과 **"쓰기가 단일 authoritative 서비스를 통과해야 함"**이라는 구체적 architectural rule을 포착함. Cline의 hook system(`PreToolUse`/`PostToolUse`)은 약한 근사치.
- **Proposed form**: "하네스가 write-path와 read-path를 구별하는가? write가 permission/audit/reload/remote-parity 일관성을 위해 단일 authoritative 서비스를 통과하도록 강제되는가? 대안 write 경로는 명시적으로 fallback으로 demoted되어 있는가?"
- **Status**: openwork 1st strong case. Cline hook-gated writes 약한 2nd 후보. 축 G로 fold할지 별도 sub-axis로 유지할지 재사용 관찰 후 결정.
- **Promotion threshold**: 2개 이상 독립 사용.
- **포인터**: `notes/harness/openwork.md` §4 (filesystem mutation policy verbatim), §11 P2.

### Δ1 refinement (openwork, 2026-04-19) — 4th 서브타입 추가 권고
- openwork는 기존 3-branch subtypology 어느 것에도 깔끔하게 맞지 않음:
  - (a) hand-reinvention (OMC↔OMX): substrate가 제공하지 않는 feature를 harness 코드로 재구현. openwork는 OpenCode가 제공하는 것을 재발명하지 않음.
  - (b) single-home + inbound (OMO): single-substrate 플러그인 + inbound 어댑터. openwork는 플러그인이 아님.
  - (c) core + adapter protocol (Cline v3.58): TypeScript core + ACP 공개 표준으로 다중 substrate 배포. openwork는 어댑터 프로토콜을 정의하지 않음.
  - **(d) product-wrapper consumer (openwork)**: 별도 코드베이스가 substrate의 공개 서피스(SDK/CLI/DB)를 소비. 다른 audience(non-tech end-users). 재발명 없이 multi-surface distribution layer 추가.
- **권고**: Δ1을 4-branch subtypology로 확장. openwork의 기여는 "multi-surface product shell이라는 새로운 포지션이 존재함"을 명시화.
- **포인터**: `notes/harness/openwork.md` §13.

### Δ5 (headless-mode-as-first-class output contract) — openwork REFUTES
- **Observed**: openwork는 `openwork-orchestrator` CLI + `--no-tui` 모드 + `openwork serve` 제공. 그러나 (a) JSON 출력 스키마 없음, (b) shell-pipe composition 패턴 문서화 없음, (c) chain composition first-class 아님. openwork의 first-class output은 **SSE events + REST API proxy**지 stdout pipeline이 아님. CLI orchestrator는 "log-only 배포 편의" 포지션.
- **결과**: Δ5 독립 사용 카운트 **무변화** (Cline 단독 강사례 유지). openwork가 headless capability를 "제공"은 하나 "first-class output contract로 승격"은 안 함 — 이 구분이 Δ5의 핵심.
- **포인터**: `notes/harness/openwork.md` §13 last paragraph.

### 축 G 재사용 확인 (openwork, 2026-04-19)
- openwork의 execution environment 제약: (a) 기본 loopback 바인딩(`127.0.0.1`) + 명시적 opt-in으로만 `0.0.0.0` 재바인딩, (b) per-launch random OpenCode 자격증명(셸 히스토리·로그 누출 방지), (c) scoped tokens (owner/collaborator/viewer) + 이중 auth 헤더(`X-OpenWork-Host-Token` legacy + `Authorization: Bearer`), (d) 선택적 Docker / Apple-container 샌드박스 + `~/.config/openwork/sandbox-mount-allowlist.json` 마운트 allowlist, (e) manual 모드 쓰기 approval gate (30s 타임아웃), (f) workspace-scoped server-routed 쓰기. 축 G("execution environment as constraint surface")의 **6번째 독립 사용** (GSD/Ouroboros/OMX-OMC/OMO/Cline에 이어). 승격 권고 최강.

### 축 F / C / A / K / L (openwork는 재사용 NO)
- **축 F**: openwork는 Skills 메커니즘을 **UI에서 관리**하지만 **오피니어네이티드 스킬 라이브러리는 ship하지 않음** (`.opencode/skills/*`은 모두 contributor-facing: release/debug/primitives-reference). Cline과 동일 구분 기준 — "propose/ship curated library" vs "support the mechanism". 카운트 **무변화**.
- **축 C**: openwork 자체의 모드 분할 없음. 모드 분할은 OpenCode 사용자 스킬에서 발생. 카운트 무변화.
- **축 A**: openwork-level iteration loop 없음. OpenCode 루프가 유일한 루프. 카운트 무변화.
- **축 K**: 의미 있는 에이전트 역할 분해 없음. named persona 개념 부재. 카운트 무변화.
- **축 L**: 패턴 자동 추출 루프 없음. openwork는 그냥 OpenCode surface를 노출.

### V. Mode-as-(prompt + tool-allowlist) declarative bundle (새 후보 — 축 C refinement/subtype)
- **Proposed by**: Kilo Code deep-dive (2026-04-19)
- **Rationale**: 모든 기존 C-축 하네스(Superpowers/GSD/Ralph/CE/OMC/Ouroboros/ECC/gstack/OMX/OMC/OMO/Cline)는 모드별 역할 제약을 **프롬프트 본문의 prose** — "you are an X, do not do Y" — 로 표현하고, 모델의 복종에 의존함. Kilo는 모드 정의 자체를 `{roleDefinition, customInstructions, groups: ["read", ["edit", {fileRegex: "\\.md$"}], "browser", "mcp"]}` 튜플로 **스키마 선언**하고, **tool dispatcher 레벨에서 강제**. Architect 모드의 `edit.fileRegex = \\.md$` 제한은 LLM이 따르는지가 아니라 런타임 레벨에서 non-markdown edit가 아예 fail됨. 축 Q(OMO의 category × skill × persona orthogonality)와 쌍대 — OMO는 분리해서 런타임 조합, Kilo는 한 원자로 묶음.
- **Proposed form**: "모드 정의가 (a) prose-only (prompt 내부 자연어) 인가, (b) 스키마-선언적(tool allow-list, per-tool parametric restrictions, regex-scoped edit) 인가? 스키마적이면 어떤 제한 vocabulary를 지원하는가(tool group / per-file regex / per-command glob / model-id override)? 강제는 prompt 신뢰에 맡기는가 dispatcher에 wire되는가?"
- **Status**: Kilo 1회 강한 사례. ECC 47-agent과 Compound Engineering 26-agent가 YAML frontmatter로 tool allowlist를 선언하는지 재확인 필요 — 그렇다면 즉시 2회+ 도달 가능.
- **Promotion threshold**: 2개 이상 독립 사용.
- **포인터**: `notes/harness/kilo-code.md` §5, §11 P1.

### W. Multi-tier server-routed model auto-selection keyed by active mode (새 후보)
- **Proposed by**: Kilo Code deep-dive (2026-04-19)
- **Rationale**: Kilo의 `kilo-auto/{frontier,balanced,free,small}` 4-tier 시스템 + gateway-side `(tier, active_mode) → concrete_model_id` 매핑 + 서버사이드 매핑 업데이트(클라이언트 재배포 없이 free model churn 흡수) + `small` internal-only tier의 positive-balance-fallback-to-free 정책은 코퍼스에서 새로운 종. Compound Engineering이 "claude-opus for reviewer / claude-sonnet for worker" 같은 **per-agent hardcode**를 쓰고, Cline v3.58이 subagent별 `modelId` override를 허용하지만 **클라이언트 pin**. Kilo는 (a) server-owned, (b) mode-triggered(agent-triggered 아님), (c) 비용 티어 매개변수화 세 차원에서 다름. OMO의 category 시스템이 per-agent model 결정을 하지만 여전히 클라이언트 사이드.
- **Proposed form**: "하네스가 '사용자가 고르는 capability tier'와 '이 요청이 실제 도는 구체 model ID'를 분리하는가? (a) 매핑 함수의 위치: 클라이언트 핀 / 서버 라우터 / 둘 다, (b) 라우팅 키: active mode / task category / subagent identity / request cost budget, (c) 매핑 업데이트 투명성(클라이언트 재배포 필요 vs 서버 즉시), (d) fallback 정책(balance zero → free tier) 존재 여부."
- **Status**: Kilo 1회 강한 사례. OMO의 category system이 클라이언트-사이드 near-twin. 서버 라우팅이 추가된 2번째 케이스가 나오면 승격.
- **Promotion threshold**: 2개 이상 독립 사용.
- **포인터**: `notes/harness/kilo-code.md` §8 (Auto-model routing), §11 P4.

### Δ1 refinement (Kilo Code, 2026-04-19) — 5th 서브타입 추가 권고
- Kilo는 기존 4-branch subtypology 어느 것에도 깔끔히 맞지 않음:
  - (a) hand-reinvention (OMC↔OMX): N/A (Kilo는 hand-reinvent 하지 않음).
  - (b) single-home + inbound (OMO): N/A (Kilo는 다중 substrate에 배포).
  - (c) core + adapter protocol (Cline v3.58): N/A (Kilo는 개방 프로토콜 정의 안 함 — SDK는 내부용).
  - (d) product-wrapper consumer (openwork): N/A (Kilo는 substrate를 래핑하지 않음, **벤더링**).
  - **(e) consolidator-fork (Kilo Code)**: 단일 upstream(OpenCode)을 monorepo로 벤더링(`packages/opencode/`)하고, 다른 upstream들(Roo Code, Cline)의 설정 파일명(`.roorules`, `.clinerules`)을 호환성 shim으로 유지해 사용자 흡수. 하나의 포크된 core에서 4+ 클라이언트 서피스(VS Code / JetBrains / TUI / headless CLI / Cloud)로 통일된 배포.
- **권고**: Δ1을 5-branch subtypology로 확장. Kilo의 기여는 "consolidator-fork라는 새 포지션 — 한 upstream 전량 벤더링 + 다른 upstreams로부터의 호환성 shim 사용자 캡처 + forked core에서 단일 출발점으로 multi-surface 배포"를 명시화.
- **포인터**: `notes/harness/kilo-code.md` §1 (CLI fork chain), §4b (`.roorules` / `.clinerules` fallback), §8 (multi-surface distribution).

### 축 C 재사용 확인 (Kilo Code, 2026-04-19)
- Kilo의 6개 native modes(architect/code/ask/debug/orchestrator/review) + user 정의 `.kilo/agents/*.md` + org 정의 Postgres-backed custom modes + primary/subagent/all 3-way mode-use trichotomy는 축 C("mode splitting")의 **12번째 독립 사용** (기존 11에 이어). **승격 확정 최강 유지**.

### 축 F (Kilo Code는 재사용 NO)
- Kilo는 `skill` 툴을 tool surface에 포함하지만 **오피니어네이티드 스킬 라이브러리를 ship하지 않음**. Cline/openwork와 동일 판정. 축 F의 "propose/ship curated library" 기준 미충족. 카운트 **무변화**.

### 축 G 재사용 확인 (Kilo Code, 2026-04-19)
- Kilo의 `kilo serve` HTTP+SSE 계약 + `kilo.jsonc` permission tree + per-command bash glob allow-list + `--auto` YOLO escape hatch + `external_directory` `ask` default + `permission.task` delegation graph 제한 + Kilo Cloud의 Cloudflare Workers / Fly.io / Docker sandbox 레이어 + KiloClaw multi-tenant per-user 머신 + Gas Town 5초 reconciler 루프는 축 G("execution environment as constraint surface")의 **7번째 독립 사용** (GSD/Ouroboros/OMX-OMC/OMO/Cline/openwork에 이어). 승격 권고 최강.

### 축 K 재사용 확인 (Kilo Code, 2026-04-19)
- Kilo의 6개 named 모드 각각이 명시된 전문가 역할(technical leader / software engineer / technical assistant / software debugger / workflow orchestrator / code reviewer)을 1차 제약 대상으로 선언 + org 커스텀 모드 템플릿(DevOps / User Story Creator / Project Research) + `.kilo/agents/*.md` 파일명-슬러그 규약은 축 K("role perspective as constraint surface")의 **7번째 독립 사용** (gstack/ECC/CE/revfactory-harness/OMX-OMC/OMO에 이어). 승격 권고 최강.

### 축 T 재사용 확인 ★ PROMOTION THRESHOLD REACHED (Kilo Code, 2026-04-19)
- Kilo Cloud는 코퍼스에서 **out-of-loop productization surface** 최대 구현: Kilo Gateway(auth/router/catalog/billing) + Cloud Agent(Cloudflare Worker + Docker sandbox) + KiloClaw(Fly.io multi-tenant) + Gas Town(Mayor/Polecat/Refinery/Triage 계층 + 5초 reconciler) + Code Review 서비스(GitHub webhook → auto-review) + Auto Triage(이슈 분류 + vector similarity dedup) + Kilo Bot(GitHub/GitLab mention → Cloud Agent) + App Builder + Webhook Agent Ingest + AI Attribution + Session Ingest. 클라이언트 서피스: VS Code / JetBrains / TUI / `kilo run --auto` headless CLI / Cloud 대시보드. openwork의 2번째 use에 이어 **축 T의 2번째 독립 사용 확인 → 승격 권고 충족**. 다음 schema bump에서 T를 메인 축으로 승격 강력 권고.

### Δ5 (Kilo Code는 provisional REFUTE)
- Kilo는 `kilo run --auto` (CI headless) 와 `kilo serve` (HTTP+SSE) 제공. 그러나 이번 라운드에서 Cline의 `ui_messages.json`에 상응하는 **typed JSON stdout contract**를 primary source에서 확인하지 못함. shell pipe composition 문서화도 발견되지 않음. Kilo는 headless capability를 제공하지만 Δ5의 핵심인 "first-class output contract로 승격" 증거 부재. **잠정 refute** — 2회 카운트 증가 안 함. Δ5는 Cline 단독 강사례 유지. (후속 라운드에서 `packages/opencode/src/` 런타임 검토로 upgrade 가능.)

### 축 U (Kilo Code는 약 2nd use)
- Kilo의 new-platform architecture에서 **모든 tool dispatch가 `kilo serve` HTTP 엔진을 경유** — VS Code extension은 thin client. write-path가 단일 authoritative 서비스(`kilo serve`)를 통과하도록 구조적으로 wire됨. 다만 openwork처럼 "쓰기는 서버, 셸은 fallback" 같은 **명시적 단일 규칙**으로 문서화되어 있지 않음 — architecture index에 암묵적. **약한 2번째 사례**. 축 U 정식 승격은 3번째 강한 사례 대기.
- **포인터**: `notes/harness/kilo-code.md` §3b (new platform), §8 (architecture index).

## Retired axes
(Empty.)
