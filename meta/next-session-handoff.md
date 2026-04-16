---
date_recorded: 2026-04-17
author_session: Anthropic sweep + digest + 5 insight cards
phase: Phase 1 마무리 단계 — Phase 2 진입 대기
---

# 다음 세션 이어서 하기 — 핸드오프 메모

## 오늘(2026-04-17) 진행 완료
1. **Anthropic Engineering 블로그 전면 스윕** (10개 포스트 → `notes/techniques/anthropic-*.md`)
   - harness-design-long-running-apps / effective-harnesses-long-running-agents / effective-context-engineering / building-effective-agents / writing-tools-for-agents / multi-agent-research-system / demystifying-evals / code-execution-with-mcp / managed-agents / building-c-compiler
2. **`sources.md` 업데이트** — Anthropic Engineering Blog를 `active` 로 승격
3. **Comparison digest 작성** — `digests/2026-04-17-anthropic-sweep-vs-community-harnesses.md`
   - Anthropic 7패턴 × 커뮤니티 9 하네스 커버리지 매트릭스
   - 수치·규칙 10행 대조표 (B section)
   - 5개 빈틈 (C section)
   - 4개 교차강화 포인트 (D section)
   - 가장 놀라운 발견: **Superpowers v5.0.6의 inline review 롤백이 Anthropic의 "멀티에이전트 ~15× 토큰 비용" 경고를 출판 이후 독립 확증**
4. **5개 Phase-1 primitive insight 카드 작성** (`insights/primitive-*.md`)
   - `primitive-regression-eval-lifecycle.md` (Capability vs Regression 분리 + grader 신뢰성)
   - `primitive-vault-proxy-credential-isolation.md` (Brain/Hands 분리, Vault+Proxy vs Bundled Auth)
   - `primitive-numerical-gate-thresholds.md` (Boolean / 수치 / Evidence-artifact 3종 게이트)
   - `primitive-response-format-density-tuning.md` (concise 모드의 재호출 역전 위험)
   - `primitive-evaluator-optimizer-diffusion.md` (Full/Inline/Rule-based 결정 트리)

## 3단계 남은 일 — Phase 2 진입

### 다음 세션 첫 질문 (사용자에게 확인해야 함)
Phase 2 graft-evaluator 를 어느 프로젝트에 대해 돌릴지:
- **A. gamemaker** — 이미 `insights/project_map_gamemaker_post_rebuttal.md` 와 `insights/report_gamemaker_improvements_post_rebuttal.md` 가 존재. 5개 primitive 카드 × gamemaker 조합으로 graft-evaluator 바로 투입 가능.
- **B. 다른 사용자 프로젝트** — project-analyzer로 map 먼저 생성 필요.
- **C. 여러 프로젝트 동시** — 카드 5 × 프로젝트 N 매트릭스.

### 즉시 실행 가능한 최우선 작업 (A 경로 가정)
`graft-evaluator` 호출 입력:
- 하네스 노트 (5개 primitive insight 중 우선순위 높은 것부터)
- 프로젝트 맵: `insights/project_map_gamemaker_post_rebuttal.md`
- 권장 우선순위: (1) regression-eval-lifecycle → (2) evaluator-optimizer-diffusion → (3) numerical-gate-thresholds → (4) response-format-density-tuning → (5) vault-proxy-credential-isolation
- 이유: 1번과 2번은 강하게 엮임(grader 검증 없는 Evaluator는 false confidence 증폭기). 함께 이식 고려.

## 덜 급한 보조 작업
- **Digest 본문 사용자 독서** — 사용자가 아직 digest 본문 미독. Phase 2 전에 읽으면 결정 정확도 상승.
- **Insight 카드 상호 연결 보강** — 카드 5개에 "관련 primitive 카드" 섹션이 있으나 실제 교차 링크는 반쪽. 필요 시 10분 짜리 정리.
- **Anthropic 블로그 미커버 포스트 (5편)** — "Claude Code auto mode", "Quantifying infrastructure noise in agentic coding evals", "the think tool", "Beyond permission prompts", "Introducing advanced tool use on the Claude Developer Platform". 제품·보안 맥락이라 Phase 1 뒷순위로 미뤘음. 필요하면 추후 증분 스윕.
- **Anthropic 블로그 신규 포스트 증분 모니터링** — 주기적으로 새 포스트 확인 (구체 자동화는 미설정).

## 현재 시점의 corpus 현황 (2026-04-17 기준)
- `notes/harness/`: 9개 커뮤니티 하네스 deep-dive (기존) + `_collected_facts_2026-04-13.md` 보조
- `notes/techniques/`: 10개 Anthropic 기술 노트 (오늘 신규)
- `notes/agents/`, `notes/llm/`: 아직 비어있음
- `digests/`: 1개 (오늘 신규)
- `insights/`: 5개 primitive 카드 (오늘 신규) + 2개 gamemaker 관련 기존

## 재진입 시 빠른 오리엔테이션 순서
1. 이 파일 읽기
2. `digests/2026-04-17-anthropic-sweep-vs-community-harnesses.md` 훑기 (특히 TL;DR + E섹션 "다음 단계 권고")
3. 5개 `insights/primitive-*.md` 각 카드 "한 줄 요약" 만 훑기
4. 사용자에게 위 "다음 세션 첫 질문" 제시
