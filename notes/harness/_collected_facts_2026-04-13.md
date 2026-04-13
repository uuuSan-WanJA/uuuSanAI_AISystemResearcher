---
title: Harness techniques — collected facts (Phase 1 initial sweep)
date: 2026-04-13
source_url: (multiple — see per-entry)
source_type: mixed
topic: harness
tags: [collected, phase1, timeline]
status: processed
---

## 메타
- Phase 1 초기 사실 수집. **분석/해석 없음, 사실만**.
- 각 기법은 향후 `harness-analyzer` 에이전트로 개별 딥다이브 노트로 승격.
- 검증되지 않은 날짜/인용은 `UNVERIFIED` 로 표시되어 있음 — 후속 라운드에서 보강.

## 1. Ralph Wiggum
- **저자**: Geoffrey Huntley (ghuntley.com)
- **공개일**: 2025-07-14
- **1차 출처**: https://ghuntley.com/ralph/
- **부가**: https://github.com/ghuntley/how-to-ralph-wiggum ; Dev Interrupted 팟캐스트 "Inventing the Ralph Wiggum Loop"
- **무엇**: 최소 자율 코딩 하네스. `while :; do cat PROMPT.md | claude-code ; done` 형태의 무한 루프로 동일 프롬프트 파일을 퍼밋션 없이 반복 투입. 매 이터레이션은 신선하게 시작하되 파일시스템에 누적된 아티팩트가 유일한 지속 메모리. Huntley는 이를 "context engineering" 패턴으로 프레임함.
- **인용**: "Ralph is a technique. In its purest form, Ralph is a Bash loop." — Geoffrey Huntley
- **상태**: 원글 단발 + 컴패니언 레포 유지 중. 바이럴.

## 2. Superpowers (obra/superpowers)
- **저자**: Jesse Vincent (blog.fsck.com / Prime Radiant, github:obra)
- **공개일**: 2025-10-09 (블로그와 레포 동일자)
- **1차 출처**: https://blog.fsck.com/2025/10/09/superpowers/
- **부가**: https://github.com/obra/superpowers ; https://github.com/obra/superpowers-lab ; https://blog.fsck.com/2025/12/18/superpowers-4/ ; Simon Willison 커버리지 2025-10-10
- **무엇**: Anthropic 플러그인 시스템 위에 얹은 Claude Code 플러그인. brainstorm → plan → implement 워크플로를 구성하는 SKILL.md 모음. TDD, 체계적 디버깅, 서브에이전트 주도 개발 + 내장 코드리뷰, git worktree 관리, 스킬 작성법 자체까지 스킬로 포함. 설치 시 스타터 시스템 프롬프트와 스킬 디렉토리가 함께 주입됨.
- **인용**: "Skills are what give your agents Superpowers." — Jesse Vincent
- **상태**: 활발. v5.x 계열(2026-03-31 v5.0.7). 400+ 커밋, 28+ 컨트리뷰터.

## 3. GSD — Get Shit Done
- **저자**: TÂCHES (github: gsd-build)
- **공개일**: UNVERIFIED. 가시적 최초 릴리즈 v1.28.0 = 2026-03-22. Medium 설명글(Agent Native) Feb 2026 → 최소 2026-02 이전 공개.
- **1차 출처**: https://github.com/gsd-build/get-shit-done
- **부가**: USER-GUIDE.md ; Medium "GET SH*T DONE: Meta-prompting and Spec-driven Development for Claude Code and Codex" ; codecentric.de 심층 글
- **무엇**: Claude Code/Codex/OpenCode/Cline 등 다중 런타임용 경량 메타프롬프팅 + 스펙 주도 플러그인. 상태를 플래닝 파일로 외부화. 워크스트림당 4단계 루프: `/gsd-discuss-phase <n>` → `/gsd-plan-phase <n>` → `/gsd-execute-phase <n>` → `/gsd-verify-work <n>`. 보조 명령 `/gsd-new-project`, `/gsd-ship`, 고속 패스 `/gsd-quick`. **각 페이즈가 새 서브에이전트 컨텍스트를 스폰해 context rot 완화.**
- **인용**: "If you know clearly what you want, this WILL build it for you." (README 증언)
- **상태**: 활발. ~3주간 v1.28→v1.35.

## 4. Ouroboros (Q00/ouroboros) ✅ 판별 완료 (2026-04-13)
- **저자**: github: Q00
- **공개일**: 2026-01-14 (레포 생성)
- **인기**: ⭐ 2.3k / 🍴 220 (2026-04-13 기준)
- **1차 출처**: https://github.com/Q00/ouroboros
- **부가**: https://github.com/Q00/ouroboros/blob/main/CLAUDE.md
- **무엇**: 사용자와 코딩 에이전트(Claude Code/Codex CLI/OpenCode) 사이에 놓이는 **스펙 우선 워크플로 엔진**. 애드혹 프롬프팅 대신 5단계 사이클: **interview → crystallize spec → execute → evaluate → evolve**. Socratic 질문으로 숨은 가정을 드러낸 뒤 생성 단계로 진입. 인스톨러가 런타임 자동 감지. Claude Code 플러그인 경로도 제공.
- **인용**: "Stop prompting. Start specifying."
- **상태**: 활발 (메인 462커밋).

### 동명 프로젝트 정리
- **razzant/ouroboros** (⭐489, 2026-02-16) — "self-modifying AI agent that writes its own code"; 텔레그램/Colab에서 구동되는 자기개조 자율체. 30+ 자가 진화 사이클 수행. **하네스가 아니라 autonomous self-rewriting agent** 카테고리. 선택적 후속 조사 대상.
- **joi-lab/ouroboros** — 초기 리서처 언급, 미검증 유지. 현 단계 우선순위 낮음.
- **결론**: 사용자의 "우로보로스"는 **Q00/ouroboros** 로 확정. 스타 4.7배 차이 + 하네스 계보 일치.

## 5. Anthropic — Building effective agents
- **저자**: Erik Schluntz, Barry Zhang (Anthropic)
- **공개일**: 2024-12-19
- **1차 출처**: https://www.anthropic.com/research/building-effective-agents
- **부가**: https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents
- **무엇**: 에이전트 패턴의 표준 분류학. **workflows**(코드 경로로 오케스트레이션) vs **agents**(LLM이 스스로 프로세스 지시) 구분. 패턴: augmented LLM, prompt chaining, routing, parallelization (sectioning/voting), orchestrator-workers, evaluator-optimizer, autonomous agents. 쿡북 코드 동반.
- **인용**: "Workflows are systems where LLMs and tools are orchestrated through predefined code paths. Agents, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."
- **상태**: 단발 포스트, 업계 표준 참조.

## 6. Anthropic — Effective context engineering for AI agents
- **저자**: Anthropic 엔지니어링 팀
- **공개일**: 2025-09-29 (Sonnet 4.5 동시 발표)
- **1차 출처**: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- **무엇**: "context engineering"을 prompt engineering의 후계로 프레이밍. 유한 어텐션 제약 하에서 모델이 보는 토큰 집합을 전략적으로 큐레이션·관리하는 것. 시스템 프롬프트 설계, 툴 셋, 검색, 메시지 히스토리 압축, 멀티턴 에이전트 동학 다룸.
- **인용**: "Find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome."
- **상태**: 단발 엔지니어링 포스트.

## 7. Anthropic Agent Skills
- **저자**: Anthropic
- **공개일**: 2025-10-16
- **1차 출처**: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **부가**: Simon Willison "Claude Skills are awesome, maybe a bigger deal than MCP" (2025-10-16)
- **무엇**: SKILL.md + 스크립트 + 리소스를 담은 자기완결 폴더를 온디맨드 로드. Anthropic 관리 스킬(.pptx/.xlsx/.docx/.pdf 저작) + 커스텀 업로드용 Skills API 동시 출시. **Superpowers 등 서드파티 스킬 에코시스템의 기판.**
- **인용**: (1차 출처 verbatim 미수집)
- **상태**: Anthropic 기본 기능, 활발.

## 8. GitHub Spec Kit
- **저자**: GitHub (github/spec-kit)
- **공개일**: 2025-08 ~ 2025-09 초 (정확일 UNVERIFIED)
- **1차 출처**: https://github.com/github/spec-kit
- **부가**: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/ ; Martin Fowler "SDD 3 tools"
- **무엇**: GitHub의 SDD 오픈소스 툴킷. Copilot/Claude Code/Gemini CLI 교차 지원. 슬래시 명령 체인: `/speckit.constitution` → `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`. 스펙이 구현의 생성 소스.
- **인용**: (미수집)
- **상태**: 활발, 대규모 스타.

## 9. BMAD-METHOD
- **저자**: bmad-code-org
- **공개일**: UNVERIFIED (CHANGELOG 존재, 미검사)
- **1차 출처**: https://github.com/bmad-code-org/BMAD-METHOD
- **무엇**: ~21개 전문 에이전트 페르소나(PM/Architect/Dev/UX…) + 50+ 워크플로, 버그픽스~엔터프라이즈까지 스케일 적응 라우팅. `npx bmad-method` 설치. "Party Mode" 다중 페르소나 동시 세션. Claude Code/Cursor 등 크로스IDE. BMAD = "Build More Architect Dreams" 로 리브랜딩.
- **상태**: 활발.

## 10. Agent OS (buildermethods/agent-os)
- **저자**: Builder Methods
- **공개일**: UNVERIFIED
- **1차 출처**: https://github.com/buildermethods/agent-os
- **무엇**: 코드베이스의 코딩 표준과 프로덕트 미션을 에이전트 워크플로에 주입하는 프레임워크. `/discover-standards`(기존 코드베이스에서 표준 도출/저자화), `/inject-standards`(플랜/스킬/대화에 주입). 스펙 작성은 Claude Code Plan Mode에 위임, `/shape-spec` 으로 증강.
- **상태**: v3 라인 (2026 기준).

## 11. Jesse Vincent — "How I'm using coding agents in September, 2025"
- **저자**: Jesse Vincent
- **공개일**: 2025-10-05
- **1차 출처**: https://blog.fsck.com/2025/10/05/how-im-using-coding-agents-in-september-2025/
- **무엇**: Superpowers 직전의 개인 Claude Code 워크플로 기록. 아이디어를 설계·스펙으로 바꾸는 Socratic 방식의 "brainstorm" 프롬프트, 이어서 코드 전 comprehensive plan을 만드는 planning 프롬프트. **4일 뒤 Superpowers의 직계 조상**.
- **상태**: 단발 포스트.

## 12. steipete — "Claude Code is My Computer"
- **저자**: Peter Steinberger (steipete.me)
- **공개일**: 2025-06-03
- **1차 출처**: https://steipete.me/posts/2025/claude-code-is-my-computer
- **부가**: /claude-code-anonymous, /command-your-claude-code-army-reloaded, /just-talk-to-it, /just-one-more-prompt
- **무엇**: `--dangerously-skip-permissions`로 Claude Code를 범용 컴퓨팅 인터페이스로 쓰는 에세이. 2개월 사용 사례: 커밋, CI 감시, 콘텐츠 마이그레이션, sysadmin. $200/월 Max 플랜 정당화 주장. "YOLO 모드" 규범 대중화 시리즈 중 핵심.
- **인용**: "I haven't typed `git commit -m` in weeks. Instead, I say 'commit everything in logical chunks' and Claude handles the entire flow."
- **상태**: 단발 + 연관 시리즈.

---

## 연대표 (공개순)

| 날짜 | 이름 | 한줄 |
|---|---|---|
| 2024-12-19 | Anthropic — Building effective agents | workflows vs agents 표준 분류학 |
| 2025-06-03 | steipete — Claude Code is My Computer | YOLO 모드 범용 컴퓨팅 대중화 |
| 2025-07-14 | Ralph Wiggum (Huntley) | `while :; do cat PROMPT.md \| claude-code ; done` |
| ~2025-08 | GitHub Spec Kit | SDD 툴킷, `/speckit.*` |
| 2025-09-29 | Anthropic — Context engineering | prompt→context engineering 패러다임 |
| 2025-10-05 | Jesse Vincent — Sep 2025 post | brainstorm→plan→implement |
| 2025-10-09 | Superpowers (obra) | 플러그인 기반 스킬 프레임워크 |
| 2025-10-16 | Anthropic Agent Skills | SKILL.md 온디맨드 로드 기판 |
| 2026-01-14 | Ouroboros (Q00) | interview→crystallize→execute→evaluate→evolve |
| ~2026-02 | GSD / Get Shit Done | discuss/plan/execute/verify 4페이즈 + 프레시 서브에이전트 |
| UNVERIFIED | BMAD-METHOD | ~21 페르소나, Party Mode |
| UNVERIFIED | Agent OS v3 | 표준 주입 레이어 |

## 갭 & 후속 작업
- [ ] GSD 최초 릴리즈 정확일 확인 (releases 페이지 페이지네이션)
- [ ] Ouroboros — 사용자가 어떤 "우로보로스"를 가리키는지 확인 필요 (Q00 / razzant / joi-lab)
- [ ] 1차 출처 verbatim 인용 미수집: Skills, Spec Kit, BMAD, Agent OS, Jesse Sep post
- [ ] BMAD / Agent OS / Spec Kit 정확한 공개일
- [ ] 한국 커뮤니티 맥락 추가 조사: revfactory/harness(한국어 README), Toss Tech "Software 3.0 시대, Harness를 통한 조직 생산성 저점 높이기", FastCampus "전현준의 하네스 엔지니어링" — 기법 발명이라기보다 조직/교육 자료
- [ ] 각 항목을 `harness-analyzer` 에이전트로 개별 심층 노트로 승격

---

## Candidates discovered 2026-04-13 (round 2)

라운드 2 스윕. WebSearch 기반, 1차 출처 URL 기록. 각 항목 `_collected_facts_2026-04-13.md` 위쪽 1~12번 엔트리와는 **중복 없음**(이미 커버된 것은 `[COVERED]` 로 명시).

### A. OpenSpec (Fission AI)
- **저자**: Fission-AI (github:Fission-AI/OpenSpec)
- **URL**: https://github.com/Fission-AI/OpenSpec ; https://openspec.dev/
- **포지셔닝**: "엄격한 3단계 스테이트 머신(proposal → apply → archive)을 강제하는 경량 스펙 주도 프레임워크. 브라운필드 이터레이션에 ADDED/MODIFIED/REMOVED 델타 마커 도입."
- **공개일**: 2025 중반 ~ 2025 말 (정확일 UNVERIFIED, 2026-04 시점 ~30k★)
- **어답션**: GitHub 30k★+, Cursor/Claude Code/Windsurf/Copilot/Trae 등 20+ 어시스턴트 지원, Martin Fowler "SDD 3 tools" 기사에서 Spec Kit과 함께 거론.
- **왜 분석할 가치**: Spec Kit 대비 **경량**(250줄 vs 800줄), 델타 모델, `/opsx:propose` 슬래시 워크플로 — 라운드 1의 Spec Kit/gstack/GSD 라인과 같은 계보이지만 가장 "라이트"한 극. SDD 축의 스펙트럼 완성에 필수.
- **커버**: ❌ (라운드 1 갭 페이지의 `후속` 언급도 아님)

### B. AWS Kiro
- **저자**: Amazon Web Services
- **URL**: https://kiro.dev/
- **포지셔닝**: "AWS의 스펙 주도 에이전트 IDE. Requirements(EARS notation) → Design → Tasks 3페이즈 강제, Amazon Bedrock 기반, agent hooks로 파일 저장/생성/삭제 이벤트 트리거."
- **공개일**: 2025-12-02 공개 프리뷰 (TechCrunch), 2026-02 GovCloud 확장
- **어답션**: AWS 공식 프로덕트, Claude Sonnet 4.0/3.7 모델 선택. 비공개 라이선스.
- **왜 분석할 가치**: SDD 상용화 축의 대표. 오픈소스(Spec Kit/OpenSpec)와 대비되는 "벤더 통합 IDE" 모델. **플러그인 아님** — 라운드 1 프레임과는 다른 카테고리(IDE-harness)라 포함 여부 논의 필요.
- **커버**: ❌

### C. Compound Engineering / Every.to 플러그인
- **저자**: Kieran Klaassen (Every/Cora), Dan Shipper
- **URL**: https://every.to/guides/compound-engineering ; https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents
- **포지셔닝**: "**Plan → Work → Review → Compound** 4단계 루프. 각 단계의 아웃풋이 다음 단계의 인풋. 12개 병렬 서브에이전트 리뷰. 26개 전문 에이전트로 구성된 Claude Code 플러그인으로 배포."
- **공개일**: 가이드 2025 후반, Claude Code 플러그인 ~2026 Q1 (정확일 UNVERIFIED)
- **어답션**: Every.to 미디어 노출 대규모, Kieran Klaassen(Cora CEO) 팟캐스트, Ry Walker "Compound Engineering Plugin" 리서치 노트.
- **왜 분석할 가치**: **Superpowers/gstack과 같은 플러그인 카테고리지만 "자기 개선(compound)" 단계가 명시적** — 리뷰 결과를 다음 루프의 시스템 개선에 피드백. 라운드 1에는 이 개념이 없음.
- **커버**: ❌

### D. Everything Claude Code (ECC)
- **저자**: Affaan Mustafa (github:affaan-m/everything-claude-code)
- **URL**: https://github.com/affaan-m/everything-claude-code
- **포지셔닝**: "agent harness performance optimization system. Skills + Instincts + Memory + Security + Research-first. 자체 오케스트레이션 엔진 NanoClaw v2(모델 라우팅, skill hot-loading, 세션 브랜칭)."
- **공개일**: 2026-01 오픈소스 공개 (10+개월 개인 사용 후)
- **어답션**: **82k★+ / 10.7k fork** (2026-03 Medium 보도 기준). 라운드 1 스윕에서 가장 큰 스타 레포 누락. Claude Code/Codex/Cursor/OpenCode 크로스.
- **왜 분석할 가치**: **규모 1위** 후보. Superpowers보다 큰 스타, "harness performance optimization" 브랜딩, NanoClaw 오케스트레이터는 독자적인 레이어. 커뮤니티 분열 서사(Medium "dividing the developer community")도 연구 가치.
- **커버**: ❌ — **최우선 탑 픽**

### E. gstack (Garry Tan)
- **저자**: Garry Tan (Y Combinator CEO), github:garrytan/gstack
- **URL**: https://github.com/garrytan/gstack
- **포지셔닝**: "Garry Tan의 실사용 Claude Code 셋업. 23개 특화 슬래시 명령(CEO / Designer / Eng Manager / Release Manager / Doc Engineer / QA) + 8 power tools. MIT."
- **공개일**: Product Hunt 런칭 2026 Q1 (UNVERIFIED)
- **어답션**: YC CEO 개인 브랜드 등에 업음. Medium/Junia/DEV 에 대량 비교글. "Superpowers/GSD/gstack 스택" 으로 페어링되는 표준 3인조.
- **왜 분석할 가치**: **이미 TaskList에 in_progress** — 별도 딥다이브 진행 중. 라운드 1 _collected_facts에는 엔트리가 없어 추가 필요.
- **커버**: ⚠️ TaskList에는 있음, 본 파일에는 ❌

### F. revfactory/harness (Minho Hwang, 한국)
- **저자**: Minho Hwang (github:revfactory)
- **URL**: https://github.com/revfactory/harness ; https://revfactory.github.io/harness/
- **포지셔닝**: "도메인별 에이전트 팀을 설계하는 **메타 스킬**. `build a harness for this project` 한 마디로 `.claude/agents/` + `.claude/skills/` 자동 생성. 6개 아키텍처 패턴(Pipeline, Fan-out/Fan-in, Expert Pool, Producer-Reviewer, Supervisor, Hierarchical Delegation) 지원."
- **공개일**: UNVERIFIED. 컨트롤드 실험(15 SE tasks, 49.5→79.3 점)이 포지셔닝 증거로 제시됨. Korean README 존재.
- **어답션**: `revfactory/harness-100` 에서 10 도메인 × 100 프로덕션 레디 팀 (영/한 200 패키지). FastCampus "전현준의 하네스 엔지니어링" 의 전현준과는 별개 인물로 보임(확인 필요).
- **왜 분석할 가치**: **한국 커뮤니티 대표 OSS harness**. 사용자가 한국인이라는 점에서 계보 조사 필수. 메타-스킬(harness-to-generate-harnesses) 개념은 이 스윕에서 유일.
- **커버**: ❌ (라운드 1 갭 섹션에 이름만 언급됨)

### G. OpenHarness (HKUDS)
- **저자**: HKU Data Intelligence Lab (github:HKUDS/OpenHarness), 리드 Chao Huang
- **URL**: https://github.com/HKUDS/OpenHarness
- **포지셔닝**: "Claude Code의 ~1/44 사이즈(11,733 LoC) 순수 Python 대안. 43 tools (98% 커버), 54 commands (61%), MCP 지원, React TUI, 멀티 에이전트 조정. Ohmo 내장 퍼스널 에이전트."
- **공개일**: 2026 Q1 (X 트윗 & PyTorchKR 한국 커뮤니티 소개 2026-04 이전)
- **어답션**: HKUDS 브랜드, 연구용/해킹용 레퍼런스 구현체, Claude/OpenAI/Codex/Kimi/GLM/MiniMax 엔드포인트 호환.
- **왜 분석할 가치**: 플러그인/스킬이 아니라 **하네스 런타임 자체**의 오픈 레퍼런스. Claude Code 바이너리 내부를 블랙박스로 못 보는 제약을 풀어주는 역할. Phase 1 "편향 없는 외부 리서치" 목적에 매우 적합 — 아키텍처 해부용 비교 샘플.
- **커버**: ❌

### H. AutoAgent (Kevin Gu)
- **저자**: Kevin Gu (github:kevinrgu/autoagent)
- **URL**: https://github.com/kevinrgu/autoagent
- **포지셔닝**: "**하네스 엔지니어링 루프 자체를 자동화**하는 오픈소스 라이브러리. 시스템 프롬프트/툴/오케스트레이션/라우팅을 벤치마크 스코어 기반으로 밤새 이터레이트. 24h 런 → SpreadsheetBench 96.5% 1위, TerminalBench 55.1% GPT-5 최고점."
- **공개일**: 2026-04-05 (MarkTechPost)
- **어답션**: MarkTechPost, Medium, 여러 뉴스레터, Karpathy "autoresearch" 프레임으로 소개됨.
- **왜 분석할 가치**: **"harness를 사람이 짜는 시대"의 종말 논제**. 자기-최적화 외부 루프 카테고리의 대표. Ralph 루프가 "같은 프롬프트 반복"이라면 AutoAgent는 "프롬프트/툴 자체를 진화". 새로운 축.
- **커버**: ❌ — **연구 사이클의 논리적 다음 단계**

### I. Harness Evolver / Meta-Harness 논문
- **저자**: Yoonho Lee, Roshen Nair, Qizheng Zhang, Kangwook Lee, Omar Khattab, Chelsea Finn (2026 preprint)
- **URL**: https://arxiv.org/abs/2603.28052 ; https://yoonholee.com/meta-harness/
- **포지셔닝**: "하네스 코드 자체를 아우터 루프로 검색. 에이전티크 프로포저가 파일시스템을 통해 과거 후보들의 소스/스코어/트레이스 접근. online text classification에서 SOTA 컨텍스트 관리 시스템 대비 +7.7점, 컨텍스트 토큰 1/4."
- **어답션**: Hugging Face Papers, arXiv, walkinglabs/awesome-harness-engineering 큐레이션 포함.
- **연관 OSS**: **Harness Evolver** — Meta-Harness를 구현한 Claude Code 플러그인, multi-agent proposers + LangSmith 평가 + git worktree 격리.
- **왜 분석할 가치**: AutoAgent와 짝. **학술-산업 브리지**. Chelsea Finn/Omar Khattab 이름 가치.
- **커버**: ❌

### J. Hermes Agent (Nous Research)
- **저자**: Nous Research (github:NousResearch/hermes-agent)
- **URL**: https://github.com/nousresearch/hermes-agent ; https://hermes-agent.nousresearch.com/docs/
- **포지셔닝**: "자기 개선 에이전트. 복잡 태스크 후 자율 스킬 생성, 사용 중 스킬 자가 개선, SQLite + FTS5로 크로스 세션 메모리(~10ms 검색, 10k+ 스킬 스케일), MEMORY.md 2,200자 / USER.md 1,375자로 바운디드 큐레이션."
- **공개일**: v0.2.0 문서화 2026 초반, 2026-04 기준 v0.8.0, 3,496+ commits.
- **어답션**: Nous Research 브랜드, awesome-hermes-agent 큐레이션, Hermes WebUI 등 에코시스템.
- **왜 분석할 가치**: **에이전트 런타임 + 자기-성장 메모리** 결합. Ouroboros의 "evolve" 단계를 데이터레이어로 구현한 사례. Anthropic 스킬 시스템과 평행진화.
- **커버**: ❌

### K. Chachamaru127/claude-code-harness (일본 커뮤니티)
- **저자**: Chachamaru (github:Chachamaru127)
- **URL**: https://github.com/Chachamaru127/claude-code-harness
- **포지셔닝**: "Plan → Parallel Implementation → Review → Commit 자율 루프. Phase 0(Planning Discussion)에서 Planner + Critic이 플랜을 챌린지 후 승인. v4에서 42 스킬을 5 verb 스킬로 통합. harness-mem으로 세션 간 기억."
- **공개일**: UNVERIFIED
- **어답션**: 일본어권 중심, SpecKit/Superpowers 비교글에서 독립 4번째 후보로 언급됨.
- **왜 분석할 가치**: **"verb 스킬" 추상화** + CI/CD 통합(CHANGELOG/tag/release 자동화)이 독특. 다만 스타 규모는 ECC/Superpowers 대비 작음.
- **커버**: ❌

### L. Agent HQ (GitHub)
- **저자**: GitHub / Microsoft
- **URL**: https://github.blog/news-insights/company-news/welcome-home-agents/
- **공개일**: 2026-02-04 런칭
- **포지셔닝**: "Claude / Codex / Copilot을 **교환 가능**하게 쓰는 GitHub 통합 미션 컨트롤. GitHub / VS Code / 모바일 / CLI 단일 인터페이스. 거버넌스 우선(아이덴티티/승인/샌드박스) 멀티 에이전트 허브."
- **어답션**: GitHub Universe 발표, 엔터프라이즈 관리 제어.
- **왜 분석할 가치**: **거버넌스 계층**의 대표. 플러그인/스킬과는 다른 "멀티 에이전트 오케스트레이터" 카테고리. 단, 상용 플랫폼이라 오픈 하네스 분석과는 축이 다름.
- **커버**: ❌ (카테고리 경계선)

### M. HumanLayer / CodeLayer
- **저자**: HumanLayer Inc. (YC F24) — Dex Horthy 등
- **URL**: https://www.humanlayer.dev/ ; https://github.com/humanlayer/humanlayer ; https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents
- **포지셔닝**: "하드 코드베이스에서 AI 코딩 에이전트를 동작시키는 오픈소스 플랫폼. CLAUDE.md 공학, context engineering 블로그 시리즈, CodeLayer(팀 스케일링 레이어)."
- **공개일**: HumanLayer 코어 2024, "Skill Issue" 포스트 2026
- **어답션**: YC, 블로그 시리즈가 Superpowers/ECC와 함께 harness-engineering 담론 주도.
- **왜 분석할 가치**: Superpowers가 "개인 크래프트"라면 HumanLayer는 "팀/기업 스케일". 그리고 **"harness engineering" 이라는 용어 자체를 유행시킨 블로그**. 이론 배경으로 필수 인용.
- **커버**: ❌

### N. Sondera — coding-agent-hooks
- **저자**: Sondera AI (github:sondera-ai/sondera-coding-agent-hooks)
- **URL**: https://github.com/sondera-ai/sondera-coding-agent-hooks
- **포지셔닝**: "AI 코딩 에이전트용 **reference monitor**. Rust 훅 바이너리 + Cedar 정책으로 모든 shell/파일/웹 호출 인터셉트, exfiltration/파괴 방지, information flow control."
- **어답션**: 블로그 트래픽은 작지만 braintrust/humanlayer 라인에서 인용.
- **왜 분석할 가치**: **보안/샌드박싱 레이어** 유일 후보. YOLO 모드 유행에 대한 카운터-내러티브. 하네스의 "안전 벨트" 축.
- **커버**: ❌

### O. 한국 커뮤니티 담론 & 자료
- **Toss Tech — "Software 3.0 시대, Harness를 통한 조직 생산성 저점 높이기"**: https://toss.tech/article/harness-for-team-productivity — 하네스를 "조직의 최저 생산성" 끌어올림 도구로 포지셔닝. 기법이 아닌 **조직론**. 이론 배경.
- **FastCampus — 전현준의 하네스 엔지니어링 (Claude Code · Codex 완벽 가이드)**: https://fastcampus.co.kr/data_online_harness — 유료 강의. 한국 시장에서 harness-engineering 용어를 대중화.
- **PyTorchKR 커뮤니티의 OpenHarness 소개**: https://discuss.pytorch.kr/t/openharness-claude-code-44-python-ai-feat-hkuds/9559 — 한국어 2차 출처로서 OpenHarness 조사에 유용.
- **박재홍의 실리콘밸리 (wikidocs) — Claude Code 소스 유출과 하룻밤 오픈소스 하니스 엔진**: https://wikidocs.net/blog/@jaehong/10418/ — OpenHarness 출현 맥락 한국어 기록.
- **gpters.org "Claude Code + OpenClaw — 하네스 엔지니어링으로 스스로 진화하는 시스템"**: https://www.gpters.org/nocode/post/ai-work-automation-becomes-ZieUe6gA1MSxYnE — "OpenClaw" 라는 추가 후보 언급. 미탐색.
- **왜 분석할 가치**: 한국 사용자의 **언어 맥락**에서 harness 용어가 어떻게 번역/유통되는지 기록. 개별 기법 발명보다 **수용사** 축. Phase 1 에서 중요도 중간.
- **커버**: ⚠️ (라운드 1 갭 섹션에 revfactory/harness, Toss, FastCampus 언급은 있으나 확장 없음)

### P. 참고 큐레이션 레포
아래는 그 자체로 딥다이브 대상이 아니라 **2차 스윕용 카탈로그**. 메타데이터만 기록.
- https://github.com/walkinglabs/awesome-harness-engineering — harness-engineering 전용 awesome 리스트. Meta-Harness, Harness Evolver 등 학술-산업 링크.
- https://github.com/ai-boost/awesome-harness-engineering — 같은 주제 다른 큐레이션.
- https://github.com/AutoJunjie/awesome-agent-harness — 에이전트 하네스 큐레이션.
- https://github.com/hesreallyhim/awesome-claude-code — skills/hooks/slash commands/orchestrators/plugins 종합.
- https://github.com/quemsah/awesome-claude-plugins — n8n으로 자동 수집된 플러그인 어답션 메트릭.
- **왜 기록**: 라운드 3 스윕에서 격자 전체를 긁을 때 진입점. 이번 라운드에서는 개별 항목 심층 추적 X.

### 룰아웃 (명시적 제외)
- **Cursor / Copilot / Aider / Cline / Windsurf** — 제네릭 AI 코딩 툴. 룰 제외.
- **joi-lab/ouroboros** — 라운드 1에서 미검증 유지 결정. 변경 없음.
- **razzant/ouroboros** — self-rewriting autonomous agent 카테고리. 하네스 아님.
- **BulloRosso/etienne**, **aden-hive/hive** — 1차 서치에만 등장, 커뮤니티 트랙션 미확인. 룰아웃 보류.
- **Agent HQ / Kiro** — 상용 IDE/플랫폼. 포함 여부는 케이스별 판단 (상기 엔트리에 카테고리 경계선 명시).

