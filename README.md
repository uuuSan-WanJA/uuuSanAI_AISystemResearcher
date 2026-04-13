# uuuSanAI — AI System Researcher

AI 에이전트 시스템 관련 최신 정보를 수집·분석·종합하는 개인 리서치 프로젝트.

## 목적
1. 최신 LLM / 에이전트 시스템 동향 추적
2. 하네스 엔지니어링 기법·프리셋 수집 및 인사이트 축적
3. 주목할 만한 AI 에이전트 시스템·프로덕트 정리

## 디렉토리 구조

```
inbox/        — 가공되지 않은 원본 캡처, 링크, 짧은 메모. 여기가 진입점.
notes/        — 가공된 리서치 노트 (주제 폴더로 분기)
  harness/      하네스 엔지니어링 기법, 프리셋, 프롬프트 패턴
  llm/          LLM 릴리즈, 모델 능력 업데이트
  agents/       에이전트 프레임워크, 프로덕트, 시스템 아키텍처
  techniques/   위 셋 어디에도 딱 안 맞는 기법 (메모리, 툴 설계, RAG 등)
insights/     — 여러 노트를 가로질러 내가 뽑아낸 패턴·종합·비평
digests/      — 주기 요약 (weekly / monthly rollup)
sources.md    — 모니터링할 소스 레지스트리 (블로그, 레포, 뉴스레터, 트위터 계정 등)
templates/    — 노트·다이제스트 템플릿
meta/         — 프로젝트 워크플로, 자동화 계획, 스케줄 설정 등
```

## 워크플로

1. **Capture**: 발견한 것 → `inbox/YYYY-MM-DD-slug.md` 에 링크+한줄 메모로 즉시 저장
2. **Process**: inbox 항목을 읽고 가공 → 적절한 `notes/<주제>/` 로 이동/승격
3. **Synthesize**: 주기적으로 `insights/` 에 종합 노트 작성
4. **Digest**: 주/월 단위로 `digests/` 에 요약
5. **Automate**: 패턴이 잡히면 `/schedule` 또는 `/loop` 으로 수집 자동화 (meta/automation.md)

## 현재 상태
- Phase 0: 구조 셋업 ✅
- Phase 1 (진행 예정): 하네스 엔지니어링 웹 리서치 — 편향 없이 외부 기법부터 먼저 수집
