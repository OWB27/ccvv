const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function fetchHealthStatus() {
  const response = await fetch(`${API_BASE_URL}/api/health`)

  if (!response.ok) {
    throw new Error(`Health check failed with status ${response.status}`)
  }

  return response.json()
}

