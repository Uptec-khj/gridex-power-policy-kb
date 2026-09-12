# 공개 검색과 근거 연결

`index/chunks.jsonl`은 사람이 편집할 수 있는 Markdown 요약의 파생 인덱스입니다. 원문 전문·OCR·내부 보관 경로는 포함하지 않습니다. `python scripts/kb.py build`로 재생성합니다.

문서 ID·공식 URL·문서 단계·판본·쪽수 인용·검수 상태를 유지합니다. `python scripts/kb.py search "전력수요"`로 검색하고, `--verified-only`는 사람이 검수한 문서만 선택합니다. 초기 문서의 AI 요약은 검수 대기 상태입니다.

벡터 검색·생성형 API는 미활성입니다. 원문 검색과 추출은 내부 운영 기능이며 공개 빌드에서 실행하지 않습니다.
