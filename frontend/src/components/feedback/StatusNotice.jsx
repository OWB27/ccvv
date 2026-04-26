function StatusNotice({ type = 'empty', title, message }) {
  const noticeClass = {
    empty: 'ui-status-empty',
    loading: 'ui-status-loading',
    error: 'ui-status-error',
  }[type] || 'ui-status-empty'

  return (
    <div className={`ui-status ${noticeClass}`}>
      <strong className="block text-base font-medium">{title}</strong>
      {message && <p className="mt-2 text-sm leading-[1.6]">{message}</p>}
    </div>
  )
}

export default StatusNotice
