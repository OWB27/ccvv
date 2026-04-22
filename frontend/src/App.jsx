import { useEffect, useState } from 'react'
import './App.css'

import { fetchHealthStatus } from './api/health'
import { matchResumeWithJd } from './api/resume'

function App() {
  const [resumeFile, setResumeFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [healthState, setHealthState] = useState({
    loading: true,
    error: '',
    data: null,
  })
  const [extractState, setExtractState] = useState({
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
    setExtractState({ loading: false, error: '', data: null })
  }

  async function handleSubmit(event) {
    event.preventDefault()

    if (!resumeFile) {
      setExtractState({ loading: false, error: '请先选择一个 PDF 简历文件。', data: null })
      return
    }
    if (!jobDescription.trim()) {
      setExtractState({ loading: false, error: '请先填写岗位 JD。', data: null })
      return
    }

    setExtractState({ loading: true, error: '', data: null })

    try {
      const data = await matchResumeWithJd(resumeFile, jobDescription)
      setExtractState({ loading: false, error: '', data })
    } catch (error) {
      setExtractState({
        loading: false,
        error: error.message || '简历匹配失败',
        data: null,
      })
    }
  }

  const healthText = healthState.loading
    ? '正在连接后端...'
    : healthState.error
      ? '后端联调失败'
      : '后端联调正常'

  const extracted = extractState.data?.resume
  const match = extractState.data?.match
  const jd = extractState.data?.jd

  return (
    <main className="app-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">CCVV - AI Resume Analyzer</p>
          <h1>智能简历分析系统</h1>
          <p className="subtitle">上传 PDF 简历并填写 JD，提取关键信息后计算岗位匹配评分。</p>
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
            {resumeFile ? `已选择：${resumeFile.name}` : '请选择一个 PDF 文件。'}
          </p>
        </section>

        <section className="panel">
          <h2>岗位 JD</h2>
          <textarea
            value={jobDescription}
            onChange={(event) => setJobDescription(event.target.value)}
            placeholder="粘贴岗位描述，用于提取关键词并计算匹配评分。"
            rows="9"
          />
        </section>

        <section className="actions">
          <button type="submit" disabled={extractState.loading}>
            {extractState.loading ? '提取中...' : '提交分析'}
          </button>
        </section>

        <section className="panel result-panel">
          <h2>结构化结果</h2>
          {extractState.error && <p className="error-text">{extractState.error}</p>}
          {!extractState.error && !extractState.data && (
            <pre>等待上传 PDF 后展示结构化提取结果。</pre>
          )}
          {extractState.data && extracted && (
            <div className="result-content">
              {match && (
                <section className="match-summary">
                  <div>
                    <span>匹配分数</span>
                    <strong>{match.score}</strong>
                  </div>
                  <p>{match.summary}</p>
                  <dl className="score-breakdown">
                    <div>
                      <dt>方式</dt>
                      <dd>{match.scoring_method === 'ai' ? 'LLM' : '规则'}</dd>
                    </div>
                    <div>
                      <dt>技能</dt>
                      <dd>{match.breakdown.skill_score}/45</dd>
                    </div>
                    <div>
                      <dt>学历</dt>
                      <dd>{match.breakdown.education_score}/15</dd>
                    </div>
                    <div>
                      <dt>经验</dt>
                      <dd>{match.breakdown.experience_score}/25</dd>
                    </div>
                    <div>
                      <dt>项目</dt>
                      <dd>{match.breakdown.project_score}/15</dd>
                    </div>
                  </dl>
                </section>
              )}

              {jd && (
                <section className="keyword-section">
                  <h3>JD 关键词</h3>
                  <div className="keyword-list">
                    {jd.keywords.length
                      ? jd.keywords.slice(0, 20).map((keyword) => (
                          <span key={keyword}>{keyword}</span>
                        ))
                      : <span>未识别到关键词</span>}
                  </div>
                </section>
              )}

              {match?.explanations?.length > 0 && (
                <section className="nested-result">
                  <h3>匹配说明</h3>
                  <ul className="explanation-list">
                    {match.explanations.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </section>
              )}

              <dl className="result-meta">
                <div>
                  <dt>文件名</dt>
                  <dd>{extractState.data.filename}</dd>
                </div>
                <div>
                  <dt>页数</dt>
                  <dd>{extractState.data.page_count}</dd>
                </div>
                <div>
                  <dt>提取方式</dt>
                  <dd>{extractState.data.extraction_method}</dd>
                </div>
                <div>
                  <dt>警告</dt>
                  <dd>{extractState.data.warnings?.length || 0}</dd>
                </div>
              </dl>

              {extractState.data.warnings?.length > 0 && (
                <div className="warning-box">
                  {extractState.data.warnings.map((warning) => (
                    <p key={warning}>{warning}</p>
                  ))}
                </div>
              )}

              <div className="structured-grid">
                <Field label="姓名" value={extracted.name} />
                <Field label="电话" value={extracted.phone} />
                <Field label="邮箱" value={extracted.email} />
                <Field label="地址" value={extracted.address} />
                <Field label="求职意向" value={extracted.job_intention} />
                <Field label="期望薪资" value={extracted.expected_salary} />
                <Field label="工作年限" value={extracted.years_of_experience} />
              </div>

              <ListSection title="学历背景" items={extracted.education} emptyText="暂无学历信息" />
              <ListSection
                title="工作经历"
                items={extracted.work_experience}
                emptyText="暂无工作经历"
              />
              <ListSection title="项目经历" items={extracted.projects} emptyText="暂无项目经历" />

              <h3>清洗后文本预览</h3>
              <pre>{extractState.data.cleaned_text_preview || '未提取到可展示文本。'}</pre>
            </div>
          )}
        </section>
      </form>
    </main>
  )
}

function Field({ label, value }) {
  return (
    <div className="field-item">
      <span>{label}</span>
      <strong>{value || '未识别'}</strong>
    </div>
  )
}

function ListSection({ title, items, emptyText }) {
  return (
    <section className="nested-result">
      <h3>{title}</h3>
      {!items?.length && <p className="helper-text">{emptyText}</p>}
      {items?.map((item, index) => (
        <pre key={`${title}-${index}`}>{JSON.stringify(item, null, 2)}</pre>
      ))}
    </section>
  )
}

export default App
