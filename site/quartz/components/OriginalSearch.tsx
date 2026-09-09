import { QuartzComponent, QuartzComponentConstructor } from "./types"
import { pathToRoot } from "../util/path"
import style from "./styles/originalSearch.scss"
import InternationalFilters from "./InternationalFilters"
// @ts-ignore
import script from "./scripts/originalSearch.inline"

export default (() => {
  const OriginalSearch: QuartzComponent = ({ fileData }) => {
    if (fileData.slug !== "original-search") return null
    return <section class="original-search" aria-label="공식 PDF 원문 검색"
      data-root={pathToRoot(fileData.slug)}>
      <p>공식 PDF에서 자동 추출한 텍스트를 찾습니다. 표·각주는 원문에서 확인하세요.</p>
      <form class="original-search-form">
        <label>검색어<input name="query" type="search" placeholder="예: 송변전 61,183" required /></label>
        <div class="original-search-filters">
          <InternationalFilters />
          <label>문서 범위<select name="plan"><option value="">전체</option><option value="10">제10차</option><option value="11">제11차</option><option value="12">제12차</option><option value="family:에너지기본계획">에너지기본계획</option><option value="family:신재생에너지기본계획">신재생에너지기본계획</option><option value="family:재생에너지기본계획">재생에너지기본계획</option><option value="technical">기술 문서</option></select></label>
          <label>문서 단계<select name="stage"><option value="">전체</option></select></label>
          <button type="submit">원문 검색</button>
        </div>
      </form>
      <p class="original-search-state" role="status" aria-live="polite">검색어를 입력하세요. 검색할 때 원문 색인을 불러옵니다.</p>
      <div class="original-search-results" />
      <noscript>원문 검색에는 JavaScript가 필요합니다. 문서 목록에서 원문 링크를 확인할 수 있습니다.</noscript>
    </section>
  }
  OriginalSearch.afterDOMLoaded = script
  OriginalSearch.css = style
  return OriginalSearch
}) satisfies QuartzComponentConstructor
