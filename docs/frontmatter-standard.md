# GRIDEX Frontmatter 표준 v1.0

공식 자료는 `content/documents/<id>.md`에 UTF-8 YAML Frontmatter와 Markdown 본문으로 저장한다. 기계 검증 규칙은 `schemas/policy-document.schema.json`이다. 허브·Timeline은 탐색 문서로서 공식 자료 수에 포함하지 않는다.

| 필드 | 형식 | 규칙 |
| --- | --- | --- |
| title | 문자열 | 원문 식별에 충실한 제목. 편집 제목은 기본정보에 명시 |
| organization | 문자열 | 발행 당시 기관명. 현재 호스팅 기관명으로 소급 변경 금지 |
| published_date | 날짜 문자열 또는 null | 따옴표로 감싼 YYYY-MM-DD. 미상은 null, 수집일·월초로 추정 금지 |
| category | 열거형 | 전력수급계획 / 전력수요 / 송변전망 |
| subcategory | 문자열 | 기본계획 / 확정발표 / 수정공고 / 장기전력수요전망 / 수립착수 / 정책토론회안내 / 기관해설 등 |
| plan_family | 열거형 | 전력수급기본계획 / 장기송변전설비계획 |
| plan_number | 정수 | MVP: 10, 11, 12 |
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
- `schema_version`: 문자열 '1.0'. `source_id`: Source Registry 키.
- `attachments`: 첨부별 URL·제목·보존 경로·해시·형식·크기·수집 시각·권리 확인 상태.
- `source_snapshot`: 게시물 HTML의 보존 경로와 SHA-256. 대표 첨부 해시와 분리.
- `ai_generated`: AI 작성·편집 포함 여부. `summary_review_status`: unreviewed / reviewed.
- `reviewed_by`, `reviewed_date`: 사람이 검수한 경우 GitHub ID 등과 날짜. 자동 채우기 금지.
- `events`: 날짜·사건명·publication/scheduled/confirmed·근거 URL. 보도일과 행사일을 분리.
- `draft`: true이면 Quartz 및 공개 RAG 인덱스에서 제외.
- `tags`, `aliases`: Obsidian·Quartz 탐색용. `date`는 확인된 published_date의 Quartz 표시용 복제값으로 null 허용.
- `last_verified_date`, `verification_notes`: 확인 범위와 한계.

확장 시 스키마를 함께 갱신한다. 예약되지 않은 필드는 CI에서 거부한다.

## 문서 단계

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
