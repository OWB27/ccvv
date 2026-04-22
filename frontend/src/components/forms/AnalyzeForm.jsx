import { useState } from 'react'

function AnalyzeForm({ loading, onAnalyze, onInputChange }) {
  const [resumeFile, setResumeFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const canSubmit = Boolean(resumeFile) && jobDescription.trim().length > 0 && !loading

  function handleFileChange(event) {
    const file = event.target.files?.[0] || null
    setResumeFile(file)
    onInputChange?.()
  }

  function handleJobDescriptionChange(event) {
    setJobDescription(event.target.value)
    onInputChange?.()
  }

  function handleSubmit(event) {
    event.preventDefault()

    if (!resumeFile || !jobDescription.trim()) {
      return
    }

    onAnalyze({
      resumeFile,
      jobDescription: jobDescription.trim(),
    })
  }

  return (
    <form className="mb-5 grid gap-5 lg:grid-cols-2" onSubmit={handleSubmit}>
      <section className="ui-panel">
        <div className="mb-4 flex gap-3">
          <span className="ui-step-badge">1</span>
          <div>
            <h2 className="ui-panel-title">PDF 简历</h2>
            <p className="ui-muted-text mt-1">支持单个 PDF 文件，提交后会自动解析并提取信息。</p>
          </div>
        </div>
        <label
          className={`ui-upload-box ${
            resumeFile
              ? 'border-sky-400 bg-sky-50 text-sky-800'
              : 'border-slate-300 bg-slate-50 text-slate-700 hover:border-sky-400 hover:bg-sky-50'
          }`}
        >
          <span className="font-semibold">{resumeFile ? '重新选择 PDF' : '选择 PDF 文件'}</span>
          <input className="mt-3 max-w-full text-sm" type="file" accept="application/pdf,.pdf" onChange={handleFileChange} />
        </label>
        <p className="ui-helper-text">
          {resumeFile ? `已选择：${resumeFile.name}` : '请选择一个 PDF 文件。'}
        </p>
      </section>

      <section className="ui-panel">
        <div className="mb-4 flex gap-3">
          <span className="ui-step-badge">2</span>
          <div>
            <h2 className="ui-panel-title">岗位 JD</h2>
            <p className="ui-muted-text mt-1">粘贴岗位描述，用于提取关键词并计算匹配评分。</p>
          </div>
        </div>
        <textarea
          className="ui-textarea"
          value={jobDescription}
          onChange={handleJobDescriptionChange}
          placeholder="例如：负责 Python 后端服务开发，熟悉 FastAPI、SQL、Docker，有 3 年以上经验..."
          rows="10"
        />
        <p className="ui-helper-text">已输入 {jobDescription.trim().length} 个字符。</p>
      </section>

      <section className="ui-panel flex justify-end lg:col-span-2">
        <button
          className="ui-primary-button"
          type="submit"
          disabled={!canSubmit}
        >
          {loading ? '分析中...' : '提交分析'}
        </button>
      </section>
    </form>
  )
}

export default AnalyzeForm
