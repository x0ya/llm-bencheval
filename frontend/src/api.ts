import type { AskResult, Source } from "./types"

export async function searchWeb(prompt: string): Promise<Source[]> {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), 30000)

  try {
    const res = await fetch("/api/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
      signal: controller.signal,
    })
    const data = await res.json()
    return Array.isArray(data.sources) ? data.sources : []
  } catch {
    return []
  } finally {
    clearTimeout(timer)
  }
}

export async function askModel(
  model: string,
  prompt: string,
  maxTokens = 500,
  sources: Source[] = []
): Promise<AskResult> {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), 70000)

  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model, prompt, max_tokens: maxTokens, sources }),
      signal: controller.signal,
    })
    const data = await res.json()

    if (data.ok) {
      return { ok: true, text: data.text, seconds: data.seconds }
    }
    return { ok: false, error: data.error ?? "unknown error" }
  } catch (e) {
    return {
      ok: false,
      error: e instanceof Error ? e.message : "network error",
    }
  } finally {
    clearTimeout(timer)
  }
}