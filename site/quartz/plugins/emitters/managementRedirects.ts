import { QuartzEmitterPlugin } from "../types"
import { FullSlug } from "../../util/path"
import { write } from "./helpers"

// Compatibility routes only: these are not Markdown documents, graph nodes,
// search records, sitemap entries or feed entries in the public knowledge base.
export const ManagementRedirects: QuartzEmitterPlugin = () => ({
  name: "ManagementRedirects",
  async *emit(ctx) {
    for (const name of ["roadmap", "development-backlog", "release-log", "international-roadmap"]) {
      const url = "../document-search"
      yield await write({ctx, slug: `project/${name}` as FullSlug, ext: ".html",
        content: `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>개발 문서 안내</title></head><body><p>개발 문서는 공개 사이트의 제공 범위에 포함되지 않습니다.</p><a href="${url}">공개 문서 찾기</a></body></html>`})
    }
  },
})
