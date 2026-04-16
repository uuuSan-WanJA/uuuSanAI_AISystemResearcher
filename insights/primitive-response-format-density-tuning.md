---
title: ResponseFormat density tuning primitive
date: 2026-04-17
based_on:
  - anthropic-writing-tools-for-agents.md
  - anthropic-code-execution-with-mcp.md
  - anthropic-effective-context-engineering.md
  - compound-engineering.md
  - digests/2026-04-17-anthropic-sweep-vs-community-harnesses.md
confidence: high
tags: [tool-design, token-efficiency, response-format, primitive]
---

## 한 줄 요약

도구 응답은 "정보량 × 토큰 수"가 아니라 **고신호(high-signal) 토큰 밀도**로 설계해야 하며, `ResponseFormat` enum을 통해 호출자가 밀도를 명시적으로 선택할 수 있도록 해야 한다.

---

## 패턴 / 주장

에이전트가 소비하는 도구 응답의 문제는 대부분 "정보 부족"이 아니라 "저신호 토큰 과잉"에서 비롯된다. UUID, MIME type, 중간 연산 결과 같은 데이터는 모델 컨텍스트를 채우지만 실제 추론에 기여하는 신호 밀도는 낮다. Anthropic의 `anthropic-writing-tools-for-agents`는 이 문제를 `ResponseFormat` enum으로 정면 돌파한다. 도구가 `"detailed"` / `"concise"` / `"ids-only"` 등의 포맷 파라미터를 받아들이면, 동일 쿼리에서 호출자가 필요한 밀도를 선택할 수 있다. 결과는 수치로 확인된다. Slack 도구의 경우 `detailed` 응답 206 토큰이 `concise` 모드에서 72 토큰으로 줄었다. 65% 절감이다(다이제스트 B1).

이 원리는 도구 응답에만 국한되지 않는다. `anthropic-code-execution-with-mcp`는 동일 원리를 실행 환경 측으로 밀었다. Google Drive 스프레드시트(10,000행)를 Salesforce로 옮기는 워크플로에서, 개별 tool call 방식은 모든 중간 결과가 컨텍스트를 통과하며 **150,000 토큰**을 소비했다. 실행 환경에서 먼저 필터링하고 최종 결과만 반환하는 코드 실행 방식으로 전환하자 **2,000 토큰**으로 줄었다. 98.7% 절감이다. 두 수치는 방법은 다르지만 같은 원리를 공유한다. **저신호 토큰은 컨텍스트에 도달하기 전에 잘라라.**

`anthropic-effective-context-engineering`은 이 원리의 이론적 배경을 제공한다. 트랜스포머 구조에서 n개의 토큰은 n² 쌍별 관계를 만들어낸다. 컨텍스트가 길어질수록 장거리 추론 정밀도는 점진적으로 저하되는 "context rot"이 발생한다. 이 포스트의 핵심 격언은 "원하는 결과를 최대화하는 최소 고신호 토큰 집합을 찾아라"다. `ResponseFormat` enum은 그 격언을 도구 설계 수준에서 구현한 것이다.

그러나 커뮤니티 하네스는 이 원리를 채택하지 않았다. `compound-engineering.md`는 26개 전문화 에이전트, 14개 병렬 리뷰어, 50개 이상 에이전트를 동시에 구동하는 `/lfg` 파이프라인을 운영하면서도, 개별 도구나 스킬의 토큰 밀도를 측정하거나 공개한 수치가 없다. ECC의 181개 스킬 묶음, Superpowers의 SKILL.md 집합도 마찬가지다. 다이제스트의 B1 항목이 이를 명시한다. "Compound의 14 리뷰 에이전트·ECC의 181 skills 모두 총 토큰 사용량의 툴별 분해가 공개되지 않음. gap: 미측정."

에이전트가 사용하는 도구의 수가 많아질수록 이 공백의 비용은 선형 이상으로 커진다.

---

## 근거가 되는 관찰

- **Slack 206→72 토큰 (65% 절감)** — `anthropic-writing-tools-for-agents`: `ResponseFormat` enum의 `detailed`/`concise` 전환 효과. 동일 도구, 동일 쿼리, 포맷 선택만 다름.
- **MCP exec 150K→2K 토큰 (98.7% 절감)** — `anthropic-code-execution-with-mcp`: 필터링을 실행 환경(sandbox)으로 이전했을 때의 효과. "filter-at-source" 원리의 가장 극단적 수치.
- **Context rot 이론** — `anthropic-effective-context-engineering`: n² 관계 비용, 고신호 토큰 최소화가 단순 최적화가 아니라 추론 정밀도 유지의 구조적 조건.
- **커뮤니티 빈틈** — `compound-engineering.md`의 26개 에이전트 + 다수 도구 운영에도 불구하고 density 비교 수치 전무. 다이제스트 B1·C4 항목이 9/9 커뮤니티 하네스 전체의 미측정 상태를 확인.

---

## 구성 요소 (이식 가능한 단위)

1. **ResponseFormat enum** — 도구 파라미터에 `format: "concise" | "detailed" | "ids-only"` 등을 추가하고, 각 포맷별로 반환 필드를 명확히 정의한다. 호출자가 컨텍스트 예산에 따라 포맷을 선택할 수 있다. `anthropic-writing-tools-for-agents`의 P1 원시요소.

2. **Truncation & pagination 기본값** — 응답에 기본 상한을 설정한다. Anthropic의 Claude Code 기본값은 응답당 25,000 토큰이다. 대용량 데이터를 반환하는 도구에는 `cursor` 기반 pagination을 내장해 한 번에 컨텍스트를 채우는 것을 방지한다.

3. **토큰 밀도 벤치마크** — 동일 쿼리에 `concise`/`detailed` 두 포맷을 교차 실행해 토큰 수와 태스크 완료율을 동시에 기록한다. 최소 기준: 포맷 별 토큰 수, 에이전트 재호출 빈도, 최종 태스크 완료 여부.

4. **Filter-at-source** — 대용량 데이터(스프레드시트, 로그, 검색 결과)를 도구 응답으로 그대로 올리지 않는다. 실행 환경(sandbox, exec side)에서 필터링 후 결과만 반환한다. `anthropic-code-execution-with-mcp`의 P2 원시요소.

---

## 반례 또는 한계

- **concise 모드가 필수 정보를 누락할 경우**, 에이전트가 동일 도구를 재호출하거나 보완 도구를 추가로 호출하게 된다. 재호출 비용이 절감 효과를 상쇄하거나 역전시킬 수 있다. 이를 확인하려면 단순 토큰 수가 아니라 **태스크당 총 토큰 비용(재호출 포함)**을 측정해야 한다.

- **밀도 튜닝의 과적합** — 특정 모델 버전의 컨텍스트 윈도우 크기나 attention 특성에 최적화된 포맷이 모델 업그레이드 후 회귀(regression)를 일으킬 수 있다. `anthropic-effective-context-engineering`이 경고한 "smarter models require less prescriptive engineering" 원칙과 직접 연결된다.

---

## 전제 / 선행 조건

- **도구 소유권**: description과 return shape를 수정할 수 있어야 한다. 외부 MCP 서버나 써드파티 API를 그대로 쓰는 경우 포맷 제어가 불가능하다.
- **토큰 카운트 로깅**: 도구별, 포맷별 토큰 수를 로그로 남겨야 벤치마크와 회귀 감지가 가능하다. `anthropic-writing-tools-for-agents`의 5대 평가 지표(top-level accuracy, runtime, total call count, token consumption, error rate) 중 token consumption이 전제다.
- **최소 2개 호출 시나리오**: 단일 도구·단일 포맷에서는 밀도 비교 실험 자체가 불가능하다. 동일 쿼리를 두 포맷으로 돌려야 baseline이 생긴다.

---

## 적용 난이도

**낮음 (단일 도구 수정 기준)**.
ResponseFormat enum 추가는 도구 description과 반환 로직을 수정하는 것으로, 외부 의존성 없이 독립적으로 적용 가능하다. filter-at-source 패턴은 실행 환경(sandbox) 설계를 요구하므로 중간 난이도다.

---

## 내 프로젝트에 적용한다면 (Phase 2 후보)

가장 먼저 적용할 대상은 **응답이 긴 도구 상위 3개를 식별하고 concise 포맷을 추가하는 것**이다. 구체적으로:

1. 현재 사용 중인 도구 응답의 토큰 수를 로깅해 상위 3개를 식별한다.
2. 해당 도구에 `format` 파라미터를 추가하고 `concise` 모드의 반환 필드를 정의한다.
3. 동일 쿼리에 `detailed`/`concise`를 교차 실행해 토큰 수 및 태스크 완료율을 기록한다.
4. concise 모드에서 재호출이 유발되는 케이스를 기록해 필수 필드 목록을 보정한다.

이 4단계는 `compound-engineering.md`가 구현하지 않은 "툴별 토큰 밀도 측정"의 최소 실행 단위이며, 다이제스트 E4 권고(ResponseFormat enum 도입 + 응답 25K cap + concise/detailed 분기 벤치마크)와 직접 대응한다.

---

## 관련 primitive 카드

- `primitive-tool-description-engineering` (예정) — 도구 description을 신입 온보딩 문서처럼 작성하는 원칙. ResponseFormat enum은 description 설계의 하위 구성요소.
- `primitive-filter-at-source` (예정) — 실행 환경에서 데이터를 미리 자르는 패턴. 98.7% 절감 수치의 직접 구현.
- `primitive-context-rot-prevention` (예정) — n² 관계 비용과 just-in-time 컨텍스트 로딩 패턴.
