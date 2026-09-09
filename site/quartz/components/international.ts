import taxonomy from "../../../schemas/international-taxonomy.json"
export { taxonomy }

export interface InternationalMetadata {
  region_group?: string
  jurisdictions?: string[]
  market_regions?: string[]
  document_language?: string
  document_type?: string
  title_original?: string | null
  title_ko?: string | null
  document_identifier?: string | null
  edition_year?: number | null
  version?: string | null
}
export interface DocumentFilters {
  region?: string; jurisdiction?: string; market?: string; language?: string; type?: string
}
export const regionLabel = (value?: string) => taxonomy.regions.find(r => r.id === value)?.label ?? "지역 미확인"
export const typeLabel = (value?: string) => taxonomy.document_types[value as keyof typeof taxonomy.document_types] ?? "문서 종류 미확인"
export function matchesFilters(meta: InternationalMetadata, filters: DocumentFilters = {}) {
  return (!filters.region || meta.region_group === filters.region) &&
    (!filters.jurisdiction || meta.jurisdictions?.includes(filters.jurisdiction)) &&
    (!filters.market || meta.market_regions?.includes(filters.market)) &&
    (!filters.language || meta.document_language === filters.language) &&
    (!filters.type || meta.document_type === filters.type)
}

// Each page owns the listeners and their cleanup. Dependent filters are reset only
// on an explicit region change, never silently when restoring a shared URL.
export function setupRegionFilters(form: HTMLFormElement) {
  const params = new URLSearchParams(location.search)
  for (const name of ["query", "region", "jurisdiction", "market", "language", "type", "stage", "plan"]) {
    const control = form.elements.namedItem(name) as HTMLInputElement | HTMLSelectElement | null
    if (control && params.has(name)) {
      const value = params.get(name)!
      if (control instanceof HTMLSelectElement && !Array.from(control.options).some(o => o.value === value)) {
        control.add(new Option("알 수 없는 선택", value))
      }
      control.value = value
    }
  }
  const region = form.elements.namedItem("region") as HTMLSelectElement
  function narrow(reset = false) {
    for (const [name, choices] of [["jurisdiction", taxonomy.jurisdictions], ["market", taxonomy.markets]] as const) {
      const select = form.elements.namedItem(name) as HTMLSelectElement
      if (reset) select.value = ""
      for (const option of Array.from(select.options)) {
        const item = choices.find(c => c.id === option.value)
        option.disabled = !!(item && region.value && item.region !== region.value)
      }
    }
    for (const a of document.querySelectorAll<HTMLAnchorElement>(".country-navigation a")) {
      if (a.dataset.region === region.value) a.setAttribute("aria-current", "page")
      else a.removeAttribute("aria-current")
    }
  }
  narrow()
  const onRegion = () => narrow(true)
  region.addEventListener("change", onRegion)
  window.addCleanup(() => region.removeEventListener("change", onRegion))
  return () => {
    const data = new FormData(form)
    const url = new URL(location.href)
    url.search = ""
    for (const [key, value] of data) if (typeof value === "string" && value) url.searchParams.set(key, value)
    history.replaceState(history.state, "", url)
    return Object.fromEntries(data) as Record<string, string>
  }
}
