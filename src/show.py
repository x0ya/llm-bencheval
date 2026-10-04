import json

with open("data/questions.json") as f:
    questions = {q["id"]: q for q in json.load(f)}

with open("data/responses.jsonl") as f:
    for line in f:
        row = json.loads(line)
        q = questions[row["id"]]
        print("=" * 60)
        print(row["id"], "|", row["model"], "| run",
              row["run"], "|", row["response_time"], "s")
        print("Q:", q["question"])
        print("Expected:", q["answer"])
        print("Got:", row["response"])
