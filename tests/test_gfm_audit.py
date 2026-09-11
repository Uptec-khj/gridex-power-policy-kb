import importlib.util
from datetime import date
from pathlib import Path
import tempfile
import unittest

import yaml

SPEC = importlib.util.spec_from_file_location("gfm_audit", Path(__file__).resolve().parents[1] / "scripts/gfm_audit.py")
audit_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_module)


class GfmAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path = self.root / "content/gfm/02_Sources/Korea/source.md"
        self.meta = {key: "미확인" for key in audit_module.REQUIRED}
        self.meta.update(id="SRC-TEST", family_id="FAM-TEST", title_ko="시험",
                         official_page_url="https://example.org/official",
                         document_status="공개회람·개정안", effective_date=None,
                         verified_on=date(2026, 9, 9), relevant_clauses_pages="§11.2",
                         terms_url="https://example.org/", redistribution="미확인")
        self.write(self.path, self.meta)

    def write(self, path, meta, body=""):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\n" + yaml.safe_dump(meta, allow_unicode=True) + "---\n" + body, encoding="utf-8")

    def run_audit(self):
        return audit_module.audit(self.root, date(2026, 9, 11))

    def test_read_only_deterministic_mapping(self):
        before = audit_module.snapshot(self.root)
        first = self.run_audit()
        self.assertEqual(first, self.run_audit())
        self.assertEqual(before, audit_module.snapshot(self.root))
        self.assertFalse(first[1]["errors"])
        self.assertEqual(first[0]["sources"][0]["last_verified"], "2026-09-09")

    def test_official_draft_not_promoted(self):
        source = self.run_audit()[0]["sources"][0]
        self.assertEqual(source["evidence_level"], "Unverified")
        self.assertEqual(source["evidence_assignment"], "not_assessed")
        self.assertIsNone(source["effective"])
        self.assertEqual(source["source_metadata"]["document_status"], "공개회람·개정안")

    def test_partial_dates_preserved(self):
        self.meta.update(publication_date=2026, facility_cutoff_date="2027-03")
        self.write(self.path, self.meta)
        registry, report = self.run_audit()
        self.assertFalse(report["errors"])
        self.assertEqual(registry["sources"][0]["published"], 2026)
        self.assertEqual(registry["sources"][0]["source_metadata"]["facility_cutoff_date"], "2027-03")

    def test_duplicate_id(self):
        self.write(self.path.with_name("duplicate.md"), self.meta)
        self.assertTrue(any("duplicate id" in x for x in self.run_audit()[1]["errors"]))

    def test_broken_relative_link(self):
        self.write(self.path, self.meta, "[없음](missing.md)")
        self.assertTrue(any("relative link" in x for x in self.run_audit()[1]["errors"]))

    def test_encoded_relative_link(self):
        self.write(self.path.with_name("한글.md"), {"id": "NOTE-LINK", "type": "hub"})
        self.write(self.path, self.meta, "[한글](%ED%95%9C%EA%B8%80.md)")
        self.assertFalse(any("relative link" in x for x in self.run_audit()[1]["errors"]))

    def test_source_reference_cannot_target_hub(self):
        hub = self.root / "content/gfm/03_Regions/hub.md"
        self.write(hub, {"id": "HUB-TEST", "source_ids": ["HUB-TEST"]})
        self.assertTrue(any("unresolved source reference" in x for x in self.run_audit()[1]["errors"]))

    def test_attachment_rejected(self):
        attachment = self.root / "content/gfm/99_Attachments/third-party.pdf"
        attachment.parent.mkdir(parents=True)
        attachment.write_bytes(b"test fixture, not a real PDF")
        self.assertTrue(any("non-Markdown" in x for x in self.run_audit()[1]["errors"]))

    def test_future_verified_date(self):
        self.meta["verified_on"] = "2026-09-12"
        self.write(self.path, self.meta)
        self.assertTrue(any("future verified_on" in x for x in self.run_audit()[1]["errors"]))

    def test_invalid_calendar_date(self):
        self.meta["effective_date"] = "2026-02-30"
        self.write(self.path, self.meta)
        self.assertTrue(any("invalid date" in x for x in self.run_audit()[1]["errors"]))

    def test_unknown_rights_stay_link_only(self):
        registry, report = self.run_audit()
        self.assertEqual(registry["sources"][0]["publication_policy"], "link-only")
        self.assertTrue(any("redistribution unresolved" in x for x in report["warnings"]))
        self.assertTrue(any("homepage" in x for x in report["warnings"]))

    def test_confirmed_needs_scope(self):
        self.meta["evidence_level"] = "Confirmed"
        self.write(self.path, self.meta)
        self.assertTrue(any("Confirmed requires" in x for x in self.run_audit()[1]["errors"]))

    def test_stale_verification_is_warning(self):
        self.meta["verified_on"] = "2025-01-01"
        self.write(self.path, self.meta)
        self.assertTrue(any("stale verification" in x for x in self.run_audit()[1]["warnings"]))

    def test_empty_vault_fails(self):
        with tempfile.TemporaryDirectory() as empty:
            self.assertTrue(audit_module.audit(Path(empty), date(2026, 9, 11))[1]["errors"])


if __name__ == "__main__":
    unittest.main()
