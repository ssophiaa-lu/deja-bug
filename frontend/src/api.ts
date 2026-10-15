// Where the backend lives. Set VITE_API_URL when deploying; defaults to the local API.
const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

// Mirrors SearchResult in api/main.py
export type SearchResult = {
  repo: string
  number: number
  title: string
  state: string
  url: string
  labels: string[]
  preview: string
  score: number
}

export async function fetchRepos(): Promise<string[]> {
  const response = await fetch(`${API_URL}/repos`)
  if (!response.ok) {
    throw new Error(`GET /repos failed with status ${response.status}`)
  }
  const data: { repos: string[] } = await response.json()
  return data.repos
}

// Same choices as the API's Literal["open", "closed"]
export type IssueState = 'open' | 'closed'

// Leave a filter out (undefined) to search everything
export type SearchFilters = {
  repo?: string
  state?: IssueState
}

export async function searchIssues(query: string, filters: SearchFilters = {}): Promise<SearchResult[]> {
  const response = await fetch(`${API_URL}/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    // JSON.stringify drops undefined fields, so unset filters aren't sent at all
    body: JSON.stringify({ query, ...filters }),
  })
  if (!response.ok) {
    throw new Error(`POST /search failed with status ${response.status}`)
  }
  const data: { results: SearchResult[] } = await response.json()
  return data.results
}
