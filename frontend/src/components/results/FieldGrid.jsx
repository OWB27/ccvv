import { displayValue } from '../../utils/display'

function FieldGrid({ fields }) {
  return (
    <div className="grid gap-3 md:grid-cols-2">
      {fields.map((field) => (
        <div className="ui-field-card" key={field.label}>
          <span className="ui-muted-text">{field.label}</span>
          <strong className="ui-strong-text">{displayValue(field.value)}</strong>
        </div>
      ))}
    </div>
  )
}

export default FieldGrid
