import { QuartzComponent, QuartzComponentConstructor } from "./types"
import { pathToRoot } from "../util/path"
import { taxonomy } from "./international"
import style from "./styles/countryNavigation.scss"

export default (() => {
  const CountryNavigation: QuartzComponent = ({ fileData }) => {
    const root = pathToRoot(fileData.slug!)
    const current = fileData.frontmatter?.region_group as string | undefined
    return <nav class="country-navigation" aria-label="국가·지역별 자료">
      <a class="internal" href={`${root}/`} data-region="" aria-current={!current ? "page" : undefined}>전체</a>
      {taxonomy.regions.map(region => <a class="internal" href={`${root}/regions/${region.slug}`}
        data-region={region.id} aria-current={current === region.id ? "page" : undefined}>{region.label}</a>)}
    </nav>
  }
  CountryNavigation.css = style
  return CountryNavigation
}) satisfies QuartzComponentConstructor
