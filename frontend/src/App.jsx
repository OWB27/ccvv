import { useEffect, useState } from 'react'
import './App.css'

import { fetchHealthStatus } from './api/health'
import { parseResumePdf } from './api/resume'

function App() {
  const [resumeFile, setResumeFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [healthState, setHealthState] = useState({
    loading: true,
    error: '',
    data: null,
  })
  const [parseState, setParseState] = useState({
    loading: false,
    error: '',
    data: null,
  })

  useEffect(() => {
    let ignore = false

    async function loadHealthStatus() {
      try {
        const data = await fetchHealthStatus()
        if (!ignore) {
          setHealthState({ loading: false, error: '', data })
        }
      } catch (error) {
        if (!ignore) {
          setHealthState({
            loading: false,
            error: error.message || '后端健康检查失败',
            data: null,
          })
        }
      }
    }

    loadHealthStatus()

    return () => {
      ignore = true
    }
  }, [])

  function handleFileChange(event) {
    const file = event.target.files?.[0] || null
    setResumeFile(file)
    setParseState({ loading: false, error: '', data: null })
  }

  async function handleSubmit(event) {
    event.preventDefault()

    if (!resumeFile) {
      setParseState({ loading: false, error: '请先选择一个 PDF 简历文件。', data: null })
      return
    }

    setParseState({ loading: true, error: '', data: null })

    try {
      const data = await parseResumePdf(resumeFile)
      setParseState({ loading: false, error: '', data })
    } catch (error) {
      setParseState({
        loading: false,
        error: error.message || 'PDF 解析失败',
        data: null,
      })
    }
  }

  const healthText = healthState.loading
    ? '正在连接后端...'
    : healthState.error
      ? '后端联调失败'
      : '后端联调正常'

  return (
    <main className="app-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">CCVV - AI Resume Analyzer</p>
          <h1>智能简历分析系统</h1>
          <p className="subtitle">上传 PDF 简历并填写岗位 JD，后续将接入 AI 提取和匹配评分。</p>
        </div>
        <div className={`health-badge ${healthState.error ? 'error' : 'ok'}`}>
          <span>{healthText}</span>
          {healthState.data && <small>{healthState.data.service}</small>}
          {healthState.error && <small>{healthState.error}</small>}
        </div>
      </header>

      <form className="workspace" onSubmit={handleSubmit}>
        <section className="panel">
          <h2>PDF 简历</h2>
          <label className="upload-box">
            <span>选择 PDF 文件</span>
            <input type="file" accept="application/pdf,.pdf" onChange={handleFileChange} />
          </label>
          <p className="helper-text">
            {resumeFile ? `已选择：${resumeFile.name}` : '请选择一个 PDF 文件，当前阶段会提取文本。'}
          </p>
        </section>

        <section className="panel">
          <h2>岗位 JD</h2>
          <textarea
            value={jobDescription}
            onChange={(event) => setJobDescription(event.target.value)}
            placeholder="粘贴岗位描述。当前阶段暂不做 JD 匹配。"
            rows="9"
          />
        </section>

        <section className="actions">
          <button type="submit" disabled={parseState.loading}>
            {parseState.loading ? '解析中...' : '提交分析'}
          </button>
        </section>

        <section className="panel result-panel">
          <h2>解析结果</h2>
          {parseState.error && <p className="error-text">{parseState.error}</p>}
          {!parseState.error && !parseState.data && (
            <pre>等待上传 PDF 后展示文本预览。</pre>
          )}
          {parseState.data && (
            <div className="result-content">
              <dl className="result-meta">
                <div>
                  <dt>文件名</dt>
                  <dd>{parseState.data.filename}</dd>
                </div>
                <div>
                  <dt>页数</dt>
                  <dd>{parseState.data.page_count}</dd>
                </div>
                <div>
                  <dt>原始文本长度</dt>
                  <dd>{parseState.data.raw_text_length}</dd>
                </div>
                <div>
                  <dt>清洗后文本长度</dt>
                  <dd>{parseState.data.cleaned_text_length}</dd>
                </div>
              </dl>
              <h3>清洗后文本预览</h3>
              <pre>{parseState.data.cleaned_text_preview || '未提取到可展示文本。'}</pre>
            </div>
          )}
        </section>
      </form>
    </main>
  )
}

export default App
