// Validate generated pages and the actual Quartz search configuration without a browser.
import fs from "node:fs"
import path from "node:path"
import assert from "node:assert/strict"
import { fileURLToPath } from "node:url"
import { createRequire } from "node:module"

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..")
const require = createRequire(path.join(root, "site/package.json"))
const { transformSync } = require("esbuild")
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
