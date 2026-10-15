import { useEffect, useState } from 'react'
import { fetchRepos } from './api'

function App() {
  const [repos, setRepos] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)

  // Runs once when the page first loads: ask the API which repos exist
  useEffect(() => {
    fetchRepos()
      .then(setRepos)
      .catch(() => setError("Couldn't reach the API. Is it running on port 8000?"))
  }, [])

  return (
    <main>
      <h1>Déjà Bug</h1>
      <p>Have I seen this bug before?</p>

      {error ? (
        <p className="error">{error}</p>
      ) : (
        <ul>
          {repos.map((repo) => (
            <li key={repo}>{repo}</li>
          ))}
        </ul>
      )}
    </main>
  )
}

export default App
