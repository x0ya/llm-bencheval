import json
import os
import sys
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL_NAME = "gemini-3.5-flash-lite"   # from list_models.py, without "models/"
MODEL_LABEL = "gemini"
OUT_FILE = "data/responses.jsonl"
RUNS = 1            # raise to 3 for the real experiment
PAUSE = 7           # seconds between calls
MAX_RETRIES = 4


def build_prompt(q):
    return "Answer the following question as accurately as you can.\n\nQuestion: " + q


def ask_gemini(question):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            start = time.time()
            reply = client.models.generate_content(
                model=MODEL_NAME,
                contents=build_prompt(question),
                config=types.GenerateContentConfig(temperature=0),
            )
            seconds = time.time() - start
            return reply.text, seconds
        except errors.APIError as e:
            if e.code == 429 and attempt < MAX_RETRIES:
                wait = 30 * attempt
                print("rate limited, waiting", wait,
                      "seconds (attempt", attempt, ")")
                time.sleep(wait)
            else:
                raise


def load_done():
    done = set()
    if os.path.exists(OUT_FILE):
        with open(OUT_FILE) as f:
            for line in f:
                row = json.loads(line)
                done.add((row["id"], row["model"], row.get("run", 1)))
    return done


def main():
    with open("data/questions.json") as f:
        questions = json.load(f)

    done = load_done()

    for run in range(1, RUNS + 1):
        for item in questions:
            key = (item["id"], MODEL_LABEL, run)
            if key in done:
                print(item["id"], "run", run, "already done, skipping")
                continue

            try:
                text, seconds = ask_gemini(item["question"])
            except errors.APIError as e:
                print("Stopped at", item["id"], "run", run, "-", e)
                print("Progress is saved. Run the script again later.")
                sys.exit(1)

            row = {
                "id": item["id"],
                "model": MODEL_LABEL,
                "run": run,
                "response": text,
                "response_time": round(seconds, 2),
            }

            with open(OUT_FILE, "a") as f:
                f.write(json.dumps(row) + "\n")

            print(item["id"], "run", run, "done")
            time.sleep(PAUSE)


main()
