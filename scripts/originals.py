"""Build page-level PDF evidence, or search it without an external API.

python scripts/originals.py build
python scripts/originals.py search "송변전 61,183" --plan 11 --stage final
"""
import argparse
import hashlib
import io
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urldefrag

import pypdf
from pypdf import PdfReader

try:
    from . import kb
except ImportError:
    import kb

ROOT = Path(__file__).resolve().parents[1]
ENGINE = f"pypdf/{pypdf.__version__}:layout-v1"


def eligible(meta):
    return not meta.get("draft") and meta.get("verification_status") in ("source_verified", "human_verified")


def sparse_text(text):
    # A review cue, not a diagnosis: covers and image posters can both be sparse.
    return bool(text.strip()) and len(re.sub(r"\s", "", text)) < 80


def extract_pdf(payload):
    """Keep physical pages intact. Never infer printed page numbers or table cells."""
    reader = PdfReader(io.BytesIO(payload))
    result = []
    for number, page in enumerate(reader.pages, 1):
        text = page.extract_text(extraction_mode="layout", layout_mode_strip_rotated=False) or ""
        result.append({"pdf_page": number, "printed_page": None, "text": text.strip(),
                       "extraction_status": "text_extracted" if text.strip() else "empty_or_image"})
    return result


def build_evidence(records, root=ROOT):
    pages, files, missing, cache = [], [], [], {}
    public = [meta for _, meta, _ in records if eligible(meta)]
    # Validate every selected byte stream before producing any derivative files.
    for meta in public:
        pdfs = [a for a in meta.get("attachments", []) if a["format"] == "pdf"]
        if not pdfs:
            missing.append(meta["id"])
        for attachment in pdfs:
            raw = (root / attachment["path"]).resolve()
            if not raw.is_relative_to((root / "data/raw").resolve()):
                raise ValueError("Unsafe original path")
            payload = raw.read_bytes()
            digest = "sha256:" + hashlib.sha256(payload).hexdigest()
            if digest != attachment["file_hash"]:
                raise ValueError(f"Original hash mismatch: {meta['id']}")
            if not payload.startswith(b"%PDF-"):
                raise ValueError(f"Not a PDF: {meta['id']}")
            if digest not in cache:
                try:
                    cache[digest] = {"pages": extract_pdf(payload)}
                except Exception as exc:
                    # Preserve the failure visibly; no fabricated or silently omitted pages.
                    cache[digest] = {"pages": [], "error": f"{type(exc).__name__}: {exc}"}
            extracted = cache[digest]
            files.append({"document_id": meta["id"], "title": attachment["title"], "file_hash": digest,
                          "page_count": len(extracted["pages"]),
                          "empty_pages": [p["pdf_page"] for p in extracted["pages"] if not p["text"]],
                          "sparse_pages": [p["pdf_page"] for p in extracted["pages"] if sparse_text(p["text"])],
                          "status": "failed" if "error" in extracted else "extracted",
                          "error": extracted.get("error")})
            for page in extracted["pages"]:
                pages.append({"chunk_id": f"{meta['id']}:{digest[7:]}:p{page['pdf_page']}",
                    "document_id": meta["id"], "title": meta["title"],
                    "attachment_title": attachment["title"], "slug": "documents/" + meta["id"],
                    "content_origin": "official_extraction", "extraction_engine": ENGINE,
                    "extraction_review_status": "unreviewed", "ocr_performed": False,
                    "sparse_text": sparse_text(page["text"]),
                    "verification_status": meta["verification_status"],
                    "source_url": meta["source_url"], "attachment_url": attachment["url"],
                    "citation_url": urldefrag(attachment["url"])[0] + f"#page={page['pdf_page']}",
                    "archive_url": "https://github.com/Uptec-khj/gridex-power-policy-kb/blob/main/" + attachment["path"],
                    "file_hash": digest, "plan_family": meta["plan_family"], "plan_number": meta["plan_number"],
                    "category": meta.get("category"), "technical": meta.get("technical"),
                    "document_stage": meta["document_stage"], "published_date": meta["published_date"], **kb.international_metadata(meta), **page})
    pages.sort(key=lambda p: (p["document_id"], p["file_hash"], p["pdf_page"]))
    report = {"schema_version": "1.0", "extraction_engine": ENGINE,
              "document_count": len(public), "documents_with_pdf": len({f["document_id"] for f in files}),
              "unique_pdf_count": len(cache), "page_records": len(pages),
              "searchable_pages": sum(bool(p["text"]) for p in pages),
              "empty_pages": sum(not p["text"] for p in pages),
              "sparse_pages": sum(p["sparse_text"] for p in pages),
              "failed_files": sum(f["status"] == "failed" for f in files),
              "documents_without_pdf": sorted(missing), "files": files}
    return pages, report


def write_atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8")
    temp.replace(path)


def build():
    records = kb.validate()
    pages, report = build_evidence(records)
    write_atomic(ROOT / "ai/index/official-pages.jsonl", "".join(json.dumps(p, ensure_ascii=False) + "\n" for p in pages))
    write_atomic(ROOT / "data/metadata/extraction-report.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    write_atomic(ROOT / "site/quartz/static/official-pages.json", json.dumps({"report": report, "pages": pages}, ensure_ascii=False))
    rows = ['---', 'title: 원문 텍스트 추출 현황', 'tags: [안내, 원문검색]', '---', '',
        '> 보존 PDF에서 자동 추출한 텍스트의 처리 현황입니다. AI 요약 검수나 표 구조 검증 완료를 의미하지 않습니다.', '',
        f"공식 자료 {report['document_count']}건 중 {report['documents_with_pdf']}건에 PDF가 있습니다. 고유 PDF {report['unique_pdf_count']}개에서 {report['page_records']}개 페이지 기록을 만들었고, {report['searchable_pages']}개 페이지에 검색 가능한 텍스트가 있습니다.", '',
        f"텍스트가 없는 페이지 {report['empty_pages']}개, 텍스트가 적은 페이지 {report['sparse_pages']}개입니다. 텍스트가 적다는 표시는 공백 제외 80자 미만이라는 휴리스틱이며 표지·이미지·간단한 페이지를 구별하지 않습니다. 제목만 추출되고 포스터·표의 글자가 누락될 수도 있으므로 모든 내용이 검색된다는 뜻은 아닙니다. OCR은 수행하지 않았습니다. 파일 처리 실패: {report['failed_files']}개.", '',
        '## PDF별 현황', '', '| 문서 | PDF 쪽수 | 텍스트 없는 쪽 | 텍스트 적은 쪽 | 상태 |', '| --- | --- | --- | --- | --- |']
    rows += [f"| [[{f['document_id']}]] · {f['title'].replace('|', '/')} | {f['page_count']} | {', '.join(map(str, f['empty_pages'])) or '없음'} | {', '.join(map(str, f['sparse_pages'])) or '없음'} | {f['status']} |" for f in report['files']]
    rows += ['', '## PDF 미확보 문서', '', '공식 HTML만 보존했거나 PDF 첨부를 확보하지 못한 문서입니다. 원문 검색 대상에는 포함되지 않습니다.', '']
    rows += [f"- [[{key}]]" for key in report['documents_without_pdf']]
    rows += ['', '[[original-search|원문 검색]] · [[collection-status|자료 확보 현황]] · [[reading-guide|이용 안내]]', '']
    write_atomic(ROOT / "content/extraction-status.md", '\n'.join(rows))
    print(f"PDF evidence: {report['unique_pdf_count']} files, {report['searchable_pages']} searchable pages, {report['empty_pages']} empty pages, {report['failed_files']} failures")
    return report


def normalize(text):
    text = unicodedata.normalize("NFKC", text).casefold()
    return re.sub(r"\s+", "", re.sub(r"(?<=\d),(?=\d)", "", text))


def search_pages(pages, query, plan=None, stage=None, limit=10, family=None,
                 region=None, jurisdiction=None, language=None, document_type=None, market=None):
    terms = [normalize(t) for t in query.split() if normalize(t)]
    if not terms:
        return []
    ranked = []
    for p in pages:
        if not p['text'] or (plan is not None and p['plan_number'] != plan) or (stage and p['document_stage'] != stage):
            continue
        if family and p.get('plan_family') != family:
            continue
        if ((region and p.get('region_group') != region) or
            (jurisdiction and jurisdiction not in (p.get('jurisdictions') or [])) or
            (market and market not in (p.get('market_regions') or [])) or
            (language and p.get('document_language') != language) or
            (document_type and p.get('document_type') != document_type)):
            continue
        title, body = normalize(p['title'] + ' ' + (p.get('title_original') or '')), normalize(p['text'])
        if all(t in title or t in body for t in terms):
            score = sum((3 if t in title else 0) + (1 if t in body else 0) for t in terms)
            ranked.append((score, p))
    ranked.sort(key=lambda item: (-item[0], item[1]['document_id'], item[1]['file_hash'], item[1]['pdf_page']))
    return [p for _, p in ranked[:limit]]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('build')
    query = sub.add_parser('search')
    query.add_argument('query')
    query.add_argument('--plan', type=int, choices=[1, 2, 3, 4, 5, 10, 11, 12])
    query.add_argument('--stage')
    query.add_argument('--family')
    query.add_argument('--region')
    query.add_argument('--jurisdiction')
    query.add_argument('--language')
    query.add_argument('--document-type')
    query.add_argument('--market')
    query.add_argument('--limit', type=int, default=10)
    args = parser.parse_args()
    if args.command == 'build':
        if build()['failed_files']:
            raise SystemExit(1)
    else:
        path = ROOT / 'ai/index/official-pages.jsonl'
        if not path.exists():
            parser.error('Run build first')
        pages = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
        print(json.dumps(search_pages(pages, args.query, args.plan, args.stage, max(1, args.limit), family=args.family,
                                     region=args.region, jurisdiction=args.jurisdiction, language=args.language,
                                     document_type=args.document_type, market=args.market), ensure_ascii=False, indent=2))
