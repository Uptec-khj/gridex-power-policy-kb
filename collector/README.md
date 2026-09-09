# 공식 자료 수집기

저장소 루트에서 `python -m collector`를 실행합니다. curated seed만 수집하며 무제한 크롤링·자동 문서 작성·자동 공개는 하지 않습니다. --id로 문서 하나를 선택하고 --refresh로 재수집합니다.

기관별 링크 추출: adapters.py의 KPX(boardDownload), 산업부(attach/down), 기후부(ajaxFileDownLoad의 fileId/fileSeq). 한전의 동적 게시판은 수동 수집 대상으로 남겨 두었습니다.

HTTPS·공식 도메인 제한, 리디렉션 확인, 타임아웃, 요청 간격, 파일 매직 바이트 검사, HWPX ZIP 내부 검사, SHA-256 기반 중복 제거를 수행합니다. 완전히 성공한 문서는 기본 실행에서 캐시를 사용합니다. 부분 실패는 실패 목록과 성공 파일 모두 보존합니다. 모든 오류는 종료코드 1로 CI/운영자가 인식할 수 있게 합니다.

수집 기록을 갱신한 뒤 콘텐츠 편집자가 실제 원문을 확인하고 Markdown에 첨부·출처·숫자를 반영해야 합니다. 검증 상태를 자동으로 human_verified로 올리지 않습니다.
