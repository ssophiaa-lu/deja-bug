// Where the backend lives. Set VITE_API_URL when deploying; defaults to the local API.
const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function fetchRepos(): Promise<string[]> {
  const response = await fetch(`${API_URL}/repos`)
  if (!response.ok) {
    throw new Error(`GET /repos failed with status ${response.status}`)
  }
  const data: { repos: string[] } = await response.json()
  return data.repos
}
