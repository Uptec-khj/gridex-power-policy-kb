import { QuartzComponent, QuartzComponentConstructor } from "./types"

const stages: Record<string, string> = {
  final: "확정 문서", amended: "수정 공고", working_draft: "실무안",
  draft: "초안", consultation: "의견수렴·토론회", announced: "추진·사전 안내",
  supporting: "공식 보조자료", press_release: "공식 발표자료", official_explainer: "기관 해설",
}

export default (() => {
  const PolicyMetadata: QuartzComponent = ({ fileData }) => {
    const m = fileData.frontmatter as Record<string, unknown> | undefined
    if (!m?.id) return null
    const reviewed = m.verification_status === "human_verified"
    return <aside class="policy-metadata" aria-label="문서 출처와 검수 상태">
      <div class="policy-badges">
        <span>{m.plan_number == null ? String(m.category) : `제${String(m.plan_number)}차`}</span>
        <span>{stages[String(m.document_stage)] ?? String(m.document_stage)}</span>
        <span class={reviewed ? "reviewed" : "pending"}>{reviewed ? "사람 검수 완료" : "AI 요약 · 검수 대기"}</span>
      </div>
      <p>{String(m.organization)} · 발행 {m.published_date ? String(m.published_date) : "일자 미확인"}</p>
      <a href={String(m.source_url)} target="_blank" rel="noopener noreferrer">공식 출처 확인 ↗</a>
    </aside>
  }
  return PolicyMetadata
}) satisfies QuartzComponentConstructor
