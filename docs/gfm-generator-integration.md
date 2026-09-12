# GRIDEX × Knowledge Base Generator

기준은 [UPTEC-KOREA/knowledge-base-generator 5fff214](https://github.com/UPTEC-KOREA/knowledge-base-generator/tree/5fff2140909089a85cdb5bd92b24db2ee1e44418)입니다. 실제 CLI 버전은 0.3.0이며 공개/비공개 저장소 정책을 기존 Quartz KB에 적용합니다.

정책 47건과 GFM 노트 61개의 경로·ID·검토일을 유지합니다. `project.yaml`, `HOME.md`, `hubs/`, `taxonomy/`, `data/source-registry.yaml`, `scripts/validate_kb.py`를 연결하고 원문 파일·추출 전문·수집기·운영 기록은 개발 저장소로 이관합니다. 공개 저장소만으로 검증·사이트 빌드가 가능합니다.

## 검증

```sh
python scripts/kb.py build
python scripts/gfm_audit.py --as-of 2026-09-12 --write
python scripts/source_registry.py
python scripts/validate_kb.py .
python -m unittest discover -s tests -v
npm --prefix site run build
```

생성기 폴더에서 `python -m kb_generator doctor ../gridex-power-policy-kb --json`을 실행하면 두 저장소의 필수 경로와 GRIDEX 검증기를 확인합니다. 전체 GFM 감사 결과는 개발 저장소 `project/audits/`에 보관하고 공개 projection만 이 저장소에 생성합니다.

## 메타데이터 연결

| 기존 필드 | 생성기 필드 | 규칙 |
| --- | --- | --- |
| 정책 문서 ID | `source_ids: [SRC-POLICY-<ID>]` | 기존 `source_id` 기관 키와 구분 |
| `published_date` / `publication_date` | `published` | 원래 날짜 정밀도 유지 |
| `effective_date` | `effective` | 미상은 null |
| `last_verified_date` / `verified_on` | `last_verified` | 이전일·실행일로 덮어쓰지 않음 |
| `document_stage` | `status` | 초안·확정·공식 보조자료 구분 유지 |
| 주장 근거수준 미배정 | `Unverified` | 공식 URL만으로 Confirmed 승격 금지 |
| 기존 문서 간 순서 | 기존 previous/next 유지 | supersedes 관계로 자동 해석하지 않음 |

정책 노트에는 공통 필드를 추가하고 기존 도메인 필드를 유지합니다. GFM은 원래 필드를 읽는 비파괴 어댑터를 사용합니다. 통합 레지스트리 74개는 두 범주의 출처 레코드 수이며 고유 공식 문서의 중복 제거 집계가 아닙니다.

`Confirmed`에는 주장 범위·locator·실제 검토 기록이 필요합니다. 정책의 주장별 locator 배정과 GFM 근거수준 경고는 후속 검수로 남아 있습니다.

## 운영 경계

GCP Level 0을 유지합니다. 수집·연구·Vertex/API·배포 예약은 미활성입니다. 변경은 branch/PR에서 검토하며 공개 사이트 배포는 별도 단계입니다. 과거 공개 Git 이력에 남은 원문은 일반 파일 삭제로 없어지지 않으며 이번 변경은 이력을 재작성하지 않습니다.
