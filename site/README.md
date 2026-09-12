# GRIDEX 공개 사이트

Quartz 4.5.2가 공개 저장소의 `../content`만 읽습니다. `npm run build`는 요약 인덱스·출처 레지스트리를 재생성하고 원문 파일 없이 빌드한 뒤 검색·그래프·국가 메뉴·공개 경계를 검사합니다.

`npm run preview`는 `http://localhost:8080`에서 미리보기를 제공합니다. `public/`은 Git에서 제외하는 파생 산출물입니다.

PDF 전문 색인과 다운로드 UI는 제거했습니다. 이전 `original-search` 주소는 공식 원문 이용 안내로, 개발 문서의 이전 주소는 비공개 주소를 포함하지 않는 안내로 유지합니다. 배포 전에 `python ../scripts/validate_kb.py .. --site public`으로 검사합니다.
