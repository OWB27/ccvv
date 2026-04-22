import { useState } from 'react'

import { matchResumeWithJd } from '../../api/resume'
import AnalyzeForm from '../forms/AnalyzeForm'
import ResultDashboard from '../results/ResultDashboard'

function ResumeAnalysisWorkspace() {
  const [analysisState, setAnalysisState] = useState({
    loading: false,
    error: '',
    data: null,
  })

  async function handleAnalyze({ resumeFile, jobDescription }) {
    setAnalysisState({ loading: true, error: '', data: null })

    try {
      const data = await matchResumeWithJd(resumeFile, jobDescription)
      setAnalysisState({ loading: false, error: '', data })
    } catch (error) {
      setAnalysisState({
        loading: false,
        error: error.message || '简历匹配失败',
        data: null,
      })
    }
  }

  function handleInputChange() {
    if (analysisState.data || analysisState.error) {
      setAnalysisState({ loading: false, error: '', data: null })
    }
  }

  return (
    <>
      <AnalyzeForm
        loading={analysisState.loading}
        onAnalyze={handleAnalyze}
        onInputChange={handleInputChange}
      />
      <ResultDashboard state={analysisState} />
    </>
  )
}

export default ResumeAnalysisWorkspace
