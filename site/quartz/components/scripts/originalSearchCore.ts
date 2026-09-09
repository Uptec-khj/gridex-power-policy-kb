export interface EvidencePage {
  chunk_id: string
  document_id: string
  title: string
  attachment_title: string
  slug: string
  text: string
  file_hash: string
  pdf_page: number
  printed_page: null
  plan_number: number | null
  document_stage: string
  published_date: string | null
  citation_url: string
  source_url: string
  archive_url: string
  sparse_text: boolean
}

export const stageLabels: Record<string, string> = {
  final: "확정 문서", amended: "수정 공고", working_draft: "실무안", draft: "초안",
  consultation: "의견수렴·토론회", announced: "추진·사전 안내", supporting: "공식 보조자료",
  press_release: "공식 발표자료", official_explainer: "기관 해설",
}

export function normalizeEvidence(text: string): string {
  return text.normalize("NFKC").toLowerCase().replace(/(?<=\d),(?=\d)/g, "").replace(/\s+/g, "")
}

export function rankEvidence(pages: EvidencePage[], query: string, plan = "", stage = "") {
  const terms = query.trim().split(/\s+/).map(normalizeEvidence).filter(Boolean)
  if (!terms.length) return []
  return pages.filter(p => p.text && (!plan || (plan === "technical" ? p.plan_number === null : String(p.plan_number) === plan)) && (!stage || p.document_stage === stage))
    .map(page => {
      const title = normalizeEvidence(page.title), body = normalizeEvidence(page.text)
      const score = terms.every(t => title.includes(t) || body.includes(t))
        ? terms.reduce((sum, t) => sum + (title.includes(t) ? 3 : 0) + (body.includes(t) ? 1 : 0), 0) : 0
      return { page, score }
    }).filter(r => r.score > 0)
    .sort((a, b) => b.score - a.score || a.page.document_id.localeCompare(b.page.document_id) ||
      a.page.file_hash.localeCompare(b.page.file_hash) || a.page.pdf_page - b.page.pdf_page)
    .map(r => r.page)
}

export function evidenceSnippet(text: string, query: string): string {
  const flat = text.replace(/\s+/g, " ")
  // Locate text terms when possible; retain the untouched full page in the disclosure.
  const locations = query.trim().split(/\s+/).map(t => flat.toLowerCase().indexOf(t.toLowerCase())).filter(i => i >= 0)
  const start = Math.max(0, (locations.length ? Math.min(...locations) : 0) - 70)
  return (start ? "…" : "") + flat.slice(start, start + 350) + (flat.length > start + 350 ? "…" : "")
}
