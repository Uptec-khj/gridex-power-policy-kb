"""Read-only GFM metadata audit and deterministic kbgen-compatible projection.

No fetching, LLM calls, evidence promotion, source edits or deployment.
--write only writes data/gfm/source-registry.json and data/gfm/metadata-audit.json.
"""
import argparse
from collections import Counter
from datetime import date, datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "c74f6625f2f570c2f68a748c26477e7634f718da"
LEVELS = {"Confirmed", "Supported", "Reported", "Inferred", "Unverified"}
REQUIRED = ("id", "family_id", "title_original", "title_ko", "organization",
            "jurisdiction_market", "document_type", "edition", "language",
            "access_status", "document_status", "applicability", "publication_mode")


def read_note(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)\Z", text, re.S)
    if not match:
        raise ValueError("YAML frontmatter missing")
    meta = yaml.safe_load(match[1])
    if not isinstance(meta, dict):
        raise ValueError("YAML frontmatter must be a mapping")
    return meta, match[2]


def string_date(value):
    return value.isoformat() if isinstance(value, (date, datetime)) else value


def web_url(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.hostname) and not parsed.username


def snapshot(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((root / "content/gfm").rglob("*")) if p.is_file()}


def audit(root, as_of):
    root = root.resolve()
    vault = root / "content/gfm"
    errors, warnings, records = [], [], []
    paths = sorted(vault.rglob("*.md"))
    ids = {}
    metas = []
    if not paths:
        errors.append("content/gfm: no Markdown notes found")
    for path in paths:
        rel = path.relative_to(root).as_posix()
        try:
            meta, body = read_note(path)
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(f"{rel}: {exc}")
            continue
        if "90_Templates" in path.parts:
            continue
        metas.append((rel, meta))
        note_id = meta.get("id")
        if note_id:
            if not isinstance(note_id, str):
                errors.append(f"{rel}: id must be a string")
            elif note_id in ids:
                errors.append(f"{rel}: duplicate id {note_id}")
            else:
                ids[note_id] = rel
        # Validate file targets; heading existence is a separate future gate.
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", body):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith(("#", "//")):
                continue
            dest = (path.parent / unquote(parsed.path)).resolve()
            if not dest.is_relative_to(root) or not dest.exists():
                errors.append(f"{rel}: broken/escaping relative link {target}")
        for target in re.findall(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]", body):
            candidates = [p for p in paths if p.stem == target or p.relative_to(vault).with_suffix("").as_posix() == target]
            if len(candidates) != 1:
                errors.append(f"{rel}: missing/ambiguous wikilink {target}")
        if "02_Sources" not in path.parts:
            continue
        for key in REQUIRED:
            if not isinstance(meta.get(key), str) or not meta[key].strip():
                errors.append(f"{rel}: missing/non-string source field {key}")
        if not web_url(meta.get("official_page_url")):
            errors.append(f"{rel}: official_page_url must be http(s)")
        for key in ("official_document_url", "terms_url"):
            if meta.get(key) and not web_url(meta[key]):
                errors.append(f"{rel}: invalid {key}")
        for key in ("publication_date", "approval_date", "effective_date", "facility_cutoff_date", "verified_on", "rights_checked_on"):
            value = string_date(meta.get(key))
            if not value:
                continue
            try:
                if re.fullmatch(r"\d{4}", str(value)):
                    date(int(value), 1, 1)  # validate year, do not invent month/day
                elif re.fullmatch(r"\d{4}-\d{2}", str(value)):
                    date.fromisoformat(value + "-01")  # preserve month precision
                else:
                    date.fromisoformat(str(value))
            except ValueError:
                errors.append(f"{rel}: invalid date {key}={value}")
        checked = string_date(meta.get("verified_on"))
        if not checked:
            warnings.append(f"{rel}: missing verified_on")
        else:
            try:
                age = (as_of - date.fromisoformat(str(checked))).days
                if age < 0:
                    errors.append(f"{rel}: future verified_on")
                elif age > 90:
                    warnings.append(f"{rel}: stale verification ({age} days)")
            except ValueError:
                errors.append(f"{rel}: verified_on requires a complete date")
        level = meta.get("evidence_level", "Unverified")
        if not isinstance(level, str) or level not in LEVELS:
            errors.append(f"{rel}: invalid evidence_level")
            level = "Unverified"
        if level == "Confirmed" and not (meta.get("evidence_scope") and checked and meta.get("relevant_clauses_pages")):
            errors.append(f"{rel}: Confirmed requires explicit evidence_scope, verification date and locator")
        if "evidence_level" not in meta:
            warnings.append(f"{rel}: explicit scoped evidence_level not yet assigned; projected Unverified")
        if not meta.get("relevant_clauses_pages"):
            warnings.append(f"{rel}: missing source locator/review scope")
        if not meta.get("redistribution") or "미확인" in str(meta.get("redistribution")):
            warnings.append(f"{rel}: redistribution unresolved; link-only")
        terms = meta.get("terms_url")
        if web_url(terms) and urlsplit(terms).path in {"", "/"}:
            warnings.append(f"{rel}: terms_url is a homepage, not verified use conditions")
        records.append({
            "id": meta.get("id"), "title": meta.get("title_ko"), "type": "source",
            "source_ids": [meta.get("id")], "published": string_date(meta.get("publication_date")),
            "effective": string_date(meta.get("effective_date")),
            "last_verified": checked, "evidence_level": level,
            "evidence_assignment": "explicit" if "evidence_level" in meta else "not_assessed",
            "note_path": rel, "note_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "collection_mode": "Manual", "publication_policy": "link-only",
            "source_metadata": {k: string_date(v) for k, v in meta.items()},
        })
    source_ids = {r["id"] for r in records if isinstance(r["id"], str)}
    for rel, meta in metas:
        for key in ("source_ids", "source_document_id"):
            refs = meta.get(key) or []
            if isinstance(refs, str):
                refs = [refs]
            if not isinstance(refs, list):
                errors.append(f"{rel}: invalid {key}")
                continue
            for ref in refs:
                if not isinstance(ref, str) or ref not in source_ids:
                    errors.append(f"{rel}: unresolved source reference {ref}")
    # Current GFM publication policy permits Markdown only. Any future exception
    # requires a reviewed rights manifest and a separate validator change.
    for path in sorted(vault.rglob("*")):
        if path.is_symlink() or (path.is_file() and path.suffix.lower() != ".md"):
            errors.append(f"{path.relative_to(root)}: non-Markdown/symlink in link-only GFM vault")
    registry = {"schema_version": 1, "upstream_commit": UPSTREAM,
                "scope": "GFM source metadata only; not claim verification",
                "sources": records}
    report = {"schema_version": 1, "as_of": as_of.isoformat(),
              "scope": "metadata/file-link audit; no live URL or claim verification",
              "status": "FAIL" if errors else ("NEEDS_REVIEW" if warnings else "PASS"),
              "notes_scanned": len(paths), "source_count": len(records),
              "evidence_levels": dict(sorted(Counter(r["evidence_level"] for r in records).items())),
              "errors": sorted(errors), "warnings": sorted(warnings)}
    return registry, report


def upstream_audit(generator, registry):
    """Audit a temporary metadata-only projection, never the live vault."""
    generator = generator.resolve()
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=generator, text=True).strip()
    if sha != UPSTREAM or subprocess.check_output(["git", "status", "--porcelain"], cwd=generator, text=True).strip():
        raise ValueError("generator must be the clean pinned checkout")
    with tempfile.TemporaryDirectory(prefix="gfm-kbgen-") as tmp:
        stage = Path(tmp)
        (stage / "content").mkdir()
        for n, record in enumerate(registry["sources"]):
            meta = {k: record[k] for k in ("id", "title", "type", "source_ids", "published", "effective", "last_verified", "evidence_level")}
            (stage / "content" / f"source-{n:03d}.md").write_text("---\n" + yaml.safe_dump(meta, allow_unicode=True) + "---\n", encoding="utf-8")
        run = subprocess.run([sys.executable, "-m", "kb_generator", "audit", str(stage), "--json"], cwd=generator, capture_output=True, text=True, check=True)
        result = json.loads(run.stdout)
        result.pop("report", None)  # temporary location is not an artifact
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--generator-root", type=Path)
    args = parser.parse_args()
    before = snapshot(args.root)
    registry, report = audit(args.root, args.as_of)
    schema = json.loads((ROOT / "schemas/gfm-source-registry.schema.json").read_text(encoding="utf-8"))
    serializable = json.loads(json.dumps(registry, default=string_date))
    report["errors"].extend(f"registry schema: {error.json_path}: {error.message}"
                            for error in Draft202012Validator(schema).iter_errors(serializable))
    if report["errors"]:
        report["status"] = "FAIL"
    if args.generator_root and not report["errors"]:
        report["upstream_audit"] = upstream_audit(args.generator_root, registry)
    if snapshot(args.root) != before:
        raise RuntimeError("canonical content changed during audit")
    if args.write and not report["errors"]:
        dest = args.root / "data/gfm"
        dest.mkdir(parents=True, exist_ok=True)
        for name, payload in (("source-registry.json", registry), ("metadata-audit.json", report)):
            (dest / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=string_date) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
