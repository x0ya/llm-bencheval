import { useState } from "react"
import ModelCard from "./ModelCard"
import "./App.css"

const MODELS = ["gemini", "chatgpt", "claude", "deepseek", "llama"]

function App() {
  const [prompt, setPrompt] = useState("")
  const [answers, setAnswers] = useState<Record<string, string>>({})

  function handleSend() {
    if (prompt.trim() === "") return
    const next: Record<string, string> = {}
    for (const name of MODELS) {
      next[name] = "[mock " + name + "] You said: " + prompt
    }
    setAnswers(next)
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
        <button onClick={handleSend}>Send</button>
      </div>

      <div className="grid">
        {MODELS.map((name) => (
          <ModelCard key={name} name={name} text={answers[name] ?? ""} />
        ))}
      </div>
    </div>
  )
}

export default App