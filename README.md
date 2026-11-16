# LLM-BenchEval

A framework to ask several LLMs the same question under the same conditions,
show their answers side by side with the web sources each one cited, and
(later) score them for accuracy, factuality, consistency and response time.

Models compared: Gemini, ChatGPT, Claude, DeepSeek, Llama. All five are called
through one OpenRouter key. Web sources come from Tavily.

## Setup

    git clone <repo-url>
    cd llm-bencheval
    python3 -m venv venv
    source venv/bin/activate (run every session)
    pip install -r requirements.txt
    cp .env.example .env
    nano .env

In `.env`, add your own keys after the `=` signs:

    OPENROUTER_API_KEY=
    TAVILY_API_KEY=

In nano, save with Ctrl+O then Enter, and exit with Ctrl+X. Never commit this file.

## Run the multi-model demo (always from the project root)

    python3 src/check_keys.py
    python3 src/cli.py

Type a question. The program searches the web once, gives the same sources to
all five models, runs them in parallel, and prints each answer with its
response time, token count and the sources that model cited.

To test without spending credit, run with fake answers:

    MOCK=1 python3 src/cli.py

## How it works

1. search.py: Tavily returns the top web pages for the question.
2. models.py: ask_model(label, prompt) sends the same prompt to one model.
3. cli.py: runs all five in parallel, then reads the [1], [2] citations in
   each answer and prints the matching links.

Note: the program shows which sources each model cited, not whether the page
actually supports the claim. Checking that is part of the planned evaluation.

## Benchmark pipeline (separate, Gemini only for now)

    python3 src/collect.py
    python3 src/score.py
    python3 src/show.py

## Files

- src/models.py: model list and ask_model
- src/search.py: web search and prompt builder
- src/cli.py: terminal demo
- src/collect.py, score.py, show.py: benchmark pipeline
- data/questions.json: question set with answer keys
- data/responses.jsonl: saved model answers
- data/manual_scores.csv: hand marks for open-ended answers
- data/scores.csv: computed scores (rewritten by score.py)

## Notes

Developed with Python 3.14 on WSL. Model names change quickly; check the
OpenRouter model list before running.
