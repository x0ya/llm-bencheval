import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic

load_dotenv()

PROMPT = "Reply with just the word: ready"


def test_openai_style(label, key_name, model, base_url=None):
    try:
        client = OpenAI(api_key=os.environ[key_name], base_url=base_url)
        reply = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": PROMPT}],
        )
        print(label, "-> OK:", reply.choices[0].message.content)
    except Exception as e:
        print(label, "-> FAIL:", str(e)[:200])


def test_anthropic(model):
    try:
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        reply = client.messages.create(
            model=model,
            max_tokens=20,
            messages=[{"role": "user", "content": PROMPT}],
        )
        print("claude -> OK:", reply.content[0].text)
    except Exception as e:
        print("claude -> FAIL:", str(e)[:200])


test_openai_style("chatgpt", "OPENAI_API_KEY", "gpt-6-luna")
test_openai_style("deepseek", "DEEPSEEK_API_KEY", "deepseek-flash", "https://api.deepseek.com")
test_anthropic("claude-haiku-4-5-20251001")