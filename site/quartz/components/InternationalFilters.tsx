import { taxonomy } from "./international"

export default function InternationalFilters() {
  return <>
    <label>국가·지역<select name="region"><option value="">전체</option>{taxonomy.regions.map(r => <option value={r.id}>{r.label}</option>)}</select></label>
    <label>관할<select name="jurisdiction"><option value="">전체</option>{taxonomy.jurisdictions.map(j => <option value={j.id}>{j.label}</option>)}</select></label>
    <label>전력시장<select name="market"><option value="">전체</option>{taxonomy.markets.map(m => <option value={m.id}>{m.label}</option>)}</select></label>
    <label>원문 언어<select name="language"><option value="">전체</option>{Object.entries(taxonomy.languages).map(([id, label]) => <option value={id}>{label}</option>)}</select></label>
    <label>문서 종류<select name="type"><option value="">전체</option>{Object.entries(taxonomy.document_types).map(([id, label]) => <option value={id}>{label}</option>)}</select></label>
  </>
}
