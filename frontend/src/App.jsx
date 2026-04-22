import { useEffect, useState } from 'react'
import './App.css'

import { fetchHealthStatus } from './api/health'

function App() {
  const [resumeFileName, setResumeFileName] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [healthState, setHealthState] = useState({
    loading: true,
    error: '',
    data: null,
  })
  const [resultMessage, setResultMessage] = useState('等待接入真实分析接口。')

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
    const file = event.target.files?.[0]
    setResumeFileName(file ? file.name : '')
  }

  function handleSubmit(event) {
    event.preventDefault()
    setResultMessage('Stage 2 仅完成页面壳子，真实分析将在后续阶段接入。')
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
          <p className="eyebrow">AI Resume Analyzer</p>
          <h1>智能简历分析系统</h1>
          <p className="subtitle">上传简历、填写岗位 JD，后续将返回结构化分析结果。</p>
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
            {resumeFileName || '当前阶段只选择文件，不执行上传。'}
          </p>
        </section>

        <section className="panel">
          <h2>岗位 JD</h2>
          <textarea
            value={jobDescription}
            onChange={(event) => setJobDescription(event.target.value)}
            placeholder="粘贴岗位描述，后续阶段将用于匹配评分。"
            rows="9"
          />
        </section>

        <section className="actions">
          <button type="submit">提交分析</button>
        </section>

        <section className="panel result-panel">
          <h2>分析结果</h2>
          <pre>{resultMessage}</pre>
          <p className="helper-text">
            后续会在这里展示简历信息提取、JD 匹配评分和结构化 JSON。
          </p>
        </section>
      </form>
    </main>
  )
}

export default App
