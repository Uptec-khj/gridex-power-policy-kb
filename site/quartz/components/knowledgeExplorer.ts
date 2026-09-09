import type { Options } from "./Explorer"

// Explorer serializes these functions for the browser; keep them self-contained.
export const knowledgeExplorer: Partial<Options> = {
  title: "자료 탐색",
  folderClickBehavior: "collapse",
  folderDefaultState: "collapsed",
  useSavedState: true,
  order: ["filter", "map", "sort"],
  filterFn: (node) => node.slugSegment !== "tags",
  mapFn: (node) => {
    const labels: Record<string, string> = {
      "regions/index": "국가별 자료", "plans/index": "전력수급계획", "documents/index": "공식 문서 전체",
      "project/index": "자료 검수", "regions/kr": "대한민국", "regions/au": "호주",
      "regions/us": "미국", "regions/cn": "중국", "regions/europe": "유럽",
      "plans/plan-10": "제10차 전력수급기본계획", "plans/plan-11": "제11차 전력수급기본계획",
      "plans/plan-12": "제12차 수립 과정", "document-search": "국가별 문서 찾기",
      "original-search": "PDF 원문 검색", "catalog": "전체 문서 목록", "timeline": "정책 연표",
      "energy-renewable-plans": "에너지·재생에너지 계획", "transmission-plans": "송변전설비계획",
      "demand-outlook": "장기 전력수요전망", "technical-documents": "계통연계·성능평가 기준",
      "reading-guide": "이용 안내", "collection-status": "자료 확보 현황",
      "extraction-status": "원문 추출 현황", "legal-basis": "관련 법령",
    }
    if (labels[node.slug]) node.displayName = labels[node.slug]
  },
  sortFn: (a, b) => {
    const priority: Record<string, number> = {
      "regions/index": 0, "plans/index": 10, "energy-renewable-plans": 11,
      "transmission-plans": 12, "demand-outlook": 13, "technical-documents": 14,
      "documents/index": 20, "document-search": 30, "original-search": 31,
      "catalog": 32, "timeline": 33, "reading-guide": 40, "legal-basis": 41,
      "collection-status": 42, "extraction-status": 43, "project/index": 44,
      "regions/kr": 0, "regions/au": 1, "regions/us": 2, "regions/cn": 3, "regions/europe": 4,
      "plans/plan-10": 0, "plans/plan-11": 1, "plans/plan-12": 2,
    }
    const difference = (priority[a.slug] ?? 100) - (priority[b.slug] ?? 100)
    if (difference) return difference
    if (a.slug.startsWith("documents/") && b.slug.startsWith("documents/")) {
      const byDate = (Date.parse(String(b.data?.published_date ?? "")) || 0) - (Date.parse(String(a.data?.published_date ?? "")) || 0)
      if (byDate) return byDate
    }
    return a.displayName.localeCompare(b.displayName, "ko", {numeric:true, sensitivity:"base"})
  },
}
