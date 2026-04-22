import { isNonEmptyArray } from '../../utils/display'

function ExplanationList({ explanations }) {
  if (!isNonEmptyArray(explanations)) {
    return null
  }

  return (
    <section className="ui-section-stack">
      <h3 className="ui-section-title">匹配说明</h3>
      <ul className="grid gap-2 pl-5 text-slate-700">
        {explanations.map((item) => (
          <li className="list-disc" key={item}>{item}</li>
        ))}
      </ul>
    </section>
  )
}

export default ExplanationList
