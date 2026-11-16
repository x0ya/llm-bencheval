export type CardState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "done"; text: string; seconds: number }
  | { status: "error"; message: string }

export type AskResult =
  | { ok: true; text: string; seconds: number }
  | { ok: false; error: string }