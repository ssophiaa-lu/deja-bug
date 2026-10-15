import { useState, type FormEvent } from 'react'
import type { IssueState, SearchFilters } from '../api'

// Checked against the real data: each finds relevant issues in a different repo
const EXAMPLE_QUERIES = [
  'request timeout not respected',
  'data is undefined on first render',
  'hydration mismatch error',
]

type Props = {
  repos: string[]
  loading: boolean
  showExamples: boolean
  onSearch: (query: string, filters: SearchFilters) => void
}

function SearchForm({ repos, loading, showExamples, onSearch }: Props) {
  const [query, setQuery] = useState('')
  const [repo, setRepo] = useState('') // '' means all repos
  const [state, setState] = useState<IssueState | ''>('') // '' means open and closed

  // '' becomes undefined, so "All repos" sends no repo instead of an invalid "" the API would reject
  function currentFilters(): SearchFilters {
    return { repo: repo || undefined, state: state || undefined }
  }

  function handleSubmit(event: FormEvent) {
    event.preventDefault() // stop the browser from reloading the page, the default for forms
    onSearch(query.trim(), currentFilters())
  }

  function runExample(example: string) {
    setQuery(example) // show the example in the box, so it's clear what was searched
    onSearch(example, currentFilters())
  }

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <textarea
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder="Paste your error or describe the bug"
        rows={3}
        required
        minLength={3} // same rule as the API, so short queries are caught before sending
        maxLength={2000}
      />
      <div className="search-controls">
        <select value={repo} onChange={(event) => setRepo(event.target.value)} aria-label="Repository">
          <option value="">All repos</option>
          {repos.map((name) => (
            <option key={name} value={name}>
              {name}
            </option>
          ))}
        </select>
        <select
          value={state}
          onChange={(event) => setState(event.target.value as IssueState | '')}
          aria-label="Issue state"
        >
          <option value="">Open and closed</option>
          <option value="open">Open only</option>
          <option value="closed">Closed only</option>
        </select>
        {/* Disabled while loading, so double-clicks can't start two racing searches */}
        <button type="submit" className="search-button" disabled={loading}>
          {loading ? 'Searching…' : 'Search'}
        </button>
      </div>

      {showExamples && (
        <div className="examples">
          <span>Try:</span>
          {EXAMPLE_QUERIES.map((example) => (
            <button
              key={example}
              type="button" // type="button" so clicking doesn't also submit the form
              className="example"
              disabled={loading}
              onClick={() => runExample(example)}
            >
              {example}
            </button>
          ))}
        </div>
      )}
    </form>
  )
}

export default SearchForm
