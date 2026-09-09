import fs from "node:fs/promises"
import { QuartzEmitterPlugin } from "../types"
import { FullSlug, QUARTZ, joinSegments } from "../../util/path"
import { write } from "./helpers"

// Static's glob intentionally respects .gitignore. This derived index is emitted
// explicitly so that it can remain untracked while still reaching the public site.
export const OriginalIndex: QuartzEmitterPlugin = () => ({
  name: "OriginalIndex",
  async *emit(ctx) {
    const content = await fs.readFile(joinSegments(QUARTZ, "static/official-pages.json"), "utf8")
    const data = JSON.parse(content)
    if (!Array.isArray(data.pages) || data.report.failed_files !== 0) {
      throw new Error("Build a valid original PDF index before publishing")
    }
    yield await write({ ctx, slug: "static/official-pages" as FullSlug, ext: ".json", content })
  },
})
