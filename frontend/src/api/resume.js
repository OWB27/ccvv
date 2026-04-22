const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function parseResumePdf(file) {
  return uploadResumeFile('/api/resumes/parse', file)
}

export async function extractResumeInfo(file) {
  return uploadResumeFile('/api/resumes/extract', file)
}

export async function matchResumeWithJd(file, jdText) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('jd_text', jdText)

  const response = await fetch(`${API_BASE_URL}/api/resumes/match`, {
    method: 'POST',
    body: formData,
  })

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    throw new Error(data?.detail || `Resume match failed with status ${response.status}`)
  }

  return data
}

async function uploadResumeFile(path, file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST',
    body: formData,
  })

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    throw new Error(data?.detail || `PDF parse failed with status ${response.status}`)
  }

  return data
}
