import type { SearchResult } from '../api'

type Props = {
  result: SearchResult
}

function ResultCard({ result }: Props) {
  return (
    <li className="result-card">
      <div className="result-meta">
        <span className={`badge badge-${result.state}`}>{result.state === 'open' ? 'Open' : 'Closed'}</span>
        <span>
          {result.repo} #{result.number}
        </span>
        {result.labels.map((label) => (
          <span key={label} className="label">
            {label}
          </span>
        ))}
      </div>
      {/* noopener noreferrer: the GitHub tab can't control or see this page */}
      <a href={result.url} target="_blank" rel="noopener noreferrer" className="result-title">
        {result.title}
      </a>
      <p className="result-preview">{result.preview}</p>
    </li>
  )
}

export default ResultCard
