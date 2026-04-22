# Sources Registry

모니터링 후보 소스. 리서치 중 발견되는 대로 추가하고, 실제로 유용하면 `status: active` 로 승격.

## Format
- **Name** — URL — type (blog/repo/newsletter/forum/social) — topic tags — status (candidate/active/dropped) — note

## Active
- Anthropic Engineering Blog — https://www.anthropic.com/engineering — blog — harness, agents, techniques, evals — active — 2026-04-17 전면 스윕: 10개 포스트를 `notes/techniques/anthropic-*.md`로 정리. 이후 신규 포스트 발행 시 증분 업데이트.
- Graphify (safishamsi/graphify) — https://github.com/safishamsi/graphify — repo — knowledge-graph, cross-harness-skill, pkm, leiden, confidence-tiering — active — 2026-04-21 deep-dive 완료 (`notes/techniques/graphify.md`). PyPI `graphifyy`. cross-harness skill tier 후보 1사례. Karpathy LLM Wiki 트윗 48h 후 릴리스. 신규 릴리스 모니터링 가치 (17일 만에 31k stars 폭발).
- Basic Memory (basicmachines-co) — https://github.com/basicmachines-co/basic-memory — repo — pkm, mcp, obsidian, markdown — active — 2026-04-21 deep-dive 완료 (`notes/techniques/basic-memory.md`). 저자 블로그 2026-03-15 "If you can't read it, edit it, or take it with you — it's not yours" + "Basic Memory vs Mem0 vs Letta vs Everyone Else". 후속 블로그/릴리스 모니터링.
- Cognee (topoteretes) — https://github.com/topoteretes/cognee — repo — agent-memory, knowledge-graph, vector, relational, memify — active — 2026-04-21 deep-dive 완료 (`notes/techniques/cognee.md`). Apache-2.0, v1.0.1 (2026-04-18). 4-op API (`remember/recall/forget/improve`) + 3중 스토리지. `cognee.ai/blog/deep-dives/ai-memory-tools-evaluation` 에 경쟁 벤치마크 (Mem0/Zep/Graphiti + 상용 Dreamify). 후속 블로그/메이저 릴리스 모니터링.
- Letta (letta-ai, 구 MemGPT) — https://github.com/letta-ai/letta + https://github.com/letta-ai/letta-code — repo — agent-memory, memfs, git-tracked, sleep-time, self-editing — active — 2026-04-21 deep-dive 완료 (`notes/techniques/letta.md`). Apache-2.0, server v0.16.7 + Letta Code v0.22.4. 두 레이어 (server Python = 4-tier blocks/files/archival/RAG + Letta Code TS/npm = MemFS git-backed markdown). MemFS 0.15.0 도입 (Letta Code 한정으로 server `memory(...)` 도구 대체). `/doctor` (context_doctor skill) + `reflection` subagent. 본 deep-dive 가 carve-out 트리거 도달시킴 (structural lint + consolidation+feedback 둘 다 2 사례). 후속 메이저 릴리스 + ACP 프로토콜 docs 모니터링.
- Claude Design (Anthropic Labs) — https://www.anthropic.com/news/claude-design-anthropic-labs + https://support.claude.com/en/articles/14604416-get-started-with-claude-design — blog+docs — design-tool, opus-4-7, handoff-bundle, frontend-design-skill — active — 2026-04-22 deep-dive 완료 (`notes/harness/claude-design.md`). research preview, `claude.ai/design`. 런칭 2026-04-17. Opus 4.7 substrate (3.75MP vision). Claude Code 로 tar+README handoff. `frontend-design` skill productization 의 첫 사례. FIG 주가 당일 −7%. 후속 릴리스 + handoff bundle schema 모니터링.
- gpt-image-2 (ChatGPT Images 2.0, "Duct Tape") — https://developers.openai.com/api/docs/models/gpt-image-2 + https://openai.com/index/introducing-chatgpt-images-2-0/ (announcement, 403) — docs+blog — image-gen-model, multilingual-text, thinking-mode, arena — active — 2026-04-22 deep-dive 완료 (`notes/harness/gpt-image-2.md`). 런칭 2026-04-21. Instant/Thinking 2-mode split. Arena +242 대 Nano Banana 2 (비-라틴 +316). 99% 타이포 주장 (benchmark 명칭 미공개). fal.ai + Azure Foundry day-0 GA. 시스템 카드/논문 release 모니터링 필요.
- Anthropic News (Opus 모델 announcement 계열) — https://www.anthropic.com/news/ — blog — model-release, pricing, benchmarks — active — Opus 4.7 (2026-04-16) 이 Claude Design 의 substrate. Anthropic Engineering Blog 와는 다른 stream (제품·모델 공지 vs 엔지니어링 방법론). 증분 모니터링.

## Candidates
- Simon Willison's Weblog — https://simonwillison.net/ — blog — llm, tools, hands-on — candidate → **promote 후보** — 2026-04-21 gpt-image-2 hands-on 이 deep-dive 에 결정적 datapoint 제공 ($0.40 / 3840×2160). 본 프로젝트 노트에 3+건 인용 시 Active 승격.
- fal.ai — https://fal.ai/ + https://fal.ai/learn/ — docs+blog — model-hosting, pricing, image-gen — candidate — gpt-image-2 day-0 host. OpenAI/Google/BFL 등 다종 모델 pay-per-call. 이미지/영상 모델 추적의 2차 벤치마크로 유용.
- Victor Dibia newsletter — https://newsletter.victordibia.com/ — newsletter — ai-tools, hands-on, technical-review — candidate — Claude Design handoff bundle 의 tar+README 구조 첫 관찰. Microsoft AutoGen 관련 배경. 기술 리뷰 품질 우수.
- Sam Henri Gold blog — https://samhenri.gold/blog/ — blog — design, ai-tools, first-principles — candidate — Claude Design "HTML and JS all the way down" 관찰. 디자이너 관점의 AI 도구 리뷰. 빈도 낮지만 신호 높음.
- The Neuron Daily — https://www.theneurondaily.com/ — newsletter — ai-community-sentiment, reddit, x — candidate — 커뮤니티 reaction 집약 (r/ClaudeAI, X, HN 동시). Claude Design + gpt-image-2 런칭 주에 여러 번 인용됨. sentiment 수집용.
- choi.openai (Threads) — https://www.threads.com/@choi.openai — social — ai-models, korean-early-signal, openai — candidate — 한국어권 OpenAI 관련 early-signal. 2025-10 Claude Code `frontend-design` skill + 2026-04 gpt-image-2 post-launch 한국어 렌더링 클레임. 영어권 언론 대비 12~48h 빠름.
- @aisocity (Threads) — https://www.threads.com/@aisocity — social — ai-models, korean-early-signal, leaks — candidate — 2026-04-04 gpt-image-2 Arena prelaunch 첫 한국어 식별. prelaunch-arena-watcher 패턴의 채널.
- qjc.ai (Threads) — https://www.threads.com/@qjc.ai — social — ai-models, benchmarks, nano-banana — candidate — Nano Banana Pro 8-point displacement 분석. 구체 테스트 프롬프트 제공.
- rohitg00/awesome-claude-design — https://github.com/rohitg00/awesome-claude-design — repo — prompt-patterns, design-templates — candidate — 런칭 직후 등장한 prompt-pattern curation. ZeroLu/awesome-gpt-image 와 함께 `primitive-prompt-pattern-market` insight carve-out 의 2 사례.
- ZeroLu/awesome-gpt-image — https://github.com/ZeroLu/awesome-gpt-image — repo — prompt-patterns, image-gen — candidate — gpt-image-2 런칭 직후 등장. awesome-claude-design 의 짝.
- LangChain Blog — blog — agents — candidate
- r/LocalLLaMA — forum — llm, harness — candidate
- HN front page (AI tag) — forum — general — candidate
- Karpathy's gists — https://gist.github.com/karpathy — gist — techniques, knowledge-base — candidate — 2026-04-19 LLM Wiki gist (442a6bf...) 조사로 편입. 추가 gist 발행 시 체크.
- Michał Nasternak (Medium) — https://michalnasternak.medium.com/ — blog — rag, wiki, production — candidate — LLM Wiki 스케일 하이브리드 글 저자. 프로덕션 RAG 관점의 재정리 유용.
- Astro-Han/karpathy-llm-wiki — https://github.com/Astro-Han/karpathy-llm-wiki — repo — agent-skills, wiki — candidate — Agent Skills 포장형 구현체. SKILL.md 딥다이브 후보.
- Brain Trinity (Brian, YouTube) — `https://youtu.be/cNlvrU-KcRg` (채널 URL 식별 필요) — youtube — 한국어권 AI 워크플로 튜토리얼 — candidate — 2026-04-21 첫 노출 (LLM Wiki+Graphify 영상). 한국 커뮤니티 수용·메타 스택 관찰용. 채널 전체 modeling 가치 재평가 필요.
- ~~Graphify — (upstream 식별 필요)~~ → **Active 섹션으로 승격** (2026-04-21 upstream 확정 + deep-dive 완료).

## Dropped
(없음)
