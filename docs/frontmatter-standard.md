# GRIDEX Frontmatter 표준 v1.1

공식 자료는 `content/documents/<id>.md`에 UTF-8 YAML Frontmatter와 Markdown 본문으로 저장한다. 기계 검증 규칙은 `schemas/policy-document.schema.json`이다. 허브·Timeline은 탐색 문서로서 공식 자료 수에 포함하지 않는다.

| 필드 | 형식 | 규칙 |
| --- | --- | --- |
| title | 문자열 | 원문 식별에 충실한 제목. 편집 제목은 기본정보에 명시 |
| organization | 문자열 | 발행 당시 기관명. 현재 호스팅 기관명으로 소급 변경 금지 |
| published_date | 날짜 문자열 또는 null | 따옴표로 감싼 YYYY-MM-DD. 미상은 null, 수집일·월초로 추정 금지 |
| category | 열거형 | 전력수급계획 / 전력수요 / 송변전망 / 기술기준 / 성능평가 / 에너지정책 / 재생에너지정책 / 전력시장 |
| subcategory | 문자열 | 기본계획 / 확정발표 / 수정공고 / 장기전력수요전망 / 수립착수 / 정책토론회안내 / 기관해설 등 |
| plan_family | 열거형 또는 null | 전력수급기본계획 / 장기송변전설비계획 / 에너지기본계획 / 신재생에너지기본계획 / 재생에너지기본계획. 기술 문서는 null |
| plan_number | 정수 또는 null | 계획 계열별 허용 차수는 아래 표 참조. 기술 문서는 null |
| document_stage | 열거형 | 아래 단계 표 참조 |
| topics | 문자열 목록 | 통제 키워드. 빈 목록 금지 |
| source_url | HTTPS URL | 공식 게시물·자료실 URL. 검색결과 URL 금지 |
| attachment_url | HTTPS URL 또는 null | 실제 수집한 대표 첨부. 다운로드 실패 시 null |
| related_documents | Wiki Link 목록 | 예: ['[[p11-final]]', '[[p11-amend]]']. YAML 문자열로 따옴표 필수 |
| previous_document | Wiki Link 또는 null | 선택한 절차·버전 순서의 직전 문서. 역참조 필수 |
| next_document | Wiki Link 또는 null | 선택한 절차·버전 순서의 다음 문서. 역참조 필수 |
| collected_date | 날짜 문자열 | 콘텐츠에 사용한 실제 수집 날짜. 발행일과 구분 |
| file_hash | 문자열 또는 null | 대표 첨부의 sha256:64자리 소문자 hex. 미수집은 null |
| verification_status | 열거형 | unverified / source_verified / needs_review / human_verified |

## 확장 필드

- `id`: 안정적인 ASCII 식별자이며 파일명과 동일. 제목 변경으로 ID를 바꾸지 않는다.
- `schema_version`: 새 문서는 문자열 '1.1'. 기존 '1.0'은 국내 계획 규칙으로 계속 검증한다. `source_id`: Source Registry 키.
- `attachments`: 첨부별 URL·제목·보존 경로·해시·형식·크기·수집 시각·권리 확인 상태.
- `source_snapshot`: 게시물 HTML의 보존 경로와 SHA-256. 대표 첨부 해시와 분리.
- `ai_generated`: AI 작성·편집 포함 여부. `summary_review_status`: unreviewed / reviewed.
- `reviewed_by`, `reviewed_date`: 사람이 검수한 경우 GitHub ID 등과 날짜. 자동 채우기 금지.
- `events`: 날짜·사건명·publication/scheduled/confirmed·근거 URL. 보도일과 행사일을 분리.
- `draft`: true이면 Quartz 및 공개 RAG 인덱스에서 제외.
- `tags`, `aliases`: Obsidian·Quartz 탐색용. `date`는 확인된 published_date의 Quartz 표시용 복제값으로 null 허용.
- `last_verified_date`, `verification_notes`: 확인 범위와 한계.

확장 시 스키마를 함께 갱신한다. 예약되지 않은 필드는 CI에서 거부한다.

## 국제 문서 필수 필드 (v1.1)

기존 17개 필드와 10개 본문 절을 유지한다. 분류 사전은 `schemas/international-taxonomy.json`이며 새 관할·계열을 추가할 때 JSON Schema의 조합 규칙과 함께 갱신한다. 국가 허브·문서 찾기·PDF 검색·편집 RAG와 원문 색인에 같은 필드를 전달한다.

| 필드 | 규칙 |
| --- | --- |
| region_group | KR / AU / US / CN / Europe. 국가·지역 메뉴를 위한 그룹 |
| jurisdictions | 관할 ID 목록. KR, AU, AU-WA, US, US-CA, US-TX, CN, EU, PAN-EUROPE, GB, DE, FR 중 그룹과 일치하는 값. 비어 있으면 안 됨 |
| market_regions | NEM / WEM / CAISO / PJM / ERCOT의 확인된 적용 시장. 미확인·비해당은 빈 목록 |
| document_language | 현재 지원하는 원어 코드 ko / en / zh-Hans / de / fr. 한국어 요약을 썼다고 원어를 ko로 변경하지 않음 |
| document_type | plan / forecast / transmission_plan / technical_standard / test_procedure / technical_notice / rule_draft / regulation / guide / study / notice / press_release / official_explainer |
| title_original | 원문과 대조한 원어 제목. 기존 국내 문서 이관 시 미대조는 null. 해외 신규 문서는 원어 제목 필수 |
| title_ko | 한국어 표시 제목 또는 null. 비공식 번역이면 본문에 AI 번역임을 표시 |
| document_identifier | 명령·법령·기준의 식별번호 또는 null |
| edition_year | 확인된 연도판 연도 또는 null. 발행연도를 자동 복사하지 않음 |
| version | 확인된 판본 표기 또는 null |

EU와 PAN-EUROPE는 국가코드가 아니다. 사전에서 각각 초국가 관할·범유럽 계통 범위로 구분하고 `country_code: null`로 둔다. 복수 관할 문서는 한 번 저장하고 해당 관할 필터마다 검색되게 한다. 국가 분류는 법률 적용에 대한 검수 완료를 뜻하지 않는다. 실제 적용 전압·설비·지역과 근거는 본문 및 기술문서의 `technical.applicability`에 적는다.

NEM은 AU, WEM은 AU-WA, 미국 시장은 US 관할과 함께 사용해야 한다. 미확인 시장을 국가명에서 추정하지 않는다. 기존 국내 37건은 KR·ko로 이관했으며 세부 시장을 추정하지 않아 `market_regions: []`로 유지한다.

기존 KB의 편집 제목은 `title`과 `title_ko`로 유지하고, 공식 게시물 제목과의 일치 대조 전에는 `title_original: null`로 둔다. 본문·원본·문서 관계는 바꾸지 않는다.

국외 계획 계열은 `integrated-system-plan`(AU), `national-transmission-needs-study`·`national-transmission-planning-study`(US), `tyndp`(Europe), `cn-energy-system-plan`(CN)을 예약했다. 아직 문서 수집을 뜻하지 않는다. 연도판 계열의 `plan_number`는 null이고 `edition_year`를 사용한다. 중국 계열은 확인한 14·15차 또는 null을 허용한다. 국외 규정·가이드·연구는 계열이 없으면 `plan_family`와 `plan_number`를 모두 null로 둔다. 국내 계획 계열·차수 제약은 기존과 같다.

`category`에 전력시장을 추가했다. 기술기준·성능평가 분류에서는 `technical`이 필수이며 최상위 `document_type`과 `technical.document_type`이 일치해야 한다. 차수가 null이라는 이유만으로 기술 문서로 분류하지 않는다.

자동 추정하지 않는 후속 항목: 비기술 문서의 별도 채택·시행·폐지 상태, 법적 효력, 번역 검수, 국제 원문 재배포 권리의 상세 스키마. 해외 자료를 공개 수집하는 G2 이전에 실제 문서·이용조건을 확인해 보강한다. 이 단계는 국가 탐색과 분류 기반이며 이 필드들에 대한 법적 검증을 구현한 것은 아니다.

## 문서 단계와 검수 상태

| 값 | 의미 |
| --- | --- |
| announced | 수립 착수 등 추진 발표 |
| working_draft | 실무안 또는 그 공개자료 |
| draft | 정부안·초안 |
| consultation | 공청회·토론회·의견수렴 |
| final | 최종 공고·확정 계획 |
| amended | 수정 공고·개정본 |
| press_release | 확정 등을 설명하는 보도자료 |
| supporting | 장기 수요 표 등 지원자료 |
| official_explainer | 기관 사보 등 해설. 계획 전문이 아님 |

문서의 공식 단계와 KB 검수 상태는 별개다. 확정 계획이라도 AI 요약은 검수 전일 수 있다.

## 검증 상태

`unverified`: 후보만 발견. `source_verified`: 공식 게시물의 존재·제목·발행 정보와 확보한 첨부를 확인했으나 AI 요약에 대한 사람의 검수는 미완료. `needs_review`: 내용 충돌·확인 실패로 재검수 필요. `human_verified`: 사람이 출처·본문·수치·단위·버전을 대조하고 검수자와 날짜를 기입.

공개 허용은 source_verified 또는 human_verified이고 draft가 false인 문서다. 출처만 확인된 문서는 사이트에서 반드시 ‘AI 요약 · 검수 대기’를 표시한다. 엄격한 RAG 소비자는 human_verified만 필터링한다.

## 관계와 버전

Wiki Link 대상은 유일한 파일 ID다. 본문은 `[[p11-amend|제11차 수정 공고]]`처럼 표시명을 붙인다. Frontmatter만으로 Quartz 그래프가 생기지 않으므로 동일 관계를 본문에도 적는다. ID 충돌·깨진 링크·비대칭 이전/다음 관계는 검증 실패다. 차수 비교는 related_documents로 연결하고 동일 절차의 순차 관계와 구분한다.

URL이 같아도 바이트가 달라지면 다른 파일이다. 새 SHA-256 경로와 이전 수집 기록을 보존한다. 동일 해시는 저장공간을 공유하되 문서의 법적 동일성을 자동 판정하지 않는다.

## 수치와 근거

각 행에 지표·연도·값·단위·전국/지역·판매단/발전단·기준/목표수요·원문 쪽수/표명을 가능한 한 기록한다. PDF 쪽수는 파일의 1-based 페이지 번호이며 인쇄 쪽수가 다르면 병기한다. AI 계산은 공식 수치와 분리하고 입력 출처와 계산식을 적는다. 미확인 값을 0이나 추정값으로 채우지 않는다.

## 기술 문서 확장 (v0.4, schema_version 1.0의 호환 확장)

`category`가 기술기준 또는 성능평가이면 `plan_family`와 `plan_number`는 모두 null이고 `technical` 객체를 필수로 입력한다. 계획 문서는 기존 차수 규칙을 유지한다. 템플릿은 `templates/technical-document.md`이다.

- `document_type`: technical_standard / test_procedure / technical_notice / rule_draft. 유형과 공식 단계(document_stage)는 별개다.
- `standard_id`, `revision`: 기준번호·개정번호 문자열 또는 null. 개정 04의 앞자리 0을 유지한다.
- `revised_date`, `effective_date`: 확인된 YYYY-MM-DD 또는 null. 게시일은 published_date에 보존한다. 예정월·미정일을 임의의 날짜로 변환하지 않는다.
- `applicability`: 대상 사업자·전압·설비·시험 범위. 일반적인 법적 적용 판정을 AI로 확정하지 않는다.
- `coverage`: 전문 / 부록 / 발췌 / 안내 / 개정안과 확보 쪽수. 부록을 전체 기준으로 표시하지 않는다.

## 근거 있는 관계 유형

선택 필드 `typed_relations`는 target(Wiki Link), type, source_url, basis를 갖는다. type은 amends(개정), implements(이행), explains(설명), uses_evidence(근거 사용), references(참조)다. 공식 근거 URL과 연결 판단의 설명을 함께 기록한다. 동일 target을 related_documents와 본문 Wiki Link에도 기록한다. 페이지 그래프는 기존 Wiki Link를 유지하고, `relations.json`에는 추가 유형·근거·해석 검수 상태를 내보낸다. 그래프의 선 색상별 유형 표현은 아직 구현하지 않았다.

검수 양식은 `templates/content-review.md`, 자동 생성 대기 목록은 `content/project/review-queue.md`이다. 자동 목록 생성은 사람 검수가 아니다.

## 계획 계열 확장 (v0.5)

계획 식별에는 `plan_family`와 `plan_number`를 함께 사용한다. 번호가 같아도 다른 계열의 문서는 동일 계획이 아니다. 스키마는 아래 조합을 검증한다. 허용 차수는 입력 구조의 범위이며 해당 차수 전문을 모두 수집했다는 뜻은 아니다.

| plan_family | 허용 차수 | category |
| --- | --- | --- |
| 전력수급기본계획 | 10, 11, 12 | 전력수급계획 / 전력수요 |
| 장기송변전설비계획 | 10, 11, 12 | 송변전망 |
| 에너지기본계획 | 1, 2, 3 | 에너지정책 |
| 신재생에너지기본계획 | 1, 2, 3, 4, 5 | 재생에너지정책 |
| 재생에너지기본계획 | 1 | 재생에너지정책 |

2026년 제1차 재생에너지 기본계획을 제6차 신재생에너지 기본계획으로 임의 변경하지 않는다. 원문의 과거 계획 평가에 따라 references 관계를 남기며, 서로 다른 계열 사이에 이전/다음 개정 관계를 추정하지 않는다. 발표일은 정부 확정 발표를 근거로 하고 재게시 기관의 등록일·표지 월호는 기본정보 또는 verification_notes에서 구분한다.
