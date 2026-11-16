type ModelCardProps = {
  name: string
  text: string
}

function ModelCard({ name, text }: ModelCardProps) {
  return (
    <div className="card">
      <h2>{name}</h2>
      <p>{text}</p>
    </div>
  )
}

export default ModelCard