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

// Turn an error status into a message a visitor can understand
function searchErrorMessage(status: number): string {
  if (status === 503) return 'Search is temporarily unavailable. Please try again.'
  if (status === 422) return "That search couldn't be processed. Try rewording it."
  return `Something went wrong (error ${status}).`
}

// Throws an Error whose message is ready to show on the page
export async function searchIssues(query: string, filters: SearchFilters = {}): Promise<SearchResult[]> {
  let response: Response
  try {
    response = await fetch(`${API_URL}/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      // JSON.stringify drops undefined fields, so unset filters aren't sent at all
      body: JSON.stringify({ query, ...filters }),
    })
  } catch {
    // fetch only throws when there's no response at all: server down, no internet, or CORS blocked
    throw new Error("Can't reach the Déjà Bug server. Check your connection and try again.")
  }
  if (!response.ok) {
    throw new Error(searchErrorMessage(response.status))
  }
  const data: { results: SearchResult[] } = await response.json()
  return data.results
}
