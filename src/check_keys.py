import os
from dotenv import load_dotenv

load_dotenv()

NAMES = [
    "GEMINI_API_KEY",
    "OPENROUTER_API_KEY"
]

for name in NAMES:
    value = os.environ.get(name)
    if not value:
        print(name, "-> MISSING")
        continue
    problems = []
    if value != value.strip():
        problems.append("has extra spaces")
    if value[0] in "\"'":
        problems.append("starts with a quote mark")
    note = " (" + ", ".join(problems) + ")" if problems else ""
    print(name, "-> set,", len(value), "characters" + note)
