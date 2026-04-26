import { useEffect, useState } from 'react'

import { fetchHealthStatus } from '../../api/health'
import BrandLogo from './BrandLogo'
import HealthBadge from './HealthBadge'

function PageHeader() {
  const [healthState, setHealthState] = useState({
    loading: true,
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

  return (
    <header className="ui-header">
      <div>
        <h1 className="ui-hero-title">简历与岗位匹配分析</h1>
        <p className="ui-hero-copy">
          上传 PDF 简历，粘贴岗位 JD。系统会提取候选人信息、识别岗位关键词，并给出一份清晰的匹配报告。
        </p>
      </div>
      <div className="ui-header-aside">
        <BrandLogo />
        <HealthBadge state={healthState} />
      </div>
    </header>
  )
}

export default PageHeader
