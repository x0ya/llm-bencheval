import { useState } from "react"
import ModelCard from "./ModelCard"
import { fakeAsk } from "./mockApi"
import type { CardState } from "./types"
import "./App.css"
import { askModel } from "./api"

const MODELS = ["gemini", "chatgpt", "claude", "deepseek", "llama"]

const USE_MOCK = false
const ask = USE_MOCK ? fakeAsk : askModel

function idleResults(): Record<string, CardState> {
  const r: Record<string, CardState> = {}
  for (const name of MODELS) r[name] = { status: "idle" }
  return r
}

function App() {
  const [prompt, setPrompt] = useState("")
  const [results, setResults] = useState<Record<string, CardState>>(idleResults())

  const busy = Object.values(results).some((r) => r.status === "loading")

  function setCard(name: string, state: CardState) {
    setResults((prev) => ({ ...prev, [name]: state }))
  }

  function handleSend() {
    const text = prompt.trim()
    if (text === "" || busy) return

    const loading: Record<string, CardState> = {}
    for (const name of MODELS) loading[name] = { status: "loading" }
    setResults(loading)

    MODELS.forEach((name) => {
      ask(name, text).then((res) => {
        if (res.ok) {
          setCard(name, { status: "done", text: res.text, seconds: res.seconds })
        } else {
          setCard(name, { status: "error", message: res.error })
        }
      })
    })
  }

  return (
    <div className="page">
      <h1>LLM Compare</h1>

      <div className="prompt-row">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Type a prompt..."
          rows={3}
        />
        <button onClick={handleSend} disabled={busy}>
          {busy ? "Working..." : "Send"}
        </button>
      </div>

      <div className="grid">
        {MODELS.map((name) => (
          <ModelCard key={name} name={name} state={results[name]} />
        ))}
      </div>
    </div>
  )
}

export default App