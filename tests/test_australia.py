import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from collector.discovery import MAX_CANDIDATES, inspect_html
from scripts import kb

ROOT = Path(__file__).resolve().parents[1]


class AustraliaPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = yaml.safe_load((ROOT / "sources/australia-pilot.yaml").read_text(encoding="utf-8"))
        cls.schema = json.loads((ROOT / "schemas/policy-document.schema.json").read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())
        cls.records = {path.stem: (meta, body) for path, meta, body in kb.notes()}
        cls.notes = {key: value[0] for key, value in cls.records.items()}

    def test_core_is_exactly_six_and_union_has_no_duplicates(self):
        documents = self.config["documents"]
        self.assertEqual(sum(item["tier"] == "core" for item in documents), 6)
        self.assertEqual(sum(item["tier"] == "supplemental" for item in documents), 4)
        self.assertEqual(len({item["id"] for item in documents}), 10)
        self.assertLessEqual(len(documents), MAX_CANDIDATES)

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

    def test_discovery_marks_missing_terms_without_inventing_match(self):
        matched = inspect_html("<h1>NER Version 254</h1><p>4 September 2026</p>",
                               ["NER Version 254", "4 September 2026"])
        self.assertEqual(matched["status"], "matched")
        changed = inspect_html("<h1>NER Version 255</h1>", ["NER Version 254"])
        self.assertEqual(changed["status"], "changed_or_incomplete")
        self.assertEqual(changed["missing_terms"], ["NER Version 254"])

    def test_first_discovery_run_is_bounded_and_records_failures(self):
        report = json.loads((ROOT / "data/metadata/discovery-australia.json").read_text(encoding="utf-8"))
        self.assertEqual(report["pilot"], "G2")
        self.assertEqual(report["documents_checked"], 10)
        self.assertLessEqual(report["documents_checked"], report["candidate_limit"])
        self.assertEqual({result["id"] for result in report["results"]},
                         {item["id"] for item in self.config["documents"]})
        self.assertTrue(all(result["status"] in
                            {"matched", "changed_or_incomplete", "access_limited", "failed", "rejected_domain"}
                            for result in report["results"]))


if __name__ == "__main__":
    unittest.main()
