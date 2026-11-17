# LLM-BenchEval

A framework to ask several LLMs the same question under the same conditions,
show their answers side by side with the web sources each one cited, and
(later) score them for accuracy, factuality, consistency and response time.

Models compared: Gemini, ChatGPT, Claude, DeepSeek, Llama. All five are called
through one OpenRouter key. Web sources come from Tavily.

There are two ways to use it:

1. A web app (React frontend and Flask backend): type a prompt, get five
   answers side by side, optionally with shared web sources.
2. A terminal demo and a benchmark pipeline (Python scripts).

## Requirements

- Python 3 (developed with 3.14) and Node.js 20 or newer
- Linux or WSL. Keep the project on the Linux side (for example ~/llm-bencheval)
  and not under /mnt/c or /mnt/d, because git can get corrupted on Windows drives.

## Setup

    git clone <repo-url>
    cd llm-bencheval
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    nano .env

Run the `source venv/bin/activate` line in every new terminal session.

In `.env`, add your own keys after the `=` signs:

    OPENROUTER_API_KEY=
    TAVILY_API_KEY=

Only the benchmark script collect.py also needs GEMINI_API_KEY (Google AI Studio).

In nano, save with Ctrl+O then Enter, and exit with Ctrl+X. Never commit this file.

Install the frontend libraries once:

    cd frontend
    npm install
    cd ..

## Run the web app (two terminals, both from the project root)

Terminal 1, the backend (activate the venv first):

    python3 src/app.py

Terminal 2, the frontend:

    cd frontend
    npm run dev

Open the address Vite prints (usually http://localhost:5173).

To test without spending credit, start the backend with fake answers:

    MOCK=1 python3 src/app.py

How to use it:

- Type a prompt and press Send. Five cards fill in independently, each with
  its own response time. A failing model shows an error in its own card only.
- Tick "Search the web and give every model the same sources" to run one web
  search first. All five models receive the same sources, and a Sources list
  appears under the cards.
- Where a model cites [1], [2] and so on, the page turns the marker into a
  small chip showing the site name. Hover the chip to see the page title and a
  snippet. A marker that points to a source that does not exist is left as text.

## Run the terminal demo

    python3 src/check_keys.py
    python3 src/cli.py

Type a question. The program searches the web once, gives the same sources to
all five models, runs them in parallel, and prints each answer with its
response time, token count and the sources that model cited.

To test without spending credit:

    MOCK=1 python3 src/cli.py

## How it works

1. search.py: Tavily returns the top web pages for the question.
2. models.py: ask_model(label, prompt) sends the same prompt to one model.
3. app.py: a Flask server with three endpoints (below).
4. The React page calls /api/search once, then sends five /api/ask requests in
   parallel with the same sources, so search is not repeated per model.
5. cli.py does the same job in the terminal.

Vite forwards every request that starts with /api to the Flask server on
port 5000 (see frontend/vite.config.ts), so the page never needs the keys.

## API

    GET  /api/models
    POST /api/search  { "prompt": "..." }
         -> { "ok": true, "sources": [ { "title", "url", "snippet" } ] }
    POST /api/ask     { "model": "claude", "prompt": "...", "max_tokens": 500, "sources": [ ... ] }
         -> { "ok": true, "text": "...", "seconds": 1.4, "tokens": 212 }
         or { "ok": false, "error": "..." }

The server limits prompt length to 2000 characters and max_tokens to 1500.

Note: the program shows which sources each model cited, not whether the page
actually supports the claim. Checking that is part of the planned evaluation.

## Benchmark pipeline (separate, Gemini only for now)

    python3 src/collect.py
    python3 src/score.py
    python3 src/show.py

## Files

- src/models.py: model list and ask_model
- src/search.py: web search and prompt builder
- src/app.py: Flask backend for the web app
- src/cli.py: terminal demo
- src/check_keys.py: shows which keys are loaded, without printing them
- src/collect.py, score.py, show.py: benchmark pipeline
- frontend/src/App.tsx: page layout, prompt box, Search toggle
- frontend/src/ModelCard.tsx: one answer card (idle, loading, done, error)
- frontend/src/Citation.tsx: the hover chip for a cited source
- frontend/src/SourcesList.tsx: the shared Sources list
- frontend/src/api.ts, types.ts: calls to the backend and shared types
- data/questions.json: question set with answer keys
- data/responses.jsonl: saved model answers
- data/manual_scores.csv: hand marks for open-ended answers
- data/scores.csv: computed scores (rewritten by score.py)

## Safety

- Keys live only in .env on the backend. They never go into the frontend or git.
- The backend runs in debug mode with open CORS. It is for local use only.
  Do not put it on the internet as it is.
- Model and web text is shown as markdown without raw HTML, and only http and
  https links are shown, opened in a new tab.

## Troubleshooting

- "source is not recognized": you are in PowerShell. Type `wsl` first.
- "ModuleNotFoundError": the venv is not active. Run `source venv/bin/activate`.
- Every card says "Failed to fetch": the backend is not running, or Vite was
  not restarted after editing vite.config.ts.
- A card says "out of credit": the OpenRouter balance is empty.
- A line starting with > in the terminal means a quote was left open. Press Ctrl+C.

## Status

Done: benchmark pipeline for Gemini, terminal demo, web app with five parallel
answers, markdown rendering, shared web sources and citation chips.

Planned: settings bar (model checkboxes, max tokens), saved history, showing
token counts on the cards, and the evaluation (accuracy, factuality,
consistency, citation accuracy).

## Notes

Developed with Python 3.14 on WSL. Model names change quickly; check the
OpenRouter model list before running.
