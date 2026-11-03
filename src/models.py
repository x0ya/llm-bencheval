import os
import random
import time

from dotenv import load_dotenv
from openai import OpenAI, APIStatusError

load_dotenv()

MOCK = os.environ.get("MOCK") == "1"
TIMEOUT = 60  # seconds before we give up on a model

# The menu: label -> exact OpenRouter model name
MODELS = {
    "gemini":   "google/gemini-3.5-flash-lite",
    "chatgpt":  "openai/gpt-6-luna",
    "claude":   "anthropic/claude-haiku-4.5",
    "deepseek": "deepseek/deepseek-v4.1-flash",
    "llama":    "meta-llama/llama-3.1-8b-instruct",
}


class OutOfCreditError(Exception):
    pass


_client = None


def get_client():
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=os.environ["OPENROUTER_API_KEY"],
            base_url="https://openrouter.ai/api/v1",
            timeout=TIMEOUT,
        )
    return _client


def ask_model(label, prompt, max_tokens=500):
    if label not in MODELS:
        raise ValueError("unknown model: " + label)

    if MOCK:
        time.sleep(random.uniform(0.5, 3))
        if random.random() < 0.1:
            raise RuntimeError("fake failure")
        return {"text": "[mock " + label + "] You said: " + prompt,
                "seconds": 1.0, "tokens": 0}

    start = time.time()
    extra = {}
    if label == "deepseek":
        extra = {"reasoning": {"enabled": False}}

    start = time.time()
    try:
        reply = get_client().chat.completions.create(
            model=MODELS[label],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            extra_body=extra,
        )
    except APIStatusError as e:
        msg = str(e).lower()
        if e.status_code == 402 or "credit" in msg or "balance" in msg:
            raise OutOfCreditError("OpenRouter is out of credit")
        raise

    usage = reply.usage
    return {
        "text": reply.choices[0].message.content or "",
        "seconds": round(time.time() - start, 2),
        "tokens": usage.total_tokens if usage else 0,
    }


if __name__ == "__main__":
    for label in MODELS:
        try:
            result = ask_model(label, "Reply with just the word: ready", max_tokens=50)
            print(label, "-> OK:", result)
        except OutOfCreditError as e:
            print(label, "-> STOP:", e)
            break
        except Exception as e:
            print(label, "-> FAIL:", str(e)[:200])
