import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import originals


class OriginalEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.payload = b"%PDF-1.4 test fixture; parser mocked"
        self.path = self.root / "data/raw/source.pdf"
        self.path.parent.mkdir(parents=True)
        self.path.write_bytes(self.payload)
        self.meta = {"id": "policy", "title": "송변전 계획", "draft": False,
            "verification_status": "source_verified", "source_url": "https://www.kepco.co.kr/source",
            "plan_family": "장기송변전설비계획", "plan_number": 11, "document_stage": "final", "published_date": "2025-05-27",
            "attachments": [{"title": "plan.pdf", "format": "pdf", "path": "data/raw/source.pdf",
                "url": "https://www.kepco.co.kr/plan.pdf#old",
                "file_hash": "sha256:" + hashlib.sha256(self.payload).hexdigest()}]}
        self.page = {"pdf_page": 14, "printed_page": None, "text": "2038 송전선로 61,183 C-km", "extraction_status": "text_extracted"}

    def tearDown(self):
        self.temp.cleanup()

    def records(self):
        return [(Path("policy.md"), self.meta, "")]

    def test_hash_mismatch_fails_before_parsing(self):
        self.path.write_bytes(b"changed original")
        with patch.object(originals, "extract_pdf") as parser:
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                originals.build_evidence(self.records(), self.root)
            parser.assert_not_called()

    def test_draft_and_unverified_originals_are_excluded(self):
        for changes in ({"draft": True}, {"draft": False, "verification_status": "unverified"}):
            self.meta.update(changes)
            with patch.object(originals, "extract_pdf") as parser:
                pages, report = originals.build_evidence(self.records(), self.root)
                self.assertEqual(pages, [])
                self.assertEqual(report["document_count"], 0)
                parser.assert_not_called()

    def test_empty_pages_and_citations_are_preserved(self):
        empty = {"pdf_page": 15, "printed_page": None, "text": "", "extraction_status": "empty_or_image"}
        with patch.object(originals, "extract_pdf", return_value=[self.page, empty]):
            pages, report = originals.build_evidence(self.records(), self.root)
        self.assertEqual(report["searchable_pages"], 1)
        self.assertEqual(report["empty_pages"], 1)
        self.assertEqual(pages[0]["citation_url"], "https://www.kepco.co.kr/plan.pdf#page=14")
        self.assertEqual(pages[0]["file_hash"], self.meta["attachments"][0]["file_hash"])
        self.assertEqual(pages[0]["content_origin"], "official_extraction")
        self.assertEqual(pages[0]["extraction_review_status"], "unreviewed")
        self.assertTrue(pages[0]["sparse_text"])
        self.assertFalse(pages[1]["sparse_text"])
        self.assertIsNone(pages[0]["printed_page"])
        self.assertEqual(len(originals.search_pages(pages, "송변전 61183", plan=11, stage="final")), 1)
        self.assertEqual(originals.search_pages(pages, "61183", plan=10), [])
        self.assertEqual(originals.search_pages(pages, "61183", stage="amended"), [])
        self.assertEqual(originals.search_pages(pages, "송변전 99999"), [])
        self.assertEqual(originals.search_pages(pages, " "), [])

    def test_parsing_failure_is_reported(self):
        with patch.object(originals, "extract_pdf", side_effect=ValueError("damaged stream")):
            pages, report = originals.build_evidence(self.records(), self.root)
        self.assertEqual(pages, [])
        self.assertEqual(report["failed_files"], 1)
        self.assertIn("damaged stream", report["files"][0]["error"])

    def test_no_pdf_does_not_look_fully_covered(self):
        self.meta["attachments"] = []
        _, report = originals.build_evidence(self.records(), self.root)
        self.assertEqual(report["documents_without_pdf"], ["policy"])
        self.assertEqual(report["documents_with_pdf"], 0)


if __name__ == "__main__":
    unittest.main()
