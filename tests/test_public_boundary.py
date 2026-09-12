import tempfile
import unittest
from pathlib import Path

from scripts.validate_kb import check_public_boundary
from scripts import source_registry


class PublicBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "content").mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def test_official_download_link_is_allowed(self):
        (self.root / "content/test.md").write_text("[PDF](https://www.kpx.or.kr/plan.pdf)", encoding="utf-8")
        self.assertEqual(check_public_boundary(self.root), [])

    def test_original_file_rejected(self):
        (self.root / "content/renamed.pdf").write_bytes(b"%PDF-1.4")
        self.assertTrue(check_public_boundary(self.root))

    def test_private_link_in_generated_html_rejected(self):
        site = self.root / "site/public"
        site.mkdir(parents=True)
        (site / "index.html").write_text('<a href="https://github.com/Uptec-khj/gridex-power-policy-kb-dev/blob/main/sources/document.pdf">source</a>', encoding="utf-8")
        self.assertTrue(check_public_boundary(self.root, site))

    def test_stale_full_text_payload_rejected(self):
        site = self.root / "site/public"
        (site / "static").mkdir(parents=True)
        (site / "index.html").write_text("public knowledge", encoding="utf-8")
        (site / "static/official-pages.json").write_text('{"pages": []}', encoding="utf-8")
        self.assertTrue(check_public_boundary(self.root, site))

    def test_archive_metadata_rejected_under_other_filename(self):
        (self.root / "content/test.md").write_text('archive_path: sources/SRC-TEST/source.pdf', encoding="utf-8")
        self.assertTrue(check_public_boundary(self.root))

    def test_legacy_public_archive_folder_rejected(self):
        (self.root / "data/raw").mkdir(parents=True)
        self.assertTrue(check_public_boundary(self.root))

    def test_registry_preserves_review_dates_and_does_not_promote_evidence(self):
        registry = source_registry.project()
        sources = registry["sources"]
        self.assertEqual(len(sources), 74)
        self.assertEqual(len({s["id"] for s in sources}), 74)
        self.assertTrue(all(s["evidence_level"] == "Unverified" for s in sources))
        self.assertTrue(all(s["last_verified"] != "2026-09-12" for s in sources))
        self.assertEqual(registry, source_registry.project())
