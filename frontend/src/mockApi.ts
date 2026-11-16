import type { AskResult } from "./types"

export function fakeAsk(name: string, prompt: string): Promise<AskResult> {
  return new Promise((resolve) => {
    const delay = 500 + Math.random() * 2500
    setTimeout(() => {
      if (Math.random() < 0.2) {
        resolve({ ok: false, error: "fake failure" })
      } else {
        resolve({
          ok: true,
          text: "[mock " + name + "] You said: " + prompt,
          seconds: Math.round(delay / 10) / 100,
        })
      }
    }, delay)
  })
}