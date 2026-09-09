"""One-time, idempotent 1.0 → 1.1 migration for the existing Korean corpus.

Only frontmatter changes. Original bytes, source links, IDs and body stay intact.
"""
import yaml

try:
    from . import kb
except ImportError:
    import kb


def migrate(meta):
    if meta['schema_version'] != '1.0':
        return meta
    kind = meta.get('technical', {}).get('document_type')
    if not kind:
        kind = {'press_release': 'press_release', 'official_explainer': 'official_explainer',
                'announced': 'notice', 'consultation': 'notice'}.get(meta['document_stage'])
    if not kind:
        kind = {'전력수요': 'forecast', '송변전망': 'transmission_plan'}.get(meta['category'], 'plan')
    if meta['id'] == 'p11-poll':
        kind = 'study'
    return {**meta, 'schema_version': '1.1', 'region_group': 'KR', 'jurisdictions': ['KR'],
            'market_regions': [], 'document_language': 'ko', 'document_type': kind,
            'title_original': None, 'title_ko': meta['title'],
            'document_identifier': None, 'edition_year': None, 'version': None}


if __name__ == '__main__':
    for path, meta, body in kb.notes():
        changed = migrate(meta)
        if changed != meta:
            path.write_text('---\n' + yaml.safe_dump(changed, allow_unicode=True, sort_keys=False, width=120)
                            + '---\n' + body, encoding='utf-8')
    print('Migrated existing Korean metadata; original attachments and bodies preserved.')
