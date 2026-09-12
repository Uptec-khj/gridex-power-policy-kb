# GFM × Knowledge Base Generator 연동

기준: [knowledge-base-generator c74f662](https://github.com/Uptec-khj/knowledge-base-generator/tree/c74f6625f2f570c2f68a748c26477e7634f718da), 실제 CLI 0.3.0. 기존 Markdown을 재생성하지 않는 Level 0 메타데이터 연동이다. GCP/API/자동 수집/자동 배포를 활성화하지 않는다.

[개발 적용 로드맵](https://github.com/Uptec-khj/gridex-power-policy-kb-dev/blob/main/content/generator-integration-roadmap.md) · [공개 GFM 홈](../content/gfm/00_Home/Home.md)

## 실행

```sh
python scripts/gfm_audit.py --as-of 2026-09-11
python -m unittest discover -s tests -p 'test_gfm_audit.py' -v
python scripts/gfm_audit.py --as-of 2026-09-11 --write
```

기본 명령은 파일을 변경하지 않는다. `--write`는 검증 오류가 없을 때만 `data/gfm/source-registry.json`, `data/gfm/metadata-audit.json`을 재생성한다. 생성 JSON을 직접 편집하지 않는다. 첫 파일은 [스키마](../schemas/gfm-source-registry.schema.json)로 검증한다. 전체 정책 검증 `python scripts/kb.py validate`와 GFM 검증은 서로 보완하며 대체하지 않는다.

생성기 실제 감사기를 함께 실행하려면 별도 위치에 해당 커밋의 깨끗한 checkout을 준비한다.

```sh
python scripts/gfm_audit.py --as-of 2026-09-11 --generator-root ../knowledge-base-generator --write
```

어댑터는 고정 SHA·깨끗한 작업 트리를 확인하고 일시 폴더에 **서지 메타데이터만** 투영한 후 `python -m kb_generator audit`를 실행한다. 원문·요약 본문은 복제하지 않는다. 결과의 임시 경로는 저장하지 않고 임시 폴더는 실행 종료 시 정리한다. 평소 감사에는 생성기 설치가 필요 없다.

## 필드 연결

| 기존 GFM | 생성기 호환 projection | 보존 원칙 |
|---|---|---|
| id / title_ko | id / title | ID와 원본 경로·SHA-256 유지 |
| publication_date | published | 년/월/일 정밀도 유지; 누락 날짜 추정 금지 |
| effective_date | effective | null 유지; 예정일을 확정일로 전환 금지 |
| verified_on | last_verified | 실행일로 덮어쓰지 않음 |
| 원문노트 id | source_ids | 서지 레코드 자기참조이며 주장 입증을 의미하지 않음 |
| document_status / applicability | source_metadata에 원형 보존 | 초안/확정과 적용 성격 분리; 공통 active로 강제 변환하지 않음 |
| access_status / redistribution / license | source_metadata에 원형 보존 | 공개 열람과 재배포 허용 분리 |
| evidence_level 미기재 | Unverified + not_assessed | 기존 원문 검토를 부정하는 의미가 아니라 생성기 근거수준의 명시적 범위 배정이 아직 없다는 뜻 |
| relevant_clauses_pages / review_status | source_metadata에 원형 보존 | 서지 검토·부분 조항·전문 검토 범위 유지 |
| approval_date / facility_cutoff_date | source_metadata에 원형 보존 | 승인일·설비 적용 기준일·시행일 혼합 금지 |

`Confirmed`를 명시하려면 최소 evidence_scope, 검토일, locator가 필요하다. 자동 검사는 필드 존재만 확인한다. 해당 출처가 실제 주장을 입증하는지와 사람 검수 완료는 별도 판단이다. 원문이 초안인 상태에서 조항 존재를 Confirmed로 검토하더라도 법적 효력은 초안이다.

## 검사 범위와 종료코드

- 오류(종료코드 1): 빈 Vault, YAML 파싱, 필수 source 필드, 중복 ID, 잘못된 날짜, 미래 검토일, 잘못된 URL 형식, 내부 파일 링크, 출처 ID 참조, GFM 영역의 Markdown 외 파일·심볼릭 링크.
- 경고(종료코드 0, `NEEDS_REVIEW`): 명시적 evidence level 미배정, 검토일/locator 누락, 90일 초과 검토일, 재배포 미확인, 이용조건 URL이 기관 홈페이지인 경우.
- 미실시: 외부 링크 실접속, Markdown 앵커 검사, 원문 사실 재검증, 시험 동등성 판정, 권리 승인, 사람 검수, 사이트 배포.

기존 GFM source 27건의 공개 링크와 자체 노트는 유지된다. 문서 수가 늘어났다고 주장하지 않는다. GFM 외 정책 47건은 다른 스키마와 검증 흐름을 유지하고 합계·중복을 자동 통합하지 않는다.

## 금지 및 다음 단계

운영 저장소에 `kbgen init --force`, `kbgen github --execute`를 실행하지 않는다. 생성기의 기본 doctor는 신규 scaffold를 대상으로 하므로 GRIDEX에서 그 필수경로를 만족시키기 위해 운영 파일을 복제하지 않는다. GFM 원문 PDF·OCR·전문 번역·임베딩을 기존 정책 원문 파이프라인에 자동 투입하지 않는다.

다음 단계는 GF3a: claim ID, source ID/판본/locator, 값·단위·적용 및 경과조건, 시험 조건, evidence type을 갖는 최소 3개 사례와 유보 판정 검증이다. KSGA 개정단계·한전 확정본/시험 부록·KPX 후속 시험규정 미확보는 별도의 evidence gap으로 유지한다.
