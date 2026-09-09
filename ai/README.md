# RAG 설계

현재 단계는 RAG에 투입할 수 있는 출처 포함 JSONL 청크와 키워드 검색입니다. 임베딩, 벡터 저장소, 생성형 답변 API는 후속 작업입니다.

## 데이터 경계

`content/documents/*.md`가 편집 원본입니다. `python scripts/kb.py build`가 절 단위로 `ai/index/chunks.jsonl`을 만듭니다. 큰 절은 문단 경계에서 약 1,500자로 나누되 표나 단일 문단을 자르지 않습니다. 숫자·표·각주를 잘라 의미를 바꾸는 문자 단위 절단은 사용하지 않습니다.

각 청크는 ID, 문서 ID, 제목, 절, 차수, 문서 단계, 출처 URL, 대표 첨부 URL, 해시, 발행일·수집일, 검증 상태, AI 편집 여부를 포함합니다. `data/metadata/relations.json`은 문서 간 명시적 관계를 별도로 제공합니다.

공개 인덱스에서는 draft와 출처 미확인 문서를 제외합니다. 출처 확인만 된 AI 문서는 `source_verified`와 `summary_review_status: unreviewed`를 그대로 전달합니다. `--verified-only` 검색은 사람 검수 완료 문서만 반환합니다. 초기 상태에서는 빈 결과가 정상입니다.

## 다음 단계

1. 공식 원문에서 추출한 텍스트를 별도 저장하고 `content_origin: official_extraction`으로 구분한다. 현재 AI 편집 Markdown을 공식 원문 추출로 표시하지 않는다.
2. 쪽수·표·각주를 유지한 원문 청크와 편집 요약 청크를 각각 임베딩한다.
3. 검색 필터로 plan_number, document_stage, published_date, verification_status를 적용한다.
4. 키워드+벡터 검색 후 문서 관계로 문맥을 확장하고 재순위화한다.
5. 답변에는 원문 URL·쪽수·버전·검수 상태를 제시하고 근거가 없으면 미확인으로 답한다.

현재 키워드 검색은 형태소 분석이나 의미 유사도 검색이 아닙니다. 브라우저 검색은 Quartz 기본 검색을 사용합니다.
