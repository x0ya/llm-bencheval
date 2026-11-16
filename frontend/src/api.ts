import type { AskResult } from "./types"

export async function askModel(
  model: string,
  prompt: string,
  maxTokens = 500
): Promise<AskResult> {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), 70000)

  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model, prompt, max_tokens: maxTokens }),
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