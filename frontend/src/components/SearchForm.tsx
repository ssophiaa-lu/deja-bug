import { useState, type FormEvent } from 'react'
import type { IssueState, SearchFilters } from '../api'

type Props = {
  repos: string[]
  onSearch: (query: string, filters: SearchFilters) => void
}

function SearchForm({ repos, onSearch }: Props) {
  const [query, setQuery] = useState('')
  const [repo, setRepo] = useState('') // '' means all repos
  const [state, setState] = useState<IssueState | ''>('') // '' means open and closed

  function handleSubmit(event: FormEvent) {
    event.preventDefault() // stop the browser from reloading the page, the default for forms
    // '' becomes undefined, so "All repos" sends no repo instead of an invalid "" the API would reject
    onSearch(query.trim(), { repo: repo || undefined, state: state || undefined })
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
        <button type="submit">Search</button>
      </div>
    </form>
  )
}

export default SearchForm
