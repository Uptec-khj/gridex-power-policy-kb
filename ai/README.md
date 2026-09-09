# RAG 설계

현재는 AI 편집 Markdown 검색과 공식 PDF 원문 페이지 검색을 제공합니다. 임베딩·벡터 저장소·생성형 답변 API는 후속 단계입니다. 개발 순서는 [로드맵](https://github.com/Uptec-khj/gridex-project-management/blob/main/content/roadmap.md)에 있습니다.

## 데이터 경계

| 산출물 | 원본 | 성격 |
| --- | --- | --- |
| `ai/index/chunks.jsonl` | `content/documents/*.md` | `ai_assisted_editorial` — AI 편집 요약 |
| `ai/index/official-pages.jsonl` | 해시로 보존한 공식 PDF | `official_extraction` — 페이지 단위 자동 추출 |
| `data/metadata/extraction-report.json` | 추출 처리 결과 | PDF 미확보·실패·빈 페이지·텍스트 적은 페이지 |
| `data/metadata/relations.json` | 문서의 Wiki Link 관계 | 문서 간 관련·이전·다음 관계 |

공식 출처 확인과 추출 품질 검수는 다릅니다. 원문 청크에도 `extraction_review_status: unreviewed`를 유지하며, AI가 쓴 편집 문장을 공식 원문 추출로 표시하지 않습니다. `human_verified`인 요약이 있어도 그 PDF 추출의 표 구조 검수가 자동 완료되는 것은 아닙니다.

## 추출과 검색

```sh
python scripts/kb.py build
python scripts/originals.py build
python scripts/originals.py search "송변전 61183" --plan 11 --stage final
```

PDF를 읽기 전에 실제 바이트의 SHA-256을 대조합니다. 물리적 페이지를 쪼개거나 인접 페이지와 합치지 않고 원본 URL·첨부 URL·파일 해시·추출 엔진·차수·단계·발행일을 기록합니다. 원본 파일 해시와 페이지 번호가 청크 ID에 들어갑니다. `printed_page`는 확인하지 않은 값을 추정하지 않고 null입니다.

텍스트 추출에는 설치 버전이 고정된 pypdf의 layout 모드를 사용합니다. 표를 구조화된 셀 데이터로 변환한 것은 아니며 이미지 글자는 추출하지 못할 수 있습니다. 제목만 추출된 포스터도 있습니다. [pypdf 공식 문서](https://pypdf.readthedocs.io/en/stable/user/extract-text.html)의 PDF 구조·OCR 한계를 참고합니다. 원문 표·각주 대조가 필요합니다.

빈 텍스트는 검색에서 제외하되 처리 현황에는 남깁니다. 공백 제외 80자 미만인 페이지는 시각 검토 후보로 표시하며, 이 기준만으로 스캔 문서나 OCR 필요를 확정하지 않습니다. 파싱 실패는 보고서에 기록하고 빌드가 실패하도록 합니다. 초안·출처 미확인 문서는 원문 공개 인덱스에서도 제외합니다.

여러 검색어는 모두 제목 또는 페이지 본문에 있어야 합니다. 한국어 띄어쓰기와 숫자 쉼표 차이를 정규화하고 차수·단계 필터를 적용합니다. 공개 사이트는 같은 원문 인덱스를 브라우저에서 검색하며 쿼리를 외부 서비스에 전송하지 않습니다. 인쇄 쪽수와 PDF 물리적 쪽수를 혼용하지 않습니다.

기존 `kb.py search --verified-only`는 사람 검수 완료된 편집 문서만 반환합니다. 원문 페이지는 아직 추출 검수 완료 상태를 제공하지 않습니다.

## 다음 단계

1. 표·수치·각주 검수 기록과 발표 당시 원문 버전 연결.
2. 실제 질문·기대 출처·근거 없음 질문으로 검색 평가 세트 구축.
3. 키워드 검색 누락을 측정한 뒤 벡터 검색과 관계 확장 검토.
4. 답변에는 출처·쪽수·버전·검수 상태를 표시하고 근거가 부족하면 미확인으로 답하도록 구현.

현재 페이지 단위 기록은 긴 표를 중간에 자르지 않기 위한 선택입니다. 페이지에 이미지가 있거나 매우 긴 경우는 별도 검토 후 OCR·표 구조화·청크 전략을 확장합니다.

## 기술 문서와 관계 (v0.4)

기술 문서는 plan_family와 plan_number가 null이다. category와 technical 객체의 document_type, standard_id, revision, revised_date, effective_date, applicability, coverage를 편집 청크와 PDF 페이지 색인에 함께 보존한다. null을 임의 차수나 현행 버전으로 바꾸지 않는다. rule_draft와 document_stage=draft는 공개된 공식 개정안이며, 게시 제외용 draft=true와 구분한다.

relations.json의 근거 있는 관계에는 source_url, basis, interpretation_review_status가 있다. 관계 자체도 편집 판단이므로 공식 규정의 명시적 연결인지 KB의 주제 연결인지 basis를 읽는다. 현재 두 가지 사례를 추가했고 기존 일반 관계는 유지한다. technical.effective_date=null인 예정안에서 시행일을 추정하거나 부록 coverage를 전문으로 확장해 답하지 않는다.

## 종합 에너지·재생에너지 계획 (v0.5)

plan_family를 필터에 포함해야 같은 차수의 다른 계획이 혼합되지 않는다. 예: `python scripts/originals.py search "100GW" --family 재생에너지기본계획 --plan 1`. 기술 문서는 기존대로 두 계획 필드가 null이다. 과거 계획 목표, 최신 계획 목표, 지방정부 별첨 계획(안)은 서로 다른 시점·범위의 근거로 취급한다. 문서 단계 final만으로 부록의 모든 숫자까지 확정 수치라고 추론하지 않는다.
