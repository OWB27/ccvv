import { useEffect, useState } from 'react'

import { fetchHealthStatus } from '../../api/health'
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
    <header className="mb-8 grid gap-5 md:flex md:items-start md:justify-between">
      <div>
        <p className="mb-2 text-sm font-bold tracking-normal text-sky-700">CCVV - AI Resume Analyzer</p>
        <h1 className="text-4xl font-bold leading-tight text-slate-950">CCVV 简历分析系统</h1>
        <p className="mt-3 max-w-2xl text-base leading-7 text-slate-600">
          上传 PDF 简历并填写 JD，提取关键信息后计算岗位匹配评分。
        </p>
      </div>
      <HealthBadge state={healthState} />
    </header>
  )
}

export default PageHeader
