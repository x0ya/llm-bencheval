# LLM-BenchEval

Pipeline to ask several LLMs the same questions, save the answers and score them.

## Setup

    git clone <repo-url>
    cd llm-bencheval
    python3 -m venv venv
    source venv/bin/activate (run every session)
    pip install -r requirements.txt
    cp .env.example .env
    nano .env

In `.env`, add your own API keys after the `=` signs. In nano, save with Ctrl+O then Enter, and exit with Ctrl+X. Never commit this file.

## Run (always from the project root)

    python3 src/check_keys.py
    python3 src/collect.py
    python3 src/score.py
    python3 src/show.py

## Files

- data/questions.json: question set with answer keys
- data/responses.jsonl: saved model answers
- data/manual_scores.csv: hand marks for open-ended answers
- data/scores.csv: computed scores (rewritten by score.py)

## Notes

Developed with Python 3.14 on WSL. Currently only Gemini is wired up in collect.py.
