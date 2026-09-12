import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from scripts import kb

ROOT = Path(__file__).resolve().parents[1]


class AustraliaPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = yaml.safe_load((ROOT / "data/australia-pilot.yaml").read_text(encoding="utf-8"))
        cls.schema = json.loads((ROOT / "schemas/policy-document.schema.json").read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())
        cls.records = {path.stem: (meta, body) for path, meta, body in kb.notes()}
        cls.notes = {key: value[0] for key, value in cls.records.items()}

    def test_core_is_exactly_six_and_union_has_no_duplicates(self):
        documents = self.config["documents"]
        self.assertEqual(sum(item["tier"] == "core" for item in documents), 6)
        self.assertEqual(sum(item["tier"] == "supplemental" for item in documents), 4)
        self.assertEqual(len({item["id"] for item in documents}), 10)
        self.assertLessEqual(len(documents), 20)

    def test_all_pilot_notes_validate_and_match_market(self):
        for item in self.config["documents"]:
            meta = self.notes[item["id"]]
            self.assertEqual(list(self.validator.iter_errors(meta)), [], item["id"])
            self.assertEqual(meta["market_regions"], [item["market"]])
            self.assertEqual(meta["status_checked_date"], "2026-09-11")
            self.assertTrue(meta["applicability"])
            self.assertEqual(meta["archive_access"], "link_only")
            body = self.records[item["id"]][1]
            self.assertIn(meta["source_url"], body)
            self.assertGreaterEqual(body.count("https://"), 2)

    def test_nem_and_wem_jurisdictions_do_not_mix(self):
        for item in self.config["documents"]:
            meta = self.notes[item["id"]]
            expected = "AU" if item["market"] == "NEM" else "AU-WA"
            self.assertEqual(meta["jurisdictions"], [expected])

    def test_draft_final_and_revision_dates_are_explicit(self):
        self.assertEqual(self.notes["au-isp-2026-draft"]["validity_status"], "superseded")
        self.assertEqual(self.notes["au-isp-2026-draft"]["next_document"], "[[au-isp-2026-final]]")
        self.assertEqual(self.notes["au-isp-2026-final"]["previous_document"], "[[au-isp-2026-draft]]")
        self.assertEqual(self.notes["au-wem-esoo-2026"]["version"], "2")
        self.assertEqual(self.notes["au-wem-esoo-2026"]["published_date"], "2026-06-23")



if __name__ == "__main__":
    unittest.main()
