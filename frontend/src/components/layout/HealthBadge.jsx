function HealthBadge({ state }) {
  const text = state.loading
    ? '正在连接后端...'
    : state.error
      ? '后端联调失败'
      : '后端联调正常'

  return (
    <div
      className={`grid min-w-48 gap-1 rounded-lg border px-4 py-3 text-left text-sm ${
        state.error
          ? 'border-red-200 bg-red-50 text-red-800'
          : 'border-sky-200 bg-sky-50 text-slate-800'
      }`}
    >
      <span className="font-semibold">{text}</span>
      {state.data && <small className="text-current opacity-75">{state.data.service}</small>}
      {state.error && <small className="text-current opacity-75">{state.error}</small>}
    </div>
  )
}

export default HealthBadge
