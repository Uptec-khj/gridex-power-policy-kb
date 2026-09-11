"""Bounded listing checks for the G2 Australia pilot.

This discovers changes; it never writes editorial notes or archives third-party files.
Access controls are reported and are not bypassed.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
MAX_CANDIDATES = 20


def load_config(root=ROOT):
    return yaml.safe_load((root / "sources/australia-pilot.yaml").read_text(encoding="utf-8"))


def allowed_domains(root=ROOT):
    registry = yaml.safe_load((root / "sources/registry.yaml").read_text(encoding="utf-8"))["sources"]
    return {domain for source in registry if source["id"] in {"au-aemo", "au-aemc"}
            for domain in source["allowed_domains"]}


def inspect_html(html, expected_terms):
    text = " ".join(BeautifulSoup(html, "html.parser").get_text(" ", strip=True).split())
    missing = [term for term in expected_terms if term.casefold() not in text.casefold()]
    return {"status": "matched" if not missing else "changed_or_incomplete", "missing_terms": missing}


def discover(fetch=None, root=ROOT, checked_at=None):
    config = load_config(root)
    documents = config["documents"][:MAX_CANDIDATES]
    domains = allowed_domains(root)
    session = requests.Session()
    session.headers["User-Agent"] = "GRIDEX-KB/0.2 (bounded official listing check)"
    # A listing check must stay short even when an official site silently drops traffic.
    fetch = fetch or (lambda url: session.get(url, timeout=(3, 3), allow_redirects=True))
    results = []
    for item in documents:
        url = item["source_url"]
        if urlparse(url).scheme != "https" or urlparse(url).hostname not in domains:
            results.append({"id": item["id"], "status": "rejected_domain", "source_url": url})
            continue
        try:
            response = fetch(url)
            final_url = getattr(response, "url", url)
            status_code = getattr(response, "status_code", 200)
            if urlparse(final_url).hostname not in domains:
                raise ValueError("redirect outside official registry")
            if status_code in (401, 403, 429):
                results.append({"id": item["id"], "status": "access_limited", "http_status": status_code,
                                "source_url": url, "resolved_url": final_url})
                continue
            response.raise_for_status()
            check = inspect_html(response.text, item["expected_terms"])
            results.append({"id": item["id"], **check, "http_status": status_code,
                            "source_url": url, "resolved_url": final_url})
        except (requests.RequestException, ValueError) as exc:
            results.append({"id": item["id"], "status": "failed", "source_url": url, "error": str(exc)})
    return {
        "pilot": config["pilot"],
        "checked_at": checked_at or datetime.now(timezone.utc).isoformat(),
        "candidate_limit": MAX_CANDIDATES,
        "documents_checked": len(results),
        "results": results,
    }


def write_report(report, root=ROOT):
    path = root / "data/metadata/discovery-australia.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    outcome = discover()
    if not args.no_write:
        write_report(outcome)
    print(json.dumps(outcome, ensure_ascii=False, indent=2))
