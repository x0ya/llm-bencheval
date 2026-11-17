import ReactMarkdown from "react-markdown"
import Citation from "./Citation"
import type { CardState, Source } from "./types"

type ModelCardProps = {
  name: string
  state: CardState
  sources: Source[]
}

function linkCitations(text: string, count: number): string {
  if (count === 0) return text
  return text.replace(
    /\[(\d+(?:\s*,\s*\d+)*)\](?!\()/g,
    (whole, group: string) => {
      const nums = group.split(",").map((p) => parseInt(p.trim(), 10))
      if (nums.some((n) => n < 1 || n > count)) return whole
      return nums.map((n) => "[" + n + "](#cite-" + n + ")").join(" ")
    }
  )
}

function ModelCard({ name, state, sources }: ModelCardProps) {
  return (
    <div className="card">
      <h2>{name}</h2>

      {state.status === "idle" && <p className="muted">No answer yet.</p>}

      {state.status === "loading" && (
        <p className="muted">
          <span className="spinner" /> Waiting...
        </p>
      )}

      {state.status === "done" && (
        <>
          <div className="answer">
            <ReactMarkdown
              components={{
                a: ({ href, children }) => {
                  if (href && href.startsWith("#cite-")) {
                    const n = parseInt(href.slice(6), 10)
                    const source = sources[n - 1]
                    if (source) return <Citation index={n} source={source} />
                    return <>{children}</>
                  }
                  return (
                    <a href={href} target="_blank" rel="noopener noreferrer">
                      {children}
                    </a>
                  )
                },
              }}
            >
              {linkCitations(state.text, sources.length)}
            </ReactMarkdown>
          </div>
          <p className="meta">{state.seconds} s</p>
        </>
      )}

      {state.status === "error" && (
        <p className="error">Error: {state.message}</p>
      )}
    </div>
  )
}

export default ModelCard