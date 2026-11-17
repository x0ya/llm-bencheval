import { useState } from "react"
import ModelCard from "./ModelCard"
import SourcesList from "./SourcesList"
import { askModel, searchWeb } from "./api"
import type { CardState, Source } from "./types"
import "./App.css"

const MODELS = ["gemini", "chatgpt", "claude", "deepseek", "llama"]

function idleResults(): Record<string, CardState> {
  const r: Record<string, CardState> = {}
  for (const name of MODELS) r[name] = { status: "idle" }
  return r
}

function App() {
  const [prompt, setPrompt] = useState("")
  const [useSearch, setUseSearch] = useState(false)
  const [searching, setSearching] = useState(false)
  const [sources, setSources] = useState<Source[]>([])
  const [searchNote, setSearchNote] = useState("")
  const [results, setResults] = useState<Record<string, CardState>>(idleResults())

  const busy =
    searching || Object.values(results).some((r) => r.status === "loading")

  function setCard(name: string, state: CardState) {
    setResults((prev) => ({ ...prev, [name]: state }))
  }

  async function handleSend() {
    const text = prompt.trim()
    if (text === "" || busy) return

    setSearchNote("")
    let found: Source[] = []

    if (useSearch) {
      setSearching(true)
      found = await searchWeb(text)
      setSearching(false)
      if (found.length === 0) {
        setSearchNote("Search returned no sources, so the models answered without them.")
      }
    }
    setSources(found)

    const loading: Record<string, CardState> = {}
    for (const name of MODELS) loading[name] = { status: "loading" }
    setResults(loading)

    MODELS.forEach((name) => {
      askModel(name, text, 500, found).then((res) => {
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
          {searching ? "Searching..." : busy ? "Working..." : "Send"}
        </button>
      </div>

      <label className="toggle">
        <input
          type="checkbox"
          checked={useSearch}
          onChange={(e) => setUseSearch(e.target.checked)}
        />
        Search the web and give every model the same sources
      </label>
      {searchNote && <p className="muted">{searchNote}</p>}

      <div className="grid">
        {MODELS.map((name) => (
          <ModelCard key={name} name={name} state={results[name]} sources={sources} />
        ))}
      </div>

      <SourcesList sources={sources} />
    </div>
  )
}

export default App