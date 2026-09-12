import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from scripts import kb
from scripts.migrate_international import migrate

ROOT = Path(__file__).resolve().parents[1]


class InternationalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / 'schemas/policy-document.schema.json').read_text(encoding='utf-8'))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())
        cls.kr, _ = kb.read_note(ROOT / 'content/documents/p11-final.md')

    def errors(self, **changes):
        return list(self.validator.iter_errors({**self.kr, **changes}))

    def foreign(self):
        return {**self.kr, 'region_group': 'AU', 'jurisdictions': ['AU'], 'market_regions': ['NEM'],
                'document_language': 'en', 'document_type': 'plan', 'title_original': 'Test plan',
                'plan_family': 'integrated-system-plan', 'plan_number': None, 'edition_year': 2026,
                'adopted_date': None, 'effective_date': None, 'validity_status': 'current',
                'status_checked_date': '2026-09-11', 'legal_force': 'statutory_plan',
                'applicability': 'NEM test fixture', 'translation_status': 'ai_summary_ko',
                'translation_review_status': 'unreviewed', 'rights_status': 'link_only_pending_terms',
                'rights_url': None, 'archive_access': 'link_only'}

    def test_country_and_jurisdiction_cannot_conflict(self):
        self.assertTrue(self.errors(jurisdictions=['EU']))
        self.assertTrue(self.errors(region_group='EU'))
        self.assertTrue(self.errors(jurisdictions=[]))
        note = self.foreign()
        self.assertEqual(list(self.validator.iter_errors(note)), [])
        note['jurisdictions'] = ['US']
        self.assertTrue(list(self.validator.iter_errors(note)))

    def test_market_must_have_matching_jurisdiction(self):
        note = self.foreign()
        note['market_regions'] = ['WEM']
        self.assertTrue(list(self.validator.iter_errors(note)))
        note['jurisdictions'] = ['AU-WA']
        self.assertEqual(list(self.validator.iter_errors(note)), [])
        note['market_regions'] = ['CAISO']
        self.assertTrue(list(self.validator.iter_errors(note)))

    def test_edition_year_is_not_a_korean_plan_number(self):
        note = self.foreign()
        note['plan_number'] = 2026
        self.assertTrue(list(self.validator.iter_errors(note)))
        note.update(plan_number=None, region_group='US', jurisdictions=['US'], market_regions=[])
        self.assertTrue(list(self.validator.iter_errors(note)))

    def test_foreign_regulation_can_have_no_plan_family(self):
        note = self.foreign()
        note.update(region_group='Europe', jurisdictions=['EU', 'DE'], market_regions=[],
                    plan_family=None, category='전력시장', document_type='regulation',
                    document_identifier='test-identifier')
        self.assertEqual(list(self.validator.iter_errors(note)), [])
        self.assertTrue(self.errors(plan_family=None, plan_number=None))

    def test_technical_kind_must_match_technical_metadata(self):
        meta, _ = kb.read_note(ROOT / 'content/documents/tech-field-test-appendix6.md')
        self.assertEqual(list(self.validator.iter_errors(meta)), [])
        meta['document_type'] = 'plan'
        self.assertTrue(list(self.validator.iter_errors(meta)))

    def test_required_language_and_legacy_migration(self):
        self.assertTrue(self.errors(document_language='not-a-language'))
        legacy = {k:v for k,v in self.kr.items() if k not in kb.INTERNATIONAL_FIELDS}
        legacy['schema_version'] = '1.0'
        self.assertEqual(list(self.validator.iter_errors(legacy)), [])
        self.assertTrue(list(self.validator.iter_errors({**legacy, 'region_group':'AU'})))
        new = migrate(legacy)
        self.assertEqual(migrate(new), new)
        for field in ('id', 'attachments', 'file_hash', 'related_documents', 'source_url'):
            self.assertEqual(new[field], legacy[field])
        self.assertEqual(list(self.validator.iter_errors(new)), [])

    def test_editorial_search_keeps_region_and_language(self):
        import contextlib
        import io
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            kb.search('수요', region='AU')
        australian = json.loads(output.getvalue())
        self.assertTrue(australian)
        self.assertTrue(all(item['region_group'] == 'AU' for item in australian))
        self.assertTrue(any(item['market_regions'] == ['WEM'] for item in australian))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            kb.search('수요', region='KR', language='ko')
        self.assertTrue(json.loads(output.getvalue()))


if __name__ == '__main__':
    unittest.main()
