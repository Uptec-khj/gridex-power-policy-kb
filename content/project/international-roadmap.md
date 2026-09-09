---
title: 국가별 전력정책·기술기준 확장 로드맵
tags: [프로젝트, 로드맵, 국제비교, 자료수집]
type: project_roadmap
status: proposed
updated: '2026-09-09'
ai_generated: true
---

[[roadmap|전체 로드맵]] · [[development-backlog|개발 백로그]] · [[technical-documents|국내 기술 문서]]

> [!info] 설계안 · 2026-09-09
> 대한민국 자료 37건을 기반으로 호주·미국·중국·유럽까지 확장한다. 이번 결과는 **메뉴·데이터·수집 운영에 대한 계획**이다. 해외 문서 수집, 국가 탭, 정기 실행은 아직 구현·활성화하지 않았다. 아래 설명은 AI가 공식 자료원을 조사해 작성한 설계이며 사람 검수는 대기 상태다.

## 1. 목표와 첫 확장 범위

나라를 선택하면 그 나라의 에너지정책, 전력계획, 송전망계획, 계통연계 기준, 발전단지 시험·성능평가 자료를 같은 구조로 읽는다. 한국어 요약에서 원어 본문·조항·PDF 쪽수로 이동하고, 개정 전후 문서를 연결한다.

해외 첫 묶음은 **4개 지역 × 6건 = 24건**을 목표로 한다. 지역마다 계획·전망 2건, 송전망·계통계획 1건, 연계기준·모델·성능평가 3건을 선정한다. 전문 확보가 어려우면 그 사실을 표시하고 부족한 수량을 완료로 계산하지 않는다. 국내 30~50건 MVP와 별도 집계하며, 번역본·첨부 형식·분할 PDF를 새 정책 문서로 중복 계산하지 않는다.

수집 순서는 **공통 구조 → 호주 → 미국 → 유럽 → 중국 → 정기 운영**으로 제안한다. 호주에서 계획과 성능기준의 연결을 검증하고, 미국에서 여러 관할을, 유럽에서 초국가 규정과 국가별 적용을, 중국에서 원어 검색과 표준번호·공개 범위를 검증한다. 이는 개발 순서이며 자료의 중요도 순위가 아니다.

## 2. 메뉴와 읽기 흐름

```text
전체 | 대한민국 | 호주 | 미국 | 중국 | 유럽
  선택한 국가·지역
    개요 · 주요 기관 · 최근 변경 · 수집/검수 현황
    에너지·재생에너지 정책
    전력수급·장기 수요전망
    송전망·계통개발 계획
    계통연계·기술기준
    발전단지 시험·성능평가·모델 검증
    전력시장·운영 규칙
    문서 목록 · Timeline · 원문 검색
```

국가 메뉴는 주소를 가진 탐색 링크로 구현한다. 예: `regions/au`, `regions/us`, `regions/cn`, `regions/europe`. 화면은 탭처럼 보이되 직접 공유·새로고침·키보드 탐색이 가능하게 하고 모바일에서도 모든 항목에 접근하게 한다. 기존 국내 문서 주소와 Wiki Link는 유지한다.

| 상위 메뉴 | 추가로 선택할 적용 범위 | 설계에서 구분할 점 |
| --- | --- | --- |
| 대한민국 | 전국 / 지역 / 개별 적용 대상 | 현재 자료·검색·링크 유지 |
| 호주 | NEM / WEM / 기타 지역 | NEM 자료를 호주 전체 기준으로 표시하지 않기 |
| 미국 | 연방 / 주 / ISO·RTO 및 적용 계통 | 기관 소재지와 문서 적용 지역 분리 |
| 중국 | 국가 / 성·지역 / 계통사업자 | 국가표준·산업표준·기업기준, 계획안·확정본 분리 |
| 유럽 | EU 공통 / 범유럽 계통 / 국가별 | 유럽은 탐색 지역, EU는 법적 관할. 영국은 국가별로 별도 표시 |

위 구분은 [AEMO의 NEM·WEM 안내](https://www.aemo.com.au/energy-systems/major-publications/integrated-system-plan-isp), [NERC의 관할별 기준 목록](https://www.nerc.com/standards/reliability-standards), [ENTSO-E Network Codes](https://www.entsoe.eu/network_codes/)를 참고한 데이터 설계다. 각 문서의 실제 적용 범위는 원문으로 확인한다.

검색은 선택한 지역 안에서 시작하며 전체 검색으로 전환할 수 있게 한다. 공통 필터는 **지역·관할·전력시장·문서 종류·발행기관·언어·문서 단계·시행 상태·발행연도·검수 상태**다. 자료가 없는 메뉴에는 수집 예정·확보 건수를 표시한다.

## 3. 공식 자료원과 초기 수집 후보

아래는 공식 자료원 탐색 결과이며, 모든 사이트에 수집기가 연결되었다는 뜻은 아니다. 기계 판독 후보 목록은 [international-candidates.yaml](https://github.com/Uptec-khj/gridex-power-policy-kb/blob/main/sources/international-candidates.yaml)에 저장한다. 후보 목록은 실행 Registry와 분리하고 `enabled: false`를 유지한다.

| 지역 | 우선 공식 자료원 | 먼저 살펴볼 자료 | 수집 시 확인할 사항 |
| --- | --- | --- | --- |
| 호주 | [AEMO ISP](https://www.aemo.com.au/energy-systems/major-publications/integrated-system-plan-isp) | Integrated System Plan, 수요·시나리오·송전망 부속자료 | 판본 연도, 초안·확정·추록, NEM 적용 범위 |
| 호주 | [AEMC NER](https://www.aemc.gov.au/regulation/energy-rules/national-electricity-rules) | National Electricity Rules, 접속·발전설비 성능 관련 조항 | 통합본 버전과 개별 개정의 시행일 |
| 호주 | [AEMO GPS template](https://aemo.com.au/consultations/current-and-closed-consultations/gps-template), [WEM GPS](https://www.aemo.com.au/energy-systems/electricity/wholesale-electricity-market-wem/system-operations/gps-framework) | 성능기준 양식·적용 안내, 모델·시험 문서로 이어지는 공식 링크 | 양식·협의 공지·규칙 전문 구분, NEM/WEM 혼합 방지 |
| 미국 | [DOE Needs Study](https://www.energy.gov/oe/national-transmission-needs-study), [Planning Study](https://www.energy.gov/oe/national-transmission-planning-study-0) | 송전 수요 평가와 장기 계획 연구 | 연구보고서와 승인된 건설계획 구분 |
| 미국 | [FERC Generator Interconnection](https://www.ferc.gov/electric-transmission/generator-interconnection) | Order 2023·2023-A, 관련 공고·설명 | 명령 원문·설명자료·지역 이행 문서 연결 |
| 미국 | [NERC Standards](https://www.nerc.com/standards/reliability-standards), [Guidelines](https://www.nerc.com/our-work/guidelines/reliability-guidelines) | TPL·MOD·PRC 계열, IBR·EMT·발전단지 모델 검증 가이드 | 표준과 비구속적 가이드, 미국 적용 상태를 별도 확인 |
| 미국 | [CAISO Transmission Planning](https://www.caiso.com/generation-transmission/transmission/transmission-planning), [Interconnection](https://www.caiso.com/generation-transmission/generation/generator-interconnection) | 지역 송전계획·접속 절차 | 첫 ISO 사례로 한정, 미국 전체로 일반화 금지 |
| 유럽 | [ENTSO-E TYNDP 진행 공지](https://www.entsoe.eu/news/2026/04/02/tyndp-2026-project-portfolio-expands-further-to-199-transmission-and-69-storage-project/), [TYNDP 포털](https://tyndp.entsoe.eu/) | Ten-Year Network Development Plan, 시나리오·평가 지침 | 개별 프로젝트 목록과 최종 계획 구분 |
| 유럽 | [ENTSO-E RfG](https://www.entsoe.eu/network_codes/rfg/), [EUR-Lex 원문 경로](https://eur-lex.europa.eu/eli/reg/2016/631/oj/eng), [적용 가이드](https://www.entsoe.eu/network_codes/cnc/cnc-igds/) | 발전설비 접속 규정, 적용 가이드 | 법령 원문·개정·통합본·비구속적 가이드 구분 |
| 중국 | [NEA 제15차 5개년 에너지계획 공고](https://www.nea.gov.cn/20260625/0ccfdc1674e84868b49480edf584eb5f/c.html), [제14차 계획](https://zfxxgk.nea.gov.cn/2022-01/29/c_1310524241.htm) | 에너지체계 계획, 전력·재생에너지 하위 계획 | 작성일·공개일·계획기간 및 발문번호 분리 |
| 중국 | [SAMR 국가표준 상세](https://std.samr.gov.cn/gb/search/gbDetailed?id=p3zoY65no%2FU%3D&mode=p) | GB/T 19964-2024 태양광발전소 계통연계 기술규정, 관련 풍력·시험 표준 | 현행/폐지/대체 표준, 전문 공개·재배포 조건 |
| 유럽 후속 | [NESO Grid Code](https://www.neso.energy/industry-information/codes/grid-code-gc/grid-code-documents), [개정 목록](https://www.neso.energy/industry-information/codes/grid-code-gc/grid-code-modifications) | 영국 계통규정·개정 이력 | 적용 계통 확인 후 별도 관할로 등록 |

이번 조사에서 확인한 버전 주의 사례:

- DOE의 현재 Needs Study 안내는 **2026년 7월 공개 초안**을 소개한다. 이전 확정 보고서와 새 초안을 각각 보존한다. [DOE 안내](https://www.energy.gov/oe/national-transmission-needs-study)
- ENTSO-E의 2026년 4월 공지는 프로젝트 포트폴리오와 이후 평가 일정을 다룬다. 이 공지만으로 TYNDP 2026 최종본 확보를 표시하지 않는다. [ENTSO-E 공지](https://www.entsoe.eu/news/2026/04/02/tyndp-2026-project-portfolio-expands-further-to-199-transmission-and-69-storage-project/)
- NEA에서 제15차 5개년 에너지체계 계획 공고를 확인했다. 제14차 문서를 최신으로 고정하지 않고 후속 계열을 함께 조사한다. 첨부 전문 검토는 수집 단계에서 수행한다. [NEA 공고](https://www.nea.gov.cn/20260625/0ccfdc1674e84868b49480edf584eb5f/c.html)
- 직접 열기에서 AEMC는 403, EUR-Lex는 브라우저 검증 화면, TYNDP 포털은 추출 본문 없음이 관찰되었다. 검색에 노출되는 것과 안정적으로 자동 수집 가능한 것은 다르다. 공식 다운로드·공개 API·수동 등록 경로를 먼저 검토한다.

장기 후속 후보는 미국의 추가 ISO/RTO·주별 에너지계획, 유럽 개별국가의 에너지·기후계획과 TSO 계획, 중국 성별·계통사업자 공개 기준이다. 첫 24건과 운영 안정성 검증 후 기관별 공식 URL을 추가 조사한다.

## 4. 공통 Metadata 설계

기존 17개 필드와 10개 본문 절을 보존하면서 국제 문서용 확장 표준을 설계한다. 아래는 **후속 스키마 변경 제안**이며 현재 템플릿에 바로 입력할 필드 목록이 아니다.

| 정보 | 제안 필드 | 처리 원칙 |
| --- | --- | --- |
| 탐색 지역 | `region_group` | KR/AU/US/CN/Europe 등 메뉴용 값 |
| 법적·운영 관할 | `jurisdictions` | 관할 ID·종류·국가코드·근거 URL. EU를 국가코드로 취급하지 않음 |
| 적용 계통·시장 | `market_regions` | NEM/WEM/CAISO 등 복수 범위 가능 |
| 원어 제목·언어 | `title_original`, `title_ko`, `document_language` | 원어 보존, 한국어 번역 제목 별도, 언어는 BCP 47 형태 |
| 문서 식별 | `document_type`, `document_identifier`, `edition_year`, `version` | 법령·표준번호·연도판·차수를 분리 |
| 시행·유효 상태 | `adopted_date`, `effective_date`, `validity_status`, `status_checked_date` | 발행·채택·시행·폐지 별도. 미확인은 null/unknown |
| 법적 성격·대상 | `legal_force`, `applicability` | 의무기준/가이드/계획/연구 등, 근거와 함께 기록 |
| 번역과 검수 | `translation_status`, `translation_review_status` | AI 번역을 공식 번역 또는 사람 검수로 표시하지 않음 |
| 이용조건 | `rights_status`, `rights_url`, `archive_access` | 원문 보존 가능 여부와 공개 재배포 가능 여부 분리 |

현재 스키마는 한국어 계획 계열·차수 조합에 제한되어 있다. 외국 계획에 한국식 차수를 강제하지 않도록 계열 사전과 문서 종류를 먼저 확장한다. `plan_number: null`을 기술문서 판별로 쓰는 현재 검색도 `document_type` 기반으로 변경해야 한다. 기존 37건을 마이그레이션할 때 문서 ID·원본 해시·공개 주소·관계 링크가 동일함을 검증한다.

원어와 번역은 동일 문서의 언어 변형으로 연결한다. 원문 추출 색인과 AI 한국어 요약 색인은 출처 유형을 분리하고, RAG 검색 결과에는 관할·판본·쪽수·검수 상태를 함께 반환한다. 영어·중국어 검색어를 한국어 주제어와 연결하되 번역된 문장을 공식 원문 인용으로 제시하지 않는다.

## 5. 문서 관계와 국제 비교

동일 계열 안에서는 이전·다음 문서, 초안→확정, 개정·폐지 관계를 기록한다. 규칙→적용 가이드→시험 절차→시험 결과 제출 안내를 연결하면 발전단지 실무자가 필요한 자료를 따라 읽을 수 있다.

국가 간에는 **주제가 비슷함**과 **제도적으로 동등함**을 구별한다. 예를 들어 한국의 송변전계획과 호주의 ISP는 비교 후보로 연결할 수 있지만 법적 위계가 동일하다고 단정하지 않는다. 기존 근거 기반 관계 모델을 확장하기 전에는 주제 허브에서 비교 목적·차이를 설명한다.

비교할 기술 주제는 계통연계, 고장 시 운전 유지, 무효전력·전압 제어, 주파수 응답, 계통 강도, 인버터 기반 자원, EMT 해석, 모델 검증, 현장 성능시험이다. 수치 비교는 적용 전압·설비 유형·측정점·기준용량·시험 조건·시행일을 확인한 항목에 한정한다. 단위와 정의가 다른 수요·재생에너지 비중도 바로 순위화하지 않는다.

## 6. 지속 수집 흐름

```text
공식 자료원 목록
  → 새 게시물·개정 후보 발견
  → 범위·중복·접근 및 이용조건 확인
  → 원본 보존 + 해시·취득 이력
  → 원문 텍스트·표·쪽수 추출
  → 관할·문서 종류·버전 분류
  → AI 요약·번역·관계 후보 작성
  → 자동 검증 + 검토 대기 목록
  → 검수 상태를 표시해 Markdown 발행
  → 국가 메뉴·Timeline·검색·RAG 색인 갱신
```

자료원별로 **발견기**와 **문서 수집기**를 나눈다. 기존 수집기는 선정된 URL과 첨부를 받는 역할이므로, 새 게시물을 찾는 발견기와 실행 이력·변경 큐가 추가되어야 한다. 공식 API/RSS가 실제 제공되는지 확인하고, 가능하면 이를 우선한다. 다음으로 사이트맵·게시판 HTML·공식 첨부 링크를 사용한다. 동적 페이지는 기관이 허용하는 공개 경로 또는 사람이 확인한 주소로 등록한다.

| 변화 | 처리 |
| --- | --- |
| 새 게시물 | 범위 분류 후 후보 큐 등록, 허브·홍보문·정책 전문 구분 |
| 동일 파일이 다른 URL에 게시 | SHA-256으로 중복 식별, 공식 재게시 출처 관계 보존 |
| 같은 URL의 파일 바이트 변경 | 이전 파일 유지, 새 해시·취득일 기록, 변경 검토 후보 생성 |
| 메뉴·배너·조회수만 변경 | 본문/첨부 목록 비교로 걸러내고 정책 개정으로 기록하지 않음 |
| 파일 메타데이터만 변경 | 바이트 변경은 기록하되 정책 내용 변경 여부는 별도 대조 |
| URL 삭제·접근 실패 | 기존 문서를 지우지 않고 마지막 성공일·실패 원인·대체 공식 경로 기록 |
| 개정안·협의 종료 | 확정·시행을 추정하지 않고 실제 후속 공고 확인 |

수집 결과가 편집 Markdown을 자동 덮어쓰지 않게 한다. 새 요약과 변경 제안은 검토 큐 또는 변경 제안으로 제출한다. 사람 검수자·날짜는 실제 검수에만 기록한다. 원문 확인이 끝난 AI 요약의 공개 여부와 기술 수치·번역의 사람 검수 완료 여부는 분리한다.

## 7. 운영 주기와 원본 보존

아래 주기는 파일을 매번 모두 내려받는 주기가 아니라 **게시 목록·버전 정보 확인 주기 제안**이다. 실제 자동 실행은 파일럿 검증과 실행 환경 설정 후 시작한다.

| 대상 | 제안 주기 | 운영 목적 |
| --- | --- | --- |
| 개정·협의·시행 공지 목록 | 하루 1회 | 새 규칙·마감·시행 변경 후보 발견 |
| 계획·전망·표준 목록 | 주 1회 | 새 판본과 부속자료 확인 |
| 과거 자료·링크·이용조건 | 월 1회 | 경로 이동·누락·공개 범위 재점검 |
| 새 첨부 | 발견 시 1회 | 허용된 파일 보존, 변경 시에만 새 판본 저장 |

첫 실행은 자료원별 제한된 기간·페이지 수·최대 20개 신규 후보로 시작한다. 호스트별 동시 요청 1개, 최소 1초 간격을 기본 제안으로 두고 기관의 더 엄격한 정책을 우선한다. ETag/Last-Modified가 제공되면 조건부 요청을 사용하고, 429의 Retry-After·일시적 서버 오류에는 지수 대기와 제한된 재시도를 적용한다. 403·인증·CAPTCHA는 자동 우회하지 않고 수동 확인 대상으로 전환한다.

실행 Registry 승격 전 robots.txt·이용약관·파일 재배포 조건·허용 다운로드 도메인을 기록한다. 현재 조사는 이 권리 검토를 완료한 것이 아니다. 공개 열람과 공개 GitHub 재배포가 같은 허용을 뜻하지 않는다. 재배포 미확인 국제 원본은 공개 `data/raw`에 넣지 않고 접근이 제한된 별도 보관 영역에서 검토한다. 보존 권한 자체가 없으면 메타데이터와 공식 링크만 기록한다. 공개 가능한 원본만 해시 저장소로 승격하고, 유료 표준 전문은 권리 확인 없이 복제하지 않는다.

자료원 상태는 마지막 성공·실패, 신규 후보 수, 실패 원인, 추출 가능한 페이지 비율, 검수 대기 수, 시행 상태 확인일을 남긴다. 변경이 없는 정상 실행도 이력은 남긴다. 알림 채널·수신자·예약 실행은 이번 계획에서 활성화하지 않는다.

## 8. 개발 단계와 완료 기준

각 단계의 완료 기준을 충족한 뒤 다음 단계로 진행한다. 기간은 실제 수집 접근성과 검수량을 측정한 뒤 정하며 현재는 날짜를 약속하지 않는다.

| 단계 | 개발 결과 | 완료 기준 |
| --- | --- | --- |
| G0 · 범위·자료원 설계 | 이 로드맵과 비활성 후보 목록 | 네 지역 자료원·메뉴·수집 흐름·남은 검증 명시 |
| G1 · 국가 탐색·표준 | 국가/지역 허브, 관할·언어·문서 종류 Metadata, 공통 필터 | 한국 37건의 주소·해시·검색 유지, 빈 지역 표시, 잘못된 관할/계열 조합 차단 |
| G2 · 호주 파일럿 | AEMO/AEMC 공식 문서 6건, 발견기 첫 사례 | NEM/WEM 구분, 초안·버전·시행일 확인, 요약에서 원문 근거 이동 |
| G3 · 미국 파일럿 | DOE/FERC/NERC 중심 6건, CAISO 지역 사례 우선 검토 | 연방/지역 적용 구분, 의무기준/가이드 구분, 시행 상태 근거 기록 |
| G4 · 유럽·중국 파일럿 | 각 6건, EUR-Lex/ENTSO-E 및 NEA/SAMR 사례 | EU/국가 범위 구분, 중국어 검색·표준 대체 관계·공개 범위 검증 |
| G5 · 지속 수집 운영 | 변경 큐, 재시도, 이용조건 확인, 실행 보고·정기 실행 설정 | 최소 2회 증분 실행에서 중복·무변경·실제 변경·실패 복구 검증, 기존 편집 보존 |
| G6 · 국제 비교·RAG | 다국어 주제 사전, 관할 필터 검색, 비교용 근거 묶음 | 20개 평가 질문에서 국가·버전 혼동 및 근거 없는 수치 답변 0건 |

파일럿 24건의 공통 통과 기준:

- 모든 문서에 공식 원문 링크·언어·적용 범위·문서 단계·확보 상태가 있다. 확보한 파일은 해시를 검증한다.
- 각 문서에서 핵심 주장 2개 이상을 원문 조항 또는 PDF 물리적 쪽수로 추적한다. 표지와 인쇄 쪽수가 다르면 둘 다 구분한다.
- OCR·번역·표 추출이 불충분한 항목은 검색 가능 범위와 검수 대기로 표시한다.
- 핵심 기술 수치·시행일·번역 표본 10개 이상을 사람이 대조해야 **검수 완료** 단계로 넘어간다. AI 대조만 완료되면 파일럿은 검수 대기로 유지한다.
- 지역 필터에 다른 관할 문서가 섞이지 않고, 복수 관할 문서는 중복 저장 없이 해당 메뉴에서 탐색된다.
- 동일 URL 파일 교체·다른 URL 동일 파일·배너 변경·429·403·본문 누락 사례를 시험한다.
- 사람의 정책 검수와 수집 프로그램의 자동 검증 결과를 각각 기록한다.

## 9. 저장소별 후속 변경 계획

| 위치 | 예정 역할 |
| --- | --- |
| `content/regions/` | 국가·지역별 Obsidian 탐색 허브, 공개 탭의 목적지 |
| `content/documents/` | 기존 위치 유지, 해외 문서는 기관·식별자·판본 기반 안정 ID 사용 |
| `sources/international-candidates.yaml` | 이번에 작성한 비활성 자료원 후보 |
| `sources/registry.yaml` | 접근·권리·파서 검증을 통과한 자료원만 승격 |
| `schemas/`, `templates/` | 관할·언어·버전 표준과 작성/검수 양식 |
| `collector/` | 자료원별 발견·수집 어댑터, 변경 비교·실패 복구 |
| `data/metadata/` | 원본 버전·문서 상태·수집 실행 이력·권리 판정 |
| `site/` | 국가 메뉴·관할 필터·원어 제목·버전·시행 상태 표시 |
| `ai/` | 한국어/원어 검색, 용어 사전, 인용 평가 질문, 번역 검수 상태 |

바로 다음 개발 작업은 **G1: 국내 자료의 호환성을 유지하는 국제 Metadata 표준과 국가별 탐색 구조**다. 그 뒤 호주 6건으로 수집·검색·검수의 전체 경로를 검증한다. 국내 원문 복원과 [[review-queue|사람 검수 대기 작업]]도 별도 완료 조건으로 계속 유지한다.
