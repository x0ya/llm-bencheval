import type { Source } from "./types"

type SourcesListProps = {
  sources: Source[]
}

function SourcesList({ sources }: SourcesListProps) {
  if (sources.length === 0) return null

  return (
    <div className="sources">
      <h2>Sources</h2>
      <ol>
        {sources.map((s) => {
          const safe = s.url.startsWith("http://") || s.url.startsWith("https://")
          return (
            <li key={s.url}>
              {safe ? (
                <a href={s.url} target="_blank" rel="noopener noreferrer">
                  {s.title || s.url}
                </a>
              ) : (
                <span>{s.title}</span>
              )}
            </li>
          )
        })}
      </ol>
    </div>
  )
}

export default SourcesList