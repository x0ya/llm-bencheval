
# LLM-BenchEval

Pipeline to ask several LLMs the same questions, save the answers and score them.

## Setup

    git clone <repo-url>
    cd llm-bencheval
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env

Open `.env` and add your own API keys. Never commit this file.
    nano .env

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
EOF
