function StatusNotice({ type = 'empty', title, message }) {
  const noticeStyles = {
    empty: 'border-slate-200 bg-slate-50 text-slate-700',
    loading: 'border-sky-200 bg-sky-50 text-sky-800',
    error: 'border-red-200 bg-red-50 text-red-800',
  }

  return (
    <div className={`rounded-lg border p-5 ${noticeStyles[type] || noticeStyles.empty}`}>
      <strong className="block text-base">{title}</strong>
      {message && <p className="mt-2 text-sm leading-6">{message}</p>}
    </div>
  )
}

export default StatusNotice
