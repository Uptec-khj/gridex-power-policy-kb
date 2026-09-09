import copy
import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from scripts.kb import read_note

ROOT = Path(__file__).resolve().parents[1]


class TechnicalSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = Draft202012Validator(json.loads((ROOT / 'schemas/policy-document.schema.json').read_text(encoding='utf-8')), format_checker=FormatChecker())
        cls.technical, _ = read_note(ROOT / 'content/documents/tech-field-test-appendix6.md')
        cls.plan, _ = read_note(ROOT / 'content/documents/p11-final.md')

    def test_technical_requires_scope_and_no_fake_plan_number(self):
        self.assertEqual(list(self.validator.iter_errors(self.technical)), [])
        for changes in ({'plan_number': 11}, {'plan_family': '전력수급기본계획'}, {'technical': None}):
            note = {**self.technical, **changes}
            self.assertTrue(list(self.validator.iter_errors(note)))

    def test_plan_still_requires_family_and_number(self):
        for field in ('plan_family', 'plan_number'):
            self.assertTrue(list(self.validator.iter_errors({**self.plan, field: None})))

    def test_provisional_month_is_not_an_effective_date(self):
        note = copy.deepcopy(self.technical)
        note['technical']['effective_date'] = '2027-03'
        self.assertTrue(list(self.validator.iter_errors(note)))
        note['technical']['effective_date'] = None
        self.assertEqual(list(self.validator.iter_errors(note)), [])

    def test_typed_relationship_needs_provenance(self):
        note = {**self.technical, 'typed_relations': [{'target': '[[p11-final]]', 'type': 'references'}]}
        self.assertTrue(list(self.validator.iter_errors(note)))


if __name__ == '__main__':
    unittest.main()
