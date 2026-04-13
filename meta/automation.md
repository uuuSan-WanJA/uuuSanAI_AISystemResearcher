# Automation Plan

수집·요약 작업을 주기 실행으로 옮기기 위한 계획. Phase 1 수동 리서치에서 패턴이 잡힌 뒤에 구체화.

## 후보 자동화

### 1. 주간 하네스/에이전트 소식 수집
- **트리거**: `/schedule` 또는 `/loop` (weekly)
- **입력**: `sources.md` 의 active 소스
- **동작**: WebSearch/WebFetch 로 최근 7일치 새 글 수집 → `inbox/` 에 raw 캡처
- **상태**: not implemented

### 2. inbox → notes 승격
- **트리거**: 수동 (`/loop` 로 자주 리마인드)
- **동작**: inbox 항목을 읽고 템플릿에 맞게 가공
- **상태**: not implemented

### 3. 월간 다이제스트
- **트리거**: 월초
- **동작**: 해당 월 `notes/` 전수 스캔 → `digests/YYYY-MM.md` 생성
- **상태**: not implemented

## 노트
- 자동화는 Phase 1 수동 수집으로 "어떤 소스가 실제로 유용한지" 가 드러난 뒤 구현
- 자동화 코드 자체도 하네스 엔지니어링의 실습 대상으로 삼을 것
