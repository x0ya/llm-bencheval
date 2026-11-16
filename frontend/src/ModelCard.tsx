import type { CardState } from "./types";
import ReactMarkdown from "react-markdown";

type ModelCardProps = {
  name: string;
  state: CardState;
};

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
          <div className="answer">
            <ReactMarkdown
              components={{
                a: ({ href, children }) => (
                  <a href={href} target="_blank" rel="noopener noreferrer">
                    {children}
                  </a>
                ),
              }}
            >
              {state.text}
            </ReactMarkdown>
          </div>
          <p className="meta">{state.seconds} s</p>
        </>
      )}

      {state.status === "error" && (
        <p className="error">Error: {state.message}</p>
      )}
    </div>
  );
}

export default ModelCard;
