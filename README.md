# GRIDEX Power Policy Knowledge Base

대한민국 전력정책의 **공식 원문을 연결하는 Markdown Knowledge Base**입니다. PDF를 내려받지 않아도 정책의 맥락·수치·변화·연관 문서를 탐색할 수 있도록 만듭니다.

[공개 Knowledge Base](https://uptec-khj.github.io/gridex-power-policy-kb/) · [개발 로드맵](content/project/roadmap.md) · [문서 표준](docs/frontmatter-standard.md) · [자료 확보 현황](content/collection-status.md) · [작성 템플릿](templates/policy-document.md)

## 현재 범위

공식 자료 **37건**을 연결했습니다. 전력수급·송변전계획 전문, 수요전망, 수립위원회·환경평가·공청회·토론회 자료와 기관 사보 해설을 포함합니다. 탐색 허브, 동일 문서의 PDF/HWP 형식 차이는 별도 문서로 세지 않습니다. 원본 첨부 36개를 SHA-256으로 보존했습니다.

조사 기준일은 **2026-09-09**입니다. 제12차 제7차 토론회 공지(9월 18일 개최 예정)까지 확인했고, 제10·11차 장기 송변전설비계획 전문을 확보했습니다. 제11차 최초 공고 PDF와 제12차 2026년 5월 수요 잠정안 원표를 추가 확보했습니다. 일부 산업부 첨부, 제12차 후속 수요 재전망과 토론회 실제 발표자료는 추가 수집 대상입니다. 조사 경로에서 제12차 확정본은 확보하지 못했으며, 전체 공개자료의 완전한 목록을 뜻하지 않습니다.

30~50건이라는 MVP 수집 규모의 하한은 달성했습니다. **사람이 검수한 콘텐츠로의 전환은 남은 작업**입니다.

현재 `source_verified`는 공식 출처 확인을 의미합니다. **AI 요약에 대한 사람의 검수는 아직 완료되지 않았습니다.** 제11차 최초 공고와 수정 공고, 안내문의 예정일과 실제 개최 결과를 구분합니다.

재생에너지 기술 범위도 포함합니다. [기술 문서](content/technical-documents.md)에서 한전 현장시험 부록, KPX 시행 안내, 계통해석 모델 규정 개정안을 읽을 수 있습니다. 기준 전문과 발췌본, 현행 문서와 개정 예정안을 구분하고 차수가 없는 기술 문서에는 null을 사용합니다. [기술 문서 템플릿](templates/technical-document.md)과 [검수 대기 목록](content/project/review-queue.md)을 제공합니다.

[에너지·재생에너지 계획](content/energy-renewable-plans.md)에 제3차 에너지기본계획(2019~2040), 제5차 신재생에너지 기본계획(2020~2034), 제1차 재생에너지 기본계획(2026~2035) 전문을 추가했습니다. 과거 계획의 목표와 현행 정책을 구분하고, 검색은 차수와 계획 계열을 함께 사용합니다.

## 구성

[국가별 확장 로드맵](content/project/international-roadmap.md)의 G1을 구현했습니다. 대한민국·호주·미국·중국·유럽 메뉴와 [국가별 문서 찾기](content/document-search.md), PDF 원문 검색의 관할·시장·언어·종류 필터를 제공합니다. 기존 국내 37건은 v1.1 표준으로 이관했으며 본문·원본·출처·관계를 보존했습니다. [국제 자료원 후보](sources/international-candidates.yaml) 11개는 **비활성 설계 목록**입니다. 해외 메뉴는 0건·수집 준비 중으로 표시하며, 실제 해외 수집·정기 실행은 G2 이후 진행합니다.

```text
content/                  Obsidian Markdown: 유일한 콘텐츠 편집 원본
  documents/              안정적인 ID를 파일명으로 쓰는 공식 자료 노트
  plans/                  10·11·12차 탐색 허브
  regions/                국가별 문서 목록과 수집 준비 상태 (자동 생성)
  document-search.md      제목·주제·관할·언어별 문서 찾기
  project/                개발 로드맵·백로그·개발 기록
  original-search.md      공식 PDF 페이지 검색
  extraction-status.md    자동 생성한 PDF 추출 현황
  index.md                공개 KB 첫 화면
  catalog.md, timeline.md  Markdown에서 생성한 문서 목록·연표
templates/                Obsidian 정책문서 작성 양식
sources/                  기관 Registry·수집 대상·확보 대기 목록
collector/                공식 게시물·첨부 수집, 기관별 링크 해석
data/
  raw/sha256/             해시 기반 원본 PDF/HWP/HWPX·HTML 보존
  metadata/               수집 이력·문서 목록·관계·Timeline JSON
  extracted/              향후 추출 중간 산출물·캐시, Git 제외
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

미리보기 주소는 `http://localhost:8080`입니다. Quartz가 `../content`를 직접 읽으므로 Markdown 복사본을 만들지 않습니다. 검색, 태그, 백링크, 관계 그래프, 목차가 포함됩니다. `npm run build`와 `preview`의 선행 단계에서 보존 PDF의 원문 색인·추출 현황을 재생성합니다. 공개 사이트의 `original-search`에서 차수·단계별 PDF 페이지 검색을 사용할 수 있습니다. 공개 사이트 생성물은 `site/public/`이며 Git에는 커밋하지 않습니다.

## 공식 자료 수집

```sh
python -m collector
python -m collector --id p11-amend --refresh
```

수집기는 `sources/seed-documents.yaml`에 등록한 대상만 방문합니다. KPX·산업부·기후부·한전 첨부 링크를 공식 HTML에서 해석하고, 리디렉션도 Registry 도메인 안에서만 허용합니다. 파일 형식과 SHA-256을 확인한 뒤 `data/raw/sha256/`에 보존합니다. TLS 검증을 끄지 않습니다.

HTML 오류를 PDF로 저장하지 않습니다. 다운로드 실패는 `data/metadata/acquisitions.json`에 남고 종료코드 1을 반환합니다. 부분 성공도 유지하며 `--refresh`는 과거 획득 기록을 history에 보존합니다. 수집기는 편집된 Markdown을 덮어쓰거나 정책 요약을 자동 확정하지 않습니다. 새 수집 결과는 원문 대조 후 문서 Frontmatter와 본문 첨부 목록에 반영합니다.

원본은 내용 해시로 중복 제거합니다. 동일 URL의 파일이 바뀌면 새 해시로 보존합니다. 대용량 자료가 늘어나면 Git LFS 또는 별도 아카이브로 확장하되 URI·해시·획득 이력은 저장소에 남깁니다. 원본 첨부는 Quartz 페이지에 복제하지 않고 공식 URL과 GitHub 보존본으로 연결합니다.

## 검색과 RAG

```sh
python scripts/kb.py build
python scripts/kb.py search "11차 전력수요"
python scripts/kb.py search "전력수요" --verified-only
python scripts/originals.py build
python scripts/originals.py search "송변전 61183" --plan 11 --stage final
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


## 개발 관리

Obsidian에서 [개발 로드맵](content/project/roadmap.md)을 열고 [백로그](content/project/development-backlog.md), [개발 기록](content/project/release-log.md)을 함께 사용합니다. 새 작업에는 [development-task 템플릿](templates/development-task.md)을 적용합니다. 플러그인 없이 Frontmatter·체크박스·Wiki Link로 동작하며 Quartz에서도 공개됩니다.

## 원문 검색의 범위

`ai/index/official-pages.jsonl`은 PDF의 물리적 페이지 단위 추출 텍스트입니다. `ai/index/chunks.jsonl`의 AI 편집 요약과 분리합니다. 원본 SHA-256, 첨부 URL, PDF 쪽수, 차수·단계, 추출 도구 버전을 보존합니다. 표 구조·인쇄 쪽수·OCR 정확도를 추정하지 않습니다. PDF가 없는 문서와 텍스트가 없거나 적은 페이지는 [추출 현황](content/extraction-status.md)에 표시합니다.

공개 검색 색인 `site/quartz/static/official-pages.json`은 매 빌드에 생성하는 파생 파일이므로 Git에서 제외합니다. HTML 출력과 함께 GitHub Pages에 배포됩니다. 검색어를 서버나 생성형 AI에 전달하지 않으며, 여러 단어는 AND 조건으로 검색합니다. 의미 검색과 생성형 답변은 후속 단계입니다.
