import { QuartzComponent, QuartzComponentConstructor } from "./types"
import { pathToRoot } from "../util/path"
import { regionLabel, typeLabel, taxonomy } from "./international"
import InternationalFilters from "./InternationalFilters"
import { stageLabels } from "./scripts/originalSearchCore"
import style from "./styles/originalSearch.scss"
// @ts-ignore
import script from "./scripts/documentSearch.inline"

export default (() => {
  const DocumentSearch: QuartzComponent = ({ fileData, allFiles }) => {
    if (fileData.slug !== "document-search") return null
    const root = pathToRoot(fileData.slug)
    const docs = allFiles.filter(f => f.frontmatter?.id && !f.frontmatter?.draft &&
      ["source_verified", "human_verified"].includes(String(f.frontmatter?.verification_status)))
      .sort((a,b) => String(b.frontmatter?.published_date ?? "").localeCompare(String(a.frontmatter?.published_date ?? "")) || String(a.slug).localeCompare(String(b.slug)))
    return <section class="original-search document-search" aria-label="국가별 문서 찾기">
      <form>
        <label>제목·주제 검색<input name="query" type="search" placeholder="예: 수요전망, 성능시험" /></label>
        <div class="original-search-filters"><InternationalFilters />
          <label>문서 단계<select name="stage"><option value="">전체</option>{Object.entries(stageLabels).map(([id,label]) => <option value={id}>{label}</option>)}</select></label>
          <button type="submit">문서 찾기</button>
        </div>
      </form>
      <p class="document-search-state" role="status" aria-live="polite">공개 공식 자료 {docs.length}건. 제목·원어 제목·주제와 분류에서 찾습니다.</p>
      <div class="document-search-results">{docs.map(f => {
        const m = f.frontmatter as Record<string, any>
        return <article data-region={m.region_group ?? ""} data-jurisdictions={JSON.stringify(m.jurisdictions ?? [])}
          data-markets={JSON.stringify(m.market_regions ?? [])} data-language={m.document_language ?? ""}
          data-type={m.document_type ?? ""} data-stage={m.document_stage}
          data-search={[m.title, m.title_original, m.title_ko, ...(m.topics ?? []), m.organization, m.document_identifier].filter(Boolean).join(" ")}>
          <h3><a class="internal" href={`${root}/${f.slug}`}>{m.title}</a></h3>
          {m.title_original && m.title_original !== m.title && <p lang={m.document_language}>{m.title_original}</p>}
          <p>{regionLabel(m.region_group)} · {(m.market_regions ?? []).join(", ") || "시장 미표기"} · {typeLabel(m.document_type)} · {stageLabels[m.document_stage] ?? m.document_stage} · {m.published_date ?? "발행일 미확인"}</p>
          {m.validity_status && <p>판본 {m.version ?? "미표기"} · 시행 {m.effective_date ?? "별도 시행일 없음·미표기"} · {m.validity_status}</p>}
          <p>{m.organization} · {taxonomy.languages[m.document_language as keyof typeof taxonomy.languages] ?? "언어 미확인"} · {m.verification_status === "human_verified" ? "사람 검수 완료" : "AI 요약 · 검수 대기"}</p>
        </article>
      })}</div>
      <noscript>필터에는 JavaScript가 필요합니다. 위 전체 문서 또는 국가별 메뉴에서 찾아볼 수 있습니다.</noscript>
    </section>
  }
  DocumentSearch.css = style
  DocumentSearch.afterDOMLoaded = script
  return DocumentSearch
}) satisfies QuartzComponentConstructor
