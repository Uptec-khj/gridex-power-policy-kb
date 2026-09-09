import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import yaml
from collector.__main__ import detect_type
from collector.adapters import discover

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("gridex_kb", ROOT / "scripts/kb.py")
kb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kb)


class SourceSafetyTests(unittest.TestCase):
    def test_html_error_is_not_a_pdf(self):
        with self.assertRaisesRegex(ValueError, "not a supported"):
            detect_type(b"<!DOCTYPE html><title>Download error</title>")

    def test_mcee_ids_are_extracted_from_observed_link(self):
        result = discover("<a href=\"javascript:ajaxFileDownLoad('311860','3');\">source.pdf</a>", "https://www.mcee.go.kr/home/web/board/read.do?boardId=1823520")
        self.assertEqual(result[0]["url"], "https://www.mcee.go.kr/home/file/readDownloadFile.do?fileId=311860&fileSeq=3")


class KnowledgeBaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for name in ("content", "schemas", "sources", "data/raw"):
            shutil.copytree(ROOT / name, self.root / name)
        self.p1 = patch.object(kb, "ROOT", self.root)
        self.p2 = patch.object(kb, "CONTENT", self.root / "content")
        self.p1.start(); self.p2.start()

    def tearDown(self):
        self.p2.stop(); self.p1.stop(); self.temp.cleanup()

    def rewrite(self, fn):
        path = self.root / "content/documents/p10-final.md"
        meta, body = kb.read_note(path)
        fn(meta)
        path.write_text("---\n" + yaml.safe_dump(meta, allow_unicode=True) + "---\n" + body, encoding="utf-8")

    def test_broken_relationship_rejected(self):
        self.rewrite(lambda m: m["related_documents"].append("[[does-not-exist]]"))
        with self.assertRaisesRegex(ValueError, "invalid relationship"):
            kb.validate()

    def test_corrupt_preserved_file_rejected(self):
        meta, _ = kb.read_note(self.root / "content/documents/p10-final.md")
        (self.root / meta["attachments"][0]["path"]).write_bytes(b"corrupt original")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            kb.validate()

    def test_false_human_verification_rejected(self):
        self.rewrite(lambda m: m.update(verification_status="human_verified"))
        with self.assertRaisesRegex(ValueError, "human review"):
            kb.validate()

    def test_unverified_public_note_rejected(self):
        self.rewrite(lambda m: m.update(verification_status="unverified"))
        with self.assertRaisesRegex(ValueError, "public note"):
            kb.validate()

    def test_draft_excluded_and_chunk_provenance_retained(self):
        self.rewrite(lambda m: m.update(draft=True, verification_status="unverified"))
        kb.build()
        chunks = [json.loads(line) for line in (self.root / "ai/index/chunks.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertFalse(any(c["document_id"] == "p10-final" for c in chunks))
        self.assertTrue(all(c["source_url"].startswith("https://") and c["content_origin"] == "ai_assisted_editorial" for c in chunks))


if __name__ == "__main__":
    unittest.main()
