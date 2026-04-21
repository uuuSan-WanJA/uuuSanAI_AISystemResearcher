# Sources Registry

모니터링 후보 소스. 리서치 중 발견되는 대로 추가하고, 실제로 유용하면 `status: active` 로 승격.

## Format
- **Name** — URL — type (blog/repo/newsletter/forum/social) — topic tags — status (candidate/active/dropped) — note

## Active
- Anthropic Engineering Blog — https://www.anthropic.com/engineering — blog — harness, agents, techniques, evals — active — 2026-04-17 전면 스윕: 10개 포스트를 `notes/techniques/anthropic-*.md`로 정리. 이후 신규 포스트 발행 시 증분 업데이트.
- Graphify (safishamsi/graphify) — https://github.com/safishamsi/graphify — repo — knowledge-graph, cross-harness-skill, pkm, leiden, confidence-tiering — active — 2026-04-21 deep-dive 완료 (`notes/techniques/graphify.md`). PyPI `graphifyy`. cross-harness skill tier 후보 1사례. Karpathy LLM Wiki 트윗 48h 후 릴리스. 신규 릴리스 모니터링 가치 (17일 만에 31k stars 폭발).
- Basic Memory (basicmachines-co) — https://github.com/basicmachines-co/basic-memory — repo — pkm, mcp, obsidian, markdown — active — 2026-04-21 deep-dive 완료 (`notes/techniques/basic-memory.md`). 저자 블로그 2026-03-15 "If you can't read it, edit it, or take it with you — it's not yours" + "Basic Memory vs Mem0 vs Letta vs Everyone Else". 후속 블로그/릴리스 모니터링.

## Candidates
- Simon Willison's Weblog — https://simonwillison.net/ — blog — llm, tools — candidate
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
