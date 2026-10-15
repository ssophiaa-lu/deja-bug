import { useState } from 'react'
import { searchIssues, type SearchResult } from './api'
import SearchForm from './components/SearchForm'
import ResultCard from './components/ResultCard'

function App() {
  // null means "hasn't searched yet", which is different from "searched and found nothing"
  const [results, setResults] = useState<SearchResult[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function handleSearch(query: string) {
    setError(null)
    try {
      setResults(await searchIssues(query))
    } catch {
      setError('Search failed. Is the API running on port 8000?')
    }
  }

  return (
    <main>
      <h1>Déjà Bug</h1>
      <p>Have I seen this bug before?</p>

      <SearchForm onSearch={handleSearch} />

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
