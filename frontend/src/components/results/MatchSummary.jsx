import MetricGrid from './MetricGrid'

function MatchSummary({ match }) {
  if (!match) {
    return null
  }

  return (
    <section className="ui-summary-panel">
      <div className="flex flex-wrap items-baseline gap-3">
        <span className="text-sm font-medium text-slate-600">匹配分数</span>
        <strong className="text-5xl font-bold leading-none text-sky-700">{match.score}</strong>
        <em className="ui-pill bg-white not-italic text-slate-600">
          {match.scoring_method === 'ai' ? 'LLM 评分' : '规则评分'}
        </em>
      </div>
      <p className="text-slate-700">{match.summary}</p>
      <MetricGrid
        items={[
          { label: '技能', value: `${match.breakdown.skill_score}/45` },
          { label: '学历', value: `${match.breakdown.education_score}/15` },
          { label: '经验', value: `${match.breakdown.experience_score}/25` },
          { label: '项目', value: `${match.breakdown.project_score}/15` },
        ]}
      />
    </section>
  )
}

export default MatchSummary
