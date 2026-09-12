"""Generator-compatible validation for GRIDEX's existing note profiles.

The public checkout is self-contained. Private file integrity is independently
checked by the private repository's validate_archive.py.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

import yaml

try:
    from . import kb, gfm_audit, source_registry
except ImportError:
    import kb
    import gfm_audit
    import source_registry

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = ("sources", "project", "gcp", "data/raw", "data/source-archive.yaml",
             "data/source-candidates.json", "data/metadata/acquisitions.json",
             "ai/index/official-pages.jsonl", "site/quartz/static/official-pages.json")
LEAK = re.compile(r"data/raw/|(?:archive_path|archive_url)[\"']?\s*:|"
                  r"(?:github\.com|raw\.githubusercontent\.com)/[^/\s]+/[^/\s\"<>]*-dev(?:[/\"<>\s]|$)|"
                  r"gridex-project-management|official_extraction|sources/SRC-", re.I)
RAW_EXTENSIONS = {".pdf", ".hwp", ".hwpx", ".docx", ".zip", ".jsonl"}


def check_public_boundary(root=ROOT, site=None):
    errors = [f"Private-only path present: {rel}" for rel in FORBIDDEN if (root / rel).exists()]
    folders = [root / "content", root / "data", root / "ai/index"]
    if site is not None:
        if not (site / "index.html").is_file():
            errors.append("Build output is missing index.html")
        folders.append(site)
    for folder in folders:
        for path in folder.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() in RAW_EXTENSIONS and path != root / "ai/index/chunks.jsonl":
                errors.append(f"Original/unsupported payload in public output: {path.relative_to(root)}")
            if path.suffix.lower() in {".md", ".json", ".jsonl", ".yaml", ".yml", ".html", ".js", ".xml", ".txt", ".css"}:
                text = path.read_text(encoding="utf-8")
                if LEAK.search(text) or path.name == "official-pages.json":
                    errors.append(f"Private archive data/link in public output: {path.relative_to(root)}")
    return errors


def validate(root=ROOT, site=None):
    root = root.resolve()
    kb.ROOT, kb.CONTENT = root, root / "content"
    errors = check_public_boundary(root, site)
    config = yaml.safe_load((root / "project.yaml").read_text(encoding="utf-8"))
    if config.get("public") is not True or config.get("source_policy") != "link-only":
        errors.append("project.yaml must select public/link-only")
    if config.get("development_repository") != config.get("public_repository", "") + "-dev":
        errors.append("development repository must be named <public>-dev")
    records = kb.validate()
    projected = source_registry.project(root)
    stored = yaml.safe_load((root / "data/source-registry.yaml").read_text(encoding="utf-8"))
    if stored != projected:
        errors.append("Source registry is stale: run scripts/source_registry.py")
    ids = [s["id"] for s in projected["sources"]]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate source ID")
    for path, meta, _ in records:
        if meta.get("source_ids") != ["SRC-POLICY-" + meta["id"].upper()]:
            errors.append(f"{path.name}: missing canonical source ID")
        if meta.get("type") != meta.get("document_type") or meta.get("status") != meta.get("document_stage"):
            errors.append(f"{path.name}: canonical type/status differs from domain metadata")
        for alias, original in (("published", "published_date"), ("effective", "effective_date"), ("last_verified", "last_verified_date")):
            if meta.get(alias) != meta.get(original):
                errors.append(f"{path.name}: {alias} must preserve {original}")
    _, gfm = gfm_audit.audit(root, date.today())
    errors.extend(gfm["errors"])
    if errors:
        raise ValueError("\n".join(errors))
    print(f"Validated {len(records)} policy documents, {len(ids)} source records; public boundary OK; GFM warnings: {len(gfm['warnings'])}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=ROOT)
    parser.add_argument("--site", type=Path)
    args = parser.parse_args()
    try:
        validate(args.root, args.site.resolve() if args.site else None)
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
