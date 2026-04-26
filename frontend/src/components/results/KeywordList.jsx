import { isNonEmptyArray } from '../../utils/display'

function KeywordList({ title, keywords }) {
  return (
    <section className="ui-section-stack">
      <h3 className="ui-section-title">{title}</h3>
      <div className="flex flex-wrap gap-2">
        {isNonEmptyArray(keywords)
          ? keywords.slice(0, 24).map((keyword) => (
              <span className="ui-pill" key={keyword}>
                {keyword}
              </span>
            ))
          : <span className="ui-pill">未识别到关键词</span>}
      </div>
    </section>
  )
}

export default KeywordList
