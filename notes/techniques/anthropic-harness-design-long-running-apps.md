---
title: Harness design for long-running application development
date: 2026-04-17
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
source_type: blog
topic: harness
tags: [anthropic, harness, long-running, multi-agent, generator-evaluator, context-anxiety, sprint-contract, sonnet, opus, evaluator-bias, playwright]
status: processed
---

## 요약 (3줄 이내)

Anthropic 엔지니어링 팀이 장시간 실행 애플리케이션(레트로 게임 메이커, DAW) 개발에 사용한 Generator-Evaluator 3-에이전트 하네스를 공개한다. 핵심 발견은 "하네스의 각 컴포넌트는 모델이 혼자 할 수 없는 것에 대한 가정을 인코딩한다"는 것이며, 모델 업그레이드마다 그 가정을 재검증해 불필요한 스캐폴딩을 제거해야 한다는 단순화-우선 원칙을 실증 데이터와 함께 제시한다.

---

## 핵심 포인트

- Generator-Evaluator 2-에이전트 구조(+ Planner)를 GAN에서 차용해 자기평가 편향(self-evaluation bias)을 외부 에이전트로 분리한다.
- Sprint Contract 패턴: Generator와 Evaluator가 구현 전 테스트 가능한 성공 기준을 협상한다 — Sprint 3(Level Editor)에서 27개 기준, 구체적 버그까지 특정.
- Context Anxiety(컨텍스트 불안): Sonnet 4.5에서 컨텍스트 창이 찰수록 조기 종료하는 현상, 인플레이스 compaction 대신 구조화 아티팩트 핸드오프 + 컨텍스트 리셋으로 대응.
- Opus 4.6에서 context anxiety 소멸, sprint 분해 제거 가능 — 같은 스캐폴딩이 모델에 따라 ROI 제로로 전락함을 실증.
- 평가 기준 언어가 생성 방향을 결정: "museum quality" 같은 문구가 예측 불가능한 방식으로 출력을 수렴시킴.
- 에이전트 간 파일 기반 통신(file-based communication)이 깨끗한 상태 핸드오프에 필수적.
- Evaluator 에이전트는 기본 설정으로 표면적 테스트만 수행; 로그를 읽고 프롬프트를 반복 업데이트하는 반복 QA 튜닝이 필요.
- Full 하네스는 Solo 대비 20x 이상 비용(레트로 게임: $9 vs $200, 20분 vs 6시간)이나 품질·기능 완성도에서 압도적 차이.
- 하네스 공간은 모델 개선으로 축소되지 않고 이동한다 — "the interesting work is to keep finding the next novel combination."
- Evaluator는 Playwright MCP로 실제 사용자 인터랙션을 시뮬레이션하고 설계 기준 대비 채점.

---

## 저자의 프레임워크 / 명시적 주장

**3-에이전트 풀스택 코딩 구조**
- Planner: 단순 프롬프트를 상세 제품 스펙으로 확장
- Generator: 스프린트 단위 구현 + 자기평가
- Evaluator: Playwright MCP를 통한 사용자 인터랙션 테스트, 기준 대비 채점

**프론트엔드 채점 4차원** (설계와 독창성에 높은 가중치)
1. Design Quality — 일관성, 무드, 아이덴티티
2. Originality — 커스텀 결정 vs 템플릿 디폴트
3. Craft — 타이포그래피, 간격, 대비, 일관성
4. Functionality — 사용성과 태스크 완성

저자들은 "purple gradients over white cards", "AI slop patterns"을 명시적 감점 대상으로 정의.

**단순화-우선(Simplification-First) 원칙**: 컴포넌트를 하나씩 제거하며 load-bearing 요소를 식별. 복잡성은 필요할 때만 추가.

**하네스 구성 전제의 모델-의존성**: 모든 컴포넌트는 모델 능력에 대한 가정. 신모델 출시마다 가정을 stress-test해 폐기 가능한 스캐폴딩을 제거해야 함.

---

## 구체적 패턴·체크리스트·숫자

| 태스크 | 하네스 유형 | 소요 시간 | 비용 |
|--------|------------|----------|------|
| Retro Game Maker | Solo | 20분 | $9 |
| Retro Game Maker | Full (3-agent) | 6시간 | $200 |
| DAW (Opus 4.6) | Simplified | 3시간 50분 | $124.70 |

- Full 하네스 비용: Solo 대비 **20x 이상**
- Sprint 3 (Level Editor) 성공 기준: **27개** 테스트 가능 항목
- Evaluator가 특정한 버그 예시: rectangle fill tool 배치 오류, delete key handler 로직, FastAPI route matching 순서 (코드 라인 레퍼런스 포함)
- 채점 기준 언어 예: `"the best designs are museum quality"` → 예측 불가 수렴 효과 발생
- Sonnet 4.5: context anxiety 발생 → 컨텍스트 리셋 + 아티팩트 핸드오프 필요
- Opus 4.6: context anxiety 없음 → sprint 분해 제거, evaluator ROI가 edge-case 태스크로 축소

**명시적 권고 체크리스트**:
1. 실제 모델로 현실적 태스크 실험 — 실행 트레이스 직접 읽기
2. 복잡한 태스크 분해 → 각 측면에 전문화 에이전트 적용
3. 신모델 출시마다 하네스 설계 재검토, 낡은 스캐폴딩 제거
4. 에이전트 간 파일 기반 통신으로 깨끗한 상태 핸드오프
5. few-shot 예시 + 상세 점수 분해로 Evaluator 캘리브레이션

---

## 인용 가치 있는 구절

> "Every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing."

> "The space of interesting harness combinations doesn't shrink as models improve. Instead, it moves, and the interesting work for AI engineers is to keep finding the next novel combination."

> "Find the simplest solution possible, and only increase complexity when needed."

> "Out-of-box evaluator agents test superficially; requires multiple feedback loops reading logs and updating prompts to achieve reliable grading."

> "Phrasing like 'the best designs are museum quality' steered outputs in unforeseen ways. Criteria language directly shapes character of generation."

---

## 이식 가능한 원시요소 (transferable primitives)

- P1. **Generator-Evaluator 분리** — 자기평가 편향을 외부 에이전트로 격리하는 2-역할 구조. GAN에서 차용한 설계 원칙. standalone-extractable: **yes**
- P2. **Sprint Contract** — 구현 전 Generator-Evaluator 간 테스트 가능 성공 기준 협상. 구현과 검증의 계약 분리. standalone-extractable: **yes**
- P3. **Context Reset + Artifact Handoff** — in-place compaction 대신 컨텍스트 초기화 후 구조화 파일로 상태 전달. Sonnet 4.5급 모델 대상 실증된 패턴. standalone-extractable: **yes**
- P4. **Simplification-First 컴포넌트 감사** — 새 모델 출시마다 컴포넌트를 하나씩 제거하며 load-bearing 여부 검증. standalone-extractable: **yes**
- P5. **가중 다차원 채점 기준(Weighted Rubric)** — 설계 품질/독창성/장인성/기능성 4차원에 도메인별 가중치. 평가 기준 언어가 생성 품질을 수렴시키는 효과 포함. standalone-extractable: **yes**
- P6. **Playwright MCP Evaluator** — 실제 UI 인터랙션 시뮬레이션으로 기능 테스트를 자동화하는 evaluator 패턴. standalone-extractable: **partial** (Playwright MCP 환경 의존)
- P7. **File-Based Inter-Agent Communication** — 에이전트 간 상태를 파일로 교환해 컨텍스트 격리와 재현성 보장. standalone-extractable: **yes**
- P8. **Evaluator Skepticism Tuning** — 기본값은 lenient; few-shot 예시와 상세 점수 분해로 skeptical 평가자로 캘리브레이션. standalone-extractable: **yes**

---

## 기존 하네스 노트와의 연결

- **ouroboros**: Ouroboros의 `evaluate` 모드도 외부 에이전트 평가를 강제하지만 EventStore/MCP 서버 기반; 이 포스트는 파일 기반 아티팩트 핸드오프를 선택 — 상태 매체의 설계 선택이 다르나 evaluator 분리 원칙은 동일. Sonnet 4.5 context anxiety 해법(리셋)이 Ouroboros의 컨텍스트 격리 전략을 보강.
- **gsd**: GSD가 "context rot → fresh 서브에이전트 컨텍스트"로 해결하는 문제를 이 포스트는 "context anxiety → artifact handoff + reset"로 명명하고 같은 방향에서 접근. P3(Context Reset) primitive는 GSD의 carve-off 개념의 구체 구현 사례.
- **compound-engineering**: Compound Engineering의 Plan→Work→Review→Compound 루프와 이 포스트의 Planner→Generator→Evaluator 3-에이전트가 구조적으로 유사. 차이: Compound는 학습 루프(자기강화)를 강조, 이 포스트는 모델 진화에 따른 하네스 단순화를 강조.
- **ecc**: ECC의 "역할·스킬 생태계 삽입" 접근과 달리 이 포스트는 역할 수를 최소화하며 단순화-우선 원칙을 실증 — 복잡도에 대한 반대 철학적 입장으로 충돌 또는 상보적 긴장.
- **revfactory-harness**: revfactory의 "하네스를 생성하는 하네스" 메타-스킬 접근과 이 포스트의 "모델마다 하네스 재설계" 권고는 방향이 다름 — revfactory는 자동화로 하네스 증식, Anthropic은 각 모델 출시마다 수동 감사로 하네스 축소.
- **superpowers**: Superpowers의 hard-gate TDD 접근과 이 포스트의 Sprint Contract(테스트 가능 기준 협상)가 유사 — 둘 다 실행 전 검증 기준 확정 원칙. 단, Superpowers는 코드 레벨 게이트, 이 포스트는 기능/UX 레벨 채점.

---

## 후속 조사 / 빈틈

- Evaluator의 Playwright MCP 실패율 또는 flakiness에 대한 언급 없음 — 실제 신뢰성 데이터 미공개.
- Sprint Contract의 27개 기준이 어떻게 도출되었는지 프로세스 상세 불명 — 수동 작성인지 Planner가 생성하는지.
- Opus 4.6에서 Evaluator ROI가 "edge-case only"로 축소되었다면, Evaluator 없는 Solo Opus 4.6 vs Full 하네스 Opus 4.6 비용/품질 비교 데이터 필요.
- 게임/DAW 이외 도메인(e.g., 데이터 파이프라인, 백엔드 API)에서 동일 패턴의 적용 가능성 미언급.
- 파일 기반 통신의 파일 포맷(JSON, YAML, Markdown)에 대한 구체적 권고 없음.
- "AI slop patterns" 및 "purple gradients over white cards" 같은 부정적 기준이 도메인별로 어떻게 재정의되어야 하는지 미제시.
