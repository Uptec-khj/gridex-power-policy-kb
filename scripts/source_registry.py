"""Deterministic public source projection; no archive paths or inferred review."""
from datetime import date
from pathlib import Path

import yaml

try:
    from . import kb, gfm_audit
except ImportError:
    import kb
    import gfm_audit

ROOT = Path(__file__).resolve().parents[1]


def project(root=ROOT):
    sources = []
    for path in sorted((root / "content/documents").glob("*.md")):
        meta, _ = kb.read_note(path)
        sources.append({
            "id": meta["source_ids"][0], "document_id": meta["id"], "title": meta["title"],
            "organization": meta["organization"], "country": meta["region_group"],
            "source_type": meta["document_type"], "url": meta["source_url"],
            "official_document_url": meta.get("attachment_url"),
            "publication_date": meta.get("published_date"), "effective_date": meta.get("effective_date"),
            "version": meta.get("version"), "status": meta["document_stage"],
            "official": True, "evidence_level": meta["evidence_level"],
            "collection_mode": "Manual", "last_verified": meta.get("last_verified"),
            "source_locator": None, "locator_status": "claim_level_mapping_pending",
            "publication_policy": "link-only", "note_path": path.relative_to(root).as_posix()})
    registry, _ = gfm_audit.audit(root, date(2026, 9, 12))
    for record in registry["sources"]:
        meta = record["source_metadata"]
        sources.append({
            "id": record["id"], "title": record["title"], "organization": meta.get("organization"),
            "country": meta.get("jurisdiction_market"), "source_type": meta.get("document_type"),
            "url": meta.get("official_page_url"), "official_document_url": meta.get("official_document_url"),
            "publication_date": record["published"], "effective_date": record["effective"],
            "version": meta.get("edition"), "status": meta.get("document_status"),
            "official": True, "evidence_level": record["evidence_level"], "collection_mode": "Manual",
            "last_verified": record["last_verified"], "source_locator": meta.get("relevant_clauses_pages"),
            "publication_policy": "link-only", "note_path": record["note_path"]})
    return {"version": 1, "sources": sorted(sources, key=lambda s: s["id"])}


def build(root=ROOT):
    data = project(root)
    (root / "data/source-registry.yaml").write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    print(f"Source registry: {len(data['sources'])} sources")


if __name__ == "__main__":
    build()
