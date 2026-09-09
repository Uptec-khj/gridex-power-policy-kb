"""Validate the Markdown source of truth and build portable indexes.

Usage: python scripts/kb.py validate | build | search QUERY [--verified-only]
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse
import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
HEADINGS = ["기본정보", "3줄 요약", "핵심 내용", "핵심 수치", "주요 정책 변화", "Timeline", "관련 문서", "관련 법령", "원문 링크", "원본 첨부파일"]
WIKI = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


def read_note(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", text, re.S)
    if not match:
        raise ValueError(f"Missing frontmatter: {path}")
    meta = yaml.safe_load(match[1])
    return meta, match[2]


def notes():
    return [(p, *read_note(p)) for p in sorted((CONTENT / "documents").glob("*.md"))]


def target_id(link):
    found = WIKI.fullmatch(link)
    return Path(found[1]).stem if found else None


def validate(generating=False):
    schema = json.loads((ROOT / "schemas/policy-document.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    records = notes()
    known = {p.stem for p in CONTENT.rglob("*.md")}
    actual_basenames = set(known)
    if generating:
        known.update({"catalog", "timeline", "review-queue"})
    ids = {m["id"]: m for _, m, _ in records}
    registry = yaml.safe_load((ROOT / "sources/registry.yaml").read_text(encoding="utf-8"))["sources"]
    sources = {s["id"]: s for s in registry}
    errors = []
    if len(ids) != len(records):
        errors.append("Duplicate document IDs")
    if len(actual_basenames) != len(list(CONTENT.rglob("*.md"))):
        errors.append("Duplicate Markdown basenames: shortest wiki links would be ambiguous")
    for path, meta, body in records:
        for error in validator.iter_errors(meta):
            errors.append(f"{path.name}: {list(error.path)} {error.message}")
        if meta.get("id") != path.stem:
            errors.append(f"{path.name}: id must match filename")
        if re.findall(r"^## (.+)$", body, re.M) != HEADINGS:
            errors.append(f"{path.name}: requires the ten ordered sections")
        summary = body.split("## 3줄 요약\n")[-1].split("## 핵심 내용")[0]
        if len(re.findall(r"^\d\. ", summary, re.M)) != 3:
            errors.append(f"{path.name}: summary must have three numbered lines")
        if not meta.get("draft", False):
            if meta.get("verification_status") not in ("source_verified", "human_verified"):
                errors.append(f"{path.name}: public note needs a verified official source")
        if meta.get("verification_status") == "human_verified" and not (meta.get("reviewed_by") and meta.get("reviewed_date")):
            errors.append(f"{path.name}: human review identity and date required")
        source = sources.get(meta.get("source_id"))
        if not source or urlparse(meta["source_url"]).hostname not in source["allowed_domains"]:
            errors.append(f"{path.name}: source URL is not in its institution registry")
        if meta.get("published_date") and meta["published_date"] > meta["collected_date"]:
            errors.append(f"{path.name}: future publication date")
        for relation in meta.get("typed_relations", []):
            if relation["target"] not in meta.get("related_documents", []):
                errors.append(f"{path.name}: typed relation must also be a related document")
            if urlparse(relation["source_url"]).hostname not in {d for s in registry for d in s["allowed_domains"]}:
                errors.append(f"{path.name}: typed relation needs an official source")
        for link in meta.get("related_documents", []) + [v for v in (meta.get("previous_document"), meta.get("next_document")) if v]:
            tid = target_id(link)
            if tid not in ids or tid == meta["id"]:
                errors.append(f"{path.name}: invalid relationship {link}")
            if tid not in WIKI.findall(body):
                errors.append(f"{path.name}: relationship must also appear in body for Quartz graph: {link}")
        for direction, inverse in (("previous_document", "next_document"), ("next_document", "previous_document")):
            if meta.get(direction):
                tid = target_id(meta[direction])
                if tid in ids and target_id(ids[tid].get(inverse) or "") != meta["id"]:
                    errors.append(f"{path.name}: {direction} must be reciprocal")
        evidence = meta.get("attachments", []) + ([meta["source_snapshot"]] if meta.get("source_snapshot") else [])
        for item in evidence:
            raw = (ROOT / item["path"]).resolve()
            if not raw.is_relative_to((ROOT / "data/raw").resolve()) or not raw.is_file():
                errors.append(f"{path.name}: missing or unsafe original {item['path']}")
            elif "sha256:" + hashlib.sha256(raw.read_bytes()).hexdigest() != item["file_hash"]:
                errors.append(f"{path.name}: hash mismatch {item['path']}")
        if meta.get("attachment_url") and not any(a["url"] == meta["attachment_url"] and a["file_hash"] == meta.get("file_hash") for a in meta.get("attachments", [])):
            errors.append(f"{path.name}: primary attachment URL/hash mismatch")
        if meta.get("file_hash") and not meta.get("attachment_url"):
            errors.append(f"{path.name}: file_hash must refer to a primary attachment")
        for e in meta.get("events", []):
            if not e.get("source_url") or e["status"] not in ("publication", "scheduled", "confirmed"):
                errors.append(f"{path.name}: event provenance/status missing")
    for path in CONTENT.rglob("*.md"):
        if generating and path.name in ("catalog.md", "timeline.md", "review-queue.md"):
            continue
        for target in WIKI.findall(path.read_text(encoding="utf-8")):
            if Path(target).stem not in known:
                errors.append(f"{path.name}: unresolved wiki link {target}")
    if errors:
        raise ValueError("\n".join(errors))
    return records


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build():
    records = validate(generating=True)
    documents, edges, timeline, chunks = [], [], [], []
    for path, meta, body in records:
        if meta.get("draft") or meta["verification_status"] in ("unverified", "needs_review"):
            continue
        slug = "documents/" + path.stem
        documents.append({**meta, "path": path.relative_to(ROOT).as_posix(), "slug": slug})
        for relation in ("related_documents", "previous_document", "next_document"):
            values = meta[relation] if isinstance(meta[relation], list) else [meta[relation]] if meta[relation] else []
            edges.extend({"source": meta["id"], "target": target_id(link), "type": relation} for link in values)
        edges.extend({**r, "source": meta["id"], "target": target_id(r["target"]),
                      "interpretation_review_status": meta["summary_review_status"]}
                     for r in meta.get("typed_relations", []))
        timeline.extend({**e, "document_id": meta["id"], "title": meta["title"]} for e in meta.get("events", []))
        # Chunk Markdown at section/paragraph boundaries; never index the raw PDF as AI prose.
        for section in re.split(r"(?=^## )", body, flags=re.M):
            if not section.startswith("## "):
                continue
            heading, _, content = section.partition("\n")
            paragraphs = re.split(r"\n\s*\n", content.strip())
            groups, current = [], ""
            for paragraph in paragraphs:
                if len(current) + len(paragraph) > 1500 and current:
                    groups.append(current); current = ""
                current += ("\n\n" if current else "") + paragraph
            if current: groups.append(current)
            for i, text in enumerate(groups):
                chunks.append({"chunk_id": f"{meta['id']}:{heading[3:]}:{i}", "document_id": meta["id"],
                    "title": meta["title"], "section": heading[3:], "text": text, "slug": slug,
                    "content_origin": "ai_assisted_editorial", "verification_status": meta["verification_status"],
                    "summary_review_status": meta["summary_review_status"], "source_url": meta["source_url"],
                    "attachment_url": meta["attachment_url"], "file_hash": meta["file_hash"],
                    "plan_family": meta["plan_family"], "plan_number": meta["plan_number"],
                    "category": meta["category"], "technical": meta.get("technical"),
                    "document_stage": meta["document_stage"], "published_date": meta["published_date"],
                    "collected_date": meta["collected_date"], "topics": meta["topics"]})
    timeline.sort(key=lambda e: (e["date"], e["document_id"]))
    write_json(ROOT / "data/metadata/documents.json", documents)
    write_json(ROOT / "data/metadata/relations.json", edges)
    write_json(ROOT / "data/metadata/timeline.json", timeline)
    (ROOT / "ai/index").mkdir(parents=True, exist_ok=True)
    (ROOT / "ai/index/chunks.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in chunks), encoding="utf-8")
    rows = ["---", 'title: "정책 Timeline"', "tags: [안내, Timeline]", "---", "", "> Markdown의 사건 메타데이터에서 자동 생성합니다. ‘예정’은 해당 안내문 기준이며 실제 개최 확인을 뜻하지 않습니다.", "", "| 날짜 | 사건 | 구분 | 문서 | 근거 |", "| --- | --- | --- | --- | --- |"]
    labels = {"publication": "게시·공고", "scheduled": "안내문상 예정", "confirmed": "실제 발생 확인"}
    rows += [f"| {e['date']} | {e['label']} | {labels[e['status']]} | [[{e['document_id']}]] | [공식 출처]({e['source_url']}) |" for e in timeline]
    (CONTENT / "timeline.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    rows = ["---", 'title: "공식 문서 목록"', "tags: [안내]", "---", "", f"공식 자료 {len(documents)}건. 사보 해설은 계획 전문과 구분하며, AI 요약은 아직 사람의 검수를 거치지 않았습니다.", "", "| 문서 | 발행일 | 차수 | 문서 단계 | 검증 |", "| --- | --- | --- | --- | --- |"]
    rows += [f"| {m['title']} · [[{m['id']}]] | {m['published_date'] or '일자 미확인'} | {m['plan_number'] if m['plan_number'] is not None else '기술 문서'} | {m['document_stage']} | {'사람 검수 완료' if m['verification_status'] == 'human_verified' else '공식 출처 확인 · 요약 검수 대기'} |" for m in documents]
    (CONTENT / "catalog.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    pending = [m for m in documents if m['verification_status'] != 'human_verified' or m['summary_review_status'] != 'reviewed']
    rows = ['---', 'title: 콘텐츠 검수 대기 목록', 'tags: [프로젝트, 검수]', '---', '',
            'Markdown 검수 상태에서 자동 생성합니다. 사람 검수 양식은 저장소 templates/content-review.md를 사용합니다. 이 목록의 생성은 검수 완료를 뜻하지 않습니다.', '',
            '[[development-backlog|개발 백로그]] · [[technical-documents|기술 문서]] · [[collection-status|자료 확보 현황]]', '',
            f'검수 대기 {len(pending)}건. 출처·버전·적용 범위·수치/단위·쪽수·요약·이용조건을 대조하세요.', '',
            '| 문서 | 문서 단계 | 첨부 | 확인 범위와 남은 사항 |', '| --- | --- | --- | --- |']
    rows += [f"| [[{m['id']}]] | {m['document_stage']} | {len(m['attachments'])}개 | {m.get('verification_notes', '').replace('|', '/')} |" for m in pending]
    (CONTENT / 'project/review-queue.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')
    validate()
    print(f"Built {len(documents)} documents, {len(edges)} relationships, {len(timeline)} events, {len(chunks)} RAG chunks")


def search(query, verified_only=False):
    path = ROOT / "ai/index/chunks.jsonl"
    if not path.exists():
        raise ValueError("Run build before search")
    terms = query.casefold().split()
    ranked = []
    for line in path.read_text(encoding="utf-8").splitlines():
        c = json.loads(line)
        if verified_only and c["verification_status"] != "human_verified":
            continue
        haystack = (c["title"] + " " + c["text"]).casefold()
        score = sum(3 if t in c["title"].casefold() else 1 for t in terms if t in haystack)
        if score: ranked.append((score, c))
    ranked.sort(key=lambda item: (-item[0], item[1]["chunk_id"]))
    print(json.dumps([c for _, c in ranked[:5]], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "build", "search"])
    parser.add_argument("query", nargs="?")
    parser.add_argument("--verified-only", action="store_true")
    args = parser.parse_args()
    if args.command == "validate": print(f"Validated {len(validate())} policy documents")
    elif args.command == "build": build()
    elif not args.query: parser.error("search requires a query")
    else: search(args.query, args.verified_only)
