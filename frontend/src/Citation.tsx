import type { Source } from "./types"

function domainOf(url: string): string {
  try {
    return new URL(url).hostname.replace(/^www\./, "")
  } catch {
    return url
  }
}

function isSafe(url: string): boolean {
  return url.startsWith("http://") || url.startsWith("https://")
}

type CitationProps = {
  index: number
  source: Source
}

function Citation({ index, source }: CitationProps) {
  if (!isSafe(source.url)) return <span>[{index}]</span>
  const domain = domainOf(source.url)

  return (
    <span className="cite">
      <a
        className="cite-chip"
        href={source.url}
        target="_blank"
        rel="noopener noreferrer"
      >
        {domain}
      </a>
      <span className="cite-pop">
        <span className="cite-pop-domain">{domain}</span>
        <span className="cite-pop-title">{source.title}</span>
        <span className="cite-pop-snippet">{source.snippet.slice(0, 160)}</span>
      </span>
    </span>
  )
}

export default Citation