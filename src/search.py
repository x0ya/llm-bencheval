import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def search_web(query, n=5):
    result = client.search(query, max_results=n)
    sources = []
    for item in result.get("results", []):
        url = item.get("url", "")
        if not url.startswith(("http://", "https://")):
            continue
        sources.append({
            "title": item.get("title", url),
            "url": url,
            "snippet": item.get("content", "")[:500],
        })
    return sources


def build_prompt(prompt, sources):
    if not sources:
        return prompt
    lines = ["Use the sources below to answer. Cite them as [1], [2], etc.", ""]
    for i, s in enumerate(sources, start=1):
        lines.append("[" + str(i) + "] " + s["title"] + ": " + s["snippet"])
    lines.append("")
    lines.append("Question: " + prompt)
    return "\n".join(lines)
