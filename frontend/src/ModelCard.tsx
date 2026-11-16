import type { CardState } from "./types"

type ModelCardProps = {
  name: string
  state: CardState
}

function ModelCard({ name, state }: ModelCardProps) {
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
          <p className="answer">{state.text}</p>
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