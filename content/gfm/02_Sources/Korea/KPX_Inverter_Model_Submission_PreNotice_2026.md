---
id: SRC-KR-KPX-2026-003
family_id: FAM-KR-KPX-INVERTER-MODEL-GOVERNANCE
title_original: 발전사업자 대상 계통해석 모델 제출 사전안내 공지문
title_ko: 인버터 설비 계통해석 모델 제출·검증 사전안내
organization: 한국전력거래소
jurisdiction_market: Republic of Korea, 송전연계 IBR·중앙계약전기저장장치
document_type: 사전안내·규칙 및 세부운영규정 개정안
edition: "2026-08-25 공지"
language: ko
publication_date: 2026-08-25
approval_date:
effective_date:
facility_cutoff_date: 2027-03
official_page_url: https://www.kpx.or.kr/board.es?act=view&bid=0042&list_no=77979&mid=a11201000000
official_document_url: https://new.kpx.or.kr/boardDownload.es?bid=0042&list_no=77979&seq=3
relevant_clauses_pages: "공지 1~7항; 첨부2 개정안 제13장 13.1~13.5"
access_status: 공식 본문과 개정안 PDF 공개·검토
document_status: 사전안내·개정안; 확정 시행본 아님
applicability: 예정 시장·계통연계 조건; 내용 변동 가능
rights_holder: 한국전력거래소
license: 미확인
terms_url: https://new.kpx.or.kr
redistribution: 미확인
rights_checked_on: 2026-09-09
publication_mode: 공식 링크·자체 한국어 요약·조항 색인
review_status: 본문·첨부2 개정안 직접 검토
verified_on: 2026-09-09
---

# 인버터 설비 계통해석 모델 제출·검증 사전안내

KPX는 송전계통에 연계되는 풍력·태양광·연료전지 및 중앙계약전기저장장치 사업자를 대상으로 계통해석 모델 제출 제도를 사전 안내했다. 공지는 2026년 3분기 규칙개정 결과 등에 따라 변동될 수 있다고 명시하며, 시행 예정 시점은 2027년 3월이다.

## 제출·승인 흐름

| 단계 | 사전안내 내용 |
|---|---|
| 대상 | 22.9 kV 전용선로 및 154 kV 이상 송전연계 IBR와 중앙계약전기저장장치 |
| 제출 | 단위기, 발전소 상세·등가모델 및 모델 유효성 검증보고서 |
| 시기 | 전력거래 개시 예정일 5개월 전까지 |
| 검토 | 모델 적합성 검증과 계통평가위원회 승인 |
| 결과 | 시행 후 승인절차를 통과해야 전력거래개시 승인 가능 |
| 버전 | 2027년 7월 이후 개시 예정 사업자는 해석프로그램 V36 제출 요청 |

공지에서 연결한 한전 근거는 `송·배전용전기설비이용규정 제35조 제3항`과 `송전계통연계 기술기준 12. 설비특성자료`다. 이는 한전 규정의 GFM 전용 조항을 직접 확인한 것과는 구분한다.

## 첨부2 제13장 개정안

- 초기모델: 단위기 시험을 반영한 단위기·발전소 상세·등가모델과 검증보고서
- 확정모델: 계통병입 후 현장시험을 반영해 초기모델을 보완
- 시험 인정방식: 전문시험기관, 제조사 공장시험, 현장시험
- 보고서 최소자료: 회로·전원측 임피던스, 단락용량·X/R·계측위치, 제어설정, 3상 Raw 및 Phasor 데이터, 적부판정, 제조사 자료
- 모델 파일: `.sav`, `.dyr`, `.sld`, 시험 시나리오 `.py`, 제어모드·파라미터 표
- 정합성 원칙: 하나의 파라미터 세트로 전체 동특성을 검증하고 모델 응답은 실제 설비보다 보수적이어야 함
- 안정구간 정량기준: 시험과 모델 결과가 정격 유·무효전력 기준 5% 이내
- 추종구간: 입력 후 5초 이내의 응답속도·상승시간·정착시간·오버슈트를 종합 판단

V36 모델 목록에는 `REPCGFMC1U`, `REGFMC1U`가 포함되어 GFM 표현이 가능한 범용 동적모델 경로를 제시한다. 그러나 이 개정안은 GFM 전용 EMT 모델 제출이나 GFM 기능별 성능시험을 확정한 문서가 아니며, RMS 범용모델 검증과 EMT 검증을 동일시하지 않는다.

관련: [KPX 확정 시장규칙](KPX_Market_Rules_2026_04_29.md) · [확정 세부운영규정 선행판본](KPX_Grid_Assessment_Detailed_Rules_2026_02.md) · [시험 색인](../../07_Tests/시험_색인.md)

