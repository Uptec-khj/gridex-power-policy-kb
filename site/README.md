# GRIDEX Quartz 사이트

Quartz 공식 엔진을 site/에 고정하고 ../content를 직접 읽습니다. 저장소 루트에서 npm --prefix site ci, npm --prefix site run build, npm --prefix site run preview를 실행합니다.

public/은 배포 생성물이며 Git 제외입니다. 검색·그래프·백링크·태그·목차를 제공합니다. PolicyMetadata 컴포넌트는 공식 자료의 문서 단계, 발행일, AI 요약 검수 상태를 표시합니다. 외부 분석 추적은 비활성화했습니다.

현재 gh-pages 브랜치를 통해 공개합니다. 저장소 루트의 scripts/publish-pages.py를 사용합니다. GitHub Actions 자동화 예제는 docs/workflows/pages.yml에 있으며 workflow 등록 권한 확보 후 활성화할 수 있습니다. Quartz 업데이트 시 UPSTREAM.md·잠금파일을 함께 갱신하고 실제 콘텐츠로 빌드 검증합니다.

CountryNavigation은 국가 허브로 연결합니다. DocumentSearch는 PDF 없는 문서를 포함해 제목·주제·원어 제목과 분류를 찾고, OriginalSearch는 공식 PDF 페이지를 찾습니다. 관할·시장·언어·문서 종류는 `schemas/international-taxonomy.json`을 공통으로 사용합니다. 필터는 URL에 보존하며 국가 변경 시 종속 관할·시장 선택을 초기화합니다. 기본 Quartz 검색은 전체 KB 검색으로 유지합니다.

자료 탐색은 `knowledgeExplorer.ts`에서 국가 → 계획·기술 → 공식 문서 → 검색 → 이용·검수 안내 순으로 정렬합니다. 국가·계획 폴더는 한글 이름과 고정 순서를 사용하며 문서 전체 폴더는 최근 날짜순입니다. 폴더 제목을 클릭하면 펼치거나 접습니다. 개발 문서는 별도 [개발 관리 저장소](https://github.com/Uptec-khj/gridex-project-management)에 보관하며 기존 공개 주소만 검색·사이트맵에 포함되지 않는 이동 안내로 유지합니다.

국가 허브 `content/regions/*.md`는 `scripts/kb.py build`로 재생성합니다. 국가 허브의 본문을 직접 편집하지 말고 생성기·원본 Metadata·자료원 후보를 수정합니다. Quartz의 내부 링크 변환은 검색 URL의 query를 보존하도록 수정했으며 `quartz/util/path.test.ts`에 회귀 검증을 추가했습니다.
