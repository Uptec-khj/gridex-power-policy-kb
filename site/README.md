# GRIDEX Quartz 사이트

Quartz 공식 엔진을 site/에 고정하고 ../content를 직접 읽습니다. 저장소 루트에서 npm --prefix site ci, npm --prefix site run build, npm --prefix site run preview를 실행합니다.

public/은 배포 생성물이며 Git 제외입니다. 검색·그래프·백링크·태그·목차를 제공합니다. PolicyMetadata 컴포넌트는 공식 자료의 문서 단계, 발행일, AI 요약 검수 상태를 표시합니다. 외부 분석 추적은 비활성화했습니다.

현재 gh-pages 브랜치를 통해 공개합니다. 저장소 루트의 scripts/publish-pages.py를 사용합니다. GitHub Actions 자동화 예제는 docs/workflows/pages.yml에 있으며 workflow 등록 권한 확보 후 활성화할 수 있습니다. Quartz 업데이트 시 UPSTREAM.md·잠금파일을 함께 갱신하고 실제 콘텐츠로 빌드 검증합니다.
