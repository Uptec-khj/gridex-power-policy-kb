import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("gridex_kb", ROOT / "scripts/kb.py")
kb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kb)


class KnowledgeBaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for name in ("content", "schemas", "data"):
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

    def test_private_archive_path_rejected(self):
        self.rewrite(lambda m: m["attachments"][0].update(path="sources/internal.pdf"))
        with self.assertRaisesRegex(ValueError, "private archive paths"):
            kb.validate()

    def test_public_validation_does_not_require_originals(self):
        self.assertFalse((self.root / "sources").exists())
        self.assertEqual(len(kb.validate()), 47)

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
