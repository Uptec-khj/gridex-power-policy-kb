"""python -m collector [--id DOCUMENT_ID] [--refresh]. Curated collection only."""
import argparse
import hashlib
import io
import json
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import requests
import yaml
from collector.adapters import discover

ROOT = Path(__file__).resolve().parents[1]


def detect_type(payload: bytes) -> str:
    if payload.startswith(b"%PDF-"):
        from pypdf import PdfReader
        if len(PdfReader(io.BytesIO(payload)).pages) < 1:
            raise ValueError("empty PDF")
        return "pdf"
    if payload.startswith(bytes.fromhex("d0cf11e0a1b11ae1")):
        return "hwp"
    if payload.startswith(b"PK"):
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            if "Contents/content.hpf" in archive.namelist():
                return "hwpx"
        raise ValueError("ZIP is not an HWPX document")
    raise ValueError("Response is not a supported PDF/HWP/HWPX; possible HTML error page")


def store_bytes(payload: bytes, suffix: str) -> tuple[str, str]:
    digest = hashlib.sha256(payload).hexdigest()
    path = ROOT / "data/raw/sha256" / digest[:2] / f"{digest}.{suffix}"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != payload:
        raise ValueError("Immutable archive collision")
    if not path.exists():
        path.write_bytes(payload)
    return path.relative_to(ROOT).as_posix(), "sha256:" + digest


def collect(selected=None, refresh=False):
    seeds = yaml.safe_load((ROOT / "sources/seed-documents.yaml").read_text(encoding="utf-8"))["documents"]
    registries = yaml.safe_load((ROOT / "sources/registry.yaml").read_text(encoding="utf-8"))["sources"]
    domains = {d for r in registries for d in r["allowed_domains"]}
    manifest_path = ROOT / "data/metadata/acquisitions.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    session = requests.Session()
    session.headers["User-Agent"] = "GRIDEX-KB/0.1 (curated official document preservation)"

    def fetch(url):
        # Validate every redirect before sending the next request; never disable TLS checks.
        for _ in range(6):
            p = urlparse(url)
            if p.scheme != "https" or p.hostname not in domains:
                raise ValueError(f"URL outside official registry: {url}")
            r = session.get(url, timeout=(15, 60), allow_redirects=False)
            if r.is_redirect:
                from urllib.parse import urljoin
                url = urljoin(url, r.headers["Location"])
                continue
            r.raise_for_status()
            return r
        raise ValueError("Too many redirects")

    for seed in seeds:
        key = seed["id"]
        if selected and key != selected:
            continue
        if key in manifest and not refresh and manifest[key].get("status") == "collected":
            print(f"{key}: cached", flush=True)
            continue
        now = datetime.now(timezone.utc).isoformat()
        record = {"id": key, "source_url": seed["source_url"], "collected_at": now, "attachments": [], "errors": []}
        if key in manifest:
            record["history"] = manifest[key].get("history", []) + [{k: v for k, v in manifest[key].items() if k != "history"}]
        try:
            r = fetch(seed["source_url"])
            if "html" not in r.headers.get("Content-Type", "").lower():
                raise ValueError("Source page is not HTML")
            r.encoding = "utf-8"
            # Reject soft 404s: a curated title fragment must exist in the page.
            from bs4 import BeautifulSoup
            text = BeautifulSoup(r.text, "html.parser").get_text(" ", strip=True)
            if seed["expected_text"] not in text:
                raise ValueError("Source title fragment missing; page may have moved")
            path, digest = store_bytes(r.content, "html")
            record["source_snapshot"] = {"path": path, "file_hash": digest, "resolved_url": r.url}
            attachments = seed.get("attachments")
            if attachments is None:
                attachments = discover(r.text, seed["source_url"])
            attachments = attachments + seed.get("additional_attachments", [])
            for attachment in attachments:
                try:
                    time.sleep(0.5)
                    raw = fetch(attachment["url"])
                    extension = detect_type(raw.content)
                    path, digest = store_bytes(raw.content, extension)
                    record["attachments"].append({**attachment, "path": path, "file_hash": digest,
                        "format": extension, "size_bytes": len(raw.content), "resolved_url": raw.url,
                        "collected_at": now, "rights_status": "check_source_terms"})
                except (requests.RequestException, ValueError, zipfile.BadZipFile) as exc:
                    record["errors"].append({"url": attachment["url"], "error": str(exc)})
            record["status"] = "partial" if record["errors"] else "collected"
        except (requests.RequestException, ValueError) as exc:
            record["status"] = "failed"
            record["errors"].append({"url": seed["source_url"], "error": str(exc)})
        manifest[key] = record
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        temp = manifest_path.with_suffix(".tmp")
        temp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp.replace(manifest_path)
        print(f"{key}: {record['status']}, {len(record['attachments'])} attachments", flush=True)
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    result = collect(args.id, args.refresh)
    if any(v["status"] != "collected" for k, v in result.items() if not args.id or k == args.id):
        raise SystemExit(1)
