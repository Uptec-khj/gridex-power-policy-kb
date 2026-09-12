import { matchesFilters, setupRegionFilters } from "../international"
import { normalizeEvidence } from "./originalSearchCore"

document.addEventListener("nav", () => {
  const host = document.querySelector<HTMLElement>(".document-search")
  if (!host) return
  const form = host.querySelector<HTMLFormElement>("form")!
  const state = host.querySelector<HTMLElement>(".document-search-state")!
  const cards = Array.from(host.querySelectorAll<HTMLElement>("article"))
  const read = setupRegionFilters(form)
  const run = (event?: Event) => {
    event?.preventDefault()
    const f = read()
    const terms = f.query.trim().split(/\s+/).map(normalizeEvidence).filter(Boolean)
    let count = 0
    for (const card of cards) {
      const d = card.dataset
      const matches = matchesFilters({region_group:d.region, jurisdictions:JSON.parse(d.jurisdictions!),
        market_regions:JSON.parse(d.markets!), document_language:d.language, document_type:d.type}, f)
        && (!f.stage || d.stage === f.stage) && terms.every(t => normalizeEvidence(d.search!).includes(t))
      card.hidden = !matches
      if (matches) count++
    }
    state.textContent = count ? `${count}건의 공식 문서가 있습니다. 원문은 각 문서의 발행기관 공식 링크에서 확인하세요.` : "조건에 맞는 공개 문서가 없습니다. 국가나 필터를 바꿔보세요."
  }
  form.addEventListener("submit", run)
  form.addEventListener("change", run)
  run()
  window.addCleanup(() => { form.removeEventListener("submit", run); form.removeEventListener("change", run) })
})
