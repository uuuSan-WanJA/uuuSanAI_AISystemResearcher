---
title: Graphify upstream identification
date: 2026-04-21
type: inbox / probe-report
status: captured
---

## 판정

- 분기: **A** (third-party 오픈소스 upstream 확정)
- 요약: 사용자의 `~/.claude/skills/graphify/` 는 `safishamsi/graphify` (MIT, PyPI 패키지 `graphifyy` v0.4.23) 의 현지 설치 사본이며, frontmatter 의 `-windows` 는 별도 포크가 아니라 공식 레포가 지원하는 플랫폼 설치 변형 표식.

## 로컬 파일 증거

- `~/.claude/skills/graphify/` 파일 2개:
  - `SKILL.md` (51 KB, 1245줄) — 파이프라인 전체 명세
  - `.graphify_version` — 내용: `0.4.23`
- `SKILL.md` frontmatter: `name: graphify-windows`, `trigger: /graphify`
- 설치 라인 (Step 1): `pip install graphifyy -q` — PyPI 패키지 `graphifyy` (y 2개) 사용
- 스폰서 라인 (Step 9 말미): `https://github.com/sponsors/safishamsi` — 저자 attribution
- Python 모듈 임포트: `graphify.detect`, `graphify.extract`, `graphify.cluster`, `graphify.build`, `graphify.export`, `graphify.serve` 등 — 동일 레포 모듈 트리
- 트러블슈팅 섹션: `pip install --upgrade graphifyy` 재확인

## 웹 조사 결과

- WebSearch 2회로 upstream 즉시 확정:
  - `github.com/safishamsi/graphify` — "AI coding assistant skill" 단일 레포, 여러 에이전트 하네스(Claude Code, Codex, Cursor, Aider, Gemini CLI, Copilot CLI, OpenClaw 등) 공용
  - `pypi.org/project/graphifyy/` — 동일 upstream 의 PyPI 배포 (CLI 이름은 `graphify`, 패키지명만 `graphifyy`)
- `graphify install --platform windows` 플래그 존재 → `-windows` suffix 는 설치 시 자동 감지된 플랫폼 변형 이름이며 별도 포크 아님

## Upstream

- 레포 URL: https://github.com/safishamsi/graphify
- 저자/조직: `safishamsi` (GitHub 개인 계정). PyPI 업로더는 `captainturbo` 로 표기 — 동일 저자의 PyPI 계정으로 추정
- 라이선스: MIT
- 첫 릴리스: **v0.1.1 / 2026-04-04** (PyPI) — 2026-04-21 기준 17일 전
- 최신 릴리스: v0.4.23 / 2026-04-18 (PyPI) — 로컬 설치본과 버전 일치
- 스타/포크: 약 31.4k stars / 3.5k forks (레포 페이지 스냅샷) — 초기 릴리스 17일 만의 수치로 매우 이례적, Brian/Brain Trinity 영상에서 언급된 "카파시 LLM Wiki 트윗 48h 이내" 서사와 정합
- `graphify-windows` 와의 관계: **별개 포크 아님**. 단일 upstream 이 설치 시 플랫폼을 감지해 skill frontmatter name 을 `graphify-<platform>` 형태로 기록. 로컬본은 upstream 의 Windows 설치 경로를 통한 사본.

## Deep-dive 권고

**yes** — 하네스 엔지니어링 관점에서 가치 높음:
1. 하네스(Claude Code, Codex, Cursor, OpenClaw 등) 여러 개를 **동일 PyPI 패키지 + 하네스별 skill 어댑터** 로 커버하는 전략은 리서치 프로젝트가 이미 deep-dive 한 OpenClaw/Hermes/Kilo Code 와 직접 대조 가능
2. `confidence=EXTRACTED/INFERRED/AMBIGUOUS` 3-tier tagging, Leiden 커뮤니티, Tree-sitter + LLM 듀얼 패스, `god_nodes` / `surprising_connections` 분석 — 사용자의 리서치 코퍼스 자체(Graph-RAG / Memory PKM survey notes) 에 바로 적용할 수 있는 툴
3. 17일 만에 31.4k stars + 다수 하네스 지원 — 에이전트 생태계의 "skill 포맷 표준화" 가속 사례로 기록 가치

## 미답 / 열린 질문

- 첫 git commit 날짜(레포 최초 커밋) 정확한 확인 — `gh` CLI 부재로 PyPI 첫 릴리스 2026-04-04 만 확인됨. 필요 시 GitHub API 직접 호출
- `captainturbo` PyPI 계정과 `safishamsi` GitHub 핸들 동일인 확정 증거 (일반적 패턴이지만 문서적 연결 고리 미확인)
- Brian/Brain Trinity 2026-04-21 영상에서 주장한 "Karpathy LLM Wiki 트윗 48h 이내 제작" 의 실제 원 트윗 URL 및 날짜 — PyPI 첫 릴리스(04-04) 와 역산 대조해 신빙성 검증 필요
- 하네스별 skill 어댑터 (Claude Code vs Codex vs OpenClaw) 가 upstream 레포 안에 어떤 디렉터리 구조로 공존하는지 — deep-dive 진입 시 첫 탐색 포인트
- Penpax 엔터프라이즈 레이어와의 관계 및 상용화 모델
