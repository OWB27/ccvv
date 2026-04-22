import ExplanationList from './ExplanationList'
import FieldGrid from './FieldGrid'
import JsonListSection from './JsonListSection'
import KeywordList from './KeywordList'
import MatchSummary from './MatchSummary'
import MetricGrid from './MetricGrid'
import StatusNotice from '../feedback/StatusNotice'

function ResultDashboard({ state }) {
  if (state.loading) {
    return (
      <section className="ui-panel">
        <h2 className="ui-panel-title mb-4">分析结果</h2>
        <StatusNotice
          type="loading"
          title="正在分析简历与岗位匹配度"
          message="系统正在解析 PDF、提取简历信息、分析 JD 并计算匹配分。"
        />
      </section>
    )
  }

  if (state.error) {
    return (
      <section className="ui-panel">
        <h2 className="ui-panel-title mb-4">分析结果</h2>
        <StatusNotice type="error" title="分析失败" message={state.error} />
      </section>
    )
  }

  if (!state.data) {
    return (
      <section className="ui-panel">
        <h2 className="ui-panel-title mb-4">分析结果</h2>
        <StatusNotice
          title="等待提交"
          message="选择 PDF 简历并填写岗位 JD 后，这里会展示匹配分数、关键词和结构化简历结果。"
        />
      </section>
    )
  }

  const data = state.data
  const resume = data.resume

  return (
    <section className="ui-panel">
      <div className="mb-5">
        <div>
          <h2 className="ui-panel-title">分析结果</h2>
          <p className="ui-muted-text mt-1">已完成简历结构化提取与 JD 匹配评分。</p>
        </div>
      </div>

      <div className="grid gap-5">
        <MatchSummary match={data.match} />
        <KeywordList title="JD 关键词" keywords={data.jd?.keywords} />
        <ExplanationList explanations={data.match?.explanations} />

        <MetricGrid
          items={[
            { label: '文件名', value: data.filename },
            { label: '页数', value: data.page_count },
            { label: '简历提取', value: data.extraction_method === 'ai' ? 'LLM' : 'Fallback' },
            { label: '解析缓存', value: data.parse_cache_hit ? '命中' : '未命中' },
            { label: '匹配缓存', value: data.match_cache_hit ? '命中' : '未命中' },
            { label: '警告', value: data.warnings?.length || 0 },
          ]}
        />

        <MetricGrid
          items={[
            { label: '简历 Hash', value: data.resume_hash ? `${data.resume_hash.slice(0, 12)}...` : '无' },
            { label: 'JD Hash', value: data.jd_hash ? `${data.jd_hash.slice(0, 12)}...` : '无' },
          ]}
        />

        {data.warnings?.length > 0 && (
          <div className="ui-warning-box">
            {data.warnings.map((warning) => (
              <p key={warning}>{warning}</p>
            ))}
          </div>
        )}

        <section className="ui-section-stack">
          <h3 className="ui-section-title">简历基本信息</h3>
          <FieldGrid
            fields={[
              { label: '姓名', value: resume.name },
              { label: '电话', value: resume.phone },
              { label: '邮箱', value: resume.email },
              { label: '地址', value: resume.address },
              { label: '求职意向', value: resume.job_intention },
              { label: '期望薪资', value: resume.expected_salary },
              { label: '工作年限', value: resume.years_of_experience },
            ]}
          />
        </section>

        <JsonListSection title="学历背景" items={resume.education} emptyText="暂无学历信息" />
        <JsonListSection title="工作经历" items={resume.work_experience} emptyText="暂无工作经历" />
        <JsonListSection title="项目经历" items={resume.projects} emptyText="暂无项目经历" />

        <section className="ui-section-stack">
          <h3 className="ui-section-title">清洗后文本预览</h3>
          <pre className="ui-code-block min-h-28">
            {data.cleaned_text_preview || '未提取到可展示文本。'}
          </pre>
        </section>
      </div>
    </section>
  )
}

export default ResultDashboard
