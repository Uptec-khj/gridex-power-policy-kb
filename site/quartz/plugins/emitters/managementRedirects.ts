import { QuartzEmitterPlugin } from "../types"
import { FullSlug } from "../../util/path"
import { write } from "./helpers"

// Compatibility routes only: these are not Markdown documents, graph nodes,
// search records, sitemap entries or feed entries in the public knowledge base.
export const ManagementRedirects: QuartzEmitterPlugin = () => ({
  name: "ManagementRedirects",
  async *emit(ctx) {
    for (const name of ["roadmap", "development-backlog", "release-log", "international-roadmap"]) {
      const url = `https://github.com/Uptec-khj/gridex-power-policy-kb-dev/blob/main/content/${name}.md`
      yield await write({ctx, slug: `project/${name}` as FullSlug, ext: ".html",
        content: `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=${url}"><link rel="canonical" href="${url}"><title>개발 관리 문서 이전</title></head><body><p>개발 관리 문서를 별도 저장소로 옮겼습니다.</p><a href="${url}">GitHub에서 문서 읽기</a></body></html>`})
    }
  },
})
