import { useEffect, useState } from 'react'
import { fetchRepos, searchIssues, type SearchFilters, type SearchResult } from './api'
import SearchForm from './components/SearchForm'
import ResultCard from './components/ResultCard'

function App() {
  const [repos, setRepos] = useState<string[]>([])
  // null means "hasn't searched yet", which is different from "searched and found nothing"
  const [results, setResults] = useState<SearchResult[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  // Runs once when the page first loads: fill the repo dropdown
  useEffect(() => {
    fetchRepos()
      .then(setRepos)
      .catch(() => {}) // the dropdown keeps just "All repos"; search still works without it
  }, [])

  async function handleSearch(query: string, filters: SearchFilters) {
    setError(null)
    try {
      setResults(await searchIssues(query, filters))
    } catch {
      setError('Search failed. Is the API running on port 8000?')
    }
  }

  return (
    <main>
      <h1>Déjà Bug</h1>
      <p>Have I seen this bug before?</p>

      <SearchForm repos={repos} onSearch={handleSearch} />

      {error && <p className="error">{error}</p>}

      {results && (
        <ul className="results">
          {results.map((result) => (
            <ResultCard key={`${result.repo}#${result.number}`} result={result} />
          ))}
        </ul>
      )}
    </main>
  )
}

export default App
