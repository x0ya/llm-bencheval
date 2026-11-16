import ModelCard from "./ModelCard"
import "./App.css"

const MODELS = ["gemini", "chatgpt", "claude", "deepseek", "llama"]

function App() {
  return (
    <div className="page">
      <h1>LLM Compare</h1>
      <div className="grid">
        {MODELS.map((name) => (
          <ModelCard key={name} name={name} text={"Fake answer from " + name} />
        ))}
      </div>
    </div>
  )
}

export default App