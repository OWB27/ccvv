import { isNonEmptyArray } from '../../utils/display'

function JsonListSection({ title, items, emptyText }) {
  return (
    <section className="ui-section-stack">
      <h3 className="ui-section-title">{title}</h3>
      {!isNonEmptyArray(items) && <p className="ui-metric-card ui-muted-text">{emptyText}</p>}
      {items?.map((item, index) => (
        <pre className="ui-code-block min-h-24" key={`${title}-${index}`}>{JSON.stringify(item, null, 2)}</pre>
      ))}
    </section>
  )
}

export default JsonListSection
