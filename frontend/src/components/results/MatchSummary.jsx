import MetricGrid from './MetricGrid'

function MatchSummary({ match }) {
  if (!match) {
    return null
  }

  return (
    <section className="ui-summary-panel">
      <div className="flex flex-wrap items-baseline gap-3">
        <span className="text-sm font-medium ui-dark-muted">匹配分数</span>
        <strong className="text-5xl font-medium leading-none text-[#faf9f5]">{match.score}</strong>
        <em className="ui-pill ui-pill-brand bg-transparent not-italic">
          {match.scoring_method === 'ai' ? 'LLM 评分' : '规则评分'}
        </em>
      </div>
      <p className="leading-[1.6] ui-dark-muted">{match.summary}</p>
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
