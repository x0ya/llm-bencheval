import os
import requests
from dotenv import load_dotenv

load_dotenv()

r = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"]},
    timeout=30,
)
for m in r.json()["data"]:
    if "gemini" in m["id"] and "flash" in m["id"]:
        print(m["id"], m["pricing"])
