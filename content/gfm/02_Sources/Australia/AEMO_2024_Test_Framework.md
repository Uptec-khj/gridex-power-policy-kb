---
id: SRC-AU-AEMO-2024-002
family_id: FAM-AEMO-GFM-SPEC
title_original: "Voluntary Specification for Grid-forming Inverters: Core Requirements Test Framework"
title_ko: GFM 핵심요건 자발적 모의시험 프레임워크
organization: AEMO
jurisdiction_market: Australia NEM
document_type: 모의시험 프레임워크
edition: January 2024
language: en
publication_date: 2024-01-18
official_page_url: https://www.aemo.com.au/initiatives/major-programs/engineering-roadmap/engineering-roadmap-execution-reports
official_document_url: https://www.aemo.com.au/-/media/files/initiatives/engineering-framework/2023/grid-forming-inverters-jan-2024.pdf
relevant_clauses_pages: "§2~3, pp.9~21; Appendix A1~A2"
access_status: 공식 전문 공개
document_status: 확정
applicability: 자발적·연구/계약 참고
rights_holder: Australian Energy Market Operator Limited
license: AEMO 저작권 허용조건 참조
terms_url: https://www.aemo.com.au/privacy-and-legal-notices/copyright-permissions
redistribution: 미확인
rights_checked_on: 2026-09-09
publication_mode: 링크·자체 한국어 요약
review_status: 핵심·수치 검토
verified_on: 2026-09-09
---

# AEMO GFM Core Requirements Test Framework

3개 모의 testbench와 7개 핵심시험을 제안한다: 동기기 상실(방전·충전·한계·전력균형), RoCoF 상하 변화, 고장 동반 SCR 저하, 위상각 계단이다. CHIL 적용과 임피던스 스캔 방법도 논의한다. 기존 NER 적합시험을 대체하지 않으며 모든 계통·운전조건의 GFM 능력을 인증하지 않는다.

검증된 대표 조건: Test 5는 SCR 10, X/R 6, 50% 출력에서 4 Hz/s로 50↔51 Hz와 50↔49 Hz를 변화시킨다. Test 6은 초기 SCR 20·100% 출력에서 SCR을 10, 3, 2, 1.5, 1.25로 낮추고 전환 직전 6-cycle 2상지락(fault depth 최소 0.5 pu)을 인가한다. Test 7은 SCR 3·50% 출력에서 ±10°, ±30°, ±60°를 적용하되 큰 각도의 판정은 접속점 조건에 따라야 한다.

관련: [비교표](../../10_Comparisons/초기_요구사항_시험_비교.md) · [추적 예제 A](../../10_Comparisons/요구_시험_증빙_연결_예제.md)

