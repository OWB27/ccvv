function HealthBadge({ state }) {
  const text = state.loading
    ? '正在连接后端...'
    : state.error
      ? '后端联调失败'
      : '后端联调正常'

  return (
    <div className={`ui-health ${state.error ? 'ui-health-error' : ''}`}>
      <span className="font-medium">{text}</span>
      {state.data && <small className="text-current opacity-75">{state.data.service}</small>}
      {state.error && <small className="text-current opacity-75">{state.error}</small>}
    </div>
  )
}

export default HealthBadge
