import { EvidencePage, evidenceSnippet, rankEvidence, stageLabels } from "./originalSearchCore"

document.addEventListener("nav", () => {
  const host = document.querySelector<HTMLElement>(".original-search")
  if (!host) return
  const form = host.querySelector<HTMLFormElement>("form")!
  const query = form.elements.namedItem("query") as HTMLInputElement
  const plan = form.elements.namedItem("plan") as HTMLSelectElement
  const stage = form.elements.namedItem("stage") as HTMLSelectElement
  const state = host.querySelector<HTMLElement>(".original-search-state")!
  const results = host.querySelector<HTMLElement>(".original-search-results")!
  const controller = new AbortController()
  const root = host.dataset.root!
  let pages: EvidencePage[] | undefined
  let request: Promise<EvidencePage[]> | undefined
  let generation = 0

  // Populate all choices before loading, so filters work on the first query.
  for (const [value, label] of Object.entries(stageLabels)) stage.add(new Option(label, value))
  const element = (tag: string, text: string) => {
    const node = document.createElement(tag)
    node.textContent = text
    return node
  }
  function link(text: string, href: string, external = false) {
    const a = document.createElement("a")
    a.textContent = text
    a.href = href
    if (external) { a.target = "_blank"; a.rel = "noopener noreferrer" }
    return a
  }
  async function load() {
    if (pages) return pages
    if (!request) request = fetch(`${root}/static/official-pages.json`, { signal: controller.signal })
      .then(async r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        const data = await r.json()
        if (!Array.isArray(data.pages)) throw new Error("Invalid index")
        pages = data.pages as EvidencePage[]
        return pages
      }).catch(e => { request = undefined; throw e })
    return request
  }
  async function run(event?: Event) {
    event?.preventDefault()
    const current = ++generation
    const value = query.value.trim()
    results.replaceChildren()
    if (!value) { state.textContent = "검색어를 입력하세요."; return }
    state.textContent = "원문 색인을 불러오는 중입니다…"
    try {
      const evidence = await load()
      if (controller.signal.aborted || current !== generation) return
      const found = rankEvidence(evidence, value, plan.value, stage.value)
      state.textContent = found.length ? `${found.length}개 페이지를 찾았습니다. 최대 25개를 표시합니다. PDF 파일의 쪽수입니다.` : "일치하는 원문 페이지가 없습니다. 검색어나 필터를 바꿔보세요. PDF 미확보·이미지 페이지는 검색되지 않습니다."
      for (const page of found.slice(0, 25)) {
        const card = document.createElement("article")
        const heading = document.createElement("h3")
        heading.append(link(page.title, `${root}/${page.slug}`))
        card.append(heading, element("p", `제${page.plan_number}차 · ${stageLabels[page.document_stage] ?? page.document_stage} · PDF p.${page.pdf_page} · ${page.published_date ?? "발행일 미확인"}`))
        card.append(element("p", evidenceSnippet(page.text, value)))
        if (page.sparse_text) card.append(element("p", "추출된 글자가 적은 페이지입니다. 표지 또는 이미지 포함 여부를 PDF에서 확인하세요."))
        const actions = document.createElement("p")
        actions.className = "original-search-links"
        actions.append(link(`공식 PDF p.${page.pdf_page} ↗`, page.citation_url, true), link("공식 게시물 ↗", page.source_url, true), link("보존 원본 ↗", page.archive_url, true))
        card.append(actions)
        const details = document.createElement("details")
        details.append(element("summary", "이 페이지의 추출 텍스트 보기"), element("p", `${page.attachment_title} · 자동 추출·검수 대기. 표·각주는 PDF에서 대조하세요.`), element("pre", page.text))
        card.append(details)
        results.append(card)
      }
    } catch (e) {
      if (!controller.signal.aborted && current === generation) state.textContent = "원문 색인을 불러오지 못했습니다. 연결을 확인한 뒤 검색을 다시 눌러주세요."
    }
  }
  form.addEventListener("submit", run)
  plan.addEventListener("change", run)
  stage.addEventListener("change", run)
  window.addCleanup(() => {
    controller.abort()
    form.removeEventListener("submit", run)
    plan.removeEventListener("change", run)
    stage.removeEventListener("change", run)
  })
})
