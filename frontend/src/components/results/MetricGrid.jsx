function MetricGrid({ items }) {
  return (
    <dl className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      {items.map((item) => (
        <div className="ui-metric-card" key={item.label}>
          <dt className="ui-muted-text">{item.label}</dt>
          <dd className="mt-1 break-words font-bold text-slate-900">{item.value}</dd>
        </div>
      ))}
    </dl>
  )
}

export default MetricGrid
