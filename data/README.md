# 데이터와 원본 보존

- raw/sha256/<앞 2자리>/<SHA-256>.<형식>: 불변 원본 바이트. PDF/HWP/HWPX와 공식 게시물 HTML을 보존합니다.
- metadata/acquisitions.json: 실제 수집 상태·오류·파일 메타데이터·과거 획득 기록. 수집기의 기록입니다.
- metadata/documents.json, relations.json, timeline.json: Markdown에서 파생된 인덱스. 직접 편집하지 않습니다.
- extracted/: 파생 텍스트 작업공간. Git에 넣지 않으며 원문 쪽수·추출 도구·버전을 기록해야 합니다.

대표 file_hash는 실제 보존한 첨부 해시입니다. HTML 스냅샷 해시와 혼합하지 않습니다. 공개 Markdown에 원문 자체를 통째로 붙이지 않으며 공식 다운로드와 GitHub 보존 경로를 연결합니다.
