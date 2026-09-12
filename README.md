# GRIDEX Power Policy Knowledge Base

전력정책과 GFM 규격·시험·인증을 공식 출처와 연결하는 Obsidian-compatible Markdown 지식창고입니다.

[공개 KB](https://uptec-khj.github.io/gridex-power-policy-kb/) · [보관함 시작](HOME.md) · [문서 표준](docs/frontmatter-standard.md) · [생성기 연동](docs/gfm-generator-integration.md) · [원문 정책](source-policy.md)

정책 문서 47건(국내 37건·호주 10건)과 GFM 노트 61개(원문 출처 27건)를 유지합니다. 두 영역은 일부 겹치므로 숫자를 합쳐 고유 문서 수로 표시하지 않습니다. 조사 기준일은 2026-09-11이며, 구조 이전일인 2026-09-12를 새로운 원문 검증일로 사용하지 않습니다. `source_verified`는 공식 출처 확인을 뜻하며 AI 요약의 사람 검수 완료가 아닙니다.

## 저장소 구성

[UPTEC-KOREA Knowledge Base Generator](https://github.com/UPTEC-KOREA/knowledge-base-generator)의 `5fff214` 기준을 적용합니다. 공개 저장소와 비공개 `<name>-dev` 저장소를 별도로 운영하고, 기존 콘텐츠 경로·ID·Quartz 엔진을 유지합니다.

| 위치 | 내용 |
| --- | --- |
| `project.yaml`, `generator-manifest.json` | 생성기 설정·상류 커밋·Level 0 |
| `content/`, `HOME.md`, `hubs/` | 공개 지식·탐색·공식 원문 링크 |
| `data/source-registry.yaml` | 정책 47건·GFM 27건의 출처 메타데이터 |
| `data/institution-registry.yaml` | 기관·공식 도메인 검증 |
| `schemas/`, `taxonomy/`, `templates/` | 도메인 규칙·공통 어휘·문서 양식 |
| `scripts/`, `tests/` | 문서·출처·링크·공개 경계 검증 |
| `site/` | 공개 `content/`만 읽는 Quartz 사이트 |
| `ai/index/chunks.jsonl` | 자체 편집 요약 검색 인덱스 |

원문 파일·추출 전문·수집기·보관 이력·연구 계획은 비공개 개발 저장소에 둡니다. 공개 콘텐츠에는 공식 URL·서지·판본·해시 등 필요한 출처 메타데이터만 유지합니다.

## 로컬 사용

Obsidian에서 저장소 루트를 보관함으로 열고 `HOME.md`에서 시작합니다. 템플릿 폴더는 `templates`, 공개 가능한 자체 제작 첨부 폴더는 `attachments`입니다.

Python 3.12 이상, Node.js 22 이상, npm 10.9.2 이상을 사용합니다. Windows에서는 `npm.cmd`로 실행할 수 있습니다.

```sh
python -m pip install -r requirements.txt
npm --prefix site ci
python scripts/kb.py build
python scripts/source_registry.py
python scripts/validate_kb.py .
python -m unittest discover -s tests -v
npm --prefix site run build
npm --prefix site run preview
```

미리보기는 `http://localhost:8080`입니다. 공개 저장소만 있어도 검증·빌드가 가능하며 비공개 원문 파일을 읽지 않습니다. 빌드 전후에 공개 경계를 검사합니다. 이전 `original-search` 주소는 공식 원문 이용 안내로 유지합니다.

생성기 폴더에서 `python -m kb_generator doctor ../gridex-power-policy-kb --json`으로 두 저장소의 구조와 GRIDEX 검증기를 확인합니다. 기존 저장소에 `init --force`를 실행하지 않습니다.

## 공개와 검수

검색은 공개 요약·제목·주제·국가·관할·시장·언어·판본을 사용합니다. 원문은 발행기관 링크에서 확인합니다. 초안/확정·시행일·주장 근거수준·사람 검수 상태를 별도로 유지합니다. 근거수준의 명시적 검토가 없는 문서에는 `Unverified`를 사용합니다.

변경은 branch/PR에서 검토합니다. 공개 사이트 배포는 검증 후 별도로 수행하며 `python scripts/publish-pages.py`도 공개 경계 검사를 통과해야 합니다. 과거 Git 이력 및 이미 게시된 사이트의 정리는 현재 작업본 전환과 별개입니다. 이 재구성은 과거 이력을 재작성하지 않습니다.

검증 workflow는 `docs/workflows/validate.yml`에 준비했습니다. 현재 GitHub OAuth 인증에 workflow 권한이 없어 등록이 거절됐으므로 자동 CI는 아직 활성화되지 않았습니다. 해당 권한으로 `.github/workflows/validate.yml`에 등록하면 같은 검증·테스트·빌드를 PR에서 실행합니다.

신규 코드에는 [MIT License](LICENSE)를 적용합니다. 제3자 원문·이미지·인용에는 적용하지 않습니다. Quartz 라이선스와 [upstream 기록](site/UPSTREAM.md)을 보존합니다.
