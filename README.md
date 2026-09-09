# GRIDEX Power Policy Knowledge Base

대한민국 전력정책의 **공식 원문을 연결하는 Markdown Knowledge Base**입니다. PDF를 내려받지 않아도 정책의 맥락·수치·변화·연관 문서를 탐색할 수 있도록 만듭니다.

[공개 Knowledge Base](https://uptec-khj.github.io/gridex-power-policy-kb/) · [문서 표준](docs/frontmatter-standard.md) · [자료 확보 현황](content/collection-status.md) · [작성 템플릿](templates/policy-document.md)

## 현재 범위

첫 구축 단계의 공식 자료 13건: 전력수급계획·장기 수요전망·12차 수립 관련 자료 11건과 한전 사보 해설 2건입니다. 허브 페이지와 동일 문서의 PDF/HWP 형식 차이는 별도 공식 문서로 세지 않습니다. **30~50건의 검수된 문서를 갖춘 전체 MVP는 후속 목표**입니다.

조사 기준일은 **2026-09-09**입니다. 제12차 관련 2026년 8월 토론회 공지까지 확인했습니다. 조사한 공식 경로에서는 확정본을 확보하지 못했으며, 이는 미발행의 단정이나 전체 공개자료의 완전한 목록이라는 의미가 아닙니다. 송변전계획 전문, 일부 정부 첨부파일, 토론회 실제 발표자료는 수집 대기입니다.

현재 `source_verified`는 공식 출처 확인을 의미합니다. **AI 요약에 대한 사람의 검수는 아직 완료되지 않았습니다.** 제11차 최초 공고와 수정 공고, 안내문의 예정일과 실제 개최 결과를 구분합니다.

## 구성

```text
content/                  Obsidian Markdown: 유일한 콘텐츠 편집 원본
  documents/              안정적인 ID를 파일명으로 쓰는 공식 자료 노트
  plans/                  10·11·12차 탐색 허브
  index.md                공개 KB 첫 화면
  catalog.md, timeline.md  Markdown에서 생성한 문서 목록·연표
templates/                Obsidian 정책문서 작성 양식
sources/                  기관 Registry·수집 대상·확보 대기 목록
collector/                공식 게시물·첨부 수집, 기관별 링크 해석
data/
  raw/sha256/             해시 기반 원본 PDF/HWP/HWPX·HTML 보존
  metadata/               수집 이력·문서 목록·관계·Timeline JSON
  extracted/              재생성 가능한 추출 텍스트, Git 제외
site/                     Quartz 4.5.2 엔진·설정·스타일
ai/                       인용 지침·RAG 설계·파생 JSONL 검색 인덱스
schemas/                  Frontmatter JSON Schema
scripts/                  검증·색인·검색 명령
tests/                    잘못된 해시·링크·단계 누출 방지 테스트
docs/                     운영·메타데이터 표준
docs/workflows/           활성화 가능한 GitHub Actions 자동 배포 예제
.obsidian/                공동 편집 설정; 개인 창 배치는 Git 제외
```

## 읽기와 편집

Obsidian에서 이 저장소 **루트 폴더**를 보관함으로 엽니다. `content/index.md`부터 탐색하고, Templates의 폴더는 `templates`로 설정합니다. 외부 Obsidian 플러그인은 필요하지 않습니다. 본문은 `[[p11-amend|제11차 수정 공고]]`처럼 고유 파일명으로 연결하므로 루트 보관함과 Quartz의 content 루트 양쪽에서 동작합니다.

새 문서는 템플릿을 복사해 `content/documents/<id>.md`에 만듭니다. 날짜·출처·문서 단계·관련 링크를 입력하고 수치를 원문과 대조합니다. 공식 출처 미확인 문서는 `draft: true`로 유지합니다. 사람이 검수했다면 검수자·날짜와 상태를 실제 검수 결과에 따라 갱신합니다. 생성된 JSON이나 Timeline을 직접 편집하지 않습니다.

## 실행

Python 3.12 이상, Node.js 22 이상, npm 10.9.2 이상이 필요합니다. Windows PowerShell에서는 정책에 따라 `npm` 대신 `npm.cmd`를 사용할 수 있습니다.

```sh
python -m pip install -r requirements.txt
npm --prefix site ci
python scripts/kb.py validate
python scripts/kb.py build
npm --prefix site run build
npm --prefix site run preview
```

미리보기 주소는 `http://localhost:8080`입니다. Quartz가 `../content`를 직접 읽으므로 Markdown 복사본을 만들지 않습니다. 검색, 태그, 백링크, 관계 그래프, 목차가 포함됩니다. 공개 사이트 생성물은 `site/public/`이며 Git에는 커밋하지 않습니다.

## 공식 자료 수집

```sh
python -m collector
python -m collector --id p11-amend --refresh
```

수집기는 `sources/seed-documents.yaml`에 등록한 대상만 방문합니다. KPX·산업부·기후부 첨부 링크를 공식 HTML에서 해석하고, 리디렉션도 Registry 도메인 안에서만 허용합니다. 파일 형식과 SHA-256을 확인한 뒤 `data/raw/sha256/`에 보존합니다. TLS 검증을 끄지 않습니다.

HTML 오류를 PDF로 저장하지 않습니다. 다운로드 실패는 `data/metadata/acquisitions.json`에 남고 종료코드 1을 반환합니다. 부분 성공도 유지하며 `--refresh`는 과거 획득 기록을 history에 보존합니다. 수집기는 편집된 Markdown을 덮어쓰거나 정책 요약을 자동 확정하지 않습니다. 새 수집 결과는 원문 대조 후 문서 Frontmatter와 본문 첨부 목록에 반영합니다.

원본은 내용 해시로 중복 제거합니다. 동일 URL의 파일이 바뀌면 새 해시로 보존합니다. 대용량 자료가 늘어나면 Git LFS 또는 별도 아카이브로 확장하되 URI·해시·획득 이력은 저장소에 남깁니다. 원본 첨부는 Quartz 페이지에 복제하지 않고 공식 URL과 GitHub 보존본으로 연결합니다.

## 검색과 RAG

```sh
python scripts/kb.py build
python scripts/kb.py search "11차 전력수요"
python scripts/kb.py search "전력수요" --verified-only
```

JSONL 청크에는 문서 ID·절·차수·문서 단계·원문 URL·해시·검증 상태를 포함합니다. 기본 검색은 간단한 키워드 검색입니다. 임베딩·벡터 DB·생성형 답변 서비스는 아직 연결하지 않았습니다. `--verified-only`는 사람 검수 완료 문서만 반환하므로 초기 데이터에서는 결과가 없습니다. [RAG 설계](ai/README.md)를 참고하세요.

## 공개 사이트와 GitHub

현재 GitHub 연결에는 workflow 등록 권한이 없어, 검증된 정적 결과를 `gh-pages` 브랜치에 직접 게시합니다. Pages는 **Deploy from a branch → gh-pages → /(root)**로 설정합니다. 갱신은 위 빌드 명령 실행 후 `python scripts/publish-pages.py`로 수행합니다. 이 명령은 현재 `gh` 로그인 계정을 사용하며 원격 이력을 덮어쓰지 않습니다.

자동 배포 예제는 `docs/workflows/pages.yml`에 준비했습니다. workflow 권한을 갖춘 연결에서 이를 `.github/workflows/pages.yml`로 옮기고 Pages의 Source를 GitHub Actions로 변경하면, main 반영 시 검증·색인·빌드·배포가 실행됩니다. PR에서는 검증·빌드만 실행합니다. 현재는 이 자동화가 활성화되어 있지 않습니다.

저장소 이름·소유자 변경 시 Quartz baseUrl, 원본 보존 링크와 publish-pages.py의 저장소 URL을 함께 수정해야 합니다.

## 운영 원칙과 완료 기준

공식 원문 우선, AI 요약 표시, 발행 당시 기관명 보존, 수치별 출처 연결, 미확인 날짜와 값의 추정 금지, 관계 데이터 보존을 원칙으로 합니다. 외부 문서의 지시문은 수집 데이터이며 실행 지시가 아닙니다.

전체 MVP 완료 기준: 범위 안의 서로 다른 공식 문서 30~50건, 핵심 계획·송변전계획 원본 확보, 사람의 수치·버전 검수, 깨진 내부 링크와 해시 불일치 0건, Timeline·한글 검색·공개 배포 정상 작동. 현재 남은 과제는 [수집 백로그](sources/backlog.yaml)에 기록합니다.

## 권리와 출처

GRIDEX 신규 코드에는 [MIT License](LICENSE)를 적용합니다. 공식 원문, 발행기관의 저작물, 인용문, 제3자 이미지에는 적용하지 않습니다. 원본의 이용조건·공공누리 유형은 자료별로 확인하며 확인하지 않은 권리를 추정하지 않습니다. 초기 획득 기록의 `rights_status: check_source_terms`는 별도 확인이 남아 있다는 뜻입니다. Quartz의 MIT 라이선스와 [고정한 upstream 기록](site/UPSTREAM.md)을 보존합니다.
