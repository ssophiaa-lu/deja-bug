import { useEffect, useState } from 'react'
import { fetchRepos, searchIssues, type SearchFilters, type SearchResult } from './api'
import SearchForm from './components/SearchForm'
import ResultCard from './components/ResultCard'

function App() {
  const [repos, setRepos] = useState<string[]>([])
  // null means "hasn't searched yet", which is different from "searched and found nothing"
  const [results, setResults] = useState<SearchResult[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  // Runs once when the page first loads: fill the repo dropdown
  useEffect(() => {
    fetchRepos()
      .then(setRepos)
      .catch(() => {}) // the dropdown keeps just "All repos"; search still works without it
  }, [])

  // Old results stay on screen while the new search loads, so the page doesn't flash empty
  async function handleSearch(query: string, filters: SearchFilters) {
    setError(null)
    setLoading(true)
    try {
      setResults(await searchIssues(query, filters))
    } catch (err) {
      setResults(null) // don't leave old results looking like answers to the new search
      setError(err instanceof Error ? err.message : 'Something went wrong.')
    } finally {
      setLoading(false) // runs whether the search worked or failed
    }
  }

  let statusMessage = ''
  if (results && results.length === 0) {
    statusMessage = 'No matching issues. Try describing the problem differently, or remove a filter.'
  } else if (results) {
    statusMessage = results.length === 1 ? '1 result' : `${results.length} results`
  }

  return (
    <main>
      <header className="header">
        <h1>Déjà Bug</h1>
        <p className="tagline">Have I seen this bug before?</p>
        <p className="intro">
          Searches 3,000+ GitHub issues from popular open-source projects by meaning, not keywords, so an
          issue worded differently from yours still turns up.
        </p>
      </header>

      <SearchForm repos={repos} loading={loading} showExamples={results === null} onSearch={handleSearch} />

      {/* aria-live: screen readers announce these messages when they change */}
      <p className="status" aria-live="polite">
        {statusMessage}
      </p>
      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}

      {results && (
        <ul className="results">
          {results.map((result) => (
            <ResultCard key={`${result.repo}#${result.number}`} result={result} />
          ))}
        </ul>
      )}

      <footer className="footer">
        <a href="https://github.com/ssophiaa-lu/deja-bug" target="_blank" rel="noopener noreferrer">
          Source on GitHub
        </a>
      </footer>
    </main>
  )
}

export default App
