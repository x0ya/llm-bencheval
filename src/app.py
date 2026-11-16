import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from models import MODELS, ask_model, OutOfCreditError
from search import search_web, build_prompt

MOCK = os.environ.get("MOCK") == "1"
MAX_PROMPT_CHARS = 2000
MAX_TOKENS_LIMIT = 1500

app = Flask(__name__)
CORS(app)  # local development only


def fake_sources(prompt):
    return [
        {"title": "Mock source 1", "url": "https://example.com/1",
         "snippet": "Fake snippet about " + prompt[:40]},
        {"title": "Mock source 2", "url": "https://example.com/2",
         "snippet": "Another fake snippet"},
    ]


def clean_sources(raw):
    cleaned = []
    if not isinstance(raw, list):
        return cleaned
    for s in raw[:5]:
        if isinstance(s, dict):
            url = str(s.get("url", ""))[:500]
            if not url.startswith(("http://", "https://")):
                continue
            cleaned.append({
                "title": str(s.get("title", ""))[:200],
                "url": url,
                "snippet": str(s.get("snippet", ""))[:500],
            })
    return cleaned


@app.get("/api/models")
def list_models():
    return jsonify({"models": list(MODELS.keys())})


@app.post("/api/search")
def api_search():
    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt or len(prompt) > MAX_PROMPT_CHARS:
        return jsonify({"ok": False, "error": "bad prompt", "sources": []}), 400
    if MOCK:
        return jsonify({"ok": True, "sources": fake_sources(prompt)})
    try:
        sources = search_web(prompt)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)[:200], "sources": []})
    return jsonify({"ok": True, "sources": sources})


@app.post("/api/ask")
def api_ask():
    data = request.get_json(silent=True) or {}
    label = data.get("model")
    prompt = (data.get("prompt") or "").strip()
    sources = clean_sources(data.get("sources"))
    max_tokens = data.get("max_tokens", 500)

    if label not in MODELS:
        return jsonify({"ok": False, "error": "unknown model"}), 400
    if not prompt or len(prompt) > MAX_PROMPT_CHARS:
        return jsonify({"ok": False, "error": "bad prompt"}), 400
    try:
        max_tokens = max(1, min(int(max_tokens), MAX_TOKENS_LIMIT))
    except (TypeError, ValueError):
        max_tokens = 500

    final_prompt = build_prompt(prompt, sources)

    try:
        result = ask_model(label, final_prompt, max_tokens)
    except OutOfCreditError:
        return jsonify({"ok": False, "error": "out of credit"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)[:200]})

    return jsonify({
        "ok": True,
        "text": result["text"],
        "seconds": result["seconds"],
        "tokens": result["tokens"],
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)
