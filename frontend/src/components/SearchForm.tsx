import { useState, type FormEvent } from 'react'

type Props = {
  onSearch: (query: string) => void
}

function SearchForm({ onSearch }: Props) {
  const [query, setQuery] = useState('')

  function handleSubmit(event: FormEvent) {
    event.preventDefault() // stop the browser from reloading the page, the default for forms
    onSearch(query.trim())
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
      <button type="submit">Search</button>
    </form>
  )
}

export default SearchForm
