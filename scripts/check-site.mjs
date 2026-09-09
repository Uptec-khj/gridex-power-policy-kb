// Validate generated pages and the actual Quartz search configuration without a browser.
import fs from "node:fs"
import path from "node:path"
import assert from "node:assert/strict"
import { fileURLToPath } from "node:url"
import { createRequire } from "node:module"

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..")
const require = createRequire(path.join(root, "site/package.json"))
const { transformSync, buildSync } = require("esbuild")
const FlexSearch = require("flexsearch")
const content = JSON.parse(fs.readFileSync(path.join(root, "site/public/static/contentIndex.json"), "utf8"))
const source = fs.readFileSync(path.join(root, "site/quartz/components/scripts/search.inline.ts"), "utf8")
const configuration = source.slice(source.indexOf("const encoder ="), source.indexOf("const p = new DOMParser()"))
assert(configuration.includes("let index = new FlexSearch.Document"))
const compiled = transformSync(configuration, { loader: "ts", format: "cjs" }).code
const index = new Function("FlexSearch", `${compiled}; return index;`)(FlexSearch)
for (const [id, record] of Object.entries(content)) index.add({ id, ...record })
for (const [query, expected] of [["수요전망", "documents/p11-demand"], ["수정 공고", "documents/p11-amend"], ["12차", "documents/p12-launch"], ["송변전", "documents/t11-final"], ["환경평가", "documents/p10-sea-scope"], ["조기폐지", "documents/p12-forum7"]]) {
  const result = index.search(query, { limit: 100 })
  const ids = result.flatMap(group => group.result)
  assert(ids.includes(expected), `${query} must find ${expected}`)
}
assert(content["documents/p11-final"].links.includes("documents/p11-amend"), "Version edge must be present in graph index")
assert(content["documents/t11-final"].links.includes("documents/t10-final"), "Transmission plans must be connected")
const publicDocuments = JSON.parse(fs.readFileSync(path.join(root, "data/metadata/documents.json"), "utf8"))
assert.equal(Object.keys(content).filter(id => id.startsWith("documents/")).length, publicDocuments.length)
const latest = fs.readFileSync(path.join(root, "site/public/documents/p12-forum7.html"), "utf8")
assert(latest.includes("2026-09-18") && latest.includes("개최 예정"), "Future forum must retain its scheduled status")
for (const slug of ["index", "timeline", "catalog", "documents/p11-amend"]) {
  const html = fs.readFileSync(path.join(root, "site/public", slug + ".html"), "utf8")
  assert(html.includes("GRIDEX"))
  if (slug.startsWith("documents/")) {
    assert(html.includes("AI 요약 · 검수 대기"))
    assert(html.includes("2025-03-13"))
  }
}
console.log(`Site smoke checks passed: ${Object.keys(content).length} indexed pages, Korean search, graph edge, review labels`)

// Exercise the exact ranking code shipped to the browser against real PDF pages.
const evidence = JSON.parse(fs.readFileSync(path.join(root, "site/public/static/official-pages.json"), "utf8"))
const core = fs.readFileSync(path.join(root, "site/quartz/components/scripts/originalSearchCore.ts"), "utf8")
const coreCode = buildSync({stdin:{contents:core, loader:'ts', resolveDir:path.join(root,'site/quartz/components/scripts')}, bundle:true, write:false, format:'cjs', platform:'browser'}).outputFiles[0].text
const coreModule = { exports: {} }
new Function("module", "exports", coreCode)(coreModule, coreModule.exports)
const { rankEvidence } = coreModule.exports
for (const [query, plan, stage, id, page] of [
  ["송변전 61183", "11", "final", "t11-final", 14],
  ["송변전 57,681", "10", "final", "t10-final", 13],
  ["72.8", "11", "press_release", "t11-release", 2],
]) {
  const found = rankEvidence(evidence.pages, query, plan, stage)
  assert(found.some(p => p.document_id === id && p.pdf_page === page), `Original search: ${query}`)
  assert(found.every(p => String(p.plan_number) === plan && p.document_stage === stage))
}
assert.equal(rankEvidence(evidence.pages, "", "", "").length, 0)
assert.equal(rankEvidence(evidence.pages, "송변전 zzz-does-not-exist", "", "").length, 0)
assert(evidence.pages.every(p => p.content_origin === "official_extraction" && p.extraction_review_status === "unreviewed"))
const originalPage = fs.readFileSync(path.join(root, "site/public/original-search.html"), "utf8")
assert(originalPage.includes('class="original-search"') && originalPage.includes('name="stage"'))
assert(content["project/roadmap"].links.includes("project/development-backlog"))
const technical = rankEvidence(evidence.pages, "유효전력", "technical", "supporting")
assert(technical.some(p => p.document_id === 'tech-field-test-appendix6' && p.pdf_page === 1))
assert(technical.every(p => p.plan_number === null))
assert(!rankEvidence(evidence.pages, '유효전력', '11').some(p => p.document_id.startsWith('tech-')))
assert(rankEvidence(evidence.pages, '657.6', '12', 'draft').some(p => p.document_id === 'p12-demand-draft-20260519' && p.pdf_page === 6))
assert(!rankEvidence(evidence.pages, '657.6', '12', 'final').length)
assert(evidence.pages.some(p => p.document_id === 'p11-final' && p.pdf_page === 1 && p.text.includes('169')))
for (const id of ['tech-field-test-appendix6', 'tech-grid-model-draft-202608']) {
  const html = fs.readFileSync(path.join(root, 'site/public/documents', id + '.html'), 'utf8')
  assert(!html.includes('제null차') && !html.includes('제undefined차'))
  assert(html.includes('AI 요약 · 검수 대기'))
}
assert(content['technical-documents'].links.includes('documents/tech-field-test-appendix6'))
assert(content['project/review-queue'].links.includes('documents/tech-grid-model-draft-202608'))
const relations = JSON.parse(fs.readFileSync(path.join(root, 'data/metadata/relations.json'), 'utf8'))
assert(relations.some(r => r.type === 'explains' && r.target === 'tech-field-test-appendix6' && r.source_url && r.basis))
for (const [family, query, id, page] of [
  ['에너지기본계획', '재생에너지', 'energy-3-final', 53],
  ['신재생에너지기본계획', '25.8', 'renewable-5-final', 6],
  ['재생에너지기본계획', '100GW', 'renewable-1-final-2026', 17],
]) {
  const found = rankEvidence(evidence.pages, query, 'family:' + family, 'final')
  assert(found.some(p => p.document_id === id && p.pdf_page === page))
  assert(found.every(p => p.plan_family === family))
}
const collision = [{ ...evidence.pages[0], text: 'same', plan_number: 1, plan_family: '에너지기본계획' },
  { ...evidence.pages[0], text: 'same', plan_number: 1, plan_family: '재생에너지기본계획' }]
assert.equal(rankEvidence(collision, 'same', 'family:재생에너지기본계획').length, 1)
assert(content['energy-renewable-plans'].links.includes('documents/renewable-1-final-2026'))
console.log(`Original search passed: ${evidence.report.searchable_pages} pages with text, PDF citations and plan/stage filters`)

// Region filters must never broaden to Korea when the requested region is empty.
assert.equal(rankEvidence(evidence.pages, '전력', '', '', {region:'AU'}).length, 0)
assert(rankEvidence(evidence.pages, '전력', '', '', {region:'KR', jurisdiction:'KR', language:'ko'}).length > 0)
assert.equal(rankEvidence(evidence.pages, '전력', '', '', {region:'KR', language:'en'}).length, 0)
const fixture = {...evidence.pages[0], title:'국제 계획', title_original:'Integrated System Plan', text:'power',
  region_group:'AU', jurisdictions:['AU'], market_regions:['NEM'], document_language:'en', document_type:'plan', plan_number:null}
assert.equal(rankEvidence([fixture], 'Integrated', '', '', {region:'AU', market:'NEM'}).length, 1)
assert.equal(rankEvidence([fixture], 'power', 'technical').length, 0, 'Null plan number is not a technical document')
assert.equal(rankEvidence([fixture], 'power', '', '', {market:'WEM'}).length, 0)
const multi = {...fixture, region_group:'Europe', jurisdictions:['EU','DE']}
for (const jurisdiction of ['EU','DE']) assert.equal(rankEvidence([multi], 'power', '', '', {jurisdiction}).length, 1)
for (const region of ['kr','au','us','cn','europe']) {
  const html = fs.readFileSync(path.join(root, 'site/public/regions', region + '.html'), 'utf8')
  assert(html.includes('aria-label="국가·지역별 자료"'))
  assert(html.includes(`href="../regions/${region}"`))
  const group = {kr:'KR',au:'AU',us:'US',cn:'CN',europe:'Europe'}[region]
  assert(html.includes(`document-search?region=${group}`), 'Country hub must retain its search filter URL')
  assert(region === 'kr' ? content['regions/kr'].links.includes('documents/p11-final') : html.includes('수집 준비 중'))
}
for (const slug of ['original-search','document-search']) {
  const html = fs.readFileSync(path.join(root, 'site/public', slug + '.html'), 'utf8')
  for (const name of ['region','jurisdiction','market','language','type']) assert(html.includes(`name="${name}"`))
}
assert(evidence.pages.every(p => p.region_group === 'KR' && p.document_language === 'ko' && p.document_type))
console.log('International navigation, region isolation, language/market filters and null-plan classification passed')
