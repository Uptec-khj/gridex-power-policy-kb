# Source Registry

`international-candidates.yaml`은 [국가별 확장 로드맵](../content/project/international-roadmap.md)의 **비활성 조사 후보**입니다. 실행 Registry가 아니며 수집기는 이 파일을 읽지 않습니다. 자료원마다 `enabled: false`이고, 공통 접근·이용조건 검토는 `defaults`에 명시합니다. URL 확인은 전문 수집·재배포 허용·자동 수집 가능성 검증을 뜻하지 않습니다. 검증을 마친 항목만 별도 작업에서 `registry.yaml`로 승격합니다.

`registry.yaml`은 기관 ID·발행기관·공식 도메인·우선순위·범위·수집 어댑터를 정의합니다. `seed-documents.yaml`은 실제 수집할 공식 게시물과 첨부 후보입니다. `backlog.yaml`은 미확보 자료와 후속 검수를 관리합니다.

기관 등록과 문서 수집은 별개입니다. 도메인이 공식이어도 사보·보도자료·법정계획 전문의 문서 단계는 구분합니다. 검색 결과를 증거로 저장하지 않고 공식 원문으로 이동해 확인합니다. 목록에 없는 도메인으로의 리디렉션은 자동 수집하지 않습니다.

발행 당시 산업통상자원부 문서는 현재 산업통상부 사이트가 제공하더라도 발행기관명을 변경하지 않습니다. 기후부의 이관 보도자료는 boardMasterId 변경을 확인했습니다. 세션 식별자나 일시적인 다운로드 토큰을 영구 URL에 넣지 않습니다.

수집 결과는 `data/metadata/acquisitions.json`에 기록합니다. status는 collected/partial/failed이며, 공식 게시물의 진위 확인과 내용 검수 여부는 문서 Frontmatter에 따로 기록합니다. 컬렉터는 공식 게시물의 expected_text를 대조해 오류·홈페이지 반환을 걸러냅니다. 새 사이트 구조에는 수동 원문 대조가 필요합니다.
